#시간 단위 변환
#문제 : 날짜를 초로, 시간을 분으로 처럼 시간 단위 변환을 해야함.
#해결 : 단위 변환이나 단위가 다른값에 대한 계산을 하려면 datetime모듈
#시간의 간격
from datetime import timedelta
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c = a+ b
c
c.days
c.seconds/3600
c.total_seconds()/3600
#특정 날짜와 시간 표현은 datetime 인스턴스를 만들고 표준 수학 연산을 한다.
from datetime import datetime
a = datetime(2012,9,23)
print(a+timedelta(days=10))

b=datetime(2012,12,21)
d = b-a
d.days
now = datetime.today()
print(now)
#계산 할 때, datetime이 윤년을 인식함.
a = datetime(2012,3,1)
b = datetime(2012,2,28)
a-b
(a-b).days
c=datetime(2013,3,1)
d=datetime(2013,2,28)
(c-d).days
#토론 대부분의 날짜 시간문제는 이 모듈로 해결 가능. 더 복잡한 계산은 dateutil.
#대부분의 비슷한 시간 계산은 dateutil.relativedelta() 함수로 수행 가능. 하지만 한 가지 주목할 만한 기능으로 달을 처리하기 위해 차이를 채워 주는 것이 있다.
a = datetime(2012,9,23)
a + timedelta(months=1)
from dateutil.relativedelta import relativedelta
a + relativedelta(months=+1)
b = datetime(2012,12,21)
d = b-a
d
d = relativedelta(b,a)
d