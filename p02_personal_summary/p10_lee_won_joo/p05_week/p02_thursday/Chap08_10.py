"""
게으른 계산을 하는 프로퍼티 사용

읽기 전용 속성을 프로퍼티로 정의하고, 이 속성에 접근할 때만 계산하도록 하고싶다!
한번 접근하고 나면 값을 캐시해놓고 ,다읍 번 접근할 땐 계산하지 않도록 하려면
"""

class lazyproperty:
    def __init__(self, func):
        self.func = func
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


#코드 활용 위해 클래스 내부에서 사용한다.

import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius

#사용하기
c = Circle(4.0)
print(c.radius)  #4
print(c.area)  #Computing area  50.26548245743669
print(c.area)  #50.26548245743669
print(c.perimeter)  #computing perimeter 25.132741228718345
print(c.perimeter)  #25.132741228718345

#computing area랑 perimeter 한번씩 나오는 점을 주목하자.
#get 주목?
#왜 한번만 나오고 말까?  lazy해서?   instance 가 none이 아니어서?


#대개의 경우 게으르게 계산 속성은 성능 향상을 위해 사용
#실제로 특정 값을 사용하기 전 까진 계산하지 않도록 하는 것
#클래스에 디스크립터가 들어가면 속성 접근 시 __Get__/set/delete 메소드 호출된다.

#하지만 디스크립터가 get메소드만 정의하면, 평소보다 약한 바인딩 갖게된다.
#특히 get 메소드는 접근하는 속성이 인스턴스 딕셔너리에 없을 때만 실행된다.



c = Circle(4.0)
#인스턴스 변수 구하기

print(vars(c))  #{'radius': 4.0}

#면적 계산 하고 추후 변수 확인

print(c.area)  #50.26548245743669

print(vars(c))  #{'radius': 4.0, 'area': 50.26548245743669}
#속성에 접근해도 더이상 프로퍼티를 다시 실행하지 않는다.   (computing 어쩌구가 뜨지 않잖아)

print(c.area)

#변수 삭제하고 프로퍼티 다시 실행됨을 확인하자.

del c.area
print(vars(c))  #{'radius': 4.0}
print(c.area)   # Computing area   50.26548245743669


#이번 레시피에서 불리한 점 한가지는 계산한 값을 생성한 후에 수정할 수 있다는 것

c.area
c.area = 25
c.area

def lazyproperty(func):
    name = '_lazy_'+ func.__name__
    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value
    return lazy


#이 버전을 사용하면 값 설정 불가능하게 된다.

c = Circle(4.0)
c.area

c.area

# c.area = 25




