from functools import partial
points = [(1,2),(3,4),(5,6),(7,8)]

import math
def distance(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2-x1, y2-y1)

#어떤 한 점에서부터 해당 점까지의 거리에 따라 정렬을 해야 한다면 어떻게 해야할까?
#리스트의 sort() 메소드는 key 인자를 받아 정렬에 사용하지만,인자가 하나인 함수에만 동작한다.
#이떄 partial() 로 이 문제를 해결한다.

pt=(4,4)  #어떤 한 점이 (4,3)에 있다.
print(partial(distance, pt))  #functools.partial(<function distance at 0x002EC618>, (4, 3))
points.sort(key=partial(distance,pt))   #그럼 p1 = pt?
print(points)  #[(3, 4), (1, 2), (5, 6), (7, 8)]

#발상을 확장해서, 다른 라이브러리에서 사용하는 콜백 함수의 매개변수 설명을 변경하는데
#partial() 을 사용할 수 있다.

#ex) multiprocessing >> 비동기식 결과 계산 >> 로깅 인자를 받는 콜백함수에 결과를 전달하는 코드가 있다.

def output_result(result, log=None):
    if log is not None:
        log.debug('Got:%r',result)

#샘플

def add(x,y):
    return x+y

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


#apply_async로 콜백 함수 지원 시, partial사용하여 추가 로깅 인자를 넣는다.
#멀티프로세싱은 하나의 값으로 콜백 함수를 호출하게 되는 것이다.

#네트워크 서버를 작성 한다고 생각하면 socketserver 모듈을 사용하면 상대적으로 편하게 작업할 수 있다.
#간단한 에코 서버 구현하기

#에코서버 : 클라이언트에서 서버에 문자를 송신하면 서버에서 클라이언트로 다시 송신하여 클라이언트 내부에서 출력한다.


from socketserver import StreamRequestHandler, TCPServer

class EchoHandler(StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'GOT:' + line)

# serv = TCPServer(('', 15000), EchoHandler)
# serv.serve_forever()


#하지만 EchoHandler 클래스에 __init__() 메소드가 추가적인 설정인자를 받게 하고 싶다고 가정해보자.


from socketserver import StreamRequestHandler, TCPServer

class EchoHandler(StreamRequestHandler):
    #ack는 키워드로만 넣을 수 있는 인자이다. *args, **kwargs는 그 외 일반적인 파라미터이다.
    def __init__(self,*args, ack, **kwargs):
        self.ack = ack
        super().__init__(*args, **kwargs)
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'GOT:' + line)

# serv = TCPServer(('', 15000), EchoHandler)
# serv.serve_forever()


#이렇게 수정하면 TCPServer 클래스에 넣을 수 있는 뚜렷한 방법이 사라진다. 이제 코드를 실행하면 다음과 같은 예외가 발생한다.

# 얼핏 보기에 socketserver를 수정하거나 이상한 해결책을 사용하지 않는한 불가능할것 같으나
# partial() 사용해서 ack 인자에 값을 넣으면 해결된다.

# serv = TCPServer(('', 15000), partial(EchoHandler, ack=b'RECEIVED:'))
# serv.serve_forever()

#이 예제에서 __init__() 메소드에 ack 인자를 명시하는 것이 이상할 순 있으나 키워드로만 넣을 수 있는 인자이기 때문에 ~^^

#partial 기능을 lambda표현으로 대신 할 수도 있음.


# points.sort(key=lambda p: distance(pt,p))
# p.apply_async(add, (3,4), callback=lambda result: output_result(result,log))

# serv = TCPServer(('',15000),lambda *args, **kwargs: EchoHandler(*args,ack=b'RECEIVED:',**kwargs))

#위 방법은 가독성이 떨어짐






"""
7.9 메소드가 하나인 클래스를 함수로 치환

__init__ 외에 메소드가 하나뿐인 클래스가 있는데, 코드를 간결하게 만들기 위해
 하나의 함수로 바꾸고 싶다면?
 
 >>>>>> 클로저를 사용하라!
 URL을 뽑아내는 클래스를 예를 든다.
"""

from urllib.request import urlopen

class UrlTemplate:
    def __init__(self,template):
        self.template = template
    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

    #사용법, 야후에서 주식 데이터를 받는다.

# yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
# for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
#     print(line.decode('utf-8'))


#클래스를 훨씬 간단한 함수로 치환

def Urltem(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# yahoo = Urltem('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
# for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
#     print(line.decode('utf-8'))

#대개의 경우 메소드가 하나뿐인 클래스가 필요할 때는 추가적인 상태를 메소드에 저장할 때 뿐이다.
#예를 들어 urltem..클래스의 목적은 open() 메소드에 사용하기 위해 값을 저장해 놓으려는 것 뿐이다.
#내부(중첩) 함수 or 클로저 사용하면 좀더 보기좋게 코드작성할 수 있다.
#클로저의 주요 기능은 정의할 때의 환경을 기억한다는 것이다.
#클로저는 클래스를 사용하는 것보다 훨씬 우아하게 해결하는 경우가 있다.


"""
7.10 콜백 함수에 추가적 상태 넣기

콜백 함수를 사용하는 코드를 작성중(event handler, complete callback)에 콜백함수의
추가 상태를 넣고 내부 호출에 사용하고 싶다면

>>>> 비동기 처리 관련 있는 프레임워크 or 라이브러리의 콜백함수 활용 알아본다.

"""

def apply_async(func, args, *, callback):
    #결과를 계산한다.
    result = func(*args)
    #결과 값으로 콜백 함수 호출
    callback(result)       #callback대상 함수는 print_result이니까 실행하라.

def print_result(result):
    print('Got:', result)

def add(x,y):
    return x+y

# apply_async(add, (2,3), callback=print_result) #func = add / args = (2,3) /callback

#앞에 나왓듯이, print_result함수는 결과 값만 하나의 인자로 받는다.
#이러한 부족한 정보로 인해 콜백에 문제가 생기기도 한다.


#콜백함수에 추가정보 넣는 방법은 함수 대신 바운드-메소드를 사용하는 것이다.
#boundmethod

#ex) 이 클래스는 결과 값을 받을 때마다 늘어나는 시퀀스 숫자를 가지고 있다.

class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self,result):
        self.sequence += 1
        print('[{}] Got:{}'.format(self.sequence, result))

#이 클래스는 인스턴스를 만든 후, 바운드 메소드 handler를 콜백으로 사용한다.

r = ResultHandler()
apply_async(add,(2,3),callback =r.handler)
apply_async(add, ('hello','world'), callback=r.handler)
apply_async(add, ('heo','wld'), callback=r.handler)
# [1] Got:5
# [2] Got:helloworld
# [3] Got:heowld

#클래스의 대안으로 클로저를 사용해서 상태를 저장해도 된다.

def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence   #중첩함수에서도 부모함수의 변수를 써먹을 수 있게 글로벌 처리하는듯?
        sequence += 1
        print('[{}] Got : {} '.format(sequence,result))
    return handler

handler = make_handler()
apply_async(add, (2,3), callback=handler)
apply_async(add, ("hello","world"), callback=handler)

#코루틴 방법

def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence,result))

handler = make_handler()
next(handler)
apply_async(add, (2,3),callback=handler.send)
next(handler)  #sequence증가는 했으나, 변수 값이 없어서 None처리
apply_async(add, (2,3),callback=handler.send)

#마지막으로 추가적인 인자와 파셜함수 응용프로그램으로 콜백에 상태를 넣을 수 있다.

class SeqNo:
    def __init__(self):
        self.sequence = 0

def handler(result, seq):
    seq.sequence += 1
    print('[{}] Got: {}'.format(seq.sequence, result))

seq = SeqNo()
from functools import partial
apply_async(add, (2,3), callback=partial(handler,seq=seq))







"""
7.11 인라인 콜백 함수
콜백 함수 작성 시 크기가 너무 작은 함수 많이 만들까 걱정된다.

제너레이터와 코루틴을 사용하면 콜백 함수를 함수 내부에 넣을 수 있다.

"""

def apply_async(func, args, *, callback):
    result = func(*args)
    callback(result)

#이제 Asyncs 클래스와 inlined_async 데코레이터 포함하고 있는 지원코드를 본다

from queue import Queue
from functools import wraps

class Async:
    def __init__(self,func,args):
        self.func =func
        self.args = args
    def inlined_async(self,func):
        @wraps(func)
        def wrapper(*args):
            f=func(*args)
            result_queue = Queue()
            result_queue.put(None)
            while True:
                result = result_queue.get()
                try:
                    a = f.send(result)
                    apply_async(a.func,a.args, callback=result_queue.put)
                except StopIteration:
                    break
        return wrapper

#두 개의 코드 조각이 있으면 yield 구문으로 콜백 단계를 인라인 할 수 있다.

def add(x,y):
    return x + y

@inlined_async
def test():
    r = yield Async(add, (2,3))
    print(r)
    r = yield Async(add, ('h','o'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n,n))
        print(r)
    print('goodbye')

# 특별 데코레이터와 yield를 제외하고는 아무런 콜백 함수가 나타나지 않음을 확인
