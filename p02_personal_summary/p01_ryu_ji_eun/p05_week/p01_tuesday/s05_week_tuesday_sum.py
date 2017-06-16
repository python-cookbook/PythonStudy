###############################################################################################################
## 7.8  인자를 N개 받는 함수를 더 적은 인자로 사용
# 파이썬 코드에 콜백 함수나 핸들러로 사용할 호출체가 있다. 하지만 함수의 인자가 너무 많고 호출했을 때
# 예외가 발생한다.
################################################################################################################
# 함수의 인자 개수를 줄이려면 functools.partial() 사용
# 그러면 함수 인자에 고정값을 할당할 수 있고, 따라서 호출할 때 넣어야 하는 인자수를 줄일 수 있다

def spam(a,b,c,d):
    print(a,b,c,d)

# partial()로 특정값 고정
from functools import partial
s1 = partial(spam,1)                        # a = 1
s1(2,3,4)                                   # 1 2 3 4

s1(4,5,6)                                   # 1 4 5 6

s2 = partial(spam, d=42)                    # d = 42
s2(1,2,3)                                   # 1 2 3 42

s2(4,5,5)                                   # 4 5 5 42

s3 = partial(spam, 1,2,d=42)                # a = 1, b = 2, d = 42
s3(3)                                       # 1 2 3 42
s3(4)                                       # 1 2 4 42
s3(5)                                       # 1 2 5 42


# partial()이 특정 인자의 값을 고정하고 새로운 호출체를 반환한다. 이 새로운 호출체는 할당하지 않은 인자를 받고
# partial()에 주어진 인자와 합친 후 원본 함수에 전달한다


points = [(1,2),(3,4),(5,6),(7,8)]

import math
def distance(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

# 이제 어떤 점에서부터 이 점까지의 거리에 따라 정렬을 해야한다면 어떻게 할까? partial() 쓰자
pt = (4,3)
points.sort(key=partial(distance,pt))
print(points)
# [(3,4),(1,2),(5,6),(7,8)]


def output_result(result,log=None):
    if log is not None:
        log.debug('Got: %r',result)


# 샘플 함수
def add(x,y):
    return x+y

if __name__=='__main__':
    import logging
    from multiprocessing import Pool
    from functools import partial

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')

    p = Pool()
    p.apply_async(add, (3,4), callback=partial(output_result, log=log))
    p.close()
    p.join()


# apply_async()로 콜백 함수를 지원할 때, partial()을 사용해서 추가적인 로깅 인자를 넣었다.
# multiprocessing은 하나의 값으로 콜백 함수를 호출하게 되는 것이다

from socketserver import StreamRequestHandler, TCPServer
class EchoHandler(StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'GOT:'+line)

serv = TCPServer(('', 15000), EchoHandler)
serv.serve_forever()


# 하지만 EchoHandler 클래스에 __init__() 메소드가 추가적인 설정 인자를 받게 하고 싶다고 가정해보자
class EchoHandler(StreamRequestHandler):
    # ack는 키워드로만 넣을 수 있다.
    # *args, **kwargs는 그 외 일반적인 파라미터이다
    def __init__(self,*args,ack,**kwargs):
        self.ack = ack
        super().__init__(*args, **kwargs)
    def handle(self):
        for line in self.rfile:
            self.wfile.write(self.ack + line)


# 이 코드는 예외가 발생하는데, partial()을 사용해서 ack인자에 값을 넣어주면 해결된다
from functools import partial
serv = TCPServer(('',15000),partial(EchoHandler, ack=b'RECEIVED'))
serv.serve_forever()





###############################################################################################################
## 7.9 메소드가 하나인 클래스를 함수로 치환
# __init__()외에 메소드가 하나뿐인 클래스가 있는데, 코드를 간결하게 만들기 위해 이를 하나의 함수로 바꾸고 싶다
################################################################################################################
# 대부분 메소드가 하나뿐인 클래스는 closure를 사용해서 함수로 바꿀 수 있다
from urllib.request import urlopen

class UrlTemplate:
    def __init__(self,template):
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))


# 저 클래스를 간단한 함수로 치환 가능하다
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# 사용법
yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))




###############################################################################################################
## 7.10 콜백 함수에 추가적 상태 넣기
# 콜백 함수를 사용하는 코드를 작성중이다. (이벤트 핸들러, 완료 콜백 등)
# 이때 콜백 함수에 추가 상태를 넣고 내부 호출에 사용하고 싶다
################################################################################################################
# 콜백 함수 활용법을 알아보기 위해 콜백 함수를 호출하는 다음 함수를 정의하자
def apply_async(func, args, *, callback):
    # 결과 계산
    result = func(*args)
    # 결과 값으로 콜백 함수 호출
    callback(result)

def print_result(result):
    print('Got:',result)

def add(x,y):
    return x + y

apply_async(add, (2,3), callback=print_result)
# Got: 5

apply_async(add, ('hello','world'),callback=print_result)
# Got: helloworld


# 콜백 함수에 추가 정보를 넣는 한 가지 방법은 하나의 함수 대신 bound-method를 사용하는 것이다.
# 아래의 클래스는 결과값을 받을 때 마다 늘어나는 내부 시퀀스 숫자를 가지고 있다
class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))


# 이 클래스를 사용하려면 인스턴스를 만들고 바운드 메소드 handler를 콜백으로 사용해야 한다
r = ResultHandler()
apply_async(add, (2,3), callback=r.handler)
# [1] Got: 5

apply_async(add,('hello','world'), callback=r.handler)
# [2] Got: helloworld

# 클로저로 해도 됨
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler


# 예제
handler = make_handler()
apply_async(add, (2,3), callback=handler)
# [1] Got: 5
apply_async(add, ('hello','world'),callback=handler)
# [2] Got: helloworld


# coroutine 사용
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))

# 코루틴은 콜백으로 send() 메소드를 써야한다

# 추가적 인자와 partial 함수로 콜백에 상태를 넣을 수 있다
class SequenceNo:
    def __init__(self):
        self.sequence = 0


def handler(result, seq):
    seq.sequence += 1
    print('[{}] Got: {}'.format(seq.sequence, result))


seq = SequenceNo()
from functools import partial
apply_async(add, (2,3),callback=partial(handler, seq=seq))
# [1] Got: 5
apply_async(add, ('hello','world'), callback=partial(handler, seq=seq))
# [2] Got: helloworld




###############################################################################################################
## 7.11 인라인 콜백 함수
# 콜백 함수를 사용하는 코드를 작성하는데, 크기가 작은 함수를 너무 많이 만들어낼까 걱정
################################################################################################################
# generator와 coroutine을 사용하면 콜백 함수를 내부 함수에 넣을 수 있다
def apply_async(func, args, *, callback):
    # 결과 계산
    result = func(*args)

    # 결과값으로 콜백 함수 호출
    callback(result)


# async 클래스와 inlined_async 데코레이터를 포함하고 있는 코드
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


# 두 개의 코드 조각이 있으면 yield 구문으로 콜백 단계를 인라인 할 수 있다
def add(x,y):
    return x + y

@inlined_async                                                # 이거 빨갛게 뜸
def test():
    r = yield Async(add, (2,3))
    print(r)
    r = yield Async(add, ('hello','world'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n,n))
        print(r)
    print('Hi my love')


if __name__=='__main__':
    import multiprocessing
    pool = multiprocessing.Pool()
    apply_async = pool.apply_async

    # 테스트 함수 실행
    print(test())
'''
5                                                   # 이렇게 나온다고 함
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
Hi my love
'''


# 몰겠음


###############################################################################################################
## 7.12 클로저 내부에서 정의한 변수에 접근
# 클로저는 확장해서 내부 변수에 접근하고 수정하고 싶다
################################################################################################################
# 일반적으로 클로저 내부 변수는 외부와 완전히 단절되어 있으나, 접근 함수를 만들고 클로저에 함수 속성으로 붙이면
# 내부 변수에 접근할 수 있다
def sample():
    n = 0
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
        return func


# 사용법
f = sample()
f()
# n = 0
f.set_n(10)
f()
# n = 10
f.get_n()
# 10


# 이번 레시피를 이루는 두 가지 주요 기능
# 첫번째. nonlocal 선언으로 내부 변수를 수정하는 함수를 작성하는 것
# 두번째. 접근 메소드를 클로저 함수에 붙여 마치 인스턴스 메소드인 것 처럼 동작하는 것이다
import sys
class ClosureInstance:
    def __init__(self, locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals

        # 인스턴스 딕셔너리를 호출체로 갱신
            self.__dict__.update((key,value) for key, value in locals.items()
                                if callable(value))

    # 특별 메소드 리다이렉트
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

    return ClosureInstance()




###############################################################################################################
## 8.1 인스턴스의 문자열 표현식 변형
# 인스턴스를 출력하거나 볼 때 생성되는 결과물을 좀 더 보기 좋게 바꾸고 싶다
################################################################################################################
# __str__()과 __repr__() 메소드를 정의한다
class Pair:
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)
    def __str__(self):
        return '({0.x!s},{0.y!s})'.format(self)


## __repr__() 메소드는 인스턴스의 코드 표현식을 반환하고, 일반적으로 인스턴스를 재생성할 때 입력하는 텍스트
## __str__() 메소드는 인스턴스를 문자열로 변환하고, str()과 print() 함수가 출력하는 결과가 된다

p = Pair(3,4)
p                                       # Pair(3,4)         # __repr__() 결과
# print(p)                                # (3,4)             # __str__() 결과


p = Pair(3,4)
print('p is {0!r}'.format(p))                               # p is Pair(3, 4)
print('p is {0}'.format(p))                                 # p is (3,4)




###############################################################################################################
## 8.2 문자열 서식화 조절
# format() 함수와 문자열 메소드로 사용자가 정의한 서식화를 지원하고 싶다
################################################################################################################
# 클래스에 __format__() 메소드를 정의
_formats = {
    'ymd':'{d.year}-{d.month}-{d.day}',
    'mdy':'{d.month}/{d.day}/{d.year}',
    'dmy':'{d.day}/{d.month}/{d.year}'
}

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self,code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)


## Date 클래스의 인스턴스는 이제 다음과 같은 서식화를 지원한다
d = Date(2012, 12, 21)
format(d)
# '2012-12-21'
format(d, 'mdy')
# '12/21/2012'
'The date is {:ymd}'.format(d)
# 'The date is 2012-12-21'
'The date is {:mdy}'.format(d)
# 'The date is 12/21/2012'



###############################################################################################################
## 8.3 객체의 콘텍스트 관리 프로토콜 지원
# 객체가 콘텍스트 관리 프로토콜(with 구문)을 지원하게 만들고 싶다
################################################################################################################
# 객체와 with 구문을 함께 사용할 수 있게 하려면, __enter__()와 __exit__() 메소드를 구현해야 한다.
from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
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

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None


## 이 코드의 네트워크 연결은 with 구문에서 이루어진다
from functools import partial
conn = LazyConnection(('www.python.org',80))
# 연결 종료
with conn as s:
    # conn.__enter__() 실행: 연결
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192),b''))
    # conn.__exit__() 실행: 연결 종료



###############################################################################################################
## 8.4 인스턴스를 많이 생성할 때 메모리 절약
# 프로그램에서 많은 인스턴스를 생성하고 메모리를 많이 소비한다
################################################################################################################
# 간단한 자료 구조 역할 클래스는 __slots__속성을 클래스 정의에 추가하면 메모리 사용 절약
class Date:
    __slots__=['year','month','day']
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day


# __slots__을 정의하면 파이썬은 인스턴스에서 훨씬 더 압축된 내부 표현식을 사용한다
# 인스턴스마다 딕셔너리를 구성하지 않고 튜플이나 리스트같은 부피가 작은 고정 배열로 인스턴스가 만들어진다
# __slots__ 명시자에 리스팅된 속성 이름은 내부적으로 이 배열의 특정 인덱스에 매핑된다
# 부작용은 인스턴스에 새로운 속성을 추가할 수 없다는 점이다




###############################################################################################################
## 8.5 클래스 이름의 캡슐화
# 클래스 인스턴스의 프라이빗 데이터를 캡슐화하고 싶지만, 파이썬에는 접근 제어 기능이 부족하다
################################################################################################################
# 밑줄 _

class A:
    def __init__(self):
        self._internal = 0
        self.public = 1

    def public_method(self):
        '''
        A public method
        '''
        # ...

    def _internal_method(self):
        # ...

# 밑줄 두개 __

class B:
    def __init__(self):
        self.__private = 0

    def __private_method(self):
        # ...

    def public_method(self):
        # ...
        self.__private_method()
        # ...

