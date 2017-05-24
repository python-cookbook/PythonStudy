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

'''
#chap 4 이터레이터와 제너레이터 