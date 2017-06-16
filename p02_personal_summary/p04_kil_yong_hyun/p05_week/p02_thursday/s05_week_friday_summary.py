#  8.6 관리 속성 만들기
#  ▣ 문제 : 인스턴스 속성을 얻거나 설정할 때 추가적인 처리(타입 체크, 검증 등)를 하고 싶다.
#  ▣ 해결 : 속성에 대한 접근을 조절하고 싶으면 "프로퍼티(property)"로 정의하면 된다.
class Person:
    def __init__(self, first_name):
        # self.first_name = first_name 은 초기화시에 setter 함수를 사용해서 _first_name 에 입력한다.
        # self._first_name = first_name 은 초기화시에 직접 _first_name 에 입력한다.
        self.first_name = first_name

    # getter 함수
    @property
    def first_name(self):
        return self._first_name

    # setter 함수
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # deleter 함수
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")

a = Person('Guido')
print(a.first_name)
a.first_name = 4
del a.first_name

#   - 이미 존재하는 get 과 set 메소드로 프로퍼티를 정의하는 방법.
class Person:
    def __init__(self, first_name):
        self.set_first_name(first_name)

    # getter
    def get_first_name(self):
        return self._first_name

    # setter
    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # deleter
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")

    # setter/getter 메소드로 프로퍼티 만들기
    name = property(get_first_name, set_first_name, del_first_name)

#  ▣ 토론 : 사실 프로퍼티 속성은 함께 묶여 있는 메소드 컬렉션이다.
#           프로퍼티가 있는 클래스를 조사해 보면 프로퍼티 자체의 fget, fset, fdel 속성에서 로우 메소드를 찾을 수 있다.
person = Person('Guido')
print(Person.first_name.fget)
print(Person.first_name.fset)
print(Person.first_name.fdel)


#   - 프로퍼티는 속성에 추가적인 처리가 필요할 때만 사용해야 한다.
class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

# - 프로퍼티는 계산한 속성을 정의할 때 사용하기도 한다.
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius ** 2

    @property
    def perimeter(self):
        return 2 * math.pi * self.radius

c = Circle(4.0)
print(c.radius)
print(c.area)
print(c.perimeter)

#   - 프로퍼티로 우아한 프로그래밍 인터페이스를 얻을 수 있지만, 게터와 세터 함수를 직접 사용하는 것도 가능하다.
p = Person('Guido')
print(p.get_first_name())
p.set_first_name('Larry')

#   - 프로퍼티 정의를 반복적으로 사용하는 파이썬 코드를 작성하지 않도록 주의 하자.
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._last_name = value


#  8.7 부모 클래스의 메소드 호출
#  ▣ 문제 : 오버라이드된 서브클래스 메소드가 아닌 부모 클래스에 있는 메소드를 호출하고 싶다.
#  ▣ 해결 : 부모의 메소드를 호출하려면 super() 함수를 사용한다.
class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()  # 부모의 spam() 호출

#  ※ super() 는 일반적으로 __init__() 메소드에서 부모를 제대로 초기화하기 위해 사용한다.

#   - 파이썬의 특별 메소드를 오버라이드한 코드에서 super() 를 사용하기도 한다.
class Proxy:
    def __init__(self, obj):
        self._obj = obj

    # 내부 obj 를 위해 델리게이트(delegate) 속성 찾기
    def __getattr__(self, item):
        return getattr(self._obj, item)

    # 델리게이트(delegate) 속성 할당
    def __setattr__(self, key, value):
        if key.startswith('_'):
            super().__setattr__(key, value)
        else:
            setattr(self._obj, key, value)

#  ▣ 토론 : super() 함수를 올바르게 사용하기는 무척 어렵다.
#           때때로 부모 클래스 메소드를 직접 호출하기 위해 다음과 같이 작성한 코드를 볼 수 있다.
class Base:
    def __init__(self):
        print('Base.__init__')

class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')

class B(Base):
    def __init__(self):
        Base.__init__(self)
        print('B.__init__')

class C(A, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')

c = C()

#   - 위의 코드는 Base 클래스를 두 번 호출한다. super() 를 사용하여 코드를 수정한다면 올바르게 동작한다.
class Base:
    def __init__(self):
        print('Base.__init__')

class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')

class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')

class C(A, B):
    def __init__(self):
        super().__init__()
        print('C.__init__')

c = C()

#   - 클래스를 정의할 때마다 파이썬은 메소드 처리 순서(method resolution order, MRO) 리스트를 계산한다.
#     MRO 리스트는 모든 베이스 클래스를 단순히 순차적으로 나열한 리스트이다.
print(C.__mro__)

#  ※ 부모 클래스의 MRO 를 다음 세 가지 제약 조건하에서 합병 정렬한다.
#   - 자식 클래스를 부모보다 먼저 확인한다.
#   - 부모 클래스가 둘 이상이면 리스팅한 순서대로 확인한다. C(A, B) : A -> B
#   - 유효한 후보가 두 가지 있으면, 첫 번째 부모 클래스부터 선택한다.

#   - super() 의 놀라운 측면 중 하나는 이 함수가 MRO 의 바로 위에 있는 부모에 직접 접근하지 않을 때도 있고, 직접적인 부모 클래스가
#     없을 때도 super() 를 사용할 수 있다는 점이다.
class A:
    def spam(self):
        print('A.spam')
        super().spam()

a = A()
a.spam()
#   - 위의 코드는 AttributeError: 'super' object has no attribute 'spam' 에러 메시지가 발생한다.
class B:
    def spam(self):
        print('B.spam')

class C(A, B):
    pass

c = C()
c.spam()
print(C.__mro__)


#  8.8 서브클래스에서 프로퍼티 확장
#  ▣ 문제 : 서브클래스에서, 부모 클래스에 정의한 프로퍼티의 기능을 확장하고 싶다.
#  ▣ 해결 : 프로퍼티를 정의하는 다음 코드를 보자.
class Person:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")

class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)  # super(클래스, 서브클래스 or 인스턴스)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)

s = SubPerson('Guido')
s.name
s.name = 'Larry'
s.name = 42

#   - 프로퍼티의 메소드 하나를 확장하고 싶은 경우
class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('Getting name')
        return super().name

#   - 세터 하나만 확장하는 경우
class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

#  ▣ 토론 : 서브클래스의 프로퍼티를 확장하면 프로퍼티가 하나의 메소드가 아닌 게터, 세터, 딜리터 메소드의 컬렉션으로 정의되었다는 사실로 인해
#           자잘한 문제가 발생한다.
#           따라서 프로퍼티를 확장할 때 모든 메소드를 다시 정의할지, 메소드 하나만 다시 정의할지 결정해야 한다.

#   - 메소드 중 하나만 재정의하려면 @property 자체만 사용하는 것으로는 충분하지 않다.
class SubPerson(Person):
    @property
    def name(self):  # 동작하지 않음
        print('Getting name')
        return super().name

s = SubPerson('Guido')  # AttributeError: can't set attribute

#   - 디스크립터를 확장하는데 사용되는 방법.

# 디스크립터
class String:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(instance, str):
            raise TypeError('Expected a string')
        instance.__dict__[self.name] = value

class Person:
    name = String('name')

    def __init__(self, name):
        self.name = name

class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)

s = SubPerson('Guido')

#  8.9 새로운 클래스나 인스턴스 속성 만들기
#  ▣ 문제 : 타입 확인 등과 같이 추가적 기능을 가진 새로운 종류의 인스턴스 속성을 만들고 싶다.
#  ▣ 해결 : 완전히 새로운 종류의 인스턴스 속성을 만들려면, 그 기능을 디스크립터 클래스 형태로 정의해야 한다.
class Integer:
    def __init__(self, name):
        self.name = name  # 실제 데이터를 인스턴스 딕셔너리에 저장할 때 사용하는 딕셔너리 키를 가지는 변수.

    def __get__(self, instance, owner):
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

#   - 디스크립터는 세 가지 중요한 속성 접근 명령을 특별 메소드 __get__(), __set__(), __delete__() 형식으로 구현한 클래스이다.
#     이 메소드는 인스턴스를 입력으로 받는다. 그리고 인스턴스의 기반 딕셔너리는 속성으로 만들어진다.
#     디스크립터를 사용하려면, 디스크립터의 인스턴스는 클래스 정의에 클래스 변수로 들어가야 한다.
class Point:
    x = Integer('x')
    y = Integer('y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(2, 3)
p.x
p.y = 5
p.x = 2.3  # TypeError: Expected an int
#   ※ 입력으로, 디스크립터의 모든 메소드는 가공 중인 인스턴스를 받는다.
#      요청 받은 작업을 수행하기 위해서, 인스턴스 딕셔너리 역시 적절히 처리된다.
#      디스크립터의 self.name 속성은 실제 데이터를 인스턴스 딕셔너리에 저장할 때 사용하는 딕셔너리 키를 가지고 있다.

#  ▣ 토론 : 디스크립터는 파이썬 클래스 기능에 __slots__, @classmethod, @staticmethod, @property 와 같이 멋진 도구를 제공한다.
#            디스크립터를 정의하면 get, set, delete 와 같이 중요한 인스턴스 연산을 아주 하위 레벨에서 얻고 어떻게 동작할지도 입맛대로 바꿀 수 있다.
#            따라서 고급 라이브러리와 프레임워크를 작성하는 프로그래머에게 매우 중요한 도구가 된다.
#            단, 인스턴스 기반이 아닌 클래스 레벨에서만 정의가 가능하다.
#            따라서 다음과 같은 코드는 동작하지 않는다.
class Point:
    def __init__(self, x, y):
        self.x = Integer('x')
        self.y = Integer('y')
        self.x = x
        self.y = y

#   - 또한 __get__() 메소드를 구현하는 것도 보기보다 간단하지 않다.
class Integer:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

#    - __get__() 이 조금 복잡해 보이는 이유는 인스턴스 변수와 클래스 변수를 구분해야 하기 때문이다.
#      만약 디스크립터를 클래스 변수로 접근하면 instance 인자가 None 이 된다.
#      이 경우에는 단순히 디스크립터 자신을 반환하는 것이 일반적이다.
p = Point(2, 3)
p.x      # Point.x.__get__(p, Point) 호출
Point.x  # Point.x.__get__(None, Point) 호출

#   - 다음은 클래스 데코레이터를 사용하는 디스크립터 기반의 고급 코드이다.
class Typed:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected ' + str(self.expected_type))
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

def typeassert(**kwargs):  # 선택한 속성에 적용되는 클래스 데코레이터
    def decorate(cls):
        for name, expected_type in kwargs.items():
            setattr(cls, name, Typed(name, expected_type))
        return cls
    return decorate

@typeassert(name=str, shares=int, price=float)
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
#   ※ 특정 클래스의 한 속성에 대한 접근을 제어하기 위해서 디스크립터를 사용하지 말아야 한다.
#      이런 경우에는 프로퍼티를 사용해야한다. 디스크립터는 코드 재사용이 빈번히 발생하는 상황에 더 유용하다.


#  8.10 게으른 계산을 하는 프로퍼티 사용
#  ▣ 문제 : 읽기 전용 속성을 프로퍼티로 정의하고, 이 속성에 접근할 때만 계산하도록 하고 싶다.
#            하지만 한 번 접근하고 나면 이 값을 캐시에 놓고 다음 번에 접근할 때에는 다시 계산하지 않도록 하고 싶다.
#  ▣ 해결 : 게으른 속성을 효율적으로 정의하기 위해서는 다음과 같이 디스크립터 클래스를 사용한다.
class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

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

c = Circle(4.0)
c.radius
c.area
c.area
c.perimeter
c.perimeter

#  ▣ 토론 : 대개의 경우 게으르게 계산한 속성은 성능 향상을 위해 사용한다.
#            예를 들어 실제로 특정 값을 사용하기 전까지 계산하지 않도록 하는 것이다.
c = Circle(4.0)
print(vars(c))
c.area
print(vars(c))
c.area
del c.area
print(vars(c))
c.area
print(vars(c))
#   - 이번 레시피에서 불리한 점 한 가지는 계산한 값을 생성한 후에 수정할 수 있다는 것이다.
c.area
c.area = 25
c.area

#   - 이 부분이 걱정이 된다면 조금 덜 효율적인 구현을 할 수 있다.
def lazyproperty(func):
    name = '_lazy_' + func.__name__
    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value
    return lazy

c = Circle(4.0)
c.area
c.area
c.area = 25

#   ※ 위의 버전은 값을 얻기 위해서 항상 프로퍼티의 getter 함수를 사용해야 한다는 불편함이 생긴다.


#  8.11 자료 구조 초기화 단순화하기
#  ▣ 문제 : 자료 구조로 사용하는 클래스를 작성하고 있는데, 반복적으로 비슷한 __init__() 함수를 작성하기에 지쳐 간다.
#  ▣ 해결 : 자료 구조의 초기화는 베이스 클래스의 __init__() 함수를 정의하는 식으로 단순화할 수 있다.
class Structure:
    _fields = []
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    class Point(Structure):
        _fields = ['x', 'y']

    class Circle(Structure):
        _fields = ['radius']
        def area(self):
            return math.pi * self.radius ** 2

s = Stock('ACME', 50, 91.1)
p = Point(2, 3)
c = Circle(4.5)
s2 = Stock('ACME', 50)

#   - 키워드 매개변수를 지원하기로 결정했다면 사용할 수 있는 디자인 옵션이 몇 가지 있다.
#     그 중 한 가지는 키워드 매개변수를 매핑해서 _fields 에 명시된 속성 이름에만 일치하도록 만드는 것이다.
class Structure:
    _fields = []
    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))

        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))

if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, price=91.1)
    s3 = Stock('ACME', shares=50, price=91.1)

#   - 혹은 _fields 에 명시되지 않은 구조에 추가적인 속성을 추가하는 수단으로 키워드 매개변수를 사용할 수 있다.
class Structure:
    _fields = []

    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        extra_args = kwargs.keys() - self._fields
        for name in extra_args:
            setattr(self, name, kwargs.pop(name))

        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))

if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, 91.1, date='8/2/2012')

#  ▣ 토론 : 제너럴한 목적으로 __init__() 메소드를 정의하는 기술은 규모가 작은 자료 구조를 대량으로 만드는 프로그램에 유용하다.
#            이 기술은 다음과 같이 일일이 __init__() 메소드를 작성하는 것에 비해 훨씬 코드의 양을 줄여 준다.

#   - 프레임 핵을 사용하면 인스턴스 변수를 자동으로 초기화할 수 있다.
def init_fromlocals(self):
    import sys
    locs = sys._getframe(1).f_locals
    for k, v in locs.items():
        if k != 'self':
            setattr(self, k, v)

class Stock:
    def __init__(self, name, shares, price):
        init_fromlocals(self)
