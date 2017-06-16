# 8.6 관리 속성 만들기
# 문제
# 인스턴스 속성을 얻거나 설정할 때 추가적인 처리(타입 체크, 검증 등)를 하고 싶다.
# 해결
# 속성에 대한 접근을 조절하고 싶으면 "프로퍼티"로 정의하면 된다.
# 예를 들어 다음 코드는 속성에 간단한 타입 체크를 추가하는 프로퍼티를 정의한다.
class Person:
    def __init__(self,first_name):
        self.first_name = first_name
    # 게터함수
    @property
    def first_name(self):
        return self._first_name
    @first_name.setter
    def first_name(self,value):
        if not isinstance(value,str):
            raise TypeError('Expected a string')
        self._first_name = value
    # 딜리터 함수(옵션)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")
# 앞의 코드에서 관련 메소드가 세 개 있는데, 모두 같은 이름을 가져야 한다.
# 첫번째 메소드는 게터함수로 first_name을 프로퍼티로 만든다.
# 다른 두 메소드는 추가적으로 세터와 딜리터 함수를 frist_name 프로퍼티에 추가한다
# 여기서 @first_name.setter와 @first_name.deleter 데코레이터는 @property를 사용해서 first_name을 만들어 놓지 않으면
# 정의되지 않는 점이 중요하다
# 프로퍼티의 중요 기능으로 일반적인 속성으로 보이지 않는다는 점이 있지만, 여기에 접근하면 자동으로 게터,세터,딜리터 메소드가 자동생성된다
a = Person('Guido')
a.first_name #  'Guido' 출력
a.first_name = 42
# Traceback (most recent call last):
#   File "<input>", line 1, in <module>
#   File "<input>", line 11, in first_name
# TypeError: Expected a string
del a.frist_name
# Traceback (most recent call last):
#   File "<input>", line 1, in <module>
# AttributeError: frist_name
# 프로퍼티를 구현할 때 기반 데이터가 있다면 여전히 어딘가에 저장해야 한다
# 따라서 게터,세터 메소드에서 _first_name 속성을 직접 다루는 것을 볼 수 있는데,
# 여기서 실제 데이터가 들어간다
class Person:
    def __init__(self,first_name):
        self.set_first_name(first_name)
    #게터 함수
    def get_first_name(self):
        return self.get_first_name
    #세터 함수
    def set_first_name(self,value):
        if not isinstance(value,str):
            raise TypeError('Expected a string')
        self._first_name = value
    #딜리터 함수(옵션)
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")
    #기존 세터/게터 메소드로 프로퍼티 만들기
    name = property(get_first_name,set_first_name,del_first_name)
# 토론
# 사실 프로퍼티 속성은 함께 묶여 있는 메소드 컬렉션이다.
# 프로퍼티가 있는 클래스를 조사해보면 프로퍼티 자체의 fget,fset,fdel 속성에서 로우 메소드를 찾을 수 있다
# 일반적으로 fget 이나 fset 을 직접 호출하지는 않고, 프로퍼티에 접근할 때 자동으로 실행된다.
# java 등에 익숙한 프로그래머는 클래스 속성에 접근할 때 무조건 게터,세터를 사용해야 한다고 생각하고 다음과 같은 코드를 작성한다
class Person:
    def __init__(self,first_name):
        self.first_name=first_name
    @property
    def first_name(self):
        return self._first_name
    @first_name.setter
    def first_name(self,value):
        self._frist_name= value
# 앞에 코드는 불필요하게 장황하고 이해하기 어렵다
# 그리고 프로그램의 실행 속도도 떨어진다.
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
# 앞에 나온 프로퍼티를 사용하면 radius, area, perimeter 가 마치 속성인 것처럼 접근할 수 있다
# 속성과 메소드 호출을 복합적으로 사용하는 것과 대조적이다
c = Circle(4.0)
c.radius # 4.0 출력
c.area # 50.265482 출력
c.perimeter # 25.132741 출력
# 프로퍼티로 우아한 프로그래밍 인터페이스를 얻을 수 있지만, 게터와 세터 함수를 직접 사용하는 것도 가능하다
p = Person('Guido')
p.get_first_name()
p.set_first_name('Larry')
# 시스템 프로그램과 같은 거대 구조에 파이썬 코드를 통합할 때 이럴 필요성도 있다
class Person:
    def __init__(self,first_name,last_name):
        self.first_name = first_name
        self.last_name=last_name
    @property
    def first_name(self):
        return self._first_name
    @first_name.setter
    def first_name(self,value):
        if not isinstance(value,str):
            raise TypeError('Expected a string')
        self._first_name = value
    # 이름이 다른 프로퍼티 코드의 반복 (좋지 않다!)
    @property
    def last_name(self):
        return self._last_name
    @last_name.setter
    def last_name(self,value):
        if not isinstance(value,str):
            raise TypeError('Expected a string')
        self._last_name=value
# 코드를 반복하면 보기 좋지 않고 에러가 발생하기도 쉽다

# 8.7 부모 클래스의 메소드 호출
# 문제
# 오버라이드된 서브클래스 메소드가 아닌 부모 클래스에 잇는 메소드를 호출하고 싶다
# 해결
# 부모(혹은 슈퍼클래스)의 메소드를 호출하려면 super() 함수를 사용한다
class A:
    def spam(self):
        print('A.spam')
class B(A):
    def spam(self):
        print('B.spam')
        super().spam()
# super() 는 일반적으로 __init__() 메소드에서 부모를 제대로 초기화하기 위해 사용한다
class A:
    def __init__(self):
        self.x = 0
class B:
    def __init__(self):
        super().__init__()
        self.y = 1
# 특별 메소드를 오버라이드한 코드에서 super()를 사용하기도 한다
class Proxy:
    def __init__(self,obj):
        self._obj = obj
    #내부 obj를 위해 델리게이트 속성 찾기
    def __getattr__(self, name):
        return getattr(self._obj,name)
    #델리게이트 속성 할당
    def __setattr__(self, name,value):
        if name.startswith('_'):
            super().__setattr__(name,value)
        else:
            setattr(self._obj,name,value)
# 이 코드에서, __setattr__() 구현에 이름확인이 들어 있다
# 만약 이름이 밑줄로 시작하면 super() 를 사용해서 __setattr__()의 원래의 구현을 호출한다
# 그렇지 않다면 내부 객체인 self._obj를 부른다
# 토론
# super() 함수를 올바르게 사용하기는 무척 어렵다. 때때로 부모 클래스 메소드를 직접 호출하기 위해 다음과 같이 작성한 코드를 볼 수 있다
class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')
# 앞에 나오는 코드가 대부분의 경우 동작하기는 하지만 다중 상속과 같은 상황에서 문제가 발생하기도 한다
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
# 이 코드를 실행하면 Base.__init__() 메소드가 두번 호출된다
c = C() # Base -> A -> Base -> B -> C 순으로 출력
Base.__init__
A.__init__
Base.__init__
# Base.__init__() 을 두번 호출하는 것이 문제가 없을 수도 있지만, 항상 그렇지만은 않다.
# 하지만 super() 를 사용하여 코드를 수정한다면 올바르게 동작한다
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
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')
# 자식 클래스를 부모보다 먼저 확인한다
# 부모 클래스가 둘 이상이면 리스팅한 순서대로 확인한다
# 유효한 후보가 두 가지 있으면, 첫 번째 부모 클래스부터 선택한다
# super() 함수를 사용할 때, 파이썬은 MRO의 다음 클래스에서 검색을 시작한다.
# 재정의한 모든 메소드가 모두 super()를 사용하고 한 번만 호출하지만, 시스템은 MRO 리스트 전체에 동작하고
# 모든 메소드는 한번만 호출된다

# 8.8 서브클래스에서 프로퍼티 확장
# 문제
# 서브클래스에서 부모 클래스에 정의한 프로퍼티의 기능을 확장하고 싶다
# 해결
# 프로퍼티를 정의하는 다음 코드를 보자
class Person:
    def __init__(self,name):
        self.name = name
    #게터함수
    @property
    def name(self):
        return self._name
    #세터함수
    @name.setter
    def name(self,value):
        if not isinstance(value,str):
            raise TypeError('Expected a string')
        self._name = value
    #딜리터함수
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")
# 다음 코드는 Person을 상속 받아 name 프로퍼티에 새로운 기능을 넣어 클래스를 확장한다
class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name
    @name.setter
    def name(self,value):
        print('Setting name to',value)
        super(SubPerson,SubPerson).name.__set__(self,value)
    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson,SubPerson).name.__delete__(self)
# 다음은 새로운 클래스를 사용하는 에제이다
s = SubPerson('Guido') # Setting name to Guido 출력
s.name # Getting name 'Guido' 출력
# 프로퍼티의 메소드 하나를 확장하고 싶으면 다음과 같은 코드를 사용한다
class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('Getting name')
        return super().name
# 혹은 세터 하나만 확장하려면 다음과 같이 한다
class Subperson(Person):
    @Person.name.setter
    def name(self,value):
        print('Setting name to',value)
        super(SubPerson,SubPerson).name.__set__(self,value)
# 토론
# 서브클래스의 프로퍼티를 확장하면 프로퍼티가 하나의 메소드가 아닌 게터,세터,딜리터 메소드의 컬렉션으로 정의되었다는 사실로 인해
# 자잘한 문제가 발생한다
# 따라서 프로퍼티를 확장할 때 모든 메소드를 다시 정의할지, 메소드 하나만 다시 정의할지 결정해야 한다
# 세터의 기존 구현으로 델리게이트하기 위해서, 컨트롤은 기존에 구현한 name 프로퍼티의 __set__() 메소드로 전달해야 한다
# 이 메소드에 도달하기 위한 유일한 방법은 인스턴스 변수가 아닌 클래스 변수로 접근하는 것이다.
class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name
    s = SubPerson('Guido') # 오류가 뜬다
# 코드를 해결책에 나왔던 처럼 수정해야 한다
class SubPerson(Person):
    @Person.getter
    def name(self):
        print('Getting name')
        return super().name
# 이렇게 하면, 기존에 정의한 모든 프로퍼티 메소드가 복사되고 게터함수가 치환된다.
s = SubPerson('Guido')
s.name # Getting name Guido 출력
# 어떤 베이스 클래스가 프로퍼티를 정의했는지 모른다면 모든 프로퍼티 메소드를 재정의하고 super()로 구현하는 방식을 사용해야 한다
# 디스크립터
class String:
    def __init__(self,name):
        self.name = name
    def __get__(self,instance,cls):
        if instance is None:
            return self
        return instance.__dict__[self.name]
    def __set__(self,instance,value):
        if not isinstance(value,str):
            raise TypeError('Expected a string')
        instance.__dict__[self.name] = value
# 디스크립터를 가진 클래스
class Person:
    name = String('name')
    def __init__(self,name):
        self.name = name
# 디스크립터에 프로퍼티를 넣어 확장
class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name
    @name.setter
    def name(self,value):
        print('Setting name to',value)
        super(SubPerson,SubPerson).name.__set__(self,value)
    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson,SubPerson).name.__delete__(self)

# 8.9 새로운 클래스나 인스턴스 속성 만들기
# 문제
# 타입 확인 등과 같이 추가적 기능을 가진 새로운 종류의 인스턴스 속성을 만들고 싶다
# 해결
# 완전히 새로운 종류의 인스턴스 속성을 만들려면, 그 기능을 디스크립터 클래스 형태로 정의해야 한다
# 타입을 확인하는 정수형 디스크립터 속성
class Integer:
    def __init__(self,name):
        self.name = name
    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]
    def __set__(self,instance,value):
        if not isinstance(value,int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name]=value
    def __delete__(self, instance):
        del instance.__dict__[self.name]
# 디스크리터는 세 가지 중요한 속성 접근 명령(get,set,delete)을 특별 메소드 __get__(),__set__(),__delete()__ 형식으로 구현한 클래스이다
# 디스크립터를 사용하려면 디스크립터의 인스턴스는 클래스 정의에 클래스 변수로 들어가야 한다
class Point:
    x = Integer('x')
    y = Integer('y')
    def __init__(self,x,y):
        self.x = x
        self.y = y
# 이렇게 할 때, 디스크립터에 대한 모든 접근은 __get__(),__set__(),__delete__() 메소드를 사용한다
p = Point(2,3)
p.x # 2 출력
p.y # 3 출력
# 토론
# 디스크립터는 파이썬 클래스 기능에 __slots__,@classmethod,@staticmethod,@property와 같이 멋진 도구를 제공한다
# 디스크립터를 정의하면 get,set,delete 와 같이 중요한 인스턴스 연산을 아주 하위 레벨에서 얻고
# 어떻게 동작할지도 입맛대로 바꿀 수 있다.
# 따라서 고급 라이브러리와 프레임워크를 작성하는 프로그래머에게 매우 중요한 도구가 된다.
# 디스크립터에 대해 한 가지 헷갈리는 부분은 인스턴스 기반이 아닌 클래스 레벨에서만 정의가 가능하다는 것
# 동작하지 않는 예제
class Point:
    def __init__(self,x,y):
        self.x = Integer('x')
        self.y = Integer('y')
        self.x = x
        self.y = y
# 또한, __get__() 메소드를 구현하는 것도 보기보다 간단하지 않다
# 타입을 확인하는 정수형 디스크립터 구성
class Integer:
    ...
    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]
    ...
# __get__() 이 조금 복잡해 보이는 이유는 인스턴스 변수와 클래스 변수를 구분해야 하기 때문이다
# 만약 디스크립터를 클래스 변수로 접근하면 instacne 인자가 None이 된다.
p = Point(2,3)
p.x # 2 출력
Point.x # Point.x.__get__(None,Point)

# 8.10 게으른 계산을 하는 프로퍼티 사용
# 문제
# 읽기 전용 속성을 프로퍼티로 정의하고, 이 속성에 접근할 때만 계산하도록 하고 싶다.
# 하지만 한 번 접근하고 나면 이 값을 캐시해 놓고 다음번에 접속할 때는 다시 계산하지 않도록 하고 싶다
# 해결
# 게으른 속성을 효율적으로 정의하기 위해서는 다음과 같은 디스크립터를 사용한다
class lazyproperty:
    def __init__(self,func):
        self.func = func
    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance,self.func.__name__,value)
            return value
# 이 코드를 활용하기 위해서는 다음과 같이 클래스 내부에서 사용한다
import math
class Circle:
    def __init_(self,radius):
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
c.radius # 4.0 출력
c.area # Computing area 50.26548 출력
c.perimeter # Computing perimeter 25.12374 출력
# 토론
# 대개의 경우 게으르게 계산한 속성은 성능 향상을 위해 사용한다
# 예를 들어 실제로 특정값을 사용하기 전까지 계산하지 않도록 하는 것이다
# 특히, __get__() 메소드는 접근하는 속성이 인스턴스 딕셔너리에 없을 때만 실행된다
# lazyproperty 클래스는 프로퍼티 자체와 동일한 이름을 사용해서 인스턴스 __get__() 메소드에 계산한 값을 저장하는 식.
c = Circle(4.0)
# 인스턴스 변수 구하기
vars(c) # {'radius' : 4.0 } 출력
# 면적을 계산하고 추후 변수 확인
c.area # 50.26548 출력
vars(c) # {'area' : 50.26548,'radius':4.0} 출력
# 속성에 접근해도 더 이상 프로퍼티를 실행하지 않는다
# 한가지 불리한 점은 계산한 값을 생성한 후에 수정할 수있다는 것이다
c.area = 25
c.area # 25 출력
# 하지만 해결책이 있다.
def lazyproperty(func):
    name = '_lazy_'+func.__name__
    @property
    def lazy(self):
        if hasattr(self,name):
            return getattr(self,name)
        else:
            value = func(self)
            setattr(self,name,value)
            return value
    return lazy
# 이렇게 하면 값 설정이 불가능하게 된다

# 8.11 자료 구조 초기화 단순화하기
# 문제
# 자료 구조로 사용하는 클래스를 작성하고 있는데, 반복적으로 비슷한 __init__() 함수를 작성하기에 지쳐간다
# 해결
# 자료 구조의 초기화는 베이스 클래스의 __init__() 함수를 정의하는 식으로 단순화할 수 있다
import math
class Structure:
    # 예상되는 필드를 명시하는 클래스 변수
    _fields=[]
    def __init__(self,*args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
        # 속성 설정
        for name,value in zip(self._fields,args):
            setattr(self,name,value)
        # 예제 클래스 정의
        if __name__ == '__main__':
            class Stock(Structure):
                _fields = ['name','shares','price']
            class Point(Structure):
                _fields = ['x','y']
            class Circle(Structure):
                _fields = ['radius']
                def area(self):
                    return math.pi * self.radius ** 2
# 결과 클래스를 사용하면 쉽게 만들 수 있다는 것을 확인 할 수 있다
# 키워드 매개변수를 지원하기로 결정했다면 사용할 수 있는 디자인 옵션이 몇가지 있다
# 그 중 키워드 매개변수를 매핑해서 _fields 에 명시된 속성 이름에만 일치하도록 만드는 것이다
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
    s3 = Stock('ACME', shares=50, price=91.1)
# 혹은 _fields 에 명시되지 않은 구조에 추가적인 속성을 추가하는 수단으로 키워드 매개변수를 사용할 수 있다
class Structure:
    # 예상하는 필드를 명시하는 클래스 변수
    _fields = []
    def __init__(self, *args, **kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
        # 속성 설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
        # 매개변수 설정
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
# 이렇게 해도 동작은 하지만, 서브클래스 구현에 대한 가정을 하는 것이 항상 안전하지는 않다
# 이 기술의 단점 중 한 가지는 문서화와 IDE의 도움말 기능에 영향을 준다는 것이다
# 사용자가 특정 클래스에 대해 도움말을 요청하면, 요청한 인자가 일반적인 방식으로 설명되지 않는다.

# 또한 유틸리티 함수와 소위 프레임 핵 을 사용하면 인스턴스 변수를 자동으로 초기화할 수 있다
def init_fromlocal(self):
    import sys
    locs = sys._getframe(1).f_locals
    for k, v in locs.items():
        if k != 'self':
            setattr(self, k, v)
    class Stock:
        def __init__(self, name, shares, price):
            init_fromlocal(self)
# init_fromlocals() 함수는 sys._getframe() 으로 호출 중인 메소드의 지역변수를 살펴본다.
# 만약 __init__() 메소드의 첫 번째 단계로 사용하면, 지역변수는 전달 받은 인자와 동일하고
# 동일한 이름으로 속성을 설정하는데 사용할 수 있다
