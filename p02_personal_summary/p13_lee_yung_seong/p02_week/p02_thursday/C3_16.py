#시간대 관련 날짜 처리
#문제 시카고 시간으로 2012년 12월 21일 오전 9시 30분에 화상 회의가 예정디ㅗ어 있다. 그렇다면 인도의 방갈로르에 있는 친구는 몇시에 회의실에 와야할까?
#해결 : 시간대와 관련있는 거의 모든 문제는 pytz모듈로 해결한다. 이 패키지는 많은 언어와 운영체제에서 기본적으로 사용하는 Olson시간대 데이터베이스를 제공한다.
#pytz는 주로 datetime 라이브러리에서 생성한 날짜를 현지화 할 때 사용한다.
#시카고 시간
from datetime import datetime,timedelta
import pytz
d = datetime(2012,12,21,9,30,0)
print(d)

#시카고에 맞게 현지화
central = timezone('US/Central')
loc_d = central.localize(d)
print(loc_d)
#날짜를 현지화 하고 나면 다른 시간대로 변환 가능. 방갈로르의 동일 시간을 구하려면 다음과 같다.
bang_d = loc_d.astimezone(timezone('Asia/Kolkata'))
print(bang_d)
#변환된 시간에 산술 연산을 하려면 서머타임제 등을 알고 있어야 한다. 예를 들어 2013년 미국에서 표준 서머타임은 3/13 오후 2시에 시작한다. 이를 고려하지 않고 계산하면 계산결과가 잘못된다.
d = datetime(2013,3,10,1,45)
loc_d = central.localize(d)
print(loc_d)
later = loc_d + timedelta(minutes=30)
print(later)#틀림 생략된 서머타임을 고려하지 않았기 때문.
#답
later = central.normalize(loc_d+timedelta(minutes=30))
print(later)
#토론 : 현지화된 날짜를 조금 더 쉽게 다루기 위한 한가지 전략으로 모든 날짜를 UTC시간으로 변환해 놓고 사용하는 것이 있다.
print(loc_d)
utc_d = loc_d.astimezone(pytz.utc)
print(utc_d)
#시간대 관련 작업 중 생기는 문제 중 한가지로 어떤 이름을 사용할지 결정하는 것이 있다. 예를 들어 이번 레시피에서 인도의 시간대 이름이
#'Asia/Kolkata"라는 것을 어떻게 알았을까? 이를 알아내기 위해서
pytz.country_timezones('IN')#이렇게 사용
#IN부분은 ISO 3166국가 코드를 사용한다.