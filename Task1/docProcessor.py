# from parser import myDict
import gc
import os,math
from tqdm import tqdm
import nltk
from multiprocessing import Pool, cpu_count
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


import dependancyManager as dm





def getStats(mailboxes):
    emailCount = count = tosCount = 0
    addresses = set()
    for sender in tqdm(mailboxes):
        for email in mailboxes[sender]:
            emailCount += 1
            if email['tos']:
                addresses.update(email['tos'])
                count += 1
                tosCount += len(email['tos'])

    print(f'There are {len(mailboxes.keys())} unique senders')
    print(f'There is also a total of {emailCount} emails')
    print(f'There are emails {count} which have addressees, with a total of {tosCount} addressees, {len(addresses)} of which are unique')

    addresses.update(mailboxes.keys())
    print(f'Thus there are {len(addresses)} unique addressees')





def getAllAddresses(mailboxes):
    addresses = set()
    for emails in mailboxes.values():
        for email in emails:
            if email['tos']:
                addresses.update(email['tos'])
    addresses.update(mailboxes.keys())
    return addresses


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

def getParticularLink(mbxs,user):
    links = {}
    if user not in links:
        links[user] = {}
    if user in mbxs:
        for message in mbxs[user]:
            for to in message['tos']:
                if to in links[user]:
                    links[user][to] += 1
                else:
                    links[user][to] = 1
    for sender, msgs in mbxs.items():
        for msg in msgs:
            if user in msg['tos']:
                if sender in links[user]:
                    links[user][sender]+=1
                else:
                    links[user][sender]=1
    return links


def getAllLinks(mbxs):
    links = {}
    for user, msgs in tqdm(mbxs.items(), desc='Generating User Links'):
        if user not in links:
            links[user]= {}
        if user in mbxs:
            for msg in msgs:
                for to in msg['tos']:        
                                
                    if to in links[user]:
                        links[user][to] += 1
                    else:
                        links[user][to] = 1

                    if to not in links:
                        links[to] = {}
                
                    if user in links[to]:
                        links[to][user] += 1
                    else:
                        links[to][user] = 1
    return links
        
                



def preProcess(doc):
    # print('starting pre')
    stemmer = nltk.stem.porter.PorterStemmer(
        nltk.stem.porter.PorterStemmer.ORIGINAL_ALGORITHM)

    stopWords = set(nltk.corpus.stopwords.words('english'))

    symbols = "!\"#$%&()*+-–./:;“<=>?@[\]^_`,'{”|}~\n"
    # # symbols = "-.,:?\n!"

    for s in symbols:
        doc = doc.replace(s, '')

    # table = doc.maketrans("","",symbols)
    # doc.translate(table)
    
    tokens = nltk.tokenize.word_tokenize(doc)  # tokenization
    # tokens = [t.lower() for t in tokens]  # case folding ?
    tokens = [t.lower() for t in tokens]
    tokens = [stemmer.stem(t) for t in tokens if t not in stopWords]  # stop word removal

    # tokens = [stemmer.stem(d) for d in tokens]  # stemming

    return tokens



def _weights(docs):
    wordWeights = {}
    for key, doc in tqdm(docs.items(), desc='Getting Weights'):
        if not doc:
            continue
        # wordWeight = dict.fromkeys(uniqueWords, 0)
        wordWeight = {}
        for word in doc:
            if word not in wordWeight:
                wordWeight[word] = 1
            else: 
                wordWeight[word] += 1
        wordWeights[key] = wordWeight

    return wordWeights

def _TF(weights):
    TF = {}
    # if weights:
    maxTF = max(weights.values())
    # else:
    #     maxTF = 1
    for word, weight in weights.items():
        if(weight > 0):
            TF[word] = weight / float(maxTF)
    return TF


def _IDF(wordWeights):
    N = len(wordWeights)
    # IDF = totalTF = dict.fromkeys(wordWeights[0].keys(), 0)
    IDF = totalTF = {}
    for wordWeight in tqdm(wordWeights.values(),desc='IDF'):
        for word, weight in wordWeight.items():
            if word in totalTF:
                totalTF[word] += weight
            else:
                totalTF[word] = weight

    for word, weight in totalTF.items():
        if float(weight) > 0:
            IDF[word] = math.log(1+N/1+float(weight))
        else:
            print('0 idf: '+word)
            IDF[word] = 0
    return IDF


def _TFIDF(TF, IDF):
    TFIDF = {}

    for word, weight in TF.items():
        if word not in IDF:
            print(f"term '{word}'' not found in idf, returnig zero")
            TFIDF[word] = 0
        else:
            TFIDF[word] = weight * IDF[word]
    return TFIDF

def vectorizeDocs(docs):

    tfidfs = {}

    weights = _weights(docs)
    del docs
    # gc.collect()
    idf = _IDF(weights)

    for key, w in tqdm(weights.items(), desc='TFIDF'):
        tfidfs[key] = _TFIDF(_TF(w), idf)
        weights[key] = None
    del weights
    gc.collect()
    return tfidfs


def preProcessAll(mailboxes):
    newMailboxes = {}
    for sender, msgs in mailboxes.items():
        for msg in msgs:
            if msg['tos']:
                if sender not in newMailboxes:
                    newMailboxes[sender] = []
                newMailboxes[sender].append(msg)

    p = Pool(processes=cpu_count() // 2)
    senders = newMailboxes.keys()
    print('Starting to process data, it is normal for this process to seem "stuck" as it waits for all threads to finish')
    processed = p.map(preProcessUser, tqdm(newMailboxes.values(),desc='PreProcessing'))
    p.close()
    p.join()
    for sender, pmb in zip(senders,processed):
        newMailboxes[sender] = pmb
    return newMailboxes


def preProcessUser(messages):
    newMSGS = []
    for msg in messages:
        msg['text'] = preProcess(msg['text'])
        newMSGS.append(msg)
    return newMSGS

def getALLDocs(mbxs):
    docs = {}
    for sender, messages in tqdm(mbxs.items(), desc='Forming Docs'):
        for msg in messages:
            for recip in msg['tos']:
                if sender == recip:
                    continue
                users = (sender,recip)
                usersR = (recip, sender)

                if users not in docs:
                    docs[users] = []
                if usersR in docs:
                    docs[users].extend( docs[usersR])
                    del docs[usersR]

                docs[users].extend( (msg['text']))
    return docs





def vectorizeUsers(vDocs):
    gc.collect()
    # vDocs = data['vd']
    # mb = data['mb']
    vUsers = {}

    vCounts = {}
    vTotals = {}
    for users, doc in tqdm(vDocs.items(),desc='Weighting User Terms'):
        A = users[0]
        B = users[1]

        if A not in vCounts:
            vCounts[A] = {}
            vTotals[A] = {}
        if B not in vCounts:
            vCounts[B] = {}
            vTotals[B] = {}

       
        for word, value in doc.items():
            if word in vCounts[A]:
                vCounts[A][word] += 1
                vTotals[A][word] += value
            else:
                vCounts[A][word] = 1
                vTotals[A][word] = value

            if word in vCounts[B]:
                vCounts[B][word] += 1
                vTotals[B][word] += value
            else:
                vCounts[B][word] = 1
                vTotals[B][word] = value
        vDocs[users] = None
    del vDocs
    gc.collect()
    skipCount = 0;
    for user in tqdm(getAllAddresses(dm.getProcMB()),desc='Vectorizing User Terms'):
        if user not in vCounts:
            skipCount +=1
            continue

        for word in vCounts[user]:
            if user not in vUsers:
                vUsers[user] = {}
            vUsers[user][word] = vTotals[user][word]/vCounts[user][word]
        del vTotals[user]
        del vCounts[user]
    print(skipCount,'users were skipped')
    gc.collect()
    return vUsers










