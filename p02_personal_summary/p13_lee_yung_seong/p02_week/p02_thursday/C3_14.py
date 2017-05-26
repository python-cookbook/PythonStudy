#현재 달의 날짜 범위 찾기
#문제 : 현재 달의 날짜를 순환해야 하는 코득 ㅏ있고 그 날짜 범위를 계산하는 효율적인 방법이 필요.
#해결 : 날짜를 순환하기 위해 모든 날짜를 리스트로 만들 필요 없음. 대신 범위의 시작일자와 마지막 날짜만 계산하고 datetime.timedelta 객체를 사용해서 날짜를 증가시키면 된다.
#datetime 객체를 받아서 그 달의 첫번째 날짜와 다음 달의 시작 날짜를 반환하는 함수 코드는 다음과 같다.
from datetime import datetime, date, timedelta
import calendar
def get_month_range(start_date = None):
    if start_date is None:
        start_date = date.today().replace(day=1)
    _, days_in_month = calendar.monthrange(start_date.year,start_date.month)
    end_date = start_date + timedelta(days=days_in_month)
    return (start_date,end_date)

a_day = timedelta(days=1)
first_day,last_day = get_month_range()
while first_day < last_day:
    print(first_day)
    first_day += a_day

#이번 레시피는 우선 월의 첫 번째 날을 계산하는 데서 시작. 첫째 날을 간단히 구하기 위해서 date의 replace()메소드에 days속성을 1로 설정.
#이상적으로는 내장함수 range()처럼 동작하는 함수를 만드는 것이 좋음. 발생자(제너레이터)를 사용하면 쉽게 구현
def date_range(start,stop,step):
    while start < stop:
        yield start
        start += step

for d in date_range(datetime(2012,9,1),datetime(2012,10,1),timedelta(hours=6)):
    print(d)