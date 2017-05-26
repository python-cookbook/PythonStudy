#문자열을 시간으로 변환
#문제 문자열 형식의 시간 데이터를 datetime객체로 변환하고 싶다.
#헤결 파이썬 datetime을 사용하자
from datetime import datetime
text = '2012-09-20'
y = datetime.strptime(text,'%Y-%m-%d')
y
z=datetime.now()
diff = z-y
diff
#토론 strptime메소드는 네자리 연도를 표시하기 위한 %Y, 두자리 월을 표시하기 위한 %m,과 같은 서식을 지원한다. 또한 datetime 객체를 문자열로 표시하기 위해서 이 서식을 사용할 수 있다.
#예를 들어 datetime 객체를 생성하는 코드가 있는데, 이를 사람이 이해하기 쉬운 형태로 변환하고자 한다면 다음 코드를 사용한다.
z
nice_z = datetime.strptime(z,'%A %B %d, %Y')#안됨

#날짜 형식을 정확히 알고 있다면 해결책을 직접 구현하는 것이 좋음.
#YYYY-MM-DD
def parse_ymd(s):
    year_s,mon_s,day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))