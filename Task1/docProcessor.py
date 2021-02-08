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
    with open(path) as f:
        return json.load(f)

def getStats(mailboxes):
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
    print(f'Thus there are {len(addresses)} unique addressees')
    # _saveToFile(list(addresses),"Task1/tmp/addr.json")





def getAllAddresses(mailboxes):
    addresses = set()
    for sender in mailboxes:
        for email in mailboxes[sender]:
            if len(email['tos']) > 0:
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
        pathMB = os.path.join('intermediary', 'mailboxes.json')
        mb = _loadFromFile(pathMB)
        return mb


def preProcess(doc):
    # print('starting pre')
    stemmer = nltk.stem.porter.PorterStemmer(
        nltk.stem.porter.PorterStemmer.ORIGINAL_ALGORITHM)

    stopWords = set(nltk.corpus.stopwords.words('english'))

    # symbols = "!\"#$%&()*+-–./:;“<=>?@[\]^_`,'{”|}~\n"

    # for s in symbols:
    #     doc = doc.replace(s, '')

    tokens = nltk.tokenize.word_tokenize(doc)  # tokenization
    # tokens = [t.lower() for t in tokens]  # case folding ?

    tokens = [t.lower() for t in tokens if t not in stopWords]  # stop word removal

    tokens = [stemmer.stem(d) for d in tokens]  # stemming

    return tokens



def _weights(docs):
    wordWeights = []
    for doc in tqdm(docs,desc='Getting Weights'):
        # wordWeight = dict.fromkeys(uniqueWords, 0)
        wordWeight = {}
        for word in doc:
            if word not in wordWeight:
                wordWeight[word] = 1
            else: 
                wordWeight[word] += 1
        wordWeights.append(wordWeight)

    return wordWeights

def _TF(weights):
    TF = {}
    maxTF = max(weights.values())
    for word, weight in weights.items():
        if(weight > 0):
            TF[word] = weight / float(maxTF)
    return TF


def _IDF(wordWeights):
    N = len(wordWeights)
    # IDF = totalTF = dict.fromkeys(wordWeights[0].keys(), 0)
    IDF = totalTF = {}
    for wordWeight in tqdm(wordWeights,desc='IDF'):
        for word, weight in wordWeight.items():
            if word in totalTF:
                totalTF[word] += weight
            else:
                totalTF[word] = weight

    for word, weight in totalTF.items():
        if float(weight) > 0:
            IDF[word] = math.log(N/float(weight))
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
    tfidfs = []
    tfs = []

    weights = _weights(docs)

    for i in tqdm(range(len(docs)),desc='TF'):
        tfs.append(_TF(weights[i]))

    idf = _IDF(weights)

    for tf in tqdm(tfs,desc='TFIDF'):
        tfidfs.append(_TFIDF(tf, idf))
    print('done vectorizing')
    return tfidfs


# def getALLDocs(mb):
#     addrs = getAllAddresses(mb)
#     docs={}
#     for A in tqdm(addrs,desc='Getting Docs'):
#         for B in addrs:
#             if A == B or B+A in docs or A+B in docs:
#                 continue 
#             doc = getDoc(mb, A, B)
#             if doc is not None and doc != "":
#                 docs[A+B] = doc
#     return docs


def getALLDocsSpeedy(mb):
    docs = {}
    for sender, messages in tqdm(mb.items(), desc='Getting Docs'):
        for msg in messages:
            msg['text'] = preProcess(msg['text'])
            for recip in msg['tos']:
                if sender == recip:
                    continue

                if sender+recip not in docs:
                    docs[sender+recip] = []
                if recip+sender in docs:                    
                    docs[sender+recip].extend( docs[recip+sender])
                    del docs[recip+sender]                
                docs[sender+recip].extend( msg['text'])
    return docs
        



# def ppALL(docs):
#     return [preProcess(item) for item in tqdm(docs.values(), desc='Pre-Processing')]


if __name__ == '__main__':
    getStats(getMB())
    docs = getALLDocsSpeedy(getMB())
    
    # docs = [preProcess(item) for item in tqdm(docs,desc='Pre-Processing')]
    # docs = ppALL(docs)
    _saveToFile(docs, os.path.join('intermediary', 'doc.json'))
    vectors = vectorizeDocs(docs) 
    _saveToFile(vectors, os.path.join('intermediary', 'doc_vecs2.json'))









