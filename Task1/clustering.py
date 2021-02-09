from random import randint
# def sim(A,B):
#     sim = {}
#     for x in A:
#         if x in B:
#             sim[x] = cosSim(A[x],B[x])
#         else:
#             sim[x] = 0
#     for x in B:
#         if x in A:
#             sim[x] = cosSim(A[x], B[x])
#         else:
#             sim[x] = 0 
#     pass

# def cosSim(x,y):
#     return 0;


def dot(A, B):
    return (sum(a*b for a, b in zip(A, B)))


def sim(A, B):
    denom = ((dot(A, A) ** .5) * (dot(B, B) ** .5))
    if denom == 0:
        return 0
    return dot(A, B) / denom


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

def closestCentr(prev,docs):
    distances = {}
    for d in docs:
        if d not in distances:
            distances[d] = {}
            for c in prev:
                distances[d][c] = sim(d,c)
        distances[d] = sorted(distances[d].values())[-1]
    return distances


def calcCentroid(points,clust):
    # cntrds = {}
    cnt = {}
    # for c in clust:
    #     if c not in dist:
    #         dist[c] = {}
    #     for p in points:
    #         dist[c][p] = sim(c,p)
        # dist[c] = sorted(dist[c].values())[-1]
    for c in clust:
        if c not in cnt:
            cnt[c] = {}
        for point, cluster in points.items():
            if point not in cnt[c]:
                cnt[c][point] = {'sor': 0, 'dee': 0}
            cnt[c][point]['sor']  +=(cluster == c)*point
            cnt[c][point]['dee'] += (cluster == c)
        cnt[c] = sum([cnt[c][point]['sor'] for point in cnt[c]]/sum([cnt[c][point]['dee'] for point in cnt[c]])
    return cnt
    

def buildClusters(userDocs, k):
    init = []
    lng = len(userDocs)
    for i in range(k):
        ind = randint(0,lng-1)
        init.append(ind)
    initClusters = []
    for x in init:
        initClusters.append(userDocs[x])
    currClust = initClusters
    prevClust = []
    s = sim(prevClust,currClust)

    closest = closestCentr(prevClust, userDocs)
    while(s!=1):
        

        s = sim(prevClust, currClust)
        closest = closestCentr(prevClust, userDocs)

def filterDocs(userDocs):
    #return userDocs
    pass
