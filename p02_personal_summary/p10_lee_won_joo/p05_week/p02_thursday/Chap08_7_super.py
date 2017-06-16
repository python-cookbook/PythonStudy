"""
8.7 부모 클래스의 메소드 호출

오버라이드 된 서브클래스 메소드가 아닌, 부모 클래스 메소드 호출 원한다.

"""


## super 사용

class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()

#super() 는 일반적으로 자식 [init 메소드]에서 [부모를 제대로 초기화] 하기 위해 사용한다.



class A:
    def __init__(self):
        self.x = 0

class B(A):
    def __init__(self):
        super().__init__()
        self.y=1

child = B()
print(child.y) #1
print(child.x) #0


# 파이썬의 특별메소드를 오버라이드한 코드에서 super() 를 사용하기도 한다.
# 부모 초기화
class Proxy:
    def __init__(self, obj):
        self._obj = obj

    #내부 오브젝트를 위해 델리게이트 속성 찾기
    '''
     델리게이트란? 
     '대리인'이라는 뜻의 델리게이트는 메소드를 참조하는 변수
    '''
    def __getattr__(self, name):
        return getattr(self._obj, name)       #기본 설정을 유지하겠다.

    #델리게이트 속성 할당
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)  #원본 __setattr__호출
        else:
            setattr(self._obj, name, value)


print(Proxy.__mro__)  #(<class '__main__.Proxy'>, <class 'object'>)

    #이 코드에서, __setattr__() 구현에 이름 확인이 들어 있다.
    #만약 이름이 밑줄로 시작하면 super() 를 사용해서 __setattr__() 의 원래 구현을 호출한다.
    #그렇지 않다면, 내부 객체인 self._obj를 부른다.
    #조금 이상하게 보일 수 있으나, 명시적으로 클래스를 표시 하지 않아도 super() 가 동작한다.

    #토론
    #super함수를 올바르게 사용하기는 무척 어렵다. 떄떄로 부모 클래스 메소드를 직접 호출하기 위해
    #다음과 같이 작성한 코드를 볼 수 있다.

class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')

#앞에 나오는 코드가 대부분의 경우 "동작하기"는 하지만, 다중 상속과 같은 상황에서 문제가 발생하기도 한다.
print('앞에 나오는 코드가 대부분의 경우 "동작하기"는 하지만, 다중 상속과 같은 상황에서 문제가 발생하기도 한다.')
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

c = C()
## Base.__init__가 두번 호출된다. 왜냐 !
#A와 B 모두 Base라는 부모에게 상속받고 있으니까


# Base.__init__() 을 두번 호출하는 것이 문제가 없을 수도 있지만, 항상 그렇지만은 않다.
# 하지만 super() 를 사용하여 코드를 수정한다면 올바르게 동작한다.

class Base:
    def __init__(self):
        print('조상이다!')
class A(Base):
    def __init__(self):
        super().__init__()
        print('나는 A에요')
class B(Base):
    def __init__(self):
        super().__init__()
        print('나는 B이다!')
class child(A,B):
    def __init__(self):
        super().__init__()
        print('A와 B의 아들입니다.')

d = child()


# 위 같은 현상은 죽음의 다이아몬드 해결한 것
# 파이썬 상속 구현을 이해해야 한다.

#클래스를 정의할 때마다 파이썬은 메소드 처리 순서 (method resolution order, MRO) 리스트를 계산한다.
# MRO 리스트는 모든 베이스 클래스를 단순히 순차적으로 나열한 리스트이다.

print(child.__mro__) #(<class '__main__.child'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Base'>, <class 'object'>)


#상속 구현을 위해 파이썬은 가장 왼쪽 --->오른쪽 이동하며 일치하는 속성을 찾는다.
#MRO  리스트 자체를 실제로 결정할 떄, C3 선형화라는 기술을 사용한다.
#너무 계산이 복잡해지지 않도록 부모 클래스의 MRO를 다음 세가지 세약 조건 하에 [합병 정렬] 한다.


"""
자식 클래스를 부모보다 먼저 확인한다.
부모 클래스가 둘 이상이라면 리스팅한 순서대로 확인한다.
유효한 후보가 두 가지 있으면, 첫번째 부모 클래스부터 선택한다.
"""

#어찌됫든 중요한건 MRO리스트의 순서가 정의하려는 거의 모든 클래스구조에 "의미가 통해야" 한다는 점

#super() 함수 -> 파이썬은 MRO의 다음 클래스에서 검색 ->
# 모든 메소드가 super() 사용하고 한번 호출 -> 시스템은 MRO 리스트 전체에 동작하고 모든 메소드는 한번만 호출된다.
#바로 이 때문에 두번째 예제의 Base.__init__이 두 번 호출되지 않은 것이다.


#super의 놀라운 측면 중 하나는 이 함수가 MRO의 바로 위에 있는 부모에 직접 접근하지 않을 때도 있고, 직접적인 부모 클래스가 없을 때도
#super를 사용할 수 있다는 점이다.


class A:
    def spam(self):
        print('A.SPAM')
        super().spam()     #얘가 B.spam을 부를거임.
        print('아 다 뽑았다.')
# A.spam() #TypeError: spam() missing 1 required positional argument: 'self'

class B:
    def spam(self):
        print('B.spam')
class C(A,B):
    pass

c = C()
c.spam()

#A 클래스의 super().spam()이 실제로 전혀 관련없는 B 클래스의 spam()을 호출했다.

print(C.__mro__) #(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>)

#쓸데없는것도 상속 받을 수 있으니 다음의 규칙을 지키자.

#1)
#상속 관계에서 이름이 같은 모든 메소드는 동일한 구조를 가지도록 한다.
#같은 인자 수, 같은 인자 이름


#2)
#가장 상위에 있는 클래스에서 메소드 구현을 제공해서 MRO에서 검색을 할 때 결국은 실제 메소드에서 멈추도록 하는 것이 좋다.











