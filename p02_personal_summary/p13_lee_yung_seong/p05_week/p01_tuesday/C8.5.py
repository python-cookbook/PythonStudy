##클래스 이름의 캡슐화
#문제
#클래스 인스턴스의 프라이빗 데이터를 캡슐화하고 싶지만 파이썬에는 접근 제어 기능이 부족하다
#해결
#파이썬 프로그래머들은 언어의 기능에 의존하기보다는 데이터나 메소드의 이름에 특정 규칙을 사용하여서 의도를 나타낸다. 첫번째 규칙은 밑줄로 시작하는 모든
#이름은 내부 구현에서만 사용하도록 가정하는 것이다.
class A:
    def __init__(self):
        self._internal = 0 #내부 속성
        self.public = 1 #공용 속성
    def public_method(self):
        '''

        publicmethod:
        '''
    def _internal_method(self):
        '''

        :return:
        '''
#파이썬은 내부 이름에 누군가 접근하는 것을 실제로 막지는 않는다. 하지만 이런 ㅅ도는 무례한 것으로 간주되고 결국 허술한 코드가 된다.
#또한 이름 앞에 밑줄을 붙이는 것은 모듈 이름과 모듈 레벨 함수에도 사용한다. 예를 들어 밑줄로 시작하는 모듈이름을 발견한다면 이는 내부 구현이다.
#또한 sys._getframe()과 같은 모듈 레벨 함수는 사용할 때 매우 조심해야한다.
#클래스 정의에 밑줄 두개로 시작하는 이름이 나오기도 한다.
class B:
    def __init__(self):
        self.__private = 0
    def __private_method(self):
        '''

        :return:
        '''
    def public_method(self):
        '''

        :return:
        '''
#이렇게 이름 앞에 밑줄을 두개 붙이면 이름이 다른것으로 변한다. 더 구체적으로 앞에 나온 클래스의 프라이빗 속성은 _B__private과 _B__private_method로 이름이 변한다.
#그렇다면 이러한 이름의 변화는 어떤 의미를 가질까? 답은 바로 속성에 있다. 이런 속성은 속성을 통해 오버리아드 할 수 없다.
class C(B):
    def __init__(self):
        super().__init__()
        self.__private = 1 #B.__private을 오버라이드 하지 않음
    #B.__private_method를 오버라이드 하지 않음
    def __private_method(self):
        '''

        :return:
        '''
#여기서 __private과 __private_method의 이름은 _C__private과 _C__private_method로 변하기 때문에 B클래스의 이름과 겹치지 않음
#토론
#프라이빗 속성에 대한 규칙이 두가지 존재해서(밑줄 한개와 두개) 이중 어떤 스타일을 써야하나?
#대개의 경우 공용이 아닌 이름은 밑줄을 하나만 붙여야 한다.
#하지만 코드가 서브클래싱을 사용할 것이고 서브클래스에서 숨겨야 할 내부 속성이 있다면 밑줄을 두개 붙인다.
#그리고 예약해 둔 단어 이름과 충돌하는 변수를 정의하고 싶을 때 이름 뒤에 밑줄 하나를 붙인다
lambda_=2.0
#밑줄을 변수 이름앞에 붙이지 않는 이유는 내부적으로 사용하는 의도와의 혼동을 피하기 위해서.