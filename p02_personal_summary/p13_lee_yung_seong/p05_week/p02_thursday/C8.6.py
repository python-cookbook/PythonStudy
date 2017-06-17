##관리속성만들기
#문제
#인스턴스속성을 얻거나 설정할 때 추가적인 처리를 하고 싶다
#해결
#속성에 대한 접근을 조절하고 싶으면 property를 사용하자.
class person:
    def __init__(self,first_name):
        self.first_name = first_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self,value):
        if not isinstance(value, str):
            raise TypeError('Expected a String')
        self._first_name = value

    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")

#앞의 코드에서 관련 메소드가 세개 있는데 모두 같은이름을 가져야 한다
#첫번째 메소드는 게터 함수로 first_name을 프로퍼티로 만든다. 다른 두 메소드는 추가적으로 세터와 딜리터 함수를 first_name 프로퍼티에 추가한다
#여기서 @데코레이터는 @property를 사용해서 first_name을 만들어 놓지 않으면 정의되지 않는 점이 중요ㅛ하다.from
#프로퍼티의 중요 기능으로 일반적인 속성으로 보이지 않는다는 점이 있지만 여기에 접귾면 자동으로 게터 세터 딜리터 메소드가 자동으로 실행된다.
a = person('Guido')
a.first_name
a.first_name=42
del a.first_name
#프로퍼티를 구현할 때 기반 데이터가 있다면 여전히 어딘가에 저장해야 한다. 따라서 게터 세터 메소드에서 _first_name 속성을 직접 다루는 것을 볼 수 있는데, 여기에 실제 데이터가 들어간다
#그리고 왜 초기화에서 self_first_name이 아닌 self.first_name을 설정하는 이유는 이번 예제에서 프로퍼티의 모든 포인트는 속성에 타입 체킹을 적용하는 것에 집중하는 것이다.
#따라서 초기화를 할 때도 이것을 확인하고 싶을 확률이 있다.
#self.first_name을 설정하면 설정 연산이 세터 메소드를 사용한다.
#이미 존재한 get과 set으로 프로퍼티를 정의할 수 도 있다
class Person:
    def __init__(self,first_name):
        self.set_first_name(first_name)
    def set_first_name(self,value):
        if not isinstance(value, str):
            raise TypeError('Expected a String')
        self._first_name = value
    def get_first_name(self):
        return self._first_name
    def del_first_name(self):
        raise AttributeError('NO DEL')

    name = property(get_first_name,set_first_name,del_first_name)

#토론
#사실 프로퍼티 속성은 함께 묶여 있는 메소드 컬렉션이다. 프로퍼티가 있는 클래스를 조사해 보면 프로퍼티 자체의 fget,fset,fdel 속성에서 raw메소드를 찾을 수 있다.
#일반적으로 fget이나 fset을 직접 호출하지는 않고 프로퍼티에 접근할 때 자동으로 실행된다.
#프로퍼티는 속성에 추가적인 처리가 필요할 때만 사용해야 한다. 자바등에 익숙한 프로그래머는 클래스 속성에 접근할 때 무조건 게터 세터를 사용해야 한다고 생각한다.

#하지만 파이썬에선 이는 좋지않다.
#프로퍼티느 ㄴ계산한 속성을 정의할 때 사용하기도 한다. 이런 속성은 실제로 저장하지는 않지만 필요에 따라 계산을 한다.
import math
class Circle:
    def __init__(self,radius):
        self.radius = radius
    @property
    def area(self):
        return math.pi * self.radius **2
    @property
    def perimeter(self):
        return 2 * math.pi * self.radius

#앞에 나온 프로퍼티를 사용하면 radius.. 가 마치 속성인 것처럼 접근할 수 있다.
c = Circle(4.0)
c.radius
c.area
c.perimeter
#()가 쓰이지 않음
#프로퍼티로 우아한 프로그래밍 인터페이스를 얻을 수 있지만 게터와 세터 함수를 직접 사용하는 것도 가능하다.
#시스템 프로그램과 같은 거대 구조에 파이썬 코드를 통합할 때 이럴 필요성이 있다.
#마지막으로 프로퍼티 정의를 반복적으로 사용하는 파이썬 코드를 작성하지 말자.
