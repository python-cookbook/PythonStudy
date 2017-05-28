#=======================================================================================================================
# 3.11 임의의 요소 뽑기
# 시퀀스에서 임의의 아이템을 고르거나 난수를 생성하고 싶다
# ㄴ random.choice() 임의의 아이템 고르기
# ㄴ random.sample() 임의의 아이템 뽑고 쓰고 버리기
# ㄴ random.shuffle() 시퀀스 아이템 무작위로 섞기
#=======================================================================================================================
## random.choice()

import random
values = [1,2,3,4,5,6]
print(random.choice(values))            # 5, 3 등등 계속 출력되는 값이 바뀐다
print(random.sample(values, 2))         # [6,2].. [4,3] 임의의 아이템을 N개 뽑아서 사용하고 ...뭐지? 삭제가 아닌데..
print(random.shuffle(values))           # 쉐낏
print(values)

print(random.randint(0,10))             # 0에서 10사이의 임의의 정수 생성
print(random.random())                  # 0과 1사이의 랜덤값(소수점 값) 생성
print(random.getrandbits(200))          # N비트로 표현된 정수로 만들기 위한 random. 1597369649337954141500711372914896056318114172155102075693866

## 이 random 모듈은 메르센 트위스터 알고리즘을 사용해 난수를 발생시킴
# 이걸 바꾸려면 random.seed() 함수로 시드값을 변경할 수 있다
print(random.seed())                    # 시스템 시간이나 os.urandom()
random.seed(12345)                      # 주어진 정수형 시드
random.seed(b'bytedata')              # 바이트 데이터 시드

## 이외의 random의 기능들
# random.uniform() 균등 분포 숫자 계산용
# random.gauss()   정규 분포 숫자 계산용

## random 함수는 암호화 관련 프로그램에선 쓰지 말고(메르센 트위스터 알고리즘이 보안상 안 좋아서??), ssl.RAND_bytes()를 쓰도록 하자. 보안상 안전하다.



#=======================================================================================================================
# 3.12 시간 단위 변환
# 날짜 -> 초, 시간 -> 분
# ㄴ 단위가 다른 것에 대한 계산을 하려면, datetime 모듈 사용
#=======================================================================================================================
from datetime import timedelta
a = timedelta(days=10, hours=6)                 # days, hours에 들어간 값들은 임시값
b = timedelta(hours=4.5)
c = a + b
print(c.days)                                   # 10 근데 hours는 인식을 못하는건지.. hours만 둬 보아도 안 나온다.
print(c.seconds)                                # 37800    hours에서 연산되어져서 나온다.
print(c.seconds/3600)                           # 10.5 1시간이 3600초
print(c.total_seconds()/3600)                     # 250.5??... 곱하기는 해보면 total_seconds()가 901800이라는 건데....이건 어디서 나옴?


## 특정 날짜와 시간을 표현하려면 datetime 인스턴스를 만들고 표준 수학 연산(??)을 한다.
from datetime import datetime                  # datetime은 윤년을 인식한다
a = datetime(2012,9,23)
print(a+timedelta(days=10))

b = datetime(2012,12,21)
d = b - a
print(d.days)                                   # 89    (위의 a의 datetime인 9월 23일과 89일의 차이가 난다)

now = datetime.today()
print(now)
print(now+timedelta(minutes=10))

a = datetime(2012,3,1)
b = datetime(2012,2,28)
print((a - b).days)

c = datetime(2013,3,1)
d = datetime(2013,2,28)
print((c-d).days)                                   # 1 (c와 d의 날짜 차이가 하루)



## dateutil 모듈: 시간대(time zone)나, 퍼지 시계 범위(fuzzy time range), 공휴일 계산 등의 날짜 계산이 필요할 때 사용
from dateutil.relativedelta import relativedelta
a = datetime(2012,9,23)
print(a + relativedelta(months=+1))             # 2012-10-23 00:00:00
print(a+relativedelta(months=+4))               # 2013-01-23 00:00:00

b = datetime(2012,12,21)
d = b-a
print(d)                                        # 89 days, 0:00:00

d = relativedelta(b,a)
print(d)                                        # relativedelta(months=+2, days=+28)

print(d.months)                                 # 2
print(d.days)                                   # 28


#=======================================================================================================================
# 3.13 마지막 금요일 날짜 구하기
# 마지막 금요일이 며칠인지 궁금하다
# ㄴ datetime 모듈
#=======================================================================================================================

from datetime import datetime, timedelta
weekdays =['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def get_previous_byday(dayname, start_date=None):
    if start_date is None:                                      # 만약에 시작 날짜가 None이면
        start_date = datetime.today()                            # 오늘을 넣어준다.
    day_num = start_date.weekday()
    print(day_num)
    day_num_target = weekdays.index(dayname)
    print(day_num_target)
    days_ago = (7+day_num-day_num_target) % 7
    print(days_ago)
    if days_ago == 0:
        days_ago = 7
    target_date = start_date - timedelta(days=days_ago)
    return target_date

get_previous_byday('Saturday')

## 계산하는 방법
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
d = datetime.now()
print(d)                                                        # 2017-05-25 16:59:36.182328
print(d+relativedelta(weekday=FR))                              # 2017-05-26 16:59:36.182328
print(d+relativedelta(weekday=FR(-1)))                          # 2017-05-19 16:59:36.182328


#=======================================================================================================================
# 3.14 현재 달의 날짜 범위 찾기
# 달의 날짜를 순환해야하는 코드가 있고, 날짜 범위를 계산하는 효율적인 방법은?
# ㄴ 범위의 시작 일자와 마지막 날짜만 계산하고 datetime.timedelta 객체를 이용해서 날짜를 증가시킴
#=======================================================================================================================

## 먼저 datetime 객체로 그 달의 첫 번째 날짜와 다음 달의 시작 날짜를 반환해보자
from datetime import datetime, date, timedelta
import calendar

def get_month_range(start_date=None):
    if start_date is None:
        start_date = date.today().replace(day=1)                    # 오늘 날짜를 1일로 대체
        # print(start_date)

    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    # print(days_in_month)
    # monthrange는 월에 포함된 날짜 수와 주의 날짜를 포함한 튜플을 반환한다.
    end_date = start_date + timedelta(days=days_in_month)
    return (start_date, end_date)                             # (datetime.date(2017, 5, 1), datetime.date(2017, 6, 1))

get_month_range()

## 날짜 범위 순환하기
a_day = timedelta(days=1)
first_day, last_day = get_month_range()
while first_day < last_day:
    print(first_day)
    first_day += a_day

# 결과
# 2017-05-01
# 2017-05-02
# .... ....
# 2017-05-30
# 2017-05-31

## range()처럼 동작하는 함수 - 제너레이터 사용
def date_range(start, stop, step):
    while start < stop:
        yield start
        start += step

for date in date_range(datetime(2012,9,1),datetime(2012,10,1),timedelta(hours=6)):
    print(date)

# 2012-09-27 12:00:00
# 2012-09-27 18:00:00
# 2012-09-28 00:00:00
# 2012-09-28 06:00:00
# 2012-09-28 12:00:00


#=======================================================================================================================
# 3.15 문자열을 시간으로 변환
# 문자열 형식의 시간 데이터를 datetime 객체로 변환하고 싶다.
# ㄴ datetime 사용
#=======================================================================================================================
from datetime import datetime
text = '2017-05-20'
y = datetime.strptime(text, '%Y-%m-%d')
z = datetime.now()
diff = z - y
# print(diff)                                                # 5 days, 18:02:35.653408

nice_z = datetime.strftime(z, '%A %B %d, %Y')
print(nice_z)                                               # Thursday May 25, 2017

## 날짜 형식이 YYYY-MM-DD일때
from datetime import datetime
def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s),int(mon_s),int(day_s))

# print(parse_ymd("1999-02-11"))


#=======================================================================================================================
# 3.16 시간대 관련 날짜 처리
# time difference
# ㄴ pytz 모듈로 해결. datetime 라이브러리에서 생성한 날짜를 현지화할 때 사용
#=======================================================================================================================

from datetime import datetime
from pytz import timezone
d = datetime(2012,12,21,9,30,0)
# print(d)

## 시카고 시간
central = timezone('US/Central')
loc_d = central.localize(d)
# print(loc_d)

## 저걸 방갈로르 시간으로 바꾸려면?
bang_d = loc_d.astimezone(timezone('Asia/Kolkata'))         # 캘커타
# print(bang_d)


# 서머 타임제 다 일일이 체크하기 힘드니 아래처럼 normalize 사용
from datetime import timedelta
later = central.normalize(loc_d + timedelta(minutes=30))
# print(later)


## 모든 날짜를 UTC 시간으로 변환해놓고 사용할 수도 있다
utc_d = loc_d.astimezone(pytz.utc)
# print(utc_d)


## 기준 시간대 이름 알아내는 방법. 키 값은 ISO 3166 국가 코드를 사용해서 pytz.country_timezones 딕셔너리에서 알아내기
print(pytz.country_timezones['IN'])



#=======================================================================================================================
# 4.1 수동으로 이터레이터 소비
# 순환 가능한 아이템을 쓸 때 for loop 쓰기 시렁
# ㄴ 수동으로 iterator를 할려면 next() 함수를 쓰고, StopIteration 예외 처리를 위한 코드도 작성해야 한다.
#=======================================================================================================================
with open('/etc/passwd') as f:                      # 파일에서 줄을 읽어오는 코드
    try:
        while True:
            line = next(f)
            print(line, end='')
    except StopIteration:
        pass


##
with open('/etc/passwd') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
        print(line, end='')


## 이터레이터
items = [1,2,3]
it = iter(items)                                        # items.__iter__() execute
print(next(it))                                         # 1    it.__next__() execute
print(next(it))                                         # 2    it.__next__() execute
print(next(it))                                         # 3    it.__next__() execute
print(next(it))                                         # StopIteration 오류 뙇


#=======================================================================================================================
# 4.2 델리게이팅 순환
# 리스트, 튜플을 순환 가능한 객체를 담은 사용자 정의 컨테이너 생성. 여기에서 사용 가능한 iterator를 만들거야
# ㄴ 컨테이너 순환에 사용할 __iter__() 메소드 정의
#=======================================================================================================================
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


if __name__=='__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)                                   # Node(1)과 Node(2)를 출력

# 이 코드에서 __iter__()는 순환 요청을 _children 속성으로 전달한다.

## 파이썬의 이터레이터 프로토콜은 __iter__()가 실제 순환을 수행하기 위한 __next__() 메소드를 구현하는 특별 이터레이터
# 객체를 반환하기를 요구한다. iter(s)는 s.__iter__()를 호출해서 이터레이터를 반환한다.



#=======================================================================================================================
# 4.3 제너레이터로 새로운 순환 패턴 생성
# 내장 함수(range(), reversed())와는 다른 순환 패턴을 만들고 싶다
# ㄴ generator 함수를 정의해서 새로운 순환 패턴을 만들면 된다
#=======================================================================================================================

def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

for n in frange(0, 10, 0.5):                        # 이걸 쓸 때는 for loop이나 순환 객체를 소비하는 다른 함수
    print(n)                                         # sum(), list() 등을 사용한 순환을 해야 한다

# 결과값
# 0.5
# 1.0
# ...
# 9.0
# 9.5

def countdown(n):
    print('Starting to count from',n)
    while n > 0:
        yield n
        n -= 1
    print('Done!')

# print(countdown(10))                              # 결과값: <generator object countdown at 0x0000000004E8DD00>

c = countdown(3)                                    # Starting to count from 3
print(next(c))                                      # 3
print(next(c))                                      # 2
print(next(c))                                      # 1
print(next(c))                                      # Done!


#=======================================================================================================================
# 4.4 이터레이터 프로토콜 구현
# 객체에 대한 순환을 구현하자
# ㄴ generator func 사용. Node를 depth-first 패턴으로 순환하는 iterator를 구현하고자 한다면 아래 코드 참고
#=======================================================================================================================
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

if __name__=='__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child1.add_child(Node(5))

    for ch in root.depth_first():
        print(ch)


# 결과물
# Node(0)
# Node(1)
# Node(3)
# Node(4)
# Node(5)
# Node(2)



#=======================================================================================================================
# 4.5 역방향 순환
# 시퀀스 아이템을 역방향으로 순환
# ㄴ reversed() 내장 함수
#=======================================================================================================================
a = [1,2,3,4]
for x in reversed(a):
    print(x)

# 4
# 3
# 2
# 1

# 역방향 순환은 객체가 __reversed__() 특별 메소드를 구현하고 있거나 크기를 알 수 있는 경우에만 가능하다. 두 조건 중
# 아무것도 만족하지 못하면 객체를 먼저 리스트로 변환해야 한다

f = open('파일 링크')
for line in reversed(list(f)):
    print(line, end='')

## 역방향 이터레이터를 사용해서 순방향/역방향 순환을 할 수도 있다
class Countdown:
    def __init__(self,start):
        self.start = start

    # 순방향
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1


#=======================================================================================================================
# 4.6 추가 상태를 가진 제너레이터 함수 정의
# 사용자에게 노출할 추가적인 상태를 노출하는 제너레이터 함수를 정의하고 싶다.
# ㄴ __iter__() 메소드에 제너레이터 함수 코드를 넣어서 클래스로 구현
#=======================================================================================================================
from collections import deque

class linehistory:
    def __init__(self, lines, histlen = 3):
        self.lines = lines
        self.history = deque(maxlen = histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines,1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()

# 일반 제너레이터 함수처럼 대해도 됨. 그런데 인스턴스를 만드므로 history 속성이나 clear() 메소드같은 내부 속성에 접근가능

with open('링크.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')
