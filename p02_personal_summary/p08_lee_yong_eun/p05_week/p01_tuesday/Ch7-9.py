##########################################################################################################
# 7.9] 메소드가 하나인 클래스를 함수로 치환
#   * __init__() 외에 메소드가 하나뿐인 클래스가 있는데, 코드를 간결하게 만들기 위해 이를 하나의 함수로 바꾸고 싶다.
#
#   * 대개의 경우 메소드가 하나뿐인 클래스가 필요할 때는 추가적인 상태를 메소드에 저장할 때뿐이다.
#     예를 들어 UrlTemplate 클래스의 목적은 open() 메소드에서 사용하기 위해 template 값을 저장해 놓으려는 것뿐이다.
#     이럴 때 내부 함수나 클로저를 사용하면 좀 더 보기 좋게 코드를 작성할 수 있다.
##########################################################################################################

# 템플릿 스킴을 사용해서 URL을 뽑아내는 클래스
from urllib.request import urlopen

class UrlTemplate:
    def __init__(self, template):
        self.template = template
    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

# 사용 예시
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM, AAPL, FB', fields='sl1c1v'):
    print(line.decode('utf-8'))

# 클래스 대신 훨씬 간단한 함수로 치환
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener   # 함수를 반환

# 사용 예시
yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM, AAPL, FB', fields='sl1c1v'):
    print(line.decode('utf-8'))