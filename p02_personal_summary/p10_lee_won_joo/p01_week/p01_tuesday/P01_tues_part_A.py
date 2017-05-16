"""
파이썬은 리스트,세트 딕셔너리와 같은 자료구조의 장점은 사용이 편리하다는 점
문제는, 검색, 정렬, 순서, 여과 등에 대한 질문이 생길 때 !

위 질문들을 다루며, collections 모듈에 대한 사용법 공부하기

"""


print('1.1 시퀀스를 개별 변수로 나누기')  #언패킹

print('### 문제 , N개의 요소를 가진 튜플이나 시퀀스가 있을 때, 이를 변수 N개로 나눠야 한다.')

# 모든 시퀀스는 간단한 할당문을 사용해서 개별 변수로 나눌 수 있다.
# 주의 사항으로는, 변수의 개수 = 시퀀스의 수 가 일치해야 한다는 것

p = (4,5)
x , y = p
print(x)
print(y)

# data = ['ACME', 50, 91.1, (2012, 12, 21)]
# name, shares, price, date = data
# print(name) #ACME
# print(date)#(2012, 12, 21)

# name, shares, price, (year,mon, day) = data
# print(name)
# print(date)
# print(year)
# print(mon)
# print(day)

print('요소 개수가 일치하지 않으면 다음과 같은 에러 발생')

# p = (4,5)
# x,y,z = p
#ValueError: not enough values to unpack (expected 3, got 2)



print('##############################################토론################################################3')

s = 'Hello'
a,b,c,d,e, = s
print(a)


data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
_, shares, price, _ = data
print(shares)
print(price)

#즉, 원래 언패킹할때는 수를 일치해야 가능하니까, 일일이 모두 다 변수명을 지정해서 빼줬었는데
#할당하고 싶지 않은 변수명은 _ 를 통해서 제낀다는 소리
# 변수명을 할당할 때에는 항상, 다른곳에ㅓ 이미 사용하고 있지는 않은지 주의하기


print('########################################1.2 임의 순환체의 요소 나누기################################')
print('#######################################문제 ################################')
print('#####################순환체를 언패킹하려는데, 요소가 N개 이상 포함되어 "값이 너무 많습니다."예외 발생한다. 이 경우엔? ################################')

# 별 표현식 활용하기
import math
def drop_first_last(grades):
    first, *middle, last = grades
    return sum(middle)/len(middle)
grade = (5,20,40,60,80,100)
print(drop_first_last(grade))  # 50.0


# 또 다른 예,
print('##################################################################################')
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record
print(name)
print(email)
print(phone_numbers)


# *가 앞으로 올 때
print('##################################################################################')
*tra, current = [10,8,7,1,9,5,10,3]
print(tra)
print(current)

print('##################################################################################')
# 패턴이나 구조가 있는 구조의 요소 나누기
# 다음과 같은 튜플이 있을 때
records = [
    ('foo',1,2),
    ('bar','hello'),
    ('foo',3,4)]

def do_foo(x,y):
    print('foo',x,y)
def do_bar(s):
    print('bar')
for tag, *args in records:     # record의 패턴이 [ (tag, values1,values2,values3 ...),(tag, values1,values2,values3 ...) ... ] 과 같기에
    if tag == 'foo':           # tag가 foo라면
        print('do_foo')
        do_foo(*args)          # values1~..values N 까지 출력하라.
    elif tag == 'bar':
        print('do_bar')
        do_bar(*args)


print('##################################################################################')
# 별표는 문자열 프로세싱에 사용해도 편리하다. 다음과 같은 문법이 가능하다.

line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
uname, *fields, homedir, sh = line.split(':')

print(uname)  #nobody
print(homedir) #/var/empty
print(sh)  #usr/bin/false
print(fields)

print('##################################################################################')
# 언패킹 이후, 특정 값을 버리고 싶다면?
# _ 또는 ign(ignored)  를 활용한다

record = ['ACME', 50, 123.1, (2012, 12, 21)]
name, *_, (*_,day) = record     #record = ['ACME', X, X, (21)]
print(name)
print(day)  #class int타입

print('*를 뒤로 보내보기')

name, *_, (year , *_) = record
print(name)
print(year)


print('##################################################################################')
# 다음과 같은 리스트가 있을 대, 손쉽게 머리와 꼬리 부분 분리 하기

items = [1, 10, 7, 4, 5, 9]
head, *tail = items
print(head)
print(tail)
# 재귀 알고리즘으로 머리와 꼬리 부분 분리한 후, 총합 구하기

def sum(items):
    head, *tail = items
    return head + sum(tail) if tail else head
print(sum(items))


print('####################################1.3 마지막 N개 아이템 유지##############################################')
# from collections import deque
#
# def search(lines, pattern, history=5):
#     previous_line = deque(maxlen=history)
#     for line in lines:
#         if pattern in line:
#             yield line, previous_line
#         previous_line.append(line)
#
# if __name__ == '__main__':
#     with open('d:/data/winter7.txt') as f:
#         for line, prevlines in search(f, 'elsa', 5):
#             for pline in prevlines:
#                 print(pline, end = '')
#             print(line, end='')
#             print('-'*20)
# 위 함수는 사용방법을 잘 모르겠음.

print('############################################ 토론 ############################################3')

#아이템을 찾는 코드 : yield를 포함한 제너레이터 함수를 활용하기
#검색과정과 결과를 사용하는 코드를 분리할 수 있다
from collections import deque
q = deque(maxlen=3)
q.append(1)
q.append(2)
q.append(3)
print(q)

q.append(4)    # que의 maxlen은 3까지이기 때문에  1 2 3 -> 2 3 4 로 변함
print(q)
q.append(5)
print(q)     # 3 4 5


print('################ 더 일반적인 que의 구조체를 필요할 때 deque사용법')
#que의 maxlen의 제한을 두지 않는다.
from collections import  deque
q = deque() #제한이 없는 que구조체 생성
q.append(1)
q.append(2)
q.append(3)
print(q)  # deque([1, 2, 3])
q.appendleft(4)
print(q)  # deque([4, 1, 2, 3])

print(q.pop())
print(q)
print(q.popleft())
print(q)
# que의 양 끝에 아이템을 넣거나, 뺴는 작업에는 시간복잡도 O(1)이 소요된다. 이는 O(N)이 소요되는 리스트의 작업에 비해 훨씬 빠르다.


"""

1.4 N개의 아이템의 최대 혹은 최소값 찾기

필요한것

모듈 : heapq
함수 : heapq.nlargest(N, var)         # 가장 큰 값
        heapq.nsmallest(N, var)       # 가장 작은 값                                   데이터가 적을때 유리
        heapq.heapify(var)            # heap정렬
        heapq.heappop(var)            # var[0]에 위치한 값을 pop시킨다.                데이터가 많을때 유리
"""

# 컬렉션 내부에서 가장 크거나 작은 N개의 아이템을 찾아야 한다.

import heapq

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums)) #[42, 37, 23]
print(heapq.nsmallest(3, nums)) #[-4, 1, 2]

# 두 함수 모두 좀더 복잡한 구조에서 사용하기 쉽도록 키 파라미터를 받을 수 있다.
import heapq

portfolio = [
    {'name': 'IBM', 'shares': 100, 'price':91.1},
{'name': 'AAPL', 'shares': 50, 'price':543.22},
{'name': 'FB', 'shares': 200, 'price':21.09},
{'name': 'HPQ', 'shares': 35, 'price':31.75},
{'name': 'YHOO', 'shares': 45, 'price':16.35},
{'name': 'ACME', 'shares': 75, 'price':115.65}
]

cheap = heapq.nsmallest(2, portfolio, key = lambda s: s['price'] )  # key를 price로 잡고, sorting해서 뽑는듯?
expensive = heapq.nlargest(1, portfolio, key = lambda s: s['price'] )

print(cheap)
print(expensive)

# 내부 구조 좀더 살펴보기
# 데이터를 힙으로 정렬시켜 놓는 리스트로 변환하기

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(type(nums))
import heapq
heap = nums      #nums와 같은 데이터를 지닌 heap이라는 리스트 생성
heapq.heapify(heap)      #정렬되지 않은 heap변수에 heap정렬을 적용
print(heap)     #[-4, 2, 1, 23, 7, 2, 18, 23, 42, 37, 8]

# heapify된 리스트의 0번째 , 즉 heap[0]은 항상 가장 작은 값을 지닌 원소가 위치하게 되어있다.
# 이를 이용하여 가장 작은 아이템 N개를 찾아 낼 수 있다.
# 가장 작은 아이템 3개 찾기     heapq.heappop() 활용하기

print(heapq.heappop(heap))  #-4
print(heapq.heappop(heap))  #1
print(heapq.heappop(heap))  #2

# 만일 N이 1개인 최소값 이나 최대값을 구하고자 한다면 min과 max를 사용하는 것이 편리함.
# 만일 N의 크기 와 컬렉션 크기가 비슷해지면 , 1. 정렬하고    2. [:N]식으로 사용하는 것이 더 편리함]


"""
1.5 우선순위 큐 구현

문제
주어진 우선 순위에 따라 아이템을 정렬하는 큐를 구현하고
항상 우선 순위가 가장 높은 아이템을 먼저 pop하도록 만들어야 한다.

"""


print('###################################################1. 5 우선순위 큐 구현 ##################################')
import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []  #자기 자신을 호출하는 queue메소드 = 빈 리스트로 초기화

        self._index = 0  #index = 0으로 설정

    def push(self,item, priority):  #푸시하는 기능
        heapq.heappush(self._queue, (-priority, self._index, item))              #  heap = (self._qeue) , item = (-priority, self._index, item)
        self._index += 1    # push하고 index값을 1씩 증가

    def pop(self):
        return heapq.heappop(self._queue)[-1]  #-1은 맨 마지막 값을 의미함,  heap으로 정렬된 시퀀스상태에서 마지막값 = 우선순위가 높은 값 이므로?


class Item:
    def __init__(self, name):
        self.name = name
    def __repr__(self): #repr메소드 호출             repr : 파이썬 인터프리터가 해당 객체를 인식할 수 있는 공식적인 문자열로 나타낼 때 사용한다.
        return 'Item({!r})'.format(self.name)


q = PriorityQueue()   #PriorityQueue를 q라는 변수명으로 인스턴스화 한다.

q.push(Item('foo'), 1)
q.push(Item('bar'), 5)
q.push(Item('spam'), 4)
q.push(Item('grok'), 1)

print(q.pop(),q.pop(),q.pop(),q.pop())
# a = Item('foo')
# b = Item('bar')


















print('############가장 우선순위가 높은것(가장 작은 값을 지닌 value)부터 제거하기##########33')
import heapq
a= []
heapq.heappush(a,5) # 5
print('1단계',a)
heapq.heappush(a,3)
print('2단계',a)    # 3,5
heapq.heappush(a,7)
print('3단계',a)
heapq.heappush(a,4)
print('최종',a)

assert a[0] == heapq.nsmallest(1,a)[0] == 3

print('Before: ', a)

a.sort()
print('After : ', a)

# print(heapq.heappop(a),heapq.heappop(a),heapq.heappop(a),heapq.heappop(a),a)

#결과로 만들어지는 list를 heapq외부에서도 쉽게 사용할 수 있다?



"""
1.6 딕셔너리의 키를 여러 값에 매핑하기

문제
딕셔너리의 키를 하나 이상의 값에 매핑하고 싶다면!?
소위 말하는 mltidict를 하려면?

키에 여러 값을 매핑하려면, 그 여러 값을 리스트 or 세트와 같은 컨테이너에 따로 저장해 두어야 한다. 
예를 들어 다음과 같은 딕셔너리를 만들 수 있다.

사용 목적에 따라 다음을 결정한다.

1. 아이템의 삽입 순서를 지키려면?
  ---> 리스트 형태의 multidict
2. 순서는 상관없이 중복을 없애려면?
  ---> 세트 형태의 multidict

collections 모듈의 defaultdict을 활용한다.

defaultdict의 기능 중 첫번째 값을 자동으로 초기화 하는 것이 있어서 사용자는 아이템 추가에만 집중할 수 있다.
"""

d = {                     # 리스트사용
    'a': [1, 2, 3],
    'b': [4, 5]

}

e = {                    # 세트 사용
    'a' : {1,2,3},
    'b' : {4,5}
}


print('############3 multidict 하기  - -------------- defaultdict활용')

from collections import defaultdict

dlist = defaultdict(list)
dlist['a'].append(1)
dlist['a'].append(2)
dlist['b'].append(4)
dlist['b'].append(6)

dset = defaultdict(set)
dset['a'].add(1)
dset['a'].add(2)
dset['b'].add(4)
dset['b'].add(6)

print(dset)
# 위 같은 기능으로 기본기능인 setdefault있으나, d = [] 이렇게 항상 새로운 인스턴스 생성해야 함. 부자연스럽
# 위처럼 하나의 키가 여러 값을 지니는 딕셔너리 만드는 것은 어렵지 않으나, 초기화를 스스로 하는 기능을 넣으려면 복잡한 과정을 걸쳐야 한다.
# 원래 같았으면 다음과 같이 작성해야 한다.


#기본 기능
# d = {}
# for key, value in pairs:
#     if key not in d:
#         d[key] = []
#     d[key].append(value)


#defaultdict 기능

# d = defaultdict(list)
# for key, value in pairs:
#     d[key].append(value)

#defaultdict기능은 레코드를 하나로 묶는 문제와 깊은 관련이 있다.



"""
1.7 딕셔너리 순서 유지

문제는?
딕셔너리 만들고, 순환이나 직렬화할 때 순서를 조절하고 싶다면??

>> 딕셔너리 내부 아이템의 순서를 조절하려면 collections 모듈의 OrderedDict를 사용한다.
이 모듈을 사용하면 삽입 초기의 순서를 그대로 기억한다.

주의사항?
OrderedDict는 더블 링크드 리스트로 삽ㅂ입 순서와 관련있는 키를 기억한다.
새로운 아이템 삽입하면 List의 맨 끝에 위치하며 키에 값을 재할당할지라도 순서는 변하지 않는다.
하지만 더블 링크드 리스트이기에, 크기가 일반 dict에 비해 2배로 크다. 따라서 크기가 큰 데이터 구조체를 Orderdict으로
만들 경우 추가적인 메모리 소비 고민해봐야함.

"""

from collections import OrderedDict

d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4

#Outputs foo 1 bar 2 spam 3  grok 4
for key in d:
    print(key, d[key])

# OrderedDict은 나중에 직렬화 or 다른포맷으로 인코딩할 매핑 만들때 유용함.
print('#########################json ########################3')
import json
print(json.dumps(d))
print(d)





print('##########################1.8 딕셔너리 계산##########################3')

"""
딕셔너리 데이터에 여러 계산을 수행하고 싶다면? 
ex) 최소값, 최대값, 정렬 등..

"""

print('딕셔너리에 주식 이름과 가격이 들어있다고 가정한다면')

prices = {

    'A':45.23,
    'B':612.78,
    'C':205.55,
    'D':37.20,
    'E':10.75
}


#일반적으로 최소값을 찾고자 한다면 다음과 같이 접근할 것
min(prices)   # return 'A'
max(prices)   # return 'E'

#값에 대한 계산을 원하기에, values()메소드를 통해 값에 접근해보자.
min(prices.values())  #return 10.75
max(prices.values())  #return 612.78

#그러나, 실제로 출력되는 원하는 값은, 단순히 values뿐만 아니라 키-밸류 정보까지 알고 싶다면?
min(prices, key=lambda k: prices[k])  #return E
max(prices, key=lambda k: prices[k])  #return B


#최소값을 위해 한번더 살펴본다.
min_value = prices[min(prices, key=lambda k: prices[k])]
# min_value = d[k] 와 같은 형태 , 즉 min_value = prices[10.75] >>> (10.75, 'E')
print(min_value)

#또 다른 방법은 zip()으로 페어 뒤집어 계산하기이다.
#이렇게 하면, 데이터 축소화 정렬작업을 명령어 하나로 할 수 있다.
print(min(zip(prices.values(),prices.keys())))  # 10.75, 'E'
# zip으로 키 -밸류 >  밸류 - 키 로 뒤집어 주고, 밸류들 중 최소값을 찾은 것..



# 만일 동일한 value를 지녔을 때 zip으로 뒤집었을 경우엔 어떨까
# >> 키의 값이 가장 작거나 또는 가장 큰 키를 가지고 있는 엔트리를 반환한다.




print('##########################       1.9 두 딕셔너리의 유사점 찾기         ###################')

"""
두 딕셔너리가 있고, 여기서 유사점을 찾고 싶다. (동일한 키, 동일한 값 등..)
"""

#다음 두 딕셔너리를 보자.

a = {
    'x' : 1,
    'y' : 2,
    'z' : 3,
}

b = {
    'w' : 10,
    'x' : 11,
    'y' : 2
}

#두 딕셔너리의 유사점을 찾으려면 keys()와 items() 메소드에 집합 연산을 수행한다.

#동일한 키 찾기
a.keys() & b.keys()    # return { 'x', 'y' }

#a에만 있고 b에는 없는 키 찾기
a.keys() - b.keys()    # return { 'z' }

#(키,값)이 동일한 것 찾기
a.items() & b.items()   # return { ('y', 2) }

#특정 키를 제거한 새로운 딕셔너리 만들기

c = {key:a[key] for key in a.keys() - {'z', 'w'} } # c에 key:value 생성/  a_dict의 키 중 'z'와'w'를 제외한 키만 key에 넣자
#keys() 메소드 = 키를 노출하는 키-뷰 객체를 반환
#키-뷰 객체는 집합 연산 기능이 있다. ex) 차집합,합집합,교집합,여집합 등..
#그래서 다음이 가능했음.   a.keys() - {'z', 'w'}


print(c) # {'y': 2, 'x': 1}


print('###########################################################################')
print('######################           1.10 순서를 깨지않고 시퀀스의 중복 없애기       ###################')

"""
시퀀스에서 중복된 값을 없애고 싶지만, 아이템의 순서는 유지하고 싶다면?

"""
print('##### 시퀀스의 값이 해시가 가능할때 세트와 제너레이터 를 사용해서 쉽게 해결하기     ########')
def dedupe(items):
    seen = set()     # seen이라는 set선언
    for item in items:
        if item not in seen:      #만일, item이 set안에 없다면
            yield item            # 생성기 만들기, 값을 반환하더라도 현재의 상태를 유지하고 있는 것..?
            seen.add(item)

a = [1, 5, 2, 1, 9, 1, 5, 10]
print(list(dedupe(a)))       # return      [1, 5, 2, 9, 10]


print('############ 해시가 불가능한 dict의 중복을 없애려면      ##################')
def dedupe(items, key = None):
    seen = set()     # seen이라는 set선언
    for item in items:
        val = item if key is None else key(item)
        if item not in seen:      #만일, item이 set안에 없다면
            yield item            # 생성기 만들기, 값을 반환하더라도 현재의 상태를 유지하고 있는 것..?
            seen.add(val)

a = [1, 5, 2, 1, 9, 1, 5, 10]
print(list(dedupe(a)))       # return      [1, 5, 2, 9, 10]
