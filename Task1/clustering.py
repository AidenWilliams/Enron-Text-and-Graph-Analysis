from random import randint
from copy import copy
import dependancyManager as dm
import graphDataBuilder as gdb
import webService as ws
from tqdm import tqdm
import io,csv

Vector = list[float]


def dot(A, B):
    return (sum(a*b for a, b in zip(A, B)))


def sim(A: Vector, B:Vector) -> float:
    denom = ((dot(A, A) ** .5) * (dot(B, B) ** .5))
    if denom == 0:
        return 0
    return dot(A, B) / denom


class point:
    parentCluster = None
    data = {}  # data vec
    username = ""

    def __init__(self,dt:dict,user=""):
        self.parentCluster = None
        self.data = dt
        self.username = user


    def similarityTo(self,clust) -> float:
        thisV = []
        clV = []
        for word,weight in self.data.items():
            thisV.append(weight)
            if word in clust.centroid.data:
                clV.append(clust.centroid.data[word])
            else:
                clV.append(0)

        return sim(thisV, clV)

    def assignClosest(self, clusters):
        sims = {}
        for c in clusters:
            sims[c] = self.similarityTo(c)
        topClust = list(dict(sorted(sims.items(), key=lambda item: item[1], reverse=True)).keys())[0]
        indx = clusters.index(topClust)
        # top.
        self.parentCluster = clusters[indx]
        return indx




class cluster:
    centroid = None  # data vec
    points = []

    def __init__(self, centroid:point):
        self.centroid = centroid
        # self.points = points

    def __copy__(self):
        newPtns = []
        for p in list(self.points):
            newPtns.append(p)

        np = cluster(point(self.centroid.data.copy()))
        np.points = newPtns
        return np

    def addPoint(self, pnt):
        newPtns = []
        for p in list(self.points):
            newPtns.append(p)
        newPtns.append(pnt)
        self.points = newPtns


    def reCalc(self):
        totals = {}
        docCount = len(self.points)
        for p in self.points:
            for word,weight in p.data.items():
                if word not in totals:
                    totals[word] = 0
                totals[word]+=weight

        for t,v in totals.items():
            self.centroid.data[t] = v/docCount


class clusterSet:
    clusters = []
    def __init__(self,clusters):
        self.clusters = clusters
    
    def reCalculateCentroids(self):
        newClust = []
        for c in self.clusters:
            c.reCalc()
            newClust.append(c)
        
        return clusterSet(newClust)

    def __copy__(self):
        nc = []
        for c in list(self.clusters):
            nc.append(copy(c))
        return type(self)(nc.copy())

    


    def distanceToOtherSet(self,other) -> float:   #IDK WHAT TO DO HERE
        total = 0
        count = 0
        for cA,cB in zip(self.clusters,other.clusters):
            cav = list(cA.centroid.data.values())
            cbv = list(cB.centroid.data.values())
            total+=sim(cav,cbv)
            count+=1
        return total/count

    def reAssignPoints(self):
        allPts = []
        for c in self.clusters:
            allPts.extend(c.points)
            c.points.clear()
        for p in allPts:
            indx = p.assignClosest(self.clusters)
            self.clusters[indx].addPoint(p)

    # def firstAssignPoints(self,userVecs):
    #     # allPts = userDocs
    #     for userN,vec in tqdm(userVecs.items(),desc='Creating points'):
    #         p = point(vec, user=userN)
    #         # indx = p.assignClosest(self.clusters)
    #         p.assignClosest(self.clusters)
    #         # self.clusters[indx].addPoint(p)

    def firstAssignPoints(self, userVecs):
        # allPts = userDocs
        for userN, vec in tqdm(userVecs.items(), desc='Assgning points'):
            p = point(vec, user=userN)
            indx = p.assignClosest(self.clusters)
            self.clusters[indx].addPoint(p)


def randomInit(userDocs,k):
    init = []
    lng = len(userDocs)

    while(len(init)) < k: #choose k random indices
        ind = randint(0, lng-1)
        if ind not in init:
            init.append(ind)

    initClusters = []
    for x in init:
        # points = list(list(userDocs.values())[x].values())
        data = list(userDocs.values())[x].copy()
        clst = cluster(point(data))
        initClusters.append(clst)
    return initClusters

def buildClusters(userDocs, k:int):
    print('starting clustering')
    lng = len(userDocs)
    if k > lng:
        raise ValueError("K larger than document count!")
        
    
    initClusters = randomInit(userDocs,k)
    currClust = clusterSet(initClusters)
    currClust.firstAssignPoints(userDocs)

    # closest = closestCentr(currClust, userDocs)
    distances = [-1,-1,-1] # if we have same 3 distances in a row, we are done
    epochCount = 0
    while True:
        epochCount+=1
        currClust.reAssignPoints()
        prevClust = copy(currClust)
        currClust = currClust.reCalculateCentroids()

        s = currClust.distanceToOtherSet(prevClust)
        
        distances.pop(0)
        distances.append(s)
        print('\r',distances[-1],end='')

        if s>=0.999 or len(set(distances))<=1:
            print(f'\nDone in {epochCount} epochs!')
            return currClust


def startCluster(k=20,userCount=300):
    uvec = dm.getuvec()
    links = dm.getLinks()
    subkeys = ws.topUsers(links,tc=userCount,chop=False)

    subDic = {key: uvec[key] for key in subkeys if key in uvec}
    print(f'clustering {len(subDic)} users into {k} classes')
    clusters = buildClusters(subDic, k).clusters
    return clusters


def clusterDataToCsv(clusters):
    i = 0
    data = []
    for c in clusters:
        i += 1
        size = len(c.points)                
        data.append({'id': i, 'size': size, 'groupid': 1})


    dest = io.StringIO()
    keys = data[0].keys()

    dict_writer = csv.DictWriter(dest, keys,delimiter=',',lineterminator='\n')
    dict_writer.writeheader()
    dict_writer.writerows(data)

    dest.seek(0)
    return dest.read()


def getTopClusterTerms(clusters,n):
    vecs = {}
    i = 0
    for c in clusters:
        i+=1
        vecs[i] = c.centroid.data
    return gdb.topTerms(vecs,n,chop=False)

# print('final:', clusterDataToCsv(getData(k=1, userCount=10)))

# matching = 0
# count = 0
# for cl in clusters:
#     if len(cl.points)>1:
#         for pt in cl.points:
#             for pt2 in cl.points:
#                 if pt == pt2:
#                     continue
#                 for key in pt.data:
#                     count+=1
#                     if key in pt2.data:
#                         matching+=1
#         break

# print(f'matching: {matching} | %: {matching/count}')
