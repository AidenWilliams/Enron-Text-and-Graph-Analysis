# from parser import myDict
import json,os
from tqdm import tqdm




def docBuilder(mailboxes):
    global docs
    docs = {}
    emails = mailboxes.keys()
    for sender in tqdm(emails):
        for email in mailboxes[sender]:
            for recipient in email['tos']:
                if sender==recipient:
                    continue;
                users = sender+recipient
                usersR = recipient+sender

                if docs.get(users) is None:
                    if docs.get(usersR) is not None:
                        tmp = users
                        users = usersR
                        usersR = tmp #useful to stop for later reference
                    else:
                        docs[users] = {}

                if docs.get(users) is not None and docs.get(usersR) is not None:
                    docs[users].update(docs[usersR])
                    docs[usersR] = None
 

                if docs[users].get('text') is None:
                    docs[users]['text'] = ""

                docs[users]['text']+=email['text']






def checkDuplicates():
    print('checking doubles')
    for emailA in mailboxes.keys():
        for emailB in mailboxes.keys():
            if (emailA+emailB) in mailboxes and (emailB+emailA) in mailboxes:
                print('DUPLICATE FOUND!')
    print('done checking doubles')


def save(data,path):
    print('saving')
    with open(path,'w') as f:
        json.dump(data,f,indent=4)


path = os.path.join('intermediary', 'mailboxes.json')
with open(path) as f:
    mailboxes = json.load(f)

docBuilder(mailboxes)
checkDuplicates()
path = os.path.join('intermediary', 'documents.json')
save(docs,path)


