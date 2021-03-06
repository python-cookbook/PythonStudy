##########################################################################################################
# 8.5] 클래스 이름의 캡슐화
#   * 클래스 인스턴스의 "private" 데이터를 캡슐화하고 싶지만, 파이썬에는 접근 제어 기능이 부족하다.
#
#   * 파이썬 프로그래머들은 언어의 기능에 의존하기보다는 데이터나 메소드의 이름에 특정 규칙을 사용하여 의도를 나타낸다.
#   * 첫번째 규칙으로, 밑줄(_)로 시작하는 모든 이름은 내부 구현에서만 사용하도록 가정하는 것이다.
#       파이썬은 내부 이름에 누군가 접근하는 것을 실제로 막지는 않는다. 하지만 이런 시도는 무례한 것으로 간주되고
#       결국 허술한 코드가 된다. 또한 이름 앞에 밑줄을 붙이는 것은 모듈명 및 모듈 레벨 함수에도 사용한다.
#   * 두번째 규칙으로, 클래스 정의에 밑줄 두 개(__)로 시작하는 이름이 나오기도 한다.
#       이름 앞에 밑줄을 두 개 붙이면 이름이 다른 것으로 변한다.
#       더 구체적으로, 앞에 나온 클래스의 프라이빗 속성은 _B__private와 _B__private_method로 이름이 변한다.
#       그렇다면 이러한 이름의 변화는 어떤 의미를 가질까? 답은 바로 속성에 있다.
#       이런 속성은 속성을 통해 오버라이드할 수 없다.
#       아래 클래스 C의 예시에서, __private와 __private_method의 이름은 _C__private, _C__private_method로
#       변하기 때문에 B 클래스의 이름과 겹치지 않는다.
#
#   * 프라이빗 속성에 대한 규칙이 두 가지 존재하는데, 언제 어떤 규칙을 써야 할까?
#       대개의 경우 공용이 아닌 이름은 밑줄을 하나만 붙여야 한다.
#       하지만 코드가 서브클래싱을 쓸 것이고 서브클래스에서 숨겨야 할 내부 속성이 있다면 밑줄을 두 개 붙인다.
#       그리고 예약해둔 단어명과 충돌하는 변수를 정의하고 싶을 때가 있는데, 이런 경우 이름 뒤에 밑줄을 하나 붙인다.
#       (예 : lambda_ = 2.0)
#       밑줄을 변수 앞에 붙이지 않는 이유는 내부적으로 사용하려는 의도와의 혼동을 피하기 위해서이다.
##########################################################################################################

# 내부 속성 및 공용 속성
class A:
    def __init__(self):
        self._internal = 0  # 내부 속성
        self.public = 1     # 공용 속성

    def public_method(self):
        '''
        A public method
        '''

    def _internal_method(self):
        '''
        A private method
        '''

class B:
    def __init__(self):
        self.__private = 0
    def __private_method(self):
        pass
    def public_method(self):
        pass

class C(B):
    def __init__(self):
        super().__init__()
        self.__private = 1  # B.__private를 오버라이드하지 않는다.

    # B.__private_method를 오버라이드하지 않는다.
    def __private_method(self):
        pass