''''''
'''

3장 11절 임의의 요소 뽑기 : 시퀀스에서 임의의 아이템을 고르거나 난수를 생성하고 싶은 경우 random모듈의 여러 메소드를 사용한다.

- 아이템 선택 : random.choice(데이터)
- 랜덤 표본 추출 : random.sample(데이터, 뽑을갯수)
- 랜덤 셔플 : random.shuffle()
- 난수 생성 : random.randint(시작, 끝)
- 소수난수 생성 : random.random()
- N비트 랜덤 정수 : random.getrandbits()
- 균등 분포 숫자 : random.uniform()
- 정규 분포 숫자 : random.gauss()



* random.seed() 한수로 시드 값을 바꿀 수 있다.
  - random.seed()            :  시스템 시간 혹은 os.urandom() 시드 
  - random.seed912345)       :  주어진 정수형 시드
  - random.seed(b'bytedata') :  바이트 데이터 시드
  
'''


# 예1.
import random
values = [1, 2, 3, 4, 5, 6]
random.choice(values)
# 6

# 예2.
random.sample(values, 2)

# 예3.
random.shuffle(values)

# 예4.
random.randint(0, 10)

# 예5.
random.random()


'''

3장 12절 시간 단위 변환 : 날짜를 초로, 시간을 분으로 시간 변환을 해야되는 경우 datetime 모듈을 사용한다.

- 시간의 간격은 timedelta 인스턴스
- 특정 날짜와 시간은 datetime 인스턴스
- 복잡한 시간 계산은 dateutil 모듈을 사용

* 시간의 계산에서 datetime이 윤년을 인직하는 것에 주의



'''

# 예7.
from datetime import timedelta
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c = a + b
c.days
# 2
c.seconds
# 37800
c.seconds/3600
# 10.5

# 예10.
from datetime import datetime
a = datetime(2012, 9, 23)
print(a + timedelta(days=10))
# 2012-10-03 00:00:00
b = datetime(2012, 12, 21)
d = b - a
d.days
# 89
a - datetime(2012, 3, 1)
b = datetime(2012, 2, 28)
a - b
# datatime.timedelta(2)
(a-b).days
# 2
c = datetime(2013, 3, 1)

'''

3.15 문자열을 시간으로 변환 : 문자열 형식의 시간 데이터를 datetime 객체로 변환하고 싶은 경우 datetime 모듈을 사용한다.

- datetime 객체를 읽기 힘들기 때문에 읽기 쉬운 형태로 변환해주는 메소드 : strftime(데이터, '날짜형식')
    (strftime() 메소드는 실행속도가 느리기 때문에 날짜형식을 알고 있는 경우는 사용자함수를 직접 생성해서 사용한다.)
'''

# 예11.
from datetime import datetime
text = '2012-09-20'
y = datetime.strptime(text, '%Y-%m-%d')
z = datetime.now()
diff = z - y
diff
# datetime.timedelta(1709, 38086, 479134)
nice_z = datetime.strftime(z, '%A %B %d, %Y')
nice_z
# 'Friday May 26, 2017'

def parse_ymd(s):   # 'YYYY-MM-DD' 형으로 날짜형식을 알고 있는 경우
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))


'''

4장 1절 이터레이터 소비 : 순환 가능한 아이템에 접근할 때 for 루프문을 사용하지 않는 경우 next() 함수를 사용하고 StopIteration 예외를 처리하기 위한 코드를 직접 작성.


* 이터레이터와 제너레이터 

1. 이터레이터

1) 이터레이블

iterable 의 의미는 member를 하나씩 차례로 반환 가능한 object를 말한다. sequence type인 list, str, tuple 이 대표적이다.

당연하게 사용했던 for 문은 사실 range() 로 생성된 list가 iterable 하기 때문에 순차적으로 member들을 불러서 사용이 가능했던 것이다. 

non-sequence type 인 dict 나 file 도 iterable 하다고 할 수 있다. dict 또한 for 문을 이용해 순차적으로 접근이 가능하다. 

또한 __iter__() 나 __getitem__() 메소드로 정의된 class 는 모두 iterable 하다고 할 수 있다.

iterable 은 for loop 말고도, zip(), map()과 같이 sequence 한 특징을 필요로 하는 작업에 유용하게 사용된다. 

zip() 이나 map() 함수의 경우 iterable 을 argument 로 받는 것으로 정의되어 있다.


2) 이터레이터

Iterator 는 next() 메소드로 데이터를 순차적으로 호출 가능한 object 이다. 

만약 next() 로 다음 데이터를 불러 올 수 없을 경우 (가장 마지막 데이터인 경우) StopIteration exception을 발생시킨다. 

iterable 이라고 해서 반드시 iterator 라는 것은 아니다. 

list 는 iterable 이지만, next() 메소드로 호출해도 동작하지 않는다. iterator 가 아니라는 에러 메시지를 볼 수 있다.

만약, iterable 을 iterator 로 변환하고 싶다면, iter() 라는 built-in function 을 사용하면 된다. 

iter() 함수를 사용하여 list의 경우 list 를 listiterator 타입으로 변경 가능하다. 

iter() 함수로 타입 변경을 하면 next() 를 이용해 list의 정보를 하나씩 꺼낼 수 있다. 

그리고 마지막 정보를 호출 한 이후에 next() 를 호출하면 StopIteration 이라는 exception 이 발생됨을 볼 수 있다.

list 나 tuple 같은 iterable 한 object 를 사용할때 굳이 iter() 함수를 사용하지 않아도 for 문을 사용하여 순차적으로 접근이 가능한 것은 
for 문으로 looping 하는 동안, python 내부에서 임시로 list를 iterator로 자동 변환해주었기 때문이다.


2. 제너레이터

1) 제너레이터

generator 는 간단하게 설명하면 iterator 를 생성해 주는 function 이다. iterator 는 next() 메소드를 이용해 데이터에 순차적으로 접근이 가능한 object 이다.

generator 는 일반적인 함수와 비슷하게 보이지만, 가장 큰 차이 점은 yield 라는 구문일 것이다.

yield 는 generator 가 일반 함수와 구분되는 가장 핵심적인 부분이다. yield 를 사용함으로서 어떤 차이가 있게 되는지 살펴보자.

먼저, 일반적인 함수의 경우를 생각해보자. 일반적인 함수는 사용이 종료되면 결과값을 호출부로 반환 후 함수 자체를 종료시킨 후 메모리 상에서 클리어 된다.

하지만, yield 를 사용할 경우는 다르다. generator 함수가 실행 중 yield 를 만날 경우, 해당 함수는 그 상태로 정지 되며, 반환 값을 next() 를 호출한 쪽으로 전달 하게 된다. 

이후 해당 함수는 일반적인 경우 처럼 종료되는 것이 아니라 그 상태로 유지되게 된다. 

즉, 함수에서 사용된 local 변수나 instruction pointer 등과 같은 함수 내부에서 사용된 데이터들이 메모리에 그대로 유지되는 것이다.

generator 함수를 좀 더 쉽게 사용할 수 있도록 generator expression 을 제공한다. list comprehension 과 비슷하지만, [ ] 대신 ( ) 를 사용하면 된다.

2) 제너레이터의 이점

(1) generator는 memory를 효율적으로 사용할 수 있다.

list 의 경우 사이즈가 커질 수록 그만큼 메모리 사용량이 늘어나게 된다. 하지만, generator 의 경우는 사이즈가 커진다 해도 차지하는 메모리 사이즈는 동일하다. 

이는 list 와 generator의 동작 방식의 차이에 기인한다. list 는 list 안에 속한 모든 데이터를 메모리에 적재하기 때문에 크기 만큼 차지하는 메모리 사이즈가 늘어나게 된다. 

하지만 generator 의 경우 데이터 값을 한꺼번에 메모리에 적재 하는 것이 아니라 next() 메소드를 통해 차례로 값에 접근할 때마다 메모리에 적재하는 방식이다. 

따라서 list 의 규모가 큰 값을 다룰 수록 generator의 효율성은 더욱 높아지게 된다.


(2) Lazy evaluation 즉 계산 결과 값이 필요할 때까지 계산을 늦추는 효과를 볼 수 있다.

def sleep_func(x):
    print "sleep..."
    time.sleep(1)
    return x

위 sleep_func() 함수는 1초간 sleep 을 수행한 후 x 값을 return 하는 함수이다. 
만약 위 sleep_func() 함수를 이용해 llist 와 generator 를 생성하면 어떻게 동작할까.

# list 생성
list = [sleep_function(x) for x in xrange(5)]

for i in list:
    print i


<결과>
sleep...
sleep...
sleep...
sleep...
sleep...
0
1
2
3
4

# generator 생성
gen = (sleep_function(x) for x in xrange(5))

for i in gen:
    print i


<결과>
sleep...
0
sleep...
1
sleep...
2
sleep...
3
sleep...
4

위 결과 값을 보면, generator 를 사용하였을 경우 어떤 차이가 있는지 알 것이다. 

list 의 경우 list comprehension 을 수행 할때, list의 모든 값을 먼저 수행하기 때문에 sleep_func() 함수를 xrange() 값 만큼 한번에 수행하게 된다. 
만약 sleep_func() 에서 수행하는 시간이 길거나 list 값이 매우 큰 경우 처음 수행 할때 그만큼 부담으로 작용된다. 

하지만 generator 의 경우 generator 를 생성할 때는 실제 값을 로딩하지 않고, for 문이 수행 될때 하나씩 sleep_func()을 수행하며 값을 불러오게 된다. 
수행 시간이 긴 연산을 필요한 순간까지 늦출 수 있다는 점이 특징이다.

이러한 특징을 이용하면, fibonacci 수열과 같은 작업을 간결한 문법과 더불어 매우 효율적으로 코드를 작성할 수 있다.

def fibonacci_func(n):
    a,b = 0, 1
    i = 0
    while True:
        if (i > n):    return
        yield a
        a, b = b, a+b
        i += 1

fib = fibonacci_func(10)
for x in fib:
    print x


'''

# 예12.
items = [1, 2, 3]
it = iter(items)
next(it)

'''

4.2 델리케이팅 순환 : 리스트, 튜플 등 순환 가능 객체를 담은 사용자 정의 컨테이너를 만들었을 때 컨테이너에 사용할 수 있는 이터레이터를 만들 경우 __iter()__ 메소드를 정의한다.

- 파이썬 이터레이터 프로토콜은 __iter__()가 실제 순환을 수행하기 위해 __next__메소드를 구현하는 특별 이터레이터 객체를 반환하게 요구한다.

'''

# 예13.

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):     # 순환 요청을 _children 속성으로 전달
        returniter(self._children)


if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)

'''

4.3 제너레이터로 새로운 순환 패턴 생성 : 내장함수 range(), reversed()와 다른 동작을 하는 순환 패턴을 만들어보고 싶은 경우
                                   제너레이터 함수를 이용해서 사용자 정의로 만든다.
                                   
- 제너레이터로 함수를 만들면 내부에 yield가 들어간다.

 * 제너레이터 함수는 순환에 의한 "다음" 연산에만 응답하기 위해 실행된다. 제너레이터 함수가 리턴되면 순환을 중료한다.



'''

# 예14.
def countdown(n):
    print('Starting to count from', n)
    while n > 0 :
        yield n
        n -= 1
    print('Done!')


c = countdown(3)
c
# <generator object countdown at 0x0000000004ACCEB8>
next(c)
# 3

'''

4장 4절 이터레이터 프로토콜 구현 : 순환을 지원하는 객체를 만들 때 이터레이터 프로토콜을 구현하는 쉬운 방법이 필요한 경우 제너레이터 함수를 사용한다.



'''

# 예15.
class Node:
    def __init__(self, value):
        self._value = value
        self.children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()

if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))

for ch in root.depth_first():
    print(ch)

# 예16.
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, other_node):
        self._children.append(other_node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        return DepthFirstIterator(self)

class DepthFirstIterator(object):
    def __init__(self, start_node):
        self._node = start_node
        self._children_iter = None
        self._chlid_iter = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._children_iter is None:
            self._children_iter = iter(self._node)
            return self._node

        elif self._child_iter:
            try:
                nextchild = next(self._child_iter)
                return nextchild
            except StopIteration:
                self._child_iter = None
                return next(self)

        else:
            self._child_iter = next(self._children_iter).depth_first()
            return next(self)


'''

4.5 역방향 순환 : 시퀀스를 역방향으로 순환하고 싶은 경우 내장함수 reversed()를 사용한다. 객체가 __reversed()__ 특별 메소드를 구현하고 있거나 크기를 알 수 있는 경우에만
                사용가능하다. 두 조건 중 아무것도 만족하지 못하면 객체를 리스트로 변환해야 한다. 이 경우 많은 메모리를 사용한다.

- __reversed__() 메소드를 구현하면 사용자 정의 클래스에서 역방향 순환이 가능하다.                
- 역방향 이터레이터를 정의하면 코드가 효율적이게 되고 데이터를 리스트로 변환하고 순환하는 수고를 덜어준다.

'''

# 예17.
a=[1, 2, 3, 4]
for x in reversed(a):
    print(x)


# 예18.
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        n = self.start
        while n>0:
            yield n
            n -= 1

    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1

'''

4장 6절 추가 상태를 가진 제너레이터 함수 정의 : 제너레이터 함수를 정의하고 싶지만 사용자에게 노출할 추가 상태를 넣고 싶은 경우 __iter__() 메소드에 제너레이터 함수를
                                         넣어서 클래스로 구현한다.



'''

# 예19.
from collections import deque

class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen = histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()

with open('.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')
