"""
                                                ▶ 3.11 임의의 요소 뽑기◀ 
♣  문제 : 시퀀스에서 임의의 아이템을 고르거나 난수를 생성하고 싶다
↘  해결 : random모듈에는 많은 함수가 있다.
        values = [1,2,3,4,5,6]
        0. 임의의 아이템 N개 뽑으려 한다.
            random.choise(values)
        1. 임의의 아이템 N개 뽑아서 사용하고 버릴 목적이라면 random.sample()을 사용한다.
            a. [a,b,c,d] ->  c
        2. 단순히 시퀀스의 아이템을 무작위로 섞으려면, random.shuffle()을 사용한다.
            a. sample(values,2)  -> [2,3]
            b. sample(values,3)  -> [6,2,5]
        3. 임의의 정수를 생성하려면 random.randint()을 사용한다.
            a. random.randint(0,10)    #0~10까지의 숫자 중 아무거나 하나 발생시켜라.
        4. 0과 1사이의 균등 부동 소수점 값을 생성하려면 random.random()을 사용한다.
            a. random.random  ->  0.924235256 ..
        5. N비트로 표현된 정수를 만들기 위해서는 random.getrandbits()을 사용한다.
            a. random.getrandbits(200)   -> 23423443535343409194349484...
   토론 : 
         random모듈은 Mersenne Twister 알고리즘을 사용해 난수를 발생시킨다. 
         이 알고리즘은 정해진 것이지만, random.seed()함수로 시드 값을 바꿀 수 있다.
         
 """

print('###############################################################################')
print('########################################## 3.11 임의의 요소 뽑기 #####################################')
print('###############################################################################')

import random
values = [1,2,3,4,5,6]
random.choice(values)

random.choice(values)
random.choice(values)

# 임의의 아이템 N개 뽑아서 사용하고 버릴 목적이라면 random.sample()을 사용한다.
random.sample(values,2)
# [6, 5]
random.sample(values,3)
# [5, 2, 4]
# 단순히 시퀀스의 아이템을 무작위로 섞으려면, random.shuffle()을 사용한다.
random.shuffle(values)

random.shuffle(values)
# [1, 5, 2, 3, 4, 6]
#임의의 정수를 생성하려면 random.randint()을 사용한다.
random.randint(0,10) #2
random.randint(0,10) #7
#0과 1사이의 균등 부동 소수점 값을 생성하려면 random.random()을 사용한다.
random.random()  #0.8761657566529589
random.random()  #0.8334977078111013
#N비트로 표현된 정수를 만들기 위해서는 random.getrandbits()을 사용한다.
random.getrandbits(200)


print('###############################################################################')
print('##################################random.seed()함수로 시드 값을 바꾸기#######################################')
print('###############################################################################')

random.seed()       #시스템 시간이나 os.urandom() 시드
random.seed(12345)  #주어진 정수형 시드
random.seed(b'bytedata') #바이트 데이터 시드

"""
위 기능 외에, random()에는 유니폼, 가우시안, 확률 분포 함수도 포함되어 있다.
예를 들어, random.uniform()은 균등분포 숫자를 계산하며
         random.gauss()는 정규분포 숫자를 계산한다.
         기타 외 등 다른 분포들이 많이 포함되어 있다.
random()의 함수는 암호화 관련 프로그램에서 사용하지 말아야 한다. 
그런 기능이 필요하다면 ssl모듈을 사용해야 한다. 예를 들어 ssl.RAND_bytes()는 보안상 안전한 임의의 바이트 시퀀스를 생성한다.
"""






"""
                                                ▶ 3.12 시간 단위 변환◀ 
♣  문제 : 날짜 -> 초, 시간 -> 분   으로 시간 단위 변환을 해야한다!
↘  해결 : 단위 변환이나 단위가 다른 값에 대한 계산을 하려면 datetime모듈을 사용한다.
         예를 들어, 시간의 간격을 나타내기 위해서는 timedelta 인스턴스를 생성한다.


 """

print('###############################################################################')
print('########################################## 3.12 시간 단위 변환#####################################')
print('###############################################################################')

from datetime import timedelta
# 시간의 간격 알아보기

a = timedelta(days=2, hours=6, seconds=0)
b = timedelta(hours=4.5)
c= a+b
print(c.days)   #2일?
print(c.seconds) #37800
print(c.seconds / 3600) #10.5          한시간에 3600초니까 38700초를 시간단위로 환산해본것
print(c.total_seconds())  #210600.0    2일하고 10.5시간을 모두 초 단위로 환산한 값
print(c.total_seconds()/3600) #58.5    위 값을 시간단위로 환산해본 것

#날짜와 시간을 표현하려면 datetime인스턴스를 만들고
#표준수학연산을 한다.
from datetime import datetime
a = datetime(2012, 9, 23)  #a라는 인스턴스
print(a)   #2012-09-23 00:00:00
print(a+timedelta(days=10))  #2012-10-03 00:00:00

b = datetime(2012,12,21)
d = b-a
print(d)   #89 days, 0:00:00
print(d.days)   #89

now = datetime.today()
print(now)  #2017-05-25 13:11:39.584240
print(now+timedelta(minutes=30))  #2017-05-25 13:42:00.774930


#계산을 할 떄는, datetime이 윤년을 인식한다는 점을 주목해야 한다.

a = datetime(2012,3,1)
b = datetime(2012,2,28)
c = datetime(2013,3,1)
d = datetime(2013,2,28)
print(a-b)   #2 days
print(c-d)   #1 day

"""
대부분의 날짜,시간 계산 문제는 datetime모듈로 해결 가능
시간대(time zone) / 퍼지 시계 범위(fuzzy time range) / 공휴일 계산 등의 더욱 복잡한 날짜 계산이 필요하다면
dateutill 모듈을 알아보자.

대부분의 비슷한 시간 계산은 dateutill.relativedelta()함수로 수행할 수 있다.
하지만 한가지 주목할 만한 기능으로 달을 처리하기 위해 차이를 채워주는 것이 있다.
"""


a = datetime(2012,9,23)
# print(a+timedelta(months=1)) #'months' is an invalid keyword argument for this function

from dateutil.relativedelta import relativedelta as reldel
print(a + reldel(months=+1))  #2012-10-23 00:00:00   9월 -> 10월로 업데이트됨
a = a+reldel(months=+1)
print(a)


#두 날짜 사이의 시간이 궁금하다면!??

froundtime = datetime(2012,12,21)
uploadtime = datetime(2012,12,23)
between_time =uploadtime-froundtime

d = reldel(froundtime,uploadtime) #relativedelta(days=-2)
print(between_time)  #2 days, 0:00:00
print(d)




"""
                                                ▶ 3.13  마지막 금요일 날짜 구하기◀ 
♣  문제 : 한 주의 마지막에 나타난 날의 날짜를 구하는 일반적인 해결책을 만들고 싶다. 
        마지막 금요일이 며칠인지 궁금해
↘  해결 : datetime모듈 이용.
         


 """

print('###############################################################################')
print('########################################## 3.13  마지막 금요일 날짜 구하기#####################################')
print('###############################################################################')


from datetime import datetime, timedelta

weekdays = ['Mon','Tue','Weds','Thur','Fri','Sat','Sun']

def get_prev_byday(dayname, start_date=None):
    if start_date is None:
        start_date = datetime.today()  #오늘날짜로 기준을 잡고
    print(start_date)  #2012-12-21 00:00:00
    day_num = start_date.weekday()  #오늘날짜의 요일을 할당한다.
    print(day_num)  #4
    day_num_target = weekdays.index(dayname)
    days_ago = (7 +day_num - day_num_target) % 7
    if days_ago == 0:
        days_ago = 7
    target_date = start_date - timedelta(days = days_ago)
    print(target_date)

get_prev_byday('Tue')  #2012-12-16 00:00:00


"""
이번 레시피는 시작날짜와 목표 날짜를 관련 있는 숫자 위치에 매핑하는 데에서 시작한다.
(월요일= 0 일요일 = 7)

그리고 모듈러 연산을 사용해 목표 일자가 나타나고, 며칠이 지났는지 알아낸다.
시작일자에서 적절한 timedelta 인스턴스를 빼서 원하는 날짜를 계산한다.
이와 같은 날짜 계산을 많이 수행한다면 python-dateutill 패키지를 설치하는 것이 좋다.

예를 들어, dateutil의 relativedelta() 를 사용한 동일한 계산은 다음과 같다.

"""


from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
d = datetime.now()
print(d)

#다음 금요일
print(d+relativedelta(weekday=FR))

#마지막 금요일
print(d+relativedelta(weekday=FR(-1)))

"""
                                                ▶ 3.14  현재 달의 날짜 범위 찾기◀ 
♣  문제 : 현재 달의 날짜를 순환해야 하는 코드가 있고, 그 날짜 범위를 계산하는 효율적인 방법이 필요하다.
↘  해결 : 날짜를 순환하기 위해 모든 날짜를 리스트로 만들 필요가 없다!
         대신 범위의 시작 일자와 마지막 날짜만 계산하고 datetime.timedelta객체를 사용해서 날짜를 증가시키면 된다.
         datetime객체를 받아서 그 달의 첫번째 날짜와 다음 달의 시작 날짜를 반환하는 함수 코드는 다음과 같다.
         



 """

print('###############################################################################')
print('##########################################3.14  현재 달의 날짜 범위 찾기#####################################')
print('###############################################################################')

from datetime import datetime,date,timedelta
import calendar


def get_month_range(start_date = None):
    if start_date is None:
        start_date = date.today().replace(day=1)  #그러니까..2017년 5월 21일이었는데..1일로바꿔버린다?
        # print(start_date)  #2017-05-01
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)  #monthrange(2017,05)
    # calendar.monthrange(start_date.year, start_date.month)  #( 0, 31)
    # monthrange(2017,5) 2017년의 5월달의 날짜범위는 무엇인지 대답해주고 있는거임..소름;; >> 0,31 start =0 last =31 이라는것..;
    # print(days_in_month)  # >>31  /  위에서 _는 0이니까 따로 할당받지 않은 것임.
    a = timedelta(days=days_in_month)
    b = start_date
    print(a)  #31 days, 0:00:00
    print(b)
    # end_date = start_date + timedelta(days=days_in_month)    # 5월 1일 + 31 days, 0:00:00  >> 5월의 한달이 지난 6월1일이되겠다.
    # print(end_date)  # 2017-06-01
    return (start_date,a+b)
print(get_month_range())


# 이제 날짜 범위를 순환하는 것은 꽤 단순하다.
aa = list()
a_day = timedelta(days=1)  #1일
first_day, last_day = get_month_range()
while first_day < last_day:
    print(first_day)
    aa.append(first_day)
    first_day += a_day
print(aa)


"""
이번 레시피는 우선 월의 첫번째 날을 계산하는데서 시작한다.
첫째 날을 간단히 구하기 위해서 date의 repace() 메소드에 days속성을 1로 설정하면 된다.
replace()는 시작한것과 동일한 객체를 만든다는 점이 좋다.
따라서 date 인스턴스를 입력하면 그결과도 date가 된다.
마찬가지로 datetime 인스턴스를 넣으면 datetime 인스턴스를 얻는다.
그 후, calendar.monthrange() 함수로 주어진 월에날짜가 몇개가있는지 찾는다.  (마치 len이 하는 일같다 ㅋㅋ)
월의날짜 수를 구하고 나면, 시작 날짜에 적절한 timedelta를 더해서 마지막 날을 구한다. 
미묘한 부분이지만,마지막 날짜는 범위에 포함되지 않는다는 것이 중요하다. 엄밀히 말하면 마지막 날짜가 아니라, 다음 달의시작날짜!!!
날짜 범위를 순환하려면 표준 수학과 비교 연산자를 사용한다.
예를 들어 날짜를 증가시키기 위해서 timedelta 인스턴스를 사용할 수 있다. < 연산자로 날짜가 마지막 날짜보다 빠른지 비교한다.

"""


# 날짜 비교하여 누가 더 빠른지 보기

#제너레이터를 사용하면 쉽게 구현할 수 있다.

def date_range(start, stop, step):
    while start < stop:
        yield start
        start += step

for d in date_range(datetime(2012,9,1), datetime(2012,10,1), timedelta(hours=6)):
    print(d)

# 9월 1일부터 10월1일까지 6시간씩 증가시키며 날짜를 순환하라!!!크..갓코드!




"""
                                                ▶ 3.15  문자열을 시간으로 변환◀ 
♣  문제 : 문자열 형식의 시간 데이터를 datetime 객체로 변환하고싶다.
↘  해결 : 파이썬의 datetime 모듈을 사용하면 상대적으로 easy하게 해결가능 

   토론 : datetime.strptime() 메소드는 네 자리 연도 표시를 위한 %Y, 두 자리 월 표시를 위한 %m과 같은 서식을 지원한다.
         또한 datetime 객체를 문자열로 표시하기 위해서 이 서식을 사용할 수 있다.
         예를 들어 datetime 객체를 생성하는 코드가 있는데, 이를 사람이 이해하기 쉬운 형태로 변환하고자 한다면 다음과 같이 하면 된다.
         
 """

print('###############################################################################')
print('##########################################3.15  문자열을 시간으로 변환#####################################')
print('###############################################################################')



from datetime import datetime
text = '2012-09-20'

user_time = datetime.strptime(text, '%Y-%m-%d')
z = datetime.now()

print(type(z-user_time)) #1708 days, 18:17:09.412832



#datetime 객체를 문자열로 표시하기 위해서 이 서식을 사용


print(z)  #2017-05-25 18:22:35.380724

nice_z = datetime.strftime(z,'%A %B %d, %Y')   #Thursday May 25, 2017
print(nice_z)


# strptime() 은 순수 파이썬만을 사용해서 구현했고, 시스템 설정과 같은 세세한 부분을 모두 처리해야하므로
# 예상보다 실행 속도가 느린 경우가 많다. 만약 코드에서 처리해야할 날짜가 아주 많은데, 그 날짜 형식을 정확히 알고 있다면
# 해결책을 직접 구현하는 것이 속도 측면에서 훨씬 유리하다. 예를 들어 날짜 형식이 "YYYY-MM-DD"라는 것이 분명하다면,
# 다음과 같은 함수를 작성한다.

from datetime import datetime
def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))

print(parse_ymd('1993-03-21'))  #'datetime.datetime'>   1993-03-21 00:00:00

#저자가 테스팅 해본 바로는 위 방식이 strptime() 보다 7배 빨랐다. !!

