


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


























