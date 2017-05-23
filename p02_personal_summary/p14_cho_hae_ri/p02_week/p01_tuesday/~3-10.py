

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

s = 'Spicy Jalapeño'
a = s.encode('ascii', errors='xmlcharrefreplace')
print(a)
# b'Spicy Jalape&#241;o'


# HTML, XML 파서는 파싱하는 동안 자동으로 값을 치환해준다. 하지만 어째서인지 자동으로 처리되지 않아서 수동으로 치환해야 하는 경우에는
# HTML, XML 에 내장되어 있는 여러 유틸리티 함수나 메소드를 사용한다.

s = 'Spicy &quot;Jalape&#241;o&quot.'
from html.parser import HTMLParser
p = HTMLParser()
print(p.unescape(s)) # Spicy "Jalapeño".

t = 'The prompt is &gt;&gt;&gt;'
from xml.sax.saxutils import unescape
print(unescape(t)) # The prompt is >>>


# HTML, XML 을 생성할 때 특수 문자를 제대로 이스케이핑(escaping) 하는 과정을 간과하기 쉽다.
# 가장 좋은 방법은 html.escape() 와 같은 유틸리티 함수를 사용하는 것이다.


######################   2.18. 텍스트 토큰화  #########################

# 문제 - 문자열을 파싱에서 토큰화하고 싶다면??

# 해결 - 다음과 같은 문자열이 있다고 하자


text = 'foo = 23 + 42 * 10'

# 문자열을 토큰화하려면 패턴 매칭 이상의 작업이 필요하다. 패턴을 확인할 방법을 가지고 있어야 한다.
# 예를 들어, 문자열을 다음고 ㅏ같은 페어 시퀀스로 바꾸고 싶다.

tokens = [('NAME', 'foo'), ('EQ','='), ('NUM', '23'), ('PLUS','+'),
    ('NUM', '42'), ('TIMES', '*'), ('NUM', '10')]

# 이런 나누기 작업을 하기 위해서는 공백을 포함해서 가능한 모든 토큰을 정의해야 한다.
# 다음 코드에서는 이름있는 캡쳐 그룹을 사용하는 정규 표현식을 사용한다.

import re
NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))

# re 패턴에서, 패턴에 이름을 붙이기 위해 ?P<TOKENNAME> 을 사용하고 있다.
# 다음으로 토큰화를 위해서 패턴 객체의 잘 알려지지 않은 scanner() 메소드를 사용한다.
# 이 메소드는 스캐너 객체를 생성하고 전달받은 텍스트에 match() 를 반복적으로 하나씩 호출한다.
#
#  스캐너 객체가 동작하는 모습은 다음 예제를 통해 확인하자
'''
scanner = master_pat.scanner('foo = 42')
print(scanner.match())
#<_sre.SRE_Match object; span=(0, 3), match='foo'>

print(_.lastgroup, _.group())
#('NAME', 'foo')
scanner.match()
#<_sre.SRE_Match object at 0x100677738>
_.lastgroup, _.group()
#('WS', ' ')
scanner.match()
#<_sre.SRE_Match object at 0x100677738>
_.lastgroup, _.group()
#('EQ', '=')
scanner.match()
#<_sre.SRE_Match object at 0x100677738>

_.lastgroup, _.group()
#('WS', ' ')
scanner.match()
#<_sre.SRE_Match object at 0x100677738>
_.lastgroup, _.group()
#('NUM', '42')
scanner.match()
'''

# 와우. 어떻게 동작한다는 건지 전혀 모르겠당

# 이제 이 기술을 코드에 사용해 보자. 다음과 같이 간단한 생성자를 만들 수 있다.

from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.goup())


# 사용 예

for tok in generate_tokens(master_pat, 'foo = 42'):
    print(tok)

'''
# 오류가 나는 것은 위의 _.lastgroup, _.group() 을 수행하지 못했기 때문!!

Traceback (most recent call last):
  File "<input>", line 59, in <module>
  File "<input>", line 54, in generate_tokens
AttributeError: '_sre.SRE_Match' object has no attribute 'goup'


'''


# 보통 더 복잡한 텍스트 파싱이나 처리를 하기 전에 토큰화를 한다. 앞에서 나온 스캔 기술을 사용하려면 다음 몇 가지 중요한 사항을 기억하자
# 우선 입력부에 나타나는 모든 텍스트 시퀀스를 re 패턴으로 확인해야 한다. 매칭하지 않는 텍스가 하나라도 있으면 스캐닝이 멈춘다.
# 공백 토큰을 명시할 필요가 있었던 이유도 마찬가지다.
# 마스터 정규 표현식의 토큰 순서도 중요하다. re는 명시한 순서대로 패턴을 매칭하기 때문에
# 한 패턴이 다른 패턴의 부분이 되는 경우가 있다면 항상 더 킨 패턴을 먼저 넣어야 한다.


LT = r'(?P<LT><)'
LE = r'(?P<LE><=)'
EQ = r'(?P<EQ>=)'

master_pat = re.compile('|'.join([LE, LT, EQ])) # Correct
# master_pat = re.compile('|'.join([LT, LE, EQ])) # Incorrect









