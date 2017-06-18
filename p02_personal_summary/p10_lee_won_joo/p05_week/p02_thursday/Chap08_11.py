"""
8.11  자료 구조 초기화 단순하기

자료 구조로 사용하는 클래스를 작성하고 있는데 , 반복적으로 비슷한 __init__함수를
작성하기에 지쳐 간다.

자료 구조의 초기화는 베이스 클래스의 __init__ 함수를 정의하는 식으로 단순화 할 수 있다.



"""

class Struc:
    #예상되는 필드를 명시하는 클래스 변수
    _fields= []
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
        #속성 설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

#예제 클래스 정의
import math
if __name__ == '__main__':
    class Stock(Struc):
        _fields = ['name','shares','price']

    class Point(Struc):
        _fields = ['x','y']

    class Circle(Struc):
        _fields = ['radius']
        def area(self):
            return math.pi * self.radius ** 2

#결과 클래스를 사용하면 쉽게 만들 수 있다는 것을 확인할 수 있다.

# s = Stock('ACME',50,91.1)
# p = Point(2,3)
# c = Circle(4,5)
# s2 = Stock('ACME',50)


# 키워드 매개변수를 지원하기로 결정했다면 사용할 수 있는 디자인 옵션이 몇 가지 있다.
# 그 중 한가지는 키워드 매개변수를 매핑해서 _fields 에 명시된 속성 이름에만 일치하도록
# 만드는 것이다.

class Struc:
    _fields = []
    def __init__(self, *args, **kwargs):
        if len(args) > len (self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        #모든 위치 매개변수 설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        #남아 있는 키워드 매개 변수 설정
        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))

        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))

if __name__ == '__main__':
    class Stock(Struc):
        0_fields = ['name','shares','price']

    s1 = Stock('ACME',50,91.1)
    s2 = Stock('ACME',shares =50, price =91.1)
    s3 = Stock('ACME',shares =50, price=91.1)

# 혹은 _fields 에 명시되지 않은 구조에 추가적인 속성을 추가하는 수단으로 키워드 매개변수를 사용할 수 있다.

class Struc:
    #예상 되는 필드
    _fields= []
    def __init__(self,*args, **kwargs):
        if len(args) != len(self._fields):
            raise TypeError('expected {} arguments'.format(len(self._fields)))

        for name, value in zip(self._fields, args):
            setattr(self, name, kwargs.pop(name))
        if kwargs:
            raise TypeError

