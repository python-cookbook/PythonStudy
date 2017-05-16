===============================================================================   
# 1_1 시퀀스를 개별 변수로 나누기
### 시퀀스와 변수는 개수가 "일치"해야 한다,
### 언패킹_튜플, 리스트, 문자열, 파일, 이터레이터, 제너레이터 등 순환 가능한 모든 객체
### 언패킹할 때, 특정 값을 무시하는 방법 = "_"

EX1>
data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
name, shares, price, date = data
name
#'ACME'
date
#(2012, 12, 21)

name, shares, price, (year, mon, day) = data
year
#2012
mon
#12
day
#21

EX2>
s = 'Hello'
a, b, c, d, e = s
a
#'H'
b
#'e'
e
#'o'

EX3>
data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
_, shares, price, _ = data
shares
#50
price
#91.1
===============================================================================





===============================================================================
# 1_2 임의 순환체의 요소 나누기
### 언패킹하는데 요소가 N개 이상 포함 되어있다면 "별 표현식" 사용
### 언패킹은 길이가 일정하지 않은 튜플에 사용하면 편리

EX1>
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record
name
#Dave'
email
#dave@example.com'
phone_numbers
#['773-555-1212', '847-555-1212']


#별표가 처음에 올 때,
EX2>
*trailing_qtrs, current_qtr = sales_record
trailing_avg = sum(trailing_qtrs) / len(trailing_qtrs)
return avg_comparison(trailing_avg, current_qtr)

*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
trailing
#name 'sales_record' is not defined???????/
current
#name 'sales_record' is not defined?????????


EX3>
records = [('foo',1,2),('bar','hello'),('foo',3,4)]
def do_foo(x,y):
    print('foo',x,y)
    
def do_var(s):
    print('bar',s)

for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_var(*args)
===============================================================================





===============================================================================    
# 1_3 마지막 N개 아이템 유지
### 순환이나 프로세싱 중 마지막으로 발견한 N개의 아이템을 유지할 때 = collections.deque
### 아이템을 찾는 코드를 작성할 때, 주로 yield 를 포함한 제너레이터 함수를 만들면 
### 검색 과정과 결과를 사용하는 코드를 분리할 수 있다,

EX1>
#from collections import deque
#def seafch(lines, pattern, history = S):
 #   previos_lines = deque(maxlen = history)
  #  for line in lines:
   #     if pattern in line:
    #        yield line, previous_lines
     #   previous_lines.append(line)
????

EX2>
q=deque(maxlen=3)   #고정 크기 큐를 생성
q=deque
q.append(1)
q.append(2)
q.append(3)
q
#오류_descriptor 'append' requires a 'collections.deque' object but received a 'int'

EX3>
q = deque()
q.append(1)
q.append(2)
q.append(3)
q
#큐 구조체가 필요할 때 deque를 사용할 수있다,
#최대 크기를 지정하지 않으면 제약 없이 양쪽에 아이템을 넣거나 뺄 수 있다.





===============================================================================
#1_4 N 아이템의 최대 혹은 최소값 찾기
### 컬렉션 내부에서 가장 크거나 작은 N개의 아이템을 찾아야 할 때
### heapq 모듈 > nlargest() , nsmallest()

EX1>
import heapq
nums = [1,8,2,23,7,-4,18,23,42,37,2]
print(heapq.nlargest(3,nums))   #[42, 37, 23]
print(heapq.nsmallest(3,nums))  #[-4, 1, 2]

##nlargest() 와 nsmallest() 함수는 찾고자 하는 아이템의 개수가 상대적으로 작을 때
##(최대값, 최소값을 구할 때는 max(), min()이 더 빠르다.)
===============================================================================





===============================================================================
#1_5 우선 순위 큐 구현
### 우선 순위에 따라 아이템을 정렬하는 큐를 구현하고 항상 우선 순위가 가장 높은
### 아이템을 먼저 팝하도록 만들어야 할 때

EX1>
import heapq
class PriorityQueue:
    def __init__(self):
        self._queue=[]
        self._index=0
    def push(self,item,priority):
        heapq.heappush(self._queue,(-priority,self._index,item))
        self._index+=1
    def pop(self):
        return heapq.heapppop(self._queue)[-1]
    
class Item:
    def __init__(self,name):
        self.name=name
    def __repr__(self):
        return 'Item({!r})'.format(self.name)
    q=PriorityQueue()
    q.push(Item('foo'),1)
    q.push(Item('var'),5)
    q.push(Item('spam'),4)
    q.push(Item('grok'),1)
    p.pop()
#name 'Item' is not defined
##첫번째 pop()이 어떻게 가장 높은 우선 순위 아이템을 반환하는지
##두 아이템의 우선 순위가 같은 경우(foo와 grok)에는 쿠에 삽입된 순서와 동일하게 반환
##(-priority,index,item)에서 index변수는 우선 순위가 동일한 아이템의 순서 정할 때 사용
##일정하게 증가하는 인덱스 값을 ㅇ유지하기 때문에 힙에 아이템이 삼입된 순서대로 정렬 가능

                      
EX2>
a=(1,Item('foo'))
b=(5,Item('bar'))
a<b
#name 'Item' is not defined

##(priority,tiem)튜플에서는 우선 순위값이 달라야만 비교 가능
c=(1Item('grok'))
a<c

##인덱스 값을 추가해서 튜플을 만들면(priority,index,item) 동일한 인덱스값 가지지 않음
a=(1,0,Item('foo'))
b=(5,1,Item('bar'))
c=(1,2,Item('grok'))
a<b
a<c
===============================================================================        





===============================================================================
# 1_6 딕셔너리의 키를 여러 값에 매핑하기
### 딕셔너리의 키를 하나 이상의 값에 매핑할 때(multidic)
### 딕셔너리의 키에 여러 값을 매핑하려면, 여러 값을 "리스트"나 "세트"같은 "컨테이너"에 저장

EX1>
d = {'a':[1,2,3],'b' : [4,5]}
## 리스트_아이템의 삽입 순서를 지켜야 할 때
e={'a'={1,2,3},'b'={4,5}}
## 세트_순서 상관없이 중복을 없앨 때

### 딕셔너리를 쉽게 만들기 위해서 collections 모듈의 defaultdict를 사용
### defaultdict_첫번째 값을 자동으로 초기화 => 아이템 추가에 집중

EX2>
from collections import defaultdict
d=defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)

d=defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['b'].add(4)
???????

#defaultdict를 사용할 대는 딕셔너리에 존재하지 않는 값이라도 한 번이라도 접근했던 키의 엔트리를
#자동으로 생성한다.
#일반 딕셔너리의 setdefault()를 사용하면 해결 가능

d={}   #일반 딕셔너리
d.setdefault('a'.[]).append(1)
d.setdefault('a'.[]).append(2)
d.setdefault('b'.[]).append(4)
????????
===============================================================================    




===============================================================================    
# 1.7 딕셔너리 순서 유지
### 딕셔너리를 만들고, 순환이나 직렬화할 때 순서를 조절하기 위해서
### "collections 모듈의 OrderedDict"
### 삽입 초기의 순서를 그대로 기억한다.
### OrderedDict는 나중에 직렬화 / 다른 포맷으로 인코딩할 다른 매핑을 만들 때 유용하다.
### 새로운 아이템을 처음으로 삽입하면 리스트의 제일 끝에 위치시킨다(더블 링크드 리스트)

EX1>
from collections import OrderedDict
d=OrderedDict()
d['foo']=1
d['bar']=2
d['spam']=3
d['grok']=4
 
for key in d:
    print(key,d[key])
    #foo 1
    #bar 2
    #spam 3
    #grok 4
===============================================================================    
  
    
    


===============================================================================
# 1.8 딕셔너리 계산
### 딕셔너리 데이터에 여러 계산을 수행할 떼(최대값, 최소값, 정렬,..)

EX1>
#키=주식이름, 값=가격
prices={'ACME':45.23,'AAPL':612.78,'IBM':205.55,'HPQ':37.20,'FB':10.75}
#딕셔너리 계산을 위해서 키와 값을 zip()으로 뒤집어 주기

#최대주가
max_price=max(zip(prices.values(),prices.keys()))
print(max_price)
#(612.78, 'AAPL')


#zip은 한 번만 소비할 수 있는 이터레이터를 생성한다.
EX2>
prices_names=zip(prices.values(),prices.keys())
print(min(prices_names))   #(10.75, 'FB')
print(max(prices_names))   #ValueError: max() arg is an empty sequence

#딕셔너리에 하나의 값만 입력하면,"키"를 반환한다.
prices={'ACME':45.23,'AAPL':612.78,'IBM':205.55,'HPQ':37.20,'FB':10.75}
min(prices)    #'AAPL'

#values를 뽑고 싶다면,
min(prices.values())    #10.75

#키에 일치하는 값 정보를 알고 싶으면, "키 함수"
min(prices,key=lambda k:prices[k])  #'FB'
#=최소값에 해당하는 키

min_value=prices[min(prices, key=lambda k:prices[k])]
print(min_value)    #10.75
===============================================================================
     
 
     
     
     
===============================================================================    
#1.9 두 딕셔너리의 유사점 찾기
### 두 딕셔너리의 유사점을 찾고 싶다면(동일한 키, 동일한 값,...)
### "keys() 와 items() 메소드에 집합 연산 수행"
### 딕셔너리의 keys() 메소드는 키를 노출하는 "키-뷰"객체를 반환한다.
### "키-뷰"에는 "합집합, 교집합, 여집합 등 집합 연산 기능이 있다.
### itmes() 메소드는 (key,value) 페어로 구성된 아이템=뷰(item-view) 객체를 반환한다.
### =두 딕셔너리에 동일한 키-값 페어를 찾을 때 사용할 수 있다.
### values() 메소드는 집합 연산 기능 지원X [키와는 다르게 값-뷰가 유일하다는 확신X]
### =비교를 수행하려면 값을 집합으로 변환

EX1>
a={'x':1,'y':2,'z':3}
b={'w':10,'y':11,'z':2}

#동일한 키찾기
a.keys()&b.keys()   #{'y', 'z'}
#a에만 있고 b에 없는 키 찾기
a.keys()-b.keys()   #{'x'}
#(키,값)이 동일한 것 찾기
a.items()&b.items()     #set()??????
#특정 키를 제거한 새로운 딕셔러니 만들기
c={key:a[key] for key in a.keys() - {'z','w'}}
print(c)    #{'y': 2, 'x': 1}
===============================================================================





===============================================================================
# 1_10 순서를 깨지 않고 시퀀스의 중복 없애기
### 시퀀스에서 중복된 값을 없애는데, 아이템의 순서는 유지하고 싶을 때
### 시퀀스의 값이 "hash"가능하다면 "세트" 와 "제너레이터" 사용

EX1>
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)
a = [1, 5, 2, 1, 9, 1, 5, 10]
list(dedupe(a))    #[1, 5, 2, 9, 10]


#해시 불가능한 딕셔너리
EX2>
def dedupe(items,key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)
a=[{'x':1,'y':2},{'x':1,'y':3},{'x':1,'y':2},{'x':1,'y':4}]
list(dedupe(a, key=lambda d: (d['x'],d['y'])))  
#[{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}]
## key 인자 = 중복 검사를 위해 함수가 시퀀스 아이템을 해시 가능한 타입으로 변환 명시

#set을 이용한 중복 제거
a = [1, 5, 2, 1, 9, 1, 5, 10]
set(a)
# {1, 2, 5, 9, 10}
## =데이터 훼손
===============================================================================





===============================================================================
# 1.11 슬라이스 이름 붙이기
### 프로그램 코드에 슬라이스를 지시하는 하드코딩
### slice()함수로 슬라이스 받는 모든 곳에 사용할 수 있는 조각을 생성

EX1>
items=[0,1,2,3,4,5,6]
a=slice(2,4)
items[a]    #[2, 3]
items[a] = [10,11]
items    #[0, 1, 10, 11, 4, 5, 6]
del items[a]
items    #[0, 1, 4, 5, 6]


EX1_1>
a=slice(10,50,2)
a.start   #10
a.stop   #50
a.step    #2


#"indeces(size) 메소드"
#특정 크기의 시퀀스에 슬라이스를 매핑 가능
# 튜플(start, stop, step) 반환
EX2>
s='HelloWorld'
#a.indices(len(s))   #(10, 10, 2)
for i in range(*a.indices(len(s))):
    print(s[i])
#출력 없을 무???????/
===============================================================================





===============================================================================
# 1.12 시퀀스에 가장 많은 아이템 찾기
### "collections.Counter" 와 "most_common()"

EX1>
words = [
'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
'my', 'eyes', "you're", 'under'
]
from collections import Counter
word_counts = Counter(words)
top_three = word_counts.most_common(3)
print(top_three)
#[('eyes', 8), ('the', 5), ('look', 4)]

#Counter 객체에는 해시 가능한 모든 아이템 입력 가능
# "Counter" = 아이템이 나타난 횟수를 가리키는 딕셔너리.
word_counts['not']      #1
word_counts['eyes']     #8


EX2>
#카운트를 수동으로 증가시키고 싶다면 더하기 사용
morewords = ['why','are','you','not','looking','in','my','eyes']
for word in morewords:
    word_counts[word] += 1
word_counts['eyes']     #10

           
#Counter 인스턴스는 여러 가지 수식 사용 가능
EX3>
words = [
'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
'my', 'eyes', "you're", 'under'
]
morewords = ['why','are','you','not','looking','in','my','eyes']
a=Counter(words)
a
#Counter({'around': 2,
#         "don't": 1,
#         'eyes': 8,
#         'into': 3,
#         'look': 4,
#         'my': 3,
#         'not': 1,
#         'the': 5,
#         'under': 1,
#         "you're": 1})
b=Counter(morewords)
b
#Counter({'are': 1,
#         'eyes': 1,
#         'in': 1,
#        'looking': 1,
#        'my': 1,
#        'not': 1,
#        'why': 1,
#        'you': 1})

    
##카운트 합치기    
c=a+b
c
#Counter({'are': 1,
#         'around': 2,
#         "don't": 1,
#         'eyes': 9,
#         'in': 1,
#         'into': 3,
#         'look': 4,
#         'looking': 1,
#         'my': 4,
#         'not': 2,
#         'the': 5,
#         'under': 1,
#         'why': 1,
#         'you': 1,
#         "you're": 1})
===============================================================================
    
    
    

    
    
===============================================================================    
# 1.13 일반 키로 딕셔너리 리스트 정렬
# 딕셔너리 리스트가 있고, 하나 혹은 그 이상의 딕셔너리 값으로 정렬
# "operator 모듈의 inemgetter 함수"

EX1>
rows = [
{'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
{'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
{'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]

from operator import itemgetter
rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))
print(rows_by_fname)
#[{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}, 
#{'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, 
#{'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
#{'fname': 'John', 'lname': 'Cleese', 'uid': 1001}]
print(rows_by_uid)
#[{'fname': 'John', 'lname': 'Cleese', 'uid': 1001}, 
#{'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, 
#{'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, 
#{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}]


##itemgetter() 함수로 키 여러 개 전달하기.
EX2>
rows_by_lfname = sorted(rows, key=itemgetter('lname','fname'))
print(rows_by_lfname)
#[{'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, 
#{'fname': 'John', 'lname': 'Cleese', 'uid': 1001}, 
#{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}, 
#{'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}]

#최대값, 최소값을 구할 때도 itemgetter()함수 사용 가능
min(rows, key=itemgetter('uid'))
#{'fname': 'John', 'lname': 'Cleese', 'uid': 1001}
max(rows, key=itemgetter('uid'))
#{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
===============================================================================




===============================================================================
#1.14 기본 비교 기능 없이 객체 정렬
# 동일한 클래스 객체를 정렬해야 한느데, 클래스가 기본적인 비교 연산을 제공하지 않을 때,
# "sorted()는 key 인자에 호출 가능 객체를 받아 sorted가 객체 비교에 사용할 수 있는 값 반환
EX1>
class User:
    def __init__(self, user_id):
        self.user_id = user_id
    def __repr__(self):
        return 'User({})'.format(self.user_id)
users = [User(23), User(3), User(99)]
users
#[User(23), User(3), User(99)]
sorted(users, key=lambda u: u.user_id)
#[User(3), User(23), User(99)]

from operator import attrgetter
sorted(users, key=attrgetter('user_id'))
#[User(3), User(23), User(99)]
##lambda 대신, operator.attrgetter() 사용 가능
===============================================================================
                                
                                
                                

                                
===============================================================================
# 1.15 필드에 따라 레코드 묶기
# 일련의 딕셔너리나 인스턴스가 있고 특정 필드 값에 기반한 그룹의 데이터를 순환할 때
# itertools.groupby() 함수

EX1>
rows = [
{'address': '5412 N CLARK', 'date': '07/01/2012'},
{'address': '5148 N CLARK', 'date': '07/04/2012'},
{'address': '5800 E 58TH', 'date': '07/02/2012'},
{'address': '2122 N CLARK', 'date': '07/03/2012'},
{'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
{'address': '1060 W ADDISON', 'date': '07/02/2012'},
{'address': '4801 N BROADWAY', 'date': '07/01/2012'},
{'address': '1039 W GRANVILLE', 'date': '07/04/2012'},]

from operator import itemgetter
from itertools import groupby

#원하는 필드로 정렬
rows.sort(key=itemgetter('date'))
#그룹 내부에서 순환
for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print(' ', i)

#07/01/2012
#  {'address': '5412 N CLARK', 'date': '07/01/2012'}
#  {'address': '4801 N BROADWAY', 'date': '07/01/2012'}
#07/02/2012
#  {'address': '5800 E 58TH', 'date': '07/02/2012'}
#  {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'}
#  {'address': '1060 W ADDISON', 'date': '07/02/2012'}
#07/03/2012
#  {'address': '2122 N CLARK', 'date': '07/03/2012'}
#07/04/2012
#  {'address': '5148 N CLARK', 'date': '07/04/2012'}
#  {'address': '1039 W GRANVILLE', 'date': '07/04/2012'}


## 단순히 날짜에 따라 데이터를 묶어서 자료 구조에 넣고 원할 대마다 접근할 때,
## "defaultdict()"를 사용해서 "multidict"
EX2>
from collections import defaultdict
rows_by_date = defaultdict(list)
for row in rows:
    rows_by_date[row['date']].append(row)

for r in rows_by_date['07/01/2012']:
    print(r)
#{'address': '5412 N CLARK', 'date': '07/01/2012'}
#{'address': '4801 N BROADWAY', 'date': '07/01/2012'}
===============================================================================




===============================================================================
# 1.16 시퀀스 필터링
# 시퀀스 내부에 데이터가 있고 특정 조건에 따라 값을 추출하거나 줄이고 싶을 때
# "리스트 컴프리헨션"

EX1>
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
[n for n in mylist if n > 0]
#[1, 4, 10, 2, 3]
[n for n in mylist if n < 0]
#[-5, -7, -1]

## 위의 식은 입력된 내용이 크면 결과도 매우 큰 결과 생성
## => "생성자 표현식"
EX2>
pos = (n for n in mylist if n > 0)
pos
#<generator object <genexpr> at 0x0000026D32E126D0>
for x in pos:
    print(x)
    #1
    #4
    #10
    #2
    #3

#리스트 컴프리헨션이나 생성자 표현식에서 필터링 도중 복잡한 내용이 들어가야 한다면,
#필터링 코드를 함수 안에 넣고 "filter()" 사용
EX3>
values = ['1', '2', '-3', '-', '4', 'N/A', '5']
def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False
ivals = list(filter(is_int, values))    #filter()는 이터레이터 생성_리스트 생성시 "list()"
print(ivals)
#['1', '2', '-3', '4', '5']
===============================================================================





===============================================================================
# 1_17 딕셔너리의 부분 추출
# 딕셔너리의 특정 부분으로부터 다른 딕셔너리르 만들고 싶을 대
# "디셔너리 컴프리헨션"

EX1>
prices = {
'ACME': 45.23,
'AAPL': 612.78,
'IBM': 205.55,
'HPQ': 37.20,
'FB': 10.75
}

#가격이 200 이상인 것에 댛나 딕셔너리
p1 = { key:value for key, value in prices.items() if value > 200 }
print(p1)
#{'AAPL': 612.78, 'IBM': 205.55}

#기술 관련 주식으로 딕셔너리 구성
tech_names = { 'AAPL', 'IBM', 'HPQ', 'MSFT' }
p2 = { key:value for key,value in prices.items() if key in tech_names }
print(p2)
#{'AAPL': 612.78, 'IBM': 205.55, 'HPQ': 37.2}

## 위 식은 튜플 시퀀스를 만들고 dict()함수에 전달하는 방법으로 구현 가능
p1 = dict((key, value) for key, value in prices.items() if value > 200)
print(p1)
#{'AAPL': 612.78, 'IBM': 205.55}
===============================================================================




===============================================================================
# 1.18 시퀀스 요소에 이름 매핑
# 리스트나 튜플의 위치로 요소에 접근하는 코드의 가동성 높이기
# 그리고 위치에 의존하는 코드의 구조 -> 이름으로 접근 가능하게 하기
# "collection.namedtuple()"
# 타입 이름과, 포함해야할 필드를 전달하면 인스턴스화 가능한 클래스 반환

EX1>
from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com', '2012-10-19')
sub
#Subscriber(addr='jonesy@example.com', joined='2012-10-19')
sub.addr
#'jonesy@example.com'
sub.joined
#'2012-10-19'

##namedtuple의 인스턴스는 튜플과 교환이 가능하고, 인덱싱이나 언패킹과 같은 튜플의 기능 지원.
len(sub)
#2
addr, joined = sub
addr
#'jonesy@example.com'
joined
#'2012-10-19'


##네임드튜플은 주로 요소의 위치를 기반으로 구현되어 있는 코드를 분리
##튜플이 요소의 위치로 접근하는 코드에서 테이블에 새 열이 추가되는 문제 예방 가능

EX2>
from collections import namedtuple
Stock = namedtuple('Stock', ['name', 'shares', 'price'])
def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total


##네임드튜플은 저장 공간을 더 필요로 하는 딕셔너리 대신 사용 가능하다.
## 하지만 딕셔너리와 다르게 수정 불가능!

EX3>
s = Stock('ACME', 100, 123.45)
s
#Stock(name='ACME', shares=100, price=123.45)

s.shares = 75
#AttributeError: can't set attribute

##속성을 수정하려면 "_replace() 메소드"
s = s._replace(shares=75)
s
#Stock(name='ACME', shares=75, price=123.45)
===============================================================================





===============================================================================
# 1.19 데이터를 변환하면서 줄이기
# 감소함수 (sum(), min(), max())를 실행해야 하는데, 먼저 데이터를 변환하거나 필터링할 때,
# "생성자 표현식"

##정사각형 넓이의 합
nums = [1, 2, 3, 4, 5]
s = sum(x * x for x in nums)
print(s)
#55

## 위의 코드는 반복적인 괄호를 할 필요가 없다.
s = sum((x * x for x in nums))    # 생성자 표현식을 인자로 전달
s = sum(x * x for x in nums)
===============================================================================






===============================================================================
# 1.20 여러 매핑을 단일 매핑으로 합치기
#딕셔너리나 매핑이 여러 개 있고, 자료 검색이나 데이터 확인을 위해서 하나의 매핑으로 합치기
#"collections 모듈의 ChainMap 클래스"

EX1>
a = {'x': 1, 'z': 3 }
b = {'y': 2, 'z': 4 }
#두 딕셔너리가 있는데, a에서 데이터를 검색하고,
#그 후 b에 그 데이터가 있는지 검색할 때,
from collections import ChainMap
c = ChainMap(a,b)
print(c['x'])    #1[a의 1]
print(c['y'])    #2[b의 2]
print(c['z'])    #3[a의 3]

##ChainMap은 매핑을 여러 개 받아서 하나처럼 "보이게" <> 하나로 합치기X
len(c)
#3
list(c.keys())
#['x', 'y', 'z']
list(c.values())
#[1, 2, 3]

## 중복 키가 있으면 첫번째 매핑으 ㅣ값을 사용
## 따라서 예제의 c['z']는 언제나 딕셔너리 a의 값을 참조하며 b의 값을 참조하지 X
## 매핑의 값을 변경한느 동작은 언제나 리스트의 첫번째 매핑에 영향을 준다.
EX2>
c['w'] = 40
del c['x']
a
#{'w': 40, 'z': 10}
del c['y']
#Traceback (most recent call last):
#  File "<ipython-input-79-df3e26fa6544>", line 1, in <module>
#    del c['y']
#  File "C:\Users\ATIV BOOK 9\Anaconda3\lib\collections\__init__.py", line 935, in __delitem__
#    raise KeyError('Key not found in the first mapping: {!r}'.format(key))
#KeyError: "Key not found in the first mapping: 'y'"


###ChainMap의 대안으로 update()를 사용해 딕셔너리를 하나로 합칠 수 있다.
EX3>
a = {'x': 1, 'z': 3 }
b = {'y': 2, 'z': 4 }
merged = dict(b)
merged.update(a)
merged['x']
#1
merged['y']
#2
merged['z']
#3
###잘 동작하지만 ,완전히 별개의 딕셔너리를 객체로 새로 만들어야 하너가 개존 딕셔너리의
### 내용을 변경해야 한다.
### 원본 딕셔너리의 내용이 변경된다 해도 합쳐 놓은 딕셔너리에 반영되지 않는다.
>>>
a['x']=13
merged['x']
#1


####ChainMap 은 원본 딕셔너리를 참조하기 때문에 문제X
a = {'x': 1, 'z': 3 }
b = {'y': 2, 'z': 4 }
merged = ChainMap(a, b)
merged['x']
#1
a['x'] = 42
merged['x']     #합친 딕셔너리에 변경 알림
#42
===============================================================================