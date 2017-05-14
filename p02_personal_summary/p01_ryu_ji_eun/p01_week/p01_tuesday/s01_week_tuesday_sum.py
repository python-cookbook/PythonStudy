#=======================================================================================================================
# 시퀀스를 개별 변수로 나누기
# N개의 요소를 가진 tuple 이나 sequence가 있다. 이를 variable N개로 나누어야 한다.
# ㄴ 간단한 할당문을 사용해서 개별 변수로 나눈다. 이때 변수의 개수가 sequence에 일치해야한다.
#=======================================================================================================================
p = (4,5)
x,y = p

## 시퀀스 내부 개수와 변수 개수가 일치하면, 각각 요소가 개별 변수로 들어간다
data=['고기', 600, 10000, (2012, 12, 21)]
product, grams, price, date = data
print(product, grams)

_, _, prices, (year, mon, day) = data
print(data[0])
print(_)                                                # 가장 뒤에 있는 _의 값으로 출력된다.


##unpacking - 튜플, 리스트, 문자열, 파일, iterator, generator
s = 'Hello!buddy'
a,b,c,d,e,f,g,h,i,j,k = s
print(i)

#=======================================================================================================================
# 임의 순환체의 요소 나누기
# 순환체를 unpacking하려는데 element가 N개 이상 포함되어 "too many values"라는 exception이 발생한다.
# ㄴ * 를 사용한다.
#=======================================================================================================================
def drop_first_last(grades):
    first, *middle, last = grades
    return avg(middle)

## *는 순환체를 뜻한다.

record = ('Dave', 'dave@example.com', '112-555-1212','847-555-1212')
name, email, *phone_numbers = user_record               # user_record    came from where?? NameError: name 'user_record' is not defined
print(name)


## 튜플에 사용해보면

records = [
    ('foo',1,2),
    ('bar','hello'),
    ('foo',3,4)
    ]

def do_foo(x,y):
    print('foo',x,y)

def do_bar(s):
    print('bar',s)

for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)

    elif tag == 'bar':
        do_bar(*args)

# 결과값
# foo 1 2           # 앞의 foo나 bar를 제외한 뒤의 것들을 *args로 그냥 데려온다.
# bar hello
# foo 3 4


record_2 = ('Jim', 58, 123.45, (12, 18, 2013))
name_2, *_, (*_, year_2) = record_2
print(name_2)
print(year_2)


## head & tail 분리
items = ['머리', '꼬리1', '꼬리2', '꼬리3', '꼬리4', '꼬리5']
head, *tail = items
print(head)
print(*tail)

def sum(items):                     # 재귀로 할때. 근데 이건 쓰지 마셈
    head, *tail = items
    return head + ' '+sum(tail) if tail else head

print(sum(items))


# 이건 그냥 써보자..

line = 'nobody: * :-2:-2:Unprivileged User: /var/empty: /usr/bin/false'
uname, *fields, homedir, sh = line.split(':')
print(uname)

#=======================================================================================================================
# ★★★★★★★★★★★★★★★★★★
# 마지막 N개 아이템 유지
# 순환이나 processing 중 마지막으로 발견한 N개의 아이템을 유지하고 싶다
# ㄴ collections.deque 사용
#=======================================================================================================================
from collections import deque             # 여러줄에 대해 간단한 텍스트 매칭을 수행하고 처음으로 발견한 N라인을 찾는다
                                            # ...는데 이해가 잘....
def search(lines, pattern, history = 5):
    previous_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        previous_lines.append(line)

if __name__=='__main__':
    with open('somefile.txt') as f:
        for pline, prevlines in search(f, 'python', 5):
            print(pline, end='')
        print(line, end='')
        print('-'*20)


## 큐 돌리깅

q = deque(maxlen = 3)
q.append(1)
q.append(2)
q.append(3)
print(q)

# 결과값 : deque([1, 2, 3], maxlen=3)      여기에서 더 집어넣으면 가장 첫번째것이 삭제되고, 최근것은 뒤에 갱신됨


#=======================================================================================================================
# N 아이템의 최대 혹은 최소값 찾기
# collections 내부에서 가장 크거나 작은 N개의 아이템을 찾아야 한다.
# ㄴ headpq 모듈에는 이 용도에 적합한 nlargest()와 nsmallest()가 있다.
#=======================================================================================================================
import heapq

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums))          # prints [42, 37, 23]
print(heapq.nsmallest(3, nums))         # prints [-4, 1, 2]

## 키 파라미터 받기
portfolio = [
    {'name':'IBM', 'shares':100, 'price':91.1},
    {'name':'AAPL', 'shares':50, 'price':543.22},
    {'name':'FB', 'shares':200, 'price':21.09},
    {'name':'HPQ', 'shares':35, 'price':31.75},
    {'name':'YHOO', 'shares':45, 'price':16.35},
    {'name':'ACME', 'shares':75, 'price':115.65}
]

cheap = heapq.nsmallest(3, portfolio, key = lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key = lambda s: s['price'])

print(cheap)
print(expensive)

# 결과값
# [42, 37, 23]
# [-4, 1, 2]
# [{'name': 'YHOO', 'shares': 45, 'price': 16.35}, {'name': 'FB', 'shares': 200, 'price': 21.09}, {'name': 'HPQ', 'shares': 35, 'price': 31.75}]
# [{'name': 'AAPL', 'shares': 50, 'price': 543.22}, {'name': 'ACME', 'shares': 75, 'price': 115.65}, {'name': 'IBM', 'shares': 100, 'price': 91.1}]



## 구현방식

# 1. 데이터를 힙으로 정렬시켜놓는 리스트로 변환한다.
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
import heapq
heap = list(nums)
heapq.heapify(heap)
heap                            # [-4, 2, 1, 23, 7, 2, 18, 23, 42, 37, 8]

# 2. heap의 가장 중요한 기능은 heap[0]이 가장 작은 아이템이 된다는 점. 첫 아이템을 팝하고 그 다음 아이템으로 치환하는
# hepq.heappop() 메소드를 사용하면 뒤이어 나오는 아이템도 쉽게 찾을 수 있다.
heapq.heappop(heap)             # -4
heapq.heappop(heap)             # 1
heapq.heappop(heap)             # 2


#=======================================================================================================================
# 우선순위 큐 구현
# 주어진 우선순위에 따라 아이템을 정렬하는 queue를 구현하고, 항상 우선순위가 가장 높은 아이템을 먼저 팝하도록 만들자
# ㄴ heapq 모듈을 사용해 간단한 우선순위 큐를 구현한다.
#=======================================================================================================================
import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


## 위의 것을 사용하는 예제

class Item:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return 'Item({!r})'.format(self.name)

q = PriorityQueue()
q.push(Item('foo'), 1)
q.push(Item('bar'), 5)
q.push(Item('spam'), 4)
q.push(Item('grok'), 1)
print(q.pop())                              # Item('bar')
print(q.pop())                              # Item('spam')
print(q.pop())                              # Item('foo')
print(q.pop())                              # Item('grok')


#=======================================================================================================================
# 딕셔너리의 키를 여러 값에 매핑하기
# 딕셔너리의 키를 하나 이상의 값에 매핑하고 싶다. (multidict)
# ㄴ 하나의 키에 여러 값을 매ㅏ핑하려면 그 여러 값을 리스트나 세트와 같은 컨테이너에 따로 저장해두어야 한다.
#=======================================================================================================================
d = {
    'a': [1,2,3],
    'b': [4,5]
}

e = {
    'a': {1,2,3},
    'b': {4,5}
}

## 아이템의 삽입 순서를 지켜야 한다면 리스트를 사용하는 것이 좋고, 순서가 상관없고 중복을 없애려면 세트를 써야 한다.
# 이런 딕셔너리를 쉽게 만들려고 collections 모듈의 defaultdict를 쓴다. 여기 기능 중에는 첫번째 값을 자동으로 초기화하는
# 것이 있어서 아이템 추가에만 집중하면 된다.

from collections import defaultdict

d = defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)

d = defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['b'].add(4)


## defaultdict를 사용할 때에는 딕셔너리에 없는 값이어도 한 번이라도 실행한 키의 엔트리를 자동 생성하기 때문에 (.......????)
# 이러면 안된다면 일반 딕셔너리의 setdefault()를 사용한다.
d = {}
d.setdefault('a', []).append(1)
d.setdefault('a', []).append(2)
d.setdefault('b', []).append(4)

#=======================================================================================================================
# 1.7 딕셔너리 순서 유지
# 딕셔너리를 만들고, 순환이나 직렬화할 때 순서를 조절하고 싶다
# ㄴ 딕셔너리 내부 순서를 조절하려면 collections 모듈의 OrderedDict를 사용한다. 삽입 초기의 순서를 그대로 기억한다.
#=======================================================================================================================
from collections import OrderedDict

d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4

for key in d:
    print(key, d['key'])


#=======================================================================================================================
# 1.8 딕셔너리 계산
# 딕셔너리 데이터에 여러 계산을 수행하고 싶다 (최소값, 최대값, 정렬 등등)
#=======================================================================================================================

# 딕셔너리에 주식 이름과 가격이 있다 가정하고, 이것에 대해 유용한 계산을 하려면 딕셔너리의 키와 값을 zip()으로
# 뒤집어주는 것이 좋다. 예를 들어 최소 주가와 최대 주가를 찾는 코드를 살펴보자.

prices = {
    'ACME':45.23,
    'AAPL':612.28,
    'IBM':205.55,
    'HPQ':37.20,
    'FB':10.75
}

min_price = min(zip(prices.values(), prices.keys()))
max_price = max(zip(prices.values(), prices.keys()))

# 계산을 할 때 zip()은 단 한 번만 소비할 수 있는 iterator를 생성한다. 때문에 min을 호출하고, 다시 max를 호출하려고 하거나
# 그 반대의 경우에도 에러가 발생한다.

## 딕셔너리에서 일반적인 데이터 축소를 시도하면, 키 작업만 이루어짐
min(prices)         # AAPL 리턴
max(prices)         # IBM 리턴

## 딕셔너리의 값에 대한 계산을 하려면 values() 메소드를 사용해야 한다.
min(prices.values())
max(prices.values())


## 키와 값 정보까지 알고 싶다면 (ex: 어떤 주식 값이 가장 낮은가?)
min(prices, key=lambda k: prices[k])            # FB 리턴
max(prices, key=lambda k: prices[k])            # AAPL 리턴

##
min_value = prices[min(prices, key=lambda k: prices[k])]


#=======================================================================================================================
# 1.9 두 딕셔너리의 유사점 찾기
# 두 딕셔너리가 있고 여기서 유사점을 찾고 싶다 (동일한 키, 동일한 값 etc)
#=======================================================================================================================
a = {
    'x': 1,
    'y': 2,
    'z': 3
}

b = {
    'w': 10,
    'x': 11,
    'y': 2
}

## 동일한 키 찾기
a.keys() & b.keys()         # {'x', 'y'}

## a에만 있고 b에는 없는 키 찾기
a.keys() - b.keys()         # {'z'}

## (키, 값)이 동일한 것 찾기
a.items() & b.items()       # { ('y', 2) }


## 이것들을 사용해서 특정 키를 제거한 새로운 딕셔너리를 만들 수도 있다.
c = {key:a[key] for key in a.keys() - {'z', 'w'}}
# c는 {'x':1, 'y':2}



#=======================================================================================================================
# 1.10 순서를 깨지 않고 시퀀스의 중복 없애기
# 시퀀스에서 중복된 값을 없애고 싶지만, 아이템의 순서는 유지하고 싶다.
# ㄴ 시퀀스의 값이 hash 가능하다면, set과 generator를 사용해서 쉽게 해결할 수 있다.
#=======================================================================================================================
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)

a = [1, 5, 2, 1, 9, 1, 5, 10]
print(list(dedupe(a)))                  # [1, 5, 2, 9, 10]  중복값이 없이 출력되었다


## hash 안되는 타입(dict)의 중복을 없애려면 아래와 같이 하면 된다.
def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)

a = [ {'x':1, 'y':2}, {'x':1, 'y':3}, {'x':1, 'y':2}, {'x':2, 'y':4} ]
print(list(dedupe(a, key=lambda d: (d['x'], d['y']))))

# 람다람다 @_@~ 근데 이게 왜 dedupe지? dedupe 정의 : to remove duplicate entries from a list or database

## 중복을 없애려면 set을 하는게 가장 쉽당
a = [1, 5, 2, 1, 9, 1, 5, 10]
print(a)
print(set(a))


## 애초에 파일을 읽어 들일때 중복을 무시함려면 아래와 같이 하면 된다
with open(somefile, 'r') as f:
    for line in dedupe(f):
        ....


#=======================================================================================================================
# 1.11 슬라이스 이름 붙이기
# 프로그램 코드에 slice를 지시하는 하드코딩이 너무 많아 이해하기 어려운 상황!!! 도움!!
#=======================================================================================================================
# 삽질 케이스
#### 012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'
record = '...............100     .................513.25 .............'
cost = int(record[30:32])   * float(record[40:48])

# 1년 뒤에도 맨정신 유지가 가능한 좋은 케이스
SHARES = slice(20, 32)
PRICE = slice(40, 48)

## slice를 이용해서 정보 얻기
a = slice(10, 50, 2)
print(a.start)
print(a.stop)
print(a.step)

s = 'HelloWorld'
print(a.indices(len(s)))

for i in range(*a.indices(len(s))):
    print(s[i])

#=======================================================================================================================
# 1.12 시퀀스에 가장 많은 아이템 찾기
# collections.Counter를 쓰고, most_common도 써보자
#=======================================================================================================================
words = [
    'look','into','my','eyes','look','into','my','eyes','the','eyes','the','eyes','the','eyes','not',
    'around','the','eyes',"don't",'look','around','the','eyes','look','into','my','eyes',"you're",'under'
]

from collections import Counter
word_counts = Counter(words)
top_three = word_counts.most_common(3)
print(top_three)


## Counter 객체에는 해시 가능한 모든 아이템을 입력할 수 있다.
print(word_counts['eyes'])

# 카운터 수동 증가
morewords = ['why','are','you','not','looking','in','my','eyes']
for word in morewords:
    word_counts[word] += 1
print(word_counts['eyes'])
print(word_counts.update(morewords))


## 카운터로 여러가지 수식을 사용할 수 있다
a = Counter(words)
b = Counter(morewords)
#print(a)
#print(b)

c = a + b
#print(c)

d = a - b
print(d)


#=======================================================================================================================
# 1.13 일반 키로 딕셔너리 리스트 정렬
# 딕셔너리 리스트가 있고, 하나 혹은 그 이상의 딕셔너리 값으로 이를 정렬하고 싶다.
# ㄴ operator 모듈의 itemgetter 함수를 사용해서 정렬한다
#=======================================================================================================================
rows = [
    {'fname':'Brian', 'lname':'Jones', 'uid': 1003},
    {'fname':'David', 'lname':'Beezley', 'uid': 1002},
    {'fname':'John', 'lname':'Cleese', 'uid':1001},
    {'fname':'Big','lname':'Jones', 'uid': 1004}
]

from operator import itemgetter
rows_by_fname = sorted(rows, key=itemgetter('fname'))       # rows_by_fname 에 따른 정렬 방법
rows_by_uid = sorted(rows, key=itemgetter('uid'))           # rows_by_uid 에 따른 정렬 방법
# print(rows_by_fname)
# print(rows_by_uid)


rows_by_lfname = sorted(rows, key=itemgetter('lname','fname'))
#print(rows_by_lfname)


## 람다로 할 수도 있다.
rows_by_fname = sorted(rows, key=lambda r: r['fname'])
rows_by_lfname = sorted(rows, key=lambda r: (r['lname'], r['fname']))
print(rows_by_fname)
print(rows_by_lfname)


#=======================================================================================================================
# 1.14 기본 비교 기능 없이 객체 정렬
# 동일한 클래스 객체를 정렬해야 하는데, 이 클래스는 기본적인 비교 연산을 제공하지 않는다
#=======================================================================================================================
class User:
    def __init__(self, user_id):
        self.user_id = user_id
    def __repr__(self):
        return 'User({})'.format(self.user_id)

users = [User(23), User(3), User(99)]
#print(users)

## 위의 것을 람다식으로 표현하면
sorted(users, key=lambda u: u.user_id)

## operator.attrgetter()를 사용할 수도 있다. 이 기능의 속도가 가장 빠르다
from operator import attrgetter
#print(sorted(users, key=attrgetter('user_id')))

# min, max에 attrgetter 사용하기
print(min(users, key=attrgetter('user_id')))                # User(3)
print(max(users, key=attrgetter('user_id')))                # User(99)


#=======================================================================================================================
# 1.15 필드에 따라 레코드 묶기
# 일련의 딕셔너리나 인스턴스가 있고 특정 필드 값에 기반한 그룹의 데이터를 순환하고 싶다
# itertools.groupby() 를 쓰자
#=======================================================================================================================
rows = [
    {'address':'5412 N CLARK', 'date':'07/01/2012'},
    {'address':'5148 N CLARK', 'date':'07/04/2012'},
    {'address':'5800 E 58TH', 'date':'07/02/2012'},
    {'address':'2122 N CLARK', 'date':'07/03/2012'},
    {'address':'5645 N RAVENSWOOD', 'date':'07/02/2012'},
    {'address':'1060 W ADDISON', 'date':'07/02/2012'},
    {'address':'4801 N BROADWAY', 'date':'07/01/2012'},
    {'address':'1039 W GRANVILLE', 'date':'07/04/2012'}
]

from operator import itemgetter
from itertools import groupby

#우선 원하는 필드로 정렬한다.
rows.sort(key = itemgetter('date'))

# 그룹 내부에서 순환 시킨다.
for date, items in groupby(rows, key = itemgetter('date')):
    print(date)
    for i in items:
        print('   ', i)

print('07/01/2012')

# groupby() 함수는 시퀀스를 검색하고 동일한 값(혹은 키 함수에서 반환한 값)에 대한 일련의 '실행'을 찾는다. 개별 순환에 대해
# 값, 그리고 같은 값을 가진 그룹의 모든 아이템을 만드는 iterator를 함께 반환한다. #... 뭐라는거야 ㅡㅡ
# groupby()를 쓰기 전에 데이터를 정렬하는 과정이 매우 중요하다. groupby() 함수는 연속된 아이템에만 동작하기 때문이다.

## 단순히 날짜에 따라 data를 묶어서 원할때마다 접근하려는 거라면 defaultdict()를 사용해서 multidict를 구성하는게 낫다.
from collections import defaultdict
rows_by_date = defaultdict(list)
for row in rows:
    rows_by_date[row['date']].append(row)

for r in rows_by_date['07/01/2012']:
    print(r)


#=======================================================================================================================
# 1.16 시퀀스 필터링
# 시퀀스 내부에 데이터가 있고 특정 조건에 따라 값을 추출하거나 줄이고 싶다
# list comprehension을 쓰자        # 그게 뭔데?
#=======================================================================================================================
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
print([n for n in mylist if n > 0])
print([n for n in mylist if n < 0])

## 이상한게 리스트에 들어갔어요! ㅇㅇ 문제없뜸여
values = ['1', '2', '-3', '-', '4', 'N/A', '5']

def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False

ivals = list(filter(is_int, values))
print(ivals)                                    # ['1', '2', '-3', '4', '5']


## 데이터 변형 기능도 있음
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
import math
print([math.sqrt(n) for n in mylist if n > 0])          # 나눈건가??


## 카운트값이 5 이상인 주소만 남겨보자!
addresses = [
    '5412 N CLARK',
    '5148 N CLARK',
    '5800 E 58TH',
    '2122 N CLARK',
    '5645 N RAVENSWOOD',
    '1060 W ADDISON',
    '4801 N BROADWAY',
    '1039 W GRANVILLE'
]

counts = [0,3,10,4,1,7,6,1]

from itertools import compress
more5 = [n > 5 for n in counts]
#print(more5)
print(list(compress(addresses, more5)))


#=======================================================================================================================
# 1.17 딕셔너리의 부분 추출
# 딕셔너리의 특정 부분으로부터 다른 딕셔너리를 만들고 싶다
# 딕셔너리 컴프리헨션을 쓰면 된댘ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ이건 또 뭐야
#=======================================================================================================================
prices = {
    'ACME':45.23,
    'AAPL':612.78,
    'IBM':205.55,
    'HPQ':37.20,
    'FB':10.75
}

# 가격이 200 이상인 것에 대한 딕셔너리
p1 = { key:value for key, value in prices.items() if value > 200}
print(p1)

# 기술 관련 주식으로 딕셔너리 구성
tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = { key:value for key, value in prices.items() if key in tech_names }
print(p2)


#=======================================================================================================================
# 1.18 시퀀스 요소에 이름 매핑
# 리스트나 튜플의 위치로 요소에 접근하는 코드가 있다. 하지만 때론 이런 코드의 가독성이 떨어진다. 또한 위치에 의존하는
# 코드의 구조도 이름으로 접근 가능하도록 수정하고 싶다.
# collections.namedtuple() 파이썬 tuple ㅌ타입의 서브 클래스를 반환하는 팩토리 메소드(??)이다. 타입 이름과 포함해야 할
# 필드를 전달하면 인스턴스화 가능한 클래스를 반환한다. 여기에 필드값을 전달함으로 사용 가능하다.
#=======================================================================================================================
from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr','joined'])
sub = Subscriber('jonesy@example.com', '2012-10-19')

print(sub)
print(sub.addr)
print(sub.joined)

# 결과값
# Subscriber(addr='jonesy@example.com', joined='2012-10-19')
# jonesy@example.com
# 2012-10-19

from collections import namedtuple
Stock = namedtuple('Stock', ['name','shares','price'])
def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total

# namedtuple은 방대한 자료 구조를 효율적으로 쓸 수 있지만, 딕셔너리와 다르게 수정할 수 없다.
# 속성을 수정해야 한다면 namedtuple 인스턴스의 _replace() 메소드를 쓰세용
s = s._replace(shares = 75)                                            # 이거 안되는데
print(s)


#=======================================================================================================================
# 1.19 데이터를 변환하면서 줄이기
# 감소 함수(sum(), min(), max())를 실행해야 하는데, 먼저 데이터를 변환하거나 필터링해야 한다.
# ㄴ 생성자 표현식을 사용하자
#=======================================================================================================================
nums = [1,2,3,4,5]
s = sum(x * x for x in nums)

print(s)

#=======================================================================================================================
# 1.20 여러 매핑을 단일 매핑으로 합치기
# 딕셔너리나 매핑이 여러개 있고, 자료 검색이나 데이터 확인을 위해서 하나의 매핑으로 합치고 싶다
# ㄴ
#=======================================================================================================================
a = {'x':1, 'z':3}
b = {'y':2, 'z':4}

# 두 딕셔너리를 모두 검색해야 할 상황이라면??
from collections import ChainMap            ## 오라클의 업뎃을 쓸 수 없는 뷰 같은 녀석?..인가?
c = ChainMap(a,b)
print(c['x'])
print(c['y'])
print(c['z'])


## ChainMAp 대신 update() 를 사용해서 딕셔너리를 하나로 합칠 수도 있다
a = {'x':1, 'z':3}
b = {'y':2, 'z':4}
merged = dict(b)
merged.update(a)
print(merged['x'])
print(merged['y'])
print(merged['z'])












































































































