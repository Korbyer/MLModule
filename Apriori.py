
def createD(dataSet):
    array = []
    for trans in dataSet:
        for number in trans:
            if not [number] in array:
                array.append([number])
    array.sort()

    return map(frozenset,array)

def scanData(data, ck, minSupport):
    group = {}
    sk=list(ck)
    numOfItems=0
    print(ck)
    for item in data:
        numOfItems+=1
        for map in sk:
            if map.issubset(item):
                if map not in group:
                    group[map] = 1
                else:
                    group[map] += 1

    returnList = []
    supportData = {}
    for key, value in group.items():
        support = value / numOfItems
        if support >= minSupport:
            returnList.insert(0, key)
        supportData[key] = support
    return returnList,supportData



def GenApriori(data, k):
    returnList = []
    lenData = len(data)
    for i in range(lenData):
        for j in range(i + 1, lenData):
            List1 = list(data[i])[:k - 2];List2 = list(data[j])[:k - 2]
            List1.sort();List2.sort()
            if List1 == List2:
                returnList.append(data[i] | data[j])
    return returnList





def apriori(data,minSupport=0.18):
    C = createD(data)
    D = map(set, data)
    List1, supportData = scanData(D, C, minSupport)
    L = [List1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = GenApriori(L[k - 2], k)

        Lk, supK = scanData(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

def genRules(L,supportData,minConf=0.7):
    ruleList=[]
    sk=list(L)
    for i in range(1,len(sk)):
        for freqSet in sk[i]:
            set=[frozenset([item]) for item in freqSet]
            if i>1:
                rulesFromResult(freqSet,set,supportData,ruleList,minConf)
            else:
                calcConf(freqSet,set,supportData,ruleList,minConf)
    return ruleList

def calcConf(freqSet,set,supportData,block,minConf=0.7):
    setD=[]
    for result in set:
        confidence=supportData[freqSet]/supportData[freqSet-result]
        if confidence>=minConf :
            print(freqSet-result,"-->",result," Confidence : ",confidence)
            block.append((freqSet-result),result,confidence)
            setD.append(result)
    return setD


def rulesFromResult(freqSet,set,supportData,block,minConf=0.7):
    m=len(set[0])
    if(len(freqSet)>(m+1)):
        x=GenApriori(set,m+1)
        x=calcConf(freqSet,x,supportData,block,minConf)
        if(len(x)>1):
            rulesFromResult(freqSet,x,supportData,block,minConf)


from LottoModule import GetInfo as info
from LottoModule import Update as up

a=info.makeDataSet(up.ReturnLastDrwNo())
L,support=apriori(a)
print("L:" + str(L))
print(".........................")
print("suppData:" + str(support))

rules=genRules(L,support,minConf=0.7)
print(rules)