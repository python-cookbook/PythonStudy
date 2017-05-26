


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



















