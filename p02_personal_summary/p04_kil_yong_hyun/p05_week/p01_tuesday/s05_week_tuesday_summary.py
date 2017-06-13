#  7.8 인자를 N개 받는 함수를 더 적은 인자로 사용
#  ▣ 문제 : 파이썬 코드에 콜백 함수나 핸들러로 사용할 호출체가 있다. 하지만 함수의 인자가 너무 많고 호출했을 때 예외가 발생한다.
#  ▣ 해결 : 함수의 인자 개수를 줄이려면 functools.partial() 을 사용해야 한다.
#            partial() 함수를 사용하면 함수의 인자에 고정 값을 할당할 수 있고, 따라서 호출할 때 넣어야 하는 인자 수를 줄일 수 있다.
def spam(a, b, c, d):
    print(a, b, c, d)


from functools import partial

s1 = partial(spam, 1)
s1(2, 3, 4)
s1(4, 5, 6)
s2 = partial(spam, d=42)
s2(1, 2, 3)
s2(4, 5, 5)
s3 = partial(spam, 1, 2, d=42)
s3(3)
s3(4)
s3(5)
#  ※ partial() 이 특정 인자의 값을 고정하고 새로운 호출체를 반환한다.
#     이 새로운 호출체는 할당하지 않은 인자를 받고, partial() 에 주어진 인자와 합친 후 원본 함수에 전달한다.

#  ▣ 토론 : 이번 레시피는 겉으로 보기에 호환되지 않을 것 같은 코드를 함께 동작하도록 하는 문제와 관련 있다.
#   - (x, y) 튜플로 나타낸 좌표 리스트가 있다. 다음 함수를 사용해서 두 점 사이의 거리를 구할 수 있다.
points = [(1, 2), (3, 4), (5, 6), (7, 8)]

import math


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)  # math.hypot(x, y) : 평면에서 두 점 사이의 직선 거리를 구하는 함수


pt = (4, 3)
points.sort(key=partial(distance, pt))
print(points)


#   - 이 발상을 확장해서, 다른 라이브러리에서 사용하는 콜백 함수의 매개변수 설명을 변경하는 데 partial() 을 사용할 수도 있다.
#     예를 들어 multiprocessing 을 사용해서 비동기식으로 결과를 계산하고, 결과 값과 로깅 인자를 받는 콜백 함수에 그 결과를 전달하는 코드가 있다.
def output_result(result, log=None):
    if log is not None:
        log.debug('Got : %r', result)


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
# ※ apply_async() 로 콜백 함수를 지원할 때, partial() 을 사용해서 추가적인 로깅 인자를 넣었다.
#     multiprocessing 은 하나의 값으로 콜백 함수를 호출하게 된다.

#   - 유사한 예제로 네트워크 서버를 작성한다고 생각해 보자.
#     socketserver 모듈을 사용하면 상대적으로 편하게 작업할 수 있다.
from socketserver import StreamRequestHandler, TCPServer


class EchoHandler(StreamRequestHandler):
    # ack 는 키워드로만 넣을 수 있는 인자이다.
    # *args, **kwargs 는 그 외 일반적인 파라미터이다.
    def __init__(self, *args, ack, **kwargs):
        self.ack = ack
        super().__init__(*args, **kwargs)

    def handle(self):
        for line in self.rfile:
            self.wfile.write(self.ack + line)


serv = TCPServer(('', 15000), partial(EchoHandler, ack=b'RECEIVED:'))
serv.serve_forever()

#   - partial() 의 기능을 lambda 표현식으로 대신하기도 한다.
points.sort(key=lambda p: distance(pt, p))
p.apply_async(add, (3, 4), callback=lambda result: output_result(result, log=log))
serv = TCPServer(('', 15000), lambda *args, **kwargs: EchoHandler(*args, ack=b'RECEIVED:', **kwargs))
#   ※ 이 코드도 동작하기는 하지만, 가독성이 떨어지고 나중에 소스 코드를 읽는 사람이 헷갈릴 확률이 더 크다.
#      partial() 을 사용하면 조금 더 작성자의 의도를 파악하기 쉽다.


#  7.9 메소드가 하나인 클래스를 함수로 치환
#  ▣ 문제 : __init__() 외에 메소드가 하나뿐인 클래스가 있는데, 코드를 간결하게 만들기 위해 이를 하나의 함수로 바꾸고 싶다.
#  ▣ 해결 : 많은 경우 메소드가 하나뿐인 클래스는 클로저를 사용해서 함수로 바꿀 수 있다.
#            템플릿 스킴을 사용해서 URL 을 뽑아 내는, 다음 클래스를 예로 들어 보자.
from urllib.request import urlopen


class UrlTemplate:
    def __init__(self, template):
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))


yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))


# - 클로저를 사용해서 함수로 변경
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))

    return opener


yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))


# ▣ 토론 : 대개의 경우 메소드가 하나뿐인 클래스가 필요할 때는 추가적인 상태를 메소드에 저장할 때뿐이다.
#            예를 들어 UrlTemplate 클래스의 목적은 open() 메소드에서 사용하기 위해 template 값을 저장해 놓으려는 것뿐이다.
#            단순히 생각해서 클로저는 함수라고 말할 수 있지만 함수 내부에서 사용하는 변수의 추가적인 환경이 있다.
#            클로저의 주요 기능은 정의할 때의 환경을 기억한다는 것이다.
#            따라서 앞의 예제에서 opener() 함수가 template 인자의 값을 기억하고 추후 호출에 사용한다.


#  7.10 콜백 함수에 추가적 상태 넣기
#  ▣ 문제 : 콜백 함수를 사용하는 코드를 작성 중이다.(이벤트 핸들러, 완료 콜백 등)
#            이때 콜백 함수에 추가 상태를 넣고 내부 호출에 사용하고 싶다.
#  ▣ 해결 : 이 레시피는 많은 라이브러리와 프레임워크에서 찾을 수 있는 콜백 함수의 활용을 알아본다.
#            예제를 위해 콜백 함수를 호출하는 다음 함수를 정의한다.
def apply_async(func, args, *, callback):
    result = func(*args)
    callback(result)


def print_result(result):
    print('Got:', result)


def add(x, y):
    return x + y


apply_async(add, (2, 3), callback=print_result)
apply_async(add, ('hello', 'world'), callback=print_result)


#   - 콜백 함수에 추가 정보를 넣는 한 가지 방법은 하나의 함수 대신 바운드-메소드를 사용하는 것이다.
#  ★ 바운드-메소드 : 자동으로 개체 인스턴스가 첫 번째 인자로 전달되는 함수.
class ResultHandler:
    def __init__(self):
        self.sequence = 0

    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))


r = ResultHandler()
apply_async(add, (2, 3), callback=r.handler)
apply_async(add, ('hello', 'world'), callback=r.handler)


#   - 클래스의 대안으로 클로저를 사용해서 상태를 저장해도 된다.
def make_handler():
    sequence = 0

    def handler(result):
        nonlocal sequence  # nonlocal : 특정 변수 이름에 할당할 때 스코프 탐색이 일어나야 함을 나타내는 키워드. (단, 모듈 수준 스코프까지 탐색할 수 없다.)
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))

    return handler


handler = make_handler()
apply_async(add, (2, 3), callback=handler)


#   - 코루틴(coroutine)을 사용할 수도 있다.
#  ★ coroutine : generator 와 반대되는 개념으로, generator 는 생산자이지만, coroutine 은 소비자 역할을 한다.
#                 따라서, yield 구문이 generator 와 반대로 입력으로 동작한다.
#                 coroutine 에서는 send('입력값') 메서드를 호출함으로써 입력을 수행한다.
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))


handler = make_handler()
next(handler)
apply_async(add, (2, 3), callback=handler.send)


#   - 마지막으로, 추가적인 인자와 partial function 어플리케이션으로 콜백에 상태를 넣을 수 있다.
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

#  ▣ 토론 : 콜백 함수를 사용하는 프로그램은 엉망으로 망가질 위험 요소를 안고 있다.
#            한 가지 문제점은 콜백 실행으로 이끄는 초기 요청 코드와 콜백 함수가 끊어진다는 점이다.
#            결과적으로 요청을 한 곳과 처리하는 곳이 서로를 찾지 못하게 된다.
#            콜백 함수가 여러 단계에 걸쳐 실행을 계속하도록 만들기 위해서는 어떻게 관련 상태를 저장하고 불러올지 정해야 한다.
#            상태를 고정시키고 저장하는 방식에는 크게 두 가지가 있다.
#             1). 인스턴스에 상태를 저장.
#             2). 클로저에 저장.
#            두 가지 기술 중에서는 함수에 기반해서 만드는 클로저가 조금 더 가볍고 자연스럽다.
#            그리고 클로저는 자동으로 사용하는 변수를 고정시키기 때문에, 저장해야 하는 정확한 상태를 걱정하지 않아도 된다.
#            클로저를 사용하면 수정 가능한 변수를 조심해서 사용해야 한다.
#            앞에 나온 예제에서 nonlocal 선언은 sequence 변수가 콜백 내부에서 수정됨을 가리킨다.
#            이 선언이 없으면 에러가 발생한다.
#            코루틴을 사용하면 단순히 하나의 함수로 이루어져 있기 때문에 더 깔끔하고 nonlocal 선언 없이도 자유롭게 변수를 수정할 수 있다.
#            코루틴의 잠재적 단점은 파이썬의 기능으로 받아들여지지 않을 때가 있다는 것이다.
#            또한 코루틴을 사용하기 전에 next() 를 호출해야 한다는 점도 있다.

#   - partial() 을 대신해서 lambda 로 해결하는 방법
apply_async(add, (2, 3), callback=lambda result: handler(result, seq))


#  7.11 인라인 콜백 함수
#  ▣ 문제 : 콜백 함수를 사용하는 코드를 작성하는데, 크기가 작은 함수를 너무 많이 만들어 낼까 걱정이 된다.
#            코드가 좀 더 정상적인 절차적 단계를 거치도록 하고 싶다.
#  ▣ 해결 : 제너레이터와 코루틴을 사용하면 콜백 함수를 함수 내부에 넣을 수 있다.
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
    @wraps(func)  # 원래 함수의 속성들이 사라지는 것을 방지하기 위해 사용되는 데코레이터
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


test()

#  ▣ 토론 : 이번 레시피를 통해 콜백 함수, 제너레이터, 컨트롤 플로우를 얼마나 잘 이해하고 있는지 알 수 있다.
#   1. 콜백과 관련 있는 코드에서 현재 연산이 모두 연기되고 특정 포인트에서 재시작한다는 점이 포인트이다.
#      연산이 재시작하면 프로세싱을 위해 콜백이 실행된다.
#      apply_async() 함수는 콜백 실행의 필수 부위를 보여주는데, 사실 실제 프로그램에서는 스레드, 프로세스, 이벤트 핸들러 등이
#      연관되면서 훨씬 복잡할 것이다.
#      프로그램 실행이 연기되고 재시작하는 발상은 자연스럽게 제너레이터 함수의 실행 모델과 매핑된다.
#      특히 yield 연산은 제너레이터 함수가 값을 분출하고 연기하도록 한다.
#      뒤이어 __next__() 나 send() 메소드를 호출하면 다시 실행된다.
#   2. inline_async() 데코레이터는 yield 구문을 통해 제너레이터 함수를 하나씩 수행한다.
#      이를 위해 결과 큐를 만들고 최소로 None 을 넣은다음 순환문을 돌며 결과를 큐에서 꺼내 제너레이터로 보낸다.
#      여기서 다음 생성으로 넘어가고 Async 인스턴스를 받는다.
#      순환문은 함수와 인자를 보고 비동기 계산인 apply_async() 를 시작한다.
#      여기서 가장 주의해야 할 부분은 이 동작이 일반적인 콜백 함수를 사용해서 이루어진 것이 아니라, 콜백이 큐 put() 메소드에 설정되었다는 것이다.
#   3. 메인 루프는 즉시 최상단으로 돌아가고 큐의 get() 을 실행한다.
#      데이터가 있으면 put() 콜백이 넣은 결과일 것이다.
#      아무것도 없다면 연산이 멈추었고, 결과 값이 도착하길 기다리고 있는 것이다.
#      실행 결과는 apply_async() 함수의 정확한 구현에 따라 달라진다.

#   - 멀티프로세싱 라이브러리와 비동기 연산을 사용해 여러 프로세스에서 실행하는 방법
if __name__ == '__main__':
    import multiprocessing

    pool = multiprocessing.Pool()
    apply_async = pool.apply_async

    test()


# ※ 복잡한 컨트롤 플로우를 제너레이터 함수에 숨기는 것은 표준 라이브러리와 서드파티 패키지에서 쉽게 찾을 수 있다.
#     예를 들어 contextlib 의 @contextmanager 데코레이터는 yield 구문을 통해 시작점과 종료점을 하나로 합치는 트릭을 수행한다.
#     유명한 패키지인 Twisted package 에도 유사한 콜백이 포함되어 있다.


#  7.12 클로저 내부에서 정의한 변수에 접근
#  ▣ 문제 : 클로저는 확장해서 내부 변수에 접근하고 수정하고 싶다.
#  ▣ 해결 : 일반적으로 클로저 내부 변수는 외부와 완전히 단절되어 있다.
#            하지만 접근 함수를 만들고 클로저에 함수 속성으로 붙이면 내부 변수에 접근할 수 있다.
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
print(f.get_n())

#  ▣ 토론 : 이번 레시피를 이루는 두 가지 주요 기능이 있다.
#            1. nonlocal 선언으로 내부 변수를 수정하는 함수를 작성하는 것.
#            2. 접근 메소드를 클로저 함수에 붙여 마치 인스턴스 메소드인 것처럼 동작하는 것.

#   - 클로저를 클래스의 인스턴스인 것처럼 동작하게 하는 방법.
import sys


class ClosureInstance:
    def __init__(self, locals=None):
        if locals is None:
            # sys._getframe(n) : n 단계 전의 프레임을 가져온다.
            # sys._getframe(n).f_code.co_name : n 단계 전의 프레임에서 함수 이름을 얻는다.
            # sys._getframe(n).f_locals : n 단계 전의 해당 프레임의 지역 변수를 얻는다.
            locals = sys._getframe(1).f_locals

        # 인스턴스 딕셔너리를 호출체로 갱신
        self.__dict__.update((key, value) for key, value in locals.items() if callable(value))

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
print(len(s))  # Stack 클로저 내의 __len__() 함수를 호출
print(s.pop())
print(s.pop())
print(s.pop())


#   - 위의 클로저를 이용한 코드가 일반 클래스 정의보다 실행 속도가 더 빠르다.
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


# Chapter 8. 클래스와 객체
#  8.1 인스턴스의 문자열 표현식 변형
#  ▣ 문제 : 인스턴스를 출력하거나 볼 때 생성되는 결과물을 좀 더 보기 좋게 바꾸고 싶다.
#  ▣ 해결 : 인스턴스의 문자열 표현식을 바꾸려면 __str__() 와 __repr__() 메소드를 정의한다.
class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)  # 0.x : 인자 0의 x 속성, !r : __repr__()

    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)  # 0.x : 인자 0의 x 속성, !s : __str__()

#  ※ __repr__() 메소드는 인스턴스의 코드 표현식을 반환하고, 일반적으로 인스턴스를 재생성할 때 입력하는 텍스트이다.
#     내장 repr() 함수는 인터프리터에서 값을 조사할 때와 마찬가지로 이 텍스트를 반환한다.
#     __str__() 메소드는 인스턴스를 문자열로 반환하고, str() 와 print() 함수가 출력하는 결과가 된다.
p = Pair(3, 4)
p
print(p)

print('p is {0!r}'.format(p))
print('p is {0}'.format(p))

#  ▣ 토론 : __repr__() 와 __str__() 를 정의하면 디버깅과 인스턴스 출력을 간소화한다.
#            __repr__() 는 eval(repr(x)) == x 와 같은 텍스트를 만드는 것이 표준이다.
#            이것을 원하지 않거나 불가능하다면 일반적으로 <와> 사이에 텍스트를 넣는다.
f = open('PythonCookBook/files/somefile.txt')
f  # <_io.TextIOWrapper name='PythonCookBook/files/somefile.txt' mode='r' encoding='cp949'>

#   - __str__() 를 정의하지 않으면 대신 __repr__() 의 결과물을 사용한다.
def __repr__(self):
    return 'Pair({0.x!r}, {0.y!r}'.format(self)  # 여기에서 0 은 인스턴스 self 를 의미

#   - % 연산자를 이용하는 방법
def __repr__(self):
    return 'Pair(%r, %r)' % (self.x, self.y)


#  8.2 문자열 서식화 조절
#  ▣ 문제 : format() 함수와 문자열 메소드로 사용자가 정의한 서식화를 지원하고 싶다.
#  ▣ 해결 : 문자열 서식화를 조절하고 싶으면 클래스에 __format__() 메소드를 정의한다.
_formats = {'ymd': '{d.year}-{d.month}-{d.day}',
            'mdy': '{d.month}/{d.day}/{d.year}',
            'dmy': '{d.day}/{d.month}/{d.year}'}

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
print(format(d, 'mdy'))
print('The date is {:ymd}'.format(d))
print('The date is {:mdy}'.format(d))

#  ▣ 토론 : __format__() 메소드는 파이썬의 문자열 서식화 함수에 hook 를 제공한다.
#            서식화 코드의 해석은 모두 클래스 자체에 달려있다는 점이 중요하다.
#            따라서 코드에는 거의 모든 내용이 올 수 있다. 예를 들어 다음 datetime 모듈을 보자.
from datetime import date
d = date(2012, 12, 21)
print(format(d))
print(format(d, '%A, %B, %d, %Y'))
print('The end is {:%d %b %Y}. Goodbye'.format(d))


#  8.3 객체의 콘텍스트 관리 프로토콜 지원
#  ▣ 문제 : 객체가 콘텍스트 관리 프로토콜(with 구문)을 지원하게 만들고 싶다.
#  ▣ 해결 : 객체와 with 구문을 함께 사용할 수 있게 만들려면, __enter__() 와 __exit__() 메소드를 구현해야 한다.
from socket import socket, AF_INET, SOCK_STREAM
from functools import partial

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

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()
        self.sock = None

conn = LazyConnection(('www.python.org', 80))

with conn as s:  # 컨텍스트 관리 프로토콜
    # conn.__enter__() 실행: 연결
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() 실행: 연결 종료

#  ▣ 토론 : 컨텍스트 매니저를 작성할 때 중요한 원리는 with 구문을 사용하여 정의된 블럭을 감싸는 코드를 작성한다는 것이다.
#           처음으로 with 를 만나면 __enter__() 메소드가 호출된다.
#           __enter__() 의 반환 값은 as 로 나타낸 변수에 위치시킨다.
#           그 후에 with 의 내부 명령어를 실행하고 마지막으로 __exit__() 메소드로 소거 작업을 한다.
#           이 흐름은 with 문 내부에서 어떤 일이 발생하는지와 상관 없이 일어나고, 예외가 발생한다해도 변함이 없다.
#           사실 __exit__() 메소드의 세 가지 인자에 예외 타입, 값, 트레이스백(traceback)이 들어 있다.
#           __exit__() 메소드는 예외 정보를 고르거나 아무 일도 하지 않고 None 을 반환하며 무시하는 방식을 선택할 수 있다.
#           만약 __exit__() 가 True 를 반환하면 예외를 없애고 아무 일도 일어나지 않았던 것처럼 with 블록 다음의 프로그램을
#           계속해서 실행한다.

#   - 이번 레시피에서 with 문을 여러 번 써서 중첩된 연결을 LazyConnection 클래스가 허용하는지 여부가 미묘한 측면이다.
#     앞에 나온 대로 한 번에 하나의 소켓 연결만 허용되고 소켓을 사용 중에 중복된 with 문이 나타나면 예외가 발생한다.
#     구현법을 조금만 바꾸면 이 제한을 피해 갈 수 있다.
from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    # AF_INET :  Internet Protocol(IP) socket 을 요청.
    # SOCK_STREAM : TCP 소켓 생성.
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

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connections.pop().close()

from functools import partial

conn = LazyConnection(('www.python.org', 80))
with conn as s1:
    with conn as s2:
        pass
    pass

#   - 두 번째 버전에서 LazyConnection 클래스는 연결을 위한 팩토리 역할을 한다.
#     내부적으로 스택을 위해 리스트를 사용했다. __enter__() 가 실행될 때마다, 새로운 연결을 만들고 스택에 추가한다.
#     __exit__() 메소드는 단순히 스택에서 마지막 연결을 꺼내고 닫는다.
#     사소한 문제지만 이로 인해서 중첩 with 구문으로 연결을 여러 개 생성할 수 있다.


#  8.4 인스턴스를 많이 생성할 때 메모리 절약
#  ▣ 문제 : 프로그램에서 많은 인스턴스를 생성하고 메모리를 많이 소비한다.
#  ▣ 해결 : 간단한 자료 구조 역할을 하는 클래스의 경우 __slots__ 속성을 클래스 정의에 추가하면 메모리 사용을 상당히 많이 절약할 수 있다.
class Date:
    __slots__ = ['year', 'month', 'day']

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

#   - __slots__ 을 정의하면 파이썬은 인스턴스에서 훨씬 더 압축된 내부 표현식을 사용한다.
#     인스턴스마다 딕셔너리를 구성하지 않고 튜플이나 리스트 같은 부피가 작은 고정 배열로 인스턴스가 만들어진다.
#     __slots__ 명시자에 리스팅된 속성 이름은 내부적으로 이 배열의 특정 인덱스에 매핑된다.
#     슬롯을 사용하는 데서 발생하는 부작용은 인스턴스에 새로운 속성을 추가할 수 없다는 점이다.
#     __slots__ 명시자에 나열한 속성만 사용할 수 있다는 제약이 생긴다.

#  ▣ 토론 : 슬롯을 사용해서 절약하는 메모리는 속성의 숫자와 타입에 따라 다르다.
#           하지만, 일반적으로 그 데이터를 딕셔너리에 저장할 때의 메모리 사용과 비교할 만하다.
#           Date 인스턴스 하나를 슬롯 없이 저장하면, 64비트 파이썬에서 428 바이트를 소비한다.
#           만약 슬롯을 정의하면 메모리 사용은 156 바이트로 떨어진다.
#           하지만, 슬롯을 정의한 클래스는 다중 상속과 같은 특정 기능을 지원하지 않는다.
#           따라서 프로그램에서 자주 사용하는 자료 구조에만 슬롯 사용을 고려하는 것이 좋다.


#  8.5 클래스 이름의 캡슐화
#  ▣ 문제 : 클래스 인스턴스의 private 데이터를 캡슐화하고 싶지만, 파이썬에는 접근 제어 기능이 부족하다.
#  ▣ 해결 : 파이썬 프로그래머들은 언어의 기능에 의존하기보다는 데이터나 메소드의 이름에 특정 규칙을 사용하여서 의도를 나타낸다.
#           첫 번째 규칙은 밑줄(_)로 시작하는 모든 이름은 내부 구현에서만 사용하도록 가정하는 것이다.
class A:
    def __init__(self):
        self._internal = 0  # 내부 속성
        self.public = 1  # 외부 속성

    def public_method(self):
        '''
        A public method
        '''

    def _internal_method(self):
        '''
        A internal method
        '''

#   - 클래스 정의에 밑줄 두 개(__)로 시작하는 이름이 나오기도 한다.
class B:
    def __init__(self):
        self.__private = 0

    def __private_method(self):
        '''
        A private method
        '''

    def public_method(self):
        '''
        self.__private_method()
        '''

#   - 이름 앞에 밑줄을 두 개 붙이면 이름이 다른 것으로 변한다. 더 구체적으로, 앞에 나온 클래스의 private 속성은 _B__private 과
#     _B__private_method 로 이름이 변한다.
#     이러한 이름의 변화는 속성은 속성을 통해 오버라이드 할 수 없다는 것이다.
class C:
    def __init__(self):
        super().__init__()
        self.__private = 1  # B.__private 를 오버라이드하지 않는다.

    # B.__private_method() 를 오버라이드하지 않는다.
    def __private_method(self):
        pass

#   - 여기서 __private 과 __private_method 의 이름은 _C__private 과 _C__private_method 로 변하기 때문에 B 클래스의 이름과
#     겹치지 않는다.

#  ▣ 토론 : 프라이빗 속성에 대한 규칙이 두 가지 존재해서, 이 중 어떤 스타일을 써야할지 의문이 들 수 있다.
#           대개의 경우 공용이 아닌 이름은 밑줄을 하나만 붙여야 한다.
#           하지만 코드가 서브클래싱을 사용할 것이고 서브클래스에서 숨겨야 할 내부 속성이 있다면 밑줄을 두 개 붙인다.
#           그리고 예약해 둔 단어 이름과 충돌하는 변수를 정의하고 싶을 때가 있다.
#           이런 경우 이름 뒤에 밑줄을 하나 붙인다.
lambda_ = 2.0  # lambda 키워드와의 충돌을 피하기 위해 밑줄을 붙인다.
#   - 밑줄을 변수 이름 앞에 붙이지 않는 이유는 내부적으로 사용하는 의도와의 혼동을 피하기 위해서이다.
#     변수 이름 뒤에 밑줄을 하나 붙여서 이 문제를 해결한다.