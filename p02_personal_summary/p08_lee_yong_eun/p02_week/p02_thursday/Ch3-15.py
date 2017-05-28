####################################################################################################
# 3.15] 문자열을 시간으로 변환
#   * 문자열 형식의 시간 데이터를 datetime 객체로 변환하고 싶다.
#
# 1] datetime.strptime()
#   : %Y, %m, %A, %B 등 원하는 서식대로 읽어서 텍스트를 날짜로 변환할 수 있다.
#     순수 파이썬만으로 구현하였고, 시스템 설정과 같은 세세한 부분을 모두 처리해야 해서 생각보다 느리다.
#     코드에서 처리할 날짜가 많은데 그 형식을 정확히 알고 있다면, 직접 해결책을 구현하는 것이 훨씬 빠르다.
# 2] datetime.strftime()
#   : datetime 객체를 사람이 이해하기 쉬운 형태로 변환할 수 있다.
####################################################################################################

from datetime import datetime
text = '2012-09-20'

## 텍스트를 날짜로 변환
y = datetime.strptime(text, '%Y-%m-%d')
print(y)    # 2012-09-20 00:00:00
z = datetime.now()
diff = z - y
print(diff) # 1707 days, 14:38:40.965992

nice_z = datetime.strftime(z, '%A %B %d, %Y')
print(nice_z)   # Wednesday May 24, 2017

## 텍스트 날짜 변환을 직접 코드로 해결('YYYY-MM-DD')
# datetime.strptime()보다 약 7배 빨랐다 !
def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))
