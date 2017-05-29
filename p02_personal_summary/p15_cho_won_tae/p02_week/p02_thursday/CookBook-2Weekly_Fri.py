# 3.11 임의의 요소 뽑기
# 문제
# 시퀀스에서 임의의 아이템을 고르거나 난수를 생성하고 싶다
# 해결
# random 모듈에는 이 용도에 사용할 수 있는 많은 함수가 있다.
# 예를 들어 시퀀스에서의 임의의 아이템을 선택하려면 random.choice()를 사용한다
import random
values = [1,2,3,4,5,6]
a = random.choice(values)
print(a) # 1~6 중 아무거나 하나 출력
# 임의의 아이템을 N개 뽑아서 사용하고 버릴 목적이라면 random.sample()을 사용한다
a = random.sample(values,2)
print(a) # 1~6 중 아무거나 [a,b]로 출력
# 단순히 시퀀스의 아이템을 무작위로 섞으려면 random.shuffle()을 사용한다
random.shuffle(values)
print(values) # [2, 4, 5, 6, 3, 1](랜덤으로 섞기) 출력
# 임의의 정수를 생성하려면 random.randint()를 사용한다
a = random.randint(0,10)
print(a) # 0~10 사이에서 아무 정수나 출력
# 0과 1 사이의 균등 부동 소수점 값을 생성하려면 random.random()을 사용한다
a = random.random()
print(a) # 0 과 1사이의 소수점 값을 랜덤으로 출력
# N비트로 표현된 정수를 만들기 위해서는 random.getrandbits()를 사용한다
a = random.getrandbits(200)
print(a) # 1387336802992043279930565569569261599345861096693398452046040 출력
# 토론
# random 모듈은 Mersenne Twister 알고리즘을 사용해 난수를 발생시킨다.
# 이 알고리즘은 정해진 것이지만,random.seed() 함수로 시드 값을 바꿀 수 있다
# 또한 random함수는 random.uniform() = 균등 분포 숫자 계산, random.gauss()는 정규분포 숫자 계산

# 3.12 시간 단위 변환
# 문제
# 날짜를 초로, 시간을 분으로처럼 시간 단위 변환을 해야 한다
# 해결
# 단위 변환이나 단위가 다른 값에 대한 계산을 하려면 datetime 모듈을 사용한다.
# 예를 들어 시간의 간격을 나타내기 위해서는 timedelta 인스턴스를 생성한다
from datetime import timedelta
a = timedelta(days=2,hours=6)
b = timedelta(hours=4.5)
c = a + b
print(c) # 2 days, 10:30:00 출력
print(c.days) # 2 출력
print(c.seconds) # 37800 출력 (시:분:초에서만 초단위로 바꿔줌)
print(c.seconds/3600) # 10.5 출력
print(c.total_seconds() / 3600) # 58.5 출력(total_seconds()함수는 day까지 초로 세줌)
# 특정 날짜와 시간을 표현하려면 datetime 인스턴스를 만들고 표준 수학 연산을 한다
from datetime import datetime
a = datetime(2012,9,23)
print(a) # 2012-09-23 00:00:00 출력
b = datetime(2012,12,21)
print(b) # 2012-12-21 00:00:00 출력
d = b - a
print(d) # 89 days, 0:00:00 출력
now = datetime.today()
print(now) # 2017-05-25 13:27:14.136383 출력(정답)
print(now+timedelta(minutes=10)) # 2017-05-25 13:37:39.519607 출력
# 즉, now 변수에서 timedelta() 함수를 써서 분에다가 10을 더한것
# 계산을 할때는 윤년을 인식한다는 점에 주목하자
a = datetime(2012,3,1)
b = datetime(2012,2,28)
print(a-b) # 2 days, 0:00:00 출력
# 토론
# 대부분의 날짜, 시간계산문제는 ㅇatetime 모듈로 해결할 수 있다
# 시간대나 퍼지 시계 범위, 공휴일 계산 등의 더욱 복잡한 날짜 계산이 필요하다면 dateutil 모듈을 알아보자!!! dateutil dateutil
# 대부분의 비슷한 시간 계산은 dateutil.relativedelta() 함수로 수행할 수 있다.
# 하지만 한 가지 주목할 만한 기능으로 달을 처리하기 위해 차이(그리고 서로 다른 날짜차이)를 채워 주는 것이 있다
a = datetime(2012,9,23)
print( a+timedelta(months=1)) # 에러뜸!!
from dateutil.relativedelta import relativedelta
a + relativedelta(months=1)
print(datetime.datetime(2012,10,23,0,0))

# 3.13 마지막 금요일 날짜 구하기
# 문제
# 한 주의 마지막에 나타난 날의 날자를 구하는 일반적인 해결책을 만들고 싶다. 예를 들어 마지막 금요일이 며칠인지 궁금하다
# 해결
# 파이썬의 datetime 모듈에 이런 계산을 도와주는 클래스와 함수가 있다
# 이문제를 해결하기 위한 괜찮은 코드는 다음과 같다
from datetime import datetime, timedelta
weekdays = ['Mon','Tue','Weds','Thur','Fir','Sat','Sun']
def get_previous_byday(dayname, start_date=None):
    if start_date is None:
        start_date = datetime.today()
    day_num = start_date.weekday()
    day_num_target = weekdays.index(dayname)
    days_ago = (7+day_num - day_num_target) % 7
    if days_ago == 0:
        days_ago = 7
    target_date = start_date - timedelta(days=days_ago)
    return target_date
# 토론
# 시작일자에서 적절한 timedelta 인ㅅ느턴스를 빼서 원하는 날짜를 계산한다

# 3.15 문자열을 시간으로 변환
# 문제
# 문자열 형식의 시간 데이터를 datetime 객체로 변환하고 싶다
# 해결
# 파이썬의 datetime 모듈을 사용하면 상대적으로 쉽게 이 문제를 해결할 수 있다
from datetime import datetime
text = '2017-06-06'
y = datetime.strftime(text,'%Y-%m-%d')
z = datetime.now()
diff = y  - z
print(diff)
# 토론
# datetime.strptime() 메소드는 네자리 연도 표시를 위한 %Y 두자리 월표시를 위한 %m와 같은 서식을 지원한다


# CHAPTER 4 - 이터레이터와 제너레이터
# 객체 순환은 파이썬의 강력 한 기능 중 하나이다. 순환을 단순히 시퀀스 내부 아이템에 접근하는 방법으로 생각할 수도있다
# 하지만 순환을 통해 할 수 있는 일은, 순환 객체 만들기, itertools 모듈의 순환 패턴 적용하기, 제너레이터 함수 만들기 등
# 4.1 수동으로 이터레이터 소비
# 문제
# 순환 가능한 아이템에 저근할 때 for 순환문을 사용하고 싶지 않다.
# 해결
# 수동으로 이터레이터를 소비하려면 next() 함수를 사용하고 StopIteration 예외를 처리하기 위한 코드를 직접 작성한다
with open (r"C:\Users\Won Tae CHO\Desktop\Python_data\dept.csv") as f:
    try:
        while True:
            line = next(f)
            print(line, end='')
    except StopIteration:
        pass
# deptno,dname,loc
# 10,ACCOUNTING,NEW YORK
# 20,RESEARCH,DALLAS
# 30,SALES,CHICAGO
# 40,OPERATIONS,BOSTON 출력
# 일반적으로 StopIteration은 순환의 끝을 알리는 데 사용한다.
# 하지만 next()를 수동으로 사용한다면 None과 같은 종료 값을 반환하는데 사용할 수도 있다
with open (r"C:\Users\Won Tae CHO\Desktop\Python_data\dept.csv") as f:
    while True:
        line = next(f,None)
        if line is None:
            break
        print(line,end='')
# 토론
# 대개의 경우, 순환에 for 문을 사용하지만 보다 더 정교한 조절이 필욯ㄴ 때도 있다
# 기저에서 어떤 동작이 일어나는지 정확히 알아둘 필요가 있다
# 다음 상호 작용을 하는 예제를 통해 순환하는 동안 기본적으로 어떤 일이 일어나는지 알아보자
items=[1,2,3]
# 이터레이터 얻기
it = iter(items) # items.__iter__() 실행
print(next(it)) # 1 출력
print(next(it)) # 2 출력
print(next(it)) # 3 출력
print(next(it)) # 출력안됨

# 4.2 델리게이팅 순환
# 문제
# 리스트, 튜플 등 순환 가능한 객체를 담은 사용자 정의 컨테이너를 만들었다. 이 컨테이너에 사용 가능한 이터레이터를 만들고 싶다
# 해결
# 일반적으로 컨테이너 순환에 사용할 __iter__() 메소드만 정의해주면 된다
class Node:
    def __init__(self,value):
        self._value = value
        self._children = []
    def __repr__(self):
        return 'Node({!r})'.format(self._value)
    def add_child(self,node):
        self._children.append(node)
    def __iter__(self):
        return iter(self._children)

if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch) #Node(1) Node(2) 출력

# 이코드에서 __iter__() 메소드는 순환 요청을 _children 속성으로 전달한다
# 토론
# 파이썬의 이터레이터 프로토콜은 __iter__()가 실제 순환을 수행하기 위한 __next__() 메소드를 구현하는 특별 이터레이터 객체를 반환
# 하기를 요구한다. 만약 다른 컨테이너에 들어 있는 내용물에 대한 순환이 해야 할 작업의 전부라면, 이터레이터의 동작 방식을
# 완전히 이해할 필요는 없다.

# 4.3 제너레이터로 새로운 순환 패턴 생성
# 문제
# 내장 함수(range(),reversed())와는 다른 동작을 하는 순환 패턴을 만들고 싶다.
# 해결
# 새로운 순환 패턴을 만들고 싶다면, 제너레이터 함수를 사용해서 정의해야 된다
# 특정 범위의 부동 소수점 숫자를 만드는 제너레이터 코드는 다음과 같다
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment
# 이런 함수를 사용하려면, for 순환문이나 순환 객체를 소비하는 다른 함수(sum(),list() 등)을 사용한 순환을 해야한다
for n in frange(0,4,0.5):
    print(n) # 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5 출력
# 토론
# 내부의 yield 문의 존재로 인해 함수가 제너레이터가 되었다.
# 일반 함수와는 다르게 제너레이터는 순환에 응답하기 위해 실행된다.
# 이런 함수가 어떻게 동작하는지 다음 예를 통해 알아보자
def countdown(n):
    print('Starting to coun from',n)
    while n > 0:
        yield n
        n -= 1
    print('Done')

print(countdown(3)) # <generator object countdown at 0x000001EAE8F5C4C0> 출력하므로 제터레이터임을 주목!!
# 값을 만들기 위한 첫 번째 실행
c = countdown(3)
next(c) # Starting to coun from 3 출력
next(c) # Starting to coun from 2 출력
next(c) # Starting to coun from 1 출력
next(c) # Done 출력
# 중요한 점은 제너레이터 함수가 순환에 의한 다음 연산에 응답하기 위해서만 실행된다는 점이다
# 제너레이터 함수가 반환되면 순환을 종료한다.
# 하지만 일반적으로 순환에 사용하는 for문이 상세내역을 책임지기 때문에 우리가 직접적으로 신경쓰지 않아도 된다.

# 4.4 이터레이터 프로토콜 구현
# 문제
# 순환을 지원하는 객체를 만드는데, 이터레이터 프로토콜을 구현하는 쉬운 방법이 필요하다
# 해결
# 객체에 대한 순환을 가장 쉽게 구현하는 방법은 제너레이터 함수를 사용하는 것이다.
# 레시피 4.2에서 트리구조를 표현하기 위해 Node 클래스를 사용했다.
# 노드를 깊이-우선 패턴으로 순환하는 이터레이터를 구현하고 싶다면 다음 코드를 참고하자
class Node:
    def __init__(self,value):
        self._value = value
        self._children = []
    def __repr__(self):
        return 'Node({!r})'.format(self._value)
    def add_child(self,node):
        self._children.append(node)
    def __iter__(self):
        return iter(self._children)
    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()

#예제)
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))
    for ch in root.depth_first():
        print(ch) # Node(0), Node(1), Node(3), Node(4), Node(2), Node(5) 출력
# 토론
# 파이썬의 이터레이터 프로토콜은 __iter__()가 __next__() 메소드를 구현하고 종료를 알리기 위해 StopIteration 예외를
# 사용하는 특별 이터레이터 객체를 반환하기를 요구한다.
# 하지만 이런 객체를 깔끔하게 구현하기가 쉽지 않다. 예를 들어, 다음 코드는 관련 이터레이터 클래스를 사용한
# depth_first() 메소드의 대안 구현법을 보여준다
class Node:
    def __init__(self,value):
        self._value = value
        self._children = []
    def __repr__(self):
        return 'Node({!r})'.format(self._value)
    def add_child(self,node):
        self._children.append(node)
    def __iter__(self):
        return iter(self._children)
    def depth_first(self):
        return DepthFirstIterator(self)

class DepthFirstIterator(object):
    '''
    Depth-first traversal
    '''

    def __init__(self, start_node):
        self._node = start_node
        self._children_iter = None
        self._child_iter = None
    def __iter__(self):
        return self
    def __next__(self):
        # 막 시작했다면 자신을 반환한다. 자식에 대해서 이터레이터를 생성한다
        if self._children_iter is None:
            self._children_iter = iter(self._node)
            return self._node
        # 반면 자식을 처리 중이라면 다음 아이템을 반환한다
        elif self._child_iter:
            try:
                nextchild = next(self._child_iter)
                return nextchild
            except StopIteration:
                self._child_iter = None
                return next(self)
        # 다음 자식으로 진행하고 순환을 시작한다
        else:
            self._child_iter = next(self._children_iter).depth_first()
            return next(self)
# DepthFirstIterator 클래스는 제너레이터를 사용한 것과 동일하게 동작한다
# 하지만 순환하는 동안 생기는 복잡한 상황을 처리하기 위해 코드가 꽤 지저분하다.
# 사실 아무도 이런 복잡한 코드를 작성하고 싶지 않기에 이터레이터를 제너레이터로 정의하고 그걸로 만족하도록 하자

# 4.5 역방향 순환
# 문제
# 시퀀스 아이템을 역방향으로 순환하고 싶다.
# 해결
# 내장 함수 reversed()를 사용한다.
a = [1,2,3,4]
for x in reversed(a):
    print(x) # 4,3,2,1 출력
# 역방향 순환은 객체가 __reversed__() 메소드를 구현하고 있거나 크기를 알 수 있는 경우에만 가능하다
# 두 조건 중에서 아무것도 만족하지 못하면 객체를 먼저 리스트로 변환해야 한다
# 파일을 거꾸로 출력하기
f = open(r'C:\Users\Won Tae CHO\Desktop\Python_data\Cosmetics3.csv')
for line in reversed(list(f)):
    print(line)
# 하지만 순환 가능 객체를 리스트로 변환할 때 많은 메모리가 필요하다는 점은 주의해야 한다
# 토론
# __reversed__() 메소드를 구현하면 사용자 정의 클래스에서 역방향 순환이 가능하다는 점을 많은 프로그래머들이 모르고 있다
class Countdown:
    def __init__(self,start):
        self.start= start
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

    # 역방향 순환
    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1

count = Countdown()
print(count.__iter__())
print(count.__reversed__())

# 역방향 이터레이터를 정의하면 코드를 훨씬 효율적으로 만들어 주고, 데이터를 리스트로 변환하고 순환하는 수고를 덜어준다
# 4.6 추가 상태를 가진 제너레이터 함수 정의
# 문제
# 제너레이터 함수를 정의하고 싶지만, 사용자에게 노출할 추가적인 상태를 넣고 싶다
# 해결
# 사용자에게 추가 상태를 노출하는 제너레이터를 원할 때, __iter__() 메소드에 제너레이터 함수 코드를 넣어서 쉽게
# 클래스로 구현할 수 있다는 점을 기억하자
from collections import deque
class linehistory:
    def __init__(self,lines,histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)
    def __iter__(self):
        for lineno,line in enumerate(self.lines,1):
            self.history.append((lineno,line))
            yield line
    def clear(self):
        self.history.clear()
# 이 클래스를 사용하려면 일반 제너레이터 함수처럼 대해야 한다. 하지만 인스턴스를 만들기 때문에 history 속성이나
# clear() 메소드 같은 내부 속성에 접근할 수 있다
with open(r'C:\Users\Won Tae CHO\Desktop\Python_data\dept.csv') as f:
    lines = linehistory(f)
    for line in lines:
        if 'DALLAS' in line:
            for lineno,hline in lines.history:
                print('{}:{}'.format(lineno,hline),end='')
# 토론
# 제너레이터를 사용하면 모든 작업을 함수만으로 하려는 유혹에 빠지기 쉽다.
# 만약 제너레이터 함수가 프로그램의 다른 부분과 일반적이지 않게 상호작용해야 할 경우 코드가 꽤 복잡해질 수 있다
# 이럴때는 앞에서 본 대로 클래스 정의만을 사용한다
# 제너레이터를 __iter__() 메소드에 정의한다고 해도 알고리즘을 작성하는 방식에는 아무런 변화가 없다. 클래스의 일부라는 점으로 인해
# 사용자에게 속성과 메소드를 쉽게 제공할 수 있다
# for 문 대신 다른 기술을 사용해서 순환을 한다면 iter()를 호출할때 추가적으로 작업을 해야 할 필요가 생기기도 한다
