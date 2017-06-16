            # 8.6 관리 속성 만들기

# 문제: 인스턴스 속성을 얻거나 설정할 때 추가적인 처리(타입 체크, 검증등)를 하고 싶다.

# 해결 방안: 프로퍼티로 정의

class Person:
    def __init__(self, first_name):
        self.first_name = first_name
        
    #게터 함수
    @property
    def first_name(self):
        return self._first_name
    
    #세터 함수
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value,str):
            raise TypeError("Expected a string")
        self._first_name = value
        
    #딜리터 함수(옵션)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")
        
    
a = Person('Guido')
a.first_name #게터 호출
# (실행결과) 'Guido'
a.first_name=42 #세터 호출
#실행이 안됨...

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
        
    # 딜리터 함수(옵션)
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")
        
    # 기존 게터/세터 메소드로 프로퍼티 만들기
    name = property(get_first_name, set_first_name, del_first_name)
    
    
            # 8.7 부모 클래스의 메소드 호출
            
#문제 : 오버라이드된 서브클래스 메소드가 아닌 부모 클래스에 있는 메소드를 호출하고 싶다

#해결방법: super() 함수 사용

class A:
    def spam(self):
        print('A.spam')
        
class B(A):
    def spam(self):
        print('B.spam')
        super().spam()      # 부모의 spam() 호출
        
class A:
    def __init__(self):
        self.x = 0
        
class B:
    def __init__(self):
        super().__init__()
        self.y = 1
        
class Proxy:
    def __init__(self, obj):
        self._obj =obj
        
    # 내부 obj를 위해 델리게이트 속성 찾기
    def __getattr__(self, name):
        return getattr(self._obj, name)
    
    # 델리게이트(delegate) 속성 할당
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value) # 원본 __setattr__ 호출
        else:
            setattr(self._obj, name, value)
            
            
            # 8.8 서브 클래스에서 프로퍼티 확장

#문제: 서브클래스에서 부모클래스에 정의한 프로퍼티 기능을 확장하고 싶다..

class Person:
    def __init__(self, name):
        self.name = name
        
        #게터함수
        @property
        def name(self):
            return self._name
        
        # 세터 함수
        @name.setter
        def name(self, value):
            if not isintance(value, str):
                raise TypeError('Expected a string')
            self._name = value
            
        # 딜리터 함수
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
        print('setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)
        
    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)
        
        
s = SubPerson('Guido')
s.name
# 실행이 안됨..........
s.name = 'Larry'
s.name = 42

class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('Getting name')
        return super().name
    
# 세터 하나만 확장하려면    
class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)
          


            #8.9 새로운 클래스나 인스턴스 속성 만들기

#문제 새로운 종류의 인스턴스 속성을 만들고 싶다

#해결방법: 디스크립터 클래스 형태로 정의해야한다

#타입을 확인하는 정수형 디스크립터 속성

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
                        
    def __delete__(self, instacne):
        del instance.__dict__[self.name]
        
class Point:
    x = Integer('x')
    y = Integer('y')
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
p = Point(2,3)
p.x                 # Point.x.__get__(p,Point) 호출
# 실행결과 2

p.y = 5             # Point.y.__set__(p, 5) 호출
p.x =2.3            # Point.x.__set__(p, 2.3) 호출

# 실행결과 
'''
raise TypeError('Expected an int')
TypeError: Expected an int
'''



            #8.10 게으른 계산을 하는 프로퍼티 사용

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
# 실행결과 4.0
c.area
# 실행결과 
'''Computing area   <- 한번씩만 나타남
50.26548245743669'''

c.area
# 실행결과 50.26548245743669

c.perimeter
# 실행결과 
'''Computing perimeter  <- 한번씩만 나타남
25.132741228718345'''

c.perimeter
# 실행결과  25.132741228718345



            #8.11 자료 구조 초기화 단순화하기

#문제 : __init__() 함수를 작성하기 지겨울떄

class Structure:
    #예상되는 필드를 명시하는 클래스 변수
    _fields= []
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
                return math.pi * self.radius **2
            
s = Stock('ACME', 50, 91.1)
p= Point(2,3)
c=Circle(4.5)
s2= Stock('ACME',50)            
# 실행결과
''' raise TypeError('Expected {} arguments'.format(len(self._fields)))
TypeError: Expected 3 arguments '''


class Structure:
    _fields=[]
    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
            
        # 모든 위치 매개변수 설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
            
        # 남아 있는 키워드 매개변수 설정
        for anme in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))
            
        # 남아 있는 기타 매개변수가 없는지 확인
        if kwargs:
            raise TypeError('Invalid argument(s): {}'.formant(','.join(kwargs)))
            
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']
        
    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, price=91.1)
    s3 = Stock('ACME', shares=50, preice=91.1)
    

class Structure:
    #예상되는 필드를 명시하는 클래스 변수
    _fields=[]
    def __init__(self, *args, **kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
    
    # 속성 설정
    for name, value in zip(self._fields, args):
        setattr(self, name, value)
        
    # 추가적인 매개변수 설정
    extra_args = kwargs.key() - self._fields
    for name in extra_args:
        setattr(self, name, kwargs.pop(name))
        
    if kwargs:
        raise TypeError('Duplicate values for {}'.format(','.join(kwargs)))
        
# 사용 예
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']
        
s1 = Stock('ACME', 50, 91.1)
s2 = Stock('ACME', 50, 91.1, data='8/2/2012')











