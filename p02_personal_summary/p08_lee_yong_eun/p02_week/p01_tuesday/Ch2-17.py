####################################################################################################
# 2.17] HTML과 XML 엔티티 처리
#   * &entity;나 &#code;와 같은 html, xml 엔티티를 해당 문자로 치환하고 싶다.
#     혹은 텍스트를 생성할 때 특정 문자(<. >, & 등)을 피하고 싶다.
#
# 1] html.escape()
#   : 특수 문자를 html 엔티티로 치환
#
#   * 텍스트를 처리하는 것도 좋지만, 더 중요한 것은 올바른 Parser 사용법을 익히는 것이다.
#     파싱 모듈로 처리를 잘 하면 엔티티 치환과 같은 기본적인 내용은 알아서 다 처리해 준다.
####################################################################################################

s = 'Elements are written as "<tag>text</tag>".'
import html
print(s)                # Elements are written as "<tag>text</tag>".
print(html.escape(s))   # Elements are written as &quot;&lt;tag&gt;text&lt;/tag&gt;&quot;.
print(html.escape(s, quote=False))  # 쌍따옴표는 남겨두도록 지정 : Elements are written as "&lt;tag&gt;text&lt;/tag&gt;".

