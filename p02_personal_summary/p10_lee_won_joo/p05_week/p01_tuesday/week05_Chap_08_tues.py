"""
8.1 인스턴스의 문자열 표현식 변형

문제:
인스터스를 출력하거나 볼 때 생성되는 결과물을 좀 더 보기 좋게 바꾸고 싶다.

해결 :
인스턴스의 문자열 표현식을 바꾸려면 __str__() 와 __repr__() 메소드를 정의한다.


__repr__메소드 :  인스턴스의 코드 표현식을 반환하며
                 인스턴스를 재생성 할 때 입력하는 텍스트이다.
                 내장 repr() 함수는 인터프리터에서 값을 조사할 때와 마찬가지로
                 이 텍스트를 반환한다.
__str__메소드  :   인스터스를 문자열로 반환하고 , str() 과 print()함수가 출력하는 결과가 된다.


"""


class Pair:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)  #대체 여기 self왜? repr이라?
        # return 'Pair(%r, %r)' % (self.x, self.y))
    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)   #얘는왜..


# repr과 str 의 역할
p =Pair(3,4)
p    # Pair(3,4)    #  __repr__의 결과

print(p)   #(3,4)    # __str__() 의 결과


#서식화에서 문자열 표현식이 어떻게 다른지, 서식화 코드 !r은 기본 값으로
#__str__대신 __repr__을 사용해야 함을 가리킨다.

#실험하기

p= Pair(3,4)
print('p is {0!r}'.format(p))
#p is Pair(3, 4)
print('p is {0}'.format(p))
#p is (3, 4)




"""
repr과 str를 정의하면 디버깅과 인스턴스 출력을 간소화 한다.
ex) 단지 출력이나 인스턴스 로깅 시, 프로그래머는 인스턴스 내용에 대해 더 유용한 정보를
얻을 수 있다.

repr은 eval(repr(x)) == x와 같은 텍스트를 만드는 것이 표준이다. 
이것을 원치 않는다면 < > 사이에 텍스트를 넣는다.
"""



"""
8.2 문자열 서식화 조절

format() 함수와 문자열 메소드로 사용자가 정의한 서식화를 지원하고 싶다.


>> 문자열 서식화를 조절하고 싶을 때 클래스에
__format__() 메소드를 정의한다.

"""



_formats = {
    'ymd' : '{d.year}-{d.month}-{d.day}',
    'mdy' : '{d.month}/{d.day}/{d.year}',
    'dmy' : '{d.day}/{d.month}/{d.year}'
}

class Date:
    def __init__(self,year,month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)

#Date클래스의 인스턴스는 이제 다음과 같이 서식화를 지원한다.
d=Date(2012,12,21)
print(format(d))  #2012-12-21
print(format(d, 'mdy'))  #12/21/2012
print('The date is {:ymd}'.format(d))
print('The date is {:mdy}'.format(d))


# __format__() 메소드는 파이썬의 문자열 서식화 함수에 후크를 제공한다.
# 서식화 코드의 해석은 모두 클래스 자체에 달려있다는 점이 중요하다.
# 따라서 코드에는 거의 모든 내용이 올 수 있다.



from datetime import date
d = date(2012, 12, 21)
print(format(d)) #2012-12-21
print(format(d, '%A, %B %d, %Y'))  #Friday, December 21, 2012

print('the end is {:%d %b %Y}. Goodbye'.format(d))  #the end is 21 Dec 2012. Goodbye

#위처럼 내장 타입의 서식화에는 어느 정도 표준이 있다.
#string 모듈 문서 참고바람


"""
8.3 객체의 콘텍스트 관리 프로토콜 지원

객체가 콘텍스트 관리 프로토콜(with구문) 을 지원하게 만들고 싶다.

객체와 with 구문을 함께 사용할 수 있게 만들려면 __enter__와 __exit__메소드를
구현해야 한다.

"""


########### 네트워크 연결 제공 클래스



from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.famaily = AF_INET
        self.type = SOCK_STREAM
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.famaily, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_type, exc_val, tb):
        self.sock.close()
        self.sock = None


#이 클래스의 주요 기능은 네트워크 연결을 표현하는 것이나,
#처음에는 아무런 작업을 하지 않는다.
#연결은 with 구문에서 이루어진다. (요구에 의해)

from functools import partial

conn = LazyConnection(('www.python.org'),80)
with conn as s:
    # conn.__enter__() 실행 : >>>>연결
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() 실행 : >>>>>연결 종료



"""
콘텍스트 매니저를 작성할 때 중요한 원리는 with 구문을 사용하여 정의되 ㄴ블럭을
감싸는 코드를 작성한다는 것이다.
처음으로 with 를 만나면 __enter__() 메소드가 호출된다.
__enter__의 반환값은 as로 나타낸 변수에 위치시킨다.
그 후에 with의 내부 명령어를 실행하고 마지막으로 __exit__ 메소드로 소거 작업을 한다.

__exit__의 세가지 인자에 예외타입/값/트레이스백 이 있다.
True면 예외를 없애고, with 블록 다음의 프로그램을 계속해서 실행한다.


"""

from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.famaily = AF_INET
        self.type = SOCK_STREAM
        self.conn = []
    def __enter__(self):
        sock = socket(self.famaily, self.type)
        sock.connect(self.address)
        self.conn.append(sock)
    def __exit__(self, exc_type, exc_val, tb):
        self.conn.pop().close()

#사용 예
from functools import partial

conn12 = LazyConnection(('www.python.org'), 80)
with conn as s1:
    with conn as s2:

        # s1과 s2는 서로 독립적인 소켓이다.

# 두번쨰 lazy.. 클래스는 연결을 위한 팩토리 역할을 한다.
#내부적으로 스택을 위해 리스트를 사용했다.
#enter가 실행될때마다, 새로운 연결을 만들고 스택에 추가한다.
#exit은 단순히 스택에서 마지막 연결을 꺼내고 닫는다.

#contextmanager 모듈 참고 9.22
#스레드환경 안전 버전 12.6참고





"""
8.4 인스턴스를 많이 생성 시 메모리 절약하려면??

간단한 자료 구조 역할을 하는 클래스의 경우 __slots__속성을 클래스 정의에 추가하면
메모리 사용을 상당히 많이 절약할 수 있다.


"""

class Date:
    __slots__ = ['year','month','day']
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day


#__slots__을 정의하면 파이썬은 인스턴스에서 훨씬 더 압축된 내부 표현식을 사용한다.
#인스턴스마다 딕셔너리를 구성하지 않고, 튜플 or 리스트 같은 부피 작은 고전 배열로 인스턴스가
#만들어진다.
# 슬롯사용 부작용은 , 인스턴스에 새로운 속성을 추가할 수 없다는 점이 있다.
#  __slots__명시자에 나열한 속성만 사용할 수 있는 제약이 있다.


#슬롯을 사용해서 절약하는 메모리는 속성의 숫자와 타입에 따라 다르다.
#튜플에 저장할 때의 메모리 사용과 비교할 만하다.
#슬롯 없이 저장 시, 64비트 파이썬 --> 428바이트 소비
#슬롯 생성 하면?              ---> 156바이트 소비


#슬롯은 다중상속이나 특정 기능 지원하지 않기에, 그냥. 최적화도구로만 쓰자





"""
8.5 클래스 이름의 캡슐화

클래스 인스턴스의 프라이빗 데이터를 캡슐화하고 싶지만, 파이썬에는 접근 제어 기능이 부족하다.

>>> 파이썬 프로그래머들은 언어의 기능에 의존하기보다는 데이터 or 메소드의 이름에 특정 규칙을
사용하여서 의도를 나타낸다.
첫번째 규칙은 _로 시작하느 모든 이름은 내부 구현에서만 사용하도록 가정하는 것

class A:
    def __init__(self):
        self._internal = 0   #내부 속성
        self.public = 1      #공용 속성
    
    def public_method(self):
        '''
        A public method
        '''
    
    def _internal_method(self):
        ...



파이썬은 내부 이름에 누군가 접근하는것을 막지는 않으나, 허술한 코드가 되고, 정신 없음..ㅠㅠㅠ
또한 이름 앞에 밑줄을 붙이는 것은 모듈이름과 모듈 레벨함수에도 사용한다.

ex) _socket 이런 모듈 발견하면, 내부구현이다.
또한 sys._getframe() 과 같은 모듈 레벨 함수는 사용할 떄 겁나 조심해야한다.

# 클래스 정의에 밑줄 두개로 시작하는 이름이 나오기도 한다.

class B:
    def __init__(self):
        self.__private = 0
    def __private_method(self):
        ...
    def public_method(self):
        ...
        self.__private_method()
        ...

이름 앞에 밑줄을 두 개 붙이면 이름이 다른 것으로 변한다. 더 구체적으로 앞에 나온 클래스의 프라이빗 속성은
_B_private  과  _B__private_method 로 이름이 변한다.

#이러한 이름의 변화는 무슨 의미?!!?!?! 
>>>>>>>> 속성에 그 답이 있다. 속성은 속성을 통해 '오버라이드' 할 수 없다.


class C(B):
    def __init__(self):
        super().__init__()
        self.__private = 1        # B.__private를 오버라이드 하지 않는다.
    # B.__private_method()를 오버라이드 하지 않는다.
    def __private_method(self):
        ...


여기서 __private과 __private_method의 이름은 _C__private과 _C__private_method로 변하기에
B클래스의 이름과 겹치지 않는다.



# 정리하면

# _XXXX  = 공용이 아닌 이름인 경우
# __XXXX = 코드가 서브클래싱을 사용할 것이며/ 서브클래스에서 숨겨야할 내부 속성이 있는 경우

# 키워드랑 이름 겹칠 것 같을 땐 이름 뒤에 밑줄 하나
 XXX_
 
 
"""


