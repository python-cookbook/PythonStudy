###############################################################################################################
## 8.12 인터페이스, 추상 베이스 클래스 정의
# 인터페이스나 추상 베이스 클래스 역할을 하는 클래스를 정의하고 싶다. 그리고 이 클래스는 타입 확인을 하고
# 특정 메소드가 서브 클래스에 구현되었는지 보장한다.
###############################################################################################################
# 추상 베이스 클래스 정의를 위해선 abc 모듈을 써야한다
from abc import ABCMeta, abstractmethod


class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass

    @abstractmethod
    def write(self, data):
        pass


## 추상 베이스 클래스의 주요 기능은 직접 인스턴스화 할 수 없다는 점이다
# 추상 베이스 클래스는 요구한 메소드를 구현하는 다른 클래스의 베이스 클래스로 사용해야 한다
class SocketStream(IStream):
    def read(self, maxbytes=-1):

    # ...
    def write(self, data):


# ...


## 이건 특정 프로그래밍 인터페이스를 강요하고 싶을 때 주로 사용한다
# 예를 들어 IStream 베이스 클래스는 데이터를 읽거나 쓰는 인터페이스에 대한 상위 레벨 스펙으로 볼 수 있다
def serialize(obj, stream):
    if not isinstance(stream, IStream):
        raise TypeError('Expected an IStream')
        # ...


# 이런 타입 확인 코드는 서브클래싱과 추상 베이스 클래스(ABC)에서만 동작할 것 같지만
# ABC는 다른 클래스가 특정 인터페이스를 구현했는지 확인하도록 허용한다
import io

# 내장 I/O 클래스를 우리의 인터페이스를 지원하도록 등록
IStream.register(io.IOBase)

# 일반 파일을 열고 타입 확인
f = open('foo.txt')
isinstance(f, IStream)  # True 반환

## @abstractmethod를 static method, class method, property에도 적용할 수 있다
# 단지 함수 정의 직전에 @abstractmethod를 적용해야 한다는 점만 기억하자
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


###############################################################################################################
## 8.13 데이터 모델 혹은 타입 시스템 구현
# 여러 종류의 자료 구조를 정의하고 싶다. 이때 특정 값에 제약을 걸어 원하는 속성이 할당되도록 하고 싶다
###############################################################################################################
# 기본적으로 특정 인스턴스 속성의 값을 설정할 때 확인을 하는 동작을 구현해야 한다.
# 이렇게 하려면 속성을 설정하는 부분을 속성 하나 단위로 커스터마이즈 해야하고, 디스크립터로 해결 가능하다

## 다음 코드는 디스크립터로 시스템 타입과 값 확인 프레임워크를 구현하는 방법을 보여준다
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
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super().__set__(instance, value)


## 앞에 나온 클래스는 데이터 모델이나 타입 시스템을 만들 때 기반으로 사용하는 빌딩 블록으로 봐야한다
# 이제 서로 다른 데이터를 구현하는 코드를 보자
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


## 타입 객체를 사용해서 다음과 같은 클래스를 정의할 수 있다
class Stock:
    # 제약 명시
    name = SizedString('name', size=8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


s = Stock('ACME', 50, 91.1)
print(s.name)


# 'ACME'


## 제약을 위한 클래스 데코레이터
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


## 예제
@check_attributes(name=SizedString(size=8),
                  shares=UnsignedInteger,
                  price=UnsignedFloat)
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


## 메타클래스를 쓸 수도 있다
class checkedmeta(type):
    def __new__(cls, clsname, bases, methods):
        # 디스크립터에 속성 이름 붙이기
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                value.name = key
        return type.__new__(cls, clsname, bases, methods)


# 예제
class Stock(metaclass=checkedmeta):
    name = SizedString(size=8)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


# 디스크립터의 모든 __init__() 메소드는 키워드 매개변수 **opts를 포함해서 동일한 시그니처를 가지도록 프로그램되어 있다
# MaxSized 클래스는 opts에서 요청한 속성을 갖지만, 이를 설정하는 Descriptor 베이스 클래스에 전달한다
# 이런 클래스를 작성할 때 주의해야 할 점은 클래스들이 어떻게 묶일지 혹은 어떤 super()가 호출될지 알 수 없다는 점이다
# 따라서 어떠한 조합으로도 잘 동작하도록 구현해야 한다.


## 일반
class Point:
    x = Integer('x')
    y = Integer('y')


# 메타클래스
class Point(metaclass=checkedmeta):
    x = Integer()
    y = Integer()


# 클래스 데코레이터와 메타클래스 코드는 단순히 클래스 딕셔너리에서 디스크립터를 찾는다
# 디스크립터를 찾으면 키 값에 기반한 이름을 채워 넣는다

## 앞서 나온 방식 중 클래스 데코레이터 방식이 가장 유연하고 안전하다
# 우선 메타클래스와 같은 고급 기술에 의존하지 않는다
# 데코레이션은 원할 때면 클래스 정의에 쉽게 추가하거나 제거할 수 있다
# 클래스 데코레이터 방식은 Mixin class, 다중 상속, 복잡한 super() 대신 사용할 수 있다

## 베이스 클래스. 값을 설정할 때 디스크립터를 사용
class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


## 타입 확인에 데코레이터 사용
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


# Unsigned 값에 데코레이터 사용
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
        super_init(self, name, **opts)

    cls.__init__ = __init__

    super_set = cls.__set__

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


# 특별 스크립터
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


###############################################################################################################
## 8.14 커스텀 컨테이너 구현
# 리스트나 딕셔너리와 같은 내장 컨테이너와 비슷하게 동작하는 커스텀 클래스를 구현하고 싶다.
# 하지만 이때 정확히 어떤 메소드를 구현해야 할지 확신이 안 선다
###############################################################################################################
# collections 라이브러리에 이 목적으로 사용하기 위한 적절한 추상 베이스 클래스가 많이 정의되어 있다.
import collections


class A(collections.Iterable):  # collections.Iterable 상속받는 것으로 시작
    pass  # ↑이걸 상속받으면 필요한 모든 특별 메소드를 구현하도록 보장


# collections에 정의되어 있는 클래스에 또 주목할만한 것으로 Sequence,Mutable Sequence,Mapping,MutableMapping, Set,
# MutableSet이 있다. 이 클래스 중 다수는 기능이 증가한다. Containter,Iterable,Sized,Sequence,MutableSequence
# 이 클래스에 어떤 메소드를 구현할지 확인하려면 인스턴스화 해보면 된다

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


## 다음은 클래스를 사용하는 예제이다
items = SortedItems([5, 1, 3])
list(items)  # 빈 리스트가 나옵니다?     쿡북은 [1,3,5]가 나온다곤 하는데...

print(items[0])  # 1
print(items[-1])  # 5
items.add(2)  # [1,2,3,5]
print(list(items))  # [-10,1,2,3,5]
print(items[1:4])  # [1,2,3]

3 in items  # True          ..결과값이 도저히 안나오지 말입니다
len(items)  # 5

for n in items:  # -10
    print(n)  # 1
    #   2
    #   3
    #   5

## SortedItems의 인스턴스는 보통의 시퀀스와 동일한 동작을 하고, 인덱싱, 순환, len(), in 연산자, 자르기 등
# 일반적인 연산을 모두 지원한다.
## bisect.insort()는 아이템을 리스트에 넣고 리스트가 순서를 유지하도록 만든다

# collections에 있는 추상 베이스 클래스를 상속받으면 커스텀 컨테이너에 필요한 메소드를 모두 구현하도록 보장할 수 있다
# 이 상속에는 타입 확인 기능도 있다
items = SortedItems()
import collections

isinstance(items, collections.Iterable)  # True
isinstance(items, collections.Sequence)  # True
isinstance(items, collections.Container)  # True
isinstance(items, collections.Sized)  # True
isinstance(items, collections.Mapping)  # False


# collections에 있는 추상 베이스 클래스는 일반적인 컨테이너 메소드의 기본 구현을 제공하는 것도 많다
# 아래 예시는 collections.MutableSequence에서 상속받는 클래스이다
class Items(collections.MutableSequence):
    def __init__(self, initial=None):
        self._items = list(initial) if initial is None else []

    # 필요한 시퀀스 메소드
    def __getitem__(self, index):
        print('Getting: ', index)
        return self._items[index]

    def __setitem__(self, index, value):
        print('Setting: ', index, value)
        self._items[index] = value

    def __delitem__(self, index):
        print('Deleting: ', index)
        del self._items[index]

    def insert(self, index, value):
        print('Inserting: ', index, value)
        self._items.insert(index, value)

    def __len__(self):
        print('Len')
        return len(self._items)


## Items의 인스턴스를 만들면 리스트 메소드 중 중요한 것을 거의 다 지원한다는 것을 확인할 수 있다
# append(), remove(), count() 등등
# 이런 메소드는 필요한 것만 사용하는 식으로 구현되어 있다

a = Items([1, 2, 3])
print(len(a))                       # 왜 Len이랑 0이 나오지?
print(a.append(4))                  # 그래도 0이 나오네? inserting: 0 4 라고 나온다
print(a.count(2))                   # 또 0임..? Getting: 0
                                    #           Getting: 1
                                    #           0
print(a.remove(3))



###############################################################################################################
## 8.15 속성 접근 델리케이팅
# 인스턴스가 속성에 대한 접근을 내부 인스턴스로 델리게이트(delegate)해서 상속의 대안으로 사용하거나
# 프록시 구현을 하고 싶다
###############################################################################################################
# delegate는 특정 동작에 대한 구현 책임을 다른 객체에게 미루는 (delegate / 위임하다) 프로그래밍 패턴이다
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


## delegate 할 메소드가 몇 개 없으면, 주어진 코드를 그대로 작성해도 무방하다
# 하지만 delegate 해야 할 메소드가 많다면, 또 다른 대안으로 다음과 같이 __getattr__() 메소드를 정의할 수 있다
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


# __getattr__() 메소드는 속성을 찾아 보는 도구 모음 정도로 생각하면 된다. 이 메소드는 코드가 존재하지 않는 속성에
# 접근하려고 할 때 호출된다. 앞에 나온 코드에서 정의하지 않은 B에 대한 접근을 A로 delegate 한다
b = B()
b.bar()  # B.bar()호출 (B에 존재함)
b.spam(42)  # B.__getattr__('spam') 호출하고 A.spam으로 delegate


## 델리게이트의 또 다른 예제로 프록시 구현이 있다
# 다른 객체를 감싸는 프록시 클래스, 하지만 public 속성을 노출한다
class Proxy:
    def __init__(self, obj):
        self._obj = obj

    # 속성 검색을 내부 객체로 델리게이트
    def __getattr__(self, name):
        print('getattr: ', name)
        return getattr(self._obj, name)

    # 속성 할당 델리게이트
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            print('setattr: ', name, value)
            setattr(self._obj, name, value)

    # 속성 삭제 델리게이트
    def __delattr__(self, name):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            print('delattr: ', name)
            delattr(self._obj, name)


# 이 프록시 클래스를 사용하려면, 단순히 다른 인스턴스를 감싸면 된다
class Spam:
    def __init__(self, x):
        self.x = x

    def bar(self, y):
        print('Spam.bar: ', self.x, y)


# 인스턴스 생성
s = Spam(2)

# 프록시를 만들고 감싸기
p = Proxy(s)

# 프록시에 접근
print(p.x)  # 2 출력
p.bar(3)  # "Spam.bar: 2 3" 출력
p.x = 37  # s.x를 37로 변경


## delegate는 상속의 대안으로 사용하기도 한다
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


# 델리게이트를 활용해서 다음과 같이 작성할 수 있다
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


## 프록시를 구현하기 위해 델리게이트를 사용할 때, remember
# 1. __getattr__() 메소드는 속성을 찾을 수 없을 때 한 번만 호출되는 fallback 메소드이다
# 2. __setattr__()과 __delattr__() 메소드는 프록시 인스턴스 자체와 내부 객체 _obj 속성의 개별 속성에 추가된 로직을
# 필요로 한다
# 3. __getattr__() 메소드는 밑줄 두 개로 시작하는 대부분의 특별 메소드에 적용되지 않는다.


class ListLike:
    def __init__(self):
        self._items = []

    def __getattr__(self, name):
        return getattr(self._items, name)


# a = ListLike()
# a.append(2)
# a.insert(0,1)
# a.sort()

## 서로 다른 연산을 지원하려면, 수동으로 관련된 특별 메소드를 델리게이트해야 한다
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


########################################################################################################################
## 8.16 클래스에 생성자 여러 개 정의
# 클래스를 작성 중인데, 사용자가 __init__()이 제공하는 방식 이외에 여러가지 방식으로 인스턴스를 생성하도록 하고 싶다
########################################################################################################################
# 생성자를 여러개 정의하려면 클래스 메소드를 사용해야 한다
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


# 두번째 생성자를 사용하려면 Date.today()와 같이 함수인 것처럼 호출해야 한다
a = Date(2012, 12, 21)  # 기본
b = Date.toady()  # 대안


## 클래스를 첫 번째 인자(cls)로 받는 것이 클래스 메소드의 중요한 기능이다
# 이 클래스는 메소드 내부에서 인스턴스를 생성하고 반환하기 위해 사용된다.
# 이 때문에 클래스 메소드가 상속과 같은 기능과도 잘 동작하게 된다
class NewDate(Date):
    pass


c = Date.today()  # Date (cls = Date) 인스턴스 생성
d = NewDate.today()  # NewDate (cls = NewDate) 인스턴스 생성


########################################################################################################################
## 8.17 init 호출없이 인스턴스 생성
# 인스턴스를 생성해야 하는데, __init__() 메소드 호출을 피하고 싶다
# 클래스의 __new__() 메소드를 호출해서 초기화하지 않은 인스턴스를 생성할 수 없다
########################################################################################################################
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day


# __init__() 호출없이 Data 인스턴스를 생성해보자
d = Date.__new__(Date)
# print(d)                                            # <Date object at 0x00000000034DD630>
# print(d.year)
# Traceback (most recent call last):
#   File "<input>", line 10, in <module>
# AttributeError: 'Date' object has no attribute 'year'

data = {'year': 2012, 'month': 8, 'day': 29}
for key, value in data.items():
    setattr(d, key, value)

print(d.year)  # 2012
print(d.month)  # 8

# __init__()을 생략하면 데이터 역직렬화(deserializing)나 대안 생성자로 정의한 클래스 메소드의 구현과 같이
# 비표준 방식으로 인스턴스를 생성할 때 문제가 발생하기도 한다. 예를 들어, Date 클래스에 today()를 다음과 같이 정의할 수 있다
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




########################################################################################################################
## 8.18 믹스인으로 클래스 확장
# 유용한 메소드를 여러 개 가지고 있고, 이 메소드를 클래스 기능 확장에 사용하고 싶다. 하지만 메소드를 붙일 클래스는
# 서로 상속관계로 묶여 있지 않다. 따라서 단순 기본 베이스 클래스에 메소드를 추가할 수는 없는 상황이다
########################################################################################################################
# 위의 문제는 클래스를 커스터마이즈하려고 할 때 종종 발생한다. 라이브러리가 기본 클래스 세트와 사용자가 원하는 경우
# 추가적으로 적용 가능한 커스터마이즈를 제공한다

## 설명을 위해 매핑 객체에 여러가지 커스터마이즈(로깅, 한 번만 설정, 타입 확인 등)를 추가하고 싶다고 가정해보자
# 클래스 혼용 예제
class LoggedMappingMixin:
    '''
    get/set/delete에 로깅 추가
    '''
    __slots__ = ()

    def __getitem__(self, key):
        print('Getting: ' + str(key))
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        print('Setting {} = {!r}'.format(key, value))
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        print('Deleting ' + str(key))
        return super().__delitem__(key)


class SetOnceMappingMixin:
    '''
    키가 한 번만 설정되도록 함
    '''
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + ' already set')
        return super().__setitem__(key, value)


class StringKEysMappingMixin:
    '''
    키에 문자열 허용
    '''
    __slots__ = ()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('keys must be strings')
        return super().__setitem__(key, value)


# 이 클래스들은 자체로는 쓸모가 없으며, 다른 매핑 클래스와 함께 다중 상속을 통해 혼용해야 한다
class LoggedDict(LoggedMappingMixin, dict):
    pass


d = LoggedDict()
d['x'] = 23  # Setting x = 23
d['x']  # Getting x
# 23
del d['x']  # Deleting x

from collections import defaultdict


class SetOnceDefaultDict(SetOnceMappingMixin, defaultdict):
    pass


d = SetOnceDefaultDict(list)
d['x'].append(2)
d['y'].append(3)
d['x'].append(10)
# d['x'] = 23

# 이 예제에서 mixin은 기존 클래스(dict,defaultdict,ordereddict)나 자기들끼리 합치는 것을 볼 수 있다
# 이렇게 결합했을 때 클래스들은 원하는 기능을 제공하기 위해 함께 동작한다

## mixin 클래스를 사용하는 표준 라이브러리가 많은데, 다중 상속도 주된 사용처 중 하나이다.
# 네트워크 코드를 작성한다면 socketserver 모듈의 ThreadMixIn을 사용해서 다른 네트워크 관련 클래스에 스레드 지원을
# 추가 가능함. 다음 코드는 멀티스레드 XMLRPC 서버 예제이다
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


## 믹스인 클래스는 절대로 직접 인스턴스화 하면 안된다. 이건 원하는 기능을 위해 다른 클래스와 함께 사용해야 한다
# socketserver 라이브러리의 ThreadingMixIn은 그 자체로 쓰지 말고 올바른 서브 클래스와 함께 사용해야 한다

## 믹스인 클래스는 일반적으로 스스로의 상태를 소유하지 않는다. 따라서 __init__() 메소드와 인스턴스 변수가 없다
## __init__() 메소드와 인스턴스 변수가 있는 믹스인 클래스를 정의할 생각이라면, 다른 클래스와 어떻게 혼용될 것인지
# 전혀 모른다는 위험성이 있다. 때문에 인스턴스 변수의 이름을 절대로 다른 클래스의 변수와 충돌하지 않게 만들어야 한다

## __init__() 메소드는 혼용하는 다른 클래스의 __init__() 메소드를 제대로 호출하도록 프로그래밍해야 한다
# at least, *arg, **kwargs 같이 제너럴한 방식으로 구현할 필요가 있다



# 믹스인 클래스의 __init__()이 자기 자신의 어떠한 매개변수라도 받는다면, 다른 변수와 충돌 방지를 위해 키워드로
# 명시해야 한다. 믹스인 클래스에서 __init__()을 정의하고 키워드 매개변수를 받는 구현법을 보자
class RestrictKeysMixin:
    def __init__(self, *args, _restrict_key_type, **kwargs):
        self.__restrict_key_type = _restrict_key_type
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if not isinstance(key, self.__restrict_key_type):
            raise TypeError('Keys must be ' + str(self.__restrict_key_type))
        super().__setitem__(key, value)


# 이 클래스를 사용하는 방법
class RDict(RestrictKeysMixin, dict):
    pass


d = RDict(_restrict_key_type=str)
e = RDict([('name', 'Dave'), ('n', 37)], _restrict_key_type=str)
f = RDict(name='Dave', n=37, _restrict_key_type=str)
print(f)


# {'name': 'Dave', 'n': 37}


## 클래스 데코레이터를 사용해서 믹스인을 구현할 수도 있다
def LoggedMapping(cls):
    cls_getitem = cls.__getitem__
    cls_setitem = cls.__setitem__
    cls_delitem = cls.__delitem__

    def __getitem__(self, key):
        print('Getting ' + str(key))
        return cls_getitem(self, key)

    def __setitem__(self, key, value):
        print('Setting {} = {!r}'.format(key, value))
        return cls_setitem(self, key, value)

    def __delitem__(self, key):
        print('Deleting ' + str(key))
        return cls_delitem(self, key)

    cls.__getitem__ = __getitem__
    cls.__setitem__ = __setitem__
    cls.__delitem__ = __delitem__
    return cls


# 이 함수는 클래스 정의에 decorator로 적용된다
@LoggedMapping
class LoggedDict(dict):
    pass


########################################################################################################################
## 8.19 상태 객체 혹은 상태 기계 구현
# 상태 기계나 여러 상태로 동작하는 객체를 구현하고 싶다. 하지만 코드에 수많은 조건문이 들어가는 상황은 안 원함
# 특정 어플리케이션에서 내부 상태에 따라 다른 동작을 하는 객체가 필요한 경우가 있다.
########################################################################################################################
# 연결 상태를 나타내는 간단한 클래스를 보자
class Connection:
    def __init__(self):
        self.state = 'CLOSED'

    def read(self):
        if self.state != 'OPEN':
            raise RuntimeError('Not open')
        print('reading')

    def write(self, data):
        if self.state != 'OPEN':
            raise RuntimeError('Not open')
        print('writing')

    def open(self):
        if self.state == 'OPEN':
            raise RuntimeError('Already open')
        self.state = 'OPEN'

    def close(self):
        if self.state == 'CLOSED':
            raise RuntimeError('Already closed')
        self.state = 'CLOSED'


# 이 구현 방법의 어려운 점 : 첫째, 상태를 확인하는 조건문이 너무 많아 복잡하다
# 둘째, read(),write()와 같은 일반적인 동작이 항상 상태를 확인해서 성능이 떨어진다

## 괜찮은 구현법은 상태 관련 동작은 별도의 클래스로 만들고 Connection 클래스를 상태 클래스로 델리게이트 하는 것이다
class Connection:
    def __init__(self):
        self.new_state(ClosedConnectionState)

    def new_state(self, newstate):
        self._state = newstate

    # 상태 클래스로 델리게이트
    def read(self):
        return NotImplementedError()

    def write(self, data):
        return NotImplementedError()

    def open(self):
        return NotImplementedError()

    def close(self):
        return NotImplementedError()


# 여러 상태 구현
class ClosedConnection(Connection):
    def read(self):
        raise RuntimeError('Not open')

    def write(self, data):
        raise RuntimeError('Not open')

    def open(self):
        self.new_state(OpenConnection)

    def cloas(self):
        raise RuntimeError('Already closed')


class OpenConnection(Connection):
    def read(self):
        print('reading')

    def write(self, data):
        print('writing')

    def open(self):
        raise RuntimeError('Already open')

    def close(self):
        self.new_state(ClosedConnection)


c = Connection()
print(c)  # <Connection object at 0x00000000034D4358>


# 원본
class State:
    def __init__(self):
        self.state = 'A'

    def action(self,x):
        if state == 'A':
            # A 동작
            # ...
            state = 'B'

        elif state == 'B':
            # B 동작
            # ...
            state = 'C'

        elif state == 'C':
            # C 동작
            # ...
            state = 'A'


# 대안
class State:
    def __init__(self):
        self.new_state(State_A)

    def new_state(self,state):
        self.__class__ = state

    def action(self,x):
        raise NotImplementedError()

class State_A(State):
    def action(self,x):
        # A 동작
        # ...
        self.new_state(State_B)

class State_B(State):
    def action(self,x):
        # B 동작
        # ...
        self.new_state(State_C)


class State_C(State):
    def action(self,x):
        # C 동작
        # ...
        self.new_state(State_A)



########################################################################################################################
## 8.20 문자열로 이름이 주어진 객체의 메소드 호출
# 문자열로 저장된 메소드 이름을 가지고 있고, 이 메소드를 실행하고 싶다
########################################################################################################################
# 간단한 경우 getattr() 사용
import math

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({!r},{!r})'.format(self.x, self.y)

    def distance(self,x,y):
        return math.hypot(self.x - x, self.y - y)

p = Point(2,3)
d = getattr(p, 'distance')(0,0)


# 또는 operator.methodcaller() 사용
# 메소드를 이름으로 찾고 동일한 매개변수를 반복적으로 넣는 경우 이걸 쓰는게 좋다
import operator
operator.methodcaller('distance',0,0)(p)


# 포인트 리스트를 정렬하고 싶다면 다음과 같이 한다
points = [
    Point(1,2),
    Point(3,0),
    Point(10,-3),
    Point(-5,-7),
    Point(-1,8),
    Point(3,2)
]

# origin (0,0)의 거리를 기준으로 정렬
points.sort(key=operator.methodcaller('distance',0,0))


########################################################################################################################
## 8.24 비교 연산을 지우너하는 클래스 만들기
# 표준 비교 연산자(>=, !=, <= 등)를 사용해 클래스 인스턴스를 비교하고 싶다.
#  하지만 특별 메소드를 너무 많이 작성하고 싶지는 않다
########################################################################################################################
# 파이썬 클래스는 비교 연산을 위한 특별 메소드를 통해 인스턴스간에 비교 기능을 지원한다.
# >= 연산을 지원하려면 __ge__() 메소드를 정의하면 된다.

## functools.total_ordering 데코레이터를 사용시, 그 과정을 단순화 할 수 있다.
from functools import total_ordering

class Room:
    def __init__(self,name,length,width):
        self.name = name
        self.length = length
        self.width = width
        self.square_feet = self.length * self.width

@total_ordering
class House:
    def __init__(self,name,style):
        self.name = name
        self.style = style
        self.rooms = list()

    @property
    def living_space_footage(self):
        return sum(r.square_feet for r in self.rooms)

    def add_room(self,room):
        self.rooms.append(room)

    def __str__(self):
        return '{}: {} square foot {}'.format(self.name, self.living_space_footage,self.style)

    def __eq__(self,other):
        return self.living_space_footage == other.living_space_footage

    def __lt__(self,other):
        return self.living_space_footage < other.living_space_footage



# 정원이랑 별장을 몇 개 만들고(심시티..) 집도 추가한다
h1 = House('h1','Park')                                               # 공원 안의
h1.add_room(Room('침실',14,21))
h1.add_room(Room('거실',18,20))
h1.add_room(Room('부엌',12,16))
h1.add_room(Room('서재',12,12))

h2 = House('h2','Summer house')                                       # 여름 별장
h2.add_room(Room('침실',14,21))
h2.add_room(Room('거실',18,20))
h2.add_room(Room('부엌',12,16))

h3 = House('h3','Home')                                                  # 그리고 집
h3.add_room(Room('침실',14,21))
h3.add_room(Room('거실',18,20))
h3.add_room(Room('부엌',15,17))
houses = [h1, h2, h3]

print('Is h1 bigger than h2?', h1 > h2)                      # True 출력
print('Is h2 smaller than h3?',h2 > h3)                      # True
print('Is h2 greater than or equal to h1?', h2 > h1)        # False
print('Which one is the bestest and good?',max(houses))               # h3: 1101-square-foot Split
print('Which is smallest and comfortable?',min(houses))             # h2: 846-square-foot Ranch

# Is h1 bigger than h2? True
# Is h2 smaller than h3? False
# Is h2 greater than or equal to h1? False
# Which one is the bestest and good? h1: 990 square foot Park
# Which is smallest and comfortable? h2: 846 square foot Garden

