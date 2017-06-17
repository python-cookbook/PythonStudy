#새로운 클래스나 인스턴스 속성 만들기
#문제
#타입 확인 등과 같이 추가적 기능을 가진 새로운 종류의 인스턴스 속성을 만들고 싶다.
#해결
#완전히 새로운 종류의 인스턴스 속성을 만드려면, 그 기능을 디스크립터 클래스 형태로 정의해야한다.
#타입을 확인하는 정수형 디스크립터 속성
class Integer:
    def __init__(self,name):
        self.name = name
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self,instance,value):
        if not isinstance(value, int):
            raise  TypeError("Expected an int")
        instance.__dict__[self.name] = value

    def __delete__(self,instance):
        del instance.__dict__[self.name]
#디스크립터는 세가지 중요한 속성 접근 명령을 특별 메소드 형식으로 구현한 클래스이다. 이 메소드는 인스턴스를 입력으로 받는다. 그리고 인스턴스의 기반 딕셔너리는 속성으로 만들어진다.
#디스크립터를 사용하려면, 디스크립터의 인스턴스는 클래스 정의에 클래스 변수로 들어가야 한다.
class Point:
    x = Integer('x')
    y = Integer('y')
    def __init__(self,x,y):
        self.x=x
        self.y=y
#이렇게 할 때, 디스크립터에 대한 모든 접근은 __get__, __set__, __delete__ 메소드를 사용한다.
p = Point(2,3)
p.x

p.y=5
p.x=2.3
#입력으로 디스크립터의 모든 메소드는 가공중인 인스턴스를 받는다. 요청 받은 작업을 수행하기 위해서 인스턴스 딕셔너리 역시 적잘히 처리된다.
#디스크립터의 self.name 속성은 실제 데이터를 인스턴스 딕셔너리에 저장할 때 사용하는 딕셔너리 키를 가지고 있다.
#토론
#디스크립터는 파이썬 클래스 기능에 __slots__. @classmethod, @staticmethod, @property와 같이 멋진 도구를 제공한다.
#디스크립터를 정의하면 get,set,delete와 같이 중요한 인스턴스 연산을 아주 하위 레벨에서 얻고 어떻게 동작할 지도 입맛대로 바꿀 수 있다. 따라서 고급 라이브러리와 프레임워크를 작성하는 프로그래머에게
#매우 중요한 도구가 된다.
#디스크립터에 대해 한가지 헷갈리는 부분은 인스턴스 기반이 아닌 클래스 레벨에서만 정의가 가능하는 것이다. 따라서 다음과 같은 코드는 동작하지 않는다.
class Point:
    def __init__(self,x,y):
        self.x = Integer('x')
        self.y = Integer('y')
        self.x = x
        self.y = y

#또한 get메소드를 구현하는 것도 보기보다 간단하지 않다.
#타입을 확인하는 정수형 디스크립터 속성
class Integer:
    '''
    def __get__(self,instance,clas):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]
    '''

#__get__()이 복잡해 보이는 이유는 인스턴스 변수와 클래스 변수를 구분해야 하기 때문이다. 만약 디스크립터를 클래스 변수로 접근하면 instance 인자가 None이 된다.
#이 경우에는 단순히 디스크립터 자신을 반환하는 것이 일반적
p=Point(2,3)
p.x
Point.x
#디스크립터는 데코레이터나 메타 클래스가 들어가는 거대한 프로그래밍 프레임워크의 한 가지 요소가 되곤 한다. 보통 디스크립터의 사용은 겉으로 드러나지 않아 사용자에게 보이지 않는다.
#예를 들어 다음은 클래스 데코레이터를 사용하는 디스크립터 기반의 고급 코드이다..
#속성타입을 확인하는 디스크립터
class Typed:
    def __init__(self,name,expected_type):
        self.name=name
        self.expected_type=expected_type
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]
    def __set__(self, instance,value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected'+str(self.expected_type))
        instance.__dict__[self.name] = value
    def __delete__(self,instance):
        del instance.__dict__[self.name]

#선택한 속성에 적용되는 클래스 데코레이터
def typeassert(**kwargs):
    def decorate(cls):
        for name, expected_type in kwargs.items():
            setattr(cls,name,Typed(name,expected_type))
        return cls
    return decorate

#사용 예
@typeassert(name=str,shares=int,price=float)
class Stock:
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
#마지막으로 특정 클래스의 한 속성에 대한 접근을 제어하기 위해서 디스크립터를 사용하지 말아야 한다는 점이 중요하다.
#이런 경우 8.6에 나왔던 것처럼 프로퍼티를 사용해야한다.
#디스크립터는 코드 재사용이 빈번히 발생하는 상황에서 더 유용하다