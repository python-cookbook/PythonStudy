#############################################################

# 3.11 임의의 요소 뽑기

# random 모듈

import random
values = [1,2,3,4,5]
random.choice(values) # 임의의 아이템 선택

random.sample(values, 2) # N개 뽑고 버릴 때

random.shuffle(values) # 무작위로 섞기

random.randint(0, 10) # 임의의 정수 생성

random.random() # 0~1 사이의 소수 뽑기

random.getrandbits(200) # N비트로 표현된 정수 생성

##############################################################

# 3.12 시간 단위 변환(datetime 모듈)

# 시간 간격 나타낼 때(timedelta)

from datetime import timedelta
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c = a+b
print(c.days)
## 2
print(c.seconds)
## 37800
print(c.seconds/3600)
## 10.5

# 특정 날짜와 시간 표현(표준 수학 연산) - 윤년도 인식함

from datetime import datetime
a = datetime(2012, 9, 23)
print(a + timedelta(days=10))
## 2012-10-03 00:00:00
b = datetime(2012, 12, 21)
d = b - a
print(d.days)
## 89
now = datetime.today()
print(now)
## 2017-05-25 22:47:49.459870
print(now + timedelta(minutes=10))
## 2017-05-25 22:57:49.459870

########################################################

# 3.13 마지막 금요일 날짜 구하기

# 한 주의 마지막 날의 날짜 구하기

from datetime import datetime, timedelta



def get_previous_byday(dayname, start_date=None):
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    if start_date is None:
        start_date = datetime.today()
    day_num = start_date.weekday()
    day_num_target = weekdays.index(dayname)
    days_ago = (7 + day_num - day_num_target) % 7
    if days_ago == 0 :
        days_ago = 7
    target_date = start_date - timedelta(days=days_ago)
    return target_date

print(get_previous_byday('Sun',datetime(2012, 12,21)))
## 2012-12-16 00:00:00

##############################################################

# 3.14 현재 달의 날짜 범위 찾기

# 이번 달의 첫번째 날짜와 다음달의 시작날짜 반환하는 함수

from datetime import datetime, date, timedelta  # 완전 신기하네!!
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

###############################################################

# 3.15 문자열을 시간으로 변환

from datetime import datetime
text = '2012-09-20'
y = datetime.strptime(text, '%Y-%m-%d')
z = datetime.now()
diff = z - y
print(diff)
## 1709 days, 0:24:15.741826

nice_z = datetime.strftime(z, '%A %B %d %Y') # 이게 훨씬 낫네!!
print(nice_z)
## Friday May 26 2017

from datetime import datetime # 형식이 YYYY-MM-DD 일 때 이걸 쓰자! 성능 좋음
def parse_ymd(s):
    year_s , mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))


###############################################################

# 3.16 시간대 관련 날짜 처리

# pytz 모듈

from datetime import datetime
from pytz import timezone
d = datetime(2012, 12, 21, 9, 30, 0)
print(d)
## 2012-12-21 09:30:00

central = timezone('US/Central') # 날짜 현지화
loc_d = central.localize(d)
print(loc_d)
## 2012-12-21 09:30:00-06:00

bang_d = loc_d.astimezone(timezone('Asia/Kolkata')) # 시간대 변환
print(bang_d)
## 2012-12-21 21:00:00+05:30

from datetime import timedelta # 섬머타임 고려
later = central.normalize(loc_d + timedelta(minutes =30))
print(later)
## 2012-12-21 10:00:00-06:00

#########################################################################

# 4.1 수동으로 이터레이터 소비

# for문 피하기
'''
with open('  ') as f:
    try :
        while True:
            line = next(f)
            print(line, end= '')
    except StopIteration:
        pass

with open('  ') as f:       # 두가지 방법 있음
    while True:
        line = next(f,None)
        if line is None:
            break
        print(line, end='')
'''
# 순환할 때 어떤 일이 일어나는가

'''
items = [1,2,3]
it = iter(items)
print(it)
## <list_iterator object at 0x0000000002963EF0>
print(next(it))
## 1
print(next(it))
## 2
print(next(it))
## 3
print(next(it))
## StopIteration
'''

###############################################################

# 4.2 델리게이팅 순환

class Node :      # __iter__() 메소드는 순환요청을 _children 속성으로 전달
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
        print(ch)
        ## Node(1)
        ## Node(2)

#######################################################

# 4.3 제너레이터로 새로운 순환 패턴 생성

# 제너레이터 함수 만들기

def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x  # yield 문으로 인해 함수가 제너레이터 함수로 변경
        x += increment

## 순환객체를 소비하는 함수 : sum, list ..

for n in frange(0, 4, 0.5):  # 이렇게도 쓰이네!!
    print(n)

print(list(frange(0, 1, 0.125)))
## [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]

# 제너레이터 함수의 동작 원리

def countdown(n):
    print('Starting to coount from',n)
    while n > 0:
        yield n
        n -= 1
    print('Done!')
'''
c = countdown(3)
print(c)
## <generator object countdown at 0x000000000294DA98>

print(next(c))
## Starting to coount from 3
## 3
print(next(c))
## 2
print(next(c))
## 1
print(next(c))
## StopIteration
'''
#################################################################

# 4.4 이터레이터 프로토콜 구현현

# depth-first 패턴으로 순환하는 이터레이터

class Node :      # __iter__() 메소드는 순환요청을 _children 속성으로 전달
    def __init__(self,value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self,node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self): # 뭔 말이야
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
    child1.add_child(Node(5))

    for ch in root.depth_first():
        print(ch)

    '''
    Node(0)
    Node(1)
    Node(3)
    Node(4)
    Node(5)
    Node(2)
    '''

#################################################################

# 4.5 역방향 순환

# reversed()

a = [1,2,3,4]
for x in reversed(a):  # 이런 좋은 방법이!!
    print(x)

# 순환가능 객체를 리스트로 변환 시 : 많은 메모리가 필요함

# 클래스에서 역방향 순환하기

class Countdown:
    def __init__(self,start):
        self.start = start

    def __iter__(self): # 순방향 순환
        n = self.start
        while n > 0:
            yield n
            n -= 1

    def __reversed__(self): # 역방향 순환 .. 뭐가 다른거지
        n = 1
        while n <= self.start:
            yield n
            n += 1

#########################################################################

# 4.6 추가상태를 가진 제너레이터 함수 정의

# 사용자에게 노출할 수 있는 클래스로 만들기

from collections import deque

class linehistory :
    def __init__(self, lines, histlen = 3):
        self.lines = lines
        self.history = deque(maxlen=histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()

with open('  ') as f:
    lines = linehistory(f)
    for line in lines :
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline),end='')




