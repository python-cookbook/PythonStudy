


################################  3.11 임의의 요소 뽑기  ####################################


# 문제 - 시퀀스에서 임의의 아이템을 고르거나 난수를 생성하고 싶다면

# 해결 - random 모듈에는 이 용도에 사용할 수 있는 많은 함수가 있다.
# 예를 들어 시퀀스에서 임의의 아이템을 선택하려면 random.choice()를 사용한다.

import random
values = [1,2,3,4,5,6]
print(random.choice(values)) # -> 랜덤수 출력됨

#임의의 아이템을 n 개 뽑아서 사용하고 버릴 목적이라면 random.sample()을 사용한다.

print(random.sample(values, 2))
# [2, 4]
print(random.sample(values, 2))
# [5, 4]
print(random.sample(values, 3))
# [6, 5, 1]

# 단순히 시퀀스의 아이템을 무작위로 섞으려면 random.shuffle()을 사용한다.

random.shuffle(values)
print(values)
# [3, 5, 2, 4, 6, 1]

# 임의의 정수를 생성하려면 random.randint()를 사용한다.

print(random.randint(0,10))
# 4
print(random.randint(0,10))
# 3
print(random.randint(0,10))
# 9
#.......


# 0과 1 사이의 균등 부돝 소수점 값을 생성하려면 random.random()을 사용한다.

print(random.random())
# 0.05898193024208498

print(random.random())
# 0.49666110029839994


# n 비트로 표현된 정수를 만들기 위해서는 random.getrandbits()를 사용한다.
print(random.getrandbits(200))
# 167033549593234300436139178263489492866200989029767797061045


#random 모듈은 Mersenne Twister 알고리즘을 사용해 난수를 발생시킨다. 이 알고리즘은 정해진 것이지만,
#random.seed() 함수로 시드값을 바꿀 수도 있다.

random.seed() # 시스템 시간이나 os.urandom() 시드
random.seed(12345) # 주어진 정수형 시드
random.seed(b'bytedata') # 바이트 데이터 시드

# 앞에 나온 기느 오이에, random() 에는 유니폼, 가우시안, 확률 분포 관련 함수도 포함되어 있다.
# random.uniform() 은 균등 분포 숫자를 계산하고
# random.gause() 는 정규 분포 숫자를 계산한다.

# random() 의 함수는 암호화 관련 프로그램에서 사용하지 말아야 한다!!! 그런 기능이 필요하다면 ssl모듈을 사용하자



################################ 3.12 시간 단위 변환 ####################################


# 문제 - 날짜를 초로, 시간을 분으로 처럼 시간 단위 변환을 해야 한다.

# 해결 - 단위 변환이나 단위가 다른 값에 대한 계산을 하려면 datetime 모듈을 사용한다.
# 예를 들어 시간의 간격을 나타내기 위해서는 timedelta 인스턴스를 생성한다.

from datetime import timedelta
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c = a + b
# c = (days=2, hours=10.5) 이렇게 되겠징!!

print(c.days)
#2
print(c.seconds)
# 37800
print(c.seconds / 3600)
# 10.5
print(c.total_seconds()/3600)
# 58.5


# 특정 날짜와 시간을 표현하려면 datetime  인스턴스를 만들고 표준 수학 연산을 한다.

from datetime import datetime
a = datetime(2012, 9, 23)
print(a+timedelta(days=10))
# 2012-10-03 00:00:00

b = datetime(2012, 12, 21)
d = b - a
print(d.days)
# 89

now = datetime.today()
print(now)
# 2017-05-25 13:39:46.273311
print(now + timedelta(minutes=10))
# 2017-05-25 13:50:15.591035
print(now + timedelta(hours=10))
# 2017-05-25 23:41:11.793171

# 계산을 할 때는 datetime 이 윤년을 인식한다는 점에 주목하자!!!

a = datetime(2012, 3, 1)
b = datetime(2012, 2, 28)
print(a - b)
# 2 days, 0:00:00

print((a-b).days)
# 2

c = datetime(2013, 3, 1)
d = datetime(2013, 2, 28)
print((c-d).days)
#1


a = datetime(2012,9,23)
a + timedelta(months = 1)  #-> 에러남

from dateutil.relativedelta import relativedelta

#a + relativedelta(months=1)
#datetime.datetime(2012, 10, 23, 0, 0)

a + relativedelta(months=+4)
# datetime.datetime(2013, 1, 23, 0, 0)


# 두 날짜 사이의 시간
b = datetime(2012, 12, 21)
d = b - a
print(d)
# 89 days, 0:00:00

print(datetime.delta(89))
#d = relativedelta(b, a)
print(d)

relativedelta(months=+2, days=+28)
#print(d.months)
#왜 에러....
#d.days




########################  3.13 마지막 금요일 날짜 구하기  ###########################

# 문제 - 한 주의 마지막에 나타난 날의 날짜를 구하는 일반적인 해결책을 만들고 싶다.
# 예를 들어 마지막 금요일이 몇 일인지 궁금하다

# 해결 = 파이썬의 datetime 모듈에 이런 계산을 도와주는 클래스와 함수가 있다.

from datetime import datetime, timedelta

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']


def get_previous_byday(dayname, start_date=None):
    if start_date is None:
        start_date = datetime.today()
    day_num = start_date.weekday()
    day_num_target = weekdays.index(dayname)
    days_ago = (7 + day_num - day_num_target) % 7
    if days_ago == 0:
        days_ago = 7
    target_date = start_date - timedelta(days=days_ago)
    return target_date



datetime.today() # For reference
#datetime.datetime(2017, 5, 26, 15, 3, 23, 523580)

get_previous_byday('Monday')
# datetime.datetime(2017, 5, 22, 15, 3, 49, 499379)

get_previous_byday('Tuesday') # Previous week, not today
# datetime.datetime(2017, 5, 23, 15, 4, 4, 302759)

get_previous_byday('Friday')
# datetime.datetime(2017, 5, 19, 15, 4, 21, 822984)


get_previous_byday('Sunday', datetime(2012, 12, 21))
# datetime.datetime(2012, 12, 16, 0, 0)


# dateutil 의 relativedelta() 를 사용한 계산은 다음과 같아

from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
d = datetime.now()
print(d)
# 2017-05-26 15:05:46.497735


# Next Friday
print(d + relativedelta(weekday=FR))
# 2017-05-26 15:05:46.497735

# Last Friday
print(d + relativedelta(weekday=FR(-1)))
# 2017-05-26 15:05:46.497735




###################### 3.14. 현재 달의 날짜 범위 찾기 #############################

# 문제 - 현재 달의 날짜를 순환해야 하는 코드가 있고, 그 날짜 범위를 계산하는 효율적인 방법이 필요하다

# 날짜를 순환하기 위해 모든 날짜를 리스트로 만들 필요가 없다. 대신 범위의 시작 날짜와 마지막 날짜만 계산하고
# datetime.timedelta 객체를 사용해서 날짜를 증가시키면 된다.

from datetime import datetime, date, timedelta
import calendar

def get_month_range(start_date=None):
    if start_date is None:
        start_date = date.today().replace(day=1)
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + timedelta(days=days_in_month)
    return (start_date, end_date)

a_day = timedelta(days=1)
first_day, last_day = get_month_range()
while first_day < last_day:
    print(first_day)
    first_day += a_day

'''
2017-05-01
2017-05-02
2017-05-03
2017-05-04
2017-05-05
2017-05-06
2017-05-07
2017-05-08
2017-05-09
2017-05-10
.....

'''



##################### 3.15 문자열을 시간으로 변환 ######################

# 문제 - 문자열 형식의 시간 데이터를 datetime 객체로 변환하고 싶다면!!

# 해결 - 파이썬의 datetime 모듈을 사용하면 상대적으로 쉽게 이 문제를 해결할 수 있다.


from datetime import datetime
text = '2012-09-20'
y = datetime.strptime(text, '%Y-%m-%d')
z = datetime.now()
diff = z - y
print(diff)
# 1709 days, 15:59:32.938441


#datetime.strftime 메소드는 네자리 연도 표시를 위한 %Y, 두자리 월 표시를 위한 %m 과 같은 서식을 지원한다.

print(z)
# 2017-05-26 15:59:32.938441

nice_z = datetime.strftime(z, '%A %B %d, %Y')
print(nice_z)
# Friday May 26, 2017


# strftime() 은 실행속도가 느릴 수 있다. 날짜 형식을 정확히 알고 있다면 해결책을 직접 구현하는 것이 더 유리하다
# 예를들어 'YYYY-MM-DD' 형식이라면

from datetime import datetime
def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))




########################## 3.16. 시간대 관련 날짜 처리 ###############################

# 문제 - 다른 나라의 다른 시간대

# 시간대와 관련된 거의 모든 문제는 pytz 모듈로 해결한다. 이 패키지는 Olson 시간 데이터베이스를 제공한다.
# pytz 는 주로 datetime 라이브러리에서 생성한 날짜를 현지화할 때 사용한다.

# 예를 들어 시카고 시간은 다음과 같이 표현한다.

from datetime import datetime
from pytz import timezone
d = datetime(2012, 12, 21, 9, 30, 0)
print(d)
# 2012-12-21 09:30:00


# 시카고에 맞게 현지화
central = timezone('US/Central')
loc_d = central.localize(d)
print(loc_d)
# 2012-12-21 09:30:00-06:00


# 날짜를 현지화하고 나면, 다른 시간대로 변환할 수 있다.
# 방갈로르의 동일 시간을 구하려면 다음과 같이 한다.

# 방갈로르 시간으로 변환
bang_d = loc_d.astimezone(timezone('Asia/Kolkata'))
print(bang_d)
# 2012-12-21 21:00:00+05:30


# 변환한 날짜에 산술 연산을 하려면 서머타임제 드을 알고 있어야 한다. 이를 고려하지 않으면 계산 결과가 잘못나옴

d=datetime(2013, 3, 10, 1, 45)
loc_d = central.localize(d)
print(loc_d)
#2013-03-10 01:45:00-06:00

later = loc_d + timedelta(minutes=30)
print(later)
# 2013-03-10 02:15:00-06:00

# 토론
# 현지화한 날짜를 좀 더 쉽게 다루기 위한 전략 - 모든 날짜를 UTC 시간으로 변환해 놓고 사용하는 방법

print(loc_d)

# 2013-03-10 01:45:00-06:00

utc_d = loc_d.astimezone(pytz.utc)
print(utc_d)
# 빨간줄!!!! 왜?????


# utc 에서는 서머타임과 같은 자잘한 문제를 신경쓰지 않아도 된다. 산술연산을 해도 문제가 없다
# 현지화 시간을 출력해야 한다면 모든 계산을 마친후에 원하는 시간대로 변환한다.


later_utc = utc_d + timedelta(minutes=30)
print(later_utc.astimezone(central))



#########################################################################
#chapter 4. 이터레이터와 제너레이터
#########################################################################

# 객체 순환(iteration)은 파이썬의 강력한 기능 중 하나이다.
# 순환을 단순히 시퀀스 내부 아이템에 접근하는 방법으로 생각할 수 도 있다.
# 하지만 순환을 통해 할 수 있는 일은, 순환 객체 만들기, itertools 모듈의 순환 패턴 적용하기, 제너레이터 함수 만들기 등 여러가지가 있다.



########################## 4.1 수동으로 이터레이터 소비 ###########################

# 문제 - 순환 가능한 아이템에 접근할때, for 순환문을 사용하고 싶지 않다면

# 해결 - 수동으로 이터레이터를 소비하려면 next() 함수를 사용하고 StopIteration 예외를 처리하기 위한 코드를 직접 작성한다.
# 아래는 파일에서 줄을 읽는 코드


with open('c:/data/...') as f:
    try:
        while True:
            line = next(f)
            print(line, end='')
    except StopIteration:
        pass



# 일반적으로 StopIteration은 순환의 끝을 알리는 데 사용한다. \
# 하지만 next()를 수동으로 사용한다면 none 과 같은 종료 값을 반환하는 데 사용할 수도 있다.

with open('c:/data/...') as f:
    while True:
        line = next(f, None)
        if line is None:
            break

        print(line, end='')


#토론

# 대개의 경우, 순환에 for 문을 사용하지만 보다 더 정교한 조정이 필요한 때도 있다.
# 기저에서 어떤 동작이 일어나는지 정확히 알아 둘 필요가 있다.
# 다음 상호작용하는 예제를 통해 순환하는 동안 기본적으로 어떤 일이 일어나는지 알아보자.


items = [1,2,3]

# 이터레이터 얻기
it = iter(items)  # items.__iter__() 실행

# 이터레이터 실행
next(it)          # it.__nex__() 실행
#1

next(it)
#2

next(it)
#3

next(it)
'''
  File "<ipython-input-25-a0d1ced6d968>", line 20, in <module>
    next(it)
StopIteration

'''



########################## 4.2 델리게이팅 순환 ###########################

# 리스트, 튜플 등 순환 가능한 객체를 담은 사용자 정의 컨테이너를 만들었다.
# 이 컨테이너에 사용 가능한 이터레이터(iterator) 를 만들고 싶다.

# 해결 - 일반적으로 컨테이너 순환에 사용할 __inter__() 메소드만 정의해 주면 된다.


class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

# Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    # Outputs Node(1), Node(2)
    for ch in root:
        print(ch)

# 이 코드에서 __inter__() 가 실제 순환을 수행하기 위한 __next__() 메소드를 구현하는 특별 이터레이터 객체를
# 반환하기를 요구한다.
# 만약 다른 컨테이너에 들어 있는 내용물에 대한 순환이 해야 할 작업의 전부라면, 이터레이터의 동작 방식을 완전히
# 이해할 필요는 없다. 이때는 요청 받은 순환을 다음으로 전달하기만 하면 된다.

#iter() 함수에 대한 사용은 코드를 깔끔하게 하는 지름길과 같다. iter(s) 는 단순히 s.__iter__() 를 호출해서 이터레이터를 반환하는데,
# 이는 len(s)가 s.__len__() 을 호출하는 것과 같은 방식이다.




############################ 4.3. 제너레이터로 새로운 순환 패턴 생성 ##############################

# 문제 : 내장함수 range(), reversed() 와는 다른 동작을 하는 순환 패턴을 만들고 싶다.

# 해결 : 새로운 순환 패턴을 만들고 싶다면 제너레이터 함수를 사용해서 정의해야 된다.


def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

# 이런 함수를 사용하려면, for 순환문이나 순환 객체를 소비하는 다른 함수 sum(), list() 등을 사용한 순환을 해야 한다.

for n in frange(0, 4, 0.5):
    print(n)

'''
0
0.5
1.0
1.5
2.0
2.5
3.0
3.5
'''

list(frange(0,1,0.125))
# [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]

# 내부의 yield 문의 존재로 인해 함수가 제너레이터가 되었다. 일반 함수와는 다르게 제너레이터는 순환에 응답하기 위해 실행된다.
# 이런 함수가 어떻게 동작하는지 다음 예를 통해 알아보자.

def countdown(n):
    print("Starting to count from", n)
    while n >0:
        yield n
        n-= 1
    print('Done! ')

# 제너레이터 생성, 아무런 출력물이 없음에 주목한다.

c = countdown(3)

c
# <generator object countdown at 0x0000000004C20830>

# 값을 만들기 위한 첫 번째 실행
next(c)
#Starting to count from 3
#Out[30]:
#3

# 다음 값을 위한 실행
next(c)
#2

# 다음 값을 위한 실행
next(c)
#1

# 다음 값을 위한 실행(순환 종료)
next(c)

'''
Done! 
Traceback (most recent call last):
  File "C:\Users\Administrator\Anaconda3\lib\site-packages\IPython\core\interactiveshell.py", line 2881, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-33-73b012f9653f>", line 1, in <module>
    next(c)
StopIteration

'''

# 중요한 점은 제너레이터 함수가 순환에 의한 "다음" 연산에 응답하기 위해서만 실행된다는 점이다.
# 제너레이터 함수가 반환되면 순환을 종료한다.




#############################  4.4. 이터레이터 프로토콜 구현  ###############################

# 순환을 지원하는 객체를 만드는데, 이터레이터 프로토콜을 구현하는 쉬운 방법이 필요하다.

# 해결 - 객체에 대한 순환을 가장 쉽게 구현하는 방법은 제너레이터 함수를 사용하는 것이다.
# 레시피 4.2 에서 트리 구조를 표현하기 위해 node 클래스를 사용했다.
# 노드를 깊이 - 우선 패턴으로 순환하는 이터레이터를 구현하고 싶다면 다음 코드를 참고한다.


class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()

# 예제

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
        print(ch)

# 이 코드에서 depth_first() 메소드는 지고간저긍로 읽고 이해할 수 있다. 처음에는 자기 자신을 만들고(yield)
# 그 다음에는 자식을 순환한다.
# 이때 그 자식은 depth_first() 메소드로 아이템을 만든다.



# 토론

# 파이썬의 이터레이터 프로토콜은 __iter__() 가 __next__() 메소드를 구현하고 종료를 알리기 위해 StopIteration 예외를 사용하는
#  특별 이터레이터 객체를 반환하기르 ㄹ요구한다.
# 다음 코드는 관련 이터레이터 클래스를 사용한 depth_first() 메소드의 대안 구현법을 보여준다.




class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, other_node):
        self._children.append(other_node)

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
        # Return myself if just started; create an iterator for children
        if self._children_iter is None:
            self._children_iter = iter(self._node)
            return self._node
        # If processing a child, return its next item
        elif self._child_iter:
            try:
                nextchild = next(self._child_iter)
                return nextchild
            except StopIteration:
                self._child_iter = None
                return next(self)
        # Advance to the next child and start its iteration
        else:
            self._child_iter = next(self._children_iter).depth_first()
            return next(self)

# DepthFirstIterator 클래스는 제너레이터를 사용한 것과 동일하게 동작한다. 하지만 순환하는 동안 생기는
# 복잡한 상황을 처리하기 위해 코드가 꽤 지저분하다.




#################################  4.5. 역방향 순환  #####################################

# 문제 - 시퀀스 아이템을 역방향으로 순환하고 싶다면

# 해결 - 내장함수 reversed() 를 사용한다.



a = [1, 2, 3, 4]
for x in reversed(a):
    print(x)

'''
4
3
2
1
'''


# 역방향 순환은 객체가 __reversed__() 특별 메소드를 구현하고 있거나 크기를 알 수 있는 경우에만 가능하다.
# 두 조건 중 아무것도 만족하지 못하면 객체를 먼저 리스트로 변환해야 한다.

# 파일을 거꾸로 출력하기

f = open('somefile')
for line in reversed(list(f)):
    print(line, end='')


# 하지만 순환 가능한 객체를 리스트로 변환할 때 많은 메모리가 필요하다는 점은 주의!!


# 토론
# __reversed__() 메소드를 구현하면 사용자 정의 클래스에서 역방향 순환이 가능하다는 점을 많은 프로그래머들이 모르고 있다.


class Countdown:
    def __init__(self, start):
        self.start = start

    # Forward iterator
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

    # Reverse iterator
    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1

for rr in reversed(Countdown(30)):
    print(rr)
for rr in Countdown(30):
    print(rr)


# 역방향 이터레이터를 정의하면 코드를 훨씬 효율적으로 만들어 주고, 데이터를 리스트로 변환하고 순환하는 수고를 덜어준다.




####################  4.6. 추가 상태를 가진 제너레이터 함수 정의  ########################


# 문제 - 제너레이터 함수를 정의하고 싶지만, 사용자에게 노출할 추가적인 상태를 넣고 싶다.

# 해결 - 사용자에게 추가 상태를 노출하는 제너레이터를 원할 때, __iter__() 메소드에 제너레이터 함수 코드를 넣어서
# 쉽게 클래스로 구현할 수 있다느 점을 기억하자.


from collections import deque

class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()

# 이 클래스를 사용하려면 일반 제너레이터 함수처럼 대해야 한다. 하지만 인스턴스를 만들기 때문에 history 속성이나
# clear() 메소드 같은 내부 속성에 접근할 수 있다.


with open('somefile.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')


# 제너레이터를 사용하면 모든 작업을 함수만으로 하려는 유혹에 빠지기 쉽다.
# 만약 제너레이터 함수가 프로그램의 다른 부분과 일반적이지 않게 상호작용해야 할 경우 코드가 꽤 복잡해질 수 있다..

f = open('somefile.txt')
lines = linehistory(f)
next(lines)
#Traceback (most recent call last):
#    File "<stdin>", line 1, in <module>
#TypeError: 'linehistory' object is not an iterator

# Call iter() first, then start iterating
it = iter(lines)
next(it)
#'hello world\n'
next(it)
#'this is a test\n'








