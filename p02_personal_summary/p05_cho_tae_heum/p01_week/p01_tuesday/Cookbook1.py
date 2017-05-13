# 1.1 시퀀스를 개별 변수로 나누기

data = ['CHO', 176, 79, (1989, 11, 29)]
name, height, weight, birth = data
name
height
weight
birth

data = ['CHO', 176, 79, (1989, 11, 29)]
name, height, weight, (year, month, day) = data
year
month
day

A = (1, 2)
a, b, c = A  # 되지 않는다. 개별 변수의 수가 일치하지 않는다.

A = 'abcde'
a, b, c, d, e = A
a
b
c
d
e

data = ['CHO', 176, 79, (1989, 11, 29)]
_, _, _, birth = data
birth
_  # 마지막으로 지정한 요소가 튀어나온다.

# 1.2 임의순환체의 요소 나누기

record = ('CHO', 'gh506015@naver.com', '010-5772-5307', '02-2281-5307')
name, email, *phone_number = record
name
phone_number  # *을 붙이지 않는다. 해당하는 값들이 list로 저장된다.

# 리스트 안의 튜플을 이렇게 태그와 아규먼츠로 분리해서 사용도 가능하다.
record = [('foo', 1, 2), ('bar', 'hello'), ('foo', 3, 4)]  # 앞에 붙은 foo, bar을 tag라고 한다.


def do_foo(x, y):
    print('foo', x, y)


def do_bar(s):
    print('bar', s)


for tag, *args in record:
    if tag == 'foo':
        do_foo(*args)

data = ['CHO', 176, 79, (1989, 11, 29)]
name, *_, (year, *_) = data
print(name)
print(year)

items = ['a', 1, 2, 3, 4, 5]
head, *tail = items
head
tail

# 1.3 마지막 N개 아이템 유지(리스트 아이템의 개수유지)

from collections import deque

q = deque(maxlen=3)  # queue는 데이터가 들어가는 방향과 나가는 방향이 서로 다른 데이터프레임
q.append(1)
q.append(2)
q.append(3)
q
q.append(4)
q  # 함수가 걸려있는 데이터 프레임을 유지
q.appendleft(5)  # 이렇게 왼쪽으로도 넣을 수 있다.
q
q = deque()  # 공백으로 deque 선언할 시
q.append(1)
q.append(2)
q.append(3)
q.append(4)
q  # 계속 들어간다.
q.pop()
q.popleft()  # 이 두개는 팁

# 1.4 아이템의 최대 혹은 최소값 찾기

import heapq

nums = [1, 2, 3, 4, 5, 6, 7, -10, -20, -1.5, 200]
print(heapq.nlargest(3, nums))
a = heapq.nlargest(3, nums)
a
a = heapq.nsmallest(3, nums)
a

portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'APPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'YAHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
expensive
cheap = heapq.nsmaillest(2, portfolio, key=lambda s: s['price'])
cheap

nums1 = (1, 2, 3, 4, 5, 6, 7, -10, -20, -1.5, 200)
heap = list(nums1)  # 튜플을 리스트로
heap
nums2 = [1, 2, 3, 4, 5, 6, 7, -10, -20, -1.5, 200]
heap = tuple(nums2)  # 리스트를 튜플로
heap

nums1 = (1, 2, 3, 4, 5, 6, 7, -10, -20, -1.5, 200)
heap = list(nums1)  # 튜플을 리스트로 바꿔준 후에
heapq.heapify(heap)  # heapify함수 걸어주기 참조:http://priv.tistory.com/61
heap  # 아이템의 수가 상대적으로 많을때 가장 빠르게 최소값을 찾아준다.

heapq.heappop(heap)  # 계속 반복해주면서 최소값을 찾아준다. 찾은 것은 list에서 하나씩 빠진다.


# 무성이한테 물어봐서 이해요망이다.!!!!!
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


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
q.pop()  # 사실 이해가 하나도 안됨 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ
# heappop는 항상 가장 작은 아이템을 반환해서 큐의 팝이 올바른 아이템에 적용될 수 있도록 함

a = Item('foo')
b = Item('bar')
a < b  # 우선순위 값이 달라야만 비교가 가능하다.(뭔 말임?)

a = (1, Item('foo'))
b = (5, Item('bar'))
a < b
c = (1, Item('grok'))
a < c  # 동일한 우선순위 값을 가진 아이템의 비교는 실패한다.

a = (1, 0, Item('foo'))
b = (5, 1, Item('bar'))
c = (1, 2, Item('grok'))
a < c  # 인덱스값을 포함해줌으로써 비교 가능해짐.

d = {'a': [1, 2, 3], 'b': [4, 5]}  # key:values
e = {'a': {1, 2, 3}, 'b': {4, 5}}  # 여기서 중괄호는 딕셔너리가 아니라 '세트'라고 한다.
# 아이템의 삽입 순서를 지켜야 한다면 list를 사용하는 것이 좋고
# 순서 상관없이 중복을 제거하려면 set를 사용하는 것이 좋다.

from collections import defaultdict

d = {}  # 이 상황에서는 존재하지 않는 key에 대해서 딕셔너리에 값을 추가할 수 없다.
d = defaultdict(list)  # 하지만 이렇게 해주면 key를 만들고 values를 추가할 수 있다.
d['a'].append(1)  # 딕셔너리의 key에 a를 만들고 거기에 1을 추가해라.
d['a'].append(2)
d['b'].append(3)
d

d = defaultdict(set)  # 중복을 제거하는 세트 딕셔너리
d['a'].add(1)
d['a'].add(2)
d['b'].add(1)
d

d = {}
for key, value in pairs:
    if key not in d:  # d 딕셔너리에 key가 존재하지 않으면
        d[key] = []  # key를 추가하고
    d[key].append(value)  # value를 넣어라

d = defaultdict(list)
for key, value in pairs:  # pair 정의하라고 하는데 뭐지??????????????????
    d[key].append(value)  # 알아서 만들어서 넣어줌

d = defaultdict(list)


def func(key, value):
    d[key].append(value)


func('a', 1)

from collections import OrderedDict

d = OrderedDict()
d['foo'] = 1, 2, 3  # 이렇게도 가능
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4
d

import json

json.dumps(d)
# Out[77]: '{"foo": 1, "bar": 2, "spam": 3, "grok": 4}'  신기하다.

prices = {'ACME': 12,
          'AAPL': 612,
          'IBM': 203,
          'HPQ': 45,
          'FB': 929.23}

min_price = min(zip(prices.values(), prices.keys()))  # keys, values!!!!
min_price
max_price = max(zip(prices.values(), prices.keys()))
max_price

price_sorted = sorted(zip(prices.values(), prices.keys()))
price_sorted

# 딕셔너리에서 일반적인 데이터 축소를 시도하면 오직 key에 대해서만 작업이 이루어진다.
min(prices)
max(prices)

min(prices.values())
max(prices.values())
min(prices.keys())  # 요고도 됨 ㅋㅋㅋ

min(prices, key=lambda k: prices[k])  # 처음 key
max(prices, key=lambda k: prices[k])  # 마지막 key

min_value = prices[min(prices, key=lambda k: prices[k])]
min_value

prices = {'AAA': 45.23, 'ZZZ': 45.23}
min(zip(prices.values(), prices.keys()))
max(zip(prices.values(), prices.keys()))
# vlaues값이 같을 경우 key의 값에 따라서 결정된다.


# 1.9 두 딕셔너리의 유사점 찾기(key값에 연산자 사용하기)
a = {'x': 1, 'y': 2, 'z': 3}
b = {'w': 10, 'x': 11, 'y': 2}

# 동일한 key찾기, 다른 key찾기, 키와 값이 동일한 것 찾기
a.keys() & b.keys()
a.keys() - b.keys()
a.items() & b.items()  # 같은게 없으면 'set()'이 출력된다.

c = {key: a[key] for key in a.keys() - {'x', 'z'}}
# a의 key들 중에서 x와 z를 제외한 키와 밸류를 계속 추가해라(loop)
c


# 1.10 순서를 깨지 않고 시퀀스의 중복 없애기

def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            # return은 하나의 값만 가능하고 하는 순간 def에서 나오기 때문에 여러개의 값을 리턴해야 할 경우에 yield를 쓴다.
            seen.add(item)


a = [1, 5, 2, 1, 9, 1, 5, 10]
list(dedupe(a))  # yield한 여러개의 값을 list 에 담아준다.
dedupe(a)  # 이렇게는 쓰지 못한다. 담아줄 list가 없기 때문에


# deduplication 데이터의 중복을 제거한다는 뜻이다.

# 참고!!!!!!!!!!!
def gen():
    for i in range(11):
        yield i ** 3


def gen():
    for i in range(11):
        return i ** 3  # 이렇게 쓰지 못한다. 하나의 값이 아니기 때문에


for x in gen():
    print(x)


# 함수 이해 안됨!! 안돌아가############################################
def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            # return은 하나의 값만 가능하고 하는 순간 def에서 나오기 때문에 여러개의 값을 리턴해야 할 경우에 yield를 쓴다.
            seen.add(item)


a = [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}]
list(dedupe(a, key=lambda d: (d['x'], d['y'])))
######################################
# 중복을 없애려면 set를 만드는 것이 가장 쉽다!
a = [1, 5, 2, 1, 9, 1, 5, 10]
b = set(a)  # a의 자료형을 바꾸지는 않는다.
b  # 하지만 데이터의 순서가 훼손된다.

# 1.11 슬라이스 이름 붙이기

record = '123456789123456789123456789123456789123456789123456789'
cost = int(record[27:30]) * float(record[2:6])
cost  # 이거슨 하드코딩

SHARES = slice(27, 30)  # 27번째에서 30번째를 자르는 함수라고 생각하면 편하다
SHARES  # 그러니까 slice(1, 4)는 1:4를 미리 선언한다고 보면된다.
PRICE = slice(30, 33)

items = [0, 1, 2, 3, 4, 5, 10]
items[2:5]
a = slice(2, 5)
items[a]
# item을 바꾸기도 한다.
items[a] = [6, 7, 8]  # 이거로 바꾸겠다.
items
del items[a]  # 해당하는 문자열 지우겠다
items

a = slice(1, 6, 2)  # 1번부터 5번까지 공차(step) 2단위로 잘라라. 문자열, item다 가능
items[a]
a.start
a.stop
a.step

# 1.12 시퀀스에 가장 많은 아이템 찾기

# Counter함수와 most_common 메소드
words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'not',
    'not', 'not', ]

from collections import Counter

word_count = Counter(words)
word_count
top_three = word_count.most_common(3)
top_three  # 튜플로 저장된다.

Counter(words)['not']
# 4
word_count['not']
# 4

a = Counter(words)
a
b = Counter(morewords)
b
c = a + b
c
d = a - b
d

# 1.13 일반키로 딕셔너리 리스트 정렬
rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'UID': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'UID': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'UID': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'UID': 1004}
]

from operator import itemgetter

rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_lname = sorted(rows, key=itemgetter('lname'))
rows_by_fname
rows_by_lname
rows_by_lfname = sorted(rows, key=itemgetter('lname', 'fname'))
rows_by_lfname
# 두개 이상의 key를 기준으로 정렬할 수 있다.

# min(), max()함수도 사용가능
min(rows, key=itemgetter('UID'))
max(rows, key=itemgetter('fname'))


# 1.14 기본비교 기능 없이 객체 정렬

class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return 'User({})'.format(self.user_id)


users = [User(23), User(3), User(4)]
users
sorted(users, key=lambda u: u.user_id)
# Out[282]: [User(3), User(4), User(23)]
min(users, key=lambda u: u.user_id)
max(users, key=lambda u: u.user_id)

# 1.15 필드에 따라 레코드 묶기

rows = [
    {'address': '5412 N CLARK', 'date': '07/01/2012'},
    {'address': '5148 N CLARK', 'date': '07/04/2012'},
    {'address': '5800 N 58TH', 'date': '07/02/2012'},
    {'address': '2122 N CLARK', 'date': '07/03/2012'},
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
    {'address': '1060 N ADDISON', 'date': '07/02/2012'},
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
    {'address': '1039 N GRANVILLE', 'date': '07/04/2012'}
]
from operator import itemgetter
from itertools import groupby

rows.sort(key=itemgetter('date'))  # data 자체를 변경한다. sorted와 다름
rows
for date, items in groupby(rows, key=itemgetter('date')):  # 정렬하려는 key와 그 key를 포함하는 dict로 나눈다. (date, items)
    print(date)  # date 출력
    for i in items:
        print('   ', i)  # items 출력, 구분되도록 앞에 공백 줘서
# groupby함수는 연속된 아이템에만 동작하기 때문에 정렬과정을 생략하면 원하는대로 실행불가

rows_by_date = defaultdict(list)
for row in rows:
    rows_by_date[row['date']].append(row)
    # date에다가 그 date에 해당하는 row를 붙인다.
rows_by_date
for r in rows_by_date['07/01/2012']:
    print(r)

# 1.16 시퀀스 필터링

mylist = [1, 4, -5, 10, -7, 2, 3, -1]
a = [n for n in mylist if n > 0]
a
b = (n for n in mylist if n > 0)
b
# 이거슨 제너레이터 대용량 데이터를 처리할 때 momory(list)에 올려놓고 작업을 할 수 없기 때문에 disk에 넣어놓고 한줄씩 memory에 올려서 처리한다.
for i in b:
    print(i)

values = ['1', '2', '3', '-4', '-', 'N/A', '5']


def is_int(val):
    try:
        x = int(val)
        return True  # int(val) 넣어보고 들어가면 true
    except ValueError:
        return False  # 안들어가서 valueerror뜨면 예외처리


ivals = list(filter(is_int, values))
# 이터레이터 생성, is_int에 values값들을 차례대로 넣어서 TRUE인 것들만 돌려준다.
# filter 함수는 첫 번째 인수로 함수 이름을, 두 번째 인수로 그 함수에 차례로 들어갈 반복 가능한 자료형을 받는다.
# 그리고 두 번째 인수인 반복 가능한 자료형 요소들이 첫 번째 인수인 함수에 입력되었을 때
# 리턴값이 참인 것만 묶어서(걸러내서) 돌려준다.
print(ivals)

mylist = [1, 4, -5, 10, -7, 2, 3, -1]
import math

a = [math.sqrt(n) for n in mylist if n > 0]  # sqrt는 square root 제곱근
b = [n if n > 0 else 0 for n in mylist]
b

prices = {
    'ACME': 45.23,
    'APPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}
p1 = {a: b for a, b in prices.items() if b > 200}
p1 = {key: value for key, value in prices.items() if value > 200}
# key와 value로 분리해서 .items()를 사용해야 한다.
p1
p2 = {key: value for key, value in prices if value > 200}
# 이렇게 안된다.

tach_names = {'APPL', 'IBM', 'HPQ'}
p3 = {key: value for key, value in prices.items() if key in tach_names}
p3

# 1.18 시퀀스 요소에 이름 매핑

from collections import namedtuple

Subscriber = namedtuple('Subscriber1', ['addr', 'joined'])  # 타입이름, 매핑할 변수명
sub = Subscriber('gh506015@naver.com', '2012.12.12')
sub
sub.addr
sub.joined

addr, joined = sub
addr
joined

Stock = namedtuple('Stock', ['name', 'shares', 'price'])


# 매핑할 namedtuple을 만들어 놓고....
def compute_cost(records):
    total = 0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total


records = [['a', 0.75, 10], ['b', 0.25, 12]]
compute_cost(records)  # 이렇게 실행해주시면 됩니다.!!@#@#!

s = Stock('ACME', 100, 123.45)
s
s.shares = 75
# tuple이기 때문에 수정할 수 없다. _replace함수를 이용해 수정하는 방법이 있다.
# 하지만 굳이 따지자면 수정하는 것이 아니라 수정을 한 완전히 새로운 데이터프레임을 만든 것
s._replace(shares=75)  # 튜플 수정

# 1.19 데이터를 변환하면서 줄이기
nums = [1, 2, 3, 4, 5]
s = sum(n ** 2 for n in nums)
s

portfolio = [
    {'name': 'GOOG', 'shares': 50},
    {'name': 'APPL', 'shares': 30},
    {'name': 'SAMS', 'shares': 10},
    {'name': 'LG', 'shares': 5}
]

min_shares = min(s['shares'] for s in portfolio)
min_shares

# 1.20 여러매핑을 단일 매핑으로 합치기
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
from collections import ChainMap

c = ChainMap(a, b)

print(c['x'])
print(c['y'])
print(c['z'])  # 중복값이 있으면 첫번째 key를 받아서 사용한다. a의 z
# ChainMap은 매핑을 여러개 받아서 하나처럼 보이게 만든다. 하지만 실제로 하나로 합친건 아님

# 대부분의 명령이 동작한다.
print(len(c))  # 중복된 것은 제거하고 출력한다.
list(c.keys())
list(c.values())
c
del c['x']
del c['z']  # 첫번째 z가 지워지고 나서 두번째 z는 찾을 수 없다고 예외처리된다.
c
del a['x']
a

values = ChainMap()  # 체인맵 선언한 후에...
values['x'] = 1  # 새로운 매핑 추가
values['y'] = 2
values['x'] = 3
values
values.new_child()  # 실제로 데이터프레임이 바뀌지는 않기 때문에....
values = values.new_child()  # 이렇게 다시 선언!!
values['x'] = 2
values
values = values.new_child()
# 비어있는 딕셔너리에 골라서 넣을 수 없기 때문에 넣을때마다 딕셔너리 추가
# 데이터는 앞으로 들어간다.
values['y'] = 3
values
values = values.parents  # 마지막매핑(딕셔너리)부터 삭제, 스택구조 데이터
values

a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
type(b)
merged = b
merged
merged.update(a)  # update가능
merged
# 딕셔너리를 새로 만드는 것이기 때문에 원본이 변해도 영향을 받지 않는다.
# 하지만@@@@하지만@@@@하지만@@@@하지만@@@@하지만@@@@
merged = ChainMap(a, b)  # 원본을 참조하는 ChainMap의 경우
a['x'] = 42  # 원본이 바뀌면
merged['x']  # ChainMap도 변한다.

a = 'askja. amsa clskd. sk adf jdk ds/ adf  ka;a;dkf'
import re

line = re.split(r'[.,/;:\s]\s*', a)  # 대괄호 안에 있는 것을 제외하고
line  # 바깥에 있는 문자가 붙어있는 경우도 제외

fields = re.split(r'(.|,|/|;|:|\s)\s*', a)
fields
