#문자열로 이름이 주어진 객체의 메소드 호출
#문제
#문자열로 저장된 메소드 이름을 가지고 있고, 이 메소드를 실행하고 싶다.
#해결
#간단한 경우 getattr()를 사용하면 된다.
import math
class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __repr__(self):
        return 'Point({!r:},{!r:}'.format(self.x,self.y)
    def distance(self):
        return math.hypot(self.x-x,self.y-y)
p=Point(2,3)
d=getattr(p,'distance')(0,0)
#혹은 operator.methodcaller()를 사용해도 된다.
import operator
operator.methodcaller('distance',0,0)(p)
#메소드를 이름으로 찾고 동일한 매개변수를 반복적으로 넣는 경우 operator.methodcaller()를 사용하는 것이 좋다. 예를 들어 포인트 리스트를 정렬하고 싶다면 다음과 같이 한다.
points = [Point(1,2), Point(3,0),Point(10,-3)]
points.sort(key=operator.methodcaller('distance',0,0))
#토론
#메소드 호출의 과정은 실제로 속성 탐색과 함수 호출이라는 두가지 과정으로 분리된다.
#따라서 메소드를 호출하려면, 다른 속성과 마찬가지로 우선 getattr()로 속성을 찾는다. 찾은 메소드를 호출하려면, 결과물을 함수로 여기면 된다.
#operator.methodcaller()는 호출 가능 객체를 생성하지만, 또한 메소드에 주어질 매개변수를 고정시키는 역할도 한다. 우리는 올바른 self인자를 제공하기만 하면 된다.
p = Point(3,4)
d = operator.methodcaller('distance',0,0)
d(p)
#문자열에 저장된 이름으로 메소드를 호출하는 방식은 case문을 이뮬레이트하거나 비지터 패턴의 변형과 어느정도 관련있음
