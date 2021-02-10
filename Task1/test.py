# import pandas as pd
import json,pickle
from datetime import datetime

prepic = {}
with open('intermediary/maildir/prePickle/NMpreProcessed.json', 'r') as handle:
    prepic = json.load(handle)

pic = {}
with open('intermediary/maildir/preProcessed.pkl', 'rb') as handle:
    pic = pickle.load(handle)
print('matchin')
for pre in prepic:
    if prepic[pre] != pic[pre]:
        print('\ndiff!')
        for pr,p in zip(prepic[pre],pic[pre]):
            if pr != p:
                for msgField in pr:
                    if pr[msgField] != p[msgField]:
                        if set(pr[msgField]) != set(p[msgField]):
                            print('\n\nold: ', pr[msgField])
                            print('new: ', p[msgField])
        break
print('done')
# startN = datetime.now()
# with open('intermediary/maildir/mb.json','r') as f:
#     data = json.load(f)
# endN = datetime.now()-startN

# startS = datetime.now()
# with open('intermediary/maildir/mb.json','w') as f:
#     json.dump(data,f)
# endS = datetime.now()-startN

# startSP = datetime.now()
# with open('intermediary/maildir/mb.pkl', 'wb') as handle:
#     pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
# endSP = datetime.now()-startSP


# startRP = datetime.now()
# with open('intermediary/maildir/mb.pkl', 'rb') as handle:
#     data = pickle.load(handle)
# endRP = datetime.now()-startRP
# df = pd.DataFrame.from_dict(data)
# df.to_pickle("intermediary/maildir/mbPD.pkl")

# startP = datetime.now()
# unpickled_df = pd.read_pickle("intermediary/maildir/mbPD.pkl")
# endP = datetime.now()-startP



# df = pd.DataFrame.from_dict(data)
# df.to_jsone("intermediary/maildir/mbD.json")

# startD = time.now()
# unJS = pd.read_json("intermediary/maildir/mbD.json")
# endD = time.now()-startP

# print('norm read:',endN)
# print('norm save:',endS)
# # print('df:',endD)
# print('pkl save:',endSP)
# print('pkl read:',endRP)











# import json
# from tqdm import tqdm
# data = {}
# dataOLD = {}

# print('loading')
# with open('intermediary/maildir/vectorizedUsers.json', 'r') as f:
#     data = json.load(f)


# print('loading old')
# with open('intermediary/maildir/tmp/vectorizedUsers.json', 'r') as f:
#     dataOLD = json.load(f)

# # missing = 0
# # for key in dataOLD:
# #     )

# # print(missing)


# missingWords = set()
# missing = 0
# for key,weights in dataOLD.items():
#     if key not in data:
#         missing+=1
#         print(key)
#         continue
#     for w in weights:
#         if w not in data[key]:
#             print(f'{w} missing from {key} -/- ')
#             missingWords.update(w)

# print(missing)
# print(missingWords)
# # data = {}
# # with open('intermediary/maildir/mb.json','r') as f:
# #     data = json.load(f)

# # # print(len(data["kim.ward@enron.com"][176]['text']))
# # # print(len(data["mailer-daemon@postmaster.enron.com"][1]['text']))
# # # print(len(data["mailer-daemon@postmaster.enron.com"][2]['text']))
# # # print(len(data["mailer-daemon@postmaster.enron.com"][3]['text']))

# # tot = 0
# # totals = []
# # for msgs in tqdm(data.values()):
# #     for msg in msgs:
# #         ln = len(msg['text'])
# #         tot += ln
# #         if ln>50000:
# #             totals.append(ln)


# # lng = len(data)

# # avg = tot/lng

# # print(tot)
# # print(lng)
# # print(avg)

# # print(totals)
