import pickle,os
import eparser as prs
import docProcessor as dp


def saveToFile(data, path):
    print('Saving')
    with open(path, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def loadFromFile(path):
    print('loading from file')
    with open(path, 'rb') as handle:
        data = pickle.load(handle)
    return data


def loadIfCan(func, path, arg=None, toSave=None):
    path = os.path.join(workDir,path)
    if os.path.exists(path):
        return loadFromFile(path)

    if arg is None:
        item = func()
    else:
        item = func(arg)

    if toSave is not None:
        item = toSave
    saveToFile(item, path)
    return item




        

mode = 'maildir'

root = os.path.join('data', mode)

workDir = os.path.join('intermediary', mode)

mb = None
def getRawMB():
    global mb

    mbp = os.path.join(workDir, 'mb.pkl')
    if mb is not None:
        return mb
    # print('')
    if os.path.exists(mbp):
        mb = loadFromFile(mbp)
        return mb
    print('MB file not found! Parsing Mailboxes from scratch')
    mb = prs.loadData(root)
    return mb

preproc = None
def getProcMB():
    global preproc
    if preproc is None:
        return preproc
    ppPath = 'preProcessed.pkl'
    if os.path.exists(os.path.join(workDir, ppPath)):
       preproc =  loadFromFile(os.path.join(workDir, ppPath))
       return preproc
    else:
        preproc =  loadIfCan(dp.preProcessAll, 'preProcessed.pkl', arg=getRawMB())
        return preproc

vdocs = None
uvec = None
docs = None
links = None
def getDocs():
    global docs
    if docs is not None:
        return docs
    docs = dp.getALLDocs(mb)
    return docs

def getuvec():
    global uvec
    if uvec is not None:
        return uvec
    uvp = 'vectorizedUsers.pkl'
    if os.path.exists(os.path.join(workDir, uvp)):
        uvec = loadFromFile(os.path.join(workDir, uvp))
        return uvec
    uvec = loadIfCan(dp.vectorizeUsers, uvp, arg={'mb': mb, 'vd': getDocs()})
    return uvec


def getVDocs():
    global vdocs
    if vdocs is not None:
        return vdocs

    vdocs = dp.vectorizeDocs(docs)
    return vdocs


def getLinks():
    global links
    if links is not None:
        return links
    links = loadIfCan(dp.getAllLinks,  'links.pkl', arg=getRawMB())
    return links





