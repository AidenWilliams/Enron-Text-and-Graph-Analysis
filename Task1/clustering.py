from random import randint
import dependancyManager as dm



def dot(A, B):
    return (sum(a*b for a, b in zip(A, B)))


def sim(A, B):
    denom = ((dot(A, A) ** .5) * (dot(B, B) ** .5))
    if denom == 0:
        return 0
    return dot(A, B) / denom


class point:
    parentCluster = None
    data = {}  # data vec

    def __init__(self,dt):
        self.parentCluster = None
        self.data = dt
    

    def similarityTo(self,clust):
        thisV = clV = []
        for word,weight in self.data.items():
            thisV.append(weight)
            if word in clust.centroid:
                clV.append(clust.centroid[word])
            else:
                clV.append(0)

        return sim(thisV, clV)

    def assignClosest(self,clusters):
        sims = {}
        for c in clusters:
            sims[c] = self.similarityTo(c)
        topClust = dict(sorted(sims.items(), key=lambda item: item[1],reverse=True)).keys()[0]
        self.parentCluster = topClust
        self.parentCluster.points.append(self)


class Cluster:
    centroid = {}  # data vec
    points = []

    def __init__(self, cntrd):
        self.centroid = cntrd 

    def reCalc(self):
        totals = {}
        docCount = len(self.points)
        for p in self.points:
            for word,weight in p.data:
                if word not in totals:
                    totals[word] = 0
                totals[word]+=weight

        for t,v in totals.items():
            self.centroid[t] = v/docCount


class clusterSet:
    clusters = []
    def __init__(self,clusters):
        self.clusters = clusters
    
    def reCalculateCentroids(self):
        for c in self.clusters:
            c.reCalc()

    # def distanceToOtherSet(self,other):   #IDK WHAT TO DO HERE
    #     return sim()

    # def distanceToVec(slef,vec):          #IDK WHAT TO DO HERE
    #     return sim()

    def reAssignPoints(self):
        allPts = []
        for c in self.clusters:
            allPts.extend(c.points)
            c.points.clear()
        for p in allPts:
            p.assignClosest(self.clusters)
            

dmv = dm.getuvec()
subkeys = list(dmv.keys())[:30]
#TODO FILTER DOCS
subDic = {k: dmv[k] for k in subkeys if k in dmv}
buildClusters(subDic, 5)


# here we will minimise the amount of nodes to calm things down for the clustering!
def filterDocs(userDocs):
    #return userDocs

    #maybe use top nodes ?

    #rank docs based on something
    #choose top N docs
    pass


def randomInit(userDocs,k):
    init = []
    while(len(init)) < k:
        ind = randint(0, lng-1)
        if ind not in init:
            init.append(ind)
    initClusters = []
    for x in init:
        points = list(list(userDocs.values())[x].values())
        clst = Cluster(points)
        initClusters.append(clst)
    return initClusters

def buildClusters(userDocs, k):
    
    lng = len(userDocs)
    if k > lng:
        ValueError("K larger than document count!")
    
    initClusters = randomInit(userDocs,k)
    currClust = clusterSet(initClusters)
    prevClust = []
    s = sim(currClust, prevClust)

    # closest = closestCentr(currClust, userDocs)
    while True:

        
        currClust.reAssignPoints()
        prevClust = currClust
        currClust.reCalculateCentroids()

        s = sim(currClust.centroid,prevClust.centroid)
        if s==1:
            return currClust
        # closest = closestCentr(currClust, userDocs)

        # prevClust = currClust
        # currClust = calcCentroids(closest, currClust)

# def buildClusters(userDocs, k):
#     init = []
#     lng = len(userDocs)
#     if k > lng:
#         ValueError("K larger than document count!")
#     while(len(init)) < k:
#         ind = randint(0, lng-1)
#         if ind not in init:
#             init.append(ind)
#     initClusters = []
#     for x in init:
#         initClusters.append(list(list(userDocs.values())[x].values()))
#     currClust = initClusters
#     prevClust = []
#     s = sim(currClust, prevClust)

#     closest = closestCentr(currClust, userDocs)
#     while(s != 1):

#         s = sim(prevClust, currClust)

#         closest = closestCentr(currClust, userDocs)

#         prevClust = currClust
#         currClust = calcCentroids(closest, currClust)




# def closestCentr(prev,docs):
#     distances = {}
#     for d in docs:
#         if d not in distances:
#             distances[d] = {}
#             for c in prev:
#                 distances[d][c] = sim(d,c)
#         distances[d] = sorted(distances[d].values())[-1]
#     return distances


# def calcCentroids(points,clust):
#     # cntrds = {}
#     cnt = {}
#     # for c in clust:
#     #     if c not in dist:
#     #         dist[c] = {}
#     #     for p in points:
#     #         dist[c][p] = sim(c,p)
#         # dist[c] = sorted(dist[c].values())[-1]
#     for c in clust:
#         if c not in cnt:
#             cnt[c] = {}
#         for point, cluster in points.items():
#             if point not in cnt[c]:
#                 cnt[c][point] = {'sor': 0, 'denom': 0}

#             cnt[c][point]['sor']  +=(cluster == c)*point
#             cnt[c][point]['denom'] += (cluster == c)
#         cnt[c] = sum([cnt[c][point]['sor'] for point in cnt[c]])/sum([cnt[c][point]['denom'] for point in cnt[c]])
#     return cnt
    


        

# def avgClusterVecs(clusters,userVectors): #SOMETHING ALONG THESE LINES
#     avgs = {}
#     for cluster in clusters:        
#         totals = counts = 0
#         for user in cluster:
#             totals+=userVectors[user]
#             counts+=1
#         avgs[cluster] = totals/counts





# def findClosestCentroids(ic, X):
#     assigned_centroid = []
#     for i in X:
#         distance = []
#         for j in ic:
#             distance.append(sim(i, j))
#         assigned_centroid.append(np.argmin(distance))
#     return assigned_centroid


# def calc_centroids(clusters, X):
#     new_centroids = []
#     new_df = pd.concat([pd.DataFrame(X), pd.DataFrame(clusters, columns=['cluster'])],axis=1)
#     for c in set(new_df['cluster']):
#         current_cluster = new_df[new_df['cluster'] == c][new_df.columns[:-1]]
#         cluster_mean = current_cluster.mean(axis=0)
#         new_centroids.append(cluster_mean)
#     return new_centroids

# def buildClusters(userDocs, k):
#     currCentroids = {}
#     prevCentroids = {}

#     for c in currCentroids:

#     s = sim(currCentroids, prevCentroids)
#     clusters = {}
#     sims = {}

#     while(s!=1): #no change in clusters
#         for user, doc in userDocs.items():
#             sims[user].append( sim(currCentroids,doc))
#             k = max(sims[user])

    # pass
