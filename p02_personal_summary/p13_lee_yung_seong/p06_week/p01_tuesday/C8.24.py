#비교연산을 지원하는 클래스 만들기
#문제
#표준 비교 연산자를 사용해 클래스 인스턴스를 비교하고 싶다. 하지만 특별 메소드를 너무 많이 작성하고 싶지는 않다.
#해결
#파이썬 클래스는 비교 연산을 위한 특별 메소드를 통해 인스터스간에 비교 기능을 지원한다.
#예를 들어 >= 연산을 지원하려면 __ge__()메소드를 정의하면 된다. 메소드 하나를 정의하는 것은 아무런 문제가 없지만 모든 비교 연산을 구현하려면 그 과정이 조금 귀찮아 진다.
#이때 functools.total_ordering 데코레이터를 사용하면 과정을 단순화 할 수 있다. 클래스에 데코레이터를 붙이고 __eq__()와 비교 메소드 하나만 더 정의하면 된다.
#그렇게 하면 데코레이터가 나머지 모든 메소드를 자동으로 추가해 준다.
#이해를 돕기 위해 집을 하나 만들고 방을 추가한다. 그리고 집의 크기를 비교해보자.
from functools import total_ordering
class Room:
    def __init__(self,name,length,width):
        self.name=name
        self.length=length
        self.width=width
        self.square_feet=self.length * self.width

@total_ordering
class House:
    def __init__(self,name,style):
        self.name=name
        self.style=style
        self.rooms=list()

    @property
    def living_space_footage(self):
        return sum(r.square_feet for r in self.rooms)
    def add_room(self,room):
        self.rooms.append(room)
    def __str__(self):
        return '{} : {} square foot {}'.format(self.name, self.living_space_footage, self.style)
    def __eq__(self,other):
        return self.living_space_footage == other.living_space_footage
    def __lt__(self,other):
        return self.living_space_footage < other.living_space_footage

#이 코드에서 House 클래스를 @total_ordering으로 꾸몄다. 그리고 집의 전체 크기를 비교하는 __eq__()와 __lt__()를 정의했다. 이렇게 최소한의 정의만 하면 나머지 모든 비교 연산도 정상적으로 동작한다.
h1=House('h1','cape')
h1.add_room(Room('Master Bedroom',14,21))
h2=House('h2','ranch')
h2.add_room(Room('Master Bedroom',14,21))

houses=[h1,h2]
print(h1>h2)

#토론
#기본 비교 연산을 모두 지원하는 클래스를 작성해 본 적이 있다면 total_ordering의 동작성을 이해할 수 있을 것이다. 이 데코레이터는 비교-지원 메소드에서 다른 모든 메소드로의 매핑을 정의한다.
#따라서 __lt__()를 클래스에 정의하면 다른 비교 연산이 이 메소드를 사용한다. 다음과 같이 클래스ㅡㄹ 메소드로 채워주는 것과 다를 바가 없는 것이다.
class House:
    def __eq__(self,other):
        '''

        :param other:
        :return:
        '''
    def __lt__(self,other):
        pass
#@total_ordering이 생성한 메소드
__le__=lambda self,other : self<other or self == other
__gt__=lambda self,other : not (self<other or self == other)
__ge__=lambda self,other : not (self < other)
__ne__=lambda self,other : not self==other
# 물론 이런 메소드를 직접 작성하는 것이 어렵지는 않지만 있는거 쓰자.