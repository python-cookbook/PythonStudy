##########################################################################################################
# 7.11] 인라인 콜백 함수
#   * 콜백 함수를 사용하는 코드를 작성하는데, 크기가 작은 함수를 너무 많이 만들어낼까 걱정된다.
#     코드가 좀 더 정상적인 절차적 단계를 거치게 하고 싶다.
#
#   * 아래 예시는 콜백 함수, 제너레이터, 컨트롤 플로우를 이해하는데 큰 도움이 된다.
#     자세한 것은 Ch7-11 토론 참조
##########################################################################################################

def apply_async(func, args, *, callback):
    # 결과 계산
    result = func(*args)

    # 결과 값으로 콜백 함수 호출
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

# yield 구문으로 콜백 단계를 인라인(inline)할 수 있다.
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
    print('Good bye')

if __name__ == '__main__':
    import multiprocessing
    pool = multiprocessing.Pool()
    apply_async = pool.apply_async

    # test 함수 실행
    test()