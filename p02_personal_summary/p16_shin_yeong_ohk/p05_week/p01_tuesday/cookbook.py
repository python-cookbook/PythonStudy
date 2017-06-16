6월 13일
===============================================================================
#7.8 인자를 N개 받는 함수를 더 적은 인자로 사용
#파이썬 코드에 콜백 함수나 핸들러로 사용할 호출체가 있다.
#하지만 함수의 인자가 너무 많고 호출했을 때 예외가 발생한다,
#함수의 인자 개수를 줄이려면 functools.partial()을 사용해야 한다,
#partial() 함수를 사용하면 함수의 인자에 고장 값을 할당할 수 있고,
#따라서 호출할 때 넣어야 하는 인자 수를 줄일 수 있다.

EX1>
def spam(a, b, c, d):
    print(a, b, c, d)
#partial()로 특정 값 고정
from functools import partial
s1 = partial(spam,1)    # a=1
s1(2,3,4)
#1 2 3 4

s1(4,5,6)
#1 4 5 6

s2 = partial(spam, d=42)    # d=42
s2(1,2,3)
#1 2 3 42

s2(4,5,6)
#4 5 6 42

s3=partial(spam, 1, 2, d=42) # a=1, b=2, d=42
s3(3)
#1 2 3 42

s3(4)
#1 2 4 42

s3(5)
#1 2 5 42


#partial()이 특정 인자의 값을 고정하고 새로운 호출체를 반환한다.
#새로운 호출에는 할당하지 않은 인자를 받고, partial()에 주어진 인자와 합친 후 원본 함수에 전달

#겉으로 보기에 호환되지 않을 것 같은 코드를 함께 동작하도록 하는 문제
#우선 (x,y) 튜플로 나타낸 좌표 리스트
#다음 함수를 사용해서 두 점 사이의 거리 구하기
EX2>
points = [ (1,2), (3,4), (5,6), (7,8) ]

import math
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)
#어떤 점에서부터 이 점까지의 거리에 따라 정렬하기
#리스트의 sort() 메소드는 key인자를 바아서 정렬에 사용하지만 인자가 하나인 함수에만 동작
#따라서 distance()는 적당하지 X

EX2_1>
pt = (4,3)
points.sort(key=partial(distance,pt))
points
#[(3, 4), (1, 2), (5, 6), (7, 8)]
===============================================================================





===============================================================================
#7.9 메소드가 하나인 클래스를 함수로 치환
#__init__() 외에 메소드가 하나뿐인 클래스가 있는데, 코드를 간결하게 만들기 위해 하나로 만들기
#많은 경우 메소드가 하나뿐인 클래스는 클로저를 사용해서 함수로 바꿀 수 있다.
#템플릿 스킴을 사용해서 URL을 뽑아내는 클래스를 예로 들면,
EX1>
from urllib.request import urlopen

class UrlTemplate:
    def __init__(self, template):
        self.template = template
    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

# 사용법. 야후(yahoo)에서 주식 데이터를 받는다.
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))
    
EX1_1>
#더 간단하게 치환
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# 사용법
yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))
===============================================================================    





===============================================================================
#7.10 콜백 함수에 추가적 상태 넣기
#콜백 함수를 사용하는 코드를 작성중(이벤트 핸들러, 완료 콜백 등)
#콜백 함수에 추가 상태를 넣고 내부 호출에 사용
#많은 라이브러리와 프레임워크(특히 비동기 처리에 관련 있는)에서 찾을 수 있는 콜백 함수의 활용

EX1>
def apply_async(func, args, *, callback):
    #결과 계산
    result = func(*args)
    
    #결과 값으로 콜백 함수 호출
    callback(result)
    

#코드 사용 예제
def print_result(result):
    print('Got:',result)

def add(x,y):
    return x + y

apply_async(add, (2, 3), callback=print_result)
#Got: 5
apply_async(add, ('hello', 'world'), callback=print_result)
#Got: helloworld

#print_result() 함수는 결과 값만 하나의 인자로 받는다.
#다른 어떠한 정보도 전달 받지 않는다.
#부족한 정보로 인해 콜백 함수가 다른 변수나 환경 등과 통신할 때 문제 발생
#콜백 함수에 추가 정보를 넣는 한 가지 방법은 하나의 함수 대신
#바운드-메소드를 사용
EX2>
class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))
        
#사용법 : 인스턴스 만들고 바운드 메소드 handler를 콜백으로 사용
r = ResultHandler()
apply_async(add, (2, 3), callback=r.handler)
#[1] Got: 5

apply_async(add, ('hello', 'world'), callback=r.handler)
#[2] Got: helloworld

 
EX3>
#클래스의 대안으로 클로저를 사용해서 상태를 저장
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler

handler = make_handler()
apply_async(add, (2, 3), callback=handler)
#[1] Got: 5
apply_async(add, ('hello', 'world'), callback=handler)
#[2] Got: helloworld


#코루틴 사용
EX4>
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
        
#코루틴의 경우에는 콜백으로 send() 메소드 사용
handler = make_handler()
next(handler)   #Advance to the yield
apply_async(add, (2, 3), callback=handler.send)
#[1] Got: 5
apply_async(add, ('hello', 'world'), callback=handler.send)
#[2] Got: helloworld

 
# 추가적인 인자와 파셜 함수 애플리케이션으로 콜백에 상태 넣기
EX5>
class SequenceNo:
    def __init__(self):
        self.sequence = 0
    
    def handler(result, seq):
        seq.sequence += 1
        print('[{}] Got: {}'.format(seq.sequence, result))
    
seq = SequenceNo()
from functools import partial
apply_async(add, (2, 3), callback=partial(handler, seq=seq))
#Traceback (most recent call last):
  #File "<ipython-input-16-8bdef16c3961>", line 12, in <module>
   # apply_async(add, (2, 3), callback=partial(handler, seq=seq))
#TypeError: the first argument must be callable
apply_async(add, ('hello', 'world'), callback=partial(handler, seq=seq))
#Traceback (most recent call last):
  #File "<ipython-input-16-8bdef16c3961>", line 12, in <module>
   # apply_async(add, (2, 3), callback=partial(handler, seq=seq))
#TypeError: the first argument must be callable
===============================================================================





===============================================================================
#7.11 인라인 콜백 함수
#콜백 함수를 사용하는 코드를 작성하는데, 크기가 작은 함수를 너무 많이 만들까봐 걱정될 때

EX1>
#제너레이터와 코루틴 사용
#어떤 작업을 하고 콜백을 호출하는 코드
def apply_async(func, args, *, callback):
    #결과 계산
    result = func(*args)
    
    #결과 값으로 콜백 함수 호출
    callback(result)

#Async 클래스와 inlined_async 데코레이터를 포함하고 있는 지원 코드
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
    
#두 개의 코드 조각이 있으면 yield 구문으로 콜백 단계를 인라인할 수 있다.
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
===============================================================================







===============================================================================
#7.12 클로저 내부에서 정의한 변수에 접근
#클로저는 확장해서 내부 변수에 접근하고 수정하기
#일반적으로 클로저 내부 변수는 외부와 완전히 단절
#하지만 접근 함수를 만들고 클로저에 함수 속성으로 붙이면 내부 변수에 접근 가능
EX1>
def sample():
    n = 0

    #클로저 함수
    def func():
        print('n=', n)

        #n에 대한 접근 메소드
        def get_n():
            return n
        
        def set_n(value):
            nonlocal n
            n = value

        #함수 속성으로 클로저에 붙임
        func.get_n = get_n
        func.set_n = set_n
        return func

#사용법
f = sample()
f()
#'NoneType' object is not callable


f.set_n(10)
f()
#AttributeError: 'NoneType' object has no attribute 'set_n'

f.get_n()
#AttributeError: 'NoneType' object has no attribute 'get_n'


#nonlocal 선언으로 내부 변수를 수정하는 함수
#접근 메소드를 클로저 함수에 붙여 인스턴스 메소드인 것처럼 동작하는 것 (클래스와 연관 X)

#클로저를 마치 클래스의 인스턴스인 것처럼 동작하게 만들기
#내부 함수를 인스턴스 딕셔너리에 복사하고 반환하기
EX1>
import sys
class ClosureInstance:
    def __init__(self, locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals

            #인스턴스 딕셔너리를 호출체로 갱신
        self.__dict__.update((key,value) for key, value in locals.items() if callable(value) )

    #특별 메소드 리다이렉트(redirect)
    def __len__(self):
        return self.__dict__['__len__']()
    
#사용 예제
def Stack():
    items = []
    def push(item):
        items.append(item)
    def pop():
        return items.pop()
    def __len__():
        return len(items)
    return ClosureInstance()

#실제 동작하는 세션
s = Stack()
s
#<__main__.ClosureInstance at 0x268a69524a8>

s.push(10)
s.push(20)
s.push('Hello')
len(s)
#4

s.pop()
#'Hello'
s.pop()
#20
s.pop()
#10
===============================================================================







CHAPTER. 클래스와 객체
===============================================================================
#8.1 인스턴스의 문자열 표현식 변형
#인스턴스를 출력하거나 볼 때 생성되는 결과물을 좀 더 보기좋게 바꾸기
#"__str__()" "__repr()__()" 메소드
EX1>
class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)
    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)

#__repr__() 메소드는 인스턴스의 코드 표현식을 반환하고 일반적으로 인스턴스를 재생성할 때 입력하는 텍스트
#내장 repr() 함수는 인터프리터에서 값을 조사할 때와 마찬가지로 이 텍스트를 반환
#__str__() 메소드는 인스턴스를 문자열로 변환하고
#str() 와 print() 함수가 출력하는 결과가 된다,

p = Pair(3, 4)
p
#Pair(3, 4)
print(p)
#(3, 4)

#서식화에서 문자열 표혆식이 어떻게 다른지
#특히 서식화 코드는 !r은 기본값으로 __str__() 대신 __repr__()를 사용해야 함을 의미
EX2>
p = Pair(3, 4)
print('p is {0!r}'.format(p))
#p is Pair(3, 4)

print('p is {0}'.format(p))
#p is (3, 4)
===============================================================================







===============================================================================
#8.2 문자열 서식화 조절
#format() 함수와 문자열 메소드로 사용자가 정의한 서식화를 지원하기
#__format__() 메소드

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

#Date 클래스의 인스턴스는 아래와 같은 서식화 지원
d = Date(2012, 12, 21)
format(d)
#'2012-12-21'
format(d, 'mdy')
#'12/21/2012'
'The date is {:ymd}'.format(d)
#'The date is 2012-12-21'
'The date is {:mdy}'.format(d)
#'The date is 12/21/2012'
===============================================================================






===============================================================================
#8.3 객체의 콘텍스트 관리 프로토콜 지원
#객체가 with 구문을 지우너하게 만들기
#객체와 with 구문을 함께 사용할 수 있게 만들려면,
#__enter__()와 __exit__() 메소드

EX1>
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
    
#위 클래스의 주요 기능은 네트어크 연결을 표현하는 것이지만 처음에는 아무런 작업을 하지 않는다.(실제 연결 등)
#그 대신 연결은 WITH 구문에서 이루어진다.
from functools import partial
conn = LazyConnection(('www.python.org', 80))
# 연결 종료
with conn as s:
    # conn.__enter__() 실행 : 연결
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() 실행 : 연결 종료
===============================================================================






===============================================================================
#8.4 인스턴스를 많이 생성할 때 메모리 절약
#프로그램에서 많은(수백만) 인스턴스를 생성하고 메모리를 많이 소비할 때
#간단한 자료 구조 역할을 하는 클래스의 경우
#__slot__() 속성을 클래스 정의에 추가하면 메모리 사용 많이 절약
EX1>
class Date:
    __slots__=['year','month','day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day =day

#__slot__()을 정의하면 파이썬은 인스턴스에서 훨씬 더 압축된 내부 표현식을 사용한다,
#인스턴스마다 딕셔너리를 구성하지 않고 튜플이나 리스트같은 부피가 작은 고정 배열로 인스턴스가 만들어진다.
#__slots__() 명시자에 리스팅된 속성 이름은 내부적으로 이 배열의 특정 인덱스에 매핑된다.
#슬롯을 사용하는 데서 발생하는 부작용은 인스턴스에 새로운 속성을 추가할 수 없다는 점이다.
#__slots__() 명시자에 나열한 속상만 사용할 수 있다는 제약이 생긴다.
===============================================================================

          
          
          
          
          

===============================================================================
#8.5 클래스 이름의 캡슐화
#클래스 인스턴스의 "프라이빗" 데이터를 캡슐화하고 싶지만, 파이썬에는 접근 제어 기능이 부족하다.

#파이썬 프로그래머들은 언어의 기능에 의존하기보다는 데이터나 메소드의 이름에 특정 규칙을 사용하여서 의도를 나타낸다.
#첫번째 규칙은 밑줄(_)로 시작하는 모든 이름은 내부 구현에서만 사용하도록 가정하는 것

EX1>
class A:
    def __init__(self):
        self._internal = 0   #내부 속성
        self.public = 1     #공용 속성
    
    def public_method(self):
        '''
        A public method
        '''
        ...
    
    def _internal_mothod(self):
        ...
        
# 파이썬은 내부 이름에 누군가 접근하는 것을 실제로 막지는 않는다.
#하지만 이런 시도는 무례한 것으로 간주되고 결국 허술한 코드가 된다,
#또한 이름 앞에 밑줄을 붙이는 것은 모듈 이름과 모듈 레벨 함수에도 사용한다,
#예를 들어, 밑줄로 시작하는 모듈 일므을 발견한다면 (ex. _socket)은 내부 구현이다.
#또한 sys._getframe()과 같은 모듈 레벨 함수는 사용할 때 조심하기

#클래스 정의에 밑주ㅠㄹ 두 개(__)로 시작하는 이름이 나오기도 한다.
EX2>
class B:
    def __init__(self):
        self.__private = 0
    def __private_method(self):
        ...
    def public_method(self):
        ...
        self.__private_method()
        ...
                 
#이름 앞에 밑줄을 두 개 붙이면 일므이 다른 것으로 변한다.
#더 구체적으로 앞에 나온 클래스의 프라이빗 속성은 _B__private과 _B__private__method로 이름이 변한다.
#이름 변화의 의미는 "속성"
#속성은 속성을 통해 오버라이드할 수 없다.
EX3>
class C(B):
    def __init__(self):
        super().__init__()
        self.__private = 1  #B.__private를 오버라이드하지 않는다.
    # B.__private_method()를 오버라이드하지 않는다.
    def __private_method(self):
        ...

# 위에서 __private와 __private_method의 이름은 _C__private과 _C__private_method로 변하기 때문에
#B클래스의 이름과 겹치지 않는다.
===============================================================================