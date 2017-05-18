            #1.1 시퀀스를 개별 변수로 나누기

#문제 : N개의 요소를 가진 튜플이나 시퀀스를 N개로 나누기

#주의할 점 : 
#    1) 변수의 개수가 시퀀스가 가진 요소의 개수와 일치해야한다.

    #예제1
p = (4,5)
x, y = p
x
#(실행결과) 4
y
#(실행결과) 5

 
     #예제2
data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, data = data
name
#(실행결과) 'ACME'

 
     #예제3 
data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, (year, mon, day) = data
year
#(실행결과) 2012

 
     #예제4 문자열
s='Hello'
a,b,c,d,e=s
a
#(실행결과) 'H'

 
     #예제5 특정값 무시
data = ['ACME', 50, 91.1, (2012,12,21)]
_, shares, price,_ =data
price                     
#(실행결과) 91.1

 
         #1.2 임의의 (길이를 알 수 없는) 순환체의 요소 나누기

#문제 시퀀스의 요소가 N개 이상이라 "값이 너무 많습니다" 라는 예외가 발생할 때

#해결 방법 : 
    #1) *표현식 사용 

    # 예제1
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record
name
#(실행결과) 'Dave'
phone_numbers
#(실행결과) ['773-555-1212', '847-555-1212']


    #예제2 *표현식을 맨 앞에 사용할 경우

*a, b = [10,8,7,1,9,5,10,3]
a
#(실행결과) [10, 8, 7, 1, 9, 5, 10]
b
#(실행결과) 3

 
     #예제3 시퀀스 요소의 개수가 일정하지 않은 경우
records = [('foo', 1, 2), ('bar', 'hello'), ('foo',3,4)]

def do_foo(x,y):
    print('foo',x,y)

def do_bar(s):
    print('bar', s)
    
for tag, *args in records:
                                        #print (tag) 
                                    #        foo
                                    #        bar
                                    #        foo
    if tag=='foo':
        do_foo(*args)
    elif tag =='bar':
        do_bar(*args)
 
       
    #예제4 여러개의 값 무시하기(버리기)
record = ('ACME', 50, 123.45, (12, 18, 2012))
name, *_, (*_, year) = record
name
#(실행결과) 'ACME'
year
#(실행결과) 2012

 
     #예제5 재귀알고리즘
items = [1, 10, 7, 4, 5, 9]
def s(items):
    head, *tail = items
    return head + s(tail) if tail else head
           # 1      
           #    +   10 
           #    +   7  
           #    +   4  
           #    +   5
           #                           + 9
                    
s(items)
#(실행결과) 36

 
 
         #1.3 마지막 N개 아이템 유지
         
# 문제 : 마지막으로 발견한 N개의 아이템을 유지하고 싶을 때

# deque 활용

    #예제1
    
import csv
from collections import deque
def search(lines, pattern, history=5):
    prev_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, prev_lines
        prev_lines.append(line)
        
if __name__=='__main__':
    f= open("d:\data\emp.csv",'r') 
    for line, prevlines in search(f, 'SCOTT', 5):
        for pline in prevlines:
            print(pline, end='') #end = ' ' 출력함수가 줄을 바꾼 것을 없애고 한 줄로 이어주는 역할
                                 #sep= ' ' 은 콤마로 이어진 명령어에서 띄어쓰기가 된 것을 삭제해주는 역할
        print(line, end='')
        print('-'*20)
 
#(실행결과)
#7844,TURNER,SALESMAN,7698,1981-08-21 0:00,1500,0,30
#7900,JAMES,CLERK,7698,1981-12-11 0:00,950,,30
#7521,WARD,SALESMAN,7698,1981-02-23 0:00,1250,500,30
#7902,FORD,ANALYST,7566,1981-12-11 0:00,3000,,20
#7369,SMITH,CLERK,7902,1980-12-09 0:00,800,,20
#7788,SCOTT,ANALYST,7566,1982-12-22 0:00,3000,,20


    #예제2
q = deque(maxlen=3)     # deque는 큐 구조체가 필요할 때 사용할 수 있다.
                        # deque(maxlen=N)으로 고정 크기 큐를 생성할 수 있다.
q.append(1)
q.append(2)
q.append(3)    
q
#(실행결과) deque([1, 2, 3])

q.append(4)
q
#(실행결과) deque([2, 3, 4])
    # 큐가 찬 상태에서 새 아이템을 넣으면 첫 아이템이 자동으로 삭제된다.


    #예제3 deque의 최대 크기를 지정하지 않으면 제약없이 양쪽에 아이템을 넣거나 뺄 수 있다.
q=deque()
q.append(1)
q.append(2)
q.append(3)
q
#(실행결과) deque([1, 2, 3])
q.appendleft(4)
q
#(실행결과)  deque([4, 1, 2, 3])
q.pop() 
#(실행결과) 3
q
#(실행결과) deque([4, 1, 2]) --pop()은 시퀀스의 오른쪽 항목을 반환한 후 그 항목을 제거한다.
q.popleft()
#(실행결과) 4
q
#(실행결과) deque([1, 2])



            #1.4 N 아이템의 최대 혹은 최소값 찾기
# 문제: 컬렉션 내부에서 가장 크거나 작은 N개의 아이템을 찾아야 한다.
# 사용 함수: heapq 모듈의 nlargest(), nsmallest()

    #예제1
import heapq

nums=[1,8,2,23,17,-4,18,23,42,37,2]

print(heapq.nlargest(3,nums)) 
#(실행결과) [42, 37, 23]
print(heapq.nsmallest(3,nums))
#(실행결과) [-4, 1, 2]


    #예제2

import heapq  
  
portfolio = [  
            {'name': 'IBM', 'shares': 100, 'price': 91.1},  
            {'name': 'AAPL', 'shares': 50, 'price': 543.22},  
            {'name': 'FB', 'shares': 200, 'price': 21.09},  
            {'name': 'HPQ', 'shares': 35, 'price': 31.75},  
            {'name': 'YHOO', 'shares': 45, 'price': 16.35},  
            {'name': 'ACME', 'shares': 75, 'price': 115.65}  ]
    
  
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])  
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])  

print(cheap)  
#(실행결과) [{'name': 'YHOO', 'shares': 45, 'price': 16.35}, {'name': 'FB', 'shares': 200, 'price': 21.09}, {'name': 'HPQ', 'shares': 35, 'price': 31.75}]

print(expensive)  
#(실행결과) [{'name': 'AAPL', 'shares': 50, 'price': 543.22}, {'name': 'ACME', 'shares': 75, 'price': 115.65}, {'name': 'IBM', 'shares': 100, 'price': 91.1}]


    #예제3 
nums = [1,8,2,23,7,-4,18,23,42,37,2]
import heapq
heap = list(nums)
heapq.heapify(heap) #heapify로 정렬하면 heap[0]이 가장 작은 아이템이 된다.
heap
#(실행결과) [-4, 2, 1, 23, 7, 2, 18, 23, 42, 37, 8]
heapq.heappop(heap) #첫번째 아이템을 반환하고 그 자리를 다음 아이템으로 치환
#(실행결과) -4
heap
#(실행결과) [1, 2, 2, 23, 7, 8, 18, 23, 42, 37]

# nlargest()와 nsmallest()함수는 찾고자 하는 아이템의 개수가 상대적으로 작을 때 가장 알맞다.

          
          
          #1.5 우선 순위 큐 구현
          
#문제 주어진 우선순위에 따라 아이템을 정렬하는 큐를 구현하고 항상 우선 순위가 가장 높은 아이템을 먼저 팝하도록 만들기


    #예제1 heapq 모듈 사용          

import heapq

class PriorityQueue:
    def __init__(self):
        self._queue=[]
        self._index=0
        
    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item)) # -로 가장 큰 수를 가장 작은 수로 만들어서 가장 큰수가 첫번째로 정렬되게 함 
        self._index +=1
        
    def pop(self):
        return heapq.heappop(self._queue)[-1] # heappop()은 첫번째 아이템을 반환하고 그 자리를 다음 아이템으로 치환
                                              # [-1]은 가장 마지막 요소인 item만 반환하게 한다
class Item:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return 'Item({!r})'.format(self.name)
    
q = PriorityQueue()
q.push(Item('foo'),1)
q.push(Item('bar'),5)
q.push(Item('spam'),4)
q.push(Item('grok'),1)

print(q.pop())
#(실행결과) Item('bar')

    # 예제2 우선순위를 이용하여 비교하기
    
a = (1, Item('foo'))
b = (5, Item('bar'))
a < b
#(실행결과) True
c=(1,Item('grok'))
a<c   #← 안됨

a = (1,0, Item('foo'))  # 인덱스를 추가해서 비교
b = (5,1, Item('bar'))
c = (1,2, Item('grok'))
a<b
#(실행결과) True
a<c
#(실행결과) True

 

            #1.6 딕셔너리의 키를 여러 값에 매핑하기
            
#문제 딕셔너리의 키를 하나 이상의 값(value)에 매핑

    #예제1
d={'a':[1,2,3],
   'b':[4,5]}     # 리스트 : 아이템의 삽입 순서를 지켜야 할 경우                     

e={'a':{1,2,3},
   'b':{4,5}}     # set : 순서 상관없이 중복을 없애고 싶을 때

   
   #예제2 collection 모듈의 defaultdict 활용

#defaultdict는 처음 값을 자동으로 초기화해준다. d[key]=[]를 할 필요 없음.

from collections import defaultdict 

d=defaultdict(list) #딕셔너리에서도 append 가능!
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)
print(d)   
#(실행결과) defaultdict(<class 'list'>, {'a': [1, 2], 'b': [4]})
print(d['a'])
#(실행결과) [1, 2]
print(d['a'][0])
#(실행결과) 1
 
d=defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['b'].add(4)
print(d)
#(실행결과) defaultdict(<class 'set'>, {'a': {1, 2}, 'b': {4}})
print(d['a']) 
#(실행결과) {1, 2}

    #예제2 setdefault 사용
d={}
d.setdefault('a',[]).append(1)
d.setdefault('a',[]).append(2)
d.setdefault('b',[]).append(4)
print(d)
#(실행결과) {'a': [1, 2], 'b': [4]}



            #1.7 딕셔너리 순서 유지
#문제 딕셔너리를 만들고, 딕셔너리 내부 아이템의 순서 조절

    #예제1 collections 모듈의 OrderedDict 사용 

#OrderedDict는 삽입 초기의 순서를 그대로 기억한다.

from collections import OrderedDict

d=OrderedDict()
d['foo']=1
d['bar']=2
d['spam']=3
d['grok']=4
print(d)
#(실행결과) OrderedDict([('foo', 1), ('bar', 2), ('spam', 3), ('grok', 4)])

for key in d:
    print(key, d[key])
#(실행결과) 
#foo 1
#bar 2
#spam 3
#grok 4

import json
json.dumps(d)
    
#(실행결과) '{"foo": 1, "bar": 2, "spam": 3, "grok": 4}'

#근데 이게 왜 순서조절인지 모르겠네?!
 
 

            #1.8 딕셔너리 계산
#문제 딕셔너리 데이터에 여러 계산을 수행할 때

    #예제1 최소주가, 최대주가 찾기 
price = {'ACME': 45.23, 'AAPL': 612.78, 'IBM': 205.55, 'HPQ': 37.20, 'FB': 10.75}
min_price=min(zip(price.values(),price.keys())) # zip() 으로 key와 value 위치 바꾸기
print(min_price)
#(실행결과) (10.75, 'FB') 
max_price=max(zip(price.values(),price.keys())) # zip() 으로 key와 value 위치 바꾸기
print(max_price)
#(실행결과) (612.78, 'AAPL')

    #예제2 데이터에 순서 매기기
price_sorted = sorted(zip(price.values(),price.keys()))
print(price_sorted)
#(실행결과) [(10.75, 'FB'), (37.2, 'HPQ'), (45.23, 'ACME'), (205.55, 'IBM'), (612.78, 'AAPL')] 

    #예제3 zip()은 한번만 소비할 수있는 이터레이터를 생성
a=zip(price.values(),price.keys())
print(min(a))
#(실행결과) (10.75, 'FB')
print(max(a)) # → 안됨. zip()은 한번만 소비되는 이터레이터

min(price)
#(실행결과) 'AAPL' # 딕셔너리에서 key 값만 리턴. key값 중 가장 작은 'AAPL'가 리턴됨
max(price) 
#(실행결과) 'IBM' # key값 중 가장 큰 'IBM'이 리턴됨

min(price, key=lambda k: price[k]) # 가장 낮은 가격의 주식 이름을 리턴해라
#(실행결과) 'FB'
#진짜 'FB'가 가장 가격이 낮은지 확인해보자
min_value=price[min(price, key=lambda k: price[k])]
print(min_value)
#(실행결과) 10.75
max(price, key=lambda k: price[k]) # 가장 높은 가격의 주식 이름을 리턴해라
#(실행결과) 'AAPL'


 
         #1.9 두 딕셔너리의 유사점 찾기
#문제 두 딕셔너리가 있고 여기서 key와 value가 동일한지 알아보고 싶을 때
#해결 방법 : 집합 연산을 활용

    #예제1
a={'x':1, 'y':2, 'z':3}
b={'w':10, 'x':11, 'y':2}

# 동일한 키 찾기
a.keys()&b.keys()
#(실행결과) {'x', 'y'}

# a에만 있고 b에는 없는 키 찾기
a.keys()-b.keys()
#(실행결과)  {'z'}

#(키, 값)이 동일한 것 찾기
a.items()&b.items()
#(실행결과) {('y', 2)}

# 특정 키를 제거한 새로운 딕셔너리 만들기
c={key: a[key] for key in a.keys() - {'z', 'w'}} # key는 집합 연산가능
print(c)
#(실행결과) {'y': 2, 'x': 1}



            #1.10 순서를 깨지 않고 시퀀스의 중복 없애기
# 해결방법 : set() 과 제너레이터 사용

    # 예제1
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)
                        
a=[1,5,10,2,1,9,1,5,10]
list(dedupe(a))
#(실행결과) [1, 5, 10, 2, 9]

# dic의 경우 중복을 없애려면?

def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        print(val)
        if val not in seen:
            yield item
            seen.add(val)

a = [{'x':1,'y':2}, {'x':1, 'y':3},{'x':1, 'y':2}, {'x':2, 'y':4}]
list(dedupe(a, key= lambda d: (d['x'],d['y'])))
#(실행결과) [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]
list(dedupe(a, key= lambda d: (d['x'])))
#(실행결과) [{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]



            #1.11 슬라이스 이름 붙이기
            
# 문제 slice가 너무 많은 경우
    
    #예제1
record='01234567892365475.25'
shares=slice(1,9)
price=slice(10,20)
cost=int(record[shares])*float(record[price])
print(cost)
#(실행결과) 29203395753469.5

 
     #예제2 ?
a=slice(10,50,2)
a.start  
#(실행결과) 10
a.stop 
#(실행결과) 50
a.step
#(실행결과) 2

s='HelloWorld'
a.indices(len(s))
for i in range(*a.indices(len(s))):
    print(s[i])

#(실행결과) ? 물어보기



            #1.12 시퀀스에 가장 많은 아이템 찾기

    #예제1 collections.counter의 most_common()메소드 사용

words = ['look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',  
         'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',  
         'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',  
         'my', 'eyes', "you're", 'under'  ]

from collections import Counter
word_counts = Counter(words)
top_three = word_counts.most_common(3)
print(top_three)
#(실행결과) [('eyes', 8), ('the', 5), ('look', 4)]

morewords = ['why','are','you','not','looking','in','my','eyes'] 
for word in morewords:
    word_counts[word] += 1
               
word_counts['eyes']               
#(실행결과) 9

     # 예제2 update() 메소드 사용
word_counts.update(morewords)
word_counts['eyes']               
#(실행결과) 10

     # 예제3 counter 인스턴스의 기능 활용
a= Counter(words)
b= Counter(morewords)
c= a+b
print(c)
#(실행결과) Counter({'eyes': 9, 'the': 5, 'look': 4, 'my': 4, 'into': 3, 'not': 2, 'around': 2, "don't": 1, "you're": 1, 'under': 1, 'why': 1, 'are': 1, 'you': 1, 'looking': 1, 'in': 1})
d= a-b
print(d)
#(실행결과) Counter({'eyes': 7, 'the': 5, 'look': 4, 'into': 3, 'my': 2, 'around': 2, "don't": 1, "you're": 1, 'under': 1})



            1.13 일반 키로 딕셔너리 리스트 정렬
            
#문제 딕셔너리 리스트가 있고, 하나 혹은 그 이상의 딕셔너리 값으로 이를 정렬하고 싶다

    #예제1 operator 모듈의 itemgetter 함수를 사용
rows= [ {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},  
        {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},  
        {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},  
        {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}  ]

from operator import itemgetter
rows_by_fname = sorted(rows, key= 
                       .
                       ('fname')) #'fname'을 기준으로 정렬
rows_by_uid = sorted(rows, key = itemgetter('uid')) #'uid'를 기준으로 정렬

print(rows_by_fname)
#(실행결과) [{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, {'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}]
print(rows_by_uid)
#(실행결과) [{'fname': 'John', 'lname': 'Cleese', 'uid': 1001}, {'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}]
           
rows_by_lfname= sorted(rows, key=itemgetter('lname','fname'))
print(rows_by_lfname)
#(실행결과) [{'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}, {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}]

    ## itemgetter()와 lambda 표현식 비교
rows_by_fname= sorted(rows, key=lambda s:s['fname'])
print(rows_by_fname)
#(실행결과) [{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, {'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}]


    #예제2 min, max 함수 사용
min(rows, key=itemgetter('uid'))
#(실행결과)  {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}
max(rows, key=itemgetter('uid'))
#(실행결과) {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}



            #1.14 기본 비교 기능 없이 객체 정렬            

    #예제1 
class User:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def __repr__(self):
        return 'User({})'.format(self.user_id)

users=[User(23),User(3), User(99)]    
print(users)
#(실행결과)  [User(23), User(3), User(99)]
sorted(users, key=lambda u: u.user_id)
#(실행결과) [User(3), User(23), User(99)]

    ##lambda 표현식과 attrgetter() 비교
from operator import attrgetter
sorted(users, key=attrgetter('user_id'))
#(실행결과) [User(3), User(23), User(99)]

min(users, key=attrgetter('user_id'))                            
#(실행결과) User(3)
max(users, key=attrgetter('user_id'))                            
#(실행결과) User(99)



            #1.15 필드에 따라 레코드 묶기
            
#문제 일련의 딕셔너리나 인스턴스가 있고 특정 필드 값에 기반한 그룹의 데이터를 순환하고 싶을 때

    #예제1 itertools.groupby() 사용
rows = [   {'address': '5412 N CLARK', 'date': '07/01/2012'},  
        {'address': '5148 N CLARK', 'date': '07/04/2012'},  
        {'address': '5800 E 58TH', 'date': '07/02/2012'},  
        {'address': '2122 N CLARK', 'date': '07/03/2012'},  
        {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},  
        {'address': '1060 W ADDISON', 'date': '07/02/2012'},  
        {'address': '4801 N BROADWAY', 'date': '07/01/2012'},  
        {'address': '1039 W GRANVILLE', 'date': '07/04/2012'} ]

from operator import itemgetter
from itertools import groupby

# 우선 원하는 필드로 정렬한다
rows.sort(key=itemgetter('date'))

for date, items in groupby(rows, key=itemgetter('date')):
    print(date) # address가 먼저 입력되어있는데 왜 date부터 나오는 걸까?
    for i in items:
        print('     ', i)

#(실행결과) 
07/01/2012
      {'address': '5412 N CLARK', 'date': '07/01/2012'}
      {'address': '4801 N BROADWAY', 'date': '07/01/2012'}
07/02/2012
      {'address': '5800 E 58TH', 'date': '07/02/2012'}
      {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'}
      {'address': '1060 W ADDISON', 'date': '07/02/2012'}
07/03/2012
      {'address': '2122 N CLARK', 'date': '07/03/2012'}
07/04/2012
      {'address': '5148 N CLARK', 'date': '07/04/2012'}
      {'address': '1039 W GRANVILLE', 'date': '07/04/2012'}



            #1.16 시퀀스 필터링
# 문제: 시퀀스 내부에 데이터가 있고 특정조건에 따라 값을 추출하거나 줄이고싶다.
# 해결방법: 리스트 컴프리헨션

    #예제1 
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
[n for n in mylist if n > 0]
#(실행결과) [1, 4, 10, 2, 3]

[n for n in mylist if n < 0]
#(실행결과) [-5,-7,-1]

pos = (n for n in mylist if n > 0) # 제너레이터
for x in pos:
    print(x)
#(실행결과) 
#1
#4
#10
#2
#3

    #예제2 filter() 사용
values = ['1','2','-3','-','4','N/A','5']

def is_int(val):
    try:
        x= int(val)
        return True
    except ValueError:
        return False
    
ivals = list(filter(is_int, values))
print(ivals)
#(실행결과) ['1', '2', '-3', '4', '5']

mylist = [1,4,-5,10,-7,2,3,-1]
import math
[math.sqrt(n) for n in mylist if n > 0]
#(실행결과) [1.0, 2.0, 3.1622776601683795, 1.4142135623730951, 1.7320508075688772]


    # 예제3 필터링 된 값을 새로운 값으로 치환하기
clip_neg = [n if n>0 else 0 for n in mylist]
clip_neg
#(실행결과) [1, 4, 0, 10, 0, 2, 3, 0]

clip_pos = [n if n<0 else 0 for n in mylist]
clip_pos
#(실행결과) [0, 0, -5, 0, -7, 0, 0, -1]


    #예제 itertools.compress()  -- 조건이 참인 요소만 반환
addresses = [  
        '5412 N CLARK',  
        '5148 N CLARK',   
        '5800 E 58TH',  
        '2122 N CLARK',  
        '5645 N RAVENSWOOD',  
        '1060 W ADDISON',  
        '4801 N BROADWAY',  
        '1039 W GRANVILLE' ]

counts=[0,3,10,4,1,7,6,1]

from itertools import compress
more5 = [n >5 for n in counts]
more5
#(실행결과) [False, False, True, False, False, True, True, False]

list(compress(addresses, more5))
#(실행결과) ['5800 E 58TH', '1060 W ADDISON', '4801 N BROADWAY']



            #1.17 딕셔너리의 부분 추출
# 문제 딕셔너리의 특정부분으로부터 다른 딕셔너리를 만들고 싶다.

    #예제1 dictionary comprehension
    
prices = {'ACME':45.23, 'AAPL':612.78, 'IBM':205.55, 'HPQ':37.20, 'FB':10.75}
p1 = {key : value for key, value in prices.items() if value > 200 }
print(p1)
#(실행결과)  {'AAPL': 612.78, 'IBM': 205.55}

tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = {key:value for key, value in prices.items() if key in tech_names}
print(p2)
#(실행결과) {'AAPL': 612.78, 'IBM': 205.55, 'HPQ': 37.2}





