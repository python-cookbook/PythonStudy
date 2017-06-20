#속성 접근 델리게이팅
#문제
#인스턴스가 속성에 대한 접근을 내부 인스턴스로 델리게이트해서 상속의 대안으로 사용하거나 프록시 구현을 하고 싶다.
#해결
#단순히 설명하자면, 델리게이트는 특정 독작에 대한 구현 책임을 다른 객체에게 미루는 프로그래밍 패턴
class A:
    def spam(self,x):
        pass
    def foo(self):
        pass

class B:
    def __init__(self):
        self._a=A()
    def spam(self,x):
        return self._a.spam(x)
    def foo(self):
        return self._a.foo()
    def bar(self):
        pass

#델리게이트 할 메소드가 몇 개 없으면 주어진 코드를 그대로 작성해도 무방하다. 하지만 델리게이트해야 할 메소드가 많다면 또 다른 대안으로 다음과 같이 getattr 메소드를 정의할 수 있다
class A:
    def spam(self,x):
        pass
    def foo(self):
        pass
class B:
    def __init__(self):
        self._a=A()
    def bar(self):
        pass
    #A클래스에 정의한 모든 메소드를 노출한다.
    def __getattr__(self,name):
        return getattr(self._a,name)

#getattr 메소드는 속성을 찾아보는 도구 모음 정도로 생각하면 된다. 이 메소드는 코드가 존재하지 않는 속성에 접근하려 할 때 호출된다. 앞에 나온 코드에서 정의하지 않은 B에 대한 접근을 A로 델리게이트 한다.
b = B()
b.bar()
b,spam(42)
#델리게이트의 또 다른 예제로 프록시 구현이 있다.
class Proxy:
    def __init__(self,obj):
        self._obj = obj
    def __getattr__(self,name):
        print('getattr:',name)
        return getattr(self._obj,name)
    def __setattr__(self,name,value):
        if name.startswith('_'):
            super().__setattr__(name,value)
        else:
            print('settattr',name,value)
            setattr(self._obj,name,value)
    def __delattr__(self,name):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            print('detattr: ',name)
            delattr(self._obj,name)
#이 프록시 클래스를 사용하려면, 단순히 다른 인스턴스를 감싸면 된다.
class Spam:
    def __init__(self,x):
        self.x=x
    def bar(self,y):
        print('Spam.bar:',self.x,y)
s=Spam(2)
p=Proxy(s)

#속성 접근 메소드 구현을 커스터마이징하면 프록시가 다른 동작을 하도록 만들 수 있다.
#토론
#델리게이트는 상속의 대안으로 사용하기도 한다.
#예를 들어 다음과 같이 코드를 쓰지 않고
class A:
    def spam(self,x):
        print('A.spam',x)
    def foo(self):
        print('A.foo')

class B:
    def spam(self,x):
        print('B.spam')
        super().spam(x)

    def bar(self):
        print('B.bar')

#델리게이트 활용
class A:
    def spam(self,x):
        print('A.spam')
    def foo(self):
        print('A.foo')

class B:
    def __init__(self):
        self._a=A()
    def spam(self,x):
        print('B.spam',x)
        self._a.spam(x)
    def bar(self):
        print('B.bar')
    def __getattr__(self, name):
        return getattr(self._a,name)

#델리게이트를 사용하는 방식은 직접 상속이 어울리지 않거나 객체 간 관계를 더 조절하고 싶을 때 유용하다.
#프록시를 구현하기 위해 델리게이트 사용할 때 주의사항.
#getattr 메소드는 속성을 찾을 수 없을 때 한번만 호출되는 폴백 메소드이다. 따라서 프록시 인스턴스의 속성 자체에 접근하는 경우 이 메소드가 호출되지 않는다.
#둘째
#setattr, delattr 메소드는 프록시 인스턴스 자체와 내부 객체 _obj 속성의 개별 속성에 추가된 로직을 필요로 한다. 프록시에 대한 일반적인 관례는, 밑줄로 시작하지 않는 속성만 델리게이트하는 것이다.
#또한 getattr 메소드는 밑줄 두개로 시작하는 특별 메소드에 적용되지 않는다.



