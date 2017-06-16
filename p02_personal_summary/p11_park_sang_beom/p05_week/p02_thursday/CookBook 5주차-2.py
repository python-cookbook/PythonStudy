'''
--------------------------------------------------------------------------------------
8.6 관리 속성 만들기

문제 : 인스턴스 속성을 얻거나 설정할 때 추가적인 처리(타입 체크, 검증 등) 하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 속성에 대한 접근을 조절하고 싶으면 프로퍼티(property) 로 정의
  속성에 간단한 타입 체크를 추가하는 프로퍼티 정의 예제
--------------------------------------------------------------------------------------
'''

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
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # 딜리티 함수(옵션)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")

a = Person('Guido')

print(a.first_name)

'''
=> 메소드가 세 개 있는데, 모두 같은 이름을 가져야 한다

=> 첫번째 메소드는 게터 함수로 first_name 을 프로퍼티로 만든다
   다른 두 메소드는 추가적으로 세터와 딜리티 함수를 first_name 프로퍼티에 추가한다

=> @first_name.setter 와 @first_name.delete 데코레이터는 @property 를 사용해서 first_name 을 
   만들어 놓지 않으면 정의되지 않는 점이 중요!!
   
=> 프로퍼티를 구현할 때, 기반 데이터가 있다면 여전히 어딘가에 저장해야 한다
   따라서 게터, 세터 메소드에서 _first_name 속성을 직접 다루는 것을 볼 수 있는데, 여기에 실제 데이터가 들어간다
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 이미 존재하는 get 과 set 메소드로 프로퍼티 정의
--------------------------------------------------------------------------------------
'''

class Person:
    def __init__(self, first_name):
        self.set_first_name(first_name)

    # 게터 함수
    def get_first_name(self):
        return self._first_name

    # 세터 함수
    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # 딜리티 함수(옵션)
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")

# 기존 게터/세터 메소드로 프로퍼티 만들기
name = property(Person.get_first_name, Person.set_first_name, Person.del_first_name)

'''
--------------------------------------------------------------------------------------
- 일반적으로 fget 이나 fset을 직접 호출하지는 않고, 프로퍼티에 접근할 때 자동으로 실행된다

- 프로퍼티는 속성에 추가적인 처리가 필요할 때만 사용해야 한다
--------------------------------------------------------------------------------------
'''

class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

'''
--------------------------------------------------------------------------------------
- 프로퍼티는 계산한 속성을 정의할 때 사용하기도 한다
  이런 속성은 실제로 저장하지는 않지만 필요에 따라 계산을 한다
--------------------------------------------------------------------------------------
'''

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

'''
--------------------------------------------------------------------------------------
- 프로퍼티 정의를 반복적으로 사용하는 파이썬 코드를 작성하지 않도록 주의!
--------------------------------------------------------------------------------------
'''

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

    # 이름이 다른 프로퍼티 코드의 반복 (좋지 않다!!!!)
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._last_name = value





'''
--------------------------------------------------------------------------------------
8.7 부모 클래스의 메소드 호출

문제 : 오버라이드된 서브클래스 메소드가 아닌 부모 클래스에 있는 메소드를 호출하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 부모 (혹은 슈퍼클래스)의 메소드를 호출하려면 super() 함수 사용
--------------------------------------------------------------------------------------
'''

class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()      # 부모의 spam() 호출


# super() 는 일반적으로 __init__() 메소드에서 부모를 제대로 초기화하기 위해 사용
class A:
    def __int__(self):
        self.x = 0

class B:
    def __init__(self):
        super().__init__()
        self.y = 1

# 파이썬의 특별 메소드를 오버라이드한 코드에서 super() 를 사용하기도 한다
class Proxy:
    def __int__(self, obj):
        self.obj = obj

    # 내부 obj를 위해 델리게이트(delgate) 속성 찾기
    def __getattr__(self, name):
        return getattr(self.obj, name)

    # 델리게이트(delgate) 속성 할당
    def __setattr__(self, name, value):
        if name.startswith('-'):
            super().__setattr__(name, value)    # 원본 __setattr__ 호출

        else:
            setattr(self.obj, name, value)

'''
=> __setattr__() 구현에 이름 확인이 들어있다

=> 만약 이름이 밑줄로 시작하면 super()를 사용해서 __setattr__() 의 원래의 구현을 호출
   그렇지 않다면 내부 객체인 self._obj 를 부른다
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 부모 클래스 메소드를 직접 호출하기 위한 예제
--------------------------------------------------------------------------------------
'''

class Base:
    def __init__(self):
        print('Base.__init__')

class A(Base):
    def __int__(self):
        Base.__init__(self)
        print('A.__init__')

'''
--------------------------------------------------------------------------------------
- 다중 상속과 같은 상황에서 문제 발생 예제
--------------------------------------------------------------------------------------
'''

class Base:
    def __int__(self):
        print('Base.__init__')

class A(Base):
    def __int__(self):
        Base.__init__(self)
        print('A.__init__')

class B(Base):
    def __int__(self):
        Base.__init__(self)
        print('B.__init__')

class C(A, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')

c = C()     # Base.__init__() 메소드가 두 번 호출된다

'''
--------------------------------------------------------------------------------------
- super() 를 사용하여 코드 수정 예제
--------------------------------------------------------------------------------------
'''


class Base:
    def __int__(self):
        print('Base.__init__')


class A(Base):
    def __int__(self):
        super().__init__()
        print('A.__init__')


class B(Base):
    def __int__(self):
        super().__init__()
        print('B.__init__')


class C(A, B):
    def __init__(self):
        super().__init__()
        print('C.__init__')

c = C()     # 여기서 super() 를 한 번만 호출한다

'''
--------------------------------------------------------------------------------------
- MRO(Method Resolution Order 메소드 처리 순서) 리스트 자체를 실제로 결정할 때는 C3 선형화 기술 사용

- 너무 계산이 복잡해지지 않도록 부모 클래스의 MRO 를 세 가지 제약 조건 하에서 합병 정렬(merge sort) 한다

    자식 클래스를 부모보다 먼저 확인한다
    부모 클래스가 둘 이상이면 리스팅 순서대로 확인한다
    유효한 후보가 두 가지 있으면, 첫번째 부모 클래스부터 실행한다
--------------------------------------------------------------------------------------
'''





'''
--------------------------------------------------------------------------------------
8.8 서브클래스에서 프로퍼티 확장

문제 : 서브클래스에서, 부모 클래스에 정의한 프로퍼티의 기능 확장하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 프로퍼티를 정의하는 예제
--------------------------------------------------------------------------------------
'''

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

    # 딜리티 함수
    @name.deleter
    def name(self):
        raise AttributeError("can't delete attribute")

'''
--------------------------------------------------------------------------------------
- Person 을 상속 받아 name 프로퍼티에 새로운 기능을 넣어 클래스를 확장하는 예제
--------------------------------------------------------------------------------------
'''

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
s.name
s.name = 'Larry'

# 프로퍼티의 메소드 하나를 확장 예제
class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('Getting name')
        return super().name

# 세터(setter) 하나만 확장 예제
class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name__set__(self, value)

'''
--------------------------------------------------------------------------------------
- 프로퍼티를 확장할 때 모든 메소드를 다시 정의할지, 메소드 하나만 다시 정의할지 결정해야 한다

- 메소드 중 하나만 재정의하려면 @property 자체만 사용하는 것으로 충분하지 않다
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 디스크립터 확장 예제
--------------------------------------------------------------------------------------
'''

# 디스크립터
class String:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if isinstance is None:
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
        print('setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)





'''
--------------------------------------------------------------------------------------
8.9 새로운 클래스나 인스턴스 속성 만들기

문제 : 타입 확인 등과 같이 추가적 기능을 가진 새로운 종류의 인스턴스 속성 만들기기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 완전히 새로운 종류의 인스턴스 속성을 만들려면 그 기능을 디스크립터 클래스 형태로 정의하기
--------------------------------------------------------------------------------------
'''

# 타입을 확인하는 정수형 디스크립터 속성
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

'''
--------------------------------------------------------------------------------------
- 디스크립터를 사용하려면 디스크립터의 인스턴스는 클래스 정의에 클래스 변수에 들아가야 한다
--------------------------------------------------------------------------------------
'''

class Point:
    x = Integer('x')
    y = Integer('y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(2, 3)

print(p.x)      # Point.x.__get__(p.Point) 호출

p.y = 5         # Point.y.__set__(p, 5) 호출
p.x = 2.3       # Point.x.__set__(p, 2.3) 호출

'''
--------------------------------------------------------------------------------------
- 디스크립터는 파이썬 클래스 기능에 __slots___, @classmethod, @staticmethod, @property 와 같은 도구 제공

- 디스크립터에 대해 한 가지 헷갈리는 부분은 인스턴스 기반이 아닌 클래스 레벨에서만 정의가 가능하다!!
--------------------------------------------------------------------------------------
'''

# 동작하지 않음
class Point:
    def __init__(self, x, y):
        self.x = Integer('x')       # 안 된다. 반드시 클래스 변수여야 한다
        self.y = Integer('y')
        self.x = x
        self.y = y

# 타입을 확인하는 정수형 디스크립터 속성
class Integer:
    ...
    def __get__(self, instance, cls):
        if instance is None:
            return self

        else:
            return instance.__dict__[self.name]

p = Point(2, 3)

print(p.x)      # Point.x.__get__(p, Point) 호출
print(Point.x)  # Point.x.__get__(None, Point) 호출

'''
--------------------------------------------------------------------------------------
- 클래스 데코레이터를 사용하는 디스크립터 기반의 고급 코드 예제
--------------------------------------------------------------------------------------
'''

# 속성 타입을 확인하는 디스크립터
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

    # 선택한 속성에 적용되는 클래스 데코레이터
    def typeassert(**kwargs):
        def decorate(cls):
            for name, expected_type in kwargs.items():
                # 클래스에 Typed 디스크립터 설정
                setattr(cls, name, Typed(name, expected_type))
            return cls
        return decorate

# 사용 예
# @typeassert(name=str, shares=int, price=float)
class Stock:
    def __int__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price





'''
--------------------------------------------------------------------------------------
8.10 게으른 계산을 하는 프로퍼티 사용

문제 : 읽기 전용 속성을 프로퍼티로 정의하고, 이 속성에 접근할 때만 계산하도록 하고 싶다
      하지만 한 번 접근하고 나면 이 값을 캐시해 놓고 다음 번에 접근할 때에는 다시 계산하지 않도록 하기 
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 게으른 속성을 효율적으로 정의하기 위한 디스크립터 클래스 예제
--------------------------------------------------------------------------------------
'''

class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)

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

print(c.radius)
print(c.area)
print(c.area)
print(c.perimeter)
print(c.perimeter)

'''
=> Computing area 와 Computing Perimeter 메시지가 한 번씩만 나타나는 점 주목!!
--------------------------------------------------------------------------------------
'''


'''
--------------------------------------------------------------------------------------
- __get__() 메소드는 접근하는 속성이 인스턴스 딕셔너리에 없을 때만 실행된다

- lazyproperty 클래스는 프로퍼티 자체와 동일한 이름을 사용해서 인스턴스 __get__() 메소드에 계산한 값을
  저장하는 식으로 이를 활용
--------------------------------------------------------------------------------------
'''

c = Circle(4.0)

print(vars(c))

# 면적을 계산하고 추후 변수 확인
print(c.area)
print(vars(c))

# 속성에 접근해도 더 이상 프로퍼티를 실행하지 않는다
print(c.area)

# 변수를 삭제하고 프로퍼티가 다시 실행됨을 확인
del c.area

print(vars(c))
print(c.area)

c.area = 25

print(c.area)

'''
=> 위 코드의 단점은 계산한 겂을 생성한 후에 수정할 수 있다
--------------------------------------------------------------------------------------
'''





'''
--------------------------------------------------------------------------------------
8.11 자료 구조 초기화 단순화하기

문제 : 자료 구조로 사용하는 클래스를 작성하고 있는데, 반복적으로 비슷한 __init__() 함수를 작성하기에 지친다
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 자료 구조의 초기화는 베이스 클래스의 __init__() 함수를 정의하는 식으로 단순화할 수 있다
--------------------------------------------------------------------------------------
'''

class Structure:
    # 예상되는 필드를 명시하는 클래스 변수
    _fields = []
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # 속성 설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # 예제 클래스 정의
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

'''
--------------------------------------------------------------------------------------
- 키워드 매개변수를 매핑해서 _fields 에 명시된 속성 이름에만 일치하도록 만드는 예제 
--------------------------------------------------------------------------------------
'''

class Structure:
    _fields = []
    def __init__(self, *args, **kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # 모든 위치 매개변수 설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # 남아 있는 키워드 매개변수 설정
        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))

        # 남아 있는 기타 매개변수가 없는지 확인
        if kwargs:
            raise TypeError('Invalid argument(s) : {}'.format(','.join(kwargs)))

# 사용 예
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, price=91.1)
    s3 = Stock('ACME', shares=50, price=91.9)

'''
--------------------------------------------------------------------------------------
- _fields에 명시되지 않은 구조에 추가적인 속성을 추가하는 수단으로 키워드 매개변수 사용할 수 있다 
--------------------------------------------------------------------------------------
'''

class Structure:
    # 예상하는 필드를 명시하는 클래스 변수
    _fields = []
    def __init__(self, *args, **kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # 속성 설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # (있다면) 추가적인 매개변수 설정
        extra_args = kwargs.keys() - self._fields
        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))
        if kwargs:
            raise TypeError('Invalid argument(s) : {}'.format(','.join(kwargs)))

# 사용 예
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, 91.1, date='8/2/2012')

'''
--------------------------------------------------------------------------------------
- 제너럴한 목적으로 __init__() 메소드를 정의하는 기술은 규모가 작은 자료 구조를 대량으로 만드는 프로그램에 아주 유용 
--------------------------------------------------------------------------------------
'''

import math

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

'''
--------------------------------------------------------------------------------------
- setattr() 함수로 값을 설정하는 매커니즘을 사용하지 안혹 인스턴스 딕셔너리에 직접 접근 하기 
--------------------------------------------------------------------------------------
'''

class Structure:
    # 예상되는 필드를 명시하는 클래스 변수
    _fields = []
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # 매개변수 설정(대안)
        self.__dict__.update(zip(self._fields, args))
'''
=> 이렇게 해도 동작은 하지만, 서브클래스 구현에 대한 가정을 하는 것이 항상 안전하지는 않다

=> 서브클래스가 __slots__ 을 사용하기로 하거나 특정 속성을 프로퍼티로 감싸기로 하면, 인스턴스 딕셔너리에
   직접 접근할 때 문제가 발생한다
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 유틸리티 함수와 소위 프레임 핵(frame hack) 을 사용하면 인스턴스 변수를 자동으로 초기화할 수도 있다 
--------------------------------------------------------------------------------------
'''

def init_fromlocal(self):
    import sys
    locs = sys._getframe(1).f_locals
    for k, v in locs.items():
        if k != 'self':
            setattr(self, k, v)
    class Stock:
        def __init__(self, name, shares, price):
            init_fromlocal(self)
