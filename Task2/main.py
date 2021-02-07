import os
from email.parser import Parser
import time
from tqdm import tqdm
import json

rootDir = os.path.join('data', 'maildir')
myDict = {}


def readMail(email):
    update = {'subject': email['subject'], 'text': email.get_payload()}
    # update = [email['subject'], email.get_payload()]
    update['tos'] = []
    if email['to']:
        email_to = email['to']
        email_to = email_to.replace("\n", "")
        email_to = email_to.replace("\t", "")
        email_to = email_to.replace(" ", "")
        update['tos'] = email_to.split(',')
    return update


def loadData(dic, root):
    for user in tqdm(os.listdir(root)):
        userPath = os.path.join(root,user)
        for folder in os.listdir(userPath):
            
            folderPath = os.path.join(root, user,folder)
            if os.path.isfile(folderPath):
                continue

            for file in os.listdir(folderPath):
                emailDir = os.path.join(rootDir,user,folder,file)
                if not os.path.isfile(emailDir):
                    continue

                with open(emailDir, "r") as f:
                    email = Parser().parsestr(f.read())
                    key = email['from']
                    if key in dic:
                        value = dic.get(email['from'])
                        value.append(readMail(email))
                        dic.update({key: value})
                    else:
                        value = [readMail(email)]
                        dic.update({key: value})

loadData(myDict, rootDir)


def _saveToFile(data, path):
    print('Saving')
    with open(path, 'w') as fp:
        json.dump(data, fp, indent=4)


_saveToFile(myDict,'intermediary/mailboxes.json')


# for _from in myDict:
#     print("From: " + _from)
#     for mail in myDict.get(_from):
#         print("Subject: " + mail['subject'])
#         #print("Text: " + mail['text'])
#         print("To: ", end='')
#         for to in mail['tos']:
#             print(to + " ")
