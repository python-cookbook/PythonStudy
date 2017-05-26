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

#