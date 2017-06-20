#데이터 혹은 타입 시스템 구현
#문제
#여러 종류의 자료 구조를 정의하고 싶다. 이때 특정 값에 제약을 걸어 원하는 속성이 할당 되도록 하고 싶다.
#해결
#이번 문제의 경우, 기본적으로 특정 인스턴스 속성의 값을 설정할 때 확인을 하는 동작을 구현해야함.
#이렇게 하려면 속성을 설정하는 부분을 속성하나단위로 커스터마이즈 해야하고, 디스크립터로 해결 가능하다.
#다음 코드는 디스크립터로 시스템 타입과 값 확인 프레임워크를 구현하는 방법을 보여준다.
#베이스 클래스 디스크립터로 값 설정
class Descriptor:
    def __init__(self,name=None,**opts):
        self.name=name
        for key,value in opts.items():
            setattr(self,key,value)
        def __set__(self,instance,value):
            instance.__dict__[self.name]=value

#타입을 강제하기 위한 디스크립터
class Typed(Descriptor):
    expected_type=type(None)

    def __set__(self,instance,value):
        if not isinstance(value,self.expected_type):
            raise TypeError('Expected',+str(self.expected_type))
        super().__set__(instance,value)
#값을 강제하기 위한 디스크립터
class Unsigned(Descriptor):
    def __set__(self,instance,value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super().__set__(instance,value)

class MaxSized(Descriptor):
    def __init__(self,name=None,**opts):
        if 'size' not in opts:
            raise TypeError
        super().__init__(name,**opts)
    def __set__(self,instance,value):
        if len(value) >= self.size:
            raise TypeError
        super().__set__(instance,value)
#앞에 나온 클래스는 데이터 모델이나 타입 시스템을 만들 때 기반으로 사용하는 빌딩 블록으로 봐야 한다. 이제 서로 다른 데이터를 구현하는 코드를 보자.
class Integer(Typed):
    expected_type = int

class UnsignedInteger(Integer,Unsigned):
    pass
class Float(Typed):
    expected_type = float
class UnsignedFloat(Float,Unsigned):
    pass
class String(Typed):
    expected_type = str
class SizedString(String,MaxSized):
    pass

#타입 객체를 사용해서 다음과 같은 클래스를 정의할 수 있다.
class Stock:
    #제약 명시
    name = SizedString('name',size=8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')
    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price
#이제 값을 할 당 할때 주어진 제약으로 검증이 이루어진다.
s= Stock('ACME',50,91.1)
s.name
s.shares=75
s.shares=-10
#클래스의 제약 스펙을 단순화하는 몇가지 기술이 있다. 클래스 데코레이터
#제약을 위한 클래스 데코레이터
def check_attributes(**kwargs):
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value,Descriptor):
                value.name=key
                setattr(cls,key,value(key)  )
            else:
                setattr(cls,key,value(key))
            return cls
        return decorate
#예제
@check_attributes(name=SizedString(size=8),shares=UnsignedInteger,price=UnsignedFloat)
class Stock:
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
#또 다른 방식으로 메타 클래스가 있다.
#확인을 위한 메타클래스
class checkedmeta(type):
    def __new__(cls,clsname,bases,methods):
        #디스크립터에 속성이름 붙이기
        for key, value in methods.items():
            if isinstance(value,Descriptor):
                value.name=key
        return type.__new__(cls,clsname,bases,methods)
#예제
class Stock(metaclass=checkedmeta):
    name = SizedString(size=8)
    shares = UnsignedInteger()
    price = UnsignedFloat()
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
#토론
#이번 레시피에서는 디스크립터, 믹스인 클래스 super활용 클래스 데코레이터 메타클래스등 고급 기술을 다루었다.
#주목해야할점
#1) descriptor 베이스 클래스에서 __set__() 메소드는 있는데 __get__()이 없다는 것을 발견한 것이다. 디스크립터가 인스턴스 딕셔너리에서 동일한 이름의 값을 추출하는 것 이외에 다른 동작을 하지 않는다면
#__get__을 정의할 필요가 없다. 사실 __get__을 정의하면 오히려 실행속도가 느려짐. 따라서 이 레시피는 set구현에만 초점
#여러 디스크립터 클래스의 전체적인 디자인은 믹스인 클래스에 기반하고 있다. 예를 들어 unsigned와 maxsized 클래스는 typed에서 상속 받은 다른 디스크립터 클래스와 함께 사용하도록 디자인했다.
#특정 데이터 타입을 처리하려면 다중 상속을 해야하낟.
#또한 디스크립터의 모든 초기화 메소드는 키워드 매개변수 **opts를 포함해서 동일한 시그니처를 가지도록 프로그램되어 있다는 점을 알 수 있다.
#maxsized 클래스는 opts 에서 요청한 속성을 차지만 이를 설정하는 디스크립터 베이스 클래스에 전달한다. 이런 클래스를 작성할 때 주의해야 할 점은,
#클래스들이 어떻게 묶일지 혹은 어떤 super()가 호출될지 알 수 없다는 것이다. 따라서 어떠한 조합으로도 잘 동작하도록 구현해야 한다.
#Integer,Float,String과 같은 타입 클래스 정의로 부터 클래스 변수로 구현을 커스터마이징하는 유용한 기술을 볼 수 있다.

#클래스 데코레이터와 메타클래스 코드는 단순히 클래스 딕셔너리에서 디스크립터를 찾는다. 디스크립터를 찾으면 키 값에 기반한 이름을 채워 넣는다.
#앞에 나온 모든 방식 중에 클래스 데코레이터 방식이 가장 유연하고 안전하다. 우선 메타 클래스와 같은 고급 기술에 의존하지 않는다. 그리고 데코레이션은 원할 때면 클래스 정의에 쉽게 추가하거나
#제거할 수 있다. 예를 들어 데코레이터에서는 원할 때면 클래스 정의에 쉽게 추가하거나 제거할 수 있다.

class Descriptor:
    def __init__(self,name=None,**opts):
        self.name=name
        for key,value in opts.items():
            setattr(self,key,value)
        def __set__(self,instance,value):
            instance.__dict__[self.name]=value
class Typed(expected_type,cls=None):
    if cls is None:
        return lambda cls : Typed(expected_type,cls)
    super_set = cls.__set__:
    def __set__(self,instance,value):
        if not isinstance(value,self.expected_type):
            raise TypeError('Expected',+str(self.expected_type))
        super().__set__(instance,value)
        return cls
#언사인드값에 데코레이터 ㅏㅅ용
def Unsigned(cls):
    super._set=cls.__set__
    def __set__(self,instance,value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super._set(self,instance,value)
    cls.__set__=__set__
    return cls

#크기 있는 값에 데코레이터 사용
def MaxSized(cls):
    super_init=cls.__init__
    def __init__(self,name=None,**opts):
        if 'size' not in opts:
            raise TypeError
        super_init(self,name,opts)
    cls.__init__ = __init__

    super_set = cls.__set__
    def __set__(self,instance,value):
        if len(value) >= self.size:
            raise ValueError
        super_set(self,instance,value)
    cls.__set__=__set__
    return cls

#특별 디스크립터
@Typed(int)
class Integer(Descriptor):
    pass
@Unsigned
class UnsignedInteger(Integer):
    pass
@Typed(float)
class Float(Float):
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
#이번 코드에서 정의한 클래스는 이전 것과 완전히 동일하게 동작하고 오히려 실행속도가 훨씬 빠르다.