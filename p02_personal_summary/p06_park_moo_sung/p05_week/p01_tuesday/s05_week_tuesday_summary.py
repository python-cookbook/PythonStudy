####################################

# 7.8 인자를 N 개 받는 함수를 더 적은 인자로 사용

# functools.partial() - 함수의 인자에 고정값 할당

def spam(a,b,c,d):
    print(a,b,c,d)

from functools import partial
s1 = partial(spam, 1)
s1(2,3,4)
## 1,2,3,4

s2 = partial(spam, d=42)
s2(1,2,3)
## 1,2,3,42

s3 = partial(spam, 1,2,d=42)
s3(100)
## 1,2,100,42

# 뭐지??

points = [(1,2), (3,4), (5,6), (7,8)]

import math
def distance(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

pt = (4,3)
points.sort(key=partial(distance, pt))
print(points)
## [(3, 4), (1, 2), (5, 6), (7, 8)]

# 콜백함수의 매개변수 설명을 변경하기(partial) - apply_async 로 콜백함수 지원할 때 partial 이용해서 추가적인 로깅 인자 넣음

def output_result(result, log=None):
    if log is not None:
        log.debug('Got: %r', result)

def add(x,y):
    return x+y

if __name__ == '__main__':
    import logging
    from multiprocessing import Pool
    from functools import partial

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')
    p = Pool()
    p.apply_async(add, (3,4), callback=partial(output_result, log=log))
    p.close()
    p.join()


####################################################

# 7.9 메소드가 하나인 클래스를 함수로 치환

# closure 이용해서 함수로 바꾸기

from urllib.request import urlopen

class UrlTemplate:              # 이 클래스를
    def __init__(self, template):
        self.template = template
    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

def urltemplate(template):      # 이렇게 하다니!
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

#################################################

# 7.10 콜백함수에 추가적 상태 넣기

# 콜뱀 함수 활용

def apply_async(func, args, *, callback):
    # 결과 계산
    result = func(*args)

    # 결과 값으로 콜백 함수 호출
    callback(result)

def print_result(result):
    print('Got:', result)

def add(x,y):
    return x+y

apply_async(add, (2,3), callback=print_result)
## Got: 5

# 콜백 함수에 추가적 정보 넣기(바운드-메소드 사용)

class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))

r = ResultHandler()
apply_async(add, (2,3), callback=r.handler)
## [1] Got : 5
apply_async(add, ('hello', 'world'), callback=r.handler)
## [2] Got : helloworld

# 콜백함수의 위험성 : 초기 요청 코드와 콜백 함수 간의 연관성이 떨어짐. 서로 잘 찾지 못해서 관리 어려움

# 상태를 고정시키고 저장하는 방식 1) 인스턴스에 상태 저장 2) 클로저에 저장(내부함수)--> 좀더 가볍고 자연스러움

# 클로저 방식의 주의사항 : 수정 가능한 변수 조심해서 사용

##############################################

# 7.11 인라인 콜백 함수

# 제너레이터, 코루틴

def apply_async(func, args, *, callback):
    result = func(*args)
    callback(result)

from queue import Queue
from functools import wraps

class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args

def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f=func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break
    return wrapper

def add(x,y):
    return x+y

@inlined_async # 데코레이터가 yield 구문을 통해 제너레이터 함수를 하나씩 돔
def test():
    r= yield Async(add, (2,3))
    print(r)
    r = yield Async(add, ('hello','world'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n,n))
        print(r)
    print('Goodbye')

test()
'''
5
helloworld
0
2
4
6
8
10
12
14
16
18
Goodbye
'''

#################################################

# 7.12 클로저 내부에서 정의한 변수에 접근

# 접근함수 만들고 클로저에 함수 속성으로 붙여서 내부 변수에 접근하기
# nonlocal 선언으로 내부 변수 수정


def sample():
    n=0
    # 클로저 함수
    def func():
        print('n=',n)

    # n에 대한 접근 메소드
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    # 함수 속성으로 클로저에 붙임
    func.get_n = get_n
    func.set_n = set_n
    return func()

f = sample()
f.set_n(10)
# n=10
f.get_n()
## 10

# 접근 메소드를 클로저 함수에 붙여 인스턴스 메소드처럼 동작

import sys
class ClosureInstance:
    def __init__(self, locals = None):
        if locals is None:
            locals = sys._getframe(1).f_locals

        # 인스턴스 딕셔너리를 호출체로 갱신
        self.__dict__.update((key,value) for key, value in locals.items() if callable(value))
    # 특별 메소드 리다이렉트
    def __len__(self):
        return self.__dict__['__len__']()

def Stack():
    items = []

    def push(item):
        items.append(item)

    def pop():
        return items.pop()

    def __len__():
        return len(items)

    return ClosureInstance()

s = Stack()
s
## <__main__.ClosureInstance object at 0x10069ed10>
s.push(10)
s.push(20)
s.push('Hello')
len(s)
## 3
s.pop()
## 'Hello'

#################################################

# 8.1 인스턴스의 문자열 표현식 변형

# __str__() 과 __repr__() 메소드

class Pair:
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def __repr__(self):  # 인스턴스의 코드 표현식 반환
        return 'Pair({0.x!r}, {0.y!r})'.format(self)
    def __str__(self):   # 인스턴스를 문자열로 변환하고 print() 함수가 출력하는 결과가 됨
        return '({0.x!s}, {0.y!s})'.format(self)

p = Pair(3,4)
p
## Pair(3,4) --> __repr__() 결과
print(p)
## (3,4) --> __str__() 결과

print('p is {0!r}'.format(p))
## p is Pair(3,4)
print('p is {0}'.format(p))
## p is (3,4)

#####################################################

# 8.2 문자열 서식화 조절

# format() 함수

_formats = {'ymd' : '{d.year}-{d.month}-{d.day}',
            'mdy' : '{d.month}/{d.day/{d.year}',
            'dmy' : '{d.day}/{d.month/{d.year}'}

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)

d = Date(2012, 12, 21)
format(d)
## '2012-12-21'
'{:mdy}'.format(d)
## '12/21/2012'

###################################################

# 8.3 객체의 콘텍스트 관리 프로토콜 지원

# __enter__() 와 __exit__() 메소드

from socket import socket, AF_INET, SOCK_STREAM

class Lazyconnection:
    def __init__(self, address, family = AF_INET, type = SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()
        self.sock = None


from functools import partial
# 연결 종료

conn = Lazyconnection(('www.python.org', 80))
with conn as s :
    # conn.__enter__() 실행 : 연결
    s.send(b'GET /index.htmml HTTP/1.0\r\n')
    s.send(b'Host : www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() 실행 :연결 종료

#########################################################

# 8.4 인스턴스를 많이 생성할 때 메모리 절약

# __slots__ (간단한 자료 구조 역할 하는 클래스인 경우 메모리 사용 절약)
# 인스턴스에서 훨씬 더 압축된 내부 표현식 사용.

class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

#########################################################

# 8.5 클래스 이름의 캡슐화

# 1. _ 로 시작하는 모든 이름은 내부 구현에서만 사용하도록 가정(조심스레 사용해 한다는 일종의 약속?)

class A:
    def __init__(self):
        self.__internal = 0 # 내부속성
        self.public = 1     # 공용 속성

# 2. 서브클래스에서 숨겨야 할 내부 속성이 있는 경우 __ 밑줄 두개로 사용(속성을 통해 오버라이드할 수 없음)

class B:
    def __init__(self):
        self.__private = 0

    def __private_method(self):
        ...
    def public_method(self):
        self.__private_method()


class C(B):
    def __init__(self):
        super().__init__()
        self.__private = 1 # B.__private 오버라이드 하지 않음

    def __private_method(self): # B.__private_method() 를 오버라이드하지 않음
        ...
# 3. 이름 뒤에 밑줄 하나(예약해 둔 단어 이름과 충돌하는 변수 정의하고 싶을 때 )

lambda_ = 2.0 # lambda 키워드와 충돌 피하기 위해 밑줄 붙임