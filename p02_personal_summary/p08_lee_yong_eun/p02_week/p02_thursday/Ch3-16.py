####################################################################################################
# 3.16] 시간대 관련 날짜 처리
#   * 시카고 시간으로 2012년 12월 21일 오전 9시 30분에 화상 회의가 예정되어 있다.
#     그렇다면 인도의 방갈로르에 있는 친구는 몇 시에 회의실에 와야 할까?
#
# 1] pytz
#   : 시간대와 관련된 거의 모든 문제는 이 모듈로 해결할 수 있다 !
#
# * 서머타임제로 인한 오류 방지
#   1) normalize 함수 사용
#   2) UTC 시간에서의 처리 후 원하는 시간대로 변환
#
# * 시간대 이름 알아내기
#   : pytz.country_timezones 딕셔너리 사용
#     키값 : ISO 3166 국가코드
####################################################################################################

from datetime import datetime, timedelta
from pytz import timezone
import pytz

d = datetime(2012, 12, 21, 9, 30, 0)
print(d)

# 시카고에 맞게 현지화
central = timezone('US/Central')
loc_d = central.localize(d)
print(loc_d)

# 방갈로르 시간으로 변환
bang_d = loc_d.astimezone(timezone('Asia/Kolkata'))
print(bang_d)


## 서머타임제 : 중간에 한시간 생략되는 영역이 있다.
## 이를 고려하지 않으면 계산 결과가 잘못된다 !
d = datetime(2013, 3, 10, 1 ,45)
loc_d = central.localize(d)
print(loc_d)    # 2013-03-10 01:45:00-06:00
later = loc_d + timedelta(minutes=30)
print(later)    # 2013-03-10 02:15:00-06:00 : 잘못된 결과 !

## normalize를 이용한 서머타임제 대비
later = central.normalize(loc_d + timedelta(minutes=30))
print(later)    # 2013-03-10 03:15:00-05:00 : 올바른 결과

## UTC 시간 사용
print(loc_d)    # 2013-03-10 01:45:00-06:00
utc_d = loc_d.astimezone(pytz.utc)
print(utc_d)    # 2013-03-10 07:45:00+00:00
later_utc = utc_d + timedelta(minutes=30)
print(later_utc.astimezone(central))    # 2013-03-10 03:15:00-05:00


## 각 나라의 시간대 이름 알아내기
print(pytz.country_timezones['IN']) # ['Asia/Kolkata'] : 인도