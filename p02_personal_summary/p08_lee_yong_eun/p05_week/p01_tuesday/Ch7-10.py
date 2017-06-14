##########################################################################################################
# 7.10] 콜백 함수에 추가적 상태 넣기
#   * 콜백 함수를 사용하는 코드를 작성 중이다(이벤트 핸들러, 완료 콜백 등).
#     이때 콜백 함수에 추가 상태를 넣고 내부 호출에 사용하고 싶다.
#
#   * 아래의 apply_async 함수가 callback 함수를 사용하는 예제이다.
#     앞의 print_result 함수는 결과 값만 하나의 인자로 받는다. 이런 콜백 함수에 추가 정보를 넣는 한 가지 방법은
#       하나의 함수 대신 바운드-메소드(Bound-Method)를 사용하는 것이다.
#       예를 들어 아래의 ResultHandler 클래스의 handler 함수는 내부 시퀀스 숫자를 가진다.
##########################################################################################################

def apply_async(func, args, *, callback):
    # 결과 계산
    result = func(*args)

    # 결과 값으로 콜백 함수 호출
    callback(result)

# 예제
def print_result(result):
    print('Got: ', result)

def add(x, y):
    return x + y

apply_async(add, (2, 3), callback=print_result)                 # Got:  5
apply_async(add, ('hello', 'world'), callback=print_result)     # Got:  helloworld

# 클래스를 사용한 추가 정보
class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got : {}'.format(self.sequence, result))

r = ResultHandler()
apply_async(add, (2, 3), callback=r.handler)

# 클로저를 사용한 추가 정보
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got : {}'.format(sequence, result))
    return handler

handler = make_handler()
apply_async(add, (2, 3), callback=handler)

# 코루틴을 사용한 추가 정보
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got : {}'.format(sequence, result))

handler = make_handler()
next(handler)   # Advance to the yield
apply_async(add, (2, 3), callback=handler.send)

# 파셜 함수 애플리케이션을 사용한 추가 정보
class SequenceNo:
    def __init__(self):
        self.sequence = 0

def handler(result, seq):
    seq.sequence += 1
    print('[{}] Got : {}'.format(seq.sequence, result))

seq = SequenceNo()
from functools import partial
apply_async(add, (2, 3), callback=partial(handler, seq=seq))

