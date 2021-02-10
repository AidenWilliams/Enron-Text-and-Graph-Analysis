import os
from email.parser import Parser
from tqdm import tqdm
import json


def readMail(email):
    update = {'subject': email['subject'],
              'text': email.get_payload()[:25000], 'tos': []} 
    #limit text size to 25k characters; should be more than enough for normal email, but cuts down the outliers

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
            # value = dic.get(email['from'])
            # value.append(readMail(email))
            # dic.update({key: value})
            dic[key].append(readMail(email))
        else:
            dic[key] =  [readMail(email)]
            # value = [readMail(email)]
            # dic.update({key: value})


def addAll(dic, emailDir):
    if not os.path.isfile(emailDir):
        for file in os.listdir(emailDir):
            addAll(dic, os.path.join(emailDir, file))
    else:
        addMail(dic, emailDir)


def loadData(root):
    dic = {}
    for user in tqdm(os.listdir(root)):
        userPath = os.path.join(root, user)
        for folder in os.listdir(userPath):
            folderPath = os.path.join(root, user, folder)
            if os.path.isfile(folderPath):
                addMail(dic, folderPath)
                continue

            for file in os.listdir(folderPath):
                addAll(dic, os.path.join(root, user, folder, file))
    return dic


# def _saveToFile(data, path):
#     print('Saving')
#     with open(path, 'w') as fp:
#         json.dump(data, fp, indent=4)


# def getMB(path,root):
#     if os.path.isfile(path) and os.access(path, os.R_OK):
#         print("Mailboxes file found!")
#         print('Reading...')
#         with open(path, 'r') as f:
#             myDict = json.load(f)

#     else:
#         print("Either file is missing or is not readable, creating file...")
#         myDict = loadData(root)
#         _saveToFile(myDict, path)

#     return myDict

# if __name__ == '__main__':
#     var = 'maildir'
#     rootDir = os.path.join('data', var)
#     path = os.path.join('intermediary', var, 'mb.json')

    # myDict = getMB(path,rootDir)

    
