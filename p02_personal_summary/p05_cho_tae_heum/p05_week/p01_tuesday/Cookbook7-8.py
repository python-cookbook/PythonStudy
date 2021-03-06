# 7.8 인자를 N개 받는 함수를 더 적은 인자를 사용
def spam(a, b, c, d):
    print(a, b, c, d)
from functools import partial
s1 = partial(spam, 1)
print(s1(2, 3, 4))
s2 = partial(spam, d=42)
print(s2(1, 2, 3))
s3 = partial(spam, 1, 2, d=42)
print(s3(3))
points = [ (1, 2), (3, 4), (5, 6), (7, 8) ]
import math

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)
pt = (4, 3)
points.sort(key=partial(distance,pt))
print(points)

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
class Echo(StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'GOT:' + line)
serv = TCPServer(('', 15000), Echo)
serv.serve_forever()
class Echo(StreamRequestHandler):
    def __init__(self, *args, ack, **kwargs):
        self.ack = ack
        super().__init__(*args, **kwargs)
    def handle(self):
        for line in self.rfile:
            self.wfile.write(self.ack + line)

from functools import partial
serv = TCPServer(('', 15000), partial(Echo, ack=b'RECEIVED:'))
serv.serve_forever()
points.sort(key=lambda p: distance(pt, p))
p.apply_async(add, (3, 4), callback=lambda result: output_result(result,log))
serv = TCPServer(('', 15000),lambda *args, **kwargs: Echo(*args,ack=b'RECEIVED:',**kwargs))


# 7.9 메소드가 하나인 클래스를 함수로 치환
from urllib.request import urlopen
class UrlTemplate:
    def __init__(self, template):
        self.template = template
    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener
yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))


# 7.10 콜백 함수에 추가적 상태 넣기
def apply_async(func, args, *, callback):
    result = func(*args)
    callback(result)

def print_result(result):
    print('Got:', result)

def add(x, y):
    return x + y

apply_async(add, (2, 3), callback=print_result)
apply_async(add, ('hell', 'wo'), callback=print_result)

class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))
r = ResultHandler()
apply_async(add, (2, 3), callback=r.handler)
apply_async(add, ('hell', 'wo'), callback=r.handler)
def make_handler():
    s = 0
    def handler(result):
        nonlocal s
        s += 1
        print('[{}] Got: {}'.format(s, result))
    return handler
handler = make_handler()
apply_async(add, (2, 3), callback=handler)
apply_async(add, ('hell', 'wo'), callback=handler)

def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
handler = make_handler()
next(handler)
apply_async(add, (2, 3), callback=handler.send)
apply_async(add, ('hello', 'world'), callback=handler.send)

class SequenceNo:
    def __init__(self):
        self.sequence = 0
    def handler(result, seq):
        seq.sequence += 1
        print('[{}] Got: {}'.format(seq.sequence, result))
seq = SequenceNo()
from functools import partial
apply_async(add, (2, 3), callback=partial(handler, seq=seq))
apply_async(add, ('hell', 'wo'), callback=partial(handler, seq=seq))


# 7.11 인라인 콜백 함수
def apply_async(func, args, *, callback):
    r = func(*args)
    callback(r)
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

    def add(x,y):
        return x + y

    def test():
        r = yield Async(add, (2, 3))
        print(r)
        r = yield Async(add, ('hell', 'wo'))
        print(r)
        for n in range(10):
            r = yield Async(add, (n, n))
            print(r)
        print('bye')

if __name__ == '__main__':
    import multiprocessing
    pool = multiprocessing.Pool()
    apply_async = pool.apply_async
    test()


# 7.12 클로저 내부에서 정의한 변수에 접근
def sample():
    n = 0
    def func():
        print('n=', n)
    def get_n():
        return n
    def set_n(value):
        nonlocal n
        n = value
    func.get_n = get_n
    func.set_n = set_n
    return func
f = sample()
f()
f.set_n(10)
f()
f.get_n()
f()
import sys
class ClosureInstance:
    def __init__(self, locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals
        self.__dict__.update((key,value) for key, value in locals.items()if callable(value) )
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
print(s)
s.push(10)
s.push(20)
s.push('Hello')
print(len(s))
print(s.pop())
print(s.pop())
print(s.pop())
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
s = Stack()
print(timeit('s.push(1);s.pop()', 'from __main__ import s'))
s = Stack2()
print(timeit('s.push(1);s.pop()', 'from __main__ import s'))


# 8.1 인스턴스의 문자열 표현식 변형
class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)
    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)
p = Pair(3, 4)
print(p)
p = Pair(3, 4)
print('p is {0!r}'.format(p))
print('p is {0}'.format(p))


# 8.2 문자열 서식화 조절
_formats = {'ymd' : '{d.year}-{d.month}-{d.day}','mdy' : '{d.month}/{d.day}/{d.year}','dmy' : '{d.day}/{d.month}/{d.year}'}
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
print(format(d))
print(format(d,'mdy'))


# 8.3 객체의 콘테스트 관리 프로토콜 지원
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

from functools import partial
conn = LazyConnection(('www.python.org', 80))
with conn as s:
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    print(resp)
from socket import socket, AF_INET, SOCK_STREAM
class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.connections = []

    def __enter__(self):
        sock = socket(self.family, self.type)
        sock.connect(self.address)
        self.connections.append(sock)
        return sock
    def __exit__(self, exc_ty, exc_val, tb):
        self.connections.pop().close()


# 8.4 인스턴스를 많이 생성할 때 메모리 절약
class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day


# 8.5 클래스 이름의 캡슐화
class A:
    def __init__(self):
        self._internal = 0
        self.public = 1
    def public_method(self):
        '''A public method'''
        ...
    def _internal_method(self):
        ...
class B:
    def __init__(self):
        self.__private = 0
    def __private_method(self):
        ...
    def public_method(self):
        ...
        self.__private_method()
        ...
class C(B):
    def __init__(self):
        super().__init__()
        self.__private = 1
    def __private_method(self):
        ...
