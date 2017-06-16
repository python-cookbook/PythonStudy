
"""
8.9 새로운 클래스 or 인스턴스 속성 만들기.

타입 확인 등과 같이 추가적 기능을 가진 새로운 종류의 인스턴스 속성을 만들고 싶다.

완전히 새로운 종류의 인스턴스 속성을 만들려면, 그 기능을 디스크립터 클래스 형태로 정의해야 한다.


"""


# 타입을 확인하는 정수형 디스크립터 속성

class Integer:
    def __init__(self , name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

# 디스크립터는 세가지 중요한 속성 접근 명령(get, set, delete) 을 특별 메소드 형식으로 구현한 클래스이다.
# __Get__(), __set__(), __delete__() 형식으로 구현한 클래스이다.
# 이 메소드는 인스턴스를 입력으로 받는다.
#그리고 인스턴스의 기반 딕셔너리는 속성으로 만들어 진다.


class Point:
    x = Integer('x')
    y = Integer('y')
    def __init__(self,x,y):
        self.x = x
        self.y = y

#이렇게 할 때, 디스크립터에 대한 모든 접근 은 get,set,delete 메소드를 사용한다.

# p = Point(2,3)
# print(p.x)   # Point.x.__get__(p.Point) 호출
#TypeError: Expected an int
# p.y = 5   #Point.y.__set(p,5)호출
# p.x = 2.3  #Point.x.__set(p,2,3) 호출


# 입력으로 디스크립터의 모든 메소드는 가공 중인 인스턴스를 받는다.
# 요청 받은 작업을 수행하기 위해서, 인스턴스 딕셔너리 역시 적절히 처리된다.
#디스크립터의 self.name 속성은 실제 데이터를 인스턴스 딕셔너리에 저장할 때 사용하는 딕셔너리 키를 가지고 있다.





#디스크립터는 파이썬 클래스 기능에 __slots__, @classmethod, #staticmethod #property 제공


class Point:
    def __init__(self,x,y):
        self.x = Integer('x')
        self.y = Integer('y')
        self.x = x
        self.y = y

# get 메소드 구현했을 떄 코드
class Integer:
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

#get이 더 복잡해 보이는 이유는, 인스턴스 변수와 클래스 변수를 구분해야 하기 때문이다.
#만약 디스크립터를 클래스 변수로 접근하면 instance 인자가 None이 된다.
#이 경우, 단순히 디스크립터 자신을 반환하는 것이 일반적이다.  (물론 다른 처리를 해도 무방하다.)


p = Point(2,3)
# p.x     #Point.x.__get__(p,Point) 호출
# Point.x  #Point.x.__get__(None,Point) 호출


#디스크립터는 데코레이터나 메타클래스가 들어 가는 거대한 프로그래밍 프레임웤의 한 가지 요소가 되곤 한다.

#보통 디스크립터의 사용은 겉으로 드러나지 않아, 사용자에게 보이지 않는데, 다음은 고급코드이다.


class Typed:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type

    def __Get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected'+str(self.expected_type))
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


    #선택한 속성에 적용되는 클래스 데코레이터 (decorator)
def typeassert(**kwargs):
    def decorate(cls):
        for name, expected_type in kwargs.items():
            # 클래스에 typed 디스크립터 설정
            setattr(cls, name, Typed(name, expected_type))
        return cls
    return decorate

#ex)

@typeassert(name=str, shares=int, price=float)
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

#마지막으로 특정 클래스의 한 속성에 대한 접근을 제어하기 위해서 디스크립터를 사용하지 말아야 한다는 점이 중요하다.
#이런 경우 프로퍼티를 사용해야 한다.
#디스크립터는 코드 재사용이 빈번히 발생하는 상황에서 더 유용하다.
#ex) 디스크립터가 제공하는 기능을 수백 군데에서 사용해야 한다거나, 라이브러리 기능으로 제공해야 하는 경우.





