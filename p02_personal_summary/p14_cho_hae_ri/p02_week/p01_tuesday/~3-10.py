

###########  2.17 HTML 과 XML 엔티티 처리  #################

# 문제 - &entity; 나 &#code; 와 같은 HTML, XML 엔티티를 이에 일치하는 문자로 치환하고 싶다.
#        또는 텍스트를 생성할 때 특정 문자 (>, <, & 등) 를 피하고 싶다.

s = 'Elements are written as "<tag>text<\\tag>".'
import html
print(s)
# Elements are written as "<tag>text<\tag>".

print(html.escape(html.escape(s)))
# Elements are written as &amp;quot;&amp;lt;tag&amp;gt;text&amp;lt;\tag&amp;gt;&amp;quot;.

# 따옴표는 남겨두도록 지정하려면
print(html.escape(s, quote=False))
# Elements are written as "&lt;tag&gt;text&lt;\tag&gt;".

# 텍스트를 아스키(ASCII) 로 만들고 캐릭터 코드를 아스키가 아닌 문자에 끼워 넣고 싶으면  errors='xmlcharrefreplace' 인자를
# 입출력 관련 함수에 사용한다.

s = 'Spicy Jala'