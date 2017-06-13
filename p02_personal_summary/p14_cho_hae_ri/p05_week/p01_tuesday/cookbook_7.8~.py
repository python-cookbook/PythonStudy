

###############################################
#    7.8 ~ 8.5
###############################################


####### 7.8 인자를 n 개 받는 함수를 더 적은 인자로 사용  ##########

# 문제
# 파이썬 코드에 콜백 함수나 핸들러로 사용할 호출체가 있다. 하지만 함수의 인자가 너무 많고 호출했을 때 예외가 발생한다.

# 해결
# 함수의 인자 개수를 줄이려면 functools.partial() 을 사용해야 한다.
# functools.partial() 함수를 사용하면 함수의 인자에 고정 값을 할당할 수 있고 따라서 호출할 떄 넣어야 하는 인자 수를 줄일 수 있다.

def spam(a, b, c, d):
    print(a, b, c, d)


from functools import partial
s1 = partial(spam, 1) # a = 1
s1(2, 3, 4)
#1 2 3 4
s1(4, 5, 6)
#1 4 5 6
s2 = partial(spam, d=42) # d = 42
s2(1, 2, 3)
#1 2 3 42
s2(4, 5, 5)
#4 5 5 42
s3 = partial(spam, 1, 2, d=42) # a = 1, b = 2, d = 42
s3(3)
#1 2 3 42
s3(4)
#1 2 4 42
s3(5)
#1 2 5 42


# 토론

points = [ (1, 2), (3, 4), (5, 6), (7, 8) ]

import math
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)



def output_result(result, log=None):
    if log is not None:
        log.debug('Got: %r', result)


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



from socketserver import StreamRequestHandler, TCPServer

class EchoHandler(StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'GOT:' + line)

serv = TCPServer(('', 15000), EchoHandler)
serv.serve_forever()




class EchoHandler(StreamRequestHandler):

    def __init__(self, *args, ack, **kwargs):
        self.ack = ack
        super().__init__(*args, **kwargs)

    def handle(self):
        for line in self.rfile:
            self.wfile.write(self.ack + line)



# Exception happened during processing of request from ('127.0.0.1', 59834)
# Traceback (most recent call last):
# ...
# TypeError: __init__() missing 1 required keyword-only argument: 'ack'



from functools import partial
serv = TCPServer(('', 15000), partial(EchoHandler, ack=b'RECEIVED:'))
serv.serve_forever()



points.sort(key=lambda p: distance(pt, p))
p.apply_async(add, (3, 4), callback=lambda result: output_result(result,log))
serv = TCPServer(('', 15000),
        lambda *args, **kwargs: EchoHandler(*args, ack=b'RECEIVED:', **kwargs))




#### 7. 9 메소드가 하나인 클래스를 함수로 치환 ########

# 문제
# __init__()외에 메소드가 하나뿐인 클래스가 있는데 코드를 간결하게 하기 위해 이를 하나의 함수로 바꾸고 싶다.

# 해결
#클로저를 사용한다


from urllib.request import urlopen

class UrlTemplate:
    def __init__(self, template):
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))


yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))





#### 7. 10. 콜백함수에 추가적 상태 넣기 ########

# 문제
# 콜백 함수를 사용하는 코드를 작성중이다
# 이 때 콜백 함수에 추가 상태를 넣고 내부 호출에 사용하고 싶다.

# 해결
# 이 레시피는 많은 라이브러리와 프레임워크에서 찾을 수 있는 콜백 함수의 활용을 알아본다



def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# 사용 예
yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))





def apply_async(func, args, *, callback):
    result = func(*args)
    callback(result)



class ResultHandler:

    def __init__(self):
        self.sequence = 0

    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))



def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler




def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))




########## 7.11. 인라인 콜백 함수 ##########


# 문제
# 콜백 함수를 사용하는 코드를 작성하는데, 크기가 작은 함수를 너무 많이 만들어 낼까 걱정임

# 해결
# 제너레이터와 코루틴(coroutine)을 사용하면 콜백함수를 함수 내부에 넣을 수 있다.


def apply_async(func, args, *, callback):
    # 결과 계산
    result = func(*args)

    # 결과값으로 콜백 호출
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


def add(x, y):
    return x + y

@inlined_async
def test():
    r = yield Async(add, (2, 3))
    print(r)
    r = yield Async(add, ('hello', 'world'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)
    print('Goodbye')





# 5
# helloworld
# 0
# 2
# 4
# 6
# 8
# 10
# 12
# 14
# 16
# 18
# Goodbye



# 토론


if __name__ == '__main__':
    import multiprocessing
    pool = multiprocessing.Pool()
    apply_async = pool.apply_async

    test()




############ 7.12. 클로저 내부에서 정의한 변수에 접근 ##########

# 문제
# 클로저는 확장해서 내부 변수에 접근하고 수정하고 싶다

# 해결
# 접근함수를 만들자


def sample():
    n = 0
    # Closure function
    def func():
        print('n=', n)

    # Accessor methods for n
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    # Attach as function attributes
    func.get_n = get_n
    func.set_n = set_n
    return func




f = sample()
f()
#n= 0
f.set_n(10)
f()
#n= 10
f.get_n()
#10



# 토론
# 클로저를 마치 클래스의 인스턴스 인 것처럼 동작하게 하려면!!

import sys
class ClosureInstance:
    def __init__(self, locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals

        # Update instance dictionary with callables
        self.__dict__.update((key,value) for key, value in locals.items()
                            if callable(value) )
    # Redirect special methods
    def __len__(self):
        return self.__dict__['__len__']()

# Example use
def Stack():
    items = []
    def push(item):
        items.append(item)

    def pop():
        return items.pop()

    def __len__():
        return len(items)

    return ClosureInstance()





###########################################################
#  chapter 8 클래스와 객체
###########################################################



#######8.1 인스턴스의 문자열 표현식 변형 ##########

# 문제
# 인스턴스를 출력하거나 볼 때 생성되는 결과물을 좀 더 보기 좋게 바꾸고 싶다면

# 해결
# 인스턴스의 문자열 표현식을 바꾸려면 __str__() 와 __repr__() 메소드를 정의한다.

class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)



p = Pair(3, 4)
p
#Pair(3, 4) # __repr__() output
print(p)
#(3, 4) # __str__() output



def __repr__(self):
    return 'Pair({0.x!r}, {0.y!r})'.format(self)


def __repr__(self):
    return 'Pair(%r, %r)' % (self.x, self.y)





#######8.2. 문자열 서식화 조절 ##########

# 문제
# format() 함수와 문자열 메소드로 사용자가 정의한 서식화를 지원하고 싶지 않다.

# 해결
# 문자열 서식화를 조절하고 싶으면 클래스에 __format__() 메소드를 정의한다.



_formats = {
    'ymd' : '{d.year}-{d.month}-{d.day}',
    'mdy' : '{d.month}/{d.day}/{d.year}',
    'dmy' : '{d.day}/{d.month}/{d.year}'
    }

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


# 사용하기

d = Date(2012, 12, 21)
format(d)
#'2012-12-21'
format(d, 'mdy')
#'12/21/2012'
'The date is {:ymd}'.format(d)
#'The date is 2012-12-21'
'The date is {:mdy}'.format(d)
#'The date is 12/21/2012'





#######8.3. 객체의 콘텍스트 관리 프로토콜 지원 ##########

# 문제
# 객체가 콘텍스트 관리 프로토콜(with구문)을 지원하게 만들고 싶다

# 해결
# __enter__()  와 __exit__() 메소드를 구현해야 한다.




from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
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



from functools import partial

conn = LazyConnection(('www.python.org', 80))
# 연결 닫힘
with conn as s:
    # conn.__enter__() 실행 : 연결
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() 실행 : 연결종료


# 토론

from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        self.connections = []

    def __enter__(self):
        sock = socket(self.family, self.type)
        sock.connect(self.address)
        self.connections.append(sock)
        return sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.connections.pop().close()

# Example use
from functools import partial

conn = LazyConnection(('www.python.org', 80))
with conn as s1:
    pass
    with conn as s2:
        pass



#######8.4. 인스턴스를 많이 생성할 때 메모리 절약 ##########

# 문제
# 인스턴스를 많이 생성하고 메모리를 많이 소비한다

# 해결
# __slots__ 속성을 클래스 정의에 추가하자


class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day





#######8.5. 클래스 이름의 캡슐화 ##########

# 문제
# 클래스 인스턴스의 프라이빗 데이터를 캡슐화하고 싶지만, 파이썬에는 접근 제어 기능이 부족하다

# 해결
# _ 로 시작하는 모든 이름은 내부에서만 사용하도록 가정하는 것



class A:
    def __init__(self):
        self._internal = 0 # 내부 속성
        self.public = 1 # 공용 속성

    def public_method(self):
        '''
        A public method
        '''
        pass

    def _internal_method(self):
        pass



# __ 로 시작하는 이름이 나온느 경우

class B:
    def __init__(self):
        self.__private = 0

    def __private_method(self):
        pass

    def public_method(self):
        pass
        self.__private_method()





class C(B):
    def __init__(self):
        super().__init__()
        self.__private = 1 # Does not override B.__private

    # Does not override B.__private_method()
    def __private_method(self):
        pass
    ##











