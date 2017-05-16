# 1.1시퀀스를 개별 변수로 나누기
p=(4,5)
x,y = p      
x
y



data  = ['ACME',50,91.1,(2012,12,21)]
name,shares,price,date = data
name
date
name,shares,price,(year,month,day) = data
name
year
month
day
# 요소 개수가 일치 하지 않으면 에러가 난다.
s = 'hello'
a,b,c,d,e = s
a

# 요소 개수를 입력하지 않고 무시하는 방법
data  = ['ACME',50,91.1,(2012,12,21)]
_,shares,price,_ = data
shares
price

# 변수명이 사용되고 있는지 확인해야한다.

# 1.2 임의 순환체의 요소 나누기
# 순환체를 언패킹 하려는데 요소가 N개 이상 포함되어 “값이 너무 많습니다”라는 예외가 발생한다.
record = ('Dave','dave@naver.com','010-1234-5678','010-4321-8756')
name,mail,*phone = record
phone

record=[('foo',1,2,),('bar','hello'),('foo',3,4,)]
def do_foo(x,y):
    print('foo',x,y)
def do_bar(s):
    print('bar',s)
for tag, *args in record:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)






# 요소 여러개를 무시하는 방법
record = ('ACME',50,123.45,(12,18,2012))
name,*_,(*_,year) =record
name
year

# 1.3 마지막 N개 아이템 유지
from collections import deque
q =deque(maxlen=3)
q.append(1)
q.append(2)
q.append(3)
q
q.append(4)
q

from collections import deque
# deque(maxlen=3) 리스트 길이를 최대 3개로 제한하겠다.


# deque의 최대 크기를 지정하지 않으면 제약없이 양쪽에 아이템을 넣거나 빼는 작업을 할 수 있다.
from collections import deque
q =deque()
q.append(1)
q.append(2)
q.append(3)
q
q.appendleft(4)
q
q.pop()
q
q.popleft()
q

# 1.4 N아이템의 최대 혹은 최소값 찾기
import heapq
nums=[1,8,2,23,7,-5,23,-43,-54,2,3,4]
print(heapq.nlargest(1,nums))
print(heapq.nsmallest(1,nums))
# nlargest(1,nums)은 nums 리스트에서 최댓값 하나만 출력해라이다.
# 3을 넣으면 가장 큰 숫자부터 3개를 출력해준다.
# nsmallest(1,nums)는 nums 리스트에서 최솟값 하나만 출력해라이다.
# 3을 넣으면 가장 작은 숫자부터 3개를 출력해준다. 


# 1.5 우선 순위 큐 구현
import heapq

class PriorityQueue:
    def __init__(self):
        self._queue=[]
        self._index=0
    def push(self,item,priority):
        heapq.heappush(self._queue,(-priority, self._index,item))
        self._index += 1
    def pop(self):
        return heapq.heappop(self._queue)[-1]

class Item:
    def __init__(self,name):
        self.name=name
        def __repr__(self):
            return 'Item({!r})'.format(self.name)
q = PriorityQueue()
q.push(Item('foo'),1)
q.push(Item('bar'),5)
q.push(Item('spam'),4)
q.push(Item('grok'),1)
q.pop()



# 1.6 딕셔너리의 키를 여러값에 매핑하기
d.setdefault('a',[]).append(1)
d.setdefault('a',[]).append(2)
d.setdefault('b',[]).append(4)
d

# 여러값을 가지는 딕셔너리를 defaultdict을 사용하면 간단하게 가능하다.
# d =defaultdict(list)
# for key, value in pairs:
#     d[key].append(value)









# 1.7 딕셔너리 순서유지
from collections import OrderedDict
d = OrderedDict()
d['foo'] = 1
d['bar']= 2
d['spam'] = 3
d['grok'] = 4
for key in d:
    print(key,d[key])

# 1.8 딕셔너리 계산
price = {'ACME': 45.23,
         'AAPL':612.78,
         'IBM':205.55,
         'HPQ':37.20,
         'FB':10.75}
min_price = min(zip(price.values(),price.keys()))
min_price
max_price = max(zip(price.values(),price.keys()))
max_price

# zip()으로 딕셔너리의 키와 값을 뒤접어서 출력해줄 수 있다.


# 데이터의 순서를 매기려면 zip()과 sorted()를 함께 사용한다.
price_sorted = sorted(zip(price.values(),price.keys()))
price_sorted

# sort는 리스트 내의 정렬을 바꿔 버리고 sorted는 출력할때만 정렬되어 보여지고 리스트내의 본래 정렬은 바뀌지 않는다.
# 1.9 두 딕셔너리의 유사점 찾기
a = {'x':1,'y':2,'z':3}
b = {'w':10,'x':11,'y':2}
a.keys() & b.keys()  #동일한 키 찾기

a.keys() - b.keys()   # a에만 있고 b에는 없는 키 찾기

a.items() & b.items() # 키와 값이 같은 것 찾기

# 1.10 순서를 유지하며 시퀀스 중복없애기
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)
a = [1,5,2,1,9,1,5,10]
list(dedupe(a))
# 위 방법으로 하면 입력된 순서를 지킬 수 있고
# set을 이용하면 중복은 제거 되지만 기존 데이터의 순서가 훼손된다.

a = [1,5,2,1,9,1,5,10]
set(a)

# 1.11 슬라이스 이름 붙이기
items = [ 0, 1, 2, 3, 4, 5, 6]
a=slice(2,4)    
items[a]
items[2:4]

items[a]=[10,11]
items
del items[a]
items

a =slice(10,50,2)
a.start
a.stop
a.step


# 1.12 시퀀스에 가장 많은 아이템 찾기
word =['look','into','my','eyes','look','into','my','eyes','the','eyes'
     'the','eyes','the','eyes','not','around','the','eyes',"don't",'look','into'
      ,'my','eyes',"you're",'under']
from collections import Counter
word_counts = Counter(word)
top_three = word_counts.most_common(3)
print(top_three)

word_counts['not']
word_counts['eyes']

# 1.13 일반 키로 딕셔너리 리스트 정렬
from operator import itemgetter
rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))
print(rows_by_fname) # fname으로 정렬한걸 출력
print(rows_by_uid)    # uid로 정렬한걸 출력

# itemgetter()함수에는 키를 여러개 전달할 수도 있다.
rows_by_lfname = sorted(rows, key=itemgetter('lname','fname'))
# 이렇게 출력하면 lname순으로 먼저 정렬하고 lname의 순위가 같다면 fname순으로 정렬해서 출력해준다.
# 1.14 기본 비교 기능 없이 객체 정렬
class User:
    def __init__(self,user_id):
        self.user_id = user_id
    def __repr__(self):
        return 'User({})'.format(self.user_id)
users = [User(23),User(3),User(99)] 
users
sorted(users, key = lambda u: u.user_id)
# lambda를 사용하는 대신 operator.attrgetter()를 사용해도 된다.
from operator import attrgetter
sorted(users, key = attrgetter('user_id'))

# 1.15 필드에 따라 레코드 묶기 
rows = [ {'address':'5412 N CLARK', 'date':'07/01/2012'},
        {'address':'5148 N CLARK', 'date':'07/04/2012'},
        {'address':'5800 E 58TH', 'date':'07/02/2012'},
        {'address':'2122 N CLARK', 'date':'07/03/2012'},
        {'address':'5645 N  RAVENSWOOD', 'date':'07/02/2012'},
        {'address':'1060 W ADDISON', 'date':'07/02/2012'},
        {'address':'4801 N BROADWAY', 'date':'07/01/2012'},
        {'address':'1039 W GRANVILLE', 'date':'07/04/2012'},
        ]
from operator import itemgetter
from itertools import groupby

rows.sort(key=itemgetter('date'))

for date, items in groupby(rows,key=itemgetter('date')):
    print(date)
    for i in items:
        print('    ',i)

# 1.16 시퀀스 필터링
mylist = [1,4,-5,10,-7,2,3,-1]
[n for n in mylist if n>0]
[n for n in mylist if n<0]

values = ['1','2','-3','-','4','N/A','5']
def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False
ivals=list(filter(is_int,values))
print(ivals)


my_list = [1,3,5,-5,10,-7,2,3,-1]
import math
[math.sqrt(n) for n in mylist if n>0] 

clip_neg = [n if n >0 else 0 for n in mylist]
clip_neg

clip_pos = [n if n<0 else 0 for n in mylist]
clip_pos

# 1.17 딕셔너리의 부분 추출
price={'ACME':45.23,'AAPL':612.78,'IBM':205.55,'HPQ':37.20,'FB':10.75}

P1 = {key:value for key, value in price.items() if value>200}
P1

tech_name={'AAPL','IBM','HPQ','MSFT'}
P2 = {key:value for key,value in price.items() if key in tech_name}
P2


