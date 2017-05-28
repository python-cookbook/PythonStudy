####################################################################################################
# 3.13] 마지막 금요일 날짜 구하기
#   * 한 주의 마지막에 나타난 날의 날짜를 구하는 일반적인 해결책을 만들고 싶다.
#     예를 들어 마지막 금요일이 며칠인지 궁금하다.
#
# 1] datetime 모듈을 이용한 클래스 생성
# 2] dateutil.relativedelta 이용
####################################################################################################

from datetime import datetime, timedelta

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

## 특정 날짜 직전의 마지막 X요일이 몇일인지 알아내는 코드
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

## 인터프리터 연산
# >>>datetime.today()
# datetime.datetime(2017, 5, 24, 11, 43, 31, 447358)
# >>>get_previous_byday('Monday')
# datetime.datetime(2017, 5, 22, 11, 43, 40, 474602)
# >>>get_previous_byday('Tuesday')
# datetime.datetime(2017, 5, 23, 11, 44, 18, 871589)
# >>>get_previous_byday('Friday')
# datetime.datetime(2017, 5, 19, 11, 44, 53, 157789)


###
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *

d = datetime.now()
print(d)    # 2017-05-24 11:52:45.114054
# 다음 금요일
print(d + relativedelta(weekday=FR))    # 2017-05-26 11:53:11.818708
# d 이전의 마지막 금요일
print(d + relativedelta(weekday=FR(-1)))    # 2017-05-19 11:53:39.609640