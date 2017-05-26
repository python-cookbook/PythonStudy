####################################################################################################
# 3.14] 현재 달의 날짜 범위 찾기
#   * 현재 달의 날짜를 순환해야 하는 코드가 있고, 그 날짜 범위를 계산하는 효율적인 방법이 필요하다.
#
####################################################################################################

from datetime import datetime, date, timedelta
import calendar

## 특정 날짜가 속한 월의 첫 날짜와 마지막 날짜를 반환
def get_month_range(start_date=None):
    if start_date is None:
        start_date = date.today().replace(day=1)    # replace 함수 : 기존과 동일한 객체를 만들어주므로 편하다!
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + timedelta(days=days_in_month)
    return (start_date, end_date)

# a_day만큼의 텀으로 월의 날짜 출력
a_day = timedelta(days=2)
first_day, last_day = get_month_range()
while first_day <= last_day:
    print(first_day)
    first_day += a_day
    # 2017 - 05 - 01
    # 2017 - 05 - 03
    # ...
    # 2017 - 05 - 31


#### 제너레이터 형식으로 만들기
def date_range(start, stop, step):
    while start <= stop:
        yield start
        start += step

for d in date_range(datetime(2017, 5, 1), datetime(2017, 6, 15), timedelta(hours=12)):
    print(d)
    # 2017 - 05 - 01
    # 00: 00:00
    # 2017 - 05 - 01
    # 12: 00:00
    # 2017 - 05 - 02
    # 00: 00:00
    # ...