##########################################################################################################
# 8.2] 문자열 서식화 조절
#   * format() 함수와 문자열 메소드로 사용자가 정의한 서식화를 지연하고 싶다.
#       : 문자열 서식화를 조절하고 싶으면 클래스에 __format__() 메소드를 정의한다.
#         내장 타입의 서식화에는 어느 정도 표준이 있다. 자세한 내용은 string 모듈의 문서를 참고한다.
##########################################################################################################

_formats = {
    'ymd' : '{d.year}-{d.month}-{d.day}',
    'mdy' : '{d.month}/{d.day}/{d.year}',
    'dmy' : '{d.day}/{d.month}/{d.year}'
}

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)


d = Date(2012, 12, 21)
print(format(d))        # 2012-12-21
print(format(d, 'mdy')) # 12/21/2012
print('The date is {:ymd}'.format(d))   # The date is 2012-12-21
print('The date is {:mdy}'.format(d))   # The date is 12/21/2012