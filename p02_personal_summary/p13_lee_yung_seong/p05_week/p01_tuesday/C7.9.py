#메소드가 하나인 클래스를 함수로 치환
#문제
#초기화 메소드외에 메소드가 하나인 클래스가 있는데 코드를 간결하기 위해 하나 함수로 만들고 싶다
#해결
#많은 경우 메소드가 하나뿐인 클래스는 클로저를 사용해서 함수를 바꿀 수 있다.
from urllib.request import urlopen

class UrlTemplate:
    def __init__(self,template):
        self.template=template
    def open(self,**kwargs):
        return urlopen(self.template.format_map(kwargs))

# 이 함수를 다음과 같이 간단히
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

#토론
#대개의 경우 메소드가 하나뿐인 클래슥 ㅏ필요할 때는 추가적인 상태를 메소드에 저장할 때 뿐이다.
#예를 들어 urltemplate 클래스의 목적은 open() 메소드에서 사용하기 위해 template값을 저장해 놓으려는 것 뿐이다.
#내부함수나 클로저를 사용하면 좀 더 보기 좋게 코드를 작성할 수 있다. 단순히 생각해서 클로저는 함수라고 말할 수 있지만 함수 내부에서 사용하는 변수의 환경이 있다.
#클로저의 주요 기능은 정의할 때의 환경을 기억한다는 것.




