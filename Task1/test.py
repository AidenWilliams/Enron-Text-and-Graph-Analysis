import json
from tqdm import tqdm
data = {}
dataOLD = {}

print('loading')
with open('intermediary/maildir/vectorizedUsers.json', 'r') as f:
    data = json.load(f)


print('loading old')
with open('intermediary/maildir/tmp/vectorizedUsers.json', 'r') as f:
    dataOLD = json.load(f)

# missing = 0
# for key in dataOLD:
#     )

# print(missing)


missingWords = set()
missing = 0
for key,weights in dataOLD.items():
    if key not in data:
        missing+=1
        print(key)
        continue
    for w in weights:
        if w not in data[key]:
            print(f'{w} missing from {key} -/- ')
            missingWords.update(w)

print(missing)
print(missingWords)
# data = {}
# with open('intermediary/maildir/mb.json','r') as f:
#     data = json.load(f)

# # print(len(data["kim.ward@enron.com"][176]['text']))
# # print(len(data["mailer-daemon@postmaster.enron.com"][1]['text']))
# # print(len(data["mailer-daemon@postmaster.enron.com"][2]['text']))
# # print(len(data["mailer-daemon@postmaster.enron.com"][3]['text']))

# tot = 0
# totals = []
# for msgs in tqdm(data.values()):
#     for msg in msgs:
#         ln = len(msg['text'])
#         tot += ln
#         if ln>50000:
#             totals.append(ln)


# lng = len(data)

# avg = tot/lng

# print(tot)
# print(lng)
# print(avg)

# print(totals)
