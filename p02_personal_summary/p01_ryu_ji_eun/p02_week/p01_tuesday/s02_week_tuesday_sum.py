#=======================================================================================================================
# 2.17 HTML과 XML 엔티티 처리
# HTML, XML 엔티티를 이에 일치하는 문자로 치환하고 싶다.
# ㄴ html.escape()를 쓰면 된다
#=======================================================================================================================

s = 'Elements are written as "<tag>text</tag>".'
import html
# print(s)
# print(html.escape(s))
print(html.escape(s, quote=False))

## 다른 방식으로 처리하고 싶다면 xml.sax.saxutils.unescape()같은 유틸 함수를 쓰도록. XML인지 HMTL인지를 처리해주는 거.
# 하지만 가급적 html.parser나 xml.etree.ElementTree 같은 파싱 모듈로 html, xml을 처리하셈


#=======================================================================================================================
# 2.18 텍스트 토큰화
# 문자열을 파싱해서 토근화하고 싶다
#=======================================================================================================================

text = 'foo = 23 + 42 * 10'

## 페어 시퀀스로 바꾸기 pair sequence
tokens = [('NAME','foo'),('EQ','='),('NUM','23'),('PLUS','+'),('NUM','42'),('TIMES','*'),('NUM','10')]


import re
NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'          # r' 정규식
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))



## scanner
from collections import namedtuple
Token = namedtuple('Token',['type','value'])

def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())

for tok in generate_tokens(master_pat, 'foo = 42'):
    print(tok)


## 공백문 걸러내기
tokens = (tok for tok in generate_tokens(master_pat, text)
          if tok.type != 'WS')

for tok in tokens:
    print(tok)

## 토큰은 항상 가장 긴 것을 앞으로
LT = r'(?P<LT><)'           # < 1개
LE = r'(?P<LE><=)'          # < 와  = 의 2개
EQ = r'(?P<EQ>=)'           # = 1개

master_pat = re.compile('|'.join([LE,LT,EQ]))           # 가장 긴 걸 항상 앞으로


#=======================================================================================================================
# 2.19 간단한 재귀 파서 작성
# 프레임 워크를 사용하지 않고 파서를 직접 작성하고 싶다
#=======================================================================================================================

## 재귀 표현식 해석기를 만드는 간단한 방식(...)을 살펴보자

import re
import collections

NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS]))

Token = collections.namedtuple('Token',['type','value'])

def generate_tokens(text):
    scanner = master_pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok



class ExpressionEvaluator:
    '''
    재귀 파서 구현, 모든 메소드는 하나의 문법 규칙을 구현한다.
    룩어헤드 토큰을 받고 테스트하는 용도로 ._accpet()를 사용한다.
    '''
    def parse(self,text):
        self.tokens = generate_tokens(text)
        self.tok = None
        self.nexttok = None
        self._advance()
        return self.expr()


    def _advance(self):
        'Advance one token ahead'
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        'Test and consume the next token if it matches toktype'
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self,toktype):
        'Consume next token if it matches toktype or raise SyntaxError'
        if not self._accept(toktype):
            raise SyntaxError('Expected '+toktype)

    def expr(self):
        "expression ::= term { ('+'|'-') term}*"
        exprval = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.tok.type
            right = self.term()
            if op == 'PLUS':
                exprval += right
            elif op == 'MINUS':
                exprval -= right
        return exprval

    def term(self):
        "term ::= factor{('*'|'/') factor}*"
        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            if op == 'TIMES':
                termval *= right
            elif op == 'DIVIDE':
                termval /= right
        return termval


    def facrot(self):
        "factor ::= NUM | (expr)"

        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')


## 간단한 파싱 트리 만드는 구현식
class ExpressionTreeBuilder(ExpressionEvaluator):
    def expr(self):
        "expression ::= term{'+'|'-') term}"
        exprval = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.tok.type
            right = self.term()
            if op == 'PLUS':
                exprval = ('+',exprval,right)
            elif op == 'MINUS':
                exprval = ('-',exprval,right)
        return exprval

    def term(self):
        "term ::= facrot {('*'|'/') factor}"
        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            if op == 'TIMES':
                termval = ('*',termval,right)
            elif op == 'DIVIDE':
                termval = ('/',termval,right)
        return termval

    def factor(self):
        'factor ::= NUM | (expr)'
        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')

## 사용법
e = ExpressionTreeBuilder()
e.parse('2 + 3')

# ...와 진짜 모르겠다.

#=======================================================================================================================
# 2.20 바이트 문자열에 텍스트 연산 수행
# 바이트 문자열에 일반적인 텍스트 연산(잘라내기, 검색, 치환 등)을 수행하고 싶다
# ㄴ 내장하고 있는 연산을 쓴다
#=======================================================================================================================
data = b'Hello World'                               # b' 바이트 문자열
print(data[0:5])

print(data.startswith(b'Hello'))
print(data.split())
print(data.replace(b'Hello',b'Hello Cruel'))         # Hello를 Hello Cruel로 치환해서 결과물은 Hello cruel world가 됨

## 위의 동작을 바이트 배열에 쓸 때
data = bytearray(b'Hello World')
print(data[0:5])

print(data.startswith(b'Hello'))
print(data.split())
print(data.replace(b'Hello',b'Hello Cruel'))


# 정규식을 쓸 때엔 패턴도 바이트로 써야함
data = b'Foo:BAR,SPAM'
import re
print(re.split(b'[:,]',data))

## 텍스트 문자열과 달리 바이트 문자열에 인덱스를 쓰면 정수를 가리킴
b = b'Hello world'
print(b[0])                             # 72가 나옴
print(b[1])                             # 101이 나옴

# 바이트 문자열은 formatting을 미지원함  '{} {}'.format(0,1) 요게 안됨
# 쓰는 사람도 멘붕이지만 보는 사람은 더 멘붕일 것이므로, 가급적 텍스트 문자열을 쓰자


#=======================================================================================================================
# 3.1 반올림
# 부동 소수점 값을 10진수로 반올림하고 싶다
# ㄴ 간단한 반올림은 round(value, ndigits)를 사용
#=======================================================================================================================

print(round(1.23,1))      # 1은 0.00 << 요 자리에서 반올림되어짐    결과값 : 1.2
print(round(1.27,1))      # 결과값 1.3
print(round(-1.27,1))     # 결과값 -1.3
print(round(1.25361,3))   # 결과값 1.254

## round()에 음수를 넣을 수 있다.
a = 1627731
print(round(a,-1))          # 1627730
print(round(a,-2))          # 1627700
print(round(a,-3))          # 1628000

## 반올림은 올려주는거고, 서식화는 해당 부분까지만 표시해주는 것으로 구분토록 하자

x = 1.23456
print(format(x,'0.2f'))             # 1.23
print('Value is {:0.3f}'.format(x))     # Value is 1.235


#=======================================================================================================================
# 3.2 정확한 10진수 계산
# 정확한 10진수를 계산해야하고, 부동 소수점을 사용할 때 발생하는 작은 오류가 안 났으면 싶다
# ㄴ 이름 예쁜 decimal 씀
#=======================================================================================================================
from decimal import Decimal
a = Decimal('4.2')
b = Decimal('2.1')
print(a + b)                             # 6.3
print((a+b) == Decimal('6.3'))          # True

## decimal은 반올림 자릿수를 조절할 수 있다
from decimal import localcontext
a = Decimal('1.3')
b = Decimal('1.7')
print(a/b)                              # 0.7647058823529411764705882353

with localcontext() as ctx:
    ctx.prec = 3
    print(a/b)                          # 0.765

with localcontext() as ctx:
    ctx.prec = 50
    print(a/b)                          # 0.76470588235294117647058823529411764705882352941176


## 정말 정밀한 계산을 요구하는 금융계가 아니면 그냥 float 써라. 속도도 decimal보다 훨씬 빠르다.
nums = [1.23e+18,1,-1.23e+18]
print(sum(nums))                    # 0.0이 나옴. 1이 사라진다

# 위와 같은 상황에서는 math.fsum()을 쓰면 된다.
import math
print(math.fsum(nums))              # 1.0이 나옴.


#=======================================================================================================================
# 3.3 출력을 위한 숫자 서식화
# 출력을 위해 자릿수, 정렬, 천 단위 구분 등 숫자를 서식화하고 싶다
# ㄴ format()
#=======================================================================================================================
x = 1234.56789

print(format(x,'0.2f'))         # 1234.57
print(format(x,'>10.1f'))       #     1234.6
print(format(x,'<10.1f'))       # 1234.6
print(format(x,'^10.1f'))       #   1234.6
print(format(x,','))             # 1,234.56789
print(format(x,'0,.1f'))        # 1,234.6

# 지수를 쓸려면
print(format(x,'e'))
print(x,'0.2E')

## 너비와 자릿수 나타내기 '[<>^]?너비[,]?(.자릿수)?'       너비와 자릿수는 정수형 표시. ?는 선택 사항
print('The value is {:0,.2f}'.format(x))
# 결과 : The value is 1,234.57

# 구분자를 변경하고 싶으면 translate() 사용
swap_separators = {ord('.'):',', ord(','):'.'}
print(format(x,',').translate(swap_separators))             # 1.234,56789


#=======================================================================================================================
# 3.4 2진수, 8진수, 16진수 작업
# 각각 bin(), oct(), hex()
#=======================================================================================================================
x = 1234
print(bin(x))               # binary(0b) - 0b10011010010
print(oct(x))               # octal(0o) - 0o2322
print(hex(x))               # hexadecimal(0x) - 0x4d2

# format으로 해보면
print(format(x,'b'))        # 10011010010
print(format(x,'o'))        # 2322
print(format(x,'x'))        # -4d2

# 음수로 해보면
x = -1234
print(format(x,'b'))        # -10011010010
print(format(x,'x'))        # -4d2

# 다른 진법 숫자를 정수형으로 변환. 이때 8진법 값은 무조건 앞에 0o (octal 표시)를 붙여야 한다
print(int('4d2',16))            # 1234
print(int('10011010010',2))     # 1234



#=======================================================================================================================
# 3.5 바이트에서 큰 숫자를 패킹/언패킹
# 바이트 문자열을 언패킹해서 정수값으로 만들거나, 매우 큰 정수값을 바이트 문자열로 바꿔야 한다.
# ㄴ 바이트 -> 정수형 : int.from_bytes()
# ㄴ 큰 정수값 -> 바이트 : int.to_bytes()
#=======================================================================================================================
# 바이트 -> 정수형
data = b'\x00\x124v\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
print(len(data))                                # 16
print(int.from_bytes(data,'little'))           # 69120565665751139577663547927631761920
print(int.from_bytes(data,'big'))               # 94525377821947740945920721189797940

# 정수값 -> 바이트
x = 945223123121512535321412414
print(x.to_bytes(16,'big'))                     # b'\x00\x00\x00\x00\x03\r\xde\xc8-\xb8S\xdf{\x03\x03>'
print(x.to_bytes(16,'little'))                  # b'>\x03\x03{\xdfS\xb8-\xc8\xde\r\x03\x00\x00\x00\x00'

# 이런식의 변환은 네트워크나 암호화가 필요한 특정 app 등에서 사용한다


#=======================================================================================================================
# 3.6 복소수 계산
# 복소수 평면을 사용할 수 밖에 없는 상황
# ㄴ complex(real,imag)
# ㄴ j를 붙인 부동 소수점 값으로 할 수 있다
#=======================================================================================================================
a = complex(2,4)
b = 3-5j
print(a)            # (2+4j)
print(b)            # (3-5j)

a.real              # 2.0 실수
a.imag              # 4.0 허수
a.conjugate()       # 켤레 복소수 (2-4j)


## 사인, 코사인, 제곱등은 cmath 모듈 사용
import cmath
print(cmath.sin(a))
print(cmath.cos(a))
print(cmath.exp(a))


# numpy로 복소수 배열을 만들고 계산 가능.
import numpy as np
a = np.array([2+3j, 4+5j, 6-7j, 8+9j])
print(a)
# [ 2.+3.j  4.+5.j  6.-7.j  8.+9.j]

print(a+2)
# [  4.+3.j   6.+5.j   8.-7.j  10.+9.j]

print(np.sin(a))
# [    9.15449915  -4.16890696j   -56.16227422 -48.50245524j
#   -153.20827755-526.47684926j  4008.42651446-589.49948373j]

#=======================================================================================================================
# 3.7 무한대와 NaN 사용
# 부동 소수점 값의 무한대, 음의 무한대, NaN 검사
# ㄴ float()
#=======================================================================================================================
a = float('inf')                # 양의 무한대
b = float('-inf')               # 음의 무한대
c = float('nan')                # 넘버가 아님
print(a)            # inf
print(b)            # -inf
print(c)            # nan

print(math.isinf(a))            # True
print(math.isnan(c))            # True

# NaN을 비교할 수 있는 건 math.isnan()뿐임


#=======================================================================================================================
# 3.8 분수 계산
# ㄴ fractions 모듈 사용
#=======================================================================================================================
from fractions import Fraction
a = Fraction(5,4)
b = Fraction(7,16)
print(a+b)      # 27/16
print(a*b)      # 35/64

# 분자랑 분모 구하기
c = a*b
print(c.numerator)          # 35
print(c.denominator)        # 64


# 소수 변환
print(float(c))             # 0.546875

# 분자를 특정값으로 제한
print(c.limit_denominator(8))       # 4/7

# 소수를 분수로 변환
x = 3.75
y = Fraction(*x.as_integer_ratio())
print(y)                                # Fration(15,4)



#=======================================================================================================================
# 3.9 큰 배열 계산
# ㄴ numpy 라이브러리 사용
#=======================================================================================================================

# 일반 파이썬 리스트와 numpy의 차이점
# 1. numpy는 배열 + 숫자간의 합이 간으
# 2. 스칼라 연산이 요소 기반으로 적용됨
# 3. 배열과 배열간 계산시 연산자가 모든 요소에 적용되고 새로운 배열 생성

import numpy as np
ax = np.array([1,2,3,4])
ay = np.array([5,6,7,8])

def f(x):
    return 3*x**2 - 2*x+7
print(f(ax))


## numpy로는 파이썬 리스트보다 훨씬 더 큰 배열을 만들 수 있다.


#=======================================================================================================================
# 3.10 행렬과 선형 대수 계산
# ㄴ numpy 라이브러리의 matrix(행렬) 사용
#=======================================================================================================================

import numpy as np
m = np.matrix([[1,-2,3],[0,4,5],[7,8,-9]])
print(m)

# [[ 1 -2  3]
#  [ 0  4  5]
#  [ 7  8 -9]]


# 전치 행렬
print(m.T)              # a-T

# [[ 1  0  7]
#  [-2  4  8]
#  [ 3  5 -9]]


# 역행렬
print(m.I)

# [[ 0.33043478 -0.02608696  0.09565217]
#  [-0.15217391  0.13043478  0.02173913]
#  [ 0.12173913  0.09565217 -0.0173913 ]]

# numpy.linalg 서브 패키지에는 더 많은 연산이 있다. determinant, Eigenvalues.. 등등
