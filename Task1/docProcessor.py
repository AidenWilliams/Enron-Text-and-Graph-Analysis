# from parser import myDict
import json,os
from tqdm import tqdm


def docBuilder(docs, mailboxes):
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






def _checkDuplicates(mailboxes):
    print('checking doubles')
    for emailA in tqdm(mailboxes.keys()):
        for emailB in mailboxes.keys():
            if (emailA+emailB) in mailboxes and (emailB+emailA) in mailboxes:
                print('DUPLICATE FOUND!')
    print('done checking doubles')


def _saveToFile(data, path):
    print('Saving')
    with open(path, 'w') as fp:
        json.dump(data, fp, indent=4)


def _loadFromFile(path):    
    with open(path) as f:
        return json.load(f)



def stats():
    emailCount = count = tosCount = uniqueAdd = 0
    addresses = set()
    for sender in tqdm(mailboxes):
        for email in mailboxes[sender]:
            emailCount += 1
            if len(email['tos']) > 0:

                addresses.update(email['tos'])
                count += 1
                tosCount += len(email['tos'])

    print(f'There are {len(mailboxes.keys())} unique senders')
    print(f'There is also a total of {emailCount} emails')
    print(f'There are {count} which have addressees, with a total of {tosCount} addressees, {len(addresses)} of which are unique')

    addresses.update(mailboxes.keys())
    print(f'Thus there are {len(addresses)} unique total emails mentioned')



def getDoc(mailboxes,A,B):
    AB = ""
    if A in mailboxes:
        for email in mailboxes[A]:
            if B in email['tos']:
                AB += email['text']
    if B in mailboxes:
        for email in mailboxes[B]:
            if A in email['tos']:
                AB += email['text']
    return AB


pathMB = os.path.join('intermediary', 'mailboxes.json')
mb = _loadFromFile(pathMB)
print(getDoc(mb, 'heather.dunton@enron.com', 'michael.mcdonald@enron.com'))


