#게으른 계산을 하는 프로퍼티 사용
#문제
#읽기 전용 속성을 프로퍼티로 정의하고 이 속성에 접근할 때만 계산하도록 하고 싶다. 하지만 한번 접근하고 나면 이 값을 캐시해 놓고 다음번에 접근할 때는 다시 계산하지 않도록 하고 싶다.
#해결
#게이른 속성을 효율적으로 정의하기 위해서는 다음과 같이 디스크립터 클래스를 사용
class lazyproperty:
    def __init__(self,func):
        self.func=func
    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance,self.func.__name__,value)
            return value

#이 코드를 사용하기 위해서는 다음과 같이 클랫 ㅡ내부에서 사용한다.
import math
class Circle:
    def __init__(self,radius):
        self.radius = radius
    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius**2
    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius

#다음은 앞에 나온 코드를 사용하는 예이다.
c = Circle(4.0)
c.radius
c.area

#토론
#대개의 경우 게으르게 계산한 속성은 성능 향상을 위해 사용한다. 예를 들어 실제로 특정 값을 사용하기 전까지 계산하지 않도록 하는 것이다.
#제시한 해결책은 단지 이것만 하지만., 아주 효율적인 방식으로 이를 실행하기 위해 디스크립터의 미묘한 기능을 활용하고 있다.
#다른 레시피에 나온 것처럼 클래스에 디스크립터가 들어가면 속성 접근 시 겟,셋,딜리트 메소드를 호출한다. 하지만 디스크립터가 겟메소드만 정의하면
#평소보다 약한 바인딩을 갖게 된다.
#특히 겟 메소드는 접근 하는 속성이 인스턴스 딕셔너리에 없을 때만 실행된다.
#Lazyproperty 클래스는 프로퍼티 자체와 동일한 이름을 사용해서 인스턴스 __get__() 메소드에 계산한 값을 저장하는 식으로 이를 활용한다.
#이렇게 하면 그 값은 인스턴스 딕셔너리에 저장되고 추후 프로퍼티의 계산을 하지 않도록 한다. 예제를 조금 자세히 살펴서 동작성을 확인해보자.
c=Circle(4.0)
vars(c)

c,area
vars(c)

c.area
del c.area
vars(c)
c.area
# 이번 레시피에서 불리한 점 한가지는 계산한 값을 생성한 후에 수정할 수 있다는 것이다.
#이 부분이 걱정이 된다면 조금 덜 효율적인 구현을 할 수 있다.
def lazyproperty(func):
    name = '_lazy_ ' +func.__name__
    @property
    def lazy(self):
        if hasattr(self,name):
            return getattr(self,name)
        else:
            value = func(self)
            setattr(self,name,value)
            return value
    return lazy
#이 버전을 사용하면 값 설정이 불가능하게됨
#하지만 값을 얻기 위해서 항상 프로퍼티의 게터함수를 사용해야 한다는 불편함이 생긴다.
#이 방식은 원래 해결책에 나왔던 것처럼 단순히 인스턴스 딕셔너리에서 값을 찾는 것보다 비효율적이다.

