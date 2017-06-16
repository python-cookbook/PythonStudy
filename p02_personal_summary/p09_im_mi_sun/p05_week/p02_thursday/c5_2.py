#######8.5 클래스 이름의 속성화
#클래스 인스턴스의 프라이빗 데이터를 캡슐화하고 싶은 경우 _, __ 사용

class A:
    def __init__(self):
        self._internal = 0 #내부 속성
        self.public = 1 #공용속성

    def public_method(self):
        '''
        A public method
        :return:
        '''
    def internal_method(self):
        ...

#파이썬은 내부 이름에 누군가 접근하는 것을 실제로 막지는 않음
#이름 앞에 밑줄 : 모듈 이름(내부구현), 모듈 레벨 함수에도 사용.sys._getframe()과 같은 모듈 레벨 함수는 사용 조심

#클래스 정의에 __로 시작하는 이름 : 이름이 다른 것으로 변함
#앞에 나온 프라이빗 속성은 _B__private / _B__private_method로 이름이 변함
# 속성을 통해 오버라이드 할 수 없음
class B:
    def __init__(self):
        self.__private = 0
    def __private_method(self):
        ...
    def public_method(self):
        ...
        self.__private_method()

class C(B):
    def __init__(self):
        super().__init__()
        self.__private = 1 #B.__private를 오버라이드 하지 않음
    def __private_method(self):
        ...

###__private / __private_method이름이 _C~~로 바뀜

#프라이빗 속성에 대한 두가지 규칙 ( _, __)
#대개의 경우 공용이 아닌 이름은 밑줄 하나
#코드가 서브 클래싱 사용 & 서브 클래스에 숨겨야 할 내부 속성이 있으면 __ 붙임

#예약해 둔 단어 이름과 충돌하는 변수를 정의하고자 할 때 이름뒤에 밑줄
lambda_ =2.0 #lambda 키워드와의 충돌을 피하기 위해 밑줄을 붙임
#밑줄을 변수 앞에 붙이지 않는 이유는 내부적으로 사용하는 의도와의 혼동을 피하기 위함


#######8.6 관리 속성 만들기
# 인스턴스 속성을 얻거나 설정할 때 추가적인 처리(타입 체크, 검증 등)을 하고 싶을 때
# 속성에 대한 접근 조절은 property로 정의

#속성에 간단한 타입 체크를 추가하는 프로퍼티를 정의하는 예시
class Person:
    def __init__(self,first_name):
        self.first_name = first_name

    #getter func
    @property
    def first_name(self):
        return self._first_name

    #setter func
    @first_name.setter
    def first_name(self,value):
        if not isinstance(value,str):
            raise TypeError ( 'Expected a string')
    #deleter func(option)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("can't delete attribute")

# 모두 같은 이름을 가져야 함
#첫번째 메소드 getter함수 : first_name을 프로퍼티로 만듦
#다른 두메소드는 추가적으로 세터 딜리터 함수를 first_name프로퍼티에 추가
# @first_name.setter @first_name.delete 데코레이터는 @property를 사용해서 first_name을 만들어 놓지 않으면 정의되지 않음!!!!

#프로퍼티의 중요 기능으로 일반적인 속성으로 보이지 않는다는 점이 있음 여기에 접근하면 자동으로 게터,세터,딜리터 메소드 실행
a = Person('Guido')
a.first_name #게터 호출
a.first_name = 42 #세터 호출
del a.first_name

# 프로퍼티 구현 시 기반데이터가 있으면 여전히 어딘가에 저장해야함
# 게터,세터 메소드에서 _first_name 속성을 직접 다루는데 여기에 실제 데이터가 들어감

# __init__()에서 self._first_name이 아닌 self.first_name을 설정하는 이유?
#프로퍼티의 모든 포인트는 속성에 타입 체킹을 적용하는 것에 집중
#따라서 초기화할 경우에도 이걸 확인하고 싶음
#self.first_name을 설정하면 설정 연산이 세터 메소드를 사용함) self._first_nameㅇ ㅔ접근하여 우회하는 것과는 대조적

#이미 존재하는 get과 set메소드로 프로퍼티 정의 가능
class Person:
    def __init__(self,first_name):
        self.set_first_name(first_name)
    #getter
    def get_first_name(self):
        return self._first_name
    #setter
    def set_first_name(self,value):
        if not isinstance(value,str):
            raise TypeError('expected a string')
        self._first_name = value

    #deleter
    def del_first_name(self):
        raise AttributeError('cant delete attribute')

    #기존 게터/세터 메소드로 프로퍼티 만들기
    name = property(get_first_name, set_first_name, del_first_name)

#프로퍼티 속성은 함께 묶여 잇는 메소드 컬렉션
#프로퍼티가 있는 클래스를 조사해보면 프로퍼티 자체의 fget, fset, fdel속성에서 로두 메소드를 찾을 수 있음
#일반적으로 fget, fset을 직접 호출하지는 않고 프로퍼티에 접근할 때 자동으로 실행 됨
#프로퍼티는 속성에 추가적인 처리가 필요할 때만 사용해야 함

#자바 익숙한 사람들
class Person:
    def __init__(self, first_name):
        self.first_name = name
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self,value):
        self._first_name= value
#그지 같이 짜놓은 코드임. 속도도 느림
#뭔소린지 모르겠음

#프로퍼티는 계산한 속성을 정의할 때 사용하기도 함 이런 속성은 실제로 저장하지는 않지만 필요에 따라 계산함
import math
class Circle:
    def __init__(self,radius):
        self.radius = radius
    @property
    def area(self):
        return math.pi * self.radius ** 2
    @property
    def perimeter(self):
        return 2 * math.pi * self.radius
# radius, area, perimeter가 마치 속성인 것처럼 접근할 수 있음
#속성과 메소드 호출을 복합적으로 사용하는 것과는 대조적
c = Circle(4,0)
c.radius #() 안쓰임
c.area #() 안쓰임
c.perimeter

#게터 세터 함수를 직접 호출할 수 도 있음
p = Person('Guido')
p.get_first_name() #'Guido'
p.set_fist_name('Larry')

#프로퍼티 정의를 반복적으로 사용하는 파이썬 코드를 작성하지 않도록 주의

######8.7 부모 클래스의 메소드 호출
# 오버라이드 된 서브클래스 메소드가 아닌 부모 클래스에 있는 메소드 호출
# 부모의 메소드를 호출하려면 super() 함수 사용
class A:
    def spam(self):
        print('A.spam')
class B(A):
    def spam(self):
        print('B.spam')
        super().spam() #부모의 spam() 호출
#1)super()는 일반적으로 __init__() 메소드에서 부모를 제대로 초기화하기 위해 사용
class A:
    def __init__(self):
        self.x = 0
class B(A):
    def __init__(self):
        super().__init__()
        self.y = 1
#2) 파이썬의 특별 메소드를 오버라이드한 코드에서 super()를 사용하기도 함
class Proxy:
    def __init__(self, obj):
        self._obj = obj
    #내부 obj를 위해 델리게이트(delegate)속성 찾기
    def __getattr__(self, name):
        return getattr(self._obj, name)
    #델리게이트 속성 할당
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value) #원본  __setattr__ 호출
        else:
            setattr(self._obj, name, value)
#__setattr() 구현에 이름 확인이 들어있음
# 이름이 밑줄로 시작하면 super()를 사용해서  __setattr__()의 원래 구현 호출
# 그렇지 않다면 내부 객체 self._obj를 부름
#명시적으로 클래스를 표시하지 않아도 super()이 동작함

#super()함수를 올바르게 사용하기 어려움
#때때로 부모 클래스 메소드를 직접 호출하기 위해 다음과 같이 작성
class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print( 'A.__init__')
#동작하기는 하지만 다중상속과 같은 상황에서 문제가 발생함

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

class C(A,B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')
#코드 실실 시 __init__() 함수가 두번 호출 됨
c = C() #Base.__init
#A.__init
#Base.__init
#B.__init
#C.__init

#Base.__init__()을 두번 호출하는 것이 문제가 될 수도 있음
#super()를 사용하여 코드 수정
class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        super().__init__(self)
        print('A.__init__')
class B(Base):
    def __init__(self):
        super().__init__(self)
        print('B.__init__')

class C(A,B):
    def __init__(self):
        super().__init__() #super를 한번만 호출
        print('C.__init__')
# __init__()메소드 한번씩만 호출됨

#팡썬의 상속 구현을 이해해야 함
#클래스를 정희라 때 마다 파이썬은 메소드 처리순서 리스트를 계산
#MRO리스트는 모든 베이스 클래스를 단순히 순차적으로 나열한 리스트
C.__mro__ # (<class 'C'>, <class 'A'>, <class 'B'>, <class 'Base'>, <class 'object'>) #오잉 나는 왜 maint이 안뜨지
#상속구현을 위해 파이썬은 가장 왼쪽에 잇는 클래스에서 시작해서 오른쪽으로 이동
#MRO이르스 자체를 실제로 결정할 땐느 C3선형화라는 기술 사용
#합병 정렬함
#1)자식 클래스를 부모보다 먼저 확인
#2)부모 클래스가 둘이상이면 리스팅한 순서대ㅗㄹ 확인
#유효한 후보가 두가지 있으면 처번째 부모 클래스부터 선택

#MRO리스트의 클래스 순서가 정의하려는 거의 모든 클래스 구조에 의미가 통해야함
#supuer()함수 사용 시 파이썬은 MRO의 다음클래스에서 검색을 시작
# 재정의한 모든 메소드가 모두 super()을 사용하고 한번만 호출하지만 시스템은 MRO 리스트 전체에 동작하고 모든 메소드를 한번만 호출
#그래서 Base.__init__()이 두번 호출 된게 아님
#super()의 놀라운 측면 중 하나는 이 함수가 MRO바로 위에 잇는 부모에 직접 접근하지 않을 때도 있고
#직접적인 부모 클래스가 없을 때도 super()를 사용할 수 있음
class A:
    def spam(self):
        print('A.spam')
        super().spam()

a= A()
#a.spam()
# Traceback (most recent call last):
#   File "<input>", line 6, in <module>
#   File "<input>", line 4, in spam
# AttributeError: 'super' object has no attribute 'spam'

#클래스를 다중 상속에 사용하면 어떻게 되는 지확인
class B:
    def spam(self):
        print('B.spam')
class C(A,B):
    pass

c= C()
c.spam()
#A.spam
#B.spam

#A클래스의 super().spam()이 실제로 A와는 전혀 관련 없는 B클래스의 spam() 호출
#C의 MRO를 보면 이를 이해할 수 있음
C.__mro__ #(<class 'C'>, <class 'A'>, <class 'B'>, <class 'object'>)

#super()를 사용하는 것은 클래스를 복합적으로 사용할 때 일반적인 모습임 ( #8.13, 8.18 참고)

#super()로 인해 원치 않는 메소드가 호출되는 현상이 발생할 수 도 있어 다음 규칙을 꼭 따르셈
#1)상속 관계에서 이름이 같은 모든 메소드ㄹ는 동일한 구조를 가지도록 함(ex)같은 인자수, 같은 인자 이름
#이렇게 하면 직접적으로 부모가 아닌 클래스 메소드를 호출할 때 발생하는 실수를 방지할 수 잇음
#2)가장 상위에 잇는 클래스에서 메소드 구현을 제공해서 MRO에서 검색할 대결국은 실제 메소드에서 멈추도록 하는 것이 좋음

####### 8.8 서브 클래스에서 프로퍼티 확장
#서브 클래스에서, 부모 클래스에서 정의한 프로퍼티 기능을 확장하고 싶음
class Person:
    def __init__(self,name):
        self.name = name
    #getter
    @property
    def name(self):
        return self._name
    #setter
    @name.setter
    def name(self,value):
        if not isinstance(value,str):
            raise TypeError('expected a string')
    #deleter
    def name(self):
        raise AttributeError('cant delete attribute')

#Person을 상속받아 name프로퍼티에 새로운 기능을 넣어 클래스 확장#######오류나!!!!!!!!
class SubPerson(Person):
    @property
    def name(self):
        print('getting name')
        return super().name

    @name.setter
    def name(self,value):
        print('setting name to',value)
        super(SubPerson, SubPerson).name.__set__(self,value)

    @name.deleter
    def name(self):
        print('Deletign name')
        super(SubPerson, SubPerson).name.__delete__(self)

#새로운 클래스를 사용하는예제
s = SubPerson('Guido') #setting name to Guido
s.name
s.name ='Larry'
s.name = 42



#프로퍼티 메소드를 하나확장하고 싶으면 아래 코드 사용
class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('getting name')
        return super().name
#혹은 세터 하나만 확장하려면 다음과 같이 함
class SubPerson(Person):
    @Person.name.setter
    def name(self,value):
        print('setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self,value)

#서브 클래스의 프로퍼티를 확장하면 프로퍼티가 ㅏ나의 메소드가 아닌 게터,세터딜리터 메소드의 컬렉션으로 정의었기 대문에 문제 발생한
#프로퍼티 확장시 모든 메소드를 다시 정의할 지 메소드 하나만 다시 정의할지 결정해야함
#첫번째 예제는 모든 메소드 재정의 : 모든 메소드에서 기존 구현을 호출하기 위해 super()호출
#세터에서 사용한 super(SubPerson,SubPerson).name.__set__(self,value)는 실수가 아님
#세터의 기존 구현으로 델리게이트 하기위해 컨트롤은 기존에 구현한 name프로퍼티의 __set__()메소드로 전달해야함
#하지만 이 메소드에 도달하기 위한 유일한 방법은 인스턴스 변수가 아닌 클래스 변수로 접근 하는 것
#super(SubPerson,SubPerson)에서 수행된 것

#메소드 중 하나만 재정의 하려면 @property 자체만 사용하는 것으로는 충분하지 않음
class SubPerson(Person):
    @property # Doesn't work
    def name(self):
        print('Getting name')
        return super().name
s = SubPerson('Guido')

class SubPerson(Person):
    @Person.getter
    def name(self):
        print('Getting name')
        return super().name

s = SubPerson('Guido')
s.name
s.name = 'Larry'
s.name
s.name = 42

# A descriptor
class String:
    def __init__(self, name):
            self.name = name
def __get__(self, instance, cls):
    if instance is None:
        return self
    return instance.__dict__[self.name]
def __set__(self, instance, value):
    if not isinstance(value, str):
        raise TypeError('Expected a string')
    instance.__dict__[self.name] = value
# A class with a descriptor
class Person:
    name = String('name')
    def __init__(self, name):
        self.name = name
# Extending a descriptor with a property
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
######8.9  새로운 클래스나 인스턴스 속성 만들기
# Descriptor attribute for an integer type-checked attribute
class Integer:
    def __init__(self, name):
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


class Point:
    x = Integer('x')
    y = Integer('y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(2, 3)
p.x
p.y
p.x

class Point:
    def __init__(self, x, y):
        self.x = Integer('x') # No! Must be a class variable self.y = Integer('y')
        self.x = x
        self.y = y
# Descriptor attribute for an integer type-checked attribute
class Integer:
    ...
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]
p = Point(2,3)
p.x
Point.x

 # Descriptor for a type-checked attribute
class Typed:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
    def __get__(self, instance, cls):
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
# Class decorator that applies it to selected attributes
    def typeassert(**kwargs):
        def decorate(cls):
            for name, expected_type in kwargs.items():
    # Attach a Typed descriptor to the class setattr(cls, name, Typed(name, expected_type))
            return cls
        return decorate
    # Example use
    @typeassert(name=str, shares=int, price=float)
    class Stock:
        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price

####8.10게르은 계산을 하는 프로퍼티 사용
#읽기 전용 속성을 프로퍼티로 정의하고 이 속성에 접근할 때만 계산하고 싶음
#하지만 한번 접근하고 나면 값을 캐시해 놓고 다음번에 접근할 때는 다시 계산하지 않도록 하고싶음
#디스크립터 클래스 사용
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


####8.11 자료 구조 초기화 단순화 하기
class Structure:
# Class variable that specifies expected fields
    _fields= []
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
        # Set the arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
# Example class definitions
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']
    class Point(Structure):
        _fields = ['x','y']
    class Circle(Structure):
        _fields = ['radius'] def area(self):
            return math.pi * self.radius ** 2

class Structure: _fields= []
def __init__(self, *args, **kwargs):
    if len(args) > len(self._fields):
        raise TypeError('Expected {} arguments'.format(len(self._fields)))
            # Set all of the positional arguments
    for name, value in zip(self._fields, args):
        setattr(self, name, value)
            # Set the remaining keyword arguments
    for name in self._fields[len(args):]:
        setattr(self, name, kwargs.pop(name))
            # Check for any remaining unknown arguments
    if kwargs:
        raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))
    # Example use
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']
    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, price=91.1)
    s3 = Stock('ACME', shares=50, price=91.1)

class Structure:
# Class variable that specifies expected fields _fields= []
    def __init__(self, *args, **kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
            # Set the arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
            # Set the additional arguments (if any)
        extra_args = kwargs.keys() - self._fields
        for name in extra_args:
            setattr(self, name, kwargs.pop(name))
        if kwargs:
            raise TypeError('Duplicate values for {}'.format(','.join(kwargs)))
# Example use
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']
    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, 91.1, date='8/2/2012')

class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius ** 2
class Structure:
# Class variable that specifies expected fields
_fields= []
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
            # Set the arguments (alternate)
        self.__dict__.update(zip(self._fields,args))

def init_fromlocals(self):
    import sys
    locs = sys._getframe(1).f_locals
    for k, v in locs.items():
        if k != 'self':
            setattr(self, k, v)
class Stock:
    def __init__(self, name, shares, price):
        init_fromlocals(self)