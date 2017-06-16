#8.6  관리속성만들기
class Person:
    def __init__(self, first_name):
        self.first_name = first_name


    @property
    def first_name(self):
        return self._first_name


    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('aaaaa')
        self._first_name = value


    @first_name.deleter
    def first_name(self):
        raise AttributeError("bbbbe")


a = Person('e')
a.first_name

a.first_name = 42

del a.first_name


class Person:
    def __init__(self, first_name):
        self.set_first_name(first_name)


    def get_first_name(self):
        return self._first_name

    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('eeee')
        self._first_name = value

    def del_first_name(self):
        raise AttributeError("eeas")


# 8.7 부모 클래스 메소드 호출
class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()

class A:
    def __init__(self):
        self.x = 0
class B(A):
    def __init__(self):
        super().__init__()
        self.y = 1


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


## 8.8 서브클래스 프로퍼티 확장


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
            raise TypeError('eee')
        self._name = value

    # deleter func
    @name.deleter
    def name(self):
        raise AttributeError("aaaa")


class SubPerson(Person):
    @property
    def name(self):
        print('ggg')
        return super().name

    @name.setter
    def name(self, value):
        print('sssss', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('ddddd')
        super(SubPerson, SubPerson).name.__delete__(self)


class SubPerson(Person):
    @Person.getter
    def name(self):
        print('gg')
        return super().name

s = SubPerson('Guido')
s.name

s.name = 'Larry'
s.name

s.name = 42


class String:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError('eeee')
        instance.__dict__[self.name] = value


class Person:
    name = String('name')
    def __init__(self, name):
        self.name = name

class SubPerson(Person):
    @property
    def name(self):
        print('gggg')
        return super().name

    @name.setter
    def name(self, value):
        print('ssss', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('ddddd')
        super(SubPerson, SubPerson).name.__delete__(self)


class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

#8.9 새로운 클래스나 인스턴스 속성 만들기

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
    def __init__(self,x,y):
        self.x = x
        self.y = y


## 8.10 게으른 계산을 하는 프로퍼티 사용

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
print(c.radius)
print(c.area)


# 8.11 자료 구조 초기화 단순화하기

class Structure:
    _fields = []
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))


        for name,value in zip(self._fields,args):
            setattr(self,name,value)


if __name__=='__main__':
    class Stock(Structure):
        _fields = ['name','shares','price']

    class Point(Structure):
        _fields = ['x','y']

    class Circle(Structure):
        _fields = ['rrrr']
        def area(self):
            return math.pi * self.radius ** 2

s = Stock('ACME',50,91.1)
p = Point(2,3)
c = Circle(4.5)
s2 = Stock('ACME',50)


class Structure:
    _fields = []
    def __init__(self,*args,**kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        for name, value in zip(self._fields,args):
            setattr(self,name,value)

        for name in self._fields[len(args)]:
            setattr(self,name,kwargs.pop(name))

        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))


if __name__=='__main__':
    class Stock(Structure):
        _fields = ['name','shares','price']

    s1 = Stock('ACME',50,91.1)
    s2 = Stock('ACME',50,price=91.1)
    s3 = Stock('ACME',shares=50,price=91.1)


class Structure:
    _fields = []
    def __init__(self,*args,**kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))


        for name,value in zip(self._fields,args):
            setattr(self,name,value)

        extra_args = kwargs.keys() - self._fields
        for name in extra_args:
            setattr(self,name,kwargs.pop(name))
        if kwargs:
            raise TypeError('Duplicate values for {}'.format(','.join(kwargs)))

if __name__=='__main__':
    class Stock(Structure):
        _fields = ['name','shares','price']

    s1 = Stock('ACME',50,91.1)
    s2 = Stock('ACME',50,91.1,date='8/2/2012')