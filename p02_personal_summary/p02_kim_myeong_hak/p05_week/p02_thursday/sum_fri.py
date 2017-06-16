## 8.6 관리 속성 만들기
# 인스턴스 속성을 얻거나 설정할 때 추가적인 처리를 하고 싶다


# property로 정의하면 된다
class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # 게터 함수
    @property
    def first_name(self):
        return self._first_name

    # 세터 함수
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value,str):
            raise TypeError('Expected a string')
        self._first_name = value

    # 딜리터 함수(optional)
    @first_name.deleter                         # 넌 또 뭐니..
    def first_name(self):
        raise AttributeError("Can't delete attribute")



# 관련 메소드가 3개인데 모두 같은 이름이어야 한다.
# 게터 함수 : first_name을 프로퍼티로 만든다.
# 다른 두 메소드는 추가적으로 세터와 딜리터 함수를 first_name 프로퍼티에 추가한다

# @first_name.setter와 @first_name.deleter 데코레이터는 @property를 사용해서 first_name을 만들어놓지 않으면
# 정의되지 않는다.

a = Person('Guido')
a.first_name                    # 게터 호출
# Guido

a.first_name = 42               # 세터 호출
# TypeError뜸

del a.first_name
# can't delete attribute


# getter, setter 메소드에서 self._first_name을 직접 다루는데 여기에 실제 데이터가 들어간다
# 그런데 __init__()는 왜 self.fist_name을 설정하는가? (self._first_name이 아니라)
# 속성에 타입 체킹을 적용하는 것에 집중  self.first_name을 설정하면, 설정 연산이 세터 메소드를 사용한다.


class Person:
    def __init__(self, first_name):
        self.set_first_name(first_name)

    # 게터 함수
    def get_first_name(self):
        return self._first_name


    # 세터 함수
    def set_first_name(self,value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    #  deleter func
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")

    # 기존 게터/세터 메소드로 프로퍼티 만들기
    name = property(get_first_name, set_first_name, del_first_name)


## actually property attribute is.. a...c 함께 묶여있는 메소드 콜렉션이에요
# 프로퍼티가 있는 클래스를 조사해보면 프로퍼티 자체의 fget,fset,fdel 속성에서 raw 메소드를 찾을 수 있다

Person.first_name.fget
# <function Person.first_name at 0x1006a60e0>
Person.first_name.fset
# <function Person.first_name at 0x1006a6170>
Person.first_name.fdel
# <function Person.first_name at 0x1006a62e0>


# property는 속성에 추가적인 처리가 필요할 때만 사용하세요.
# 프로퍼티는 계산한 속성을 정의할 때 사용하기도 한다.

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


# 이렇게 하면 radius, area, perimeter를 마치 속성처럼 접근할 수 있다
c = Circle(4.0)
print(c.radius)                     # 올ㅋ 결과 나옴 4.0
print(c.area)                       # () 안씀. 그런데 나옴 50.26548245743669
print(c.perimeter)                  # () 안씀. 25.132741228718345


## 8.7 부모 클래스의 메소드 호출
# 오버라이드 된 서브클래스 메소드가 아닌 부모 클래스에 있는 메소드를 호출하고 싶다
# super()
class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()                          # 엄빠 spam()호출

# 일반적으로는 __init__() 메소드에서 부모를 제대로 초기화(ㅇㅁㅇ)하기 위해 쓴다
class A:
    def __init__(self):
        self.x = 0


class B(A):
    def __init__(self):
        super().__init__()
        self.y = 1


# 특별 메소드를 오버라이드한 코드에서 쓰기도 함 super()
class Proxy:
    def __init__(self,obj):
        self._obj = obj

    # inner obj를 위해 delegate 속성 찾기
    def __getattr__(self, name):
        return getattr(self._obj, name)

    # delegate 속성 할당
    def __setattr__(self, name, value):
        if name.startswith('_'):                    # '_'   'ㅁ'    ^_^
            super().__setattr__(name, value)                                    # 원본 __setattr__ 호출
        else:
            setattr(self._obj, name, value)

# 명시적으로 클래스를 표시하지 않아도 super()는 동작한다


## 제대로 된 super() 코드
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

class C(A,B):
    def __init__(self):
        super().__init__()
        print('C.__init__')

# print(Base())
c = C()

# Base.__init__
# B.__init__
# A.__init__
# C.__init__


# Method Resolution Order : 메소드 처리 순서
C.__mro__

## (__main__.C, __main__.A, __main__.B, __main__.Base, object)
# 파이썬은 가장 왼쪽 클래스에서 시작해서, mro 리스트의 오른쪽으로 이동하며 일치하는 속성을 찾는다

# MRO 리스트 자체를 결정할때는 C3 선형화라는 기술을 쓴다
# 부모 클래스의 MRO를 다음 세 가지 제약 조건 하에서 합병 정렬(merge sort)한다

# - 자식 클래스를 부모보다 먼저 확인한다
# - 부모 클래스가 둘 이상이면 리스팅한 순서대로 확인한다
# - 유효한 후보가 두 가지 있으면, 첫번째 부모 클래스부터 선택한다



# 직접적인 부모 클래스가 없이 super()를 쓴 클래스를 다중 상속에 사용하면??


class A:
    def spam(self):
        print('A.spam')
        super().spam()

class B:
    def spam(self):
        print('B.spam')

class C(A,B):
    pass

c = C()
c.spam()

# A.spam
# B.spam

# A 클래스의 super().spam()이 A와 전혀 관련없는 B클래스의 spam()을 호출함. C클래스의 MRO를 보면 이해 가능
C.__mro__
# (__main__.C, __main__.A, __main__.B, object)



## 8.8 서브클래스에서 프로퍼티 확장
# 서브 클래스에서 부모 클래스에 정의한 프로퍼티의 기능을 확장하고 싶다

class Person:
    def __init__(self, name):
        self.name = name

    # 게터 함수
    @property
    def name(self):
        return self._name

    # 세터 함수
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    # deleter func
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")


# 이 코드는 Person을 상속받아 name property에 새로운 기능을 넣어 클래스를 확장한다
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


## 서브클래스의 프로퍼티를 확장하면 프로퍼티가 하나의 메소드가 아닌 게터, 세터, 딜리터 메소드의 컬렉션으로 정의된거라
# 자잘한 문제가 발생해서- 프로퍼티 확장 시에는 모든 메소드를 다시 정의할지, 메소드 하나만 다시 정의할지 결정해야 함

## 돌아가는 코드
class SubPerson(Person):
    @Person.getter
    def name(self):
        print('Getting name')
        return super().name

s = SubPerson('Guido')
s.name
# Getting name
# 'Guido'
s.name = 'Larry'
s.name
# Getting name
# 'Larry'
s.name = 42                    #TypeError



# 이걸로는 하드코딩한 Person 클래스를 generic하게 치환 못함
# 디스크립터

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


# 디스크립터를 가진 클래스
class Person:
    name = String('name')
    def __init__(self, name):
        self.name = name


# 디스크립터에 프로퍼티를 넣어 확장
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




# 8.9 새로운 클래스나 인스턴스 속성 만들기
# 타입 확인 등과 같이 추가적 기능을 가진 새로운 종류의 인스턴스 속성을 만들고 싶을떄

# 디스크립터 클래스 형태로 정의
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


# 디스크립터는 get, set, delete를 특별 메소드 __get__(), __set__(), __delete__() 형식으로 구현한 클래스
# 디스크립터를 쓰려면 인스턴스는 클래스 정의에 클래스 변수로 들어가야 함
class Point:
    x = Integer('x')
    y = Integer('y')
    def __init__(self,x,y):
        self.x = x
        self.y = y

# 디스크립터는 파이썬 클래스 기능에 __slots__, @classmethod, @staticmethod, @property 같은 도구를 제공한다
# 얘를 정의하면 get, set, delete와 같은 인스턴스 연산을 아주 하위 레벨에서 얻고 어떻게 동작할지도 바꿀 수 있다
# 디스크립터는 인스턴스 기반이 아닌 클래스 레벨에서만 정의가 가능하다

# 속성 타입을 확인하는 디스크립터
class Typed:
    def __init__(self,name,expected_type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self,instance,value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected '+str(self.expected_type))
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


# 선택한 속성에 적용되는 클래스 데코레이터

def typeassert(**kwargs):
    def decorate(cls):
        for name,expected_type in kwargs.items():
            # 클래스에 Typed 디스크립터 설정
            setattr(cls,name,Typed(name, expected_type))
        return cls
    return decorate

# 사용 예
@typeassert(name=str, shares=int, price=float)
class Stock:
    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price


## 8.10 게으른 계산을 하는 프로퍼티 사용
# 읽기 전용 속성을 프로퍼티로 정의하고, 이 속성에 접근할 때만 계산하고 싶다. 하지만 한 번 접근하고 나면 이 값을 캐시해놓고 다음 번에 접근할 때에는 다시 계산하지 않을때

# 아래처럼 디스크립터 클래스를 사용하세요

class lazyproperty:
    def __init__(self,func):
        self.func = func

    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance,self.func.__name__, value)
            return value

# 위 코드를 활용하는 클래스

import math

class Circle:
    def __init__(self,radius):
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
print(c.radius)                        # 4.0
print(c.area)                          # Computing area
                                    # 50.26548245743669
print(c.perimeter)                      # Computing perimeter
                                        # 25.132741228718345
print(c.perimeter)                      # Computing perimeter가 또 나왔는데... 전체를 다시 돌리니 1번만 나왔다


# 예제 설명
c = Circle(4.0)
# 인스턴스 변수 구하기
# vars(c)                                 # {'radius': 4.0}

# 면적을 계산하고 추후 변수 확인
c.area
vars(c)                                    # {'area': 50.26548245743669, 'radius': 4.0}

c.area                                     # 50.26548245743669

# 변수를 삭제하고 프로퍼티가 다시 실행됨을 확인한다

del c.area
vars(c)                                 # 'radius': 4.0}


## 이 방식의 단점은 계산값을 생성한 뒤에야 수정이 가능하다는 것




# 8.11 자료 구조 초기화 단순화하기
# 자료 구조로 사용하는 클래스를 작성하고 있는데, 반복적으로 비슷한 __init__()함수를 작성하기에 지쳐간다

# 베이스 클래스의 __init__() 함수를 정의

class Structure:
    # 예상되는 필드를 명시하는 클래스 변수
    _fields = []
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # 속성 설정
        for name,value in zip(self._fields,args):
            setattr(self,name,value)


# 예제 클래스 정의
if __name__=='__main__':
    class Stock(Structure):
        _fields = ['name','shares','price']

    class Point(Structure):
        _fields = ['x','y']

    class Circle(Structure):
        _fields = ['radius']
        def area(self):
            return math.pi * self.radius ** 2


s = Stock('ACME',50,91.1)
p = Point(2,3)
c = Circle(4.5)
s2 = Stock('ACME',50)
#   File "<ipython-input-24-a6398cb7c55a>", line 6, in __init__
#     raise TypeError('Expected {} arguments'.format(len(self._fields)))
# TypeError: Expected 3 arguments


# 키워드 매개변수를 지원하기로 결정했을때 사용할 수 있는 디자인 옵션즈 중 하나가 키워드 매개변수를 매핑해서
# _fields에 명시된 속성 이름만 일치하도록 하는 것
class Structure:
    _fields = []
    def __init__(self,*args,**kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # 모든 위치 매개변수 설정
        for name, value in zip(self._fields,args):
            setattr(self,name,value)

        # 남아있는 키워드 매개변수 설정
        for name in self._fields[len(args)]:
            setattr(self,name,kwargs.pop(name))

        # 남아있는 기타 매개변수가 없는지 확인
        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))

# 사용 예
if __name__=='__main__':
    class Stock(Structure):
        _fields = ['name','shares','price']

    s1 = Stock('ACME',50,91.1)
    s2 = Stock('ACME',50,price=91.1)
    s3 = Stock('ACME',shares=50,price=91.1)


## 또는 _fields에 명시되지 않은 구조에 다른 속성을 추가하는 수단으로 키워드 매개변수를 쓸 수 있다
class Structure:
    # 예상되는 필드를 명시하는 클래스 변수
    _fields = []
    def __init__(self,*args,**kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # 속성 설정
        for name,value in zip(self._fields,args):
            setattr(self,name,value)

        # (있다면) 추가적인 매개변수 설정
        extra_args = kwargs.keys() - self._fields
        for name in extra_args:
            setattr(self,name,kwargs.pop(name))
        if kwargs:
            raise TypeError('Duplicate values for {}'.format(','.join(kwargs)))

# 사용 예
if __name__=='__main__':
    class Stock(Structure):
        _fields = ['name','shares','price']

    s1 = Stock('ACME',50,91.1)
    s2 = Stock('ACME',50,91.1,date='8/2/2012')


# 제너럴한 목적
#  __init__() 메소드를 정의하는 기술은 규모가 작은 자료 구조를 대량으로 만들때 유용하다
# 유틸리티 함수와 프레임 핵을 사용하면 인스턴스 변수를 자동으로 초기화할 수 있다


def init_fromlocals(self):
    import sys
    locs = sys._getframe(1).f_locals
    for k,v in locs.items():
        if k != 'self':
            setattr(self,k,v)

class Stock:
    def __init__(self,name,shares,price):
        init_fromlocals(self)
