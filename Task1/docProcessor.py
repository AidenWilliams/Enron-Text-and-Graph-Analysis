# from parser import myDict
import json,os
from tqdm import tqdm


docs = {}

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


def _saveToFile(data, path):
    print('Saving')
    with open(path, 'w') as fp:
        json.dump(data, fp, indent=4)


pathMB = os.path.join('intermediary', 'mailboxes.json')
with open(pathMB) as f:
    mailboxes = json.load(f)


path = os.path.join('intermediary', 'documents.json')

if os.path.isfile(path) and os.access(path, os.R_OK):
    print("Docs file found!")
    print('Reading...')
    with open(path, 'r') as f:
        docs = json.load(f)

else:
    print("Either file is missing or is not readable, creating file...")
    docBuilder(mailboxes)
    checkDuplicates()
    _saveToFile(docs, path)


