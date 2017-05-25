####################################################################################################
# 3.12] 시간 단위 변환
#   * 날짜를 초로, 시간을 분으로처럼 시간 단위 변환을 해야 한다.
#
# 1] datetime 모듈
#       1) timedelta 인스턴스 사용
#           : 단위 변환이나 단위가 다른 값에 대한 계산을 해 주는 모듈
#       2) datetime 인스턴스 사용
#           : 특정 날짜와 시간 표현
#             윤년도 인식해준다 !
# 2] dateutil 모듈 : 시간대(time zone), 퍼지 시계 범위(fuzzy time range), 공휴일 계산 등
#                    더욱 복잡한 날짜 계산이 필요할 때 사용
#       1) relativedelta()
#           : timedelta와 비슷한 시간 계산 가능, 하지만 timedelta에는 없는 months가 있다!
#
####################################################################################################
from datetime import timedelta, datetime

### 시간 단위 간의 계산 및 단위 변환
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)

c = a + b
print(c.days)                   # 2일 + @
print(c.seconds)                # 결과를 초로 환산 : 37800
print(c.total_seconds() / 3600) # 결과를 시간으로 환산 : 58.5


## 특정 날짜와 시간 표현
a = datetime(2012, 9, 23)
print(a + timedelta(days=10))   # 2012-10-03 00:00:00
b = datetime(2012, 12, 21)
d = b - a
print(d.days)   # 89

now = datetime.today()
print(now)  # 2017-05-24 10:13:00.960939
print(now + timedelta(minutes=10))  # 2017-05-24 10:23:00.960939


### dateutil.relativedelta()
from dateutil.relativedelta import relativedelta

a = datetime(2012, 9, 23)
print(a + relativedelta(months=+1)) # 2012-10-23 00:00:00

## 두 날짜 간의 시간
b = datetime(2012, 12, 21)
d = b - a
print(d)    # 89 days, 0:00:00
d = relativedelta(b, a)
print(d)    # relativedelta(months=+2, days=+28)