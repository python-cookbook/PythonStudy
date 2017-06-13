"""
7.8~ 8.5

7.8 인자를 N 개 받는 함수를 더 적은 인자로 사용
7.9 메소드가 하나인 클래스를 함수로 치환
7.10 콜백 함수에 추가적 상태 넣기
7.11 인라인 콜백 함수
7.12 클로저 내부에서 정의한 변수에 접근하기
8.1 인스턴스의 문자열 표현식 변형
8.2 문자열 서식화 조절
8.3 객체의 콘텍스트 관리 프로토콜 지원
8.4 인스턴스를 많이 생성할 때 메모리 절약
8.5 클래스 이름의 캡슐화


"""

"""
7.8 인자를 N 개 받는 함수를 더 적은 인자로 사용

파이썬 코드에 콜백 함수나 핸들러로 사용할 호출체가 있다.
인자가 너무많으면 예외 발생한다.

인자 개수를 줄이고자 한다면?
    
    functools.partial() 
    
    을 사용 해야 한다.
    
함수 인자 고정 값 할당한다.

    
"""
from functools import partial

points = [(1, 2), (3, 4), (5, 6), (7, 8)]

import math


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)


# 어떤 한 점에서부터 해당 점까지의 거리에 따라 정렬을 해야 한다면 어떻게 해야할까?
# 리스트의 sort() 메소드는 key 인자를 받아 정렬에 사용하지만,인자가 하나인 함수에만 동작한다.
# 이떄 partial() 로 이 문제를 해결한다.

pt = (4, 4)  # 어떤 한 점이 (4,3)에 있다.
print(partial(distance, pt))  # functools.partial(<function distance at 0x002EC618>, (4, 3))
points.sort(key=partial(distance, pt))  # 그럼 p1 = pt?
print(points)  # [(3, 4), (1, 2), (5, 6), (7, 8)]


# 발상을 확장해서, 다른 라이브러리에서 사용하는 콜백 함수의 매개변수 설명을 변경하는데
# partial() 을 사용할 수 있다.

# ex) multiprocessing >> 비동기식 결과 계산 >> 로깅 인자를 받는 콜백함수에 결과를 전달하는 코드가 있다.

def output_result(result, log=None):
    if log is not None:
        log.debug('Got:%r', result)


# 샘플

def add(x, y):
    return x + y


# if __name__== '__main__':
#     import logging
#     from multiprocessing import Pool
#     from functools import partial
#
#     logging.basicConfig(level=logging.DEBUG)
#     log = logging.getLogger('test')
#
#     p = Pool()
#     p.apply_async(add, (3,4), callback=partial(output_result,log=log))
#     p.close()
#     p.join()


# apply_async로 콜백 함수 지원 시, partial사용하여 추가 로깅 인자를 넣는다.
# 멀티프로세싱은 하나의 값으로 콜백 함수를 호출하게 되는 것이다.

# 네트워크 서버를 작성 한다고 생각하면 socketserver 모듈을 사용하면 상대적으로 편하게 작업할 수 있다.
# 간단한 에코 서버 구현하기

# 에코서버 : 클라이언트에서 서버에 문자를 송신하면 서버에서 클라이언트로 다시 송신하여 클라이언트 내부에서 출력한다.


from socketserver import StreamRequestHandler, TCPServer


class EchoHandler(StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'GOT:' + line)


# serv = TCPServer(('', 15000), EchoHandler)
# serv.serve_forever()


# 하지만 EchoHandler 클래스에 __init__() 메소드가 추가적인 설정인자를 받게 하고 싶다고 가정해보자.


from socketserver import StreamRequestHandler, TCPServer


class EchoHandler(StreamRequestHandler):
    # ack는 키워드로만 넣을 수 있는 인자이다. *args, **kwargs는 그 외 일반적인 파라미터이다.
    def __init__(self, *args, ack, **kwargs):
        self.ack = ack
        super().__init__(*args, **kwargs)

    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'GOT:' + line)


# serv = TCPServer(('', 15000), EchoHandler)
# serv.serve_forever()


# 이렇게 수정하면 TCPServer 클래스에 넣을 수 있는 뚜렷한 방법이 사라진다. 이제 코드를 실행하면 다음과 같은 예외가 발생한다.

# 얼핏 보기에 socketserver를 수정하거나 이상한 해결책을 사용하지 않는한 불가능할것 같으나
# partial() 사용해서 ack 인자에 값을 넣으면 해결된다.

# serv = TCPServer(('', 15000), partial(EchoHandler, ack=b'RECEIVED:'))
# serv.serve_forever()

# 이 예제에서 __init__() 메소드에 ack 인자를 명시하는 것이 이상할 순 있으나 키워드로만 넣을 수 있는 인자이기 때문에 ~^^

# partial 기능을 lambda표현으로 대신 할 수도 있음.


# points.sort(key=lambda p: distance(pt,p))
# p.apply_async(add, (3,4), callback=lambda result: output_result(result,log))

# serv = TCPServer(('',15000),lambda *args, **kwargs: EchoHandler(*args,ack=b'RECEIVED:',**kwargs))

# 위 방법은 가독성이 떨어짐






"""
7.9 메소드가 하나인 클래스를 함수로 치환

__init__ 외에 메소드가 하나뿐인 클래스가 있는데, 코드를 간결하게 만들기 위해
 하나의 함수로 바꾸고 싶다면?

 >>>>>> 클로저를 사용하라!
 URL을 뽑아내는 클래스를 예를 든다.
"""

from urllib.request import urlopen


class UrlTemplate:
    def __init__(self, template):
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

        # 사용법, 야후에서 주식 데이터를 받는다.


# yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
# for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
#     print(line.decode('utf-8'))


# 클래스를 훨씬 간단한 함수로 치환

def Urltem(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))

    return opener


# yahoo = Urltem('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
# for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
#     print(line.decode('utf-8'))

# 대개의 경우 메소드가 하나뿐인 클래스가 필요할 때는 추가적인 상태를 메소드에 저장할 때 뿐이다.
# 예를 들어 urltem..클래스의 목적은 open() 메소드에 사용하기 위해 값을 저장해 놓으려는 것 뿐이다.
# 내부(중첩) 함수 or 클로저 사용하면 좀더 보기좋게 코드작성할 수 있다.
# 클로저의 주요 기능은 정의할 때의 환경을 기억한다는 것이다.
# 클로저는 클래스를 사용하는 것보다 훨씬 우아하게 해결하는 경우가 있다.


"""
7.10 콜백 함수에 추가적 상태 넣기

콜백 함수를 사용하는 코드를 작성중(event handler, complete callback)에 콜백함수의
추가 상태를 넣고 내부 호출에 사용하고 싶다면

>>>> 비동기 처리 관련 있는 프레임워크 or 라이브러리의 콜백함수 활용 알아본다.

"""


# def apply_async(func, args, *, callback):
#     # 결과를 계산한다.
#     result = func(*args)
#     # 결과 값으로 콜백 함수 호출
#     callback(result)  # callback대상 함수는 print_result이니까 실행하라.
#
#
# def print_result(result):
#     print('Got:', result)
#
#
# def add(x, y):
#     return x + y


# apply_async(add, (2,3), callback=print_result) #func = add / args = (2,3) /callback

# 앞에 나왓듯이, print_result함수는 결과 값만 하나의 인자로 받는다.
# 이러한 부족한 정보로 인해 콜백에 문제가 생기기도 한다.


# 콜백함수에 추가정보 넣는 방법은 함수 대신 바운드-메소드를 사용하는 것이다.
# boundmethod

# ex) 이 클래스는 결과 값을 받을 때마다 늘어나는 시퀀스 숫자를 가지고 있다.

class ResultHandler:
    def __init__(self):
        self.sequence = 0

    def handler(self, result):
        self.sequence += 1
        print('[{}] Got:{}'.format(self.sequence, result))


# 이 클래스는 인스턴스를 만든 후, 바운드 메소드 handler를 콜백으로 사용한다.
#
# r = ResultHandler()
# apply_async(add, (2, 3), callback=r.handler)
# apply_async(add, ('hello', 'world'), callback=r.handler)
# apply_async(add, ('heo', 'wld'), callback=r.handler)


# [1] Got:5
# [2] Got:helloworld
# [3] Got:heowld

# 클래스의 대안으로 클로저를 사용해서 상태를 저장해도 된다.

# def make_handler():
#     sequence = 0
#
#     def handler(result):
#         nonlocal sequence  # 중첩함수에서도 부모함수의 변수를 써먹을 수 있게 글로벌 처리하는듯?
#         sequence += 1
#         print('[{}] Got : {} '.format(sequence, result))
#
#     return handler
#
#
# handler = make_handler()
# apply_async(add, (2, 3), callback=handler)
# apply_async(add, ("hello", "world"), callback=handler)
#
#
# # 코루틴 방법
#
# def make_handler():
#     sequence = 0
#     while True:
#         result = yield
#         sequence += 1
#         print('[{}] Got: {}'.format(sequence, result))
#
#
# handler = make_handler()
# next(handler)
# apply_async(add, (2, 3), callback=handler.send)
# next(handler)  # sequence증가는 했으나, 변수 값이 없어서 None처리
# apply_async(add, (2, 3), callback=handler.send)
#
#
# # 마지막으로 추가적인 인자와 파셜함수 응용프로그램으로 콜백에 상태를 넣을 수 있다.
#
# class SeqNo:
#     def __init__(self):
#         self.sequence = 0
#
#
# def handler(result, seq):
#     seq.sequence += 1
#     print('[{}] Got: {}'.format(seq.sequence, result))
#
#
# seq = SeqNo()
# from functools import partial
#
# apply_async(add, (2, 3), callback=partial(handler, seq=seq))
#
# """
# 7.11 인라인 콜백 함수
# 콜백 함수 작성 시 크기가 너무 작은 함수 많이 만들까 걱정된다.
#
# 제너레이터와 코루틴을 사용하면 콜백 함수를 함수 내부에 넣을 수 있다.
#
# """
#
#
# def apply_async(func, args, *, callback):
#     result = func(*args)
#     callback(result)
#
#
# # 이제 Asyncs 클래스와 inlined_async 데코레이터 포함하고 있는 지원코드를 본다
#
# from queue import Queue
# from functools import wraps
#
#
# class Async:
#     def __init__(self, func, args):
#         self.func = func
#         self.args = args
#
#     def inlined_async(self, func):
#         @wraps(func)
#         def wrapper(*args):
#             f = func(*args)
#             result_queue = Queue()
#             result_queue.put(None)
#             while True:
#                 result = result_queue.get()
#                 try:
#                     a = f.send(result)
#                     apply_async(a.func, a.args, callback=result_queue.put)
#                 except StopIteration:
#                     break
#
#         return wrapper
#
#
# # 두 개의 코드 조각이 있으면 yield 구문으로 콜백 단계를 인라인 할 수 있다.
#
#         def add(x, y):
#             return x + y
#
#
#         @inlined_async
#         def test():
#             r = yield Async(add, (2, 3))
#             print(r)
#             r = yield Async(add, ('h', 'o'))
#             print(r)
#             for n in range(10):
#                 r = yield Async(add, (n, n))
#                 print(r)
#             print('goodbye')
#
#     # 특별 데코레이터와 yield를 제외하고는 아무런 콜백 함수가 나타나지 않음을 확인
#
#
#
# # 이번 레시피통해 콜백함수/제너레이터/컨트롤 플로우를 얼마나 잘 이해하고 있나 알 수 있다.
# #첫째, 콜백과 관련있는 코드에서 현재 연산이모두 연기되고, 특정 포인트에서 재시작한다는 점
#
#
# if __name__ == '__main__':
#     import multiprocessing
#     pool = multiprocessing.Pool()
#     apply_async=pool.apply_async()
#
#     # test()




"""
7.12 클로저 내부에서 정의한 변수에 접근

클로저는 확장해서 내부 변수에 접근하고 수정하고 싶다.

일반적으로 클로저 내부 변수는 외부와 완전히 단절되어 있다.
하지만 접근 함수를 만들고 클로저에 함수 속성으로 붙이면 내부 변수에 접근할 수 있다.



# 두가지 기능이 중요하다.
# nonlocal 선언으로 내부 변수를 수정하는 함수 작성
# 접근 메소드를 클로저 함수에 붙여 마치 인스턴스 메소드인 것처럼 동작하는 것

"""

def sample():
    n =0
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
    func.get_n = set_n
    return func
# f=sample()
# f()
# f.set_n(10)
#
# f.get_n()
#


#클로저를 마치 클래스의 인스턴스인것처럼 동작하게 만들수 있다.
#내부 함수를 인스턴스 딕셔너리 에 복사하고 반환하기만 하면 된다.



import sys
class ClosureInstance:
    def __init__(self,locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals


    # 인스턴스 딕셔너리를 호출체로 갱신
        self.__dict__.update((key,value) for key, value in locals.items()
                             if callable(value))
    #특별 메소드 리다이렉트
    def __len__(self):
        return self.__dict__['__len__']()


#사용 예

def Stack():
    items = []

    def push(item):
        items.append(item)

    def pop():
        return items.pop()

    def __len__():
        return len(items)

    return ClosureInstance()



#실제 동작

s = Stack()    #<__main__.ClosureInstance object at 0x007F7E50> 클로져인스턴스
print(s)

s.push(10)
s.push(20)
s.push('Hello')
print(len(s))   # 3

s.pop()
print(len(s))   # 2


#이 코드는 일반 클래스 정의보다 실행 속도가 더 빠르다.
#비교하기


class Stack2:
    def __init__(self):
        self.items=[]

    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()

    def __len__(self):
        return len(self.items)

from timeit import timeit

#클로저

s = Stack()
a = timeit('s.push(1);s.pop()', 'from __main__ import s')
print(a)   #0.7178065056351765

s = Stack2()

b =timeit('s.push(1);s.pop()', 'from __main__ import s')
print(b)   #0.8129973246608436

#클로저가 8%빠르다. 변수에 접근하는 속도의 차이 !
#추가적인 self호출도 한몫했음

