# 8.12 인터페이스, 추상 베이스 클래스 정의
from abc import ABCMeta, abstractmethod
class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass
    @abstractmethod
    def write(self, data):
        pass
a = IStream()

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
    name = SizedString('name', size=8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
s = Stock('ACME', 50, 91.1)
print(s.name)

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

class Point:
    x = Integer('x'
    y = Integer('y'


class Point(metaclass=checkedmeta):
    x = Integer(
    y = Integer()

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

def Unsigned(cls):
    super_set = cls.__set__
def __set__(self, instance, value):
    if value < 0:
        raise ValueError('Expected >= 0')
    super_set(self, instance, value)
cls.__set__ = __set__
return cls

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
import collections
import bisect
class SortedItems(collections.Sequence):
    def __init__(self, initial=None):
        self._items = sorted(initial) if initial is None else []


    def __getitem__(self, index):
        return self._items[index]
    def __len__(self):
        return len(self._items)
    # 올바른 장소에 아이템을 추가하기 위한 메소드
    def add(self, item):
        bisect.insort(self._items, item)

items = SortedItems([5,1,3])
print(list(items))
import collections
import bisect
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

    def __getattr__(self, name):
        return getattr(self._a, name)


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

    def __len__(self):
        return len(self._items)
    def __getitem__(self, index):
        return self._items[index]
    def __setitem__(self, index, value):
        self._items[index] = value
    def __delitem__(self, index):
        del self._items[index]


# 8.16 클래스에 생성자 여러 개 정의
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

import operator
operator.methodcaller('distance', 0, 0)(p)
points = [Point(1, 2),Point(3, 0),Point(10, -3),Point(-5, -7),Point(-1, 8),Point(3, 2)]
points.sort(key=operator.methodcaller('distance', 0, 0))



# 8.24 비교 연산을 지원하는 클래스 만들기
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
print('Is h2 smaller than h3?', h2 < h3)
print('Is h2 greater than or equal to h1?', h2 >= h1)
print('Which one is biggest?', max(houses))
print('Which is smallest?', min(houses))
