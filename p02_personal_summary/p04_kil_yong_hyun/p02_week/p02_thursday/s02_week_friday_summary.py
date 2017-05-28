#  3.11 임의의 요소 뽑기
#  ▣ 문제 : 시퀀스에서 임의의 아이템을 고르거나 난수를 생성하고 싶다.
#  ▣ 해결 : random 모듈에는 이 용도에 사용할 수 있는 많은 함수가 있다.
#           예를 들어 시퀀스에서 임의의 아이템을 선택하려면 random.choice() 를 사용한다.
import random
values = [1, 2, 3, 4, 5, 6]
print(random.choice(values))

#   - 임의의 아이템을 N개 뽑아서 사용하고 버릴 목적이라면 random.sample() 을 사용한다.
print(random.sample(values, 2))

#   - 시퀀스의 아이템을 무작위로 섞으려면 random.shuffle() 을 사용한다.
random.shuffle(values)
print(values)

#   - 임의의 정수를 생성하려면 random.randint() 를 사용한다.
print(random.randint(0, 10))

#   - 0 과 1 사이의 균등 부동 소수점 값을 생성하려면 random.random() 을 사용한다.
print(random.random())

#   - N 비트로 표현된 정수를 만들기 위해서는 random.getrandbits() 를 사용한다.
print(random.getrandbits(200))

#  ▣ 토론 : random 모듈은 Mersenne Twister 알고리즘을 사용해 난수를 발생시킨다.
#           이 알고리즘은 정해진 것이지만, random.seed() 함수로 시드 값을 바꿀 수 있다.
#           random() 의 함수는 암호화 관련 프로그램에서 사용하지 말아야 한다.
#           그런 기능이 필요하다면 ssl 모듈을 사용해야 한다.
random.seed()  # 시스템 시간이나 os.urandom() 시드
random.seed(12345)  # 주어진 정수형 시드
random.seed(b'bytedata')  # 바이트 데이터 시드


#  3.12 시간 단위 변환
#  ▣ 문제 : 날짜를 초로, 시간을 분으로처럼 시간 단위 변환을 해야 한다.
#  ▣ 해결 : 단위 변환이나 단위가 다른 값에 대한 계산을 하려면 datetime 모듈을 사용한다.
#            예를 들어 시간의 간격을 나타내기 위해서는 timedelta 인스턴스를 생성한다.
from datetime import timedelta
a = timedelta(days=2, hours=6)  # days, hours 따로 동작한다.
b = timedelta(hours=4.5)
c = a + b
print(c.days, c.seconds, c.seconds/3600, c.total_seconds() / 3600)

#   - 특정 날짜와 시간을 표현하려면 datetime 인스턴스를 만들고 표준 수학 연산을 한다.
from datetime import datetime
a = datetime(2012, 9, 23)
print(a + timedelta(days=10))
b = datetime(2012, 12, 21)
d = b - a
print(d.days)
now = datetime.today()
print(now)
print(now + timedelta(minutes=10))

#   - datetime 이 윤년을 인식한다는 점에 주목하자.
a = datetime(2012, 3, 1)
b = datetime(2012, 2, 28)
print(a - b)
print((a - b).days)
c = datetime(2013, 3, 1)
d = datetime(2013, 2, 28)
print((c - d).days)

#  ▣ 토론 : 대부분의 날짜, 시간 계산 문제는 datetime 모듈로 해결할 수 있다.
#           시간대나, 퍼지 시계 범위, 공휴일 계산 등의 더욱 복잡한 날짜 계산이 필요하다면 dateutil 모듈을 알아보자.
a = datetime(2012, 9, 23)
print(a + timedelta(months=1))  # months 는 지원하지 않음

from dateutil.relativedelta import relativedelta
print(a + relativedelta(months=+1))
print(a + relativedelta(months=+4))

#   - 두 날짜 사이의 시간
b = datetime(2012, 12, 21)
d = b - a
print(d)
d = relativedelta(b, a)
print(d)
print(d.months, d.days)


#  3.13 마지막 금요일 날짜 구하기
#  ▣ 문제 : 한 주의 마지막에 나타난 날의 날짜를 구하는 일반적인 해결책을 만들고 싶다.
#           예를 들어 마지막 금요일이 며칠인지 궁금하다.
#  ▣ 해결 : 파이썬의 datetime 모듈에 이런 계산을 도와 주는 클래스와 함수가 있다.
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

print(datetime.today())
print(get_previous_byday('Monday'))
print(get_previous_byday('Tuesday'))
print(get_previous_byday('Friday'))
print(get_previous_byday('Sunday', datetime(2012, 12, 21)))

#  ▣ 토론 : 이번 레시피는 시작 날짜와 목표 날짜를 관련 있는 숫자 위치에 매핑하는 데에서 시작한다.
#            이와 같은 날짜 계산을 많이 수행한다면 python-dateutil 패키지를 설치하는 것이 좋다.
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
d = datetime.now()
print(d)

#   - 다음 금요일
print(d + relativedelta(weekday=FR))

#   - 마지막 금요일
print(d + relativedelta(weekday=FR(-1)))


#  3.14 현재 달의 날짜 범위 찾기
#  ▣ 문제 : 현재 달의 날짜를 순환해야 하는 코드가 있고, 그 날짜 범위를 계산하는 효율적인 방법이 필요하다.
#  ▣ 해결 : 날짜를 순환하기 위해 모든 날짜를 리스트로 만들 필요가 없고, 시작과 마지막 날짜만 계산하고 datetime.timedelta
#            객체를 사용해서 날짜를 증가시키면 된다.
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

#  ▣ 토론 : 위처럼 구현할 수도 있지만 이상적으로는 generator 를 사용하면 아주 쉽게 구현할 수 있다.
def date_range(start, stop, step):
    while start < stop:
        yield start
        start += step

for d in date_range(datetime(2012, 9, 1), datetime(2012, 10, 1), timedelta(hours=6)):
    print(d)


#  3.15 문자열을 시간으로 변환
#  ▣ 문제 : 문자열 형식의 시간 데이터를 datetime 객체로 변환하고 싶다.
#  ▣ 해결 : 파이썬의 datetime 모듈을 사용하면 상대적으로 쉽게 이 문제를 해결할 수 있다.
from datetime import datetime
text = '2012-09-20'
y = datetime.strptime(text, '%Y-%m-%d')
z = datetime.now()
diff = z- y
print(diff)

#  ▣ 토론 : datetime.strptime() 메소드는 네 자리 연도 표시를 위한 %Y, 두 자리 월 표시를 위한 %m 과 같은 서식을 지원한다.

#   - datetime 객체를 생성하는 코드가 있는데, 이를 사람이 이해하기 쉬운 형태로 변환할 수 있다.
print(z)
nice_z = datetime.strftime(z, '%A %B %d, %Y')
print(nice_z)

#   - strptime() 함수는 순수 파이썬만을 사용해서 구현했고, 시스템 설정과 같은 세세한 부분을 모두 처리해야 하므로 예상보다 실행 속도가
#     느린 경우가 많다.
#     따라서 직접 구현하는 것이 속도 측면에서 훨씬 유리하다.
from datetime import datetime

def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))


#  3.16 시간대 관련 날짜 처리
#  ▣ 문제 : 시카고 시간으로 2012년 12월 21일 오전 9시 30분에 화상 회의가 예정되어 있다.
#           그렇다면 인도의 방갈로르에 있는 친구는 몇 시에 회의실에 와야 할까?
#  ▣ 해결 : 시간대와 관련 있는 거의 모든 문제는 pytz 모듈로 해결한다.
#           이 패키지는 많은 언어와 운영 체제에서 기본적으로 사용하는 Olson 시간대 데이터베이스를 제공한다.
#           pytz 는 주로 datetime 라이브러리에서 생성한 날짜를 현지화할 때 사용한다.
from datetime import datetime, timedelta
from pytz import timezone
d = datetime(2012, 12, 21, 9, 30, 0)
print(d)

#   - 시카고에 맞게 현지화.
central = timezone('US/Central')
loc_d = central.localize(d)
print(loc_d)

#   - 방갈로르 시간으로 변환.
bang_d = loc_d.astimezone(timezone('Asia/Kolkata'))
print(bang_d)

#   - 변환한 날짜에 산술 연산을 하려면 서머타임제 등을 알고 있어야 한다.
#     예를 들어 2013 년 미국에서 표준 서머타임은 3월 13일 오전 2시에 시작한다.
d = datetime(2013, 3, 10, 1, 45)
loc_d = central.localize(d)
print(loc_d)
later = loc_d + timedelta(minutes=30)
print(later)

#   - 서머타임을 고려하면 normalize() 메소드를 사용한다.
from datetime import timedelta
later = central.normalize(loc_d + timedelta(minutes=30))
print(later)

#  ▣ 토론 : 현지화된 날짜를 조금 더 쉽게 다루기 위한 한 가지 전략으로, 모든 날짜를 UTC(세계 표준 시간) 시간으로 변환해 놓고 사용하는 것이 있다.
import pytz
print(loc_d)
utc_d = loc_d.astimezone(pytz.utc)
print(utc_d)

#   - 현지화 시간을 원할 경우 모든 계산을 마친 후에 원하는 시간대로 변환한다.
later_utc = utc_d + timedelta(minutes=30)
print(later_utc.astimezone(central))

#   - 특정 국가 시간대 이름 출력. (pytz.country_timezones)
#     키 값으로 ISO 3166 국가 코드를 사용.
print(pytz.country_timezones['IN'])


# Chapter 4. 이터레이터와 제너레이터
#  4.1 수동으로 이터레이터 소비
#  ▣ 문제 : 순환 가능한 아이템에 접근할 때 for 순환문을 사용하고 싶지 않다.
#  ▣ 해결 : 수동으로 이터레이터를 소비하려면 next() 함수를 사용하고 StopIteration 예외를 처리하기 위한 코드를 직접 작성한다.
with open('files/somefile.txt', 'r') as f:
    try:
        while True:
            line = next(f)
            print(line, end='')
    except StopIteration:
        pass

with open('files/somefile.txt', 'r') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
        print(line, end='')

#  ▣ 토론 : 대개의 경우 순환에 for 문을 사용하지만 보다 더 정교한 조절이 필요한 때도 있다.
#           기저에서 어떤 동작이 일어나는지 정확히 알아둘 필요가 있다.
items = [1, 2, 3]
it = iter(items)
print(next(it))
print(next(it))
print(next(it))
print(next(it))


#  4.2 델리게이팅 순환
#  ▣ 문제 : 리스트, 튜플 등 순환 가능한 객체를 담은 사용자 정의 컨테이너를 만들었다.
#           이 컨테이너에 사용 가능한 이터레이터를 만들고 싶다.
#  ▣ 해결 : 일반적으로 컨테이너 순환에 사용할 __iter__() 메소드만 정의해 주면 된다.
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

if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)

#  ▣ 토론 : 파이썬의 이터레이터 프로토콜은 __iter__() 가 실제 순환을 수행하기 위한 __next__() 메소드를 구현하는 특별 이터레이터
#           객체를 반환하기를 요구한다.


#  4.3 제너레이터로 새로운 순환 패턴 생성
#  ▣ 문제 : 내장 함수(range(), reversed())와는 다른 동작을 하는 순환 패턴을 만들고 싶다.
#  ▣ 해결 : 새로운 순환 패턴을 만들고 싶다면, 제너레이터 함수를 사용해서 정의해야 한다.
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

for n in frange(0, 4, 0.5):
    print(n)

for n in frange(0, 1, 0.125):
    print(n)

#  ▣ 토론 : 내부의 yield 문의 존재로 인해 함수가 제너레이터가 되었다.
#           일반 함수와는 다르게 제너레이터는 순환에 응답하기 위해 실행된다.
def countdown(n):
    print('Starting to count from', n)
    while n > 0:
        yield n
        n -= 1
    print('Done!')

c = countdown(3)
print(c)

print(next(c))
print(next(c))
print(next(c))
print(next(c))


#  4.4 이터레이터 프로토콜 구현
#  ▣ 문제 : 순환을 지원하는 객체를 만드는데, 이터레이터 프로토콜을 구현하는 쉬운 방법이 필요하다.
#  ▣ 해결 : 객체에 대한 순환을 가장 쉽게 구현하는 방법은 제너레이터 함수를 사용하는 것이다.
#           노드를 깊이-우선 패턴으로 순환하는 이터레이터를 구현하고 싶다면 다음 코드를 참고한다.
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


#  4.5 역방향 순환
#  ▣ 문제 : 시퀀스 아이템을 역방향으로 순환하고 싶다.
#  ▣ 해결 : 내장 함수 reversed() 를 사용한다.
a = [1, 2, 3, 4]
for x in reversed(a):
    print(x)

#   - 역방향 순환은 객체가 __reversed__() 특별 메소드를 구현하고 있거나 크기를 알 수 있는 경우에만 가능하다.
#     두 조건 중에서 아무것도 만족하지 못하면 객체를 먼저 리스트로 변환해야 한다.
f = open('files/somefile.txt')
for line in reversed(list(f)):
    print(line, end='')

#   - 순환 가능 객체를 리스트로 변환할 때 많은 메모리가 필요하다.


#  4.6 추가 상태를 가진 제너레이터 함수 정의
#  ▣ 문제 : 제너레이터 함수를 정의하고 싶지만, 사용자에게 노출할 추가적인 상태를 넣고 싶다.
#  ▣ 해결 : 사용자에게 추가 상태를 노출하는 제너레이터를 원할 때, __iter__() 메소드에 제너레이터 함수 코드를 넣어서 쉽게 클래스로
#           구현할 수 있다.
from collections import deque

class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):  # enumerate(self.lines, 1) 함수의 출력값 : (줄 번호, 줄 내용), 1번부터 번호 출력
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()

with open('files/somefile.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')

#  ▣ 토론 : 제너레이터를 사용하면 모든 작업을 함수만으로 하려는 유혹에 빠지기 쉽다.
#           만약 제너레이터 함수가 프로그램의 다른 부분과 일반적이지 않게 상호작용해야 할 경우 코드가 꽤 복잡해질 수 있다.
#           이럴 때는 앞에서 본 대로 클래스 정의만을 사용한다.
f = open('files/somefile.txt')
lines = linehistory(f)
next(lines)  # __iter__ 메서드가 iter 객체를 리턴하지 않아 next 메소드가 호출되지 않는다.

it = iter(lines)
next(it)
next(it)