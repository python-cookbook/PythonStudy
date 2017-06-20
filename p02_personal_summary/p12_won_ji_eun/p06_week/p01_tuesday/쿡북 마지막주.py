            # 8.12 인터페이스, 추상 베이스 클래스 정의

#문제 인터페이스나 추상 베이스 클래스 역할을 하는 클래스 정의

from abc import ABCMeta, abstractmethod
class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass
    @abstractmethod
    def write(self, data):
        pass
a = IStream()   # TypeError: 추상 메소드 read, write를 포함한
                # 추상 클래스 IStream을 인스턴스화할 수 없음

                
class SocketStream(IStream):
    def read(self, maxbytes=-1):
        pass
    
    def write(self, data):
        pass


from abc import ABCMeta, abstractmethod
class A(metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
        def name(self, value):
        pass

    @classmethod
    @abstractmethod
    def method1(cls):
        pass

    @staticmethod
    @abstractmethod
    def method2():
        pass

from decimal import Decimal
import numbers

x = Decimal('3.4')
isinstance(x, numbers.Real)


            # 8.13 데이터 모델 혹은 타입 시스템 구현

#문제: 여러 종류의 자료구조 정의 
#해결방법: 베이스 클래스. 디스크립터로 값을 설정한다.

# 베이스 클래스, 디스크립터로 값을 설정
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
            raise TypeError('expected ' + str(self.expected_type))
        super().__set__(instance, value)

#값을 강제하기 위한 디스크립터
class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super().__set__(instance, value)

class MaxSized(Descriptor):
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super().__set__(instance, value)
    
class Integer(Typed):
    expected_type = int

class UnsignedInteger(Integer, Unsigned):
    pass

class Float(Typed):
    expected_type = float

class UnsignedFloat(Float, Unsigned):
    pass

class String(Typed):
    expected_type = str

class SizedString(String, MaxSized):
    pass

class Stock:
    #제약 명시
    name = SizedString('name', size=8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

s = Stock('ACME', 50, 91.1)
print(s.name)


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


@check_attributes(name=SizedString(size=8),shares=UnsignedInteger,price=UnsignedFloat)
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


# 확인을 위한 메타 클래스
class checkedmeta(type):
    def __new__(cls, clsname, bases, methods):
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                value.name = key
        return type.__new__(cls, clsname, bases, methods)


class Stock(metaclass=checkedmeta):
    name = SizedString(size=8
    shares = UnsignedInteger()
    price = UnsignedFloat(
    def __init__(self, name, shares, price):
        self.name = nam
        self.shares = shares
        self.price = price


# 일반
class Point:
    x = Integer('x'
    y = Integer('y'

# 메타클래스
class Point(metaclass=checkedmeta):
    x = Integer(
    y = Integer()

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
            raise TypeError('expected ' + str(expected_type))
        super_set(self, instance, value)
    cls.__set__ = __set__
    return cls

# 언사이드 값에 데코레이터 사용
def Unsigned(cls):
    super_set = cls.__set__

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super_set(self, instance, value)
    cls.__set__ = __set__
    return cls

#크기 있는 값에 데코레이터 사용
def MaxSized(cls):
    super_init = cls.__init__
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super_init(self, name, **opts)
    cls.__init__ = __init__

    super_set = cls.__set__
    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super_set(self, instance, value)
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



            # 8.14 커스텀 콘테이너 구현
#문제 리스트나 딕셔너리와 같은 내장 컨테이너와 비슷하게 동작하는 커스텀 클래스를 구현하고 싶다


#아이템을 정렬된 상태로 저장하는 시퀀스
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


items = SortedItems([5,1,3])
print(list(items))


#collections.MutableSequence에서 상속받는 클래스
class Items(collections.MutableSequence):
    def __init__(self, initial=None):
        self._items = list(initial) if initial is None else []
        
    # 필요한 시퀀스 메소드
    def __getitem__(self, index):
        print('Getting:', index)
        return self._items[index]
    
    def __setitem__(self, index, value):
        print('Setting:', index, value)
        self._items[index] = value
                   
    def __delitem__(self, index):
        print('Deleting:', index)        
        del self._items[index]
        
    def insert(self, index, value):
        print('Inserting:', index, value)
        self._items.insert(index, value)
        
    def __len__(self):
        print('Len')
        return len(self._items)
    
a=Items([1,2,3])
print(len(a))

a.append(4)
a.count(2)
a.remove(3)



            # 8.15 속성 접근 델리게이팅

#문제: 인스턴스가 속성에 대한 접근을 내부 인스턴스로 델리게이트해서 상속의 대안으로 사용하거나 프록시 구현을 하고싶다
#해결방법: 델리게이트는 특정 동작에 대한 구현 책임을 다른 객체에게 미루는 프로그래밍 패턴

class A:
    def spam(self, x):
        pass
    def foo(self):
        pass
class B:
    def __init__(self):
        self._a = A()

    def spam(self, x):
    #  내부 self._a 인스턴스로 델리게이트
        return self._a.spam(x)

    def foo(self):
        # 내부 self._a 인스턴스로 델리게이트
        return self._a.foo()

    def bar(self):
        pass

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
    # A 클래스에 정의한 모든 메소드를 노출한다.

    def __getattr__(self, name):
        return getattr(self._a, name)


# 델리게이트의 또 다른 예제로 프록시 구현이 있다.
class Proxy:
    def __init__(self, obj):
        self._obj = obj

    # 속성 검색을 내부 객체로 델리게이트
    def __getattr__(self, name):
        print('getattr:', name)
        return getattr(self._obj, name)

    # 속성 할당 델리게이트
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            print('setattr:', name, value)
            setattr(self._obj, name, value)

    # 속성 삭제 델리게이트
    def __delattr__(self, name):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            print('delattr:', name)
            delattr(self._obj, name)


# 이 프록시 클래스를 사용하려면 단순히 다른 인스턴스를 감싸면 된다.
class Spam:
    def __init__(self, x):
        self.x = x

    def bar(self, y):
        print('Spam.bar:', self.x, y)

s = Spam(2)
p = Proxy(s)
print(p.x)
p.bar(3)
p.x = 37


# 델리 게이트는 상속의 대안으로 사용하기도한다. 예를 들어 다음과 같이 코드를 쓰지 않고
class A:
    def spam(self, x):
        print('A.spam', x)

    def foo(self):
        print('A.foo')

class B(A):
    def spam(self, x):
        print('B.spam')
        super().spam(x)

    def bar(self):
        print('B.bar')


# 델리게이트를 활용해서 다음과 같이 작성 할 수 있다.
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


# __getattr__() 메소드는 밑줄 두개로 시작하는 대부분의 특별 메소드에 적용되지 않는다는 점도 중요
class ListLike:
    def __init__(self):
        self._items = []
        
def __getattr__(self, name):
    return getattr(self._items, name)

a = ListLike()
a.append(2)
a.insert(0, 1)
a.sort()
len(a)


class ListLike:
    def __init__(self):
        self._items = []

    def __getattr__(self, name):
        return getattr(self._items, name)

    # 특정 리스트 연산을 지원하기 위한 특별 메소드 추가
    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value

    def __delitem__(self, index):
        del self._items[index]


            # 8.16 클래스에 생성자 여러 개 정의
#문제: __init__() 제공하는 방식 이외에 여러가지 방식으로 인스턴스를 생성할 수 있도록 하고 싶다.
#해결방법 : 생성자를 여러개 정의하려면 클래스 메소드를 사용해야 한다.

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

a = Date(2012, 12, 21)
b = Date.today()
print(a)
print(b)


class NewDate(Date):
    pass
c = Date.today()
d = NewDate.today()


class Date:
    def __init__(self, *args):
        if len(args) == 0:
            t = time.localtime()
            args = (t.tm_year, t.tm_mon, t.tm_mday)
            self.year, self.month, self.day = args
a = Date(2012, 12, 21)
b = Date()
c = Date.today()



            # 8.17 init 호출 없이 인스턴스 생성

# 해결방법: 클래스의 __new__() 메소드를 호출해서 초기화 하지 않는 인스턴스를 생성할 수 있다.
 
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

d = Date.__new__(Date)
print(d)
d.year
data = {'year':2012, 'month':8, 'day':29}

for key, value in data.items():
    setattr(d, key, value)

d.year
d.month


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

data = {'year': 2012, 'month': 8, 'day': 29}



            # 8.20 문자열로 이름이 주어진 객체의 메소드 호출
#해결방법: 문자열로 저장된 메소드 이름을 가지고 있고, 이 메소드를 실행하고 싶다면 getattr()를 사용하면 된다.
                                                
import math
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({!r:},{!r:})'.format(self.x, self.y)

    def distance(self, x, y):
        return math.hypot(self.x - x, self.y - y)

p = Point(2, 3)
d = getattr(p, 'distance')(0, 0) # Calls p.distance(0, 0)


# 혹은 operator.methodcaller()를 사용해도 된다.
import operator

operator.methodcaller('distance', 0, 0)(p)
points = [Point(1, 2),Point(3, 0),Point(10, -3),Point(-5, -7),Point(-1, 8),Point(3, 2)]
points.sort(key=operator.methodcaller('distance', 0, 0))



            # 8.24 비교 연산을 지원하는 클래스 만들기
#문제 표준 비교 연산자(>=, !=, <= 등)을 사용해 클래스 인스턴스를 비교

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
        return '{}: {} square foot {}'.format(self.name,self.living_space_footage,self.style)

    def __eq__(self, other):
        return self.living_space_footage == other.living_space_footage

    def __lt__(self, other):
        return self.living_space_footage < other.living_space_footage

h1 = House('h1', 'Cape')
h1.add_room(Room('Master Bedroom', 14, 21))
h1.add_room(Room('Living Room', 18, 20))
h1.add_room(Room('Kitchen', 12, 16))
h1.add_room(Room('Office', 12, 12))
h2 = House('h2', 'Ranch')
h2.add_room(Room('Master Bedroom', 14, 21))
h2.add_room(Room('Living Room', 18, 20))
h2.add_room(Room('Kitchen', 12, 16))
h3 = House('h3', 'Split')
h3.add_room(Room('Master Bedroom', 14, 21))
h3.add_room(Room('Living Room', 18, 20))
h3.add_room(Room('Office', 12, 16))
h3.add_room(Room('Kitchen', 15, 17))
houses = [h1, h2, h3]

print('Is h1 bigger than h2?', h1 > h2)
#실행결과 Is h1 bigger than h2? True
print('Is h2 smaller than h3?', h2 < h3)
#실행결과 Is h2 smaller than h3? True
print('Is h2 greater than or equal to h1?', h2 >= h1)
#실행결과 Is h2 greater than or equal to h1? False
print('Which one is biggest?', max(houses))
#실행결과 Which one is biggest? h3: 1101 square foot Split
print('Which is smallest?', min(houses))
#실행결과 Which is smallest? h2: 846 square foot Ranch