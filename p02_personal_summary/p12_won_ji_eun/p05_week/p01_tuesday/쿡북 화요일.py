            #7.8 인자를 N 개 받는 함수를 더 적은 인자로 사용

#문제: 함수의 인자가 너무 많을 때 
#해결방법: functools.partial() 사용

def spam(a,b,c,d):
    print(a,b,c,d)

from functools import partial
s1 = partial(spam, 1)
s1(2,3,4)
#(실행결과) 1 2 3 4

s1(4,5,6)
#(실행결과) 1 4 5 6

s2 = partial(spam, d=42)
s2(1,2,3)
#(실행결과) 1 2 3 42

s2(4,5,5)
#(실행결과) 4 5 5 42

s3 = partial(spam, 1,2,d=42)
s3(3)
#(실행결과) 1 2 3 42

s3(4)
#(실행결과) 1 2 4 42

s3(5)
#(실행결과) 1 2 5 42

points = [(1,2), (3,4), (5,6), (7,8)]

import math
def distance(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

pt = (4,3)
points.sort(key=partial(distance, pt))
print(points)
#(실행결과) [(3, 4), (1, 2), (5, 6), (7, 8)]


def output_result(result, log=None):
    if log is not None:
        log.debug('Got: %r', result)

#샘플함수
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




            #7.9 메소드가 하나인 클래스를 함수로 치환

#문제: 코드를 간결하게 만들기
#해결방법 : closure 사용

from urllib.request import urlopen

class UrlTemplate:
    def __init__(self, template):
        self.template = template
    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

def urltemplate(template):      
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener


            #7.10 콜백함수에 추가적 상태 넣기

#문제: 콜뱀 함수에 추가상태를 넣고 내부 호출에 사용
#해결방법: 콜백 함수의 활용
 
def apply_async(func, args, *, callback):
    result = func(*args)

    callback(result)

def print_result(result):
    print('Got:', result)

def add(x,y):
    return x+y

apply_async(add, (2,3), callback=print_result)
# (실행결과) Got: 5

apply_async(add, ('hello', 'world'), callback=print_result)
# (실행결과) Got: helloworld


class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))

r = ResultHandler()
apply_async(add, (2,3), callback=r.handler)
# (실행결과) [1] Got : 5

apply_async(add, ('hello', 'world'), callback=r.handler)
# (실행결과) [2] Got : helloworld

  

            #7.11 인라인 콜백 함수

#문제: 콜백함수를 사용하는 코드를 작성하는데 크기가 작은 함수를 너무 많이 많들어낸다.
#해결방법 : 제너레이터와 코루틴 사용

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

@inlined_async 
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

#(실행결과) 
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



            #7.12 클로저 내부에서 정의한 변수에 접근

#문제: 클로저는 확장해서 내부변수에 접근하고 수정하고 싶다,
#해결방법: 접근함수 만들고 클로저에 함수 속성으로 붙여서 내부 변수에 접근


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
f()
#(실행결과) n= 0

f.set_n(10)
f()
#(실행결과) n=10

f.get_n()
#(실행결과) 10

 
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
#(실행결과) <__main__.ClosureInstance object at 0x10069ed10>

s.push(10)
s.push(20)
s.push('Hello')
len(s)
#(실행결과) 3

s.pop()
#(실행결과) 'Hello'
s.pop()
#(실행결과) 20
s.pop()
#(실행결과) 10

 
 
                     #Chapter 8 클래스와 객체
                     
         #8.1 인스턴스의 문자열 표현식 변형

#문제: 인스턴스를 출력하거나 볼 때 생성되는 결과물을 좀 더 보기 좋게 바꾸고 싶다
#해결방법: __str__() 과 __repr__() 메소드

class Pair:
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def __repr__(self): 
        return 'Pair({0.x!r}, {0.y!r})'.format(self)
    def __str__(self):  
        return '({0.x!s}, {0.y!s})'.format(self)

p = Pair(3,4)
p
#(실행결과) Pair(3,4) #  __repr__() 결과
print(p)
#(실행결과) (3,4) # __str__() 결과

print('p is {0!r}'.format(p))
#(실행결과) p is Pair(3,4)
print('p is {0}'.format(p))
#(실행결과) p is (3,4)


        
            #8.2 문자열 서식화 조절

#문제: format() 함수와 문자열 메소드로 사용자가 정의한 서식화 지원
#해결방법:__format__() 메소드를 정의

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
#(실행결과) '2012-12-21'
format(d, 'mdy')
#(실행결과) '12/21/2012'



            # 8.3 객체의 콘텍스트 관리 프로토콜 지원

#문제 __enter__() 와 __exit__() 메소드

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


conn = Lazyconnection(('www.python.org', 80))
with conn as s :
    # conn.__enter__() 실행 : 연결
    s.send(b'GET /index.htmml HTTP/1.0\r\n')
    s.send(b'Host : www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() 실행 :연결 종료


            # 8.4 인스턴스를 많이 생성할 때 메모리 절약

# 문제 : 인스턴스를 많이 생성하고 메모리를 많이 소비할때
#해결방법 __slots__ 사용

class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day



            # 8.5 클래스 이름의 캡슐화

# 예제 _ 로 시작하는 모든 이름은 내부 구현에서만 사용하도록 가정

class A:
    def __init__(self):
        self.__internal = 0 # 내부속성
        self.public = 1     # 공용 속성

# 예제 서브클래스에서 숨겨야 할 내부 속성이 있는 경우 __ 밑줄 두개로 사용

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
        self.__private = 1 # B.__private 오버라이드 하지 않는다

    def __private_method(self): # B.__private_method() 를 오버라이드하지 않는다
        ...
#예제 이름 뒤에 밑줄 하나붙이기

lambda_ = 2.0 # lambda 키워드와 충돌 피하기 위해 밑줄 붙인다.
