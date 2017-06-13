#콜백함수에 추가적 상태 넣기
#문제
#콜백함수를 사용하는 코드를 작성중이다. 이때 콜백 함수에 추가 상태를 넣고 내부 호출에 사용하고 싶다.
#해결
#이 레시피는 많은 라이브러리와 프레임워크에서 찾을 수 있는 콜백 함수의 활용을 알아본다. 예제를 위해 콜백 함수를 호출하는 다음 함수를 정의한다.
def apply_async(func,args,*,callback):
    #결과계산
    result = func(*args)
    #결과 값으로 콜백 함수 호출
    callback(result)

#실제 어플리케이션이라면 이런 코드에서는 스래드, 프로세스, 타이머 등과 관련 있는 고급 동작을 구현하겠지만, 여기서는 그런 것이 중요하지 않으므로 건너뛰고
#콜백 호출 자체에만 집중한다. 이 코드를 사용하는 예제는 다음과 같다.
def print_result(result):
    print('Got :',result)

def add(x,y):
    return x+y

apply_async(add,(2,3),callback=print_result)
#앞에 나왔듯이 print_result 함수느 ㄴ결과 값만 하나의 인자로 받는다. 다른 어떠한 정보도 전달 받지 않는다.
#이렇게 부족한 정보로 인해 콜백 함수가 다른 변수나 환경 등과 통신 할 때 문제가 발생하기도 한다.
#콜백 함수에 추가 정보를 넣는 한가지 방법은 하나의 함수 대신 바운드-메소드를 사용하는 것이다. 예를 들어 이 클래스는 결과 값을 받을 때마다 늘어나는 내부 시퀀스 숫자를 가지고 있다.
class ResultHanler:
    def __init__(self):
        self.sequence = 0
    def handler(self,result):
        self.sequence +=1
        print('[{}] GOT : {}'.format(self.sequence,result))
#이 클래스를 사용하려면 인스턴스를 만들고 바운드 메소드 hadler를 콜백으로 사용해야 한다.
r=ResultHanler()
apply_async(add,(2,3),callback=r.handler)

#클래스의 대안으로 클로저를 사용해서 상태를 저장해도 된다.
def make_hadler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] GOT : {}'.format(sequence,result))

    return handler
#이 방법은 예제는 다음과 같다
handler = make_hadler()
apply_async(add,(2,3),callback=handler)

#추가적인 인자와 파셜 함수 애플리케이션으로 콜백에 상태를 넣을 수 있다.
class SequnceNo:
    def __init__(self):
        self.sequence = 0
    def handler(self,seq):
        seq.sequnce +=1
        print('[{}] GOT : {}'.format(seq.sequnce, result))
#토론
#콜백 함수를 사용하는 프로그램은 엉망으로 망가질 위험 요소를 안고 있다.
#콜백 함수가 여러 단계에 걸쳐 실행을 계속 하도록 만드릭 위해서는 어떻게 관련 상태를 저장하고 불러올지 정해야 한다.
#상태를 고정시키고 저장하는 방식에는 크게 두가지가 있다. 인스턴스에 상태르 저장하거나 혹은 클로저에 저장한다.
