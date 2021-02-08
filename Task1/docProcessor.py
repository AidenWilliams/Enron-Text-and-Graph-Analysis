# from parser import myDict
from multiprocessing import Pool
import json,os,math
from tqdm import tqdm
import nltk
nltk.download('punkt')
nltk.download('stopwords')


def _saveToFile(data, path):
    print('Saving')
    with open(path, 'w') as fp:
        json.dump(data, fp, indent=4)


def _loadFromFile(path):
    print('loading from file')
    with open(path) as f:
        return json.load(f)

def getStats(mailboxes):
    emailCount = count = tosCount = uniqueAdd = 0
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
    print(f'There are {count} which have addressees, with a total of {tosCount} addressees, {len(addresses)} of which are unique')

    addresses.update(mailboxes.keys())
    print(f'Thus there are {len(addresses)} unique addressees')





def getAllAddresses(mailboxes):
    addresses = set()
    for sender in mailboxes:
        for email in mailboxes[sender]:
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


mb = None
def getMB():
    global mb
    if mb is not None:
        return mb
    else:
        print("Loading mailboxes")
        pathMB = os.path.join('intermediary', 'submailboxes.json')
        mb = _loadFromFile(pathMB)
        return mb


def preProcess(doc):
    # print('starting pre')
    stemmer = nltk.stem.porter.PorterStemmer(
        nltk.stem.porter.PorterStemmer.ORIGINAL_ALGORITHM)

    stopWords = set(nltk.corpus.stopwords.words('english'))

    # symbols = "!\"#$%&()*+-–./:;“<=>?@[\]^_`,'{”|}~\n"
    # symbols = "-.,:?\n"

    # for s in symbols:
    #     doc = doc.replace(s, '')
    
    tokens = nltk.tokenize.word_tokenize(doc)  # tokenization
    # tokens = [t.lower() for t in tokens]  # case folding ?

    tokens = [stemmer.stem(t.lower()) for t in tokens if t not in stopWords]  # stop word removal

    # tokens = [stemmer.stem(d) for d in tokens]  # stemming

    return tokens



def _weights(docs):
    wordWeights = {}
    for key,doc in tqdm(docs.items(),desc='Getting Weights'):
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
        if word not in IDF.keys():
            print(f"term '{word}'' not found in idf, returnig zero")
            TFIDF[word] = 0
        else:
            TFIDF[word] = weight * IDF[word]
    return TFIDF

def vectorizeDocs(docs):
    print('vectorizing')
    tfidfs = {}
    tfs = {}

    weights = _weights(docs)

    for key,w in tqdm(weights.items(),desc='TF'):
        tfs[key] = (_TF(w))

    idf = _IDF(weights)

    for key,tf in tqdm(tfs.items(),desc='TFIDF'):
        tfidfs[key] = (_TFIDF(tf, idf))
    print('done vectorizing')
    return tfidfs


def preProcessAll(mailboxes):
    newMailboxes = {}
    for sender, msgs in mailboxes.items():
        for msg in msgs:
            if msg['tos']:
                if sender not in newMailboxes:
                    newMailboxes[sender] = []
                newMailboxes[sender].append(msg)

    for sender in tqdm(newMailboxes, desc='PreProcessing'):
        for msg in newMailboxes[sender]:
            msg['text'] = preProcess(msg['text'])

    return newMailboxes



def getALLDocs(mb):
    docs = {}
    for sender, messages in tqdm(mb.items(), desc='Getting Docs'):
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


def loadIfCan(func, path, arg=None,toSave = None):
    if os.path.exists(path):
        return _loadFromFile(path)

    if arg is None:
        item = func()
    else:
        item = func(arg)

    if toSave is not None:
        item = toSave
    _saveToFile(item, path)
    return item


def vectorizeUsers(vDocs):
    vUsers = {}
    
    for user in tqdm(getAllAddresses(getMB()),desc='Vectorizing Users'):
        relevantVecs = []
        vCounts = {}
        vTotals = {}
        for users in vDocs:
            if user in users:
                relevantVecs.append(vDocs[users])
        for vec in relevantVecs:
            for word, value in vec.items():
                if word in vCounts:
                    vCounts[word] += 1
                    vTotals[word] += value
                else:
                    vCounts[word]=1
                    vTotals[word] = value
        for key in vCounts:
            if user not in vUsers:
                vUsers[user] = {}
            vUsers[user][key] = vTotals[key]/vCounts[key]
                
    return vUsers



                

if __name__ == '__main__':
    
    getStats(getMB())

    mb = loadIfCan(preProcessAll, os.path.join('intermediary', 'sppMailBoxes.json'), arg = getMB())
    docs = getALLDocs(getMB())
    # vectorDocs = loadIfCan(vectorizeDocs, os.path.join('intermediary', 'svectorizedDocs.json'), docs)
    vectorDocs = vectorizeDocs(docs)
    vectorUsers = loadIfCan(vectorizeUsers, os.path.join('intermediary', 'svectorizedUsers.json'), arg=vectorDocs)










