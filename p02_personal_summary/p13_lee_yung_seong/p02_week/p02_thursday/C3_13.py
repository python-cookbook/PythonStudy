#마지막 금요일 날짜 구하기.
#문제 : 한주의 마지막에 나타난 달의 날짜를 구하는 일반적인 해결책을 만들고 싶다. 예를 들면 마지막 금요일은 며칠?
#해결 : 파이썬의 datetime 모듈을 사용하자
from datetime import datetime,timedelta
weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

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

datetime.today()
get_previous_byday('Monday')
#선택적으로 설정 가능한 start_date에는 또 다른 datetime 인스턴스 제공
get_previous_byday('Sunday',datetime(2012,12,21))
#토론 : 이번 레시피는 ㅣㅅ작 날짜와 목표 날짜를 관련 있는 수자 위치에 매핑하는 데에서 시작한다(월요일부터 0).
#그리고 모듈러 연산을 사용해 목표 일자가 나타나고 며칠이 지났는지 알아낸다.
#이제 시작 일자에서 적절한 timedelta 인스턴스를 빼서 원하는 날짜를 계산한다.
#이와 같은 날짜 계산을 많이 수행한다면 python-dateutil 패키지를 설치하는 것이 좋다.
#예를 들어 dateutil의 relativedelta()를 사용한 동일한 계산은 다음과 같다.
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
d = datetime.now()
d
#다음 금요일
print(d + relativedelta(weekday=FR))
#마지막 금요일
print(d + relativedelta(weekday=FR(-1)))