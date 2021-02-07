import os
from email.parser import Parser
import time
from tqdm import tqdm

rootDir = "../maildir/"
myDict = {}


def readMail(email):
    update = {'subject': email['subject'], 'text': email.get_payload()}
    #update = [email['subject'], email.get_payload()]
    update['tos'] = []
    if email['to']:
        email_to = email['to']
        email_to = email_to.replace("\n", "")
        email_to = email_to.replace("\t", "")
        email_to = email_to.replace(" ", "")
        update['tos'] = email_to.split(',')
    return update


def loadData(dic, root):
    for directory, subdirectory, filenames in tqdm(os.walk(root)):
        for file in filenames:
            dir = directory + "/" + file
            with open(dir, "r") as f:
                email = Parser().parsestr(f.read())
                key = email['from']
                if key in dic:
                    value = dic.get(email['from'])
                    value.append(readMail(email))
                    dic.update({key: value})
                else:
                    value = [readMail(email)]
                    dic.update({key: value})


x = time.perf_counter()
loadData(myDict, rootDir)
y = time.perf_counter()
print(str(y-x))
# for _from in myDict:
#     print("From: " + _from)
#     for mail in myDict.get(_from):
#         print("Subject: " + mail['subject'])
#         #print("Text: " + mail['text'])
#         print("To: ", end='')
#         for to in mail['tos']:
#             print(to + " ")
