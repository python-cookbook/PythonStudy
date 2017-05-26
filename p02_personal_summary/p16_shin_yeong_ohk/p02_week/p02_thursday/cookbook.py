===============================================================================
#3.11 임의의 요소 뽑기
# 시퀀스에서 임이의 아이템을 고르거나 난수를 생성하고 싶을 때,
#"random 모듇"

EX1>
import random
values = [1,2,3,4,5,6]
random.choice(values)
# 4
random.choice(values)
# 6
random.choice(values)
# 2



EX2>
#시퀀스에서 임의의 아이템 선택
random.sample(values,2)
#[1,4]
random.sample(values,2)
#[2,4]
random.sample(values,3)
#[6,4,1]
random.sample(values,3)
#[5,4,1]



EX3>
#임의의 아이템을 N개 뽑아서 사용하고 버릴 때
random.shuffle(values)
values
#[4,2,5,6,3,1]
random.shuffle(values)
values
#[5,3,2,1,6,4]



EX4>
#임이의 정수 생성
random.randint(1,10)
#4
random.randint(0,10)
#4
random.randint(0,10)
#7


EX5>
#0과 1 사이의 균등 부동 소수점 값을 생성할 때
random.random()
#0.9826232353263736
random.random()
#0.5195526698334441


EX6>
#N비트로 표현된 정수를 만들기 위해서
random.getrandbits(200)
#590728042719697246497053964898262720175333557299814344291097
===============================================================================





===============================================================================
#3.12 시간 단위 변환
#날짜를 초로, 시간을 분으로처럼 시간 단위 변환을 해야 할 떼
#단위 변환이나 단위가 다른 값에 대한 계산
#"datetime 모듈

EX1>
from datetime import timedelta    #시간의 간격
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c= a+b
c.days
#2
c.seconds
#37800
c.seconds/3600
#10.5
c.total_seconds()/3600
#58.5



EX2>
#특정 날짜와 시간을 표현하려면 datetime 인스턴스를 만들고 연산
from datetime import datetime
a = datetime(2012,9,23)
print(a+timedelta(days=10))
#2012-10-03 00:00:00

b=datetime(2012,12,21)
d=b-a
d.days
#*9

now=datetime.today()
print(now)


print(now+timedelta(minutes=10))



EX3>
#datetime은 윤년 인식
a = datetime(2012,3,1)
b = datetime(2012,2,28)
a-b
# datetime.timedelta(2)
(a-b).days
#2
c=datetime(2013,3,1)
d=datetime(2013,2,28)
(c-d).days
#1
===============================================================================






===============================================================================
#3.13 마지막 금요일 날짜 구하기
#한 주의 막지막에 나타난 날의 날짜 구하기

EX1>
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

datetime.today()    #참고용
# datetime.datetime(2017, 5, 26, 22, 9, 45, 800553)
get_previous_byday('Monday')
# datetime.datetime(2017, 5, 22, 22, 11, 37, 129819)
get_previous_byday('Tuesday')   #저번주, 오늘 아님
#datetime.datetime(2017, 5, 23, 22, 12, 1, 20810)
get_previous_byday('Friday')
#datetime.datetime(2017, 5, 19, 22, 12, 47, 392690)

#start_date에는 또 다른 datetime 인스턴스 제공
get_previous_byday('Sunday',datetime(2012,12,21))
#datetime.datetime(2012, 12, 16, 0, 0)
===============================================================================





===============================================================================
#3.14 현재 달의 날짜 범위 찾기
#현재 달의 날짜를 순환해야 하는 코드가 있고 그 날짜 법위를 계산하는 효율적인 방법
#날짜를 순환하기 위해 모든 날짜를 리스트로 만들기X
#범위의 시작 일자와 마지막 날짜만 계산하고 datetime.timedelta 객체를 사용해서 날짜 증가시키기
#datetime 객체를 받아서 그 달의 첫번째 날짜오 ㅏ다음달의 시작 날짜를 반환하는 함수 코드

EX1>
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
#2017-05-01
#2017-05-02
#2017-05-03



EX2>
#날짜 범위를 순환하려면 표준 수학과 비교 연산자를 사용한다.
#예를 들어 날짜를 증가시키기 위해서 timedelta 인스털스 사용가능
#"<" 연산자로 날짜가 마지막 날짜보다 큰지 비교
#"range()함수" "발생자(generator)" 
def date_range(start, stop, step):
    while start < stop:
        yield start
        start += step
for d in date_range(datetime(2012, 9, 1), datetime(2012,10,1),timedelta(hours=6)):
    print(d)
#2012-09-01 00:00:00
#2012-09-01 06:00:00
#2012-09-01 12:00:00
===============================================================================






===============================================================================
#3.15 문자열을 시간으로 변환
#문자열 형식의 시간 데이터를 datetime 객체로 변환시키기

EX1?
from datetime import datetime
text = '2012-09-20'
y = datetime.strptime(text, '%Y-%m-%d')
z = datetime.now()
diff = z - y
diff
#datetime.timedelta(1709, 82466, 965196)

#datetime.striptime() 메소드는 네 자리 연도 표시를 위한 %Y,
#두 자리 월 표시를 위한 %m 같은 서식을 지원한다.
#datetime 객체를 문자열로 표시하기 위해서 사용가능

#사람이 이해하기 쉬운 datetime 객체 생성 코드
EX2>
z
# datetime.datetime(2017, 5, 26, 22, 54, 26, 965196)
nice_z = datetime.strftime(z, '%A %B %d, %Y')
nice_z
#'Friday May 26, 2017'
===============================================================================







===============================================================================
#3.16 시간대 관련 날짜 처리
#다른 나라와의 시간차
#"pytz 모듈"
#Olson 시간대 데이터베이스 제공
#pytx는 datetime 라이브러리에서 생성한 날짜를 현지화할 때 사용

EX1>
from datetime import datetime
from pytz import timezone
d = datetime(2012, 12, 21, 9, 30, 0)
print(d)
#2012-12-21 09:30:00



EX2>
#시카고에 맞게 현지화
central = timezone('US/Central')
loc_d = central.localize(d)
print(loc_d)
#2012-12-21 09:30:00-06:00


#날짜를 현지화하고 나면, 다른 시간대로 변호나 가능
#방갈로르의 동일 시간
EX3>
bang_d = loc_d.astimezone(timezone('Asia/Kolkata'))
print(bang_d)
#2013-03-10 13:15:00+05:30



EX4>
#변환된 날짜에 산술 연산을 하려면 서머타임제 등을 알고 있어야 한다.
#예를 들어 2013년 미국에서 표준 서머타임은 3월 13일 오전 2시에 시작한다.(여기서 한시간 생략된다.)
#이를 고려하지 않고 계산하면 계산결과가 잘못된다.
d = datetime(2013, 3, 10, 1, 45)
loc_d = central.localize(d)
print(loc_d)
#2013-03-10 01:45:00-06:00
later = loc_d + timedelta(minutes=30)
print(later)
#2013-03-10 02:15:00-06:00
틀렸어 틀렸다구


EX4_1>
#한 시간이 생략된 서머타임을 고려하지 않았기 때문
#"normalize() 메소드"
from datetime import timedelta
later = central.normalize(loc_d + timedelta(minutes=30))
print(later)
#2013-03-10 03:15:00-05:00
===============================================================================








#Chapter4_이터레이터와 제너레이터
#객체 순환
#순환 객체 만들기, itertolls 모듈의 순호나 패턴 적용하기, 제너레이터 함수 만들기
===============================================================================
#4.1 수동으로 이터레이터 소비
#FOR 순환문 사용하지 않고 순환 가능한 아이템에 접근할 때

EX1>
#"next() 함수" "StopIteration 예외를 처리하기 위한 코드 작성"
#파일에서 줄을 읽는 코드
with open('/etc/passwd')  as f:
    try:
        while True:
            line = next(f)
            print(line, end='')
    except StopIteration:
        pass
#StopIteration은 순환의 끝을 알리는데 사용
#next()를 수동으로 사용한다면 None과 같은 종료 값을 반환하는 데 사용가능
with open('/etc/passwd') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
        print(line, end='')
===============================================================================        
        




===============================================================================
#4.2 델리게이팅 순환
#리스트, 튜플 등 순환 가능한 객체를 다믕ㄴ 사용자 정의 컨테이너를 만들었다.
#이 컨테이너에 사용 가능한 이터레이터 만들기
#"__init__()" 메소드

EX1>
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
# 예제
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)
    # Node(1), Node(2) 출력
#Node(1)
#Node(2)
#이 코드에서 "__init__()" 메소드는 순환 요청을 _children 속성으로 전달
===============================================================================
                 
                 
                 
                 

                 
===============================================================================                 
#4.3 제너레이터로 새로운 순환 패턴 생성
#내장함수[range(), reversed()]와는 다른 동작을 하는 순환 패턴을 만들고 싶을 때.

EX1>
#새로운 순환 패턴을 만들고 싶다면, 제너레이터 함수를 사용해서 정의
#특정 범위의 부동 소수점 숫자를 만드는 제너레이터 코드
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment
        
#이런 함수를 사용하려면, for 순환문이나 순환 객체를 소비하는 다른 함수(sum(), list(0 등)를 사용한 순환
for n in frange(0,4,0.5):
    print(n)
#0
#0.5
#1.0
#1.5
#2.0
#2.5
#3.0
#3.5
list(frange(0,1,0.125))
#[0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
===============================================================================





===============================================================================
#4.4 이터레이터 프로토콜 구현
#순환을 지원하는 객체를 만드는데, 이터레이터 프로토콜을 구현하는 쉬운 방법

EX1>
#객체에 대한 순환을 가장 쉽게 구현하는 방법은 제너레이터 함수를 사용하는 것
#노드를 깊에 -우선 패턴으로 순환하는 이터레이터를 구현하고 싶다.
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
##예제
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
#Node(0)
#Node(1)
#Node(3)
#Node(4)
#Node(2)
#Node(5)

#depth_first()메소드
#처음에는 자기 자신을 만들고 (yield) 그 다음에는 자식을 순환한다.
#이떼 그 자식은 depth_first() 메소드 (yield from을 사용)로 아이템을 만든다.
===============================================================================

                    
                     
                     
                     
===============================================================================                   
#4.5 역방향 순환
#시퀀스 아이템을 역방향으로 순환하기
#"reversed() 함수"

EX1>
a = [1, 2, 3, 4]
for x in reversed(a):
    print(x)
#4
#3
#2
#1

#역방향 순환은 객체가 __reversed__() 특별 메소드를 구현하고 있거나 크기를 알 수 있는 경우에만 가능
#두 조건 중에서 아무것도 만족하지 못하면 객체를 먼저 리스트로 반환

#파일을 거꾸로 출력하기
f = open('somefile')
for line in reversed(list(f)):
    print(line, end='')
#하지만 순환 가능 객체를 리스트로 변환할 때 많은 메모리가 필요하다.


EX2>
#__reversed__() 메소드를 구현하면 사용자 정의 클래스에서 역방향 순환이 가능하다.
class Countdown:
    def __init__(self, start):
        self.start = start
    # 순방향 순환
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
===============================================================================
 





===============================================================================
#4.6 추가 사아태를 가진 제너레이터 함수 정의
#제너레이터 함수를 정의하고 싶지만, 사용자에게 노출할 추가적인 상태 넣기

EX1>
#사용자에게 추가 상태를 노출하는 제너레이터를 원할 때, __iter__() 메소드에 
# 제너레이터 함수 코드를 넣어서 쉽게 클래스로 구현할 수 있다.
from collections import deque
class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)
    def __iter__(self):
        for lineno, line in enumerate(self.lines,1):
            self.history.append((lineno, line))
            yield line
    def clear(self):
        self.history.clear()

#이 클래스를 사용하려면 일반 제너레이터 함수처럼 대해야 한다.
#하지만 인스턴스를 만들기 때문에 history속성이나 clear()메소드 같은 내부 속성에 접근 가능
with open('somefile.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')
===============================================================================                