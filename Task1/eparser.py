import os
from email.parser import Parser
from tqdm import tqdm
# from multiprocessing import Pool


def readMail(email):
    # update = {'subject': email['subject'],'text': email.get_payload()[:25000], 'tos': []} 
    update = {'subject': email['subject'],'text': email.get_payload()[-25000:], 'tos': []} 
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
            dic[key].append(readMail(email))
        else:
            dic[key] =  [readMail(email)]


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

    
