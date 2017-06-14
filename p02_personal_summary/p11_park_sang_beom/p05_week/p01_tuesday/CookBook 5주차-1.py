'''
--------------------------------------------------------------------------------------
7.8 인자를 N개 받는 함수를 더 적은 인자로 사용

문제 : 파이썬 코드에 콜백함수나 핸들러로 사용할 호출체가 있다. 하지만 함수의 인자가
      너무 많고 호출했을 때  예외가 발생한다
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 함수의 인자를 줄이려면 functools.partial() 사용

- partial() 함수를 사용하면 함수의 인자에 고정 값을 할당할 수 있고, 따라서 호출할 때
  넣어야 하는 인자 수를 줄일 수 있다
--------------------------------------------------------------------------------------
'''

# partial()로 특정 값 고정
from functools import partial

def spam(a, b, c, d):
    print(a, b, c, d)

s1 = partial(spam, 1)           # a = 1
s2 = partial(spam, d=42)        # d = 42
s3 = partial(spam, 1, 2, d=42)  # a = 1, b = 2, d = 42

s1(2, 3, 4)
s2(1, 2, 3)
s2(4, 5, 5)
s3(3)
s3(4)
s3(5)

'''
=> partial()이 특정 인자의 값을 고정하고 새로운 호출체를 반환
   이 새로운 호출체는 할당하지 않은 인자를 받고, partial()에 주어진 인자와 합친 후 원본 함수에 전달
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 함수를 사용해서 두 점 사이의 거리 구하기
--------------------------------------------------------------------------------------
'''

import math
from functools import partial

points = [(1, 2), (3, 4), (5, 6), (7, 8)]

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

pt = (4, 3)
points.sort(key=partial((distance, pt)))

print(points)

'''
--------------------------------------------------------------------------------------
- multiprocessing을 사용해서 비동기식으로 결과를 계산하고, 결과 값과 로깅 인자를 받는 콜백 함수에
  그 결과를 전달하는 코드 
--------------------------------------------------------------------------------------
'''

def output_result(result, log=None):
    if log is not None:
        log.debug('Got : %r', result)

# 샘플 함수
def add(x, y):
    return x + y

if __name__ == '__main__':
    import logging
    from multiprocessing import Pool
    from functools import partial

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')

    p = Pool()
    p.apply_async(add, (3, 4), callback=partial(output_result, log=log))
    p.close()
    p.join()

'''
=> apply_async()로 콜백 함수를 지원할 때, partial() 을 사용해서 추가적인 로깅 인자를 넣었다

=> multiprocessing은 하나의 값으로 콜백 함수를 호출하게 되는 것이다다
-------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 네트워크 서버를 작성한다고 할때 socketsever 모듈을 사용하면 상대적으로 편하게 작업할 수 있다
--------------------------------------------------------------------------------------
'''

from socketserver import StreamRequestHandler, TCPServer

class EchoHandler(StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'GOT : ' + line)

serv = TCPServer(('', 15000), EchoHandler)
serv.serve_forever()

# EchoHandler 클래스에 __init__() 메소드가 추가적인 설정 인자 받기
class EChoHandler(StreamRequestHandler):
    # ack 는 키워드로만 넣을 수 있는 인자
    # *args, **kwargs 는 그 외 일반적인 파라미터 이다
    def __init__(self, *args, ack, **kwargs):
        self.ack = ack
        super().__init__(*args, **kwargs)

    def handle(self):
        for line in self.rfile:
            self.wfile.write(self.ack + line)




'''
--------------------------------------------------------------------------------------
7.9 메소드가 하나인 클래스를 함수로 치환

문제 : __init__() 외에 메소드가 하나뿐인 클래스가 있는데, 코드를 간결하게 만들기 위해 이를 하나의 함수로 만들기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 많은 경우 메소드가 하나뿐인 클래스는 클로저(closure)를 사용해서 함수로 바꾸기
  템플릿 스킴을 사용해서 URL 을 뽑아내는 예제
--------------------------------------------------------------------------------------
'''

from urllib.request import urlopen

class UrlTemplate:
    def __init__(self, template):
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

# 사용법. 야후(yahoo)에서 주식 데이터 받기
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')

for line in yahoo.open(names='IBM, AAPL, FB', field='sl1c1v'):
    print(line.decode('utf-8'))


# 클래스를 훨씬 간단한 함수로 치환
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# 사용법
yahoo = urlopen('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM, AAPL, FB', field='sl1c1v'):
    print(line.decode('utf-8'))

'''
--------------------------------------------------------------------------------------
=> 대개의 경우 메소드가 하나뿐인 클래스가 필요할 때는 추가적인 상태를 메소드에 저장할때 뿐이다

=> opener() 함수가 template 인자의 값을 기억하고 추후 호출에 사용
--------------------------------------------------------------------------------------
'''





'''
--------------------------------------------------------------------------------------
7.10 콜백 함수에 추가적 상태 넣기

문제 : 콜백 함수를 사용하는 코드를 작성 중이다(이벤트 핸들러, 완료 콜백등)
      이때 콜백 함수에 추가 상태를 넣고 내부 호출에 사용하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 콜백 함수의 활용 예제
--------------------------------------------------------------------------------------
'''

def apply_async(func, args, *, callback):
    # 결과 계산
    result = func(*args)

    # 결과 값으로 콜백 함수 호출
    callback(result)

def print_result(result):
    print('Got : ', result)

def add(x, y):
    return x + y

apply_async(add, (2, 3), callback=print_result)
apply_async(add, ('hello', 'world'), callback=print_result)

'''
--------------------------------------------------------------------------------------
- 콜백 함수에 추가 정보를 넣는 방법으로 하나의 함수 대신 바운드-메소드(bound-method) 사용하기
--------------------------------------------------------------------------------------
'''

class ResultHandler:
    def __init__(self):
        self.sequence = 0

    def handler(self, result):
        self.sequence += 1
        print('[{}] Got : {}'.format(self.sequence, result))

# 위 클래스를 사용하려면 인스턴스를 만들고 바운드-메소드 handler를 콜백으로 사용
r = ResultHandler()

apply_async(add, (2, 3), callback=r.handler)
apply_async(add, ('hello', 'world'), callback=r.handler)

# 클래스의 대안으로 클로저 사용해서 상태를 저장
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got : {}'.format(sequence, result))

handler = make_handler()

apply_async(add, (2, 3), callback=handler)
apply_async(add, ('hello', 'world'), callback=handler)

# 코루틴(coroutine) 사용
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got : {}'.format(sequence, result))

# 코루틴의 경우에는 콜백으로 send() 메소드 사용
handler = make_handler()
next(handler)       # Advance to the yield

apply_async(add, (2, 3), callback=handler.send)
apply_async(add, ('hello', 'world'), callback=handler.send)

# 추가적인 인자와 파셜 함수(partial funcion) 애플리케이션으로 콜백에 상태에 넣을 수 있다
from functools import partial
class SequenceNo:
    def __init__(self):
        self.sequence = 0

    def handler(result, seq):
        seq.sequence += 1
        print('[{}] Got : {}'.format(seq.sequence, result))

seq = SequenceNo()

apply_async(add, (2, 3), callback=partial(handler, seq=seq))
apply_async(add, ('hello', 'world'), callback=partial(handler, seq=seq))

'''
--------------------------------------------------------------------------------------
=> 콜백 함수의 문제점
   
   콜백 실행으로 이끄는 초기 요청 코드와 콜백 함수가 끊어진다
   결과적으로 요청을 한 곳과 처리하는 곳이 서로를 찾지 못하게 된다
   
   콜백 함수가 여러 단계에서 걸쳐 실행을 계속하도록 만들기 위해서는 어떻게 관련 상태를 저장하고 불러올지 정해야 한다
   
=> 클로저를 사용하면 수정 가능한 변수를 조심해서 사용해야 한다
 
=> 콜백 핸들러로 코루틴을 사용하는 것은 클로저 방식과 밀접한 관련이 있다
   코루틴은 단순히 하나의 함수로 이루어져 있기 때문에 더 깔끔하게 볼 수도 있다

=> partial()에서 해야 하는 작업이 추가적인 값을 콜백에 전달하는 것 뿐일때 유용
   apply_async(add, (2, 3), callback=lambda r: handler(r, seq))
--------------------------------------------------------------------------------------
'''





'''
--------------------------------------------------------------------------------------
7.11 인라인 콜백 함수

문제 : 콜백 함수를 사용하는 코드를 작성하는데, 크기가 작은 함수를 너무 많이 만들어 낼까 걱정이 된다
      코드가 좀 더 정상적인 절차적 단계를 거치도록 하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 제너레이터(generator) 와 코루틴(coroutine)을 사용하면 콜백 함수를 함수 내부에 넣을 수 있다
--------------------------------------------------------------------------------------
'''

def apply_async(func, args, *, callback):
    # 결과 계산
    result = func(*args)

    # 결과 값으로 콜백 함수 호출
    callback(result)

# Async 클래스와 inlined_async 데코레이터를 포함하고 있는 지원 코드
from queue import Queue
from functools import wraps

class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def inlined_async(func):
        @wraps(func)
        def wrapper(*args):
            f = func(*args)
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

# 두 개의 코드 조각이 있으면 yield 구문으로 콜백 단계를 인라인(inline) 할 수 있다
    def add(x, y):
        return x + y

    @inlined_async
    def test(self):
        r = yield Async(add, (2, 3))
        print(r)

        r = yield  Async(add, ('hello', 'world'))
        print(r)

        for n in range(10):
            r = yield Async(add, (n, n))
            print(r)
        print('Goodbye')

'''
--------------------------------------------------------------------------------------
=> 콜백과 관련 있는 코드에서 현재 연산이 모두 연기되고 특정 포인트에서 재시작한다

=> 프로그램 실행이 연기되고 재시작하는 발상은 자연스럽게 제너레이터 함수의 실행 모델과 매핑된다

=> 데코레이터가 yield 구문을 통해 제너레이터 함수를 하나씩 돈다
   이를 위해 결과 큐를 만들고 최소로 None 을 넣는다
   그리고 순환문을 돌며 결과를 큐에서 꺼내 제너레이터로 보낸다
   여기서 다음 생성으로 넘어가고 Async 인스턴스를 받는다다
-------------------------------------------------------------------------------------
'''





'''
--------------------------------------------------------------------------------------
7.12 클로저 내부에서 정의한 변수에 접근

문제 : 클로저는 확장해서 내부 변수에 접근하고 수정하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 일반적으로 클로저 내부 변수는 외부와 완전히 단절되어 있다
  하지만 접근 함수를 만들고 클로저에 함수 속성으로 붙이면 내부 변수에 접근할 수 있다
--------------------------------------------------------------------------------------
'''

def sample():
    n = 0
    # 클로저 함수
    def func():
        print('n=', n)

    # n에 대한 접근 메소드
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    # 함수 속성으로 클로저에 붙임
    func.get_n = get_n
    func.set_n = set_n
    return func

f = sample()
f()

f.set_n(10)
f()

f.get_n()

'''
=> nonlocal 선언으로 내부 변수를 수정하는 함수를 작성

=> 접근 메소드를 클로저 함수에 붙여 마치 인스턴스 메소드인 것처럼 동작하는 것(클래스와는 아무 관련 X)
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 클로저를 마치 클래스의 인스턴스인 것처럼 동작하게 만들 수 있다
  내부 함수를 인스턴스 딕셔너리에 복사하고 반환하기만 하면 된다
--------------------------------------------------------------------------------------
'''

import sys

class ClosureInstance:
    def __init__(self, locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals

        # 인스턴스 딕셔너리를 호출체로 갱신
        self.__dict__.update((key, value) for key, value in locals.items())

    # 특별 메소드 리다이렉트(redirect)
    def __len__(self):
        return self.__dict__['__len__']()

# 사용 예제
def Stack():
    items = []

    def push(item):
        items.append(item)

    def pop():
        return items.pop()

    def __len__():
        return len(items)

    return ClosureInstance

s = Stack()

print(s)
print(s.push(10))
print(s.push(20))
print(s.push('Hello'))
print(len(s))
print(s.pop())


# 클래스 속도 비교
class Stack2:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def __len__(self):
        return len(self.items)

from timeit import timeit

# 클로저
s = Stack()

# 클래스
s = Stack2()





'''
--------------------------------------------------------------------------------------
Chapter 8 클래스와 객체

8.1 인스턴스의 문자열 표현식 변형

문제 : 인스턴스를 출력하거나 볼 때 생성되는 결과물을 좀 더 보기 좋게 바꾸기 
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 인스턴스 문자열 표현식을 바꾸려면 __str__() 와 __repr__() 메소드 정의
--------------------------------------------------------------------------------------
'''

class Pair:
    def __init__(self, x ,y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)

p = Pair(3, 4)

p           # __repr__() 결과
print(p)    # __str__() 결과


# 서식화 코드 !r은 기본값으로 __str__() 대신 __repr__()을 사용
p = Pair(3, 4)

print('p is {0!r}'.format(p))
print('p is {0}'.format(p))

'''
=> __repr__() 메소드는 인스턴스의 코드 표현식을 반환하고, 일반적으로 인스턴스를 재생성할때 입력하는 텍스트

=> 내장 repr() 함수는 인터프리터에서 값을 조사할 때와 마찬가지로 이 텍스트 반환

=> __str__() 메소드는 인스턴스를 문자열로 변환하고, str() 와 print() 함수가 출력
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- __repr__() 와 __str__() 를 정의하면 디버깅과 인스턴스 출력을 간소화

- __repr__() 는 eval(repr(x)) == x 와 같은 텍스트로 만드는 것이 표준
  이것을 원하지 않거나 불가능하다면 일반적으로 <와> 사이에 텍스르를 넣는다
  
- __str__() 를 정의하지 않는면 대신 __repr__()의 결과물 사용
--------------------------------------------------------------------------------------
'''





'''
--------------------------------------------------------------------------------------
8.2 문자열 서식화 조절

문제 : format() 함수와 문자열 메소드로 사용자가 정의한 서식화 지원하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 문자열 서식화를 조절하고 싶으면 클래스에 __format__() 메소드 정의
--------------------------------------------------------------------------------------
'''

_formats = {'ymd' : '{d.year}-{d.month}-{d.day}',
            'mdy' : '{d.month}/{d.day}/{d.year}',
            'dmy' : '{d.day}/{d.month}/{d.year}'}

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

d = Date(2012, 12 ,21)

print(format(d))
print(format(d, 'mdy'))
print('The date is {:ymd}'.format(d))
print('The date is {:mdy}'.format(d))

'''
--------------------------------------------------------------------------------------
- __format__() 메소드는 파이썬의 문자열 서식화 함수에 후크(hook) 제공

- 서식화 코드의 해석은 모두 클래스 자체에 달려있다는 점이 중요
  따라서 코드에는 거의 모든 내용이 올 수 있다
--------------------------------------------------------------------------------------
'''

from datetime import date

d = date(2012, 12 ,21)

print(format(d))
print(format(d, '%A, %B %d, %Y'))
print('The end is {:%d %b %Y}. Goodbye'.format(d))





'''
--------------------------------------------------------------------------------------
8.3 객체의 콘텍스트 관리 프로토콜 지원

문제 : 객체가 콘텍스트 관리 프로토콜(with 구문)을 지원하게 만들기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 객체와 with 구문을 함께 사용할 수 있게 만들려면, __enter__() 와 __exit__() 메소드를 구현해야 한다
  네트워크 연결을 제공하는 예제 코드
--------------------------------------------------------------------------------------
'''

from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.famliy = family
        self.type = SOCK_STREAM
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.famliy, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None

# with 구문
from functools import partial

conn = LazyConnection(('www.python.org', 80))

# 연결종료
with conn as s:
    # conn.__enter__() 실행 : 연결
    s.send(b'GET /index.html HTTP/1.0\r\n\\')
    s.send(b'\r\n')
    resp = b''.join(partial(s.recv, 8192), b'')
    # conn.__exit__() 실행 : 연결 종료

'''
--------------------------------------------------------------------------------------
- 처음으로 with를 만나면 __enter__() 메소드가 호출된다
  __enter__()의 반환 값(있다면)은 as로 나타낸 변수에 위치시킨다
  
- __exit__() 메소드의 세 가지 인자에 예외 타입, 값, 트레이스백(traceback)이 들어있다

- __exit__() 메소드는 예외 정보를 고르거나 아무 일도 하지 않고 None을 반환하며 무시하는 방식을 선택할 수 있다
  만약 __exit__() 가 True를 반환하면 예외를 없애고 아무 일도 일어나지 않았던 것처럼 with 블록 다음의 프로그램을 계속해서 실행
--------------------------------------------------------------------------------------
'''

from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.famliy = family
        self.type = SOCK_STREAM
        self.connections = []

    def __enter__(self):
        sock = socket(self.famliy, self.type)
        sock.connect(self.address)
        self.connections.append(sock)
        return sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.connections.pop().close()

# 사용 예제
from functools import partial

conn = LazyConnection(('www.python.org', 80))
with conn as s1:
    ...
    with conn as s2:
        ...
        # s1 과 s2는 독립적 소켓

'''
--------------------------------------------------------------------------------------
- LazyConnection 클래스는 연결을 위한 팩토리(factory) 역할을 한다

- 내부적으로 스택을 위해 리스트를 사용, __enter__() 가 실행될 때마다, 새로운 연결을 만들고 스택에 추가

- __exit__() 메소드는 단순히 스택에서 마지막 연결을 꺼내고 닫는다
  사소한 문제지만 이로 인해서 중첩 with 구문으로 연결을 여러 개 생성할 수 있다
--------------------------------------------------------------------------------------
'''





'''
--------------------------------------------------------------------------------------
8.4 인스턴스를 많이 생성할 때 메모리 절약

문제 : 프로그램에서 많은(예 : 수백만) 인스턴스를 생성하고 메모리를 많이 소비한다
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 간단한 자료 구조 역할을 하는 클래스의 경우 __slots__ 속성을 클래스 정의에 추가하면 메모리 사용을 상당히 많이 절약
--------------------------------------------------------------------------------------
'''

class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

'''
=> __slots__ 을 정의하면 파이썬을 인스턴스에서 훨씬 더 압축된 내부 표현식을 사용

=> 인스턴스마다 딕셔너리를 구성하지 않고 튜플이나 리스트 같은 부피가 작은 고정 배열로 인스턴스가 만들어진다

=> __slots__ 명시자에 리스팅된 속성 이름은 내부적으로 이 배열의 특징 인덱스에 매핑된다

=> 슬롯을 사용하는 데서 발생하는 부작용은 인스턴스에 새로운 속성을 추가할 수 없다는 점
   __slots__ 명시자에 나열한 속성만 사용할 수 있다는 제약이 생긴다
--------------------------------------------------------------------------------------
'''





'''
--------------------------------------------------------------------------------------
8.5 클래스 이름의 캡슐화

문제 : 클래스 인스턴스의 프라이빗(private) 데이터를 캡슐화하고 싶지만 파이썬에는 접근 제어 기능이 부족
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 데이터나 메소드의 이름에 특정 규칙을 사용하여서 의도를 나타낸다

- 밑줄(_)로 시작해서 모든 이름은 내부구현에서만 사용하도록 가정
--------------------------------------------------------------------------------------
'''

class A:
    def __init__(self):
        self._internal = 0
        self.public = 1

    def public_method(self):
        '''
        A Public method
        '''

    def _internal_method(self):
        ...

'''
--------------------------------------------------------------------------------------
- 파이썬은 내부 이름에 누군가 접근하는 것을 실제로 막지는 않는다

- 이름 앞에 밑줄을 붙이는 것은 모듈이름과 모듈 레벨 함수에도 사용한다
--------------------------------------------------------------------------------------
'''

class B:
    def __init__(self):
        self.__private = 0

    def __private_method(self):
        ...

    def public_method(self):
        ...
        self.__private_method()
        ...

'''
--------------------------------------------------------------------------------------
- 이름 앞에 밑줄을 두 개 붙이면 이름이 다른 것으로 변한다
  앞에 나온 클래스의 프라이빗 속성은 _B__private 과 _B__private_method 로 이름이 변한다
  이런 속성은 속성을 통해 오버라이드 할 수 없다
--------------------------------------------------------------------------------------
'''

class C(B):
    def __init__(self):
        super().__init__()
        self.__private = 1  #B.__private를 오버라이드하지 않는다

    # B.__private_method()를 오버라이드하지 않는다
    def __private_method(self):
        ...

'''
=> __private 과 __private_method 의 이름은 _C__private 과 _C_private_method 로 변하기 때문에 
   B 클래스의 이름과 겹치지 않는다
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 대개의 경우 공용이 아닌 이름은 밑줄을 하나만 붙어야 한다
  하지만 코드가 서브클래싱을 사용할 것이고 서브클래스에서 숨겨야 할 내부 속성이 있다면 밑줄을 두 개 붙인다
  
- 예약해 둔 단어 이름과 충돌하는 변수를 정의하고 싶을 때가 있다
  이런 경우 이름 뒤에 밑줄을 하나 붙인다
  
  lambda_ = 2.0     # lambda 키워드와의 충돌을 피하기 위해 밑줄을 붙인다

- 밑줄을 변수 이름 앞에 붙이지 않은 이유는 내부적으로 사용하는 의도와의 혼동을 피하기 위해서이다
  변수 이름 뒤에 밑줄을 하나 붙여서 이 문제를 해결
--------------------------------------------------------------------------------------
'''






