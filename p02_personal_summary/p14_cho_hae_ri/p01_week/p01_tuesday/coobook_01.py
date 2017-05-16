1.1
시퀀스를
개별
변수로
나누기

data = ['haery', '26', 'qwer', '01026098364']
name, age, qwer, phone_number = data
print(name)
print(age)
print(phone_number)

결과
haery
26
010260
98364

** 요소
개수가
일치하지
않으면
오류
발생.
p = [1, 2]
x, y, z = p
print(x)
print(y)

ValueError: not enough
values
to
unpack(expected
3, got
2)

언패킹(unpacking)
은
튜플이나
리스트
뿐
`아니라, 순환
가능한
모든
객체에
사용
가능하다.문자열, 파일, 이터레이터, 제너레이터가
포함된다.

언패킹할
때, 특정값을
무시하는
방법도
있다.단순히
버릴
변수명을
지정
가능

data = ['peony', '34', '84.2', (12, 3, 54)]
_, name, price, _ = data
print(name)
print(price)

34
84.2

1.2
임의
순환체의
요소
나누기

언패킹할
때
요소가
N개
이상
포함되어
"값이 너무 많습니다."
라는
예외가
발생할
경우
별
표현식을
사용하여
문제를
해결한다.

record = ('Haeri', 'gow1231@naver.com', '010-2609-8364', '055-687-8364')
name, email, *phone_numbers = record

print(name)
print(email)
print(phone_numbers)

Haeri
gow1231 @ naver.com
['010-2609-8364', '055-687-8364']

records = [
    ('foo', 1, 2),
    ('bar', 'hello'),
    ('foo', 3, 4)
]


def do_foo(x, y):
    print('foo', x, y)


def do_bar(s):
    print('bar', s)


for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)

foo
1
2
bar
hello
foo
3
4

언패킹
이후에
특정
값을
버리고
싶다면?
_
이나
ign(ignored)
를
사용한다.

record = ('ACME', 50, 123.45, (12, 18, 2016))
name, *_, (*_, year) = record
print(name)
print(year)

ACME
2016

별표(*)
를
사용한
언패킹과
리스트
프로세싱
사이에
여러
유사점이
존재한다.
예를
들어, 리스트에서
다음
예와
같이
쉽게
머리와
꼬리
부분으로
분리할
수
있다.

items = [1, 4, 24, 6, 67, 45]
head, *tail = items
print(head)
print(tail)

1
[4, 24, 6, 67, 45]

다음처럼
재귀
알고리즘을
사용하는
함수를
작성할
수도
있다.
하지만
파이썬에
재귀적
제약이
존재하므로
이
함수는
실질적으로
사용하기에는
무리가
있다.


def sum(items):
    head, *tail = items
    return head + sum(tail) if tail else head


print(sum(items))  # 결과 : 21

1.3.마지막
n개
아이템
유지

순환이나
프로세싱
중
마지막으로
발견한
n개의
아이템을
유지하고
싶다.

from collections import deque


def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)

    for line in lines:

        if pattern in line:
            yield line, previous_lines

        previous_lines.append(line)


# Example use on a file

if __name__ == '__main__':

    with open('somefile.txt') as f:

        for line, prevlines in search(f, 'python', 5):

            for pline in prevlines:
                print(pline, end='')

            print(line, end='')

            print('-' * 20)

** deque(maxlen=N)
으로
고정
크기
큐를
생성한다.
큐가
꽉
찬
상태에서
새로운
아이템을
넣으면
가장
마지막
아이템이
자동으로
삭제된다.

from collections import deque

q = deque(maxlen=3)
q.append(1)
q.append(2)
q.append(3)

print(q)
# deque([1, 2, 3], maxlen=3)

q.append(4)
print(q)
# deque([2, 3, 4], maxlen=3)

q.append(5)
print(q)
# deque([3, 4, 5], maxlen=3)

** 최대
크기를
지정하지
않으면
제약
없이
양쪽에
아이템을
넣거나
빼는
작업을
할
수
있다.
from collections import deque

q = deque()
q.append(1)
q.append(2)
q.append(3)

print(q)
# deque([1, 2, 3])

q.appendleft(4)
print(q)
# deque([4, 1, 2, 3])

print(q.pop())
# 3

print(q)
# deque([4, 1, 2])

print(q.popleft())
# 4

1.4.n
아이템의
최대
또는
최소값
찾기

컬렉션
내부에서
가장
크거나
작은
n개의
아이템을
찾아야
할
때
-> heaqp
모듈의
nlargest()
와
nsmallest()
함수를
사용한다.
import heapq

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums))  # [42, 37, 23]
print(heapq.nsmallest(3, nums))  # [-4, 1, 2]
nlargest()
와
nsmallest()
함수는
찾고자
하는
아이템의
개수가
상대적으로
작을
때
쓰도록
하자.
만약
최소값이나
최대값을
구하려
한다면(n=1)
min() or max()
를
사용하는
것이
더
빠르다.
n의
크기가
컬렉션
크기와
비슷해지면
우선
컬렉션을
정렬해놓는
것이
더
빠르다.
-> sorted(items)[:N]
이나
sorted(items)[-:N]
을
사용한다.nlargest()
와
nsmallest()
의
실제
구현이
이러한
방식을
채용해서
성능향상을
추구한다는
점을
기억하자.

nlargest()
와
nsmallest()
함수는
좀
더
복잡한
구조에
사용하기
쉽도록
키
파라미터를
받는다.
import heapq

portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]

cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])

print(cheap)
print(expensive)

[{'price': 16.350000000000001, 'name': 'YHOO', 'shares': 45}, {'price': 21.09, 'name': 'FB', 'shares': 200},
 {'price': 31.75, 'name': 'HPQ', 'shares': 35}]
[{'price': 543.22000000000003, 'name': 'AAPL', 'shares': 50},
 {'price': 115.65000000000001, 'name': 'ACME', 'shares': 75},
 {'price': 91.099999999999994, 'name': 'IBM', 'shares': 100}]

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
import heapq

heap = list(nums)
heapq.heapify(nums)

print(heap)

-> 책과
다른
결과…

[1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
이
출력됨.

heap[0]
이
가장
작은
아이템이
되어야
하는데.

1.5.우선
순위
큐
구현

“주어진
우선
순위에
따라
아이템을
정렬하는
큐를
구현하고
항상
우선
순위가
가장
높은
아이템을
먼저
팝하도록
만들어야
한다.
"

- 다음에
나온
코드애서
heaps
모듈을
사용해
간단한
우선
순위
큐를
구현한다.
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


# Example use
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

print("Should be bar:", q.pop())
print("Should be spam:", q.pop())
print("Should be foo:", q.pop())
print("Should be grok:", q.pop())

< 결과 >
Should
be
bar: Item('bar')
Should
be
spam: Item(‘spam
')
Should
be
foo: Item('foo')
Should
be
grok: Item('grok')

pop()
은
우선순위가
높은
순으로
아이템을
반환한다.
    두
아이템의
우선순위가
같은
경우(foo, grok)
는
큐에
삽입된
순서대로
반환된다.

< heapq
모듈의
사용법 >

heapq.heappush()
와
heapq.heappop()
은
list_queue
의
첫
번째
아이템이
가장
작은
우선
순위를
가진
것처럼
아이템을
삽입하거나
제거한다.(레시피
1.4)
heappop()
메소드는
항상
가장
작은
아이템을
반환해서
큐의
팝이
올바른
아이템에
적용될
수
있도록
한다.

    위의
예제에서는
큐가
튜플
형태로
구성되었다.(-priority, index, item).priority
값은
큐
내부
아이템을
가장
높은
우선
순위에서
낮은
우선
순위로
정렬하기
위해
무효화된다.이는
가장
낮은
값에서
높은
값으로
정렬되는
일반적인
힙과는
반대다.
    index
변수는
우선
순위가
동일한
아이템의
순서를
정할
때
사용한다.일정하게
증가하는
인덱스
값을
유지하기
때문에
힙에
아이템이
삽입된
순서대로
정렬할
수
있다.

    이를
살펴보기
위해
순서를
매길
수
없는
다음
item
인스턴스를
살펴보자.

a = Item('foo')
b = Item('bar')
a < b

TypeError: '<'
not supported
between
instances
of
'Item' and 'Item'

(priority, item)
튜플을
만들었다면
우선
순위
값이
달라야만
비교가
가능하다.하지만
동일한
우선
순위를
가진
두
아이템의
비교는
할
수
없다.

a = (1, Item('foo'))
b = (5, Item('bar'))
a < b
# True

c = (1, Item('grok'))
a < c
# '<' not supported between instances of 'Item' and 'Item'

여기
인덱스
값을
추가해서
튜플을
만들면(priority, index, item), 어떠한
튜플도
동일한
인덱스
값을
가질
수
없으므로
위의
문제를
원천적으로
해결할
수
있다.

a = (1, 0, Item('foo'))
b = (5, 1, Item('bar'))
c = (1, 2, Item('grok'))
a < b
# True
a < c
# True


1.6.딕셔너리의
키를
여러
값에
매핑하기

딕셔너리의
키를
하나
이상의
값에
매핑하고
싶다.(소위 “multidict”라
불린다.)

-> 하나의
키에
하나의
값이
매핑되어
있는
것을
딕셔너리라
부른다.키에
여러
값을
매핑하기
위해서는
여러개의
값을
리스트나
세트와
같은
컨테이너에
따로
저장해
두어야
한다.

    예제
d = {
    'a': [1, 2, 3],
    'b': [4, 5]
}

e = {
    'a': {1, 2, 3},
    'b': {4, 5}
}

리스트나
세트
사용
여부는
사용
목적에
따라
달라진다.아이템의
삽입
순서를
지켜야
한다면
리스트를
사용하는
것이
좋고, 순서가
상관
없고
중복을
없애려면
세트를
사용해야
한다.
    이러한
딕셔너리를
쉽게
만들기
위해서
collections
모듈의
defaultdict를
사용한다.defaultdict의
기능
중에는
첫
번째
값을
자동으로
초기화하는
것이
있어서
사용자는
아이템
추가에만
집중할
수
있다.

from collections import defaultdict

d = defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)

# print(d)
# defaultdict(<class 'list'>, {'a': [1, 2], 'b': [4]})

d = defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['b'].add(4)

# print(d)
# defaultdict(<class 'set'>, {'a': {1, 2}, 'b': {4}})

다만
defaultdict
를
사용할
때는
딕셔너리에
존재하지
않는
값이라도
한
번이라도
접근했던
키의
엔트리를
자동으로
생성한다는
점을
주의해야
한다.이런
동작성이
마음에
들지
않는다면
일반
딕셔너리의
set
default()
를
사용한다.

d = {}  # 일반 딕셔너리
d.setdefault('a', []).append(1)
d.setdefault('a', []).append(2)
d.setdefault('b', []).append(4)

print(d)
# {'a': [1, 2], 'b': [4]}

하지만
많은
프로그래머들은
setdefault()
가
자연스럽지
않다고
생각한다.첫
번째
값에
대해서
항상
새로운
인스턴스를
생성한다는
점이
특히
치명적인가
봄.(-> 위
예제에서도
빈
리스트[]
를
만들었다.)

이론적으로
여러
값을
가지는
딕셔너리를
만드는
것이
복잡하지는
않다.하지만
첫
번째
값에
대한
초기화를
스스로
하려면
꽤나
복잡한
과정을
거쳐야
한다.예를
들어
아래와
같은
코드를
작성해야
한다.

d = {}
for key, value in pairs:
    if
key not in d:
d[key] = []
d[key].append(value)

defaultdict
를
사용하면
좀
더
깔끔한
코드가
된다.

d = defaultdict(list)
for key, value in pairs:
    d[key].append(value)

1.7.딕셔너리
순서
유지

딕셔너리를
만들고, 순환이나
직렬화할
때
순서를
조절하고
싶다.

-> 딕셔너리
내부
아이템의
순서를
조절하려면
collections
모듈의
OrderedDict
를
사용한다.
    이
모듈을
사용하면
삽입
초기의
순서를
그대로
기억한다.

from collections import OrderedDict

d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4

for key in d:
    print(key, d[key])

# foo 1
# bar 2
# spam 3
# grok 4


OrderedDict는
나중에
직렬화하거나
다른
포맷으로
인코딩할
다른
매핑을
만들
때
특히
유용한다.예를
들어, JSON
인코딩에
나타나는
특정
필드의
순서를
조절하기
위해
OrderedDict에
다음과
같이
데이터를
생성한다.

import json

json.dumps(d)
# '{"foo": 1, "bar": 2, "spam": 3, "grok": 4}'

OrderedDict는
내부적으로
더블
링크드
리스트(double
linked
list)로
삽입
순서와
관련
있는
키를
기억한다.새로운
아이템을
처음으로
삽입하면
리스트의
제일
끝에
위치시킨다.기존
키에
재할당을
한다
해도
순서에는
변화가
생기지
않는다.
    더블
링크드
리스트를
사용하기
때문에
OrderedDict의
크기는
일반적인
딕셔너리에
비해
2
배
크다.따라서
OrderedDict로
크기가
매우
큰
데이터
구조체를
만든다면, OrderedDict를
사용하는
데서
오는
추가적인
메모리
소비가
애플리케이션에
실질적으로
유용한
것인지
고려해야
한다.

1.8.딕셔너리
계산

딕셔너리
데이터에
여러
계산을
수행하고
싶다.(최소값, 최대값, 정렬
등)

- 딕셔너리에
주식
이름과
가격이
들어있다고
가정해
보자.
prices = {
             'ACME': 45.23,
             'AAPL': 612.78,
             'IBM': 205.55,
             'HPQ': 37.20,
             'FB': 10.75
         }

         - 딕셔너리
내용에
대해
유용한
계산을
하려면
딕셔너리의
키와
값을
zip()
으로
뒤집어
주는
것이
좋다.
    아래의
최소
주가와
최대
주가를
찾는
코드를
살펴보자.

min_price = min(zip(prices.values(), prices.keys()))
# (10.75, ‘FB')
max_price = max(zip(prices.values(), prices.keys()))
# (612.77999999999997, 'AAPL')

이와
유사하게
데이터의
순서를
매기려면
zip()
과
sorted()
를
함께
사용한다.

prices_sorted = sorted(zip(prices.values(), prices.keys()))

# [(10.75, 'FB'), (37.2, 'HPQ'), (45.23, 'ACME'), (205.55, 'IBM'), (612.78, 'AAPL')]

계산을
할
때, zip()
은
단
한번만
소비할
수
있는
이터레이터(iterator)
를
생성한다.
    예를
들어, 아래와
같은
코드에서는
에러가
난다.
prices_and_names = zip(prices.values(), prices.keys())

print(min(prices_and_names))
# (10.75, 'FB')

print(max(prices_and_names))
# ValueError: max() arg is an empty sequence


딕셔너리에서
일반적인
데이터
축소를
시도하면, 키에
대해서만
작업이
이뤄진다.

    print(min(prices))  # AAPL
print(max(prices))  # IBM

딕셔너리의
값에
대한
계산을
하기
위해서는
딕셔너리의
values()
메소드를
사용한다.

    print(min(prices.values()))  # 10.75
print(max(prices.values()))  # 612.78

키에
일치하는
값
정보까지
알고
싶다면
어떻게
해야
할까(예를
들어, 어떤
주식의
값이
가장
낮은지
알고
싶다면)?
최소, 최대값에
일치하는
키를
찾으려면
min과
max에
키
함수를
제공한다.

    print(min(prices, key=lambda k: prices[k]))  # FB
print(max(prices, key=lambda k: prices[k]))  # AAPL

하지만
최소값을
얻기
위해서는
아래와
같이
코드를
작성해야
한다.

min_value = prices[min(prices, key=lambda k: prices[k])]
print(min_value)  # 10.75

zip()
을
포함한
해결책은
딕셔너리의
시퀀스를(value, key)
페어로
뒤집는
것으로
문제를
해결한다.이런
튜플에
비교를
수행하면
값(value)
요소를
먼저
비교하고
뒤이어
키(key)
를
비교한다.이렇게
하면
명령어
하나만으로
정확히
우리가
원하는
데이터
축소와
정렬을
수행한다.
    여러
엔트리가
동일한
값을
가지고
있을
때
비교
결과를
결정하기
위해
키를
사용한다는
점을
주목하자.예를
들어, min()
과
max()
를
계산할
때
중복된
값이
있으면
가장
작거나
큰
키를
가지고
있는
엔트리를
반환한다.

prices = {'AAA': 45.23, 'ZZZ': 45.23}

min(zip(prices.values(), prices.keys()))
# (45.23, 'AAA')
max(zip(prices.values(), prices.keys()))
# (45.23, 'ZZZ')



1.9.두
딕셔너리의
유사점
찾기

두
딕셔너리가
있고
여기서
유사점을
찾고
싶다.(동일한
키, 동일한
값
등)

다음
두
딕셔너리를
보자.

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

두
딕셔너리의
유사점을
찾으려면
keys()
와
items()
메소드에
집합
연산을
수행한다.

    # 동일한 키 찾기
    a.keys() & b.keys()  # {'x', 'y'}

# a에만 있고 b에는 없는 키 찾기
a.keys() - b.keys()  # {'z'}

# (키, 값)이 동일한 것 찾기
a.items() & b.items()  # {('y', 2)}

이런
연산을
사용해서
딕셔너리의
내용을
수정하거나
걸러
낼
수도
있다.예를
들어, 선택한
키를
삭제한
새로운
딕셔너리를
만들고
싶을
때는
다음과
같은
딕셔너리
생성
코드를
사용한다.

# 특정 키를 제거한 새로운 딕셔너리 만들기
c = {key: a[key] for key in a.keys() - {'z', 'w'}}
print(c)  # {'x': 1, 'y': 2}

딕셔너리는
키와
값의
매핑으로
이루어진다.딕셔너리의
keys()
메소드는
키를
노출하는
키 - 뷰(key - view)
객체를
반환한다.키 - 뷰에는
합집합, 교집합, 여집합과
같은
집합
연산
기능이
있다.따라서
딕셔너리
키에
집합
연산을
수행하기
위해서
집합으로
변환할
필요없이
키 - 뷰
객체를
바로
사용하면
된다.
    딕셔너리의
items()
메소드는(key, value)
페어로
구성된
아이템 - 뷰(item - view)
객체를
반환한다.이
객체는
집합
연산과
유사한
것을
지원하므로
두
딕셔너리에
동일한
키 - 값
페어를
찾을
때
사용할
수
있다.
    유사하긴
하지만
values()
메소드는
앞에
나온
집합
연산을
지원하지
않는다.이는
키와는
다르게
값 - 뷰는
유일하다는
보장이
없기
때문이다.이
사실만으로도
특정
집합
연산을
사용할
수
없다.반드시
이러한
비교를
해야
한다면
먼저
값을
집합으로
변환해야
한다.

1.10.순서를
깨지
않고
시퀀스의
중복
없애기

시퀀스에서
중복된
값을
없애고
싶지만, 아이템의
순서는
유지하고
싶다.

-> 시퀀스의
값이
해시(hash)
가능하다면
이
문제는
세트와
제너레이터(generator)
를
사용해서
쉽게
해결할
수
있다.


def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)


a = [1, 5, 2, 1, 9, 1, 5, 10]

list(dedupe(a))
# [1, 5, 2, 9, 10]

앞에서도
말했지만
시퀀스의
아이템이
해시
가능한
경우에만
사용할
수
있다.
해시
불가능한
타입(예를
들어
dict)의
중복을
없애려면
레시피에
약간의
수정이
필요하다.


def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


a = [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}]

list(dedupe(a, key=lambda d: (d['x'], d['y'])))
# [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]  -> (x, y) 값이 중복되지 않게

list(dedupe(a, key=lambda d: d['x']))
# [{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]   -> x 값이 중복되지 않게

key
인자의
목적은
중복
검사를
위해
함수가
시퀀스
아이템을
해시
가능한
타입으로
변환한다고
명시하는
데
있다.(위의
코드)

아래의
해결책은
필드가
하나이거나
커다란
자료
구조에
기반한
값의
중복을
없앨
때도
잘
동작한다.

중복을
없애려면
대개
세트를
만드는
것이
가장
쉽다.

a
#  [1, 5, 2, 1, 9, 1, 5, 10]
set(a)
#  {1, 2, 5, 9, 10}

하지만
위
방식을
사용하면
기존
데이터의
순서가
훼손된다.하지만
앞서
설명한
방식으로
이
문제를
해결할
수
있다.
제너레이터
함수를
사용하면
단순히
리스트
프로세싱
말고도
아주
일반적인
목적의
함수를
사용할
수
있다.예를
들어
파일을
읽어들일
때
중복된
라인을
모시하려면
단순히
아래와
같은
코드를
사용한다.

with open(somefile, 'r') as f:
    for line in dedupe(f):
        …

        key함수의
        스펙은
        파이썬
        내장함수인
        sorted(), min(), max()
        등의
        기능을
        흉내
        내고
        있다.자세한
        내용은
        레시피
        1.8, 1.13
        을
        참고한다.

        1.11.슬라이스
        이름
        붙이기

        프로그램
        코드에
        슬라이스(slice)
        를
        지시하는
        하드코딩이
        너무
        많아
        이해하기
        어려운
        상황이다.이를
        정리해야
        한다.

        - 고정된
        문자열로부터
        특정
        데이터를
        추출하는
        코드가
        있다고
        가정해
        보자.

        ###### 012345678901234567890123456789012345678901234567890123456789'
        record = '....................100         ........513.25  ...............'
        cost = int(record[20:32]) * float(record[40:48])

        print(cost)  # 51325.0

        위의
        방법대신
        다음과
        같이
        이름을
        붙이는
        것은
        어떨까?

        SHARES = slice(20, 32)
        PRICE = slice(40, 48)

        cost = int(record[SHARES] * float(record[PRICE]))

        두번째
        방법으로
        하면
        의미
        없는
        하드
        코딩에
        이름을
        붙여서
        이후에
        이해하기가
        훨씬
        수월하다.

        일반적으로
        프로그램을
        작성할
        때
        하드코딩이
        늘어날수록
        이해하기
        어렵고
        지저분해진다.예를
        들어, 1
        년
        후에
        이
        코드를
        다시
        읽는다면
        도대체
        그땐
        무슨
        생각으로
        코드를
        작성했는지
        이해가
        안된다.여기서
        보여준
        해결책을
        따르면
        코드가
        무슨
        일을
        하고
        있는지
        좀
        더
        명백해질
        것이다.

        일반적으로
        내장함수인
        slice()
        는
        슬라이스
        받는
        모든
        곳에
        사용할
        수
        있는
        조각을
        생성한다.

        items = [0, 1, 2, 3, 4, 5, 6]
        a = slice(2, 4)
        items[2:4]
        # [2, 3]

        items[a]
        # [2, 3]

        items[a] = [10, 11]
        items
        # [0, 1, 10, 11, 4, 5, 6]

        del items[a]
        items
        # [0, 1, 4, 5, 6]

        ** slice
        인스턴스
        s가
        있다면
        s.start와
        s.stop, s.step
        속성을
        통해
        좀
        더
        많은
        정보를
        얻을
        수
        있다.

        a = slice(10, 50, 2)
        a.start
        # 10
        a.stop
        # 50
        a.step
        # 2

        추가적으로
        indices(size)
        메소드를
        사용하면
        특정
        크기의
        시퀀스에
        슬라이스를
        매핑할
        수
        있다.이렇게
        하면
        튜플(start, stop, step)
        을
        반환하는데, 모든
        값은
        경계를
        넘어서지
        않도록
        제약이
        걸려
        있다.(인덱스에
        접근할
        때
        IndexError예외가
        발생하지
        않도록
        하기
        위함).

        s = 'HelloWorld'
        a.indices(len(s))
        # (10, 10, 2) ????뭐지??? 책에서는 (5, 10, 2)

        for i in range(*a.indices(len(s))):
            print(s[i])
        ->??????????????


        1.12.시퀀스에
        가장
        많은
        아이템
        찾기

        시퀀스에
        가장
        많이
        나타난
        아이템을
        찾고
        싶다면?

        - 이러한
        문제를
        해결하기
        위해
        존재하는
        클래스가
        바로
        collections.Counter
        이다.
        most_common()
        메소드는
        이러한
        상황에
        특히
        알맞음

    예를
    들어, 단어가
    여러
    개
    들어있는
    리스트에서
    가장
    많은
    단어를
    찾아보자.

    words = ['look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes', 'the', 'eyes', 'the', 'eyes', 'the', 'eyes',
             'not', 'around', 'the', 'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into', 'my', 'eyes',
             "you're", 'under']
    from collections import Counterword_counts = Counter(words)
    top_three = word_counts.most_common(3)
    print(top_three)  # outputs [('eyes', 8), ('the', 5), ('look', 4)]

    Counter
    객체에서는
    해시
    가능한
    모든
    아이템을
    입력할
    수
    있다.내부적으로
    Counter는
    아이템이
    등장하는
    횟수를
    가리키는
    딕셔너리이다.

    word_counts['not']  # 1
    word_counts['eyes']  # 8

    카운트를
    수동으로
    증가시키고
    싶다면
    심플하게
    더하기를
    사용한다.

    morewords = ['why', 'are', 'you', 'not', 'looking', 'in', 'my', 'eyes']
    for word in morewords:
        word_counts[word] += 1
    # [('eyes', 8), ('the', 5), ('look', 4)]

    word_counts['eyes']
    # 9

    ** 혹은
    update()
    메소드를
    사용할
    수도
    있다.

    word_counts.update(morewords)
    # [('eyes', 8), ('the', 5), ('look', 4)]

    Counter
    인스턴스는
    여러
    가지
    수식을
    사용할
    수
    있는
    기능이
    있다.

    a = Counter(words)
    b = Counter(morewords)

    a
    Counter({'around': 2,
             "don't": 1,
             'eyes': 8,
             'into': 3,
             'look': 4,
             'my': 3,
             'not': 1,
             'the': 5,
             'under': 1,
             "you're": 1})

    b
    Counter({'are': 1,
             'eyes': 1,
             'in': 1,
             'looking': 1,
             'my': 1,
             'not': 1,
             'why': 1,
             'you': 1})

    # 카운트 합치기
    c = a + b

    Counter({'are': 1,
             'around': 2,
             "don't": 1,
             'eyes': 9,
             'in': 1,
             'into': 3,
             'look': 4,
             'looking': 1,
             'my': 4,
             'not': 2,
             'the': 5,
             'under': 1,
             'why': 1,
             'you': 1,
             "you're": 1})

    # 카운트 빼기
    d = a - b
    Counter({'around': 2,
             "don't": 1,
             'eyes': 7,
             'into': 3,
             'look': 4,
             'my': 2,
             'the': 5,
             'under': 1,
             "you're": 1})

    데이터의
    개수를
    파악해야
    하는
    문제에서
    Counter
    객체는
    매우
    유용하다.딕셔너리를
    직접
    사용해서
    아이템의
    개수를
    세는
    방식보다는
    Counter를
    사용하는
    것이
    더
    권장된다.

    1.13.일반
    키로
    딕셔너리
    리스트
    정렬

    딕셔너리
    리스트가
    있고, 하나
    혹은
    그
    이상의
    딕셔너리
    값으로
    이를
    정렬하고
    싶다면?

    - 이와
    같은
    구조는
    operator
    모듈의
    itemgetter
    함수를
    사용하면
    쉽게
    정렬할
    수
    있다.어느
    웹
    사이트
    회원
    리스트를
    데이터베이스로부터
    불러와
    다음과
    같은
    자료
    구조를
    만들었다고
    가정해보자.

    rows = [
        {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
        {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
        {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
        {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
    ]

    모든
    딕셔너리에
    포함된
    필드를
    기준으로
    데이터를
    정렬해
    출력하는
    것은
    어렵지
    않다.

    from operator import itemgetter

    rows_by_fname = sorted(rows, key=itemgetter('fname'))
    rows_by_uid = sorted(rows, key=itemgetter('uid'))

    print(rows_by_fname)

    [{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
     {'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}]

    print(rows_by_uid)

    [{'fname': 'John', 'lname': 'Cleese', 'uid': 1001}, {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
     {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}]

    itemgetter()
    함수에는
    키를
    여러
    개
    전달할
    수도
    있다.예를
    들어

    rows_by_lfname = sorted(rows, key=itemgetter('lname', 'fname'))
    print(rows_by_lfname)

    [{'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
     {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}]

    이번
    예제에서
    키워드
    인자
    key를
    받는
    내장
    함수
    sorted()
    에
    rows를
    전달했다.이
    인자는
    rows로부터
    단일
    아이템을
    받는
    호출
    가능
    객체를
    입력으로
    받고
    정렬의
    기본이
    되는
    값을
    반환한다.itemgetter()
    함수는
    그런
    호출
    가능
    객체를
    생성한다.
    operator.itemgetter()
    함수는
    rows
    레코드에서
    원하는
    값을
    추출하는
    데
    사용하는
    인덱스를
    인자로
    받는다.딕셔너리
    키
    이름이나
    숫자
    리스트
    요소나, 객체의
    __getitem__()
    메소드에
    넣을
    수
    있는
    모든
    값이
    가능하다.

    itemgetter()
    에
    여러
    인덱스를
    전달하면, 생성한
    호출
    가능
    객체가
    모든
    요소를
    가지고
    있는
    튜플을
    반환하고, sorted가
    튜플의
    정렬
    순서에
    따라
    결과의
    순서를
    잡는다.이
    방식은
    여러
    필드를
    동시에
    정렬할
    때
    유용하다.(예제처럼
    이름과
    성)

    ** itemgetter()
    의
    기능은
    때때로
    lambda 표현식으로 대체할
    수
    있다.

    rows_by_fname = sorted(rows, key=lambda r: ['fname'])
    rows_by_lfname = sorted(rows, key=lambda r: (['lname'], r['fname']))

    위
    코드도
    잘
    동작하지만, itemgetter()
    를
    사용한
    코드의
    실행
    속도가
    좀
    더
    빠르다.프로그램
    성능이
    신경쓰인다면
    처음부터
    더
    나은
    방식을
    사용한다.

    마지막으로, 이
    레시피에
    나온
    내용은
    min()
    과
    max()
    와
    같은
    함수에도
    사용할
    수
    있음을
    알아두자.

    min(rows, key=itemgetter('uid'))
    # {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}

    max(rows, key=itemgetter('uid'))
    # {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}


    1.14.기본
    비교
    기능
    없이
    객체
    정렬

    동일한
    클래스
    객체를
    정렬해야
    하는데, 이
    클래스는
    기본적인
    비교
    연산을
    제공하지
    않는다.

    - 내장
    함수
    sorted()
    는
    key
    인자에
    호출
    가능
    객체를
    받아
    sorted가
    객체
    비교에
    사용할
    수
    있는
    값을
    반환한다.예를
    들어, 앱에
    User
    인스턴스를
    시퀀스로
    갖고
    있고
    이를
    user_id
    요소를
    기반으로
    정렬하고
    싶다.이럴
    때는
    User
    인스턴스를
    입력으로
    받고
    user_id를
    반환하는
    코드를
    작성할
    수
    있다.


    class User:
        def __init__(self, user_id):
            self.user_id = user_id

        def __repr__(self):
            return 'User({})'.format(self.user_id)


    users = [User(23), User(3), User(99)]
    print(users)
    # [User(23), User(3), User(99)]

    sorted(users, key=lambda u: u.user_id)
    # [User(3), User(23), User(99)]

    ** lambda 를 사용하는
    대신, operator.attrgetter()
    를
    사용해도
    된다.
    from operator import attrgetter

    print(sorted(users, key=attrgetter('user_id’)))

    -> [User(3), User(23), User(99)]

    lambda 를 사용할지
    attrgetter()
    를
    사용할지의
    여부는
    개인의
    선호에
    따라
    갈린다.하지만
    attrgetter()
    의
    속도가
    빠른
    경우가
    종종
    있고
    동시에
    여러
    필드를
    추출하는
    기능이
    추가되어
    있다.
        예를
    들어, User
    인스턴스에
    first_name과
    last_name
    속성이
    있다면
    다음과
    같이
    정렬할
    수
    있다.

    by_name = sorted(users, key=attrgetter('last_name', 'first_name'))

    또한
    이번
    레시피에서
    사용한
    기술을
    min(), max()
    와
    같은
    함수에
    사용할
    수
    있다는
    점도
    중요하다.

        min(users, key=attrgetter('user_id'))  # User(3)
    max(users, key=attrgetter('user_id'))  # User(99)


    1.15.필드에
    따라
    레코드
    묶기

    일련의
    딕셔너리나
    인스턴스가
    있고
    특정
    필드
    값에
    기반한
    그룹의
    데이터를
    순환하고
    싶다.

    - itertools.groupby()
    함수는
    이왁
    같은
    데이터를
    묶는
    데
    유용하다.다음과
    같은
    딕셔너리
    리스트가
    있다고
    가정해보자.

    rows = [
        {'address': '5412 N CLARK', 'date': '07/01/2012'},
        {'address': '5148 N CLARK', 'date': '07/04/2012'},
        {'address': '5800 E 58TH', 'date': '07/02/2012'},
        {'address': '2122 N CLARK', 'date': '07/03/2012'},
        {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
        {'address': '1060 W ADDISON', 'date': '07/02/2012'},
        {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
        {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
    ]

    이제
    날짜로
    구분
    지을
    데이터
    조각을
    순환해야
    한다.우성
    원하는
    필드에
    따라
    정렬해야
    하고(이
    경우에는
    date
    필드), 그
    후에
    itertools.groupby()
    를
    사용한다.

    from operator import itemgetter
    from itertools import groupby

    # 우선 원하는 필드로 정렬한다.
    rows.sort(key=lambda r: r['date'])
    # 그룹 내부에서 순환한다.
    for date, items in groupby(rows, key=lambda r: r['date']):
        print(date)
    for i in items:
        print('    ', i)

    다음과
    같은
    결과가
    출력된다.

    07 / 01 / 2012
    {'address': '5412 N CLARK', 'date': '07/01/2012'}
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'}
    07 / 02 / 2012
    {'address': '5800 E 58TH', 'date': '07/02/2012'}
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'}
    {'address': '1060 W ADDISON', 'date': '07/02/2012'}
    07 / 03 / 2012
    {'address': '2122 N CLARK', 'date': '07/03/2012'}
    07 / 04 / 2012
    {'address': '5148 N CLARK', 'date': '07/04/2012'}
    {'address': '1039 W GRANVILLE', 'date': '07/04/2012'}

    groupby()
    함수는
    시퀀스를
    검색하고
    동일한
    값(혹은
    키
    함수에서
    반환한
    값) 에
    대한
    일련의 “실행”을
    찾는다.개별
    순환에
    대해서
    값, 그리고
    같은
    값을
    가진
    그룹의
    모든
    아이템을
    만드는
    이터레이터(iterator)
    를
    함께
    반환한다.
        그에
    앞서
    원하는
    필드에
    따라
    데이터를
    정렬하는
    과정이
    중요하다.groupby()
    함수는
    연속된
    아이템에서만
    동작하기
    때문에
    정렬
    과정을
    생략하면
    원하는
    대로
    함수를
    실행할
    수
    없다.
        단순히
    날짜에
    따라
    데이터를
    묶어서
    커다란
    자료
    구조에
    넣어
    놓고
    원할
    때마다
    접근하려는
    것이라면, 레시피
    1.6
    에
    나온대로
    defaultdict()
    를
    사용해서
    multidict를
    구성하는
    게
    더
    나을
    수도
    있다.

    from collections import defaultdict

    rows_by_date = defaultdict(list)
    for row in rows:
        rows_by_date[row['date']].append(row)

    for r in rows_by_date['07/01/2012']:
        print(r)

    {'address': '5412 N CLARK', 'date': '07/01/2012'}
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'}

    이
    방법을
    사용하면
    정렬
    과정을
    생략해도
    된다.그러므로
    메모리
    사용량에
    크게
    구애받지
    않는다면
    이
    방식을
    사용하는
    것이
    정렬한
    후에
    groupby()
    를
    사용하는
    첫
    번째
    방법보다
    더
    빠를
    것이다.

    1.16.시퀀스
    필터링

    시퀀스
    내부에
    데이터가
    있고, 특정
    조건에
    따라
    값을
    추출하거나
    줄이고
    싶다면?

    - 가장
    간단한
    해결책은
    리스트
    컴프리헨션(list
    comprehension)이다

    mylist = [1, 4, -5, 10, -7, 2, 3, -1]

    [n
    for n in mylist if n > 0]
    # [1, 4, 10, 2, 3]
    [n for n in mylist if n < 0]
    # [-5, -7, -1]

    이 방식은 입력된 내용이 크면 매우 큰 결과가 생성될 수도 있다는 단점이 있다.
    이 부분이 걱정이라면 생성자 표현식을 사용해서 값을 걸러 낼 수 있다.

    mylist =[1, 4, -5, 10, -7, 2, 3, -1]

    pos = (n for n in mylist if n > 0)
    pos
    # <generator object <genexpr> at 0x1152b67d8>

    for x in pos:
        print(x)

    1
    4
    10
    2
    3

    리스트
    컴프리헨션이나
    생성자
    표현식에
    필터
    조건을
    만드는
    것이
    쉽지
    않을
    때도
    있다.예를
    들어, 필터링
    도중에
    예외
    처리를
    해야
    한다거나
    다른
    복잡한
    내용이
    들어가야
    한다면
    어떻게
    해야
    할까? 이때는
    필터링
    코드를
    함수
    안에
    넣고
    filter()
    를
    사용하면
    된다. \
    values = ['1', '2', '-3', '-', '4', 'N/A', '5']


    def is_int(val):
        try:
            x = int(val)
            return True
        except ValueError:
            return False


    ivals = list(filter(is_int, values))
    print(ivals)
    # ['1', '2', '-3', '4', '5'] 가 출력된다


    filter()
    는
    이터레이터(iterator)
    를
    생성한다.따라서
    결과의
    리스트를
    만들고
    싶다면
    위에서
    나온대로
    list()
    도
    함께
    사용해야
    한다.

    리스트
    컴프리헨션과
    생성자
    표현식은
    간단한
    데이터를
    걸러
    내기
    위한
    가장
    쉽고
    직관적인
    방법이다.또한
    동시에
    데이터
    변형
    기능도
    갖고
    있다.

    >> > mylist = [1, 4, -5, 10, -7, 2, 3, -1]
    >> > import math
    >> > [math.sqrt(n) for n in mylist if n > 0]
    # [1.0, 2.0, 3.1622776601683795, 1.4142135623730951, 1.7320508075688772]

    필터링에는
    조건을
    만족하지
    않는
    값ㅇ르
    걸러내는
    것
    외에도
    새로운
    값으로
    치환하는
    방식도
    있다.예를
    들어, 잘못된
    값을
    특정
    범위에
    들어가도록
    수정할
    수
    있다.필터링
    조건을
    조건
    표현식으로
    바꿔주면
    간단히
    구현
    가능하다.

    >> > clip_neg = [n if n > 0 else 0 for n in mylist]
    >> > clip_neg
    # [1, 4, 0, 10, 0, 2, 3, 0]

    clip_pos = [n if n < 0 else 0 for n in mylist]
    clip_pos
    # [0, 0, -5, 0, -7, 0, 0, -1]

    또
    다른
    주목할
    만한
    필터링
    도구로
    순환
    가능한
    것과
    boolean
    셀렉터
    시퀀스를
    입력으로
    받는
    itertools.compress()
    가
    있다.이
    함수는
    셀렉터에서
    조건이
    참인
    요소만
    골라서
    반환한다.어떤
    시퀀스의
    결과를
    다른
    시퀀스에
    반영하려고
    할
    때
    유용하게
    쓰인다.
    다음과
    같이
    두
    개의
    열이
    있는
    데이터를
    가정해
    보자.

    addresses = [
        '5412 N CLARK',
        '5148 N CLARK',
        '5800 E 58TH',
        '2122 N CLARK',
        '5645 N RAVENSWOOD',
        '1060 W ADDISON',
        '4801 N BROADWAY',
        '1039 W GRANVILLE',
    ]

    counts = [0, 3, 10, 4, 1, 7, 6, 1]

    ** 카운트
    값이
    5
    이상이
    주소만
    남기려
    한다면
    다음과
    같이
    하면
    된다.

    from itertools import compress

    more5 = [n > 5 for n in counts]
    more5
    # [False, False, True, False, False, True, True, False]

    a = list(compress(addresses, more5))
    print(a)
    # ['5800 E 58TH', '1060 W ADDISON', '4801 N BROADWAY']

    우선
    주어진
    조건에
    만족하는지
    여부를
    담은
    boolean
    시퀀스를
    만들어
    두는
    것이
    포인트다.그리고
    compress()
    함수로
    true에
    일치하는
    값만
    골라낸다.
    filter()
    와
    마찬가지로, compress()
    는
    일반적으로
    이터레이터를
    반환한다.따라서
    실행
    결과를
    리스트에
    담고
    싶다면
    list()
    를
    사용해야
    한다.

    1.17.딕셔너리의
    부분
    추출

    딕셔너리의
    특정
    부분으로부터
    다른
    딕셔너리를
    만들고
    싶다면?

    -> 딕셔너리
    컴프리헨션(dictionary
    comprehension)을
    사용하면
    간단하게
    해결할
    수
    있다.

    prices = {'ACME': 45.23, 'AAPL': 612.78, 'IBM': 205.55, 'HPQ': 37.20, 'FB': 10.75}

    prices = {
        'ACME': 45.23,
        'AAPL': 612.78,
        'IBM': 205.55,
        'HPQ': 37.20,
        'FB': 10.75
    }

    # 가격이 200 이상인 것에 대한 딕셔너리
    p1 = {key: value for key, value in prices.items() if value > 200}

    # 기술 관련 주식으로 딕셔너리 구성
    tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
    p2 = {key: value for key, value in prices.items() if key in tech_names}

    print(p1)
    # {'AAPL': 612.78, 'IBM': 205.55}

    print(p2)
    # {'AAPL': 612.78, 'IBM': 205.55, 'HPQ': 37.2}



    딕셔너리
    컴프리헨션으로
    할
    수
    있는
    대부분의
    일은
    튜플
    시퀀스를
    만들고
    dict()
    함수에
    전달하는
    것으로도
    할
    수
    있다.
    다음
    코드를
    참고하자.

    p1 = dict((key, value) for key, value in prices.items() if value > 200)

    하지만
    딕셔너리
    컴프리헨션을
    사용하는
    것이
    더
    깔끔하고
    실행
    속도도
    좀
    더
    빠르다.
    동일한
    문제를
    해결하는
    데는
    언제나
    많은
    방법이
    존재한다.예를
    들어
    두번째
    예제는
    다음과
    같이
    작성할
    수도
    있다.

    tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
    p2 = {key: prices[key] for key in prices.keys() & tech_names}

    하지만
    이
    방식은
    처음
    방식에
    비해
    실행속도가
    더
    느리다.

    1.18.시퀀스
    요소에
    이름
    매핑


