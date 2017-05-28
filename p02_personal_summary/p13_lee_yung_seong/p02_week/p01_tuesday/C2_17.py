#2.17 html과 xml 엔티티 처리
#문제 &entity나 &#code; 와 같은 html, xml 엔티티를 이에 일치하는 문자로 치환하고 싶다.
#해결 텍스트를 생성할 때 <나>와 같은 특수 문자를 치환하는 것은 html.escape()함수를 사용하면 상대적으로 간단히 처리할 수 있다.
s = 'Elements are written as "<tag>text</tag>"'
import html
print(s)
print(html.escape(s))
#텍스트를 아스키로 만들고 캐릭터 코드를 아스키가 아닌 문자에 끼워 넣고 싶음
s = 'spicy jalap§no'
s.encode('ascii',errors='xmlcharrefreplace')
#텍스트의 엔티티를 치환하면 또 다른 처리를 해야 한다. 실제로 html,xml을 처리할 예정이면
#우선 올바른 html,xml 파서를 사용하도록 한다. 일반적으로 이런 도구는 파싱하는 동안 자동으로 값을 치환해준다.
#자동으로 안되었다면 수동으로 치환을 하도록 한다.
s = 'Spicy &quot;Jalape&#241;o&quot'
from html.parser import HTMLParser
p = HTMLParser()
p.unescape(s)
#토론 html,xml을 생성할 때 특수 문자를 제대로 이스케이핑하는 과정을 간과하기 쉽다.  print()로 결과물을 생성하거나 기본적인 문자열 서식기능을 사용할 때 특히 더 그렇다.
#가장 쉬운 해결책은 html.escape()와 같은 유틸리티함수를 사용하는것
#또 다른 방식으로 텍스트를 처리하고 싶담ㄴ xml.sax.saxutils.unescape()와 같은 여러 유틸리티 함수가 도움이 된다.
# 하지만 올바른 파서 방법을 익히는 것이 중요. 예를들어 html.parser나 xml.etree.ElementTree 같은 파싱 모듈로 html,xml을 처리하면 엔티티 치환과 같은 기본적인 내용을 알아서 다 처리해준다.
