import os
from email.parser import Parser
from tqdm import tqdm
import json
import networkx as nx

dataroot = os.path.join('..', 'EnronEmails_Filtered', 'maildir')


def splitEmails(maillist: str, tag):
    split = maillist[tag]
    split = split.replace("\n", "")
    split = split.replace("\t", "")
    split = split.replace(" ", "")
    return split.split(',')


def readMail(email):
    update = {'subject': email['subject'], 'text': email.get_payload(), 'tos': [], 'ccs': [], 'bccs': []}
    if email['to']:
        update['tos'] = list(set(splitEmails(email, 'to')))
    if email['cc']:
        update['ccs'] = list(set(splitEmails(email, 'cc')))
        # This for if is O(n^2) it slows the parsing by a bit but it does remove duplicates in cc and bcc
        # Still takes around a minute
        for a in update['ccs']:
            if a in update['tos']:
                update['ccs'].remove(a)
    if email['bcc']:
        update['bccs'] = list(set(splitEmails(email, 'bcc')))
        for a in update['bccs']:
            if a in update['ccs']:
                update['bccs'].remove(a)
    return update


def addMail(dic, emailDir):
    with open(emailDir, "r", encoding='utf-8', errors='ignore') as f:
        email = Parser().parsestr(f.read())
        key = email['from']
        if key in dic:
            value = dic.get(email['from'])
            value.append(readMail(email))
            dic.update({key: value})
        else:
            value = [readMail(email)]
            dic.update({key: value})


def addAll(dic, emailDir):
    if not os.path.isfile(emailDir):
        for file in os.listdir(emailDir):
            addAll(dic, os.path.join(emailDir, file))
    else:
        addMail(dic, emailDir)


def loadData(dic, root):
    for user in tqdm(os.listdir(root)):
        userPath = os.path.join(root, user)
        for folder in os.listdir(userPath):
            folderPath = os.path.join(root, user, folder)
            if os.path.isfile(folderPath):
                addMail(dic, folderPath)
                continue

            for file in os.listdir(folderPath):
                addAll(dic, os.path.join(dataroot, user, folder, file))


def _saveToFile(data, path):
    print('Saving')
    with open(path, 'w') as fp:
        json.dump(data, fp, indent=4)


class Edge:
    def __init__(self, alias1: str, alias2: str, weight=0):
        self.alias1 = alias1
        self.alias2 = alias2
        self.weight = weight


edges = {}


def addEdgeToDict(frm, to):
    key = tuple([frm, to])
    if key in edges.keys():
        w = edges.get(key)
        w += 1
        edges.update({key: w})
    else:
        edges.update({key: 1})


myDict = {}
path = "../intermediary/file.json"
if os.path.isfile(path) and os.access(path, os.R_OK):
    print("Docs file found!")
    print('Reading...')
    with open(path, 'r') as f:
        myDict = json.load(f)
    print("...done!")

else:
    print("Either file is missing or is not readable, creating file...")
    loadData(myDict, dataroot)
    _saveToFile(myDict, path=path)
G = nx.DiGraph()

# get set of users
print("Reading Users")
users = {_from for _from in myDict.keys()}
for k in tqdm(myDict.keys()):
    emails = myDict.get(k)
    for e in emails:
        for t in e['tos']:
            users.update(t)
        for c in e['ccs']:
            users.update(c)
        for b in e['bccs']:
            users.update(b)

print("Building Users")
# weight dict
for _from in myDict.keys():
    e = myDict.get(_from)
    for t in e['tos']:
        addEdgeToDict(_from, t)
    for c in e['ccs']:
        addEdgeToDict(_from, c)
    for b in e['bccs']:
        addEdgeToDict(_from, b)
# for tweet in tweets:
#     if "@" in tweet.content:
#         mentions = re.findall("@(\w+)", tweet.content)
#         for mention in mentions:
#             key = tuple([tweet.alias, mention])
#             if key in edges.keys():
#                 w = edges.get(key)
#                 w += 1
#                 edges.update({key: w})
#             else:
#                 edges.update({key: 1})
#
# for edge in edges.keys():
#     G.add_edge(edge[0], edge[1], weight=edges.get(edge))
