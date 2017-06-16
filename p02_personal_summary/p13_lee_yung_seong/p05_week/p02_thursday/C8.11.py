#자료구조 초기화 단순화하기
#문제
#자료구조로 사용하는 클래스를 작성하고 있는데 반복적으로 비슷한 초기화 함수를 장석하기에 지쳐간다
#해결
#자료구조의 초기화는 베이스 클래스의 init함수를 정의하는 식으로 단순화 할 수 있다.
class Structure:
    _fields=[]
    def __init__(self,*args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
    #속성 설정
        for name, value in zip(self._fields,args):
            setattr(self,name,value)

if __name__=='__main__':
    class Stock(Structure):
        _fields = ['name','shares','price']
    class Point(Structure):
        _fields = ['x','y']
    class Circle(Structure):
        _fields = ['radius']
        def area(self):
            return math.pi * self.radius **2
#결과 클래스를 사용하면 쉽게 만들 수 있다는 것을 확인할 수 있다.
s = Stock('ACME',50,91.1)
p = Point(2,3)
c = Circle(4.5)
s2 = Stock('ACME',50)
#키워드 매개변수를 지원하기로 결정했다면 사용할 수 있는 디자인 옵션이 몇가지 있다 그중 한가지는 키워드 매개변수를 매핑해서 _fields에 명시된 속성 이름에만 일치하도록 만드는 것
class Structure:
    _fields=[]
    def __init__(self,*args,**kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        #모든 위치 매개변수 설정
        for name, value in zip(self._fields,args):
            setattr(self,name,value)
        #남아 있는 키워드 매개변수 설정
        for name in self._fields[len(args):]:
            setattr(self,name,kwargs.pop(name))
        #남아 있는 기타 매개변수가 없는지 확인
        if kwargs:
            raise TypeError('Invalid argments'.format(','.join(kwargs)))
# 사용예
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name','shares','price']
    s1 = Stock('ACME',50,91.1)
    s2 = Stock('ACME',50,price=91.1)
    s3 = Stock('ACME',shares=50,price=91.1)
#혹은 _fields에 명시되지 않은 구조에 추가적인 속성을 추가하는 수단으로 키워드 매개변수를 사용할 수 있다.
class Structure:
    #예상되는 필드를 명시하는 클랫 ㅡ변수
    _fields=[]
    def __init__(self,*args,**kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

         # 속성설정
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
        #(있다면) 추가적인 매개변수 설정
        extra_args = kwargs.keys() - self._fields
        for name in extra_args:
            setattr(self,name,kwargs.pop(name))
        if kwargs:
            raise TypeError('Duplicated values for {}'.format(','.join(kwargs)))

if __name__=='__main__':
    class Stock(Structure):
        _fields = ['name','shares','price']
    s1 = Stock('ACME',50,91.1)
    s2 = Stock('ACME',50,91.1,date='8/2/2012')

#토론
#제너럴한 목적으로 초기화 메소드를 정의하는 기술은 규모가 작은 자료구조를 대량으로 만드는 프로그램에 유용. 이 기술은 일일이 초기화 메소드를 작성하는 것에 비해 코드 양 줄여줌
class Stock:
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price
class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
class Circle:
    def __init__(self,radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius **2

#구현할 때 setattr 함수로 값을 설정하는 메커니즘을 사용했다. 이렇게 하지 않고 인스턴스 딕셔너리에 직접 접근해도 되지 않을까?
class Structure:
    _fields=[]
    def __init__(self,*args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        #매개변수 설정(대안)
        self.__dict__.update(zip(self._fields,args))

#이렇게 해도 동작은 하지만 서브 클래스 구현에 대한 가정을 하는 것이 항상 안전하지는 않다.
#서브클래스가 slots를 사용하기로 하거나 특정 속성을 프로퍼티 혹은 디스크립터로 갑싸기로 하면 인스턴스 딕셔너리에 직접 접근할 때 문제가 발생
#앞에 나온 해결책은 최대한 제너럴한 목적으로 사용할 수 있도록 작성했고 서브클래스에 대해 아무런 가정도 하지 않는다.
#이 기술의 단점 중 한가지는 문서화와 IDE의 도움말 기능에 영향을 준단는 것.
#대부분  이런 문제점은 타입 시그니쳐를 초기화 함수에 첨부하는 식으로 해결 ㄱ가능.