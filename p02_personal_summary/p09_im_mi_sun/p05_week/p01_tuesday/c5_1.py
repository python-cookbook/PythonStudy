###############7.8 인자 N개를 받는 함수를 더 적은 인자로 사용
# 파이썬 코드에 콜백 함수나 핸들러로 사용할 호출체가 있음 근데 함수의 인자가 너무 많고 호출했을 때 예외생
# 함수 인자 개수 축소 : functools.partial() 함수의 인자에 고정값 할당 인자수를 줄일 수 있음
def spam(a,b,c,d):
    print(a,b,c,d)

from functools import partial
s1 = partial(spam,1) #처음오는게 a, b, c...
s1(2,3,4) #1 2 3 4
s1(4,5,6) #1 4 5 6
s2 = partial(spam,d=42) #지정도 가능
s2(1,2,3) #1 2 3 42
s2(4,5,5) # 4 5 5 42
s3 = partial(spam,1,2,d=42)
s3(3) # 1 2 3 42
s3(4) #1 2 4 42
s3(5) #1 2 5 42

#partial(): 특정 인자 값을 고정하고 새로운 호출체를 반환
#할당하지 않은 인자를 받고 partial()에 주어진 인자와 합친 후 원본 함수에 전달

#호환되지 않을 것 같은 코드를 함께 동작하도록 도와줌
#두점 사이의 거리를 구할 수 있음
points = [ (1,2),(3,4),(5,6),(7,8)]
import math
def distance(p1,p2):
    x1, y1 =p1
    x2, y2 = p2
    return math.hypot(x2-x1, y2-y1)

#어떤 점에서부터 이점 까지의 거리에 따라 정렬을 해야하는 경우
#리스트의 sort() 메소드는 key인자를 받아 정렬에 사용 but, 인자가 하나인 함수에만 동작
#partial()
pt = (4,3)
points.sort(key=partial(distance,pt))
points

def output_result(result,log=None):
    if log is not None:
        log.debug('Got:%r', result)

#샘플함수
def add(x,y):
    return x+y

if __name__ == '__main__':
    import logging
    from multiprocessing import pool
    from functools import partial

    logging.basicConfig(level=logging.DEBUG)
    log=logging.getLogger('test')

    p = Pool()
    p.apply_async(add,(3,4), callback=partial(output_result,log=log))
    p.close()
    p.join()

from socketserver import StreamRequestHandler, TCPServer
class EchoHandler(StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'Got:'+line)

serv = TCPServer(('',15000), EchoHandler)
serv.serve_forerver()

class EchoHandler(StreamRequestHandler):
    #ack는 키워드로만 넣을수있는 인자
    # *args, **kwargs는 그 외 일반적인 파라미터
    def __init__(self, *args, ack, **kwargs):
        self.ack=ack
        super().__init__(*args, **kwargs)
    def handle(self):
        for line in self.rfile:
            self.wfile.write(self.ack + line)

#실행하면 오류 발생
#partial() 사용해서 ack에 인자값 넣어주면 해결
from functools import partial
serv = TCPSErver(('',15000),partial(EchoHandler,ack=b'RECIEVED:'))
serv.serve_forerver()
# 키워드로만 넣을 수 있는 인자라서 __init__() 메소드에 ack를 명시 (7.2)

#partial기능을 lambda로도 표현하기도 함 근데 partial이 의도 파악이 쉬우니까 이거 쓰셈
points.sort(key=lambda p:distance(pt,p))
p.apply_async(add, (3,4), callback = lambda result : output_result(result,log))
serv = TCPServer(('',15000), lambda *args, **kwargs : EchoHandler(*args, ack=b'RECEIVED:',**kwargs))




###############7.9 메소드가 하나인 클래스를 함수로 치환
#__init__()외에 메소드가 하나뿐인 클래스는 클로저를 사용해서 함수로 만들 수 있음

from urllib.request import urlopen
class UrlTemplate:
    def __init__(self, template):
        self.template = template
    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))
#사용법 아휴에서 주식 데이터를 받음
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))

#클래스를 함수로 치환할 수 있음
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

#사용법
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))

#대개의 경우 메소드가 하나뿐인 클래스가 필요할 때는 추가적인 상태를 메소드에 저장할 때 뿐
#UrlTemplate의 목적은 open()메소드에서 사용하기 위해 template 값을 저장해 놓으려는 것 뿐
#클로저는 단순히 함수처럼 보일 수 있지만 정의할 때의 환경을 기억함
#opener() 함수가 template 인자의 값을 기억하고 추후 호출에 사용


###############7.10 콜백 함수에 추가적 상태 넣기
#콜백 함수를 사용하는 코드를 작성 중(이벤트 핸들러 완료 콜백 등
# 콜백 함수에 추가 상태를 넣고 내부 호출에 사용하고 싶음

#많은 라이브러리와 프레임워크에서 찾을 수 있는 콜백 함수 활용법

def apply_async(func, args, *, callback):
    # 결과계산
    result = func(*args)
    #결과 값으로 콜백 함수 호출
    callback(result)

#예제
def print_result(result):
    print('Got:',result)

def add(x,y):
    return x+y
apply_async(add,(2,3),callback=print_result)
apply_async(add, ('hello','world'),callback=print_result)
#print_result()함수는 결과 값만 하나의 인자로 받음
#부족한 정보로 인해 콜백함수가 다른 변수나 환경 등과 통신할 때 문제가 발생하기도 함

#콜백함수에 추가 정보를 넣기 위한 방법으로 하나의 함수 대신 bound-method사용
#예를 들어 이 클래스는 겨로가값으 받을 때마다 늘어나는 내부 시퀀스 숫자를 지니고 있음
class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))

#클래스 사용을 위해 인스턴스 생성 후 바운드 메소드 handler를 콜백으로 사용해야 함
r = ResultHandler()
apply_async(add, (2, 3), callback=r.handler)
apply_async(add, ('hello', 'world'), callback=r.handler)

#2)클래스의 대안으로 클로저를 사용해서 상태를 저장해도 됨
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler

#예제
handler = make_handler()
apply_async(add, (2, 3), callback=handler)
apply_async(add, ('hello', 'world'), callback=handler)

#3)코루틴 사용
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
#코루틴의 경우 콜백으로 send()메소드 사용
handler = make_handler()
next(handler)
apply_async(add, (2, 3), callback=handler.send)
apply_async(add, ('hello', 'world'), callback=handler.send)

#4)추가적 인자와 파셜함수 애플리케이션
class SequenceNo:
    def __init__(self):
        self.sequence = 0

def handler(result, seq):
    seq.sequence += 1
    print('[{}] Got: {}'.format(seq.sequence, result))

seq = SequenceNo()
from functools import partial
apply_async(add, (2, 3), callback=partial(handler, seq=seq))
apply_async(add, ('hello', 'world'), callback=partial(handler, seq=seq))

#[토론]
apply_async(add, (2, 3), callback=lambda r: handler(r, seq))



####7.11 인라인 콜백 함수
#크기가 작은 함수를 너무 만들거 같음
#코드가 절차적 단계를 거치게 하고 싶음
#generator, coroutine 사용

def apply_async(func, args, *, callback):
    # 결과 계산
    result = func(*args)

    #결과 값으로 콜백 함수 호출
    callback(result)

#async 클래스와 inlined_async데로레이터를 포함하고 있는 지원코드
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

#두개의 코드 조각이 있으면 yield구문으로 콜백단계를 인라인 할 수 있음
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

###test() 호출하면 결과가 나옴
#특별 데코레이터와 yield를 제외하고는 아무런 콜백함수가 나타나지 않음

#[토론]
#inline_async() 데코레이터 함수!!
#키포인트는 데코레이터가 yield 구문을 통해 제너레이터 함수를 하나씩 돈다는것
#이를 위해 결과를 큐로 만들고 최소로 None을 넣음
#순환문을 돌며 결과를 큐에서 꺼내 제너레이터로 보냄
# 다음 생성으로 넘어가고 Async인스턴스를 받음
#순환문은 함수와 인자를 보고 비동기 계산인 apply_async()를 시작
# ==> 일반적인 콜백 함수 사용이 아니라 콜백이 큐 put()에 설정된거임!!!

if __name__ == '__main__':
    import multiprocessing
    pool = multiprocessing.Pool()
    apply_async = pool.apply_async
        # 테스트 함수 실행
    test()

####### 7.12 클로저 내부에서 정의한 변수에 접근
# 클로저는 확장해서 내부 변수에 접근하고 수정하고 싶음
#클로저 내부변수는 외부와 완전히 단절되어 있음
#접근함수를 만들고 클로저에 함수 속성으로 붙이면 내부 변수에 접근 가능

def sample():
    n=0
    #클로저 함수
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
#사용법
f = sample()
f()
f.set_n(10)
f()
f.get_n()

#1)nonlocal선언으로 내부 변수를 수정하는 함수 작성
#2)접근 메소드를 클로저 함수에 붙여 마치 인스턴스 메소드인 것처럼 동작(클래스와는 아무 상관x)

#클로저를 마치 클래스의 인스턴스인 것처럼 동작하게 만들 수 있음
#내부 함수를 인스턴스 딕셔너리에 복사하고 반환하기만 하면 됨
import sys
class ClosureInstance:
    def __init__(self, locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals
            # 인스턴스 딕셔너리를 호출체로 갱신
        self.__dict__.update((key,value) for key, value in locals.items() if callable(value) )
    # 특별 메소드 리다이렉트
    def __len__(self):
        return self.__dict__['__len__']()
# 사용예제
def Stack():
    items = []
    def push(item):
        items.append(item)
    def pop():
        return items.pop()
    def __len__():
        return len(items)
    return ClosureInstance()

#실제 동작을 보여주는 세션
s = Stack()
s
s.push(10)
s.push(20)
s.push('Hello')
len(s)
s.pop()

#위에 실행한게 클래스 정의보다 속도가 빠름
#아래는 클래스 속도 비교
class Stack2:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def __len__(self):
        return len(self.items)

#실행결과는 유사하게 나옴
from timeit import timeit
#클로저
s = Stack()
timeit('s.push(1);s.pop()', 'from __main__ import s')
s = Stack2()
timeit('s.push(1);s.pop()', 'from __main__ import s')

#클로저 실행속도가 약 8%빠름
#추가적인 self변수를 사용하지 앟아서 클로저의 실행속도가 더 빠름
#....구냥 스킵 뭔소리야


####chap8. 클래스와 객체
#일반적인 파이썬 기능을 객체가 지원하도록 하기
#특별메소드 사용
#캡슐화 기술
#상속
#메모리관리
#유용한 디자인 패턴
########8.1 인스턴스의 문자열 표현식 변형
#인스턴스 출력or열람 시 생성되는 결과물을 바꾸고 싶음
# __str() / __repr()__
class Pair:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)
    def __str__(self):
        return '({0.x!s},{0.y!s})'.format(self)

#__repr() 메소드는 인스턴스 코드 표현식 반환 일바넉으로 인스턴스를 재생성할 때 입력하는 텍스트
#내장 repr() 함수는 인터프리터에서 값을 조사할 때와 마찬가지로 텍스트 반환
#__str__() 인스턴스를 문자열로 반환 str()/print()함수가 출력하는 결과가 됨
p = Pair(3,4)
p #Pair(3,4) #__repr__() 결과
print(p) #(3,4) #__str__() 결과

#서식화 코드 !r은 기본값으로 __str()__대신 __repr__()을 사용해야함

p=Pair(3,4)
print('p is {0!r}'.format(p)) #p is Pair(3, 4)
print('p is {0}'.format(p)) #p is (3,4)

#__repr__()와 __str__()를 정의하면 디버기과 인스턴스 출력을 간소화함
# 출력이나 인스턴스 로깅 시에도 유용한 정보르 얻을 ㅅ 있음

#__repr__(): eval(repr(x)) == x 와 같은 텍스트를 만드는 것이 표준
#원하지 않을 경우 <>사이에 텍스트 추가
f = open('file.dat')
f
#__str__()를 정의하지 않으면 __repr__()의 결과물 사용
# #{0.x}는 인자 0의 x속성 명시

#다음에서는 실제로 인스턴스 self를 의미
def __repr__(self):
    return 'Pair({0.x!r}, {0.y!r})'.format(self)
#대안으로 %연산자와 다음 코드 사용
def __repr__(self):
    return 'Pair(%r,%r)' % (self.x, self.y)

########8.2 문자의 서식화 조절
#format()함수와 문자열 메소드로 사용자가 정의한 서식화 지원이 필요함
#클래스에 __format__()메소드 정의
_formats = {
    'ymd' : '{d.year}-{d.month}-{d.day}',
    'mdy' : '{d.month}/{d.day}/{d.year}',
    'dmy' : '{d.day}/{d.month}/{d.year}'
}

class Date:
    def __init__(self, year, month, day) :
        self.year = year
        self.month = month
        self.day= day

    def __format__(self,code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)

d = Date(2012,12,21)
format(d) #'2012-12-21'
format(d,'mdy') #'12/21/2012'
'the date is {:ymd}'.format(d) #'the date is 2012-12-21'
'the date is {:mdy}'.format(d) #the date is 12/21/2012'

#__format__()메소드는 파이썬 문자열 서식화 함수에 hook(후크)를 제공
# 서식화 코드의 해석은 모두 클래스 자체에 달려있음
#코드에는 거의 모든 내용이 올 수 있음

from datetime import date
d = date(2012,12,21)
format(d) #'2012-12-21'
format(d, '%A,%B %d,%Y') #'Friday,December 21,2012' ## A: 요일 , B: 달, C: 일, D: 달/일/연도 d:일
'the end is {:%d %b %Y}. Goodbye'.format(d) #'the end is 21 Dec 2012. Goodbye'
#내장 타입의 서식화는 어느정도 표준이 있음 자세한 내용은 string모듈의 문서 참고

#########8.3 개겣의 콘텍스트 관리 프로토콜 지원
#객채와 with구문 함께 사용
# __enter__(), __exit__() 메소드 구현

#네트워크 연결
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
#클래스의 주요 기능은 네트워크 연결을 표현하는 것이지만 처음에는 아무 작업을 하지 x(실제 연결x)
#그 대신 with구문에서 이루어짐
from functools import partial
conn=LazyConnection(('www.python.org',80))
#연결 종료
with conn as s:
    #conn.__enter__() 실행:연결
    s.send(b'Get /index.html HTTP/1.0\r\n')
    s.send(b'Host:www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    #conn.__exit__() 실행:연결 종료

#콘텍스트 매니저 ㅅ작성 시 중요한 원리는 with구문을 사용하여 정의된 블럭을 감싸는 코드를 작성해야함
#with을 만나면 __enter__()메소드 호출 --> __enter__()반환 값이 있으면 as로 나타낸 변수에 위치시킴
#-->with내부 명령어를 실행 --> __exit__() 메소드로 소거작업
#=> with내부에서 어떤 일이 발생하는 지와 상관없이 일어나고 예외가 발생해도 변함이 없음
#__exit__() 메소드의 세가지 인자에 예외타입 값 트레이스백이 들어있음
#__exit__()메소드는 예외 정보를 고르거나 아무일도 하지 않고 None을 방황하며 무시하는 방식을 선택할 수 있음

#__exit__()가 True반환하면 예외를 없애고 아무일도 일어나지 않았던 것처럼 with블록 다음의 프로그램을 계속해서 실행
# with문을 여러번 써서 중첩된 연결을 lazyconnection클래스가 허용하는지 여부가 미묘한 측면?
#하나의 소켓 연결만 허용되고 소켓을 사용중에 중복된 with문이 나타나면 예외 발생
#아래로 제한을 피해가셈

from socket import socket,AF_INET,SOCK_STREAM
class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.connection = []
    def __enter__(self):
        sock = socket(self.family, self.type)
        sock.connect(self.address)
        self.connections.append(sock)
        return sock
    def __exit__(self, exc_ty, exc_val, tb):
        self.connections.pop().close()
#사용예제
from functools import partial
conn = LazyConnection(('www.python.org',80))
with conn as s1:
    ...
    with conn as s2:
        ...#s1과 s2는 독립적 소켓

#lazyconnection클래스는 연결을 위한 팩토리 역할을 함
#내부적으로 스택을 위해 리스트를 사용함
#__enter__()가 실행될 때마다 새로운 연결을 만들고 스택에 추가함
#__exit__()메소드는 단순히 스택에서 마지막 연결을 꺼내고 닫는다
#중첩 with구문으로 연결을 여러개 생성할 수 있음
#먼소린지 모르겠어ㅠㅠ

########8.4 인스턴스를 많이 생성할 때 메모리 저약
#인스턴스를 수많이 생성하고 메모리 과소비
# 간단한 자료 구조 역항르 하는 클래스의 경우 __slots__ 속성을 클래스 정의에 추가
class Date:
    __slots__=['year','month','day']
    def __init__(self, year,month,day):
        self.year = year
        self.month = month
        self.day =day

#__slots__을 정의하면 파이썬은 인스턴스에서 훨씬 더 압축된 내부 표현식을 사용함
# 인스턴스마다 딕셔너리를 구성하지 않고 튜플이나 리스트 같은 부피가 작은 고정 배열로 인스턴스 생성
# __slots__ 명시자에 리스팅된 속성 이름은 내부적으로 특정 인덱스에 매핑됨
#슬롯을 사용하는 데서 발생한 부작용은 인스턴스에 새로운 속성을 추가할 수 없음
#__slots__명시자에 나열한 속성만 사용할 수 있다는 제약이 생김

#슬롯을 사용해서 절약하는 메모리는 속성의 숫자와 타입에 따라 다른다
#Data 인스턴스 하나를 슬롯 없이 저장하면 64비트 파이썬에서 428qkdlxm thql
#슬롯 사용하면 156바이트로 떨어짐
#대개의 코드에서 슬롯 사용을 피하는 것이 좋음딕셔너리 기반 구현에 의존하는 부분이 많기 때문
#슬롯을 정의한 클래스는 다중 상속과 같은 특정 기능을 지원하지 않음
# 프로그램에서 자주 사용하는 자료 구조에만 슬롯 사용을 고려하는 것이 좋다
#__slots__은 항상 최적화 도구로만 사용해야함
