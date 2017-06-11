#클로저 내부에서 정의한 변수에 접근
#문제
#클로저는 확장해서 내부 변수에 접근하고 수정하고 싶다.
#해결
#일반적으로 클로저 내부 변수는 외부와 완전히 단절 되어 있다. 하지만 접근 함수를 만들고 크로저에 함수 속성으로 붙이면 내부 변수에 접근할 수 있다.
def sample():
    n = 0
    #클로저
    def func():
        print('n=',n)

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
f.set_n(10)
f()
f.get_n()
#토론
#이번 레시피를 ㅣㅇ루는 두가지 주요기능이 있다. 첫째는 nonlocal 선언으로 내부변수를 수정하는 함수를 작성하는 것이고, 두번째는 접근 메소드를 클로저 함수에 붙여 마치 인스턴스 메소드인 것처럼 동작하는 것이다.
#이번 레시피를 조금 확장해서클로저를 마치 클래스의 인스턴스 인 것처럼 동작하게 만들 수 있다. 내부 함수를 인스턴스 딕셔너리에 복사하고 반환하기만 하면 된다.
import sys
class ClosureInstance:
    def __init__(self,locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals

    #인스턴스 딕셔너리를 호출체로 갱신
        self.__dict__.update((key,value) for key, value in locals.items() if callable(value))

        def __len__(self):
            return self.__dict__['__len__']()

def Stack():
    items = []
    def push(item):
        item.append(item)
    def pop():
        return items.pop()
    def __len__():
        return len(items)

    return ClosureInstance()

#실제 동작
s = Stack()
s
s.push(10)
#이 코드는 일반 클래스 저으이보다 실행속도가 빠름.