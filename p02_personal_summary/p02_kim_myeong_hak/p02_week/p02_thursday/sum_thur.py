'''
#3.11 임의의 요소 뽑기

import random
values = [1, 2, 3, 4, 5, 6]

print(random.choice(values))

#선택된 항목에서 N개의 항목을 sampling 하기 위해서는 대신 random.sample() 메서드를 사용합니다.

print(random.sample(values,2))
print(random.sample(values,3))


#단순히 시퀀스의 아이템을 무작위로 섞으려면 random.shuffle()을 사용한다.
random.shuffle(values)
print(values)


#임의의 정수를 생성하려면 random.randint()를 사용한다.
print(random.randint(0,10))

#0과 1사이의 균등 부동 소수점 값을 생성하려면 random.random()을 사용한다.

print(random.random())

#N비트로 표현된 정수를 만들기 위해서는 random.getranbits()를 사용한다.
print(random.getrandbits(200))

#D
#random 모듈은 Mersenne Twister Algorithm을 사용하여 난수를 계산합니다. 이는 결정적(deterministic) 알고리즘이지만, random.seed()함수를 사용함으로써 초기 seed를 변경할 수 있습니다.

random.seed()               #시스템 시간이나 os.urandom() 시드
random.seed(12345)          #주어진 정수형 시드
random.seed(b'bytedata')    #바이트 데이터 시드

#3.12 시간 단위 변환

#Q 일 수를 초로, 시간을 분으로 하는 등 간단한 시간 변환을 해야하는 코드가 있습니다.
#A 다른 시간 단위를 포함하는 변환과 계산을 수행하기 위해서는 datetime 모듈을 사용합니다. 예를 들면 시간 간격을 표현하기 위해 timedelta 인스턴스를 만듭니다.

from datetime import timedelta
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c = a + b
print(c.days)
#2
print(c.seconds)
#37800
print(c.seconds / 3600)
#10.5
print(c.total_seconds() / 3600)
#58.5


# 특정 날짜와 시간을 표현하려면 datetime 인스턴스를 만들고 표준 수학 연산을 한다.

from datetime import datetime
a = datetime(2012, 9, 23)
print(a + timedelta(days=10))
#2012-10-03 00:00:00
b = datetime(2012, 12, 21)
d = b - a
print(d.days)
#89
now = datetime.today()
print(now)
#2017-05-24 17:41:36.579554
print(now + timedelta(minutes=10))
#2017-05-24 17:51:36.579554

#계산을 할 때는 , datetime이 윤년을 인식한다는 점에 주목하자.

a = datetime(2012, 3, 1)
b = datetime(2012, 2, 28)
print((a - b).days)
#2
c = datetime(2013, 3, 1)
d = datetime(2013, 2, 28)
print((c - d).days)
#1

#D 대부분의 날짜, 시간 계산 문제는 datetime 모듈로 해결할 수 있다. 시간대나, 퍼지 시계 범위, 공휴일 계산 등의 더욱 복잡한 날짜 계산이 필요하다면 dateutil모듈을 알아보자.
#대부분의 비슷한 시간 계산은 dateutil.relativedelta() 함수로 수행할 수 있다. 하지만 한 가지 주목할 만한 기능으로 달을 처리하기 위해 차이( 그리고 서로 다른 날짜 차이)를 채워주는 것이 있다.

a = datetime(2012, 9, 23)
a + timedelta(months=1)
#TypeError: 'months' is an invalid keyward argument for this functions

from dateutil.relativedelta import relativedelta
a = relativedelta(months=+1)
print(a)
#datetime.datetime(2012, 10, 23, 0, 0)
a += relativedelta(months=+4)
print(a)
#datetime.datetime(2013, 1, 23, 0, 0)

#두 날짜 사이의 시간
b = datetime(2012, 12, 21)
d = b - a
print(d)
datetime.delta(89)
d = relativedelta(b, a)
print(d)
relativedelta(months=+2, days=+28)
print(d.months)
#2
print(d.days)
#28

#3.13 마지막 금요일 날짜 구하기
#한 주의 마지막에 나타난 날의 날짜를 구하는 일반적인 해결책을 만들고 싶다. 예를들어 마지막 금요일이 며칠인지 궁금하다.

#A
#파이썬의 datetime 모듈에 이런 계산을 도와 주는 클래스와 함수가 있다. 이 문제를 해결 하기 위한 괜찮은 코드는 다음과 같다.

from datetime import datetime, timedelta

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

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

print(get_previous_byday('Monday'))
#인터프리터 세션에서 앞의 코드를 사용한 결과는 다음과 같다.
datetime.today()                #참고용
get_previous_byday('Monday')
get_previous_byday('Tuesday')   #오늘이 아닌 저번주
get_previous_byday('Friday')

#d

from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
d=datetime.now()
print(d)
#2017-05-24 17:58:42.194276


# 다음 금요일
print(d + relativedelta(weekday=FR))
#2017-05-26 17:58:42.194276


# 마지막 금요일
print(d + relativedelta(weekday=FR(-1)))
#2017-05-19 17:58:42.194276

#3.14 현재 달의 날짜 범위 찾기
#Q 현재 달의 날짜를 순환해야 하는 코드가 있고, 그 날짜 범위를 계산하는 효율적인 방법이 필요하다.

#날짜를 반복하는 것은 미리 모든 날짜의 list를 작성할 필요성이 없습니다. 다만 시작과 종료 날짜를 해당 범위에서 계산할 수 있고 그 때 datetime을 사용합니다. timedelta 객체는 날짜를 증가시킬 수 있습니다.
#다음은 datetime 객체를 사용하는 함수이며, 해당 월의 처음 날짜와 다음 달의 시작 일을 포함한 tuple을 반환합니다.
from datetime import datetime, date, timedelta
import calendar

def get_month_range(start_date=None):
    if start_date is None:
        start_date = date.today().replace(day=1)
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + timedelta(days=days_in_month)
    return(start_date, end_date)

#이를 통해 날짜 범위를 반복하는 것이 매우 간단해 집니다.


a_day = timedelta(days=1)
first_day, last_day = get_month_range()
while first_day < last_day:
    print(first_day)
    first_day += a_day

#D

def date_range(start, stop, step):
    while start < stop:
        yield start
        start += step

#사용 예제
for d in date_range(datetime(2017, 5, 1), datetime(2017, 6, 1), timedelta(hours=6)):
    print(d)

#3.15 문자열을 시간으로 변환
#문자열 형식의 시간 데이터를 datetime 객체로 변환하고 싶다.

#A 파이썬의 datetime 모듈을 사용하면 상대적으로 쉽게 이 문제를 해결할 수 있다.

from datetime import datetime
text = '2017-05-01'
y = datetime.strptime(text, '%Y-%m-%d')
z = datetime.now()
diff = z - y
print(diff)

#datetime.striptime() 메소드는 네 자리 연도 표시를 위한 %Y, 두 자리 월 표시를 위한 %m과 같은 서식을 지원한다. 또한 datetime 객체를 문자열로 표시하기 위해서 이 서식을 사용할 수 있다.
#예를 들어 datetime 객체를 생성하는 코드가 있는데, 이를 사람이 이해하기 쉬운 형태로 변환하고자 한다면 다음 코드를 사용한다.


print(z)
nice_z = datetime.strftime(z, '%A %B %d, %Y')
print(nice_z)
#'Wednesday May 24, 2017'

#순수 Python으로 쓰여지고 모든 종류의 system locale setting을 다루기에 사실 때문에
# strptime()의 성능이 가끔 기대한 것 보다 훨씬 좋지 않을 수도 있다는 점을 주목해야합니다.
# 만약 코드와 알고있는 정밀한 형식에서 많은 양의 날짜를 parsing 해야 한다면 커스텀 해결책으로 대신하여 아마도 훨씬 더 나은 성능을 얻게 될 것입니다.
# 예를 들어 날짜가 YYYY-MM-DD 형태로 되어 있는 것을 알고 있었다면 함수를 다음과 같이 쓸 수 있을 것입니다.


from datetime import datetime
def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))

#위의 방식이 datetime.strptime() 을 사용하는 것보다 대략 7배 가량 빨랐다.


#3.16 시간대 관련 날짜 처리

#Q 시카고 시간으로 2012년 12월 21일 오전 9시 30분에 화상 회의가 예정되어있다. 그렇다면 인도의 방갈로르에 있는 친구는 몇시에 회의실에 와야 할까?


from datetime import datetime
from pytz import timezone

d = datetime(2012, 12, 21, 9, 30, 0)
print(d)

#시카고에 맞게 현지화
central = timezone('US/Central')
loc_d = central.localize(d)
print(loc_d)

# 날짜를 현지화하고 나면, 다른 시간대로 변환할 수 있다. 방갈로르의 동일 시간을 구하려면
# 방갈로르의 시간으로 변환
bang_d = loc_d.astimezone(timezone('Asia/Kolkata'))
print(bang_d)

#변환한 날짜에 산술 연산을 하려면 서머타임제 등을 알고 있어야 한다. 예를 들어 2013년 미국에서 표준 서머타임은 3월 13일 오전 2시에 시작한다.
#이를 고려하지 않고 계산하면 계산 결과가 잘못된다.

d = datetime(2013, 3, 10, 1, 45)
loc_d = central.localize(d)
print(loc_d)        # 2013-03-10 01:45:00-06:00
later = loc_d + timedelta(minutes=30)
print(later)        # 2013-03-10 02:15:00-06:00 틀림!


#답이 틀렸는데 이는 한 시간이 생략된 서머타임을 고려하지 않았기 때문이다. 이를 수정하려면 normalize()메소드를 사용한다.

from datetime import timedelta
later = central.normalize(loc_d + timedelta(minutes=30))
print(later)
#2013-03-10 01:45:00-06:00

#D
print(loc_d)        # 2013-03-10 01:45:00-06:00
utc_d = loc_d.astimezone(pytz.utc)
print(utc_d)        # 2013-03-10 07:45:00+00:00

#UTC에서는 일광 절약 시간과 연관된 문제나 다른 문제들을 염려하지 않아도 됩니다. 그러므로 간단히 표준 날짜 계산을 이전과 같이 수행할 수 있습니다.
# 지역화된 시간에서 날짜를 출력해야 한다면, 그 다음에 적절한 time zone으로 바꾸기만 하면 됩니다.

later_utc = utc_d + timedelta(minutes=30)
print(later_utc.astimezone(central))
# 2013-03-10 03:15:00-05:00


print(pytz.country_timezones['IN'])
#['Asia/Kolkata']

#chap 4 이터레이터와 제너레이터
#4.1 수동으로 이터레이터 소비


#iterable 객체를 수동으로 consume(소비)하려면 next() 함수를 사용하고 StopIteration
#예외를 catch하는 코드를 직접 작성 합니다. 예를 들어 이 예제는 파일로부터 수동으로 라인을 읽습니다.

with open('/etc/passwd') as f:
    try:
        while True:
            line = next(f)
            print(line, end='')
    except StopIteration:
        pass

#일반적으로 StopIteration은 iteration의 끝을 나타낼 때(signal) 사용됩니다.
#하지만 next()를 수동적으로 사용하게 될 경우(위와 같이) None과 같은 끝을 나타내는 값(terminating value)을 대신 반환하도록 해야합니다.

with open('/etc/passwd') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
        print(line, end='')

#D
#대개의 경우, 순환에 for 문을 사용 하지만 보다 더 정교한 조절이 필요한 때도 있다.
#기저에서 어떤 동작일 일어나는지 정확히 알아둘 필요가 있다.


items = [1, 2, 3]
# 이터레이터 얻기
it = iter(items)        # items.__iter__() 실행
# 이터레이터 실행
next(it)                # it.__next__() 실행
#1
next(it)
#2
next(it)
#3
next(it)
StopIteration

#4.2 델리게이팅 순환
#Q 리스트, 튜플 등 순환 가능한 객체를 담은 사용자 정의 컨테이너를 만들었다.
#이 컨테이너에 사용 가능한 이터레이터를 만들고 싶다.

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self.children.append(node)

    def __iter__(self):
        return iter(self._children)

#예제
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)
    # Node(1), Node(2) 출력

#D
#파이썬의 이터레이터 프로토콜은 __iter__()가 실제 순환을 수행하기 위한 __next__() 메소드를 구현하는 특별 이털이터 객체를 반환하기를 요구한다.

'''
#4.3 제너레이터로 새로운 순환 패턴 생성
#내장함수 range(), reversed() 와는 다른 동작을 하는 순환 패턴을 만들고 싶다.
#새로운 순환 패턴을 만들고 싶다면, 제너레이터 함수를 사용해서 정의해야 된다

def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

#이런 함수를 사용하려면, for 순환문이나 순환 객체를 소비하는 다른 함수 sum(),list()를 사용한 순환을 해야한다.

for n in frange(0, 4, 0.5):
    print(n)
#0
#0.5
#1.0
#1.5
#2.0
#2.5
#3.0
#3.5
print(list(frange(0, 1, 0.125)))
#[0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]

#D
def countdown(n):
    print('Starting to count from', n)
    while n > 0:
        yield n
        n -= 1
    print('Done!')
#제너레이터 생성, 아무런 출력물이 없음에 주목한다.
c = countdown(3)
#값을 만들기 위한 첫 번째 실행
print(next(c))         # 첫번째 yield의 반환 값
# 3
# 값을 만들기 위한 첫번째 실행
print(next(c))
# 2
print(next(c))
# 1
#다음 값을 위한 실행 (순환 종료)
print(next(c))
# Done!
# StopIteration

#4.4 이터레이터 프로토콜 구현
#순환을 지원하는 객체를 만드는데, 이터레이터 프로토콜을 구현하는 쉬운 방법이 필요하다.

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

#예제
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    child1_1 = Node(3)
    child1_2 = Node(4)
    child2_1 = Node(5)

    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(child1_1)
    child1.add_child(child1_2)
    child2.add_child(child2_1)

    for ch in root.depth_first():
        print(ch)
    # Node(0) Node(1) Node(3) Node(4) Node(2) Node(5) 출력


#D
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
    def __init__(self, start_node):
        self._node = start_node
        self._children_iter = None
        self._child_iter = None

    def __iter__(self):
        return self

    def __next__(self):
        #막 시작했다면 자신을 반환한다. 자식에 대해서 이터레이터를 생성한다.
        if self._children_iter is None:
            self._children_iter = iter(self._node)
            return self._node

        #자식을 처리중이라면 다음 아이템을 반환한다.
        elif self._child_iter:
            try:
                nextchild = next(self._child_iter)
                return nextchild
            except StopIteration:
                self._child_iter = None
                return next(self)
        #다음 자식으로 진행하고 순환을 시작한다.
        else:
            self._child_iter = next(self._children_iter).depth_first()
            return next(self)


#4.5 역방향 순환

a = [1, 2, 3, 4]
for x in reversed(a):
    print(x)

#역방향 순환은 객체가 __reversed__() 특별 메소드를 구현하고 있거나 크기를 알 수 있는 경우에만 가능하다.
#두 조건 중에서 아무것도 만족하지 못하면 객체를 먼저 리스트로 변환해야한다

#파일을 거꾸로 출력하기
f = open('somefile')
for line in reversed(list(f)):
    print(line, end='')

#d
#reversed__() 메소드를 구현하면 사용자 정의 클래스에서 역방향 순환이 가능하다는 점을 많은 프로그래머들이 모르고 있다.

class Countdown:
    def __init__(self, start):
        self.start = start

    #순방향 순환
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

#역방향 이터레이터를 정의하면 코드를 훨씬 효율적으로 만들어주고, 데이터를 리스트로 변환하고 순환하는 수고를 덜어준다.


#4.6 추가 상태를 가진 제너레이터 함수 정의
#제너 레이터 함수를 정의하고 싶지만, 사용자에게 노출할 추가적인 상태를 넣고 싶다.

#A. 사용자에게 추가 상태를 노출하는 제너레이터를 원할 때. __iter__() 메소드에 제너레이터 함수 코드를 넣어서 쉽게 클래스로 구현할 수 있다는 점을 기억하자.

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

# 이 클래스를 사용하려면 일반 제너레이터 함수처럼 대해야 한다. 하지만 인스턴스를 만들기 때문에 history 속성이나 clear() 메소드 같은 내부 속성에 접근 할 수 있다.


with open('somefile.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')


f = open('somefile.txt')
lines = linehistory(f)
next(lines)
TypeError
#iter()를 먼저 호출하고, 순환을 시작한다.
it = iter(lines)
next(it)
#'hello world\n'
next(it)
#'this is a test\n'