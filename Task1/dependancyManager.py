import pickle,os,json
import eparser as prs
import docProcessor as dp

mode = 'maildir'
# mode = 'subset'

root = os.path.join('data', mode)

workDir = os.path.join('Task1','intermediary', mode)


def saveToFile(data, path):
    print(f'Saving data to: {path}')
    with open(path, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def loadFromFile(path):
    print(f'Loading data from: {path}')
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




_mb = None
def getRawMB():
    global _mb

    mbp = os.path.join(workDir, 'mb.pkl')
    if _mb is not None:
        return _mb
    # print('')
    if os.path.exists(mbp):
        _mb = loadFromFile(mbp)
        return _mb
    # print('MB file not found! Parsing Mailboxes from scratch')
    print('MB was not generated yet! Parsing Mailboxes from scratch')
    _mb = prs.loadData(root)
    return _mb

_preproc = None
_vdocs = None
_uvec = None
_docs = None
_links = None
def getProcMB():
    global _preproc
    if _preproc is not None:
        return _preproc
    ppPath = 'preProcessed.pkl'

    if os.path.exists(os.path.join(workDir, ppPath)):
       _preproc =  loadFromFile(os.path.join(workDir, ppPath))
       return _preproc

    _preproc =  loadIfCan(dp.preProcessAll, 'preProcessed.pkl', arg=getRawMB())
    return _preproc


def getDocs():
    global _docs
    if _docs is not None:
        return _docs
    _docs = dp.getALLDocs(getProcMB())
    return _docs

def getuvec():
    global _uvec
    if _uvec is not None:
        return _uvec
    uvp = 'vectorizedUsers.pkl'
    if os.path.exists(os.path.join(workDir, uvp)):
        _uvec = loadFromFile(os.path.join(workDir, uvp))
        return _uvec
    _uvec = loadIfCan(dp.vectorizeUsers, uvp, arg={'mb': getProcMB(), 'vd': getVDocs()})
    return _uvec


def getVDocs():
    global _vdocs
    if _vdocs is not None:
        return _vdocs

    _vdocs = dp.vectorizeDocs(getDocs())
    return _vdocs


def getLinks():
    global _links
    if _links is not None:
        return _links
    lp = 'links.pkl'
    if os.path.exists(os.path.join(workDir, lp)):
        _links = loadFromFile(os.path.join(workDir, lp))
        return _links

    ppPath = 'preProcessed.pkl'
    if os.path.exists(os.path.join(workDir, ppPath)):
        _links = loadIfCan(dp.getAllLinks,  'links.pkl', arg=getProcMB())
    else:
        _links = loadIfCan(dp.getAllLinks,  'links.pkl', arg=getRawMB())
    return _links


def jsonDump(data, path=os.path.join(workDir, 'JSON_DUMP.json')):
    print(f'Saving data as json to: {path}')
    with open(path, 'w') as handle:
        json.dump(data, handle,indent=4)




