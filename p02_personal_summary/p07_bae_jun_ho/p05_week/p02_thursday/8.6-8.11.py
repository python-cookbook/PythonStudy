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


서브 클래스의 프로퍼티를 확장하면 프로퍼티가 하나의 메소드가 아닌 게터, 세터, 딜리터 메소드의 컬렉션으로 정의된 사실로 인해 문제가 발생한다.
따라서 프로퍼티를 확장할 땐 모든 메소드를 재 정의할지 메소드 하나만 재 정의할지 결정해야 한다.



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
# Setting name to Larry


#프로퍼티의 메소드 하나를 확장하고 싶은 경우 (getter)

class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('Getting name')
        return super().name


#프로퍼티의 메소드 하나를 확장하고 싶은 경우 (setter)

class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)


# 예8.

class SubPerson(Person):
    @Person.getter      # getter를 상속을 통해 setter 처럼 사용할 수 있다.
    def name(self):
        print('Getting name')
        return super().name

s = SubPerson('Guido')
s.name
# Getting name
# 'Guido'
s.name = 'Larry'
s.name
# Getting name
# 'Larry'



# 예9.

# 디스크립터

class String:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(selfself, instance, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        instance.__dict__[self.name] = value


# 디스크립터를 가진 클래스

class Person:
    name = String('name')
    def __init__(self, name):
        self.name = name

# 디스크립터를 프로퍼티에 넣어 확장

class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)




'''


8장 9절 새로운 클래스나 인스턴스 속성 만들기 : 타입 확인 등과 같은 추가 기능을 가진 새 인스턴스 속성을 만들고 싶은 경우 완전히 새로운 종류의 인스턴스 속성을 만드려면 그 기능을 디스크립터 클래스 형태로
                                        정의해야 한다.
                                        
- 디스크립터는 get, set, delete를 특별 메소드인 __get__(), __set__(), __delete__() 형식으로 구현한 클래스다. 이 메소드는 인스턴스를 입력받으며 인스턴스의 기반 딕셔너리는 속성으로 만들어진다.
- 디스크립터를 사용하려면 디스크립터의 인스턴스는 클래스 정의에 클래스 변수로 들어가야 한다.


https://www.slideshare.net/dahlmoon/descriptor-20160403 참조.


3. Descriptor 란  __get__(self, instance, class), __set__(self, instance, value), __delete__(self, instance )  3개의 메소드를 가지는 클래스 
    Self는 Descriptor 클래스의 인스턴스  Instance는 class로 생성되는 인스턴스  다른 클래스 변수에 descriptor 인스턴스를 할 당해서 사용
   
4. Descriptor aggregation 구조 인스턴스에서 클래스변수(aggregation)를 호출하 면 descriptor 인스턴스가 descriptor 메소드를 호출하여 인스턴스 내부 변수와 할당값을 세팅 
   Descriptor class User defined class 변수 Descriptor instance User defined instance _변수 __init__ __get__ __set__ __delete__ 
    1. 인스턴스.변수 호출 2. 클래스 내의 변수 확 인 3. Descriptor 인스턴 스가 get/set 메소 드 호출 4. 인스턴스.__dict__에 _변수 할당
    
5. Descriptor aggregation 주의사 항 : 변수명 사용자 인스턴스 저장되는 변수를 클래스 내부에 정의된 변수와 구별 필요 ( _변수명) 

   
6. Descriptor aggregation 주의사 항 : get 인스턴스.변수명을 사용하면 __get__가 호출되므 로 인스턴스._변수명이 미존재하므로 초기값 정의 필요 

   
7. Descriptor 상속 구조 Descriptor 상속관계로 구현시 실제 descriptor 인 스턴스에 값을 보관하여 처, 실제 __get__을 사용 해서 값을 검색해야 함 

8. Descriptor 상속 구조 사용 descriptor 클래스를 상속해서 get 만 사용하는 경우 

class D(object): 
    def __init__(self, x=None): 
        self.x = x
         
    def __get__(self,instance=None,cls=None):
        return self.x 
        
class D1(D): 
def __init__(self, x,y): 
    self.x = D(x) 
    self.y = D(y) 
    
d1 = D1(2,3)
print(" d1")
print(d1.__dict__)
print(d1.x)
print(d1.y)
print(" direct call",d1.x.__get__(), d1.y.__get__()) 
print (" Class binding call x ", D1.__get__(d1.x,d1.x)) 
print (" Class binding call y ", D1.__get__(d1.y,d1.y)) 
print (" class binding",type(d1).__get__(d1.x,d1.x)) 

D1 {'x': <__main__.D object at 0x113f46400>, 'y': <__main__.D object at 0x113f461d0>} 

<__main__.D object at 0x113f46400> 
<__main__.D object at 0x113f461d0> 
direct call 2 3 Class binding call x 2 Class binding call y 3 class binding 2

9. Descriptor 구성

10. Descriptor 처리 절차 Descriptor class를 생성하여 실제 구현 클래스 내부의 속성에 대한 init/getter/setter/deleter 를 통제할 수 있도록 구조화 Class 
    
class Person(): 
    name= Descriptor() 
    user = Person() 
    user.name = ‘Dahl’ 
    
Descriptor class 생성 구현 
class 정의시 속성에 대한 인스턴스 생성 구현
class에 대한 인스턴 스 생성 및 인스턴스 속성 에 값 세팅

11. Descriptor class 정의 클래스에 인스턴스를 관리하는 생성자와 실제 인스 턴스의 값을 관리 

get/set/delete 메소드 정의 

class Descriptor(object): 
    def __init__(self,name): 
    
        self.name = ‘_’ + str(name) 
    def __get__(self, instance, owner): 
    
        return instance.__dict__[self.name] 
    def __set__(self, instance, value): 
        instance.__dict__[self.name] = value 
    
    def __delete__(self, instance): 
        del instance.__dict__[self.name] 
        
인스턴스 객체의 변수명 으로 세팅될 변수명 저장
    
    
12. __get__/__set__ 검색1  getattr,setattr 함수를 이용해서 내부의 값을 직접 검색 및 갱신 
def __get__(self, instance, owner): 
    return getattr(instance, self.name) 
    
def __set__(self, instance, value): 
    setattr(instance,self.name,value)

13. __get__/__set__ 검색2  Instance 내부의 값을 직접 검색 
def __get__(self, instance, owner): 
    return instance.__dict__[self.name] 
    
def __set__(self, instance, value): 
    instance.__dict__[self.name] = value


14. Data descriptor 여부 확인  Inspect 모듈을 이용해서 data descriptor 여 부 확인 i
mport inspect 
print(inspect.isdatadescriptor(descriptor()) #true



15. Descriptor 사용 class 정의/실행 
    1. 구현 클래스에는 속성에 descriptor인스턴스 생성 
    2. 인스턴스 객체의 변수에 직접 값을 할당(set) 
    3. 인스턴스 객체의 변수로 조회(get) 
    
class Person(object): 
    name = Descriptor(“name”) 
    user = Person() 
    print(user.__dict__ ) # {} 
    user.name = 'john smith‘ 
    print(user.__dict__) # {'_name': 'john smith'} 
    print "user.name ",user.name # user.name john smith 
    
    인스턴스의 변수와 내부 관리 변수의 name을 상이하게 관리도 가능



16. Descriptor 메소드 호출 예시 2개 호출 처리는 동일 한 결과가 나온다. 실제 구현시 첫번째 방식이 가독성이 높음 
user = Person() 
user.name = 'john smith’ # Descriptor

.__set__ 호출 
print user.name # Descriptor

.__get__ 호출 
print(user.__dict__) 
user1 = Person() 
Descriptor.__set__(Descriptor(),user1,"dahl") 
Descriptor.__get__(Descriptor(),user1,Descriptor) 
print(user1.__dict__)



17. Descriptor : 함수처리



18. Descriptor 정의
    Descriptor 클래스 정의 
    
    class descriptor(object): 
        def __init__(self,name,func): 
            self.name = '_'+ str(name) 
            self.func = func 
        
        def __get__(self, instance, owner): 
            return getattr(instance,self.name) 
        
        def __set__(self, instance, value): 
            setattr(instance,self.name,value)   # value에 함수 할당



19. Descriptor 실행 함수를 정의하고 할당해서 실행 
    def add(x,y): 
        return x+y 
        
    class A(object): 
        add = descriptor("add",add) 

    a = A() 

    print(a.__dict__) 

    print(A.__dict__) 

    print(a.add(5,5)) 

    print(type(a.__dict__['_add'])) 

    print(A.__dict__['add']) 

    print(a.add) 

    print(A.__dict__['add'].__dict__) 

    da = descriptor("aaa","") 

    print(type(da), da.__dict__, da.name) 
    

20. Descriptor 종류


21. Descriptor 종류 
    Method descriptor와 Data descripter 로 구분
      Method descriptor는 __get__(self, instance, owner) 구현 
      Data descriptor는 __get__(self, instance, owner), __set__(self,instance, value) or __delete__(self, instance) 구현


22. Creating data descriptor Data Descriptor 클래스를 생성해서 처리하는 방법 \
    class Descriptor(object): 
        def __init__(self): 
            self._name = '' 
            
        def __get__(self, instance, owner): 
            print "Getting: %s" % self._name 
            return self._name 
            
        def __set__(self, instance, name): 
            print "Setting: %s" % name 
            self._name = name.title() 
            
        def __delete__(self, instance): 
            print "Deleting: %s" %self._name 
            del self._name 
            
    class Person(object): 
        name = Descriptor() 
        
    >>> user = Person() 
    >>> user.name = 'john smith' Setting: john smith 
    >>> user.name Getting: John Smith 'John Smith‘ 
    >>> del user.name Deleting: John Smith



23. 여러 개 속성변수 처리하기



24. Descriptor : init 메소드 수정 
    Descriptor class에 생성자 메소드에 변수명, 변 수 타입, 변수값을 받아 생성하도록 만듦 
    Class Decriptor : # 변수명, 값타입, 디폴트값, 


25. 구현 class 처리: 클래스 내부의 변수에 descriptor 인스턴스를 생 성함. class Person(object): name =Descriptor ("name",str) age = Descriptor("age",int,42) user = Person()



27. Property 처리


28. Creating Property- 객체 직접 정의(1) 
인스턴스 객체의 변수 접근을 메소드로 제약하기 위해서는 Property 객체로 인스턴스 객체의 변수를 Wrapping 해야 함 

property(fget=None, fset=None, fdel=None, doc=None) 
class P: 
    def __init__(self,x): 
        self.x = x 
        
    def getx(self) : 
        self.x 
        
    def setx(self, x) : 
        self.x = x 
        
    def delx(self) : 
        del self.x 
        x = property(getx,setx,delx," property test ") # Getter, setter, deleter 메 소드를 정의 인스턴스 객체의 변수명과 동일하게 Property 객체 생성(내부에 _x 생김)


29. Creating Property–객체 직접 정의(2) 
실제 인스턴스 객체의 변수에 접근하면 Property 객체의 메소드를 호출하여 처리되고 인스턴스 객 체의 변수값이 변경됨 

p1 = P(1001) 
print id(p1.x) 
print P.__dict__['x']
print id(p1.__dict__['x']) 
print p1.x p1.x = -12 
print p1.x 
print p1.__dict__ #처리결과값 44625868 <property object at 0x02C1D4E0> 44625868 1001 -12 {'x': -12}


30. Decorator 처리


31. Creating Property decorator(1) 인스턴스 객체의 변수 접근을 메소드로 제약하기 위해서는 Property 객체로 인스턴스 객체의 변수를 Wrapping 해야 함 

property(fget=None, fset=None, fdel=None, doc=None) 
class P: 
    def __init__(self,x): 
        self._x = x @property 
    
    def x(self): 
        return self._x 
        
    @x.setter 
    def x(self, x): 
        self._x = x 
            
    @x.deleter 
    def x(self): 
        del self._x # Getter, setter, deleter 메 소드를 정의 인스턴스 객체의 변수명과 동일하게 Property 객체 생성(내부에 _x 생김)


32. Creating Property decorator(2) 
Property 객체 생성하여 처리하는 방식과 동일 

p1 = P(1001) print(id(p1.x)) 
print(p1.x) p1.x = -12 
print (p1.x) 
print (p1.__dict__) #처리결과값 46261915041001 -12 {'_x': -12}


33. 내장함수를 통한 객체접근


34. Built-in 내장함수 내장함수를 이용하여 객체의 속성에 대한 접근 

object.x  getattr() object.x = value  setattr() del(object.x)  delattr() 

함수 구조 

    getattr(object, name[, default]) 
    setattr(object, name, value) 
    delattr(object, name) 
    hasattr(object, name) 
    callable(object)



35. Built-in 내장함수: 예시 1 객체의 속성을 접근하고변경 

class A():
    def __init__(self, name,age): 
        self.name = name 
        self.age = age 
        a = A('dahl',50) 
        if hasattr(a,"name"): 
            print getattr(a,"name") setattr(a,"name","Moon") 
            print getattr(a,"name") 
        else: 
            pass 
        
        if hasattr(a,"age"): 
            print getattr(a,"age") 
        else: 
            pass #처리결과값 dahl Moon 50



36. Built-in 내장함수: 예시 2 메소드 및 함수여부 확인 후 실행 
class A(): 
    def __init__(self, name,age): 
        self.name = name 
        self.age = age 
    
    def in_set(self,name,default): 
        self.__dict__[name] = default 
        print self.__dict__[name]
 
    a = A('dahl',50) 
    
    def add(x,y): return x+y 
        if callable(add): 
            add(5,6) 
        else: 
            pass 
        ifcallable(a.in_set):
            a.in_set('age',20) 
        else:
            pass #처리결과값 dahl Moon 50 20


'''

# 예10.

# 타입을 확인하는 정수형 드스크립터 속성
class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

# 예11.
class Point:
    x = Integer('x')
    y = Integer('y')

'''

8장 10절 게으른 계산을 하는 프로퍼티 사용 : 읽기 전용 속성을 프로퍼티로 정의하고 이 속성에 접근할 때만 계산하도록 할 때 한번 접근하고 나면 이 값을 캐시해 놓고 다음 번에 접근할 때에는 다시 계산하지 않게 하고 싶으면 아래 디스크립터 클래스를 사용한다.

- 게으른 프로퍼티(값 수정이 가능)
class lazyproperty:
    def __init__(self, func):
        self.func = func
    
    del __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

- 게으른 프로퍼티(값 수정이 불가능)
def lazyproperty(func):
    name = '_lazy_' + func.__name__

    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value
    return lazy
    
    이 방법을 사용하면 값 설정이 불가능하다. 읽기 전용으로만 실행되기 때문에 값을 얻기 위해서 항상 프로퍼티의 getter 함수를 사용해야만 한다.

- lazyproperty 클래스는 프로퍼티와 동일한 이름을 사용해서 인스턴스 __get__() 메소드에 계산한 값을 저장하는 식으로 이를 활용한다. 이렇게 하면 그 값은 인스턴스 딕셔너리에 저장되고 추후 프로퍼티의 계산을 하지 않도록 한다.            
       
- 디스크립터가 __get__() 메소드만 정의하면 접근하는 속성이 인스턴스 딕셔너리에 없을 때만 실행된다.             

            
'''

# 예12.
class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print('Computing area')
        return 2 * math.pi * self.radius

    @lazyproperty
    def perimeter(self):
        print('Conputing perimeter')
        return 2 * math.pi * self.radius

c = Circle(4.0)
vars(c)     # 인스턴스 변수 구하는 법
# {'radius': 4.0}
c.radius
# 4.0
c.area      # 면적을 계산하고 추후 변수 확인
# Computing area
# 50.2654824
vars(c)
# {'area': 50.2654824, 'radius': 4.0}
c.area
# 50.2654824  # 두 번째 실행에서 Computing area 메세지가 없어졌다. 즉 속성에 접근해도 더 이상 프로퍼티를 실행하지 않는다. 인스턴스 딕셔너리에 저장되고 프로퍼티의 계산을 하지 않았기 때문이다.
c.perimeter
# Computing perimeter
# 25.1327412
c.perimeter
# 25.1327412    # 두 번째 실행에서 Computing perimeter 메세지가 없어졌다. 위와 동일하다. 프로퍼티를 다시 실행하려면 변수 c를 삭제하고 다시 생성한 다음 실행하면 된다.

'''

8장 11절 자료 구조 초기화 단순화 하기 : 자료 구조로 사용하는 클래스를 작성하고 있는데, 반복적으로 비슷한 __init__() 함수를 작성해서 사용해야 한다면 베이스 클래스의 __init__() 함수를 정의하는 식으로 단순화 할 수 있다.





'''

# 예13.

class Structure:
    # 예상되는 필드를 명시하는 클래스 변수
    _fields = []
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # 속성 설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # 예제 클래스 정의

if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    class Point(Structure):
        _fields = ['x', 'y']

    class Circle(Structure):
        _fields = ['radius']
        def area(self):
            return math.pi * self.radius ** 2

s = Stock('ACME', 50, 91.1)     # 여기서 이미 3개의 매개변수를 입력해서
p = Point(2, 3)
c = Circle(4.5)
s2 = Stock('ACME', 50)      # s의 매개변수 개수와 다르므로 정의한 TypeError: Expected 3 arguments 가 발생한다.

# 키워드 매개변수를 매핑해서 _fields에 명시된 속성 이름에만 일치하도록 만드는 방법
# 예14.
class Structure:
    _fields = []
    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # 모든 위치 매개변수 설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # 남아있는 키워드 매개변수 설정
        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))

        # 남아있는 기타 매개변수가 없는지 확인
        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))


if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, price=91.1)
    s3 = Stock('ACME', shares=50, price=91.1)


