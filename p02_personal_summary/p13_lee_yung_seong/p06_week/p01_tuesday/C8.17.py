#init호출업시 인스턴스 생성
#문제
#인스턴스를 생성해야 하는데 init메소드 호출을 피하고 싶다
#해결
#클래스의 new 메소드를 호출해서 초기화하지 않은 인스턴스를 생성할 수 있다.
class Date:
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day

d = Date.__new__(Date)

#앞에 나온 것처럼 생성된 인스턴스는 초기화 되지 않음. 따라서 적잘한 인스턴스 변수를 설정하는 것은 사용자의 몫
date = {'year':2012, 'month':8, 'day':29}
for key,value in data.items():
    setattr(d,key,value)

d.year
d.month
#토론
#__init__ 을 생략하면 데이터 역직렬화나 대안 생성자로 정의한 클래스 메소드의 구현과 같이 비 표준 방식으로 인스턴스를 생성할 때 문제가 발생하기도 한다.
#예를 들어 Date클래스에 today()를 다음과 같이 정의할 수 있다.
from time import localtime
class Date:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day
    @classmethod
    def today(cls):
        d=cls.__new__(cls)
        t=localtime()
        d.year = t.tm_year
        d.month=t.tm_month
        d.day=t.tm_day
        return d
#이와 유사하게 json 데이터를 역직렬화하면 다음과 같은 딕셔너리가 생성된다
data = {'year':2012,'month':8,'day':29}
#이것을 date 인스턴스로 변환하려면 앞에서 나온 해결책의 기술을 사용하면 된다.
#비표준 방식으로 인스턴스를 생성할 때, 구현에 대해서 너무 많은 가정을 하지 않는 것이 좋다. 일반적으로 확실히 정의되어 있다고 보장되어 있지 않다면 인스턴스 딕셔너리 __dict__에 직접 접근해서 수정하는 코드는 작성하지 말아야 한다.
#그렇지 않으면, 클래스가 __slots__, 프로퍼티, 디스크립터 등 고급기술을 사용하는 경우에 코드에 문제가 생긴다. setattr로 값을 정함ㄴ 코드가 최대한 일반적인 목적이 된다.




