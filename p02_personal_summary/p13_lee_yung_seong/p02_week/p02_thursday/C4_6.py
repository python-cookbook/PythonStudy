#추가 상태를 가진 제너레이터 함수 정의
#문제
#제너레이터 함수를 정의하고 싶지만, 사용자에게 노출할 추가적인 상태를 넣고 싶다.
#해결
#사용자에게 추가 상태를 노출하는 제너레이터를 원할 때, __iter__() 메소드에 제너레이터 함수 코드를 넣어서 쉽게 클래스로 구현할 수 있다는 점을 기억하자.
from collections import deque

class linehistory:
    def __init__(self,lines,histlen=3):
        self.lines = lines
        self.history = deque(maxlen = histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines,1):
            self.history.append((lineno,line))
            yield line
    def clear(self):
        self.history.clear()

#이 클래스를 사용하려면 일반 제너레이터 함수처럼 대해야 한다. 하지만 인스턴스를 만들기 때문에 history 속성이나 clear()메소드 같은 내부 속성에 접근할 수 있다.

#토론 제너레이터를 사용하면 모든 작업을 함수만으로 하려는 유혹에 빠지기 쉽다.
#만약 제너레이터 함수가 프로그램의 다른 부분과 일반적이지 않게(속성 노출, 메소드 호출로 조절하기 등) 상호작용해야 할 경우 코드가 꽤 복잡해 질 수 있다.
#이럴 때는 앞에서 본 대로 클래스 정의만을 사용한다. 제너레이터를 __iter__()메소드에 정의한다고 해도 알고리즘을 작성하는 방식에는 아무런 변화가 없다.
#클래스의 일부라는 점으로 인해 사용자에게 속성과 메소드를 쉽게 제공할 수 있다.
#for 문 대신 다른 기술을 사용해서 순환을 한다면 iter()를 호출할 때 추가적으로 작업을 해야할 필요가 생기기도 한다.