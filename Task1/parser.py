import io
import os
from enron_reader import EnronReader
import json
# import pickle

_reader = EnronReader("data/subset/")

def _getMailBoxes():
    maxCount = len(_reader.get_user_ids())
    count = 0
    mailboxes = {}
    messages = {}
    for userID in _reader.get_user_ids():
       
        count+=1
        print('\rFetching Mailboxes: '+str(count/maxCount *100)+'%                         ',end='')

        mailbox = _reader.get_mailbox_for_user(userID)
        main_folders = mailbox.root_folder.subfolders

        if len(main_folders) <= 1:
            print(
                f'\n\nMain Folders for "{userID}" were not found!\nSkipping...\n')
            continue;
            

        inbox_folder = main_folders[1]
        messages.clear()

        for message in inbox_folder.messages:
            message.email_from = message.email_from[1]
            message.email_to = [u[1] for u in message.email_to if message.email_to is not None]
            message.plaintext.lower().replace('"',"'")


            # msg = {'subject': message.subject, 'from': message.email_from,'to': message.email_to, 'text': message.plaintext}
            msg = {'subject': message.subject, 'text': message.plaintext}
            

            if message.email_to is not None:
                for recip in message.email_to:
                    if messages.get(recip) is None:
                        messages[recip] = []
                    messages[recip].append(msg);

            if mailboxes.get(message.email_from) is None:
                mailboxes[message.email_from] = {}
            mailboxes[message.email_from].update(messages)
    return mailboxes


def _saveToFile(data, path):
    print('Saving')
    with open(path, 'w') as fp:
        json.dump(data, fp, indent=4)


def getDistinctAddrs(mailboxes):
    _emailAddresses = []
    for key, msgs in mailboxes.items():
        if key not in _emailAddresses:
            _emailAddresses.append(key)

        for key2 in msgs.keys():
            if key2 not in _emailAddresses:
                _emailAddresses.append(key2)
    return _emailAddresses


def combineMail(_emailAddresses,mailboxes):
    combinedMail = {}
    for userA in _emailAddresses:
        if mailboxes.get(userA) is None:
            continue

        for userB, messages in mailboxes[userA].items():
            users = userA+userB
            usersR = userB+userA

            if users in combinedMail or usersR in combinedMail:
                continue

            combined = messages
            
            if mailboxes.get(userB) is not None and mailboxes[userB].get(userA) is not None:
                combined.extend(mailboxes[userB][userA])
            combinedMail[users] = combined
    return combinedMail

def _docBuilder(mailboxes):    
    

    _emailAddresses = getDistinctAddrs(mailboxes)
    combinedMail = combineMail(_emailAddresses, mailboxes)

    docs = {}
    for key, mail in combinedMail.items():
        [print(email) for email in mail if isinstance(email, list)]


        docs[key] = ""
        for email in mail:
            docs[key] += email['text']
    return docs


def buildMailBoxes():
    print("Bulding mailboxes")
    path = 'intermediary/mailboxes.json'
    mailboxes = None
    if os.path.isfile(path) and os.access(path, os.R_OK):
        print("Mailboxes file found!")
        print('Reading...')
        with open(path,'r') as f:
            mailboxes = json.load(f)

    else:
        print("Either file is missing or is not readable, creating file...")
        mailboxes = _getMailBoxes()
        _saveToFile(mailboxes,path=path)
    return mailboxes


def buildDocs(mailboxes):
    print("Bulding Docs")
    path = 'intermediary/documents.json'
    docs = {}

    if os.path.isfile(path) and os.access(path, os.R_OK):
        print("Docs file found!")
        print('Reading...')
        with open(path, 'r') as f:
            docs = json.load(f)

    else:
        print("Either file is missing or is not readable, creating file...")
        docs = _docBuilder(mailboxes)
        _saveToFile(docs, path=path)
    return docs


mb = buildMailBoxes()
docs = buildDocs(mb)

# print(mb['allen-p']['subject'])
