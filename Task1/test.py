import json
me = wim =  []
with open('Task1/tmp/addr.json','r') as f:
    me = json.load(f)
with open('Task1/tmp/WIMLSaddr.json','r') as f:
    wim = json.load(f)

diff = set()
dup = 0

print('start+')
for x in me:
    if x not in wim:
        if x in diff:
            dup+=1
        diff.update(x)


print("len dif:",len(x))
print(dup,"dups")