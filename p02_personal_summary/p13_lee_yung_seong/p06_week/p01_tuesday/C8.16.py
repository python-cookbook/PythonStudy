#클래스에 생성자 여러 개 정의
#문제
#클래스를 작성 중인데 사용자가 초기화 메소드가 제공하는 방식 이외에 여러가지 방식으로 인스턴스를 생성할 수 있도록 하고 싶다.
#해결
#생성자를 여러개 정의하려면 클래스 메소드를 사용해야,..
import time
class Date:
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day
    #대안 생성자
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year,t.tm_mon,t.tm_mday)
#두번째 생성자를 사용하려면 Date.today()와 같이 함수인 것처럼 호출하면 된다.
b=Date.today()
#토론
#클래스 메소드를 사용하는 주된 목적 중 하낙 ㅏ바로 앞에 나온 것과 같은 생성자를 정의하는 것이다.
#클래스를 첫번째 인자로 받는 것이 클래스 메소드의 중요한 기능이다. 이 클래스는 메소드 내부에서 인스턴스를 생성하고 반환하기 위해 사용된다. 아주 미묘한 부분이지만, 바로 이 측면으로 인해 클래스 메소드가 상속과 같은 기능과도 잘 동작한다.
class NewDate(Date):
    pass
c=Date.today()
d=NewDate.today()

#생성자가 많은 클래스를 정의할 때 주어진 값을 속성에 할당하는 이상 아무런 동작을 하지 않도록 될 수 있으면 초기화메소드를 최대한 단순하게 만들어야 한다. 그리고 대안이 되는 생성자에서 필요한 경우 더 고급 연산을 수행하면 된다.
#개별적인 클랫 ㅡ메소드를 정의하지 않고 __init__메소드에서 여러 동작을 호출하도록 하고 싶을 수도 있다.
class Date:
    def __init__(self,*args):
        if len(args) == 0:
            t = time.localtime()
            args = (t.tm_year, t.tm_mon, t.tm_mday)
        self.year, self.month, self.day = args
#이 기술이 제대로 동작하는 경우도 있지만 대개의 경우 이 코드는 이해하기도 어렵고 유지보수도 얿다.