# MLModule
로또 자동추첨 및 분석 모듈에서 머신러닝을 담당하는 모듈입니다.

***

## Apriori.py

현재 로또 번호추출에 쓰이는 핵심적인 머신러닝은 연관분석입니다. 연관분석 기법을 로또 번호 자동추출 모듈의 핵심으로 정한 이유는 다음과 같습니다.

- 연관분석을 사용한 이유
  + 우선 연관 데이터 안에 존재하는 항목간의 연관규칙을 발견하는 것이 주 목적이다.
  + 연관성 분석의 시작은 하나 이상의 품목(여기서는 당첨번호이다.) 이 포함하는 다른 내역(누적된 당첨정보들) 을 가지고 하는것이다.
  + 규칙을 어떤 기준에 얽매이지 않고 세우기 때문에 로또의 자동번호추첨기의 성격과 비슷하게 만들어 낼 수 있는 것이다.
  
- 코딩설명

    + createD : 연관분석을 시작하기 전, 인자로 받은 dataSet에 대한 전처리가 이루어 지도록 하는 함수이다. 이 함수를 통해 반환되는 배열은 불가변이 된다.
    
```  
  def createD(dataSet):  # 인자로 받는 dataSet 의 형식은 List 형식이다.
    array = [] 
    for trans in dataSet: 
        for number in trans:
            if not [number] in array:
                array.append([number])
    array.sort()

    return map(frozenset,array)
```


   + scanData : 각 번호(1~45)에 대한 지지도(1등당첨에 얼마나 참여했는지) 를 계산해주는 함수이다.
    
```
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
    
```

   + GenApriori : returnList 에 넣을 핵심 데이터들을 가지치기하여 구하는 함수이다. 여기서 핵심데이터는 특정 지지도 이상의 데이터들만을 이야기한다. 즉, 당첨횟수가 가장 많고, 연관있는 숫자들끼리 묶어서 해당 집합의 연관성 정도까지 정보를 담아서 합해주는 것이다. 
```
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
```

   + Apriori : 지금까지 작성했던 위의 모든 함수들의 기능을 넣어 실제로 수행되는 함수이다. 여기서 핵심은 87번째 이다. 최종적으로 최소 지지도를 만족하는 빈발아이템의 집합을 찾아내어 집합을 다시 만들어 사용자에게 해당 *아이템의 지지도* 와 *아이템 구성* 들을 리턴시켜주는 함수이다. 
```
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
```

## KNN.py

머신러닝 기법 중 하나인 K-NN 머신러닝의 알고리즘의 원리를 기반으로 만든 파일입니다. 현재 가장 핵심적인 기능을 담당할 연관분석 기능 구현에 충실하기 위해 해당 파일은 아직 만들어지지 않았습니다. 추후에 계속 개발할 예정입니다.

- K 최근접 이웃 알고리즘을 사용하는 이유
  + 고객 개인이 가장 선호하는 번호를 고르도록 하는 기능을 추가할 경우, 그에 맞게 가장 확률이 높은 번호를 추출해줄 수 있는 머신러닝 기법입니다.
  + 연관분석과는 달리, 기준이 정해져 있어 당첨확률이 높은 번호들의 분류가 더 효율적일 수 있습니다.
  
- K 최근접 이웃 알고리즘의 단점
  + 연관분석과는 달리, 해당 알고리즘은 반드시 기준(K) 가 있어야 합니다.
  + 기준을 반드시 정해야 분석을 할 수 있다는 점은, 즉 번호(K) 가 반드시 당첨된다는 전제를 가지고 있어야 한다는 점이 됩니다. 이는 로또 번호추출의 원리에 매우 위배되는 성격입니다.
