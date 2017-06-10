#인자를 N개 받는 함수를 더 적은 인자로 사용
#문제
#파이썬 코드에 콜백 함수나 핸들러로 사용할 호출체가 있다. 하지만 함수의 인자가 너무 많고 호출했을 때 예외가 발생한다.
#해결
#함수의 인자 개수를 줄일면 functools.partial()을 사용해야 한다. partial() 함수를 사용하면 함수의 인자에 고정 값을 할당 할 수 있고, 따라서 호출할 때 넣어야 하는 인자 수를 줄일 수 있다.
#다음과 같은 함수가 있다고 가정하자.
def spam(a,b,c,d):
    print(a,b,c,d)
#이제 partial로 특정 값을 고정했다
from functools import partial
s1 = partial(spam,1)
s1(2,3,4)
s1(4,5,6)
s2=partial(spam, d=42)
s2(1,2,3)
s3 = partial(spam, 1,2,d=42)
#partial()이 특정 인자의 값을 고정하고 새로운 호출제를 반환한다. 이 새로운 호출체는 할당하지 않은 인자를 받고, partial()에 주어진 인자와 합친 후 원본 함수에 전달한다.
#토론
#이번 레시피는 겉으로 보기에 호환되지 않을 것 같은 코드를 함께 동작하도록 하는 문제와 관련있다.
#우선 x,y튜플로 나타낸 좌표 리스트가 있다. 다음 함수를 사용해서 두 점 사이의 거리를 구할 수 있다.
points=[(1,2),(3,4),(5,6),(7,8)]
import math
def distance(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return math.hypot(x2-x1, y2-y1)
#이제 어떤 점에서부터 이 점까지의 거리에 따라 정렬을 해야 한다면 어떻게 할까? 리스트의 sort()메소드는 key 인자를 받아서 정렬에 사용하지만 인자가 하나인 함수에만 동작한다.
#(따라서 distance()는 적당하지 않다.) 이때 partial()로 이 문제를 해결한다.
pt = (4,3)
points.sort(key=partial(distance,pt))
points
#이 발상을 확장해서 다른 라이브러리에서 사용하는 콜백 함수의 매개변수 설명을 변경하는데 partial()을 사용할 수도 있다. 예를 들어 multiprocessing을 사용해서 비 동기식으로 결과를 계산하고, 결과값과 로깅 인자를 받는 콜백함수에
#그 결과를 전달하는 코드가 있다.
def output_result(result,log=None):
    if log is not None:
        log.debug('Got : %r',result)
#샘플함수
def add(x,y):
    return x+y
if "__name__"=='__main__':
    import logging
    from multiprocessing import pool
    from functools import partial

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')
    p=pool()
    p.apply_async(add,(3,4), callback=partial(output_result, log=log))
    p.close()
    p.join()

#apply_async()로 콜백 함수를 지원할 때, partial()을 사용해서 추가적인 로깅 인자를 넣었다. multiprocessing은 하나의 값으로 콜백 함수를 호출하개 되는 것이다.
#유사한 예제로 네트워크 서버를 작성한다고 생각해보자. socketserver 모듈을 사용하면 상대적으로 편하게 작업할 수 있다. 예를 들어 다음 코드는 간단한 에코 서버를 구현한다.
from socketserver import StreamRequestHandler, TCPServer

class EchoHandler(StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'GOT:'+line)

serv = TCPServer(('',15000),EchoHandler)
serv.serve_forever()
#하지만 에코핸들러 클래스에 초기화 메소드가 추가적인 설정 인자를 받게 하고 싶다고 가정해보자.
class EchoHandler(StreamRequestHandler):
    def __init__(self,*args,ack,**kwargs):
        self.ack = ack
        super().__init__(*args,**kwargs)
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'GOT:'+line)

#이렇게 수정하면 tcpserver 클래스에 넣을 수 있는 뚜렷한 방법이 사라진다. 이제 코드를 실행하면 다음과 같은 예외가 발생한다.

#얼핏 보기에 socket서버를 수정하거나 이상한 해결책을 사용하지 않는 한 이 코드르 고치기 불가능한것처럼 느껴지지만, partial()을 이용해서 ack인자에 값을 넣어줌ㄴ 간단히 해결된다.
from functools import partial
serv = TCPServer(('',15000), partial(EchoHandler, ack=b'RECEOVED: '))
serv.serve_forever()

#이 예제에서 __inir__() 메소드에 ack 인자를 명시하는 것이 우습게 보일 수 있지만 키워드로만 넣을 수 있는 인자랏 ㅓ그렇다.
#partial 기능을 람다 표현식으로
points.sort(key=lambda p: distance(pt,p))
p.apply_async(add,(3,4),callback=lambda result : output_result(result,log))
serv = TCPServer(('',15000), lambda *args, **kwargs: EchoHandler(*args,ack=b'RECEIVED:',**kwargs))
#이 코드도 동작하기는 하지만 가독성이 떨어짐.