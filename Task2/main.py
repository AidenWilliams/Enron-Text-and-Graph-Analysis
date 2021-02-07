import os
from email.parser import Parser
from tqdm import tqdm
import json

rootDir = os.path.join('..', 'maildir')
myDict = {}


def readMail(email):
    update = {'subject': email['subject'], 'text': email.get_payload(), 'tos': []}

    if email['to']:
        email_to = email['to']
        email_to = email_to.replace("\n", "")
        email_to = email_to.replace("\t", "")
        email_to = email_to.replace(" ", "")
        update['tos'] = list(set(email_to.split(',')))
    return update


def addMail(dic, emailDir):
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
                addAll(dic, os.path.join(rootDir, user, folder, file))


def _saveToFile(data, path):
    print('Saving')
    with open(path, 'w') as fp:
        json.dump(data, fp, indent=4)


def init(path="../intermediary/file.json"):
    myDict = {}
    if os.path.isfile(path) and os.access(path, os.R_OK):
        print("Docs file found!")
        print('Reading...')
        with open(path, 'r') as f:
            myDict = json.load(f)

    else:
        print("Either file is missing or is not readable, creating file...")
        loadData(myDict, rootDir)
        _saveToFile(myDict, path=path)


myDict = {}
init()


