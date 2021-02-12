import dependancyManager as dm
from tqdm import tqdm

# dm.jsonDump(dm.getProcMB())
dm.jsonDump(dm.getuvec())


# vdc = dm.getVDocs()
# docs = dm.getDocs()
userVectors = dm.getuvec()



# a = 'k..allen@enron.com'
# b = 'john.arnold@enron.com'
a = 'susan.mara@enron.com'
b = 'richard.shapiro@enron.com'

print(userVectors[b].keys())

# count = 0
# keys = []
# adict = userVectors[a]
# for key, val in userVectors.items():
#     if val == userVectors[a] and key != a:
#         count+=1
#         keys.append(key)

# print(keys)
# print(count)


# filteredDocs = {}
# for docK,doc in vdc.items():
#     for key in keys:
#         if key in docK:
#             for otherKeys in keys:
#                 if otherKeys !=key and  otherKeys not in docK:
#                     added = docK[0]+docK[1]
#                     filteredDocs[added] = vdc[docK]

# dm.jsonDump(filteredDocs)








# print(docs[a].keys())
# print('\n\n')
# print(docs[b].keys())
# print('\n\n')
# aset = set()
# bset = set()

# for key,docs in tqdm(vdc.items()):
#     if a in key:
#         for k in key:
#             if k!=a:
#                 aset.add(k)
#     if b in key:
#         for k in key:
#             if k != b:
#                 bset.add(k)


# for key in aset:
#     if key not in bset:
#         print('A not match!',key)

# for key in bset:
#     if key not in aset:
#         print('Bnot match!', key)
#     if a in key and b in key:
#         print('match',key)
#     if (a in key) != (b in key):
#         print('not matching: ',key)
# print('end')


# vala = []
# valb = []
# for key,values in tqdm(docs.items()):
#     if val1 in key:
#         vala.append(values)
#         # print(values)

# for key, values in tqdm(docs.items()):
#     if val2 in key:
#         valb.append(values)
#         # print(values)


# print(len(vala))
# print(len(valb))

# diff = 0
# setA = set(vala)
# setB = set(valb)
# for x,y in tqdm(zip(vala,valb)):
#     if x!=y:
#         print('diff')



# print(doc[val1].keys())
# print('\n\n')
# print(doc[val2].keys())
# print('\n\n')


