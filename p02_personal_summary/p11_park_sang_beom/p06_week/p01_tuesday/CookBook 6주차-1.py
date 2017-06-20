'''
--------------------------------------------------------------------------------------
8.12 인터페이스, 추상 베이스 클래스 정의

문제 : 인터페이스나 추상 베이스 클래스 역할을 하는 클래스를 정의하고 이 클래스는 타입 확인을 하고 특정 메소드가
      서브 클래스에 구현되었는지 보장하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 추상 베이스 클래스를 정의하려면 abc 모듈 사용
--------------------------------------------------------------------------------------
'''

from abc import ABCMeta, abstractclassmethod

class IStream(metaclass=ABCMeta):
    @abstractclassmethod
    def read(self, maxbytes=-1):
        pass
    @abstractclassmethod
    def write(self, data):
        pass

'''
=> 추상 베이스 클래스의 주요 기능은 직접 인스턴스화 할 수 없다!!!

=> 추상 베이스 클래승는 요구한 메소드를 구현하는 다른 클래스의 베이스 클래스로 사용해야 한다!!

=> 추상 클래스는 특정 프로그래밍 인터페이스를 강요하고 싶을 때 주로 사용!!
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 인터페이스를 명시적으로 확인하는 예제
--------------------------------------------------------------------------------------
'''

def serialize(obj, stream):
    if not isinstance(stream, IStream):
        raise TypeError('Expeected an IStream')
    ...

'''
--------------------------------------------------------------------------------------
- ABC는 다른 클래스가 특정 인터페이스를 구현하는 예제
--------------------------------------------------------------------------------------
'''

import io

# 내장 I/O 클래스를 우리의 인터페이스를 지원하도록 등록
IStream.register(io.IOBase)

# 일반 파일을 열고 타입 확인
f = open('e:\data\somefile.txt')

print(isinstance(f, IStream))

'''
--------------------------------------------------------------------------------------
- @abstractmethod 를 스태틱 메소드(static method), 클래스 메소드, 프로퍼티에도 적용할 수 도 있다
--------------------------------------------------------------------------------------
'''

class A(metaclass=ABCMeta):
    @property
    @abstractclassmethod
    def name(self):
        pass

    @name.setter
    @abstractclassmethod
    def name(self, value):
        pass

    @classmethod
    @abstractclassmethod
    def method(cls):
        pass

    @staticmethod
    @abstractclassmethod
    def method2():
        pass

'''
--------------------------------------------------------------------------------------
- 추상 베이스 클래스를 더 일반적인 타입 확인에 사용 가능
--------------------------------------------------------------------------------------
'''

import collections

x = ''

# x 가 시퀀스인지 확인
if isinstance(x, collections.Sequence):
    ...

# x 가 순환 가능한지 확인
if isinstance(x, collections.Iterable):
    ...

# x 가 크기가 있는지 확인
if isinstance(x, collections.Sized):
    ...

# x 가 매핑인지 확인
if isinstance(x, collections.Mapping):
    ...





'''
--------------------------------------------------------------------------------------
8.13 관리 속성 만들기

문제 : 여러 종류의 자료 구조를 정의하고 싶다. 이때 특정 값에 제약을 걸어 원하는 속성이 할당되도록 하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 디스크립터로 시스템 타입과 값 확인 프레임워크를 구현 예제
--------------------------------------------------------------------------------------
'''

# 베이스 클래스, 디스크립터로 값을 설정한다
class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

# 타입을 강제하기 위한 디스크립터
class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('expected' + str(self.expected_type))
        super().__set__(instance, value)

# 값을 강제하기 위한 디스크립터
class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super().__set__(instance, value)

class MaxSized(Descriptor):
    def __int__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be' + str(self.size))
        super().__set__(instance, value)

'''
--------------------------------------------------------------------------------------
- 서로 다른 데이터를 구현하는 예제
--------------------------------------------------------------------------------------
'''

class Integer(Typed):
    expected_type = int

class UnisgnedInteger(Integer, Unsigned):
    pass

class Float(Typed):
    expected_type = float

class UnsignedFloat(Float, Unsigned):
    pass

class String(Typed):
    expected_type = str

class SizedString(String, MaxSized):
    pass

'''
--------------------------------------------------------------------------------------
- 타입 객체를 사용해서 다음과 같은 클래스를 정의
--------------------------------------------------------------------------------------
'''

class Stock:
    # 제약 명시
    name = SizedString('name', size=8)
    shares = UnisgnedInteger('shares')
    price = UnsignedFloat('price')

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

s = Stock('ACME', 50, 91.1)
s.shares = 75
s.shares = -10          # 에러
s.price = 'a lot'       # 에러
s.name = 'ABRACADABRA'  # 에러

print(s.name)

'''
--------------------------------------------------------------------------------------
- 클래스 데코레이터 사용하는 예제
--------------------------------------------------------------------------------------
'''

# 제약을 위한 클래스 데코레이터
def check_attributes(**kwargs):
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls
    return decorate

# 예제
@check_attributes(name=SizedString(size=8),
                  shares=UnisgnedInteger,
                  price=UnsignedFloat)

class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

# 확인을 위한 메타클래스
class checkedmeta(type):
    def __new__(cls, clasname, bases, methods):
        # 디스크립터에 속성 이름 붙이기
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                value.name = key
        return type.__new__(cls, clasname, bases, methods)

# 예제
class Stock(metaclass=checkedmeta):
    name = SizedString(size=8)
    shares = UnisgnedInteger()
    price = UnsignedFloat()
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

'''
--------------------------------------------------------------------------------------
- 클래스 데코레이터나 메타클래스를 사용하면 사용자의 스펙을 단순화할 때 유용
--------------------------------------------------------------------------------------
'''

# 일반
class Point:
    x = Integer('x')
    y = Integer('y')

# 메타클래스
class Point(metaclass=checkedmeta):
    x = Integer()
    y = Integer()

'''
--------------------------------------------------------------------------------------
- 클래스 데코레이터의 방식은 믹스인(mixin) 클래스, 다중 상속, 복잡한 super() 대신 사용할 수 있다
--------------------------------------------------------------------------------------
'''

# 베이스 클래스, 값을 설정할 때 디스크립터를 사용
class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

# 타입 확인에 데코레이터 사용
def Typed(expected_type, cls=None):
    if cls is None:
        return lambda cls: Typed(expected_type, cls)

    super_set = cls.__set__
    def __set__(self, instance, value):
        if not isinstance(value, expected_type):
            raise TypeError('expected' + str(expected_type))
        super_set(self, instance, value)
    cls.__set__ = __set__
    return cls

# 언사인드(unsigned) 값에 데코레이터 사용
def Unsigned(cls):
    super_set = cls.__set__
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super_set(self, instance, value)
    cls.__set__ = __set__
    return cls

# 크기 있는 값에 데코레이터 사용
def MaxSized(cls):
    super_init = cls.__init__
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super_init = __init__
    cls.__init__ = __init__

    super_set = cls.__set__
    def __set__(self, instane, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super_set(self, instane, value)
    cls.__set__ = __set__
    return cls

# 특별 디스크립터
@Typed(int)
class Integer(Descriptor):
    pass

@Unsigned
class UnsignedInteger(Integer):
    pass

@Typed(float)
class Float(Descriptor):
    pass

@Unsigned
class UnsignedFloat(Float):
    pass

@Typed(str)
class String(Descriptor):
    pass

@MaxSized
class SizedString(String):
    pass





'''
--------------------------------------------------------------------------------------
8.14 커스텀 컨테이너 구현

문제 : 리스트나 딕셔너리와 같은 내장 컨테이너와 비슷하게 동작하는 커스텀 클래스를 구현하는데
      하지만 이때 정확히 어떤 메소드를 구현해야 할지 확신이 없다
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- collections 라이브러리에 이 목적으로 사용하기 적절한 추상 베이스 클래스가 많이 정의되어 있다
--------------------------------------------------------------------------------------
'''

import collections

class A(collections.Iterable):
    pass

a = A()     # 에러

'''
=> collections.Iterable 을 상속 받으면 필요한 모든 특별 메소드를 구현하도록 보장해 준다
 
=> 메소드 구현을 잊으면 인스턴스화 과정에서 에러 발생!

=> 에러를 고치려면 클래스가 필요로 하는 __iter__() 매소드 구현
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 필요한 메소드를 모두 구현해서 아이템을 정렬된 상태로 저장하는 시퀀스 예제
--------------------------------------------------------------------------------------
'''

import collections
import bisect

class SortedItems(collections.Sequence):
    def __init__(self, initial=None):
        self._items = sorted(initial) if initial is None else []

    # 필요한 시퀀스 메소드
    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    # 올바른 장소에 아이템을 추가하기 위한 메소드
    def add(self, item):
        bisect.insort(self._items, item)

items = SortedItems([5, 1, 3])
items.add(2)

print(list(items))
print(items[0])
print(items[-1])
print(items[1:4])
print(3 in items)
print(len(items))

for n in items:
    print(n)

'''
=> SortedItems의 인스턴스는 보통의 시퀀스와 동일한 동작을 하고 인덱싱, 순환, 
   len(), in 연산자, 자르기 등 일반적인 연산 모두 지원
   
=> bisect 모듈은 아이템을 정렬한 상태로 리스트에 보관할때 매우 편리
   bisect.insort() 는 아이템을 리스트에 넣고 리스트가 순서를 유지하도록 만든다
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 커스텀 컨테이너에 타입 확인 예제
--------------------------------------------------------------------------------------
'''

items = SortedItems()

import collections

print(isinstance(items, collections.Iterable))
print(isinstance(items, collections.Sequence))
print(isinstance(items, collections.Container))
print(isinstance(items, collections.Sized))
print(isinstance(items, collections.Mapping))

'''
--------------------------------------------------------------------------------------
- collections.MutableSequence 에서 상속 받는 클래스 예제
--------------------------------------------------------------------------------------
'''

import collections

class Items(collections.MutableSequence):
    def __init__(self, initial=None):
        self._items = list(initial) if initial is None else []

    # 필요한 시퀀스 메소드
    def __getitem__(self, index):
        print('Getting : ', index)
        return self._items[index]

    def __setitem__(self, index, value):
        print('Setting : ', index, value)
        self._items[index] = value

    def __delitem__(self, index):
        print('Deleting : ', index)
        del self._items[index]

    def insert(self, index, value):
        print('Inserting : ', index, value)

    def __len__(self):
        print('Len')
        return len(self._items)

a = Items([1, 2, 3])

print(len(a))
print(a.append((4)))
print(a.append((2)))
print(a.count(2))
print(a.remove(3))





'''
--------------------------------------------------------------------------------------
8.15 속성 접근 델리게이팅

문제 : 인스턴스가 속성에 대한 접근을 내부 인스턴스로 델리게이트(delegate) 해서 상속의 대안으로 사용하거나
      프록시 구현 하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 델리게이트는 특정 동작에 대한 구현 책임을 다른 객체에게 미루는(델리게이트) 프로그래밍 패턴
--------------------------------------------------------------------------------------
'''

class A:
    def spam(self, x):
        pass

    def foo(self):
        pass

class B:
    def __init__(self):
        self._a = A()

    def spam(self, x):
        # 내부 self._a 인스턴스로 델리게이트
        return self._a.spam(x)

    def foo(self):
        # 내부 self._a 인스턴스로 델리게이트
        return self._a.foo()

    def bar(self):
        pass

'''
--------------------------------------------------------------------------------------
- 델리게이트할 메소드가 몇 개 없으면, 주어진 코드를 그대로 작성해도 무방하다
  하지만, 델리게이트해야 할 메소드가 많으면 또 다른 대안으로 __getattr__() 메소드 정의
--------------------------------------------------------------------------------------
'''

class A:
    def spam(self, x):
        pass

    def foo(self):
        pass

class B:
    def __init__(self):
        self._a = A()

    def bar(self):
        pass

    # A 클래스에 정의한 모든 메소드를 노출한다
    def __getattr__(self, name):
        return getattr(self._a, name)

'''
=> __gatattr__() 메소드는 속성을 찾아 보는 도구 모음 정도로 생각
   이 메소드는 코드가 존재하지 않은 속성에 접근하려 할 때 호출
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 델리게이트의 또 다른 예제로 프록시 구현 
--------------------------------------------------------------------------------------
'''

# 다른 객체를 감싸는 프록시 클래스, 하지만 public 속성을 노출
class Proxy:
    def __init__(self, obj):
        self._obj = obj

    # 속성 검색을 내부 객체로 델리게이트
    def __getattr__(self, name):
        print('getattr : ', name)
        return getattr(self._obj, name)

    # 속성 할당 델리게이트
    def __setattr__(self, name, value):
        if name.startswitch('_'):
            super().__setattr__(name, value)
        else:
            print('setattr : ', name, value)
            setattr(self._obj, name, value)

    # 속성 삭제 델리게이트
    def __delete__(self, name):
        if name.startswitch('_'):
            super().__delattr__(name)
        else:
            print('delattr : ', name)
            delattr(self._obj, name)

# 이 프록시 클래스를 사용하려면, 단순히 다른 인스턴스를 감싸면 된다
class Spam:
    def __init__(self, x):
        self.x = x

    def bar(self, y):
        print('Spam.bar : ', self.x, y)

# 인스턴스 생성
s = Spam(2)

# 프록시를 만들고 감싸기
p = Proxy(s)

# 프록시에 접근
print(p.x)      # 2 출력
p.bar(3)        # 'Spam.bar : 2 3' 출력
p.x = 37        # s.x 를 37로 변경

'''
--------------------------------------------------------------------------------------
- 델리게이트는 상속의 대안으로 사용하기도 한다
--------------------------------------------------------------------------------------
'''

class A:
    def spam(self, x):
        print('A.spam', x)

    def foo(self):
        print('A.foo')

class B:
    def __init__(self):
        self._a = A()

    def spam(self, x):
        print('B.spam', x)
        self._a.spam(x)

    def bar(self):
        print('B.bar')

    def __getattr__(self, name):
        return getattr(self._a, name)

'''
=> 델리게이트를 사용하는 방식은 직접 상속이 어울리지 않거나 객체 간 관계를 더 조절하고 싶을 때
   (특정 메소드만 노출시키거나 인터페이스를 구현하는 등) 유용

=> 프록시를 구현하기 위해 델리게이트를 사용할 때 기억해야 할 사항 몇 가지

        - __getattr__() 메소드는 속성을 찾을 수 없을 때 한 번만 호출되는 풀백 메소드
          따라서 프록시 인스턴스의 속성 자체에 접근하는 경우, 이 메소드가 호출되지 않는다
          
        - __setattr__() 메소드는 프록시 인스턴스 자체와 내부 객체 _obj 속성의 개별 속성에
          추가된 로직을 필요로 한다
          
        - 프록시에 대한 일반적인 관례는, 밑줄로 시작하지 않는 속성만 델리게이트하는 것이다
          (프록시는 공용 속성만 노출한다)
          
        - __getattr__() 메소드는 밑줄 두 개로 시작하는 대부분의 특별 메소드에 적용되지 않는다는 점
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- ListLike 객체를 만들려고 하면 append() 와 insert() 같은 일반적인 리스트 메소드를 지원한다는 것
  하지만, len(), 아이템 검색 등의 연산을 지원하지 않는다
--------------------------------------------------------------------------------------
'''

class ListLike:
    def __init__(self):
        self._items = []

    def __getattr__(self, name):
        return getattr(self._items, name)

a = ListLike()
a.append(2)
a.insert(0, 1)
a.sort()

print(len((a)))     # 에러

'''
--------------------------------------------------------------------------------------
- 서로 다른 연산을 지원하려면, 수동으로 관련된 특별 메소드를 델리게이트 해야 한다
--------------------------------------------------------------------------------------
'''

class ListLike:
    def __init__(self):
        self.items = []

    def __getattr__(self, name):
        return getattr(self._items, name)

    # 특정 리스트 연산을 지원하기 위한 특별 메소드 추가
    def __len__(self):
        return len(self._items)

    def __getattr__(self, index):
        return self._items[index]

    def __setattr__(self, index, value):
        self._items[index] = value

    def __delitem__(self, index):
        del self._items[index]





'''
--------------------------------------------------------------------------------------
8.16 클래스에 생성자 여러 개 정의

문제 : 클래스를 작성 중인데, 사용자가 __init__() 이 제공하는 방식 이외에 여러 가지 방식으로 인스턴스를
      생성할 수 있도록 하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 생성자를 여러 개 정의하려면 클래스 메소드를 사용
--------------------------------------------------------------------------------------
'''

import time

class Date:
    # 기본 생성자
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # 대안 생성자
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)

# 두 번째 생성자를 사용하려면 Date.today() 와 같이 함수인 것처럼 호출
a = Date(2012, 12, 21)      # 기본
b = Date.today()            # 대안

'''
--------------------------------------------------------------------------------------
- 클래스 메소드를 사용하는 주된 목적 중 하나가 바로 앞에 나온 것과 같은 생성자를 정의하는 것

- 클래스를 첫 번째 인자(cls) 로 받는 것이 클래스 메소드의 중요한 기능이다
  이 클래스는 메소드 내부에서 인스턴스를 생성하고 반환하기 위해 사용
-------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 개별적인 클래스 메소드를 정의하지 않고, __init__() 메소드에서 여러 동작을 호출
--------------------------------------------------------------------------------------
'''

import time

class Date:
    def __init__(self, *args):
        if len(args) == 0:
            t = time.localtime()
            args = (t.tm_year, t.tm_mon, t.tm_mday)
        self.year, self.month, self.day = args





'''
--------------------------------------------------------------------------------------
8.17 init 호출 없이 인스턴스 생성

문제 : 인스턴스를 생성해야 하는데 __init__() 메소드 호출 피하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 클래스의 __new__() 메소드를 호출해서 초기화하지 않은 인스턴스를 생성할 수 있다
--------------------------------------------------------------------------------------
'''

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

# __init__() 호출 없이 Date 인스턴스 생성
d = Date.__new__(Date)

print(d)
print(d.year)       # 에러

# 생성된 인스턴슨느 초기화되지 않았다. 따라서 적절한 인스턴스 변수를 설정하는 것은 사용자의 몫이다
date = {'year':2012, 'month':8, 'day':29}

for key, value in date.items():
    setattr(d, key, value)

print(d.year)
print(d.month)

'''
--------------------------------------------------------------------------------------
- __init__() 을 생략하면 데이터 역직렬화나 대안 생성자로 정의한 클래스 메소드의 구현과 같이
  비표준 방식으로 인스턴스를 생성할 때 문제가 발생하기도 한다
--------------------------------------------------------------------------------------
'''

from time import localtime

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def today(cls):
        d = cls.__new__(cls)
        t = localtime()
        d.year = t.tm_year
        d.month = t.tm_mon
        d.day = t.tm_mday
        return d





'''
--------------------------------------------------------------------------------------
8.20 문자열로 이름이 주어진 객체의 메소드 호출

문제 : 문자열로 저장된 메소드 이름을 가지고 있고, 이 메소드를 실행
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- getattr() 사용
--------------------------------------------------------------------------------------
'''

import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({!r:}, {!r:})'.format(self.x, self.y)

    def distance(self, x, y):
        return math.hypot(self.x - x, self.y - y)

p = Point(2, 3)
d = getattr(p, 'distance')(0, 0)        # p.distance(0, 0) 호출

# operator.methodcaller() 사용
import operator

operator.methodcaller('distance', 0, 0)(p)

'''
=> 메소드를 이름으로 찾고 동일한 매개변수를 반복적으로 넣는 경우 operator.methodcaller() 사용
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 포인트 리스트 정렬
--------------------------------------------------------------------------------------
'''

point = [ Point(1, 2), Point(3, 0), Point(10. -3),
          Point(-5, -7), Point(-1, 8), Point(3, 2)]

# origin (0, 0) 의 거리를 기준으로 정렬
point.sort(key=operator.methodcaller('distance', 0, 0))

'''
--------------------------------------------------------------------------------------
- operator.methodcaller() 는 호출 가능 객체를 생성하지만, 또한 메소드에 주어질 매개변수를 고정시키는 역할
--------------------------------------------------------------------------------------
'''

p = Point(3, 4)
d = operator.methodcaller('distance', 0, 0)

print(d(p))





'''
--------------------------------------------------------------------------------------
8.24 비교 연산을 지원하는 클래스 만들기

문제 : 표준 비교 연산자(>=, !=, <= 등)를 사용해 클래스 인스턴스를 비교하기
      하지만, 특별 메소드를 너무 많이 작성하고 싶지 않다
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- functools.total_ordering 데코레이터 사용
--------------------------------------------------------------------------------------
'''

from functools import total_ordering

class Room:
    def __init__(self, name, length, width):
        self.name = name
        self.length = length
        self.width = width
        self.square_feet = self.length * self.width

@total_ordering
class House:
    def __init__(self, name, style):
        self.name = name
        self.style = style
        self.rooms = list()

    @property
    def living_space_footage(self):
        return sum(r.square_feet for r in self.rooms)

    def add_room(self, room):
        self.rooms.append(room)

    def __str__(self):
        return '{} : {} square foot {}'.format(self.name, self.living_space_footage, self.style)

    def __eq__(self, other):
        return self.living_space_footage == other.living_space_footage

    def __lt__(self, other):
        return self.living_space_footage < other.living_space_footage

# 집을 몇 개 만들고 방을 추가한다
h1 = House('h1', 'Cape')
h1.add_room(Room('Master Bedroom', 14, 21))
h1.add_room(Room('Living Room', 18, 20))
h1.add_room(Room('Kitchen', 12, 16))
h1.add_room(Room('office', 12, 12))

h2 = House('h2', 'Ranch')
h2.add_room(Room('Master Bedroom', 14, 21))
h2.add_room(Room('Living Room', 18, 20))
h2.add_room(Room('Kitchen', 12, 16))

h3 = House('h3', 'Split')
h3.add_room(Room('Master Bedroom', 14, 21))
h3.add_room(Room('Living room', 18, 20))
h3.add_room(Room('office', 12, 16))
h3.add_room(Room('Kitchen', 15, 17))
houses = [h1, h2, h3]

print('Is h1 bigger than h2?', h1 > h2)
print('Is h2 smaller than h3?', h2 < h3)
print('Is h2 greater than or equal to h1?', h2 >= h1)
print('Which one is biggest?', max(houses))
print('which is smallest?', min(houses))

'''
--------------------------------------------------------------------------------------
- __lt__() 를 클래스에 정의하면 다른 비교 연산이 이 메소드를 사용
--------------------------------------------------------------------------------------
'''

class House:
    def __eq__(self, other):
        ...

    def __lt__(self, other):
        ...

    # @total_ordering 이 생성한 메소드
    __le__ = lambda self, other: self < other or self == other
    __gt__ = lambda self, other: not (self < other or self == other)
    __ge__ = lambda self, other: not (self < other)
    __ne__ = lambda self, other: not self == other













