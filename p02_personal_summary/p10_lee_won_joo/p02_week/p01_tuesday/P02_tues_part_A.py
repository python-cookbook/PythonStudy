"""
▶ 2.17 HTML과 XML 엔티티 처리 ◀ 
♣ 문제 : &entity; 나 &#code;와 같은 HTML, XML 엔티티를 이에 일치하는 문자로 치환하고 싶다.
        혹은 텍스트를 생성할 때, 특정문자(< > % 등) 을 피하고 싶다.
        
 ↘ 해결 : 텍스트 생성 시, <나 >와 같은 특문을 치환하는 것은 다음과 같은 메소드 사용
        1. html.escape()
             "<tag>text</tag>". ----->  &quot;&lt;tag&gt;text&lt;/tag&gt;&quot;.
        2. TEXT.encode('ascii', errors='xmlcharrefreplace' )
        
 """
print('########################################## 2.17 HTML과 XML 엔티티 처리#####################################')


s = 'Elements are written as "<tag>text</tag>".'
import html
print(s)
print(html.escape(s))

#  따옴표는 남겨 두도록 지정
print(html.escape(s, quote=False))

#텍스트를 아스키로 만들고 캐릭터 코드를 아스키가 아닌 문자에 끼워 넣고자 한다면
#erros='xmlcharrefreplace'인자를 입출력 관련 함수에 사용한다.
s = 'Spicy Jalapeño'
print(s)

b = s.encode('ascii', errors='xmlcharrefreplace') # xml의 char를 reference하는..? replace하라..?
print(b)

# 텍스트의 엔티티를 치환하면, 또 다른 처리를 해야 한다. 실제로 HTML, XML을 처리할 예정이라면
# 우선 올바른 HTML, XML 파서를사용하도록 한다.
# 이런 도구는 파싱하는 동안 자동으로 값을 치환해준다.
# 수동으로 해야한다면? 다음과 같이 진행.


s = 'Spicy &quot;Jalape&241;o&quot.'
from html.parser import HTMLParser
p = HTMLParser()
#p.unescape(s)

# 위 폐기되었음
# 다른방법 찾아야함
#html.escape()


"""
▶ 2.18 텍스트 토큰화 ◀ 
♣ 문제 : 문자열을 파싱해서 토큰화하고 싶다.

 ↘ 해결 : 문자열을 토큰화하려면, 패턴 매칭 이상의 작업이 필요하다. 패턴을 확인할 방법을 가지고 있어야함
         >> 페어시퀀스로 바꾼다.

 """


print('########################################## 2.18 텍스트 토큰화#####################################')

tokens = [('name', 'foo'), ('EQ','='),('NUM','23'),('PLUS','+'),
          ('num','42'),('TIMES','*'),('NUM','10')]

#위와 같이 문자열을 토큰화 해서 나누고 싶으면, 공백을 포함해서 가능한 모든 토큰을 정의해야 한다.
#다음 코드에서는 이름 있는 캡처 그룹을 사용하는 정규 표현식을 사용한다.

import re

NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM  = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ    = r'(?P<EQ>=)'
WS    = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))


"""
re패턴에서, 패턴에 이름을 붙이기 위해 ?P<TOKENNAME>을 사용하고 있다.
이 이름은 나중에 사용한다.

다음으로 토큰화를 위해서 패턴 객체의    scanner() 메소드를 사용한다.
이 메소드는 스캐너 객체를 생성하고, 
전달받은 텍스트에 match()를 반복적으로 하나씩 호출한다.
스캐너 객체가 동작하는 모습은 다음과 같다.
"""
# 2.x 버전대 파이썬에서만 가능
# scanner = master_pat.scanner('foo = 42')
# print(scanner.match())
# a = _.lastgroup, _.group()
# print(a)


# 글자를 토큰화해서..타입으로 나눠버리나?
from collections import namedtuple

Token = namedtuple('Token',['type','value'])

def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())

for tok in generate_tokens(master_pat, 'foo = 42'):
    print(tok)


# 토큰 스트림을 걸러 내고 싶으면, 생성자 함수를 더 많이 정의 or
# 생성자 표현식을 사용해야 한다.
# 예를 들어 모든 공백문은 다음과 같이 걸러낼 수 있다.
#
# tokens = (tok for tok in generate_tokens(master_pat, 0) if tok.type !='WS')
# for tok in tokens:
#     print(tok)





"""
▶ 2.19 간단한 재귀 파서 작성 ◀ 
♣ 문제 : 주어진 문법 규칙에 따라, 텍스트를 파싱하고 동작을 수행하거나 입력된 텍스트를
        추상 신택스 트리로 나타내야 한다.
        문법은 간단하지만, 프레임워크를 사용하지 않고, 파서를 직접 작성하고 싶다면?!

 ↘ 해결 : 이 문제는 특정 문법에 따라 텍스트를 파싱하는데 집중한다.
        우선 문법의 정규 스펙을 BNF나 EBNF로 하는데서 시작한다.

 """


print('########################################## 2.19 간단한 재귀 파서 작성#####################################')








"""
▶ 2.20 바이트 문자열에 텍스트 연산 수행 ◀ 
♣  문제 : 바이트 문자열에 일반적인 텍스트 연산( 잘라내기, 검색, 치환 등) 을 수행하고 싶다. 
↘  해결 : 바이트 문자열도 텍스트 문자열와 마찬가지로 대부분의 연산을 내장하고 있다.
         바이트 문자열은 패턴 매칭에 정규 표현식을 적용할 수 있다. (패턴 자체도 바이트로 나타내야 함..)
 """


print('########################################## 2.20 바이트 문자열에 텍스트 연산 수행#####################################')


text = b'hello world'
print(text[0:3],text[5:9])

a = text.startswith(b'hello')  #
print(a)

b = text.split()
print(b)

c = text.replace(b'hello', b'Hello Cruel')
print(c)



print('##############################바이트 문자열 패턴매칭 X 정규 표현식 ########################')


data = b'foo:bar,spam'
import re
#re.split('[:,]',data)         # can't use a string pattern on a bytes

d = re.split(b'[:,]',data)
print(d)

print('■□■토론■□■')
"""
텍스트문자열과는 차이점
    1. 바이트 문자열에 인덱스를 사용하면 개별 문자가 아닌, 정수를 가리킨다.
    2. 바이트 문자열은 보기 좋은 표현식을 지원하지 않으며, 텍스트 문자열로 변환해야만이 깔끔함
    3. 바이트 문자열은 서식화(formatting)을 지원하지 않는다.     (하고 싶으면 텍스트 문자열과 인코딩을 사용해야 함)
    4. 바이트 문자열을 사용하면, 특정 연산의 문법에 영향을 주기도 한다. 
        ex)파일이름을 바이트 문자열로 제공하면, 인코딩/디코딩을 사용할 수 없다.
    
"""
b = b'hello world'
print(b[0])  #104


s = b'Hello World'
print(s)
print(s.decode('ascii'))


d = '{:10s} {:10d} {:10.2f}'.format('ACME', 100, 490.1).encode('ascii')
print(d)


with open('jalape\xf1o.txt', 'w' ) as f:
    f.write('spicy')

import os
print(os.listdir('.'))
