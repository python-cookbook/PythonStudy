#인라인 콜백 함수
#문제
#콜백 함수를 사용하는 코드를 작성하는데, 크기가 작은 함수를 너무많이 만들어 낼까 걱정이다. 코드가 좀 더 정상적인 절차적 단계를 거치도록 하고 싶다.
#해결
#제너레이터와 코루틴을 사용하면 콜백 함수를 함수 내부에 넣을 수 있다.
def apply_async(func,args,*,callback):
    #결과 계산
    result = func(*args)
    #결과 값으로 콜백함수 호출
    callback(result)

#이제 async 클래스와 inlined_async 데코레이터를 포함하고 있는 지원 코드를 보자.
from queue import Queue
from functools import wraps

class Async:
    def __init__(self,func,args):
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
                    apply_async(a.func,a.args,callback=result_queue.put)
                except StopIteration:
                    break
        return wrapper

#두개의 코드 조각이 있으면 yield 구문으로 콜백 단계를 인라인 할 수 있다
def add(x,y):
    return x+y
@inlined_async
def test():
    r = yield  Async(add,(2,3))
    print(r)
    r = yield  Async(add,('hello','world'))
    print(r)
    for n in range(10):
        r = yield Async(add,(n,n))
        print(r)
    print('Goodbye')

#test()를 호출하면 다음과 같은 결과가 나온다.

#특별 데코레이터와 yield를 제외하고는 아무런 콜백함수가 나타나지 않았음을 확인할 수 있다.
#토론
#콜백과 관련있는 코드에서 현재 연산이 모두 연기되고 특정 포인트에서 재 시작한다는점
#연산이 재시작하면 프로세싱을 위해 콜백이 실행된다.