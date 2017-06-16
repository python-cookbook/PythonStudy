"""
8.8 서브클래스에서 프로퍼티 확장
>> 서브 클래스에서 부모 클래스에 정의한 프로퍼티의 기능을 확장하고 싶다.

프로퍼티를 정의하는 다음 코드를 보자.

"""


class Person:
    def __init__(self, name):
        self.name = name

    # 게터 함수
    @property
    def name(self):
        return self._name

    # 세터 함수
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    # 딜리터 함수
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")


# 다음 코드는 Person 을 상속받아 name프로퍼티에 새로운 기능을 넣어 클래스를 확장한다.

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


s = SubPerson('Guido')  # setter함수에 Guido 넣고
s.name  # Getting name
s.name = 'Larry'  # Setting name to Larry
s.name = 42  # Person.name.setter 발동하여 예외처리


# 프로퍼티의 메소드 하나를 확장하고 싶으면 다음과 같은 코드를 사용한다.

class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('Getting name')
        return super().name


# 혹은 세터 하나만 확장 하려면 다음과 같이 한다.



class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)


# 토론

# 서브클래스의 프로퍼티 확장 하면, 프로퍼티가 하나의 메소드가 아닌 게터,세터,딜리터 메소드의 컬렉션으로 정의되었다는 사실로 인해
# 자잘한 문제가 발생한다.

# 따라서 프로퍼티 확장 시, 모든 메소드 정의할지
# 메소드 하나만 재정의할지 결정해야 함


# 첫 예제에서는 모든 메소드 재정의함
# 모든 메소드에서 기존 구현을 호출하기 위해 super() 사용함
# 세터 함수에서 사용한 super(SubPerson, SubPerson).name.__set__(self,value) 는 실수가 아니다.
# 세터의 기존 구현으로 델리게이트하기 위해서, 컨트롤은 기존에 구현한 name 프로퍼티의 __set__메소드로 전달해야 한다.

# 하지만, 이 메소드에 도달하기 위한 유일한 방법은 인스턴스 변수가 아닌 클래스 변수로 접근하는 것이다.
# 바로 이내용이 super(SubPerson,SubPerson)에서 수행된 것.
# 메소드 중 하나만 재정의하려면 @property 자체만 사용하는 것으로는 충분하지 않다. 예를 들어 다음 코드는 동작하지 않는다.

class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name


# 이 코드를 사용하려고 하면 세터 함수가 모두 사라진 것을 확인하게 된다.

# s = SubPerson('Guido')

# 위 코드는 AttributeError 가 발생한다.

# 수정하려면

class SubPerson(Person):
    @Person.getter
    def name(self):
        print('Getting name')
        return super().name


s = SubPerson('Guido')
s.name
s.name = 'Larry'
s.name


# 이렇게 하면, 기존에 정의한 모든 프로퍼티 메소드가 복사되고 게터 함수가 치환된다.

# 이 해결책으로는, 하드코딩된 클래스 이름 Person을 좀 더 제네릭한 것으로 치환할 방법이 없다.
# 어떤 베이스 클래스가 프로퍼티를 정의했는지 모른다면 모든 프로퍼티 메소드를 재정의하고
# super() 로 기존 구현에 컨트롤을 전달하는 방식을 사용해야 한다.

# 레시피 8.9 에 나온 것처럼 이번 레시피에 나온 첫번째 기술을 디스크립터를 확장하는데 사용할 수도 있다.

# 디스크립터

class String:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        instance.__dict__[self.name] = value


# 디스크립터를 가진 클래스
class Person:
    name = String('name')

    def __init__(self, name):
        self.name = name


# 디스크립터에 프로퍼티를 넣어 확장
class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        print('Setting name to ', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)
