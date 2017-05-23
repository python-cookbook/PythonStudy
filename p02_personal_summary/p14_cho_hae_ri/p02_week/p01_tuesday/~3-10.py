

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



############################  chapter 3. 숫자, 날짜, 시간  ################################

# 파이썬에서 분수, 배열, 날짜, 시간 계산하기!!!


# 3.1 반올림

# 문제 - 부동 소수점 값을 10진수로 반올림하고 싶다.

# 해결 - 간단한 반올림은 내장 함수인 round() 함수를 사용한다.

round(1.23, 1)

round(1.27, 1)

round(-1.27, 1)

round(1.23543, 3)


# 값이 정확히 두 선택지의 가운데 있으면 더 가까운 짝수가 된다. 예를 들어 1.5 와 2.5 는 모두 2가 된다.
# round() 에 전달하는 자릿수는 음수가 될 수 있다. 이 경우에는 10의 자리, 100의 자리 등의 순으로 자릿수가 결정된다.

a = 1627731
round(a, -1)
#1627730
round(a, -2)
#1627700
round(a, -3)
#1628000

# 반올림과 서식화를 헷갈리지 않도록 주의하자.특정 자릿수까지 숫자를 표현하는 것이 목적이라면
# 서식화를 위한 자릿수를 명시하기만 하면 된다.

x = 1.23456
format(x, '0.2f')
#'1.23'
format(x, '0.3f')
#'1.235'
'value is {:0.3f}'.format(x)
#'value is 1.235'


# 또한 정확도 문제를 "수정하려고" 부동 소수점을 반올림하는 방법도 지양해야 한다.
# 다음의 코드를 보자

a = 2.1
b = 4.2
c = a + b
print(c)
#6.300000000000001
c = round(c, 2)     # 결과를 "수정한다" (???)
print(c)
#6.3


# 부동 소수점 계산을 하는 대부분의 app 에서 이런 코드는 불필요하다.(권장하지 않는다)
# 하지만 이런 작은 오류를 절대로 피해야 한다면(금융 app 등) decimal 모듈을 사용한다.


################## 3.2 정확한 10진수 계산  ###################

# 문제 - 정확한 10진수 계산을 해야 하고, 부동 소수점을 사용할 때 발생하는 작은 오류를 피하고 싶다면

# 해결 - 부동 소수점 값에는 10진수를 아주 정확히 표현하지 못한다는 단점이 있다.
# 심지어 아주 작은 계산을 하더라도 오류가 발생하기도 한다.

a = 4.2
b = 2.1
print(a + b)
#6.300000000000001
(a + b) == 6.3
#False


## 위 오류는 float를 사용해도 피할 수 없다. 하지만 더 정확한 계산을 하고 싶다면(그리고 성능 측면에서 희생할 용의가 있다면)
## decimal 모듈을 사용한다.

from decimal import Decimal
a = Decimal('4.2')
b = Decimal('2.1')
print(a + b == Decimal('6.3'))  # True

# 숫자를 문자열로 표현하는 이 모듈이 이상해 보일수 있다. 그러나 Decimal 객체는 우리가 기대하는 모든 동작을 정확하게 수행한다.
# 문자열 서식화 함수에 사용하거나 출력하면 마치 일반적인 숫자처럼 보인다.

#  Decimal 의 중요한 기능으로 반올림의 자릿수와 같은 계산적 측면을 조절할 수 있다는 점이 있다.

from decimal import localcontext
a = Decimal('1.3')
b = Decimal('1.7')
print(a / b)    # 0.7647058823529411764705882353

with localcontext() as ctx:
    ctx.prec = 3
    print(a / b)
# 0.765
with localcontext() as ctx:
    ctx.prec = 50
    print(a / b)
# 0.76470588235294117647058823529411764705882352941176



#  Decimal 모듈에 비해 float 의 속도 가 훨씬 빠르다. 그래서 보통은 float 을 사용하는 것이 더 유리하겠다.
# 금융 등 숫자 계산을 철저히 해야하는 분야라면 decimal 객체를 사용해야 한다.

nums = [1.23e+18, 1, -1.23e+18]
sum(nums)       # 1이 사라진다.
#0.0

# fsum 을 사용해 더 정확히 계산할 수 있다.

import math
math.fsum(nums)
#1.0



###########################  3. 3 출력을 위한 숫자 서식화  #############################

#문제 - 출력을 위해 자릿수, 정렬, 천 단위 구분 등 숫자를 서식화 하고 싶다면

# 해결 - 출력을 위해 숫자를 서식화하려면 내장 함수인 format() 을 사용한다.

x = 1234.56789

# 소수점 둘째 자리 정확도
format(x, '0.2f')
#'1234.57'

#소수점 한 자리 정확도로 문자 10개 기준 오른쪽에서 정렬
format(x, '>10.1f')
#'    1234.6'

# 왼쪽에서 정렬
format(x, '<10.1f')
#'1234.6    '

# 가운데 정렬
format(x, '^10.1f')
#'  1234.6  '

# 천 단위 구분자 넣기
format(x, ',')
#'1,234.56789'

format(x, '0,.1f')
#'1,234.6'


# 지수 표현법을 사용하려면 f를 e나 E로 바꾸면 된다.

format(x, 'e')
#'1.234568e+03'

format(x, '0.2E')
#'1.23E+03'


# 출력을 위한 숫자 서식화는 대개 간단하다. 자릿수를 제한하면 round() 함수와 동일한 규칙으로 반올림한다.

x = 1234.56789

x
#1234.56789

format(x, '0.1f')
#'1234.6'

format(-x, '0.1f')
#'-1234.6'


## 천 단위 구분자는 지역 표기법을 따르지 않는다. 이를 염두에 둔다면 locale 모듈의 함수를 사용한다.
# translate() 메소드를 사용하면 구분자 문자를 변경할 수도 있다.

swap_separators = { ord('.'):',', ord(','):'.' }
format(x, ',').translate(swap_separators)
#'1.234,56789'


# 많은 파이썬 코드에서 숫자를 % 연산자로 서식화한다.

'%0.2f' % x
#'1234.57'

'%10.1f' % x
#'    1234.6'

'%-10.1f' % x
#'1234.6    '


# 이 기능도 괜찮지만 format() 을 사용하는 것만큼 기능이 많지는 않다. 1000단위 구분자를 넣는 등의 기능은 % 연산자에서 지원하지 않는다.



#############################  3. 4 2진수, 8진수, 16진수 작업  ###############################


# 문제 - 숫자를 2진수, 8진수, 16진수로 출력해야 한다

# 해결 - 정수를 2진수 , 8진수, 16진수 문자열로 변환하려면 bin(), oct(), hex()를 사용한다.

x = 1234
bin(x)
#'0b10011010010'

oct(x)
#'0o2322'

hex(x)
#'0x4d2'


# 숫자 앞에 0b, 0o, 0x 가 붙는 것이 싫다면 format() 함수를 사용한다.

format(x, 'b')
#'10011010010'
format(x, 'o')
#'2322'
format(x, 'x')
#'4d2'


# 정수형은 부호가 있는 숫자이므로, 음수를 사용하면 결과물에도 부호가 붙는다.

x = -1234
format(x, 'b')
#'-10011010010'

format(x, 'x')
#'-4d2'


# 부호가 없는 값을 사용하려면 최대값을 더해서 비트 길이를 설정해야 한다. 예를 들어 32 비트 값을 보여주려면 아래와 같이

x = -1234
format(2**32 + x, 'b')
#'11111111111111111111101100101110'

format(2**32 + x, 'x')
#'fffffb2e'


# 다른 진법의 숫자를 정수형으로 변환하려면 int() 함수에 적절한 진수를 전달한다.

int('4d2', 16)
#1234

int('10011010010', 2)
#1234


#  2진수 , 8진수, 16진수 변환은 대개 간단하게 해결할 수 있다.
# 파이썬이 8진법을 나타내는 방식은 다른 언어와 약간 다르므로 주의해야 한다.

import os
os.chmod('script.py', 0755)
##SyntaxError: invalid token


# 8진법 값 앞에는 0o를 붙여야 한다.

os.chmod('script.py', 0o755)




###################  3.5 바이트에서 큰 숫자를 패킹/ 언패킹  ########################

# 문제 - 바이트 문자열을 언패킹해서 정수 값으로 만들어야 한다. or 매우 큰 정수 값을 바이트 문자열로 변환해야 한다!

# 해결 - 프로그램에서 128비트 정수 값을 담을 수 있는, 길이 16의 바이트 문자열을 다루어야 한다고 가정해보자.

data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'

# 바이트를 정수형으로 변환하려면 int.from_bytes() 를 사용하고 바이트 순서를 명시한다.

len(data)
#16

int.from_bytes(data, 'little')
#69120565665751139577663547927094891008

int.from_bytes(data, 'big')
#94522842520747284487117727783387188


# 큰 정수값을 바이트 문자열로 변환하려면 int.to_bytes() 메소드를 사용하고, 바이트 길이와 순서를 명시한다.

x = 94522842520747284487117727783387188

x.to_bytes(16, 'big')
#b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'

x.to_bytes(16, 'little')
#b'4\x00#\x00\x01\xef\xcd\x00\xab\x90x\x00V4\x12\x00


# 정수형 값과 바이트 문자열 ㄱ간의 변환은 일반적인 작업이 아니다. 하지만 네트워크나 암호화 가 필요한 특정 앱에서 사용하는 경우가 있긴 하다.


# 바이트 순서(little or big)은 정수형을 이루는 바이트가 가장 작은 것부터 표시되었는지 큰것부터 표시되었는지를 나타낸다.
# 16진수 값을 사용해서 이에 대한 예를 들어보자.

x = 0x01020304

x.to_bytes(4, 'big')
#b'\x01\x02\x03\x04'

x.to_bytes(4, 'little')
#b'\x04\x03\x02\x01'


# 정수형 값을 바이트 문자열로 변환하려는데 지정한 길이에 다 들어가지 않는다면 에러가 발생한다.
# 이를 방지하려면 int.bit_length() 메소드를 사용해서 얼마나 많은 비트가 필요한지를 미리 알 수 있다.

x = 523 ** 23

x
#335381300113661875107536852714019056160355655333978849017944067

x.to_bytes(16, 'little')
#OverflowError: int too big to convert

x.bit_length()
#208

nbytes, rem = divmod(x.bit_length(), 8)

if rem:
    nbytes += 1

x.to_bytes(nbytes, 'little')
#b'\x03X\xf1\x82iT\x96\xac\xc7c\x16\xf3\xb9\xcf...\xd0'




###########################  3.6 복소수 계산  #################################

# 문제 - 최신 웹 인증을 사용하는 코드를 작성하더 ㄴ도중에 특이점을 발견하고 복소수 평면을 사용할 수밖에 없는 상황에 처함.
# 혹은 복소수를 사용해서 계산을 해야 한다.


# 해결 - 복소수는 complex(real, imag) 함수를 사용하거나 j를 붙인 부동 소수점 값으로 표현할 수 있다.

a = complex(2, 4)

b = 3 - 5j

a
#(2+4j)
b
#(3-5j)


# 실수, 허수, 켤레 복소수를 구하는 방법은 어렵지 않다.

a.real
# 2.0

a.imag
# 4.0

a.conjugate()
# (2-4j)


# 또한 일반적인 수학 계산도 잘 동작한다.

a + b
#(5-1j)

a * b
#(26+2j)

a / b
#(-0.4117647058823529+0.6470588235294118j)

abs(a)
#4.47213595499958

# 사인, 코사인, 제곱 등을 계산하려면 cmath 모듈을 사용한다.

import cmath

cmath.sin(a)
#(24.83130584894638-11.356612711218174j)

cmath.cos(a)
#(-11.36423470640106-24.814651485634187j)

cmath.exp(a)
#(-4.829809383269385-5.5920560936409816j)


# 파이썬의 수학 관련 모듈을 대개 복소수를 인식한다. 예를 들어, numpy 모듈을 사용해 복소수 배열을 어렵지 않게 만들 수 있다.

import numpy as np

a = np.array([2+3j, 4+5j, 6-7j, 8+9j])

a
#array([ 2.+3.j,  4.+5.j,  6.-7.j,  8.+9.j])

a + 2
#array([  4.+3.j,   6.+5.j,   8.-7.j,  10.+9.j])

np.sin(a)
#array([    9.15449915  -4.16890696j,   -56.16227422 -48.50245524j,
#        -153.20827755-526.47684926j,  4008.42651446-589.49948373j])



# 하지만 파이썬의 표준 수학 함수는 기본적으로 복소수 값을 만들지 않는다. 따라서 코드에서 이런 값이 항상 예상치 않게 발생하지는 않는다.

import math
math.sqrt(-1)
#ValueError: math domain error


# 계산결과로 복소수를 얻으려면 명시적으로 cmath를 사용하거나 라이브러리에서 복소수 사용을 선언해야 한다.

import cmath
cmath.sqrt(-1)
#1j





##########################  3.7 무한대와 NaN 사용  #################################

# 문제 - 부동 소수점 값의 무한대, 음의 무한대,  NaN(NOT A NUMBER) 를 검사해야 한다.

# 해결 - 이와 같은 특별한 부동 소수점 값을 표현하는 파이썬 문법을 없지만 FLOAT() 을 사용해서 만들 수는 있다.

a = float('inf')
b = float('-inf')
c = float('nan')

a
#inf
b
#-inf
c
#nan


# 이 값을 확인하려면 math.isinf()와 math.isnan() 함수를 사용한다.

math.isinf(a)
#True

math.isnan(c)
#True



# 앞에 나온 부동 소수점 값에 대한 더 많은 정보를 원한다면 IEEE 754스펙을 확인해야 함.

# 무한대 값은 일반적인 수학 계산법을 따른다.

a = float('inf')
a + 45
#inf

a * 10
#inf

10 / a
#0.0

# 하지만 특정 연산자의 계산은 정의되어 있지 않고 NaN을 발생시킨다.

a = float('inf')

a/a
#nan

b = float('-inf')
a + b
#nan


# nan 값은 모든 연산자에 대해 예외를 발생시키지 않는다.

c = float('nan')
c + 23
#nan

c / 2
#nan

c * 2
#nan

math.sqrt(c)
#nan

# nan 에서 주의해야 할 점은, 이 값은 절대로 비교 결과가 일치하지 않는다는 점이다.

c = float('nan')
d = float('nan')

c == d
#False

c is d
#False


# 따라서 nan 을 비교하는 방법은 math.isnan() 을 사용하는 것 뿐이다.





############################## 3.8 분수 계산 ###############################

# 문제 - 분수 계산을 해야 한다.

# 해결 = fractions 모듈을 사용한다.


from fractions import Fraction
a = Fraction(5, 4)
b = Fraction(7, 16)
print(a + b)            # 27/16
print(a * b)            # 35/64

# Getting numerator/denominator
c = a * b
print(c.numerator)      # 35
print(c.denominator)    # 64

# Converting to a float
print(float(c))         # 0.546875

# Limiting the denominator of a value
print(c.limit_denominator(8))   # 4/7

# Converting a float to a fraction
x = 3.75
y = Fraction(*x.as_intager_ratio())
print(y)                # Fraction(15, 4)


# 사실 프로그래밍에서 분수 계산을 많이 할 일이 없다.....




######################### 3.9 큰 배열 계산 ########################


# 문제 - 배열이나 그리드와 같이 커다란 숫자 데이터셋에 계산을 해야 한다면

# 해결 = 배열이 관련된 커다란 계산을 하려면 numpy 라이브러리를 사용한다.



# 파이썬 리스트와 numpy 의 차이점을 보여주는 간단한 예제

# Python lists
x = [1, 2, 3, 4]
y = [5, 6, 7, 8]
x * 2
#[1, 2, 3, 4, 1, 2, 3, 4]

x + 10
#TypeError: can only cancatenate list (not "int") to list

x + y
#[1, 2, 3, 4, 5, 6, 7, 8]

# NumPy arrays
import numpy as np
ax = np.array([1, 2, 3, 4])
ay = np.array([5, 6, 7, 8])

ax * 2
#array([ 2, 4, 6, 8])
ax + 10
#array([11, 12, 13, 14])
ax + ay
#array([ 6, 8, 10, 12])
ax * ay
#array([ 5, 12, 21, 32])


# 다항식을 계산하고 싶으면 다음과 같이 한다.






