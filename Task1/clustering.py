from random import randint
import dependancyManager as dm
from copy import copy, deepcopy
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

    def __init__(self,dt:dict):
        self.parentCluster = None
        self.data = dt
    

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

    def assignClosest(self,clusters):
        sims = {}
        for c in clusters:
            sims[c] = self.similarityTo(c)
        topClust = list(dict(sorted(sims.items(), key=lambda item: item[1],reverse=True)).keys())[0]
        indx = clusters.index(topClust)
        # clusters[indx].addPoint(self)
        # points = topClust.points.copy()
        # topClust = Cluster(topClust.centroid.copy())
        # topClust.points = points
        # top.
        self.parentCluster = clusters[indx]
        return indx
        # self.parentCluster.points.append(self)
        # self.parentCluster.addPoint(self)


class Cluster:
    centroid = None  # data vec
    points = []

    def __init__(self, centroid:point):
        self.centroid = centroid
        # self.points = points

    def __copy__(self):
        newPtns = []
        for p in list(self.points):
            newPtns.append(p)
        # newPtns.append(pnt)
        np = Cluster(point(self.centroid.data.copy()))
        np.points = newPtns
        return np

    def addPoint(self,pnt):
        # print('appending')
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
            # total+=sim(cA.data,cB.data)
            count+=1
        return total/count

    # def distanceToPoint(slef,vec):          #IDK WHAT TO DO HERE//needed??
    #     return sim()

    def reAssignPoints(self):
        allPts = []
        for c in self.clusters:
            allPts.extend(c.points)
            c.points.clear()
        for p in allPts:
            indx = p.assignClosest(self.clusters)
            self.clusters[indx].addPoint(p)

    def firstAssignPoints(self,userVecs):
        # allPts = userDocs
        for user,vec in userVecs.items():
            p = point(vec)
            indx = p.assignClosest(self.clusters)
            self.clusters[indx].addPoint(p)
            




# here we will minimise the amount of nodes to calm things down for the clustering!
def filterDocs(userVecs):
    totals = {}
    for user,vec in userVecs.items():
        if user not in totals:
            totals[user] = 0
        totals[user] +=vec
    #return userDocs

    #maybe use top nodes ?

    #rank docs based on something
    #choose top N docs
    # pass


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
        clst = Cluster(point(data))
        initClusters.append(clst)
    return initClusters

def buildClusters(userDocs, k:int):
    print('starting')
    lng = len(userDocs)
    if k > lng:
        ValueError("K larger than document count!")
    
    initClusters = randomInit(userDocs,k)
    currClust = clusterSet(initClusters)
    currClust.firstAssignPoints(userDocs)

    # closest = closestCentr(currClust, userDocs)
    distances = [-1,-1,-1] # if we have same 3 distances in a row, we are done
    while True:
        
        currClust.reAssignPoints()
        prevClust = copy(currClust)
        currClust = currClust.reCalculateCentroids()

        s = currClust.distanceToOtherSet(prevClust)
        
        distances.pop(0)
        distances.append(s)
        print(distances)

        if s>=1 or len(set(distances))<=1:
            return currClust


dmv = dm.getuvec()
subkeys = list(dmv.keys())[:300]
#TODO FILTER DOCS
subDic = {k: dmv[k] for k in subkeys if k in dmv}
clusters = buildClusters(subDic, 20).clusters


matching = 0
count = 0
for cl in clusters:
    if len(cl.points)>1:
        for pt in cl.points:
            for pt2 in cl.points:
                if pt == pt2:
                    continue
                for key in pt.data:
                    count+=1
                    if key in pt2.data:
                        matching+=1
        break

print(f'matching: {matching} | %: {matching/count}')