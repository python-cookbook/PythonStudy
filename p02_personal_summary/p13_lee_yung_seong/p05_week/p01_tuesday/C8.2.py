##문자열 서식화 조절
#문제
#format함수와 문자열 메소드로 사용자가 정의한 서식화를 지원하고 싶다.
#해결
#무자열 서식화를 조절하고 싶으면 클래스에 __format__() 메소드를 정의한다.
_formats = {
    'ymd' : '{d.year}-{d.month}={d.day}'
}
class Date:
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)

#date 클래스의 인스턴스는 이제 다음과 같은 서식화를 지원한다.
d = Date(2012,12,21)
format(d)
format(d,'mdy')

#토론
#format메소드는 파이썬 문자열 서식화 함수에 후크를 제공한다. 서식화 코드의 해석은 모두 클래스 자체에 달ㄹ있다는 점이 중요하다. 따라서 코드에는 거의 모든 내용이 올 수 있다. 예를 들어 다음 datetime 모듈을 보자
from datetime import date
d = date(2012,12,21)
format(d)
format(d,'%A, %B %d, %Y')
