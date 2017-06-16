#부모 클래스의 메소드 호출
#문제
#오버리아드된 서브클래스 메소드가 아닌 부모 클래스에 있는 메소드를 호출하고 싶다
#해결
class A:
    def spam(self):
        print('A.Spam')
class B(A):
    def spam(self):
        print("B.Spam")
        super().spam()#부모의 spam 호출

#super는 일반저긍로 초기화 메소드에서 부모를 제대로 초기화 하기 위해 사용한다.
class A:
    def __init__(self):
        self.x=0
class B(A):
    def __init__(self):
        super().__init__()
        self.y=1
#그리고 파이썬의 특별 메소드를 오버라읻 ㅡ한 코드에서 super()를 사용하기도 함
class Proxy:
    def __init__(self,obj):
        self._obj = obj
    #내부 obj를 위해 델리게이트 속성 찾기
    def __getattr__(self, name):
          return getattr(self._obj, name)
    #델리게이트 속성 할당
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name,value)
        else:
            setattr(self._obj,name,value)
#이 코드에서, __setattr__() 구현 이름 확인이 들어 있다. 만약 이름이 밑줄로 시작하면 super()를 사용해서 __setattr__()의 원래의 구현을 호출한다. 그렇지 않다면
#내부 객체인 self._obj를 부른다. 조금 이상하게 보일지도 모르겠지만, 명시적으로 클래스를 표시하지않아도 super()가 동작한다.
#토론
#super()함수를 올바르게 사용하기는 무척어렵다. 때때로 부모 클래스 메소드를 직접 호출하기 위해 다음과 같이 작성한 코드를 볼 수 있다.
class Base:
    def __init__(self):
        print('base.__init')
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A._init')
#앞에 나오는 코드가 대부분의 경우 동작하기는 하지만 다중 상속에서 문제가 발생한다.
#super사용
class Base:
    def __init__(self):
        print('Base.__init')
class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init')
class B(Base):\
    def __init__(self):
        super().__init__()
        print('B.__init')
class C(A,B):
    def __init__(self):
        super().__init__()
        print('C.__init')


#MRO 리스트의 클래스 순서가 정의하려는 거의 모든 클래스 구조에 의미가 통해야 한다는 점이다.
#super 함수를 사용할 때 파이썬은 MRO의 다음 클래스에서 검색을 시작한다. 재 정의한 모든 메소드가 모듀 super()를 사용하고 한 번만 호출하지만, 시스템은 MRO리스트 전체에 동작하고
#모든 메소드가 모두 super()를 사용하고 한번만 호출하지만 시스템은 MRO리스트 전체에 동작하고 모든 메소드는 한번만 호출된다.
#super 주의사항
#첫째, 상속 관계에서 이름이 같은 모든 메소드는 동일한 구조를 가지도록 한다.
#둘째, 가장 상위에 있는 클래스에서 메소드 구현을 제공해서 MRO에서 검색을 할 때 결국은 실제 메소드에서 멈추도록 하는 것이 좋다.