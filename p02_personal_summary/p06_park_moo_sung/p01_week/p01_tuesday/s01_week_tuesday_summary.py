#1. 자료구조와 알고리즘

1.1 시퀀스를 개별 변수로 나누기

•    data = [1, 2, 3, (2012, 12, 21)]
__, two, three, (year, month, date) = data
라고 치면 각 요소가 변수에 들어감

•    s = 'HELLO'
a, b, c, d, e = s
라고 치면 각 글자가 변수에 들어감

1.2 별 표현식을 활용한 임의 순환체 요소 나누기(*args)

•    record = ('a', 'b', 'c', 'd', 'e')
A, B, *C, E = record
print(*C)
--> c, d

•    records = [('a', 1, 2), ('b', 3, 4), ('c', 5, 6, 7, 8)]
for letter, *number in records:
    print('letter', letter)
    print('number', *number)

•    items = [1, 10, 7, 4, 5, 9]
head, *tail = items
print(head)
print(tail)


def sum(items):
    head, *tail = items
    return head + sum(tail) if tail else head  # tail 이 있다면 return head+sum(tail) 하고
    # tail 없다면 head 를 출력하라


print(sum(items))

1.3 마지막 n개 아이템 유지하기(collections.deque)

•    from collections import deque

q = deque(maxlen=3)

q.append(1)
print(q)
# deque([1], maxlen=3)
q.append(2)
print(q)
# deque([1, 2], maxlen=3)
q.append(3)
print(q)
# deque([1, 2, 3], maxlen=3)
q.append(4)  # 오른쪽에 붙이니 맨 왼쪽 꺼가 빠지고
print(q)
# deque([2, 3, 4], maxlen=3)

q.appendleft(5)  # 왼쪽에 붙이면 맨오른쪽 꺼가 빠진다
print(q)
# deque([5, 2, 3], maxlen=3)

q.pop()
print(q)
# deque([5, 2], maxlen=3)

q.popleft()  # 왼쪽꺼가 빠지네
print(q)
# deque([2], maxlen=3)

print(list(q))
# [2]

print(q)
# deque([2], maxlen=3)      # list(q) 해도 q 자체는 변하지 x

print(tuple(q))  # tuple(q) 하면 왜 (2,)으로 되는거지?
# (2,)

1.4 N 아이템의 최대, 최소값 찾기(heapq)

•    import heapq

nums = [0, 5, 4, 3, 2, 1]
print(heapq.nlargest(3, nums))
# [5, 4, 3]
# 큰 순서대로 3개 뽑기
print(heapq.nsmallest(3, nums))
# [0, 1, 2]
# 큰 순서대로 3개 뽑기

•    import heapq

portfolio = [{'a': 0, 'b': 3, 'c': 'ABC'},
             {'a': 1, 'b': 4, 'c': 'DEF'},
             {'a': 2, 'b': 5, 'c': 'GHI'}]
low = heapq.nsmallest(2, portfolio, key=lambda portfolio: portfolio['a'])
print(low)
# [{'a': 0, 'b': 3, 'c': 'ABC'}, {'a': 1, 'b': 4, 'c': 'DEF'}]
# key 는 nsmallest 데이터 뽑을 때 기준이 되는 데이터를 설정해주는 역할
# key 에 따라 포트폴리오의 각 'a' 값이 작은 순서대로 두 개의 딕셔너리가 뽑힘

high = heapq.nlargest(2, portfolio, key=lambda portfolio: portfolio['b'])
print(high)
# [{'a': 2, 'b': 5, 'c': 'GHI'}, {'a': 1, 'b': 4, 'c': 'DEF'}]
# key 에 따라 포트롤리오의 각 'b' 값이 큰 순서대로 두 개의 딕셔너리가 뽑힘

•    import heapq

nums = [5, 4, 3, 2, 1]
heapq.heapify(nums)
# heapq.heapify 는 해당 리스트를 힙으로 정렬시켜서 리스트로 다시 리턴해주는 함수
print(nums)
# [1, 2, 3, 5, 4] 는 힙으로 정렬됨. 첫번째 숫자는 리스트 내 가장 작은 숫자가 됨!!

print(heapq.heappop(nums))
# 1
# 리스트 내 가장 작은 값을 출력해줌.(가장 왼쪽에 놓인 숫자를 출력해줌)
print(heapq.heappop(nums))
# 2
print(heapq.heappop(nums))
# 3
print(heapq.heappop(nums))
# 4


nums = [5, 4, 3, 2, 1]
print(heapq.heappop(nums))
# 5
# 힙으로 정렬시켜주지 않으면 첫번째 heappop에서는 가장 왼쪽에 놓인 숫자를 출력해줌
print(heapq.heappop(nums))
# 1
# 두번째 heappop 부터는 남은 수 중 가장 작은 수를 출력해줌
print(heapq.heappop(nums))
# 2
print(heapq.heappop(nums))
# 3

1.5 우선순위 큐 구현(heapq)

•    import heapq


class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Item{!r}'.format(self.name)
        # print(Item('foo')) --> Item'foo'
        return 'Item{}'.format(self.name)
        # print(Item('foo')) --> Itemfoo

# repr
>> > repr('test')
"'test'"
>> > str('test')
'test'
>> > repr(1L)
'1L'
>> > str(1L)
'1'

•    import heapq


class PriorityQueue:
    def __init__(self):
        self.__queue = []
        self.__index = 0

    def push(self, item, priority):
        heapq.heappush(self.__queue, (-priority, self.__index, item))
        self.__index += 1

    def pop(self):
        return heapq.heappop(self.__queue)[-1]


class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Item{!r}'.format(self.name)


A = [1, 2, 3]
print(A.pop())
# 3
print(A)
# [1,2]
# pop 은 제일 오른쪽 요소를 출력하고, 리스트에서 지워줌

q = PriorityQueue()
q.push(Item('aaa'), 1)
q.push(Item('bbb'), 2)
q.push(Item('ccc'), 1)
q.push(Item('ddd'), 2)
# Item'ccc' Item'aaa' Item'ddd' Item'bbb' 이 순서대로 들어가 있음
# 같은 우선순위인 경우, 나중에 들어간게 더 왼쪽에 놓임
print(q.pop())
# Item'bbb'
print(q.pop())
# Item'ddd'
print(q.pop())
# Item'aaa'
print(q.pop())
# Item'ccc'


# 대체 왜 써야하는가?

순서 비교할 수 없는 문자(ex: Item'aaa', Item'bbb') 등을 비교하기 위해

heapq를 안 쓰는 경우 방법: 튜플을 만든다.튜플의 첫번째 요소(우선순위 숫자 or 인덱스)부터 비교하고
                        비교결과가 나오면 뒤에 있는 요소(문자) 는 비교x

(우선순위, 비교할 문자)
a = (1, Item'aaa')
b = (2, Item'bbb')
a < b --> True

만약 우선순위가 같을 경우에는 (우선순위, 인덱스, 비교할 문자)
a = (1, 0, item'aaa')
b = (1, 1, item'bbb')
a < b --> True

1.6 딕셔너리의 키를 여러 값에 매핑하기(collections.defaultdict)

•    딕셔너리 하나의 key에 여러 value를 입력하고 싶다면?
d = {'a': [1, 2, 3], 'b': [4, 5]}  # [  ] 는 리스트. 아이템 삽입 순서 지키려면 사용
e = {'a': {1, 2, 3}, 'b': {4, 5}}  # {   } 는 세트. 삽입 순서 상관 없고 중복 없앨 때 사용

•    리스트로 만들기
from collections import defaultdict

d = defaultdict(list)
d['a'].append(2)
d['a'].append(1)
d['a'].append(1)
d['b'].append(3)

print(d)
# defaultdict(<class 'list'>, {'a': [2, 1], 'b': [3]})
print(d['a'][0])
# 1

d = defaultdict(set)
d['a'].add(2)
d['a'].add(1)
d['a'].add(1)
d['b'].add(3)

print(d)
# defaultdict(<class 'set'>, {'a': {1, 2}, 'b': {3}})
# set는 중복 제거, 입력된 순서 상관 없이 정렬됨
print(d['a'])
# {1, 2}
print(d['a'][0])
# 에러 남. set는 인덱싱 못 씀

•    활용 방법
from collections import defaultdict

d = defaultdict(list)
for key, value in group:
    d[key].append(value)

1.7 딕셔너리 순서 유지(collections.OrderedDict)

•    입력한 순서에 따라 저장됨
•    but 저장용량이 2배로 큼(뭔지는 모르지만 doubly linked list)...?


1.8 딕셔너리 계산(zip)

•    price = {'f': 100, 'b': 5, 'c': 3}
print(min(price))
# 그냥 min 해버리면 key 중 가장 작은 key를 출력(이 경우 알파벳 중 가장 순서가 빠른 b 출력)

# value 값을 비교하고 싶다면 zip() 을 이용해 key 와 value 순서 바꿔주기
print(zip(price.values(), price.keys()))
# 이래도 값은 안 나옴
print(min(zip(price.values(), price.keys())))
# (3, 'c')
# 값이 바뀌어서 나옴
# 한번 쓴 zip 은 또 못 씀. 또 쓰려면 에러남.(단 한번만 소비할 수 있는 이터레이터 생성하므로)
# 만약 다른 key가 동일한 value를 쓰고 있을 때는 min을 구하면 key가 가장 작은 쪽을, max를 구하면 key 가 가장 큰 쪽을 출력해줌
print(price)
# zip 을 써도 딕셔너리 자체는 바뀌지 않음

•    딕셔너리 최소 value 값의 키와 value 구하고 싶을때는?
print(min(price, key=lambda k: price[k]), price[min(price, key=lambda k: price[k])])
# value 최소일 때의 key            # value 최소일 때의 key를 넣어서 value 출력

1.9 두 딕셔너리의 유사점 찾기( &, -, items())

•    동일한 키 찾기
a.keys() & b.keys()

•    a에만 있는 키 찾기
a.keys() - b.keys()

•    key, value 모두  동일한 것 찾기
a.items() & b.items()

a = {'x': 1, 'y': 2, 'z': 3}
print(a.items())
# dict_items([('x', 1), ('y', 2), ('z', 3)])

•    특정 키 제거하고 새로운 딕셔너리 만들기
a = {'x': 1, 'y': 2, 'z': 3}
c = {key: a[key] for key in a.keys()}
print(c)
# { 'x':1,'y':2,'z':3 }
# a 딕셔너리를 복사하는 방법
a = {'x': 1, 'y': 2, 'z': 3}
c = {key: a[key] for key in a.keys() - {'x'}}
print(c)
# {'y': 2, 'z': 3}
# 특정 키('x') 제거하고 딕셔너리 복사하는 방법

1.10 순서를 깨지 않고 시퀀스의 중복 없애기(set) - --- 무슨 말이야

•    해시 가능한 경우


def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)


a = [1, 2, 3, 5, 1, 2, 3, 5]
print(list(dedupe(a)))
# [1,2,3,5]
# 이해가 안되네

•    해시 불가능한 경우


def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(item)


a = [1, 2, 3, 5, 1, 2, 3, 5]
print(list(dedupe(a)))
# 이해가 안되네222

•    활용(파일 로드할 때 중복된 라인 무시하려면)
with open(somefile, 'r') as f:
    for line in dedupe(f):

1.11 슬라이스 이름 붙이기(slice)

•    안 좋은 예
record = '12312412415910190259102951'
cost = int(record[5:9]) * float(record[15:20])
print(cost)
# 잘라낸 게 뭘 뜻하는지 모름

•    slice 써서 이름 붙임
record = '12312412415910190259102951'
shares = slice(5, 9)
price = slice(15, 20)
cost = int(record[shares]) * float(record[price])
print(cost)
# 잘라낸 것에 이름 붙임

•    이런 것도 가능
items = [0, 1, 2, 3, 4, 5]
a = slice(2, 4, 2)  # 2부터 4 미만까지 공차는 2로
print(items[a])
del items[a]
print(items)
# del ~~~~ 는 리스트에서 지우는 명령어임

1.12 시퀀스에 가장 많은 아이템 찾기(collections.counter) - --- 매우 유용

•    리스트 내 각 변수들의 개수 세기
words = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a',
         'b', 'b', 'b', 'b',
         'c', 'c']

from collections import Counter

word_count = Counter(words)
print(word_count)
# Counter({'a': 8, 'b': 4, 'c': 2})
# 딕셔너리 형태로 출력해줌
print(word_count['a'])
# 8
# 딕셔너리처럼 쓸 수 있음
most_count_word = word_count.most_common(3)
print(most_count_word)
# [('a', 8), ('b', 4), ('c', 2)]

•    업데이트하기
more_words = ['a', 'a', 'b', 'c']
word_count.update(more_words)
print(word_count)
# Counter({'a': 10, 'b': 5, 'c': 3})
# 쉽게 업데이트 가능

a = Counter(words)
b = Counter(more_words)

•    더하고 빼기
print(a + b)
# Counter({'a': 10, 'b': 5, 'c': 3})
# 쉽게 더할 수 있고
print(a - b)
# Counter({'a': 6, 'b': 3, 'c': 1})
# 쉽게 뺄 수 있다

1.13 일반 키로 딕셔너리 리스트 정렬(operator.itemgetter)

•    itemgetter 쓴 버전
from operator import itemgetter

rows = [{'a': 1, 'b': 2, 'c': 3}, {'a': 3, 'b': 1, 'c': 2}, {'a': 1, 'b': 3, 'c': 1}]
row_by_abname = sorted(rows, key=itemgetter('a', 'b'))
print(row_by_abname)
# [{'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'b': 3, 'c': 1}, {'a': 3, 'b': 1, 'c': 2}]
# key = itemgetter의 'a', 'b'의 value값을 기준으로


•    lambda 쓴 버전
row_by_abname = sorted(rows, key=lambda r: (r['a'], r['b']))
print(row_by_abname)
# [{'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'b': 3, 'c': 1}, {'a': 3, 'b': 1, 'c': 2}]
# 위에꺼랑 원리는 같음. but 성능은 위에꺼가 더 좋음

1.14 기본 비교 기능 없이 객체 정렬(operator.attrgetter)

•    attrgetter 쓴 버전
from operator import attrgetter


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return 'User({})'.format(self.user_id)


users = [User(23), User(3), User(99)]
print(users)
# [User(23), User(3), User(99)]

•    lambda 쓴 버전
print(sorted(users, key=lambda k: k.user_id))
# [User(3), User(23), User(99)]

print(min(users, key=attrgetter('user_id')))

1.15 필드에 따라 레코드 묶기(operator.itemgetter, itertools.groupby)

•    groupby
from operator import itemgetter
from itertools import groupby

rows = [{'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'b': 3, 'c': 4}, {'a': 5, 'b': 6, 'c': 7}, {'a': 8, 'b': 9, 'c': 2}]

rows.sort(key=itemgetter('a'))

# groupby 는 연속된 아이템에만 동작하므로 미리 sort 해주기

for a, args in groupby(rows, key=itemgetter('a')):
    print(a)
    for arg in args:
        print(arg)

#
1
{'a': 1, 'b': 2, 'c': 3}
{'a': 1, 'b': 3, 'c': 4}
5
{'a': 5, 'b': 6, 'c': 7}
8
{'a': 8, 'b': 9, 'c': 2}

1.16 시퀀스 필터링(filter)

•    간단한 필터링
my_list = [1, 2, 3, 4, -1, -2, -3, -4]
print([i for i in my_list if i > 0])
# [1, 2, 3, 4]


•    복잡한 필터링
pos = (i for i in my_list if i > 0)
print(pos)
for x in pos:
    print(x)
# 입력된 내용이 커서 매우 큰 결과 생성되는게 싫다면
# 생성자 표현식을 사용해 값을 걸러낼 수 있음(...?)

my_hard_list = ['1', '2', '-3', 'a', 'b', 'c']


# a,b,c를 걸러내기 애매할때는 filter 쓰기

def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False


ivals = list(filter(is_int, my_hard_list))
print(ivals)
# ['1', '2', '-3']
# filter() 는 이터레이터 생성(?). 결과의 리스트 만들고 싶으면 list()도 써야 함

1.17 딕셔너리의 부분 추출

•    딕셔너리 컴프리헨션
prices = {'a': 5, 'b': 4, 'c': 3}
p1 = {key: value for key, value in prices.items() if value > 4}
print(p1)

1.18 시퀀스 요소에 이름 매핑(collections.namedtuple)

•    namedtuple 사용법
from collections import namedtuple

Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('abc@naver.com', '2012-10-19')
print(sub)
# Subscriber(addr='abc@naver.com', joined='2012-10-19')
print(sub.addr)
# abc@naver.com

a, b = sub
print(a)
# abc@naver.com
print(b)
# 2012-10-19

•    활용법
from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price'])


def comput_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total

# 가독성 좋고, 자료의 구조형에 영향 크게 안 받음
# but 수정할 수 없음

•    내용을 바꾸고 싶을때
from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price'])
s = Stock('a', 1, 2)
print(s)
# s.shares = 75 라고 바꾸려 해도 에러남. 수정 불가
s = s._replace(shares=75)
print(s)
# Stock(name='a', shares=75, price=2)
# 바꾸려면 _replace   (이때 _는 1개) 써야함

•    default 값 주고 필요할 때 내용만 추가하려면?
Stock = namedtuple('Stock', ['name', 'shares', 'price', 'date', 'time'])
stock_prototype = Stock('', 0, 0, None, None)


# 프로토타입 만들기
def dict_to_stock(s):
    return stock_prototype._replace(**s)


# 프로토타입에 내용 넣는 함수
a = {'name': 'a', 'price': 1}
print(dict_to_stock(a))
# Stock(name='a', shares=0, price=1, date=None, time=None)

1.19 데이터 변환하며 줄이기

•    신박한 생성자 표현식
nums = [1, 2, 3, 4, 5]
s = sum(x * x for x in nums)
print(s)
# 1*1 + 2*2 + 3*3 + 4*4 + 5*5 와 같음

•    딕셔너리에서 신박한 생성자 표현식
# 이 방법도 있고
portfolio = [{'name': 'a', 'shares': 1}, {'name': 'b', 'shares': 3}, {'name': 'c', 'shares': 5}]
min_shares = min(p['shares'] for p in portfolio)
print(min_shares)
# 1

# 요 방법도 있네!
min_shares = min(portfolio, key=lambda k: k['shares'])
print(min_shares)
# {'name': 'a', 'shares': 1}
print(min_shares['shares'])
# 1

1.20 여러 매핑을 단일 매핑으로 합치기(collections.ChainMap)

•    두 개 이상의 딕셔너리 한번에 검색하기
from collections import ChainMap

a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
c = ChainMap(a, b)
print(c['x'])
# 1
print(c['y'])
# 2
print(c['z'])
# 3 --> a부터 검색하고 없으면 b 검색.(중복키 있을 때는 첫번재 값만 사용)

•    ChainMap 의 값 변경하기(무조건 첫번째 딕셔너리에만 영향 줌)

c['z'] = 10
# 키가 둘다 있어도 첫번째 딕셔너리 value만 변경
c['w'] = 20
print(a)
# {'x': 1, 'z': 10, 'w': 20}
# 키가 둘다 없는 경우 첫번째 딕셔너리 value만 추가
c['y'] = 30
print(b)
# 변화 없음
# 첫 번째 딕셔너리에 없는 키는 바꿀 수 없음.

•    업그레이드 활용법

values = ChainMap()
values['x'] = 1
values = values.new_child()
# new_child()는 새로운 매핑 추가하는 함수
values['x'] = 2
values = values.new_child()
values['x'] = 3
print(values)
# ChainMap({'x': 3}, {'x': 2}, {'x': 1})
# 완전 신기함
print(values['x'])
# 3
# 키가 동일한 경우 마지막으로 넣은 value 값 출력
values = values.parents
# parents는 마지막 매핑 삭제하는 함수
print(values)
# ChainMap({'x': 2}, {'x': 1})

•    Chainmap 대신 update를 활용한 방법

a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
merged = dict(b)
merged.update(a)
print(merged['z'])
# 3. update 된 value가 출력됨
# but ChainMap 과는 달리 원본 딕셔너리 참조x
# 원본 딕셔너리 변경돼도 반영되지 않는 문제
















