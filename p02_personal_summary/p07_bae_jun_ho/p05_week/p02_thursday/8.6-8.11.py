''''''
'''

8장 6절 관리 속성 만들기 : 인스턴스 속성을 얻거나 설정할 떄 추가적인 처리를 하고 싶은 경우 접근성을 조절하려면 프로퍼티(property)를 정의하면 된다.

- Property
property와 getter, setter

객체 지향 언어에선 외부 직접적인 접근을 막아놓은 private라는 객체 속성을 지원한다. 이 private 속성의 값을 읽고 쓰기 위해 getter 메소드와 setter 메소드를 사용한다. 

property는 데코레이터로 사용한다. property는 실제모양을 보면 attribute와 거의 유사하지만, 차이점은 실제 데이터를 access 할때 그 값을 계산을 한다. 몇 가지 예를 보면 이해가 쉽다.

import math
class Rectangle(object):

    def __init__(self,r):
        self.r = r

    @property
    def area(self):
        return self.r*self.r

    @property
    def sqrt(self):
        return self.r*math.sqrt(2)

a = Rectangle(4)
print a.area  
# 16 
print a.sqrt  
# 5.65685424949
a.area = 1  
# AttributeError: can't set attribute			

여기서 보면 a.r 은 attribute이다. 따라서 읽기, 쓰기가 모두 된다. 반면에 a.area랑 a.sqrt는 읽기만 되고, 호출할 때 그 값을 계산을 한다. 읽기만 가능하므로 이것을 보완하기 위해서 setter에 access가 가능하다.

또 다른 예는 다음과 같다.

class Test:
   def __init__(self):
      self.__color = "red"

   @property
      def color(self):
          return self.__color

   @color.setter
      def color(self,clr):
          self.__color = clr

if __name__ == '__main__':
     t = Test()
     t.color = "blue"
     print(t.color)

이렇게 함수 위에서 @property를 선언해주면 외부에서 .color로 이 변수를 바로 불러올 수 있다. 또 다른 예를 살펴보면 

class C:
    def __init__(self):
        self._x = None

    def getx(self):
        return self._x

    def setx(self, value):
        self._x = value

    def delx(self):
        del self._x

    x = property(getx, setx, delx, "I'm the 'x' property.")  
    ## x 가 Attribute 이다.


이런 식으로 클래스를 정의해 놓고 하나씩 살펴보면 class C 의 내에 있는 x 는 property 함수의 return 값으로 결정이 되는 내부 변수이다. 
인스턴스를 cc = C 로 생성하고, cc.x 를 보면, property(getx) 가 실행되는데, 이것은 self._x 를 return 하게 되고, 이것은 결국 cc.x 의 값을 출력하라는 뜻이 된다. 다음 예를 살펴보면

class Parrot:
    def __init__(self):
        self._voltage = 100000

    @property
    def voltage(self):
        """Get the current voltage."""
        return self._voltage

    @voltage.setter
    def voltage(self, value):
         self._voltage = value

## voltage 는 함수 명(메소드)이자 attribute 이다.

aParret = Parrot
aParret.voltage = 20000
aParret.voltage

aParret = Parrot 으로 인스턴스를 만들고 난 뒤, aParret.voltage = 20000 식으로 Attr. 을 할당(set)할 수 있고, aParret.voltage 를 출력(get)할 수도 있다. 
@property를 선언하고 난 뒤에는 @Attribute.getterw @Attribute.setter, 등을 사용할 수 있게 된다. 
@property 를 사용하는 목적을 간단하게 말하면 1. 변수를 변경 할 때 어떠한 제한을 두고 싶어서, 2. get,set 함수를 만들지 않고 더 간단하게 접근하게 하기 위해서, 3. 하위호환성에 도움이 됨 등이 있다. 

- Deleter는 property를 명시하지 않으면 정의되지 않는다.

'''


# 예1.
class Person:
    def __init__(self, first_name):
        self._first_name = first_name

    # 게터
    @property
    def first_name(self):
        return self._first_name

    # 세터
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # 딜리터
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")


a = Person('Guido')
a.first_name
# 'Guido'
a.first_name = 42
# Traceback (most recent call last):
#   File "F:\Python\envVirtual\lib\site-packages\IPython\core\interactiveshell.py", line 2881, in run_code
#     exec(code_obj, self.user_global_ns, self.user_ns)
#   File "<ipython-input-4-73dafed1e4ef>", line 1, in <module>
#     a.first_name = 42
#   File "<ipython-input-3-dd6c7f85f80f>", line 15, in first_name
#     raise TypeError('Expected a string')
# TypeError: Expected a string
a.first_name = 'Kim'
a.first_name
# 'Kim'

# 예2.
import math


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius ** 2

    @property
    def perimeter(self):
        return 2 * math.pi * self.radius


c = Circle(4.0)
c.radius
# 4.0
c.area  # ()가 쓰이지 않았다.
# 50.2654
c.perimeter  # ()가 쓰이지 않았다.
# 25.1327


'''

8장 7절 부모 클래스의 메소드 호출 : 오버라이드 된 서브클래스 메소드가 아닌 부모 클래스에 있는 메소드를 호출하고 싶은 경우 부모(super)의 메소드를 호출하려면 super() 함수를 사용한다.

- 상속

코드를 재사용.
기존 클래스에 필요한 기능을 추가하는 경우 기존 클래스를 수정하는 것은 위험성을 내포하고 있다.
이를 방지하기 위해 기존 클래스를 복사해서 새 클래스를 만들어 사용하면 코드 양이 많아지고 같은 기능을 하는 클래스가 다른 곳에 생성되기 때문에 혼란스러워 질 가능성이 높다.
이를 방지하기 위한 개념이 바로 상속(inheritance)이다.
상속을 이용하면 새로운 클래스는 기존의 클래스를 복사하지 않아도 기존 클래스의 모든 코드를 쓸 수 있다.
상속받은 클래스는 필요한 기능만 추가 혹은 변경하여 새 클래스를 정의하고 기존 클래스를 오버라이드(override : 재 정의) 한다.
기존 클래스를 부모(parent)클래스, 슈퍼(super)클래스, 베이스(base) 클래스 등으로 부른다.
새 클래스는 자식(child)클래스, 서브(sub)클래스, 파생(derived)클래스 라고 부른다.

   상속 클래스의 예1)

    class Car():
        def exclaim(self):
            print("I'm a Car!")
    
    class Yugo(Car):  # 자식 클래스에 부모 클래스를 객체로 입력한다.
        pass
    
    give_me_a_car = Car()
    give_me_a_yugo = Yugo()
    give_me_a_car.exclaim() 
    # I'm a Car!
    give_me_a_yugo.exclaim()
    # I'm a Car!     # 부모 클래스로부터 따로 가져온 것 없이 상속(exclaim() 메소드를 통해)을 통해 I'm a Car!를 가져왔다.

위에서 확인한 것 처럼 서브 클래스는 슈퍼 클래스로 부터 모든 것을 상속받는다. 하지만 자식 클래스는 부모 클래스와 같지는 않다. 아래 예에서 확인 할 수 있다.

    상속 클래스의 예2)

    class Car():
        def exclaim(self):
            print("I'm a Car!")
    
    
    class Yugo(Car):
        def exclaims(self):
            print("I'm a Yugo!")
    
    
    give_me_a_car = Car()
    give_me_a_yugo = Yugo()
    give_me_a_car.exclaim()
    # I'm a Car!
    give_me_a_yugo.exclaim()
    # I'm a Car!
    give_me_a_yugo.exclaims()
    # I'm a Yugo!
    
서브 클래스는 슈퍼 클래스로부터 모든 것을 상속 받는다.

    상속 클래스의 예3)
    
    class Person():
        def __init__(self, name):
            self.name = name
            
    class MDPerson(Person):    
        def __init__(self, name):
            self.name = "Doctor " + name
            
    class JDPerson(Person):
        def __init__(self, name):
            self.name = name + ", Esquire"
    
    person = Person('Fudd')
    doctor = MDPerson('Fudd')
    lawyer = JDPerson('Fudd')
    print(person, name)
    # Fudd
    print(doctor, name)
    # Doctor Fudd
    print(lawyer, name)
    # Fudd, Esquire

위 예에서 볼 수 있듯이 __init__() 초기화 메소드는 슈퍼 클래스의 Person과 같은 인자를 취하지만 객체 인스턴스 내부엔 다른 name 값을 저장한다.

서브 클래스는 또한 슈퍼 클래스에 없는 메소드를 추가할 수 있다. 서브 클래스에 추가한 메소드는 서브클래스를 호출하면 서브클래스에서 사용이 가능하지만 슈퍼 클래스에선 사용이 불가능하다.
따라서 이점이 서브 클래스를 이용하는 이유이기도 하다.

서브 클래스에서 슈퍼 클래스의 메소드를 호출하고 싶다면 super() 메소드를 사용한다.

    상속 클래스의 예4)
    class Person():
        def __init__(self, name):
            self.name = name
            
    class EmailPerson(Person):
        def __init__(self, name, email):
            super().__init__(name)     # 슈퍼 클래스인 Person()의 __init__을 서브 클래스인 EmailPerson()에서 사용한다. 이를 통해 슈퍼 클래스만 변경하면 서브 클래스도 변경될 수 있게 된다.
            self.email = email 

super()는 일반적으로 __init__() 메소드에서 부모를 제대로 초기화하기 위해 사용한다. 그리고 파이썬의 특별 메소드를 오버라이드 한 곳에서 super()를 사용하기도 한다.

파이썬은 클래스를 정의할 때 마다 메소드 처리 순서(Method Resolution Order, MRO) 리스트를 계산한다. 이를 통해 상속 구현을 하게 되는데 MRO 리스트는 모든 베이스 클래스를 순차적으로 나열한 리스트다.

상속 구현을 위해 파이썬은 가장 왼쪽에 있는 클래스에서 시작해서 MRO 리스트의 오른쪽으로 이동하면서 일치하는 속성을 찾는다. 

MRO 리스트는 서브 클래스를 슈퍼 클래스보다 먼저 확인하고 슈퍼 클래스가 둘 이상이면 리스트화 된 순서대로 확인하고 유효한 후보가 두가지 이상 있으면 첫 슈퍼 클래스부터 선택하는 제약을 가지고 순서를 정한다.
 
super()를 사용하면 파이썬은 MRO 리스트의 다음 클래스에서 검색을 시작하는데 재정의한 모든 메소드가 모두 super()를 사용하고 한 번만 호출하지만 시스템은 리스트 전체에 동작하고 모든 메소드는 한번 호출된다.
따라서 메소드의 중복 호출을 피할 수 있다. 또한 MRO의 바로 위에 있는 부모에 직접 접근하지 않을 수도 있고 직접적인 부모 클래스가 없을 때도 super()를 사용할 수 있다.

super()를 사용할 땐 조심해야할 점이 있다. super()로 인해 원치 않는 메소드가 호출되는 현상이 발생할 수 있다.
이를 방지하기 위해 상속 관계에서 이름이 같은 모든 메소드는 동일한 구조를 가지도록 한다 이렇게 하면 super()가 직접적으로 부모가 아닌 클래스 메소드를 호출할 때 발생하는 실수를 방지할 수 있다.
또한 가장 상위 클래스에서 메소드 구현을 통해 MRO에서 검색을 할 때 서브 클래스가 아닌 슈퍼 클래스의 실제 메소드에서 멈추도록 하는 것이 좋다.




'''

# 예3.
class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()  # 슈퍼 클래스의 spam() 호출

# 예4.
class A:
    def __init__(self):
        self.x = 0

class B(A):
    def __int__(self):
        super().__init__()  # 서브 클래스에서 슈퍼 클래스를 초기화화
        self.y = 1

# 예5.
class Proxy:
    def __init__(self, obj):
        self._obj = obj

    #내부 obj를 위해 delicate 속성 찾기
    def __getattr__(self, name):
        return getattr(self._obj, name)     # 아래 속성 할당에서 name을 key로 사용한다.

    #delicate 속성 할당
    def __setattr__(self, name, value):
        if name.startwith('_'):       # 이름이 _로 시작하면 super()를 사용해서 __setattr__()의 원본을 호출한다. 그렇지 않은 경우 self._obj를 부른다.
                                      # 명시적으로 super()를 하지 않아도 super()가 동작한다.
            super().__setattr__(name, value)    # 원본 __setattr__ 호출
        else:
            setattr(self._obj, name, value)

'''

8장 8절 서브 클래스에서 프로퍼티 확장 : 서브 클래스에서 슈퍼 클래스의 프로퍼티 기능을 확장하고 싶은 경우 상속을 받는다.



'''

# 예6.
class Person:
    def __init__(self, name):
        self.name = name

    # getter
    @property
    def name(self):
        return self._name

    # setter
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    # deleter
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")


# 예7.
class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name__delete__(self)

s = SubPerson('Guido')
# Setting name to Guido
s.name
# Getting name
# 'Guido'
s.name = 'Larry'
