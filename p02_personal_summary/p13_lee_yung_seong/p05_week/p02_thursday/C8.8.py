#서브클래스에서 프로퍼티 확장
#문제
#서브클래스에서 부모 클래스에 정의한 프로퍼티의 기능을 확장하고 싶다.
#해결
#프로퍼티를 정의하는 다음 코드를 보자
class Person:
    def __init__(self,name):
        self.name = name
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        if not isinstance(value,str):
            raise TypeError('Expected a string')
        self._name = value
    @name.deleter
    def name(self):
        raise AttributeError('Cant delete')

#다음 코드는 person을 상속 받아 name 프로퍼티에 새로운 기능을 넣어 클래스를 확장한다.
class SubPerson(Person):
    @property
    def name(self):
        print('Getting Name')
        return super().name
    @name.setter
    def name(self,value):
        print('setting name to ',value)
        super(SubPerson,SubPerson).name.__setattr__(self,value)
    @name.deleter
    def name(self):
        print('Deleting Name')
        super(SubPerson, SubPerson).name.__delete__(self)

#다음은 새로운 클래스를 사용하는 예제이다.
s=SubPerson('Guido')
s.name
#프로퍼티의 메소드 하나를 확장하고 싶으면 다음과 같은 코드를 사용한다.\
class Subperson(Person):
    @Person.name.getter
    def name(self):
        print('Getting Name')
        return super().name

#혹은 세터 하나만 확장하려면 다음과 같이 한다.
class SubPerson(Person):
    @Person.name.setter
    def name(self,value):
        print('Setting name to', value)
        super(SubPerson,SubPerson).name.__set__(self,value)

#토론
#서브클래스의 프로퍼티를 확장하면 프로퍼티가 하나의 메소드가 아닌 게터 세터 딜리터 메소드의 컬렉션으로 정의 되었다는 사실로 인해 자잘한 문제가 발생한다.
#따라서 프로퍼티를 확장할 때 모든 메소드를 다시 정의할지 메소드 하나만 다시 정의할지 결정해야함.
#첫번째 예제는 모든 메소드를 재정의. 기존 구현을 호출하기 위해 슈퍼 사용.
#세터함수에서 사용한 super(subperson...) 은 실수가 아니고 세터의 기존구현으로 델리게이트 하기 위해서 컨트롤은 기존에 구현한 네임 프로퍼티의 셋메소드로 전달해야 한다.
#하지만 이 메소드에 도달하기 위한 유일한 방법은 인스턴스 변수가 아닌 클랫 ㅡ변수로 접근하는 것이다. 바로 이 내용이 super(subperson)... 에서 수행된것이다.
#메소드중 하나만 재정의하려면 @property 자체만 사용하는 것으로는 충분하지 않다. 예를 들어 다음 코드는 동작하지 않는다.
class SubPerson(Person):
    @property
    def name(self):
        print('Getting Name')
        return super().name

#이 코드를 사용하력 ㅗ하면 세터 함수가 모두 사라진것을 확인하게됨
#해결책
class SubPerson(Person):
    @Person.getter
    def name(self):
        print('Getting Name')
        return super().name

#이렇게 하면 기존에 정의한 모든 프로퍼티 메소득 ㅏ복사되고 게터함수가 치환됨.
#이 해결책으로는 하드코딩된 클래스 이름 person을 좀 더 제네릭 한 것으로 치환 할 방법이 없다.
#어떤 베이스 클래스가 프로퍼티를 정의했는지 모른다면 모든 프로퍼티 메소드를 재 정의하고 super()로 기존 구현에 컨트롤을 전달하는 방식을 사용해야 한다.
#디스크립터
class String:
    def __init__(self,name):
        self.name = name
    def __get__(self,instance,cls):
        if instance is None:
            return self
        return instance.__dict__[self.name]
    def __set__(self,instance,value):
        if not isinstance(value,str):
            raise TypeError('Exoected a String')
        instance.__dict__[self.name] = value
#디스크립터 가진 클래스
class Person:
    name = String('name')
    def __init__(self,name):
        self.name = name
#디스크립터에 프로퍼티를 넣어 확장
class SubPerson(Person):
    @property
    def name(self):
        print('Getting Name')
        return super().name
    @name.setter
    def name(self,value):
        print('Setting Name to',value)
        super(SubPerson, SubPerson).name.__set__(self,value)
    @name.deleter
    def name(self):
        print('Deleting Name')
        super(SubPerson,SubPerson).name.__delete__(self)
