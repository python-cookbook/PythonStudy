"""

8.6 관리 속성 만들기

문제

인스턴스 속성을 얻거나 or
                        설정할 때 추가적인 처리를 하고 싶다.

ex) 타입체크, 검증 등등..


속성에 대한 접근을 조절하고 싶으면 프로퍼티 로 정의하면 된다.
예를 들어 다음 코드는 속성에 간단한 타입 체크를 추가하는 프로퍼티를 정의한다.


프로퍼티의 중요 기능

일반적인 속성으로 보이지 않는다는 점!
여기에 접근하면 게터,세터,딜리터 메소드가 자동 실행된다.


"""

class Person:
    def __init__(self, first_name):
        self.first_name = first_name


    #게터 함수
    @property
    def first_name(self):
        return self._first_name

    #세터 함수
    @first_name.setter
    def first_name(self,value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    #딜리터 함수(옵션)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("can't delete attribute")

"""
#위 코드에서 관련 메소드가 3개 있다
#모두 같은 이름을 가져야 한다!
#first_name을 프로퍼티로 만든다.  
나머지 두 메소드는 추가적으로 세터와 딜리터 함수를
first_name 프로퍼티에 추가한다.

여기서 @first_name.setter와 @first_name.deleter 데코레이터는
@property 를 사용해서 first_name을 만들어 놓지 않으면 정의되지 않는 점이 중요하다!

"""


a = Person('Guido')
a.first_name    #게터 호출
# a.first_name=42 #세터 호출   --> 함수내용 중 예외발생 --> #Expected a string
# del a.first_name  #딜리터 호출   --> 함수 내용중 예외발생 --> #can't delete attribute


"""
프로퍼티 구현 시, 기반 데이터가 있다면, 여전히 어딘가에 저장해야 한다.
따라서 게터,세터 메소드에서 _first_name 속성을 직접 다루는 것을 볼 수 있다.

그렇다면 왜 __init__에서 self._first_name이 아닌       self.first_name을 설정하는
이유가 무엇인가?

이번 레시피 속 프로퍼티의 모든 포인트는 속성에 타입 체킹을 적용하는 것에 집중하면 됨
초기화 시 이것을 확인 하고 싶을 확률..이있다... __init__에 self.first_name 설정하면
설정 연산이 세터 메소드에 사용된다. 

이미 존재하는 get과 set 메소드로 프로퍼티를 정의할 수도 있다.
#프로퍼티는 계산한 속성을 정의할 때 사용하기도 한다.
프로퍼티 정의를 반복적으로 사용하는 파이썬 코드 작성하기.


"""


class Person:
    def __init__(self, first_name):
        self.set_first_name = first_name


    #게터 함수
    def get_first_name(self):
        return self._first_name

    #세터 함수
    def set_first_name(self,value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    #딜리터 함수(옵션)
    def del_first_name(self):
        raise AttributeError("can't delete attribute")
    #기존 게터/세터 메소드로 프로퍼티 만들기
    name = property(get_first_name,set_first_name,del_first_name)

b = Person('Guido')


# 프로퍼티 속성은 함께 묶여 있는 메소드 컬렉션이다.
# 프로퍼티가 있는 클래스를 조사해 보면 프로퍼티 자체의 fget, fset, fdel 속성에서
# raw 메소드를 찾을 수 있다.
# 프로퍼티 접근 시 자동 실행된다.

# 프로퍼티는 속성에 추가적인 처리가 필요할 때만 사용해야한다.
# Java 등에 익숙하지 않은 프로그래머는 무조건 게터 세터 써야한다고 생각하고 다음과 같이 짤것이다

class Person:
    def __init__(self,first_name):
        self.first_name = first_name
    @property
    def first_name(self):
        return self._first_name
    @first_name.setter
    def first_name(self, value):
        self._first_name = value


#위 코드는 좋지 않다. 우선 남들이 보기에 불필요하게 장황하며, 이해하기 어렵고, 속도 떨어진다.
#디자인 측면도 별로다.

#수정도 어렵다. 속성에 접근하는 코드의 구문을 수정하면 안되기 때문

#프로퍼티는 계산한 속성을 정의할 때 사용하기도 한다.
# 이런 속성은 실제로 저장하지는 않지만 필요에 따라 계산을 한다.

import math
class Circle:
    def __init__(self, radius):
        self.radius = radius
    @property
    def area(self):
        return math.pi * self.radius **2
    @property
    def perimeter(self):
        return 2 * math.pi * self.radius

c = Circle(4.0)
print(c.radius)   #self.radius = 4
print(c.area)     #50.26548245743669
print(c.perimeter)


# 게터와 세터 직접 사용하기
#
# p = Person('Guido')
# print(p.get_first_name())
# p.set_first_name('Larry')


#시스템 프로그램과 같은 거대 구조에 파이썬 코드를 통합할 때, 이런 필요성이 있다.
#예를 들어, 파이썬 클래스를 원격 절차 호출 or 분산 객체에 기반한 방대한 분산 시스템에 넣기도 한다.

#이런 경우 명시적으로 게터/세터 메소드를 일반적인 메소드처럼 직접 호출하는 것이 사용보다 훨씬 이해하기 쉽다.

# 프로퍼티 정의를 반복적으로 사용하는 파이썬 코드 작성하기.

class Person:
    def __init__(self,first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        return self._first_name

    @first_name
    def first_name(self,value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    #이름이 다른 프로퍼티 코드에 의해 반복(좋지 않음)

    @property
    def last_name(self,value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._last_name = value

