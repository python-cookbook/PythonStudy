            #3.11 임의의 요소 뽑기
#문제 : 난수를 생성
    #예제 
import random
values = [1,2,3,4,5,6]

random.choice(values)
#(실행결과) 2
random.choice(values)
#(실행결과) 6

random.sample(values,2)
#(실행결과) [4, 3]
random.sample(values,2)
#(실행결과) [5, 2]

random.shuffle(values)
values
#(실행결과) [3, 6, 4, 5, 2, 1]

random.shuffle(values)
values
#(실행결과) [4, 3, 6, 1, 2, 5]

random.randint(0,10) # 임의의 정수 선택
#(실행결과) 2
#(실행결과) 1
#(실행결과) 7

random.random() # 0과 1사이의 소수점 값을 생성
#(실행결과) 0.5341377210157413

random.getrandbits(200) #N비트로 표현된 정수 ?????
#(실행결과) 762446508741541077604166948025168709242841962807187967661735

random.seed(12345)
random.seed(b'bytedata')



            #3.12 시간단위 변환
#문제 : 날짜를 초로, 시간을 분으로처럼 시간 단위 변환을 해야 한다.
    
    #예제
from datetime import timedelta
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c=a+b
c.days
#(실행결과) 2

c.seconds
#(실행결과) 37800

c.seconds/3600

#(실행결과) 10.5

c.total_seconds()/3600
#(실행결과) 58.5

 
from datetime import timedelta
from datetime import datetime
a= datetime(2012,9,23)
print(a + timedelta(days=10))
#(실행결과) 2012-10-03 00:00:00

b=datetime(2012,12,21)
d=b-a
d.days
#(실행결과) 89

now = datetime.today()
print(now)
#(실행결과) 2017-05-26 10:42:18.508753

print(now+timedelta(minutes=10))
#(실행결과) 2017-05-26 10:52:18.508753

a=datetime(2012,3,1)
b=datetime(2012,2,28)
a-b
#(실행결과) datetime.timedelta(2)
(a-b).days
#(실행결과) 2
c=datetime(2013,3,1)
d=datetime(2013,2,28)
(c-d).days
#(실행결과) 1

 

            #3.13 마지막 금요일 날짜 구하기

#문제 한 주의 마지막 날짜

    #예제 
from datetime import datetime, timedelta
weekdays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def get_previous_byday(dayname, start_date=None):
    if start_date is None: 
        start_date =datetime.today()
    day_num = start_date.weekday()
    day_num_target = weekdays.index(dayname)
    days_ago = (7 + day_num - day_num_target)%7
    if days_ago == 0:
        days_ago = 7
    target_date = start_date - timedelta(days=days_ago)
    return target_date

datetime.today()
#(실행결과) datetime.datetime(2017, 5, 26, 11, 10, 24, 331826)

get_previous_byday('Monday')
#(실행결과) datetime.datetime(2017, 5, 22, 11, 13, 28, 692737)

get_previous_byday('Saturday')
#(실행결과) datetime.datetime(2017, 5, 20, 11, 46, 53, 502315) #저번주 토요일

get_previous_byday('Sunday', datetime(2012,12,21)) # start date 설정
#(실행결과) datetime.datetime(2012, 12, 16, 0, 0)



            #3.14 현재 달의 날짜 범위 찾기
            
#현재 달의 날짜를 순환해야하는 코드가 있고 그 날짜 범위를 계산

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
    first_day +=a_day
    
#(실행결과) 
#2017-05-01
#2017-05-02
#2017-05-03
#2017-05-04
#2017-05-05
#2017-05-06
#2017-05-07
#2017-05-08
#2017-05-09
#2017-05-10



            #3.15 문자열을 시간으로 변환
            
from datetime import datetime
text = '2012-09-20'
y=datetime.strptime(text, '%Y-%m-%d')
z=datetime.now()
diff = z - y
diff
#(실행결과) datetime.timedelta(1709, 54112, 847943)           



            #3.16 시간대 관련 날짜 처리
            
    #예제
from datetime import datetime
from pytz import timezone
d= datetime(2012,12,21,9,30,0)
print(d)
#(실행결과) 2012-12-21 09:30:00

central = timezone('US/Central')
loc_d = central.localize(d)
print(loc_d)
#(실행결과) 2012-12-21 09:30:00-06:00

bang_d = loc_d.astimezone(timezone('Asia/Kolkata'))
print(bang_d)

#(실행결과) 2012-12-21 21:00:00+05:30

d = datetime(2013, 3, 10, 1, 45)
loc_d = central.localize(d)
print(loc_d)
#(실행결과) 2013-03-10 01:45:00-06:00

later = loc_d + timedelta(minutes=30)
print(later)
#(실행결과) 2013-03-10 02:15:00-06:00 #틀림 

 
from datetime import timedelta
later = central.normalize(loc_d+timedelta(minutes=30))

print(later)
#(실행결과) 2013-03-10 03:15:00-05:00

 
 

 
                     #Chapter 4 이터레이터와 제너레이터
                     
            #4.1 수동으로 이터레이터 소비
            
    #예제 : next() 함수 사용

with open('d:\\data\\emp.txt') as f:
    try:
        while True:
            line = next(f)
            print(line, end='')
    except StopIteration:
        pass


with open('d:\\data\\emp.txt') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
        print(line, end='')
                     
items = [1,2,3]
it = iter(items)
next(it)
#(실행결과)1 
next(it)
#(실행결과) 2 
next(it)
#(실행결과) 3

 
 
         #4.2 델리게이팅 순환
    #예제
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []
    
    def __repr__(self):
        return 'Node({!r})'.format(self._value)
    
    def __iter__(self):
        return iter(self._children)
    
if __name__ =='__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)
    

            #4.3 제너레이터로 새로운 순환 패턴 생성
            
    #예제
def frange(start, stop, increment):
    x= start
    while x < stop:
        yield x
        x += increment
        
for n in frange(0,4,0.5):
    print(n)
#(실행결과) 
#0
#0.5
#1.0
#1.5
#2.0
#2.5
#3.0
#3.5



list(frange(0,1,0.125))
#(실행결과)  [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]



            #4.4 이터레이터 프로토콜 구현
    #예제
    
class Node:
    def __init__(self, value):
        self._value = value
        self._children=[]
    
    def __repr__(self):
        return 'Node({!r})'.format(self._value)
    
    def __add_child(self, node):
        self._children.append(node)
        
    def __iter__(self):
        return iter(self._children)
    
    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()
            
            
        
            #4.5 역방향 순환
    #예제 
a=[1,2,3,4]
for x in reversed(a):
    print(x)
#(실행결과)
4
3
2
1

#파일을 거꾸로 출력하기

f = open('somefile')
for line in reversed(list(f)):
    print(line, end='') 
    
    
    
            #4.6 추가 상태를 가진 제너레티러 함수 정의
            
#예제
from collections import deque

class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines=lines
        self.history = deque(maxlen=histlen)
    
    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line
    
    def clear(self):
        self.history.clear()
        
        