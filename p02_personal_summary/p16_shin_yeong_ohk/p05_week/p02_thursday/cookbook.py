6월 16일
========================================================================================================================
#8.6 관리 속성 만들기
#인스턴스 속성을 얻거나 설정할 때 추가적인 처리(타입 체크, 검증 등)를 하고 싶을 때
#속성에 대한 접근을 조절하고 싶으면, = "프로퍼티(property)" 정의

EX1>
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
            if not isinstance(value, str):
                raise TypeError('Expected a string')
            self._first_name = value
            
        #필터링 함수(옵션)
        @first_name.deleter
        def first_name(self):
            raise AttributeError("Can't delete attribute")
#위의 코드에서 관련 메소드가 세 개 있는데, 모두 같은 이름을 가져야 한다.*
#첫번째 메소드는 게터함수로, forst_name 을 프로퍼티로 만든다.
#다른 두 메소드는 추가적으로 세터와 딜리터 함수를 first_name 프로퍼티에 추가한다.
# @fisrt_name.setter와 @first_name.deleter 데코리에터는 @property를 사용해서 first_name을 만들어 놓지 않으면 정의되지 않는다.


#프로퍼티의 중요 기능으로 일반적인 속성으로 보이지 않는다는 점이 있지만, 여기세 접근하면
#자동으로 게터, 세터, 딜리터 메소드가 자동으로 실행된다.

a = Person('Guido')    #게터 호출
a.first_name
#Guido
a.first_name = 42   #세터 호출

del a.first_name

#게터, 세터 메소드에서 _first_name 속성을 직접 다루는 것을 볼 수 있는데, 여기에 실제 데이터가 들어간다.
#__init__()에서 self._first_name 이 아닌 self.first_name을 설정하는 이유?
#프로퍼티 > 속성에 타입 체킹을 적용하는 것
#초기화할 때 확인하기 = self.first_name 설정하면, 설정 연산이 세터 메소드를 사용한다.
#self._first_name 에 접근하여 우회하는 것과 대조적으로



#이미 존재하는 get과 set 메소드로 프로펀티 정의하기
EX2>
class Person:
    def __init__(self, first_name):
        self.set_first_name(first_name)
        
    #게터 함수
    def get_first_name(self):
        return self.get_first_name()
    
    #세터 함수
    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value
        
    #딜리터 함수(옵션)
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")
    
    #기존 게터/세터 메소드로 프로퍼티 만들기
name = property(get_first_name, set_first_name, del_first_name)
========================================================================================================================







========================================================================================================================
# 8.7 부모 클래스의 메소드 호출
#오버라이드된 서브클래스 메소드가 아닌 부모 클래스에 있는 메소드를 호출하고 싶을 때,
#super() 함수
EX1>
class A:
    def spam(self):
        print('A spam')
    
class B:
    def spam(self):
        print('B spam')
        super().spam()  #부모의 spam() 호출

#super()는 일반적으로 __init__() 메소드에서 부모를 제대로 초기화하기 위해 사용한다.

EX2>
class A:
    def __init__(self):
        self.x = 0
    
class B(A):
    def __init__(self):
        super().__init__()
        self.y = 1
        

#그리고 파이썬의 특별 메소드를 오버라이드한 코드에서 super()를 사용하기도 한다.
EX3>
class Proxy:
    def __init__(self, obj):
        self._obj = obj
    
    #내부 obj를 위해 델리게이트 속성 찾기
    def __getattr__(self, name):
        return getattr(self._obj, name)
    
    # 델리게이트 속성 할당
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value) # 원본 __setattr__ 호출
        else:
            setattr(self._obj, name, value)
            
##이 코드에서, __setattr__() 구현에 이름 확인이 들어 있다.
##만약 이름이 밑줄로 시작하면 super()를 사용해서 __setattr__()의 원래의 구현을 호출한다.
##그렇지 않다면 내부 객체인 self.__obj를 부른다.
##명시적으로 클래스를 표시하지 않아도 super()가 동작한다.
========================================================================================================================

                           
                           
                           
                           
                           
                           
========================================================================================================================
#8.8 서브클래스에서 프로퍼티 확장
#서브클래스에서, 부모 클래스에 정의한 프로퍼티의 기능을 확장하고 싶을 때,
# 프로퍼티를 정의하는 코드
EX1>
class Person:
    def __init__(self, name):
        self.name = name
    
    #게터 함수
    @property
    def name(self):
        return self._name
    
    #세터 함수
    @name.setter
    def name(self, value):
        if not isinstance(values, str):
            raise TypeError('Expected a string')
        self._name = value
        
    #딜리터 함수
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")
       
        
        
EX2>
#Person을 상속 받아 name 프로퍼티에 새로운 기능을 넣어 클래스를 확장하는 코드
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
    
#새로운 클래스를 사용하는 예제
s = SubPerson('Guido')
#name 'values' is not defined
s.name
#name 's' is not defined
s.name = 'Larry'
#name 's' is not defined
s.name = 42
#name 's' is not defined



EX3>
#프로퍼티의 메소드 하나를 확장하고 싶을 때,
class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('Getting name')
        return super().name   
    
#혹은 세터 하나만 확장하려면,
class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)     
========================================================================================================================      
        





========================================================================================================================
#8.9 새로운 클래스나 인스턴스 속성 만들기
#타입 확인 등과 같이 추가적 기능을 가진 새로운 종류의 인스턴스 속성을 만들고 싶을 때,
#완전히 새로운 종류의 인스턴스 속성을 만들려면,
#그 기능을 디스크립터 클래스 형태로 정의해야 한다.

EX1>
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
                         
    def __delete__(self, instance):
        del instance.__dict__[self.name]

##디스크립터는 세 가지 중욯나 속성 접근 명령(get, set, delete)을 특별 메소드 __get__(),
##__set__(), __delete__() 형식으로 구현한 클래스
##이 메소드는 인스턴스를 입력으로 받는다.
##그리고 인스턴스의 기반 딕셔너리는 속성으로 만들어진다.
##디스크립터를 사용하려면, 디스크립터의 인스턴스는 클래스 정의에 클래스 변수로 들어가야 한다.

EX2>
class Point:
    x = Integer('x')
    y = Integer('y')
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
#이렇게 할 때, 디스크립터에 대한 모든 접근 (x 또는 y)은 __get__(), __set__(), __delete__() 메소드를 사용
p = Point(2, 3)
p.x     #Point.x.__get__(p,Point) 호출
#NameError: name 'Integer' is not defined
p.y = 5      #Point.x.__get__(p,5) 호출
p.x = 2.3    #Point.x.__get__(p,2.3) 호출
#NameError: name 'Integer' is not defined

##입력으로, 디스크립터의 모든 메소드는 가공 중인 인스턴스를 받는다.
##요청받은 작업을 수행하기 위해서, 인스턴스 딕셔너리(__dict__ 속성) 역시 적절히 처리된다.
##디스크립터의 self.name 속성은 실제 데이터를 인스턴스 딕셔너리에 저장할 때 사용하는 딕셔너리 키를 가지고 있다.
========================================================================================================================







========================================================================================================================
#8.10 게으른 계산을 하는 프로퍼티 사용
#읽기 전용 속성을 프로퍼티로 정의하고, 이 속성에 접근할 때만 계산하도록 하고 싶다.
#하지만 한 번 접근하고 나면 이 값을 캐시해 놓고 다음 번에 접근할 때에는 다시 계산하지 않도록 하고 싶을 때,

EX1>
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
        
#이 코드를 활용하기 위해서는 다음과 같이 클래스 내부에서 사용하기
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

#코드 사용 예
c = Circle(4.0)
c.radius
#4.0
c.area
#Computing area
#50.26548245743669
c.area
#50.26548245743669
c.perimeter
#Computing perimeter
#25.132741228718345
c.perimeter
#25.132741228718345
#"Computer area" 와 "Computing perimeter" 메시지가 한 번씩만 나타난다!
========================================================================================================================






========================================================================================================================
#8.11 자료 구조 초기화 단순화하기
#자료 구조로 사용하는 클래스를 작성하고 있는데, 반복적으로 비슷한 __init__()함수를 작성하기 지칠 때
#자료 구조의 초기화는 베이스 클래스의 __init__() 함수를 정의하는 식으로 단순화할 수 있다.

EX1>
class Structure:
# 예상되는 필드를 명시하는 클래스 변수
    _fields= []
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
            
        # 속성 설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
            
        #예제 클래스 정의
        if __name__ == '__main__':
            class Stock(Structure):
                _fields = ['name', 'shares', 'price']
                
            class Point(Structure):
                _fields = ['x','y']
           
            class Circle(Structure):
                _fields = ['radius']
                def area(self):
                    return math.pi * self.radius ** 2
                
#결과 클래스를 사용하면, 쉽게 만들 수 있다는 것을 확인할 수 있다.
s = Stock('ACME', 50, 91.1)
p = Point(2, 3)
c = Circle(4.5)
s2 = Stock('ACME', 50)
#Traceback (most recent call last):
#  File "<ipython-input-18-f763706fab91>", line 1, in <module>
 #   s = Stock('ACME', 50, 91.1)
#NameError: name 'Stock' is not defined



EX2>
#키워드 매개변수를 지원하기로 결정했다면 사용할 수 있는 디자인 옵션이 몇 가지 있다.
#그 중 한 가지는 키워드 매개변수를 매핑해서 _fields에 명시된 속성 이름에만 일치하도록 만다는 것
class Structure:
    _fields= []
    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
            
        # 모든 위치 매개변수 설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
            
        #남아 있는 키워드 매개변수 설정
        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))
            
        #남아 있는 기타 매개변수가 없는지 확인
        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))
            
#사용 예
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']
        
    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, price=91.1)
    s3 = Stock('ACME', shares=50, price=91.1)
        
    

EX2_1>    
#혹은 _fields에 명시되지 않은 구조에 추가적인 속성을 추가하는 수단으로 키워드 매개변수를 사용할 수 있다.
class Structure:
    
    # 예상되는 필드를 명시하는 클래스 변수
    _fields= []
    def __init__(self, *args, **kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
            
        # 속성 설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
            
        # (있다면) 추가적인 매개변수 설정
        extra_args = kwargs.keys() - self._fields
        for name in extra_args:
            setattr(self, name, kwargs.pop(name))
        if kwargs:
            raise TypeError('Duplicate values for {}'.format(','.join(kwargs)))
            
# 사용 예
if __name__ == '__main__':
    class Stock(Structure):
    _fields = ['name', 'shares', 'price']
    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, 91.1, date='8/2/2012')
========================================================================================================================