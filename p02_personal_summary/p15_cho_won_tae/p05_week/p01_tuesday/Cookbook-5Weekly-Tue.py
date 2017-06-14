# 7.8 인자를 N개 받는 함수를 더 적은 인자로 사용
# 문제
# 파이썬 코드에 콜백 함수나 핸들로 사용할 호출체가 있다. 함지만 함수의 인자가 너무 많고 호출했을 때 예외가 발생한다
# 해결
# 함수의 인자 개수를 줄이려면 functools.partial()을 사용해야 한다.
# partial() 함수를 사용하면 함수의 인자에 고정 값을 할당할 수 있고, 따라서 호출할 때 넣어야 하는 인자 수를 줄일 수 있다.
# 다음과 같은 함수가 있다고 가정해보자
def spam(a,b,c,d):
    print(a,b,c,d)
# 이제 partial() 로 특정 값을 고정했다
from functools import partial
s1 = partial(spam,1)
print(s1(2,3,4)) # 1 2 3 4 출력
s1(4,5,6) # 1 4 5 6 출력
s2 = partial(spam,d=42)
s2(1,2,3) # 1 2 3 42 출력
s2(4,5,5) # 4 5 5 42
s3 = partial(spam,1,2,d=42)
s3(3) # 1 2 3 42
s3(4) # 1 2 4 42
s3(5) # 1 2 5 42
# 토론
# 이번 레시피는 겉으로 보기에 호환됮 않을 것 같은 코드를 함께 동작하도록 하는 문제와 관련있다
points = [(1,2),(3,4),(5,6),(7,8)]
import math
def distance(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return math.hypot(x2 - x1,y2 - y1)
# 리스트의 sort() 메소드는 key 인자를 받아서 정렬에 사용하지만 인자가 하나인 함수에만 동작한다
# 이때 partial()로 이 문제를 해결한다
pt = (4,3)
points.sort(key=partial(distance,pt))
print(points) # [(3, 4), (1, 2), (5, 6), (7, 8)]
# 발상을 확장해서, 다른 라이브러리에서 사용하는 콜백 함수의 매개변수 설명을 변경하는데 partial() 을 사용할 수도 있다
def output_result(result,log=None):
    if log is not None:
        log.debug('Got:%r',result)
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
# apply_async() 로 콜백 함수를 지원할 때, partial() 을 사용해서 추가적인 로깅 인자를 넣었다.
# 유사한 예제로 네트워크 서버를 작성한다고 생각해보자.
# socketserver 모듈을 사용하면 상대적으로 편하게 작업할 수 있다
from socketserver import StreamRequestHandler, TCPServer

class EchoHandler(StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'GOT : ' + line)

serv = TCPServer(('', 15000), EchoHandler)
serv.serve_forever()
# 하지만 EchoHandler 클래스에 __init__() 메소드가 추가적인 설정 인자를 받게 하고 싶다고 가정해보자
class EChoHandler(StreamRequestHandler):
    # ack 는 키워드로만 넣을 수 있는 인자
    # *args, **kwargs 는 그 외 일반적인 파라미터 이다
    def __init__(self, *args, ack, **kwargs):
        self.ack = ack
        super().__init__(*args, **kwargs)

    def handle(self):
        for line in self.rfile:
            self.wfile.write(self.ack + line)
# 이렇게 수정하면 TCPServer 클래스에 넣을 수 있는 뚜렷한 방법이 사라진다.

# 7.9 메소드가 하나인 클래스를 함수로 치환
# 문제
# __init__() 외에 메소드가 하나뿐인 클래스가 있는데, 코드를 간결하게 만들기 위해 이를 하나의 함수로 바꾸고 싶다
# 해결
# 많은 경우 메소드가 하나뿐인 클래스는 클로저를 사용해서 함수로 바꿀 수 있다
# 템플릿 스킴을 사용해서 URL 을 뽑아내는 다음 클래스를 예로 들어보자
from urllib.request import urlopen
class UrlTemplate:
    def __init__(self,template):
        self.template = template
    def open(self,**kwargs):
        return urlopen(self.template.format_map(kwargs))
# 사용법. 야후에서 주식 데이터를 받는다
yahoo= UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f{fields}')
for line in yahoo.open(names='IBM,AAPL,FB',fields='sl1c1v')
    print(line.decode('utf-8'))
# 클래스를 훨씬 간단한 함수로 치환할 수 있다
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# 사용법
yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={name}&f={fields}')
for line in yahoo(names='IBM,AAPL,FB',fields='sl1c1v'):
    print(line.decode('utf-9'))
# 토론
# 대개의 경우 메소드가 하나뿐인 클래스가 필요할 때는 추가적인 상태를 메소드에 저장할 때 뿐이다.
# 예를 들어 UrlTemplate 클래스의 목적은 open() 메소드에서 사용하기 위해 template 값을 저장해 놓으려는 것 뿐이다
# 내부 함수나 클로저를 사용하면 좀 더 보기 좋게 코드를 작성할 수 있다. 단순히 생각해서 클로저는 함수라고 말할 수있다
# 하지만 함수 내부에서 사용하는 변수의 추가적인 환경이 있다.
# 클로저의 주요 기능은 정의할 때의 환경을 기억한다는 것이다.

# 7.10 콜백 함수에 추가적 상태 넣기
# 문제
# 콜백 함수를 사용하는 코드를 작성 중이다.
# 이때 콜백 함수에 추가상태를 넣고 내부 호출에 사용하고 싶다
# 해결
# 많은 라이브러리와 프레임워크에서 찾을 수 있는 콜백 함수의 활용을 알아본다
def apply_async(func,args,*,callback):
    # 결과 계산
    result = func(*args)
    # 결과 값으로 콟랙 함수 호출
    callback(result)
# 실제 애플리케이션이라면 이런 코드에서는 스레드, 프로세스, 타이머 등과 관련 있는 고급 동작을 구현하겠지만,
# 여기서는 그런 것이 중요하지 않으므로 건너뛰고, 콜백 호출 자체에만 집중한다
def print_result(result):
    print('Got : ', result)
def add(x, y):
    return x + y
apply_async(add, (2, 3), callback=print_result)
apply_async(add, ('hello', 'world'), callback=print_result)
# print_result() 함수는 결과 값만 하나의 인자로 받는다
# 다른 어떠한 정보도 전달 받지 않는다.
# 이렇게 부족한 정보로 인해 콜백 함수가 다른 변수나 환경 등과 통신할 때 문제가 발생하기도 한다
# 콜백 함수에 추가 정보를 넣는 한 가지 방법은 하나의 함수 대신 바운드-메소드를 사용하는 것이다
class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got : {}'.format(self.sequence, result))
# 인스턴스를 만들고 바운드 메소드 handler 를 콜백으로 사용해야 한다
r = ResultHandler()
apply_async(add, (2, 3), callback=r.handler)
apply_async(add, ('hello', 'world'), callback=r.handler)
# 클래스의 대안으로 클로저를 사용해서 상태를 저장해도 된다
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got : {}'.format(sequence, result))
    return handler

handler = make_handler()
apply_async(add, (2, 3), callback=handler)
apply_async(add, ('hello', 'world'), callback=handler)
# 코루틴을 사용할 때
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got : {}'.format(sequence, result))
# 코루틴의 경우에는 콜백으로 send() 메소드를 사용해야 한다
handler = make_handler()
next(handler)       # Advance to the yield
apply_async(add, (2, 3), callback=handler.send)
apply_async(add, ('hello', 'world'), callback=handler.send)
# 추가적인 인자와 파셜 함수 애플리케이션으로 콜백에 상태를 넣을 수 있다
class SequenceNo:
    def __init__(self):
        self.sequence = 0
    def handler(result,seq):
        seq.sequence += 1
        print('[{}] Got: {}'.format(seq.sequence,result))
seq = SequenceNo()
from functools import partial
apply_async(add, (2, 3), callback=partial(handler, seq=seq))
apply_async(add, ('hello', 'world'), callback=partial(handler, seq=seq))
# 토론
# 콜백 함수를 사용하는 프로그램은 엉망으로 망가질 위험 요소를 안고 있다
# 문제점은 콜백 실행으로 이끄는 초기 요청 코드와 콜백 함수가 끊어진다는 점이다
# 결과적으로 요청을 한 곳과 처리하는 곳이 서로를 찾지 못하게 된다
# 클로저를 사용할때는 수정 가능한 변수를 조심해서 사용해야 한다
# 코루틴의 잠재적 단점은 파이썬의 기능으로 받아들여지지 않을 때가 있다는 것이다
# 또한 코루틴을 사용하기 전에 next() 를 호출해야 한다는 점도 있다

# 7.11 인라인 콜백 함수
# 문제
# 콜백 함수를 사용하는 코드를 작성하는데, 크기가 작은 함수를 너무 많이 만들어 낼까 걱정이 된다
# 코드가 좀 더 정상적인 절차적 단계를 거치도록 하고 싶다
# 해결
# 제너레이터와 코루틴을 사용하면 콜백 함수를 함수 내부에 넣을 수 있다
# 예를 들어 어떤 작업을 하고 콜백을 호출하는 다음 코드를 보자
def apply_async(func, args, *, callback):
    # 결과 계산
    result = func(*args)
    # 결과 값으로 콜백 함수 호출
    callback(result)
# Async 클래스와 inlined_async 데코레이터를 포함하고 있는 지원 코드를 보자
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
# 두개의 코드 조각이 있으면 yield 구문으로 콜백 단계를 인라인 할 수 있다
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
# test 를 호출하면
# 5 helloworld 0 2 4 6 8 10 12 14 16 18 출력
# 토론
# 이번 레시피를 통해 콜백 함수, 제너레이터, 컨트롤 플로우를 얼마나 잘 이해하고 있는지 알 수 있다
# 첫째, 콜백과 관련 있는 코드에서 현재 연산이 모두 연기되고 특정 포인트에서 재시작한다는 점이 포인트
# 프로그램 실행이 연기되고 재시작하는 발상은 자연스럽게 제너레이터 함수의 실행 모델과 매핑된다
# 특히 yield 연산은 제너레이터 함수가 값을 분출하고 연기하도록 한다.
# 뒤어어 __next__() 나 send() 메소드를 호출하면 다시 실행된다

# 7.12 클로저 내부에서 정의한 변수에 접근
# 문제
# 클로저는 확장해서 내부 변수에 접근하고 수정하고 싶다
# 해결
# 일반적으로 클로저 내부 변수는 외부와 완전히 단절되어 있다.
# 하지만 접근 함수를 만들고 클로저에 함수 속성으로 붙이면 내부 변수에 접근 할 수 있다
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
        return func
# 사용법
f = sample()
f() # n=0 출력
f.set_n(10)
f() # n=10 출력
f.get_n() # 10 출력
# 토론
# 이번 레시피를 이루는 두 가지 주요 기능이 있다.
# 첫째는 nonlocal 선언으로 내부 변수를 수정하는 함수를 작성하는것
# 두번째는 접근 메소드를 클로저 함수에 붙여 마치 인스턴스 메소드인것처럼 동작하는 것
# 조금 확장해서 클로저를 마치 클래스의 인스턴스인 것처럼 동작하게 만들 수 있다
# 내부 함수를 인스턴스 딕셔너리에 복사하고 반환하기만 하면 된다
import sys
class ClosureInstance:
    def __init__(self,locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals
        # 인스턴스 딕셔너리를 호출체로 갱신
            self.__dict__.update((key,value) for key,value in locals.items() if callable(value))
        # 특별 메소드 리다이렉트
    def __len__(self):
        return self.__dict__['__len__']()
# 사용 예제
def Stack():
    items=[]
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
len(s) # 3 출력
s.pop() # Hello 출력

# 챕터 8장은 금요일까지 몰아서....하겠습니다...
# 그놈의 스콥ㅠㅠㅠㅠ