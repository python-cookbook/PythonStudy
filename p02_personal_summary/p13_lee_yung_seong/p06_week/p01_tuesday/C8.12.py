#인터페이스 추상 베이스 클래스 정의
#문제
#인터페이스나 추상 베이스 클래스 역할을 하는 클래스를 정의하고 싶다. 그리고 이 클래스는 타입 확인을 하고 특정 메소드가 서브 클래스에 구현되었는지 보장한다.
#해결
#추상 베이스 클래스를 정의하려면,,
from abc import ABCMeta, abstractmethod
class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self,maxbytes=-1):
        pass
    @abstractmethod
    def write(self,data):
        pass

#추상 베이스 클래스의 주요 기능은 직접 인스턴스화 할 수 없다는 점이다. 예를 들어 다음 코드를 시도하면 에러가 발생한다.
a=IStream
#추상 베이스 클래스는 요구한 메소드를 구현하는 다른 클래스의 베잇 ㅡ클래스로 사용해야 한다.
class SocketStream(IStream):
    def read(self,maxbytes=-1):
        pass
    def write(self,data):
        pass

#추상 베이스 클래스는 특정 프로그래밍 인터페이스를 강요하고 싶을 때 주로 사용.
#예를 들어 Istream 베이스 클래스는 데이터를 읽거나 쓰는 인터페이스에 대한 상위 레벨 스펙으로 볼 수 있다. 인터페이스를 명시적으로 확인하는 코드는 다음과 같이 작성한다.
#이런 타입 확인 코드는 서브 클래싱과 추상 베이스 클래스(ABC)에서만 동작할 것 같지만, ABC는 다른 클래스가 특정 인터페이스를 구현했는지 확인하도록 허용한다.
import io
#내장 io 클래스를 우리의 인터페이스를 지원하도록 등록
IStream.register(io.IOBase)
#일반파일을 엵고 타입확인
f = open('foo.txt')
isinstance(f,IStream)
#@abstractmethod를 스태틱 메소드, 클래스 메소드, 프로퍼티에도 적용할 수도 있다. 단지 함수 정의 직전에 @abstractmethod를 적용해야 한다는 점만 기억하자.
from abc import ABCMeta, abstractmethod
class A(metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self):
        pass
    @name.setter
    @abstractmethod
    def name(self,value):
        pass
    @classmethod
    @abstractmethod
    def method1(cls):
        pass
    @staticmethod
    @abstractmethod
    def method2():
        pass
#토론
#파이썬 표준 라이브러리에서 추상 베이스 클래스를 사용하는 경우가 많다. collections 모듈은 콘테이너 이터레이터 등에 abc를 정의하고 있고
#numbers 라이브러리는 숫자 관련 객체등이 abc를 정의하며 io라이브러리는 io 처리에 abc를 정의한다.
#추상 베이스 클래스를 더 일반적인 타입 확인에 사용할 수 있다.
import collections
#x가 시퀀스이닞 화깅ㄴ
if isinstance(x,collections.Sequence):
    '''
    
    '''
#x가 순환 가능한지 확인
if isinstance(x,collections.Iterable):
    ''
    ''
#x에 크기가 있는지
if isinstance(x,collections.Sized):
    '''
    '''
#x가 매핑인지
if isinstance(x,collections.Mapping):
    '''
    '''
#이 책을 쓰고 있는 시점에 특정 라이브러리 모듈은 독자의 예상대로 abbc를 활용하지 않음
from decimal import Decimal
import numbers
x = Decimal('3.4')
isinstance(x,numbers.Real)
#3.4는 엄밀히 따지면 실수이지만, 의도하지 않은 부동 소수점 숫자와 소수이ㅡ 혼합 사용을 방지하기 위해 false를 반환.
#abc에 타입확인 기능이 있지만 남용하면 안좋음.