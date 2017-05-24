'''
--------------------------------------------------------------------------------------
2.17 HTML 과 XML 엔티티 처리

문제 : &entity; 나 &#code; 와 같은 HTML, XML 엔티티를 이에 일치하는 문자로 치환
      혹은 텍스트를 생성할 때 특정 문자(<, >, & 등)를 피하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- html.escape() 함수를 사용하면 상대적으로 간단히 특수 문자 치환 가능
--------------------------------------------------------------------------------------
'''

import html

s = 'Elements are written as "<tag>text</tag>".'

print(s)
print(html.escape(s))
print(html.escape(s,quote=False))

'''
--------------------------------------------------------------------------------------
- 텍스트를 아스키로 만들고 캐릭터 코드를 아스키가 아닌 문자에 끼워 넣고 싶으면
  errors = ‘xmlcharrefreplace’ 인자를 입출력 관련 함수에 사용
--------------------------------------------------------------------------------------
'''

s = 'Spicy jalapeño'

print(s.encode('ascii',errors='xmlcharrefreplace'))

'''
--------------------------------------------------------------------------------------
- 텍스트의 엔티티를 치환하면 또 다른 처리를 해야 한다. 파싱하는 동안 자동으로 값을 치환해주는데
  자동으로 처리되지 않았고 수동으로 치환을 해야 한다면 HTML, XML 파서에 내장되어 있는 
  여러 유틸리티 함수나 메소드 사용
--------------------------------------------------------------------------------------
'''

from html.parser import HTMLParser
from xml.sax.saxutils import unescape

s = 'Spicy &quot;jalape&#241;o&quot.'
t = 'The prompt is &gt;&gt;&gt;'
p = HTMLParser()

print(p.unescape(s))
print(unescape(t))

'''
=> print() 로 결과물을 생성하거나 기본적인 문자열 서식 기능을 사용할 때 가장 쉬운 해결책은
   html.escape() 와 같은 유틸리티 함수 사용
--------------------------------------------------------------------------------------
'''





'''
--------------------------------------------------------------------------------------
2.18 텍스트 토큰화

문제 : 문자열을 파싱해서 토큰화 하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 문자열을 토큰화하려면 패턴 매칭 이상의 작업이 필요, 문자열을 페어 시퀀스로 바꾸는 작업을 하기 위해서
  공백을 포함해서 가능한 모든 토큰을 정의
--------------------------------------------------------------------------------------
'''

import re

text = 'foo = 23 + 42 * 10'
tokens = [('NAME', 'foo'), ('EQ', '='), ('NUM', '23'), ('PLUS', '+'), ('NUM', '42'),
          ('TIMES', '*'), ('NUM', '10')]


NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))
scanner = master_pat.scanner('foo = 42')

print(scanner.match())

'''
--------------------------------------------------------------------------------------
- 간결한 생성자 만들기
--------------------------------------------------------------------------------------
'''

import re
from collections import namedtuple

tokens = [('NAME', 'foo'), ('EQ', '='), ('NUM', '23'), ('PLUS', '+'), ('NUM', '42'),
          ('TIMES', '*'), ('NUM', '10')]

NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

Token = namedtuple('Token', ['type', 'value'])
master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))

def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())


for tok in generate_tokens(master_pat, 'foo = 42'):
    print(tok)





'''
--------------------------------------------------------------------------------------
2.19 간단한 재귀 파서 작성

문제 : 주어진 문법 규칙에 따라 텍스트를 파싱하고 동작을 수행하거나 입력된 텍스트를 
      추상 신택스 트리로 나타내기 (프레임워크를 사용하지 않고 파서를 직접 작성하기)
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 재귀 표현식 해석기 만들기
--------------------------------------------------------------------------------------
'''

import re
import collections

# 토큰 스팩화
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES,
                                  DIVIDE, LPAREN, RPAREN, WS]))
# 토큰화
Token = collections.namedtuple('Token', ['type', 'value'])


def generate_tokens(text):
    scanner = master_pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok

# 파서
class ExpressionEvaluator:
    '''
    재귀 파서 구현, 모든 메소드는 하나의 문법 규칙 구현
    현재 룩어헤드 토큰을 받도 테스트하는 용도로 ._accept() 사용
    입력 받은 내역에 완벽히 매칭하고 다음 토큰을 무시할 때는
    ._accept() 사용 (혹시 매칭하지 않은 경우에는 SyntaxError 발생)
    '''

    def parse(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None         # 마지막 심볼 소비
        self.nexttok = None     # 다음 심볼 토큰화
        self._advance()         # 처음 룩어헤드 토큰 불러오기
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

    def _expect(self, toktype):
        'Consume next token if it matches toktype or raise SyntaxError'
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    # 문법 규칙
    def expr(self):
        "expression ::= term { ('+'|'-') term }*"

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
        "term ::= factor { ('*'|'/') factor }*"

        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            if op == 'TIMES':
                termval *= right
            elif op == 'DIVIDE':
                termval /= right
        return termval

    def factor(self):
        "factor ::= NUM | ( expr )"

        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')

if __name__ == '__main__':
    e = ExpressionEvaluator()
    print(e.parse('2'))
    print(e.parse('2 + 3'))
    print(e.parse('2 + 3 * 4'))
    print(e.parse('2 + (3 + 4) * 5'))

'''
--------------------------------------------------------------------------------------
- 파싱 트리 구현 코드
--------------------------------------------------------------------------------------
'''

WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES,
                                  DIVIDE, LPAREN, RPAREN, WS]))
# 토큰화
Token = collections.namedtuple('Token', ['type', 'value'])


def generate_tokens(text):
    scanner = master_pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok

# 파서
class ExpressionEvaluator:
    '''
    재귀 파서 구현, 모든 메소드는 하나의 문법 규칙 구현
    현재 룩어헤드 토큰을 받도 테스트하는 용도로 ._accept() 사용
    입력 받은 내역에 완벽히 매칭하고 다음 토큰을 무시할 때는
    ._accept() 사용 (혹시 매칭하지 않은 경우에는 SyntaxError 발생)
    '''

    def parse(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None         # 마지막 심볼 소비
        self.nexttok = None     # 다음 심볼 토큰화
        self._advance()         # 처음 룩어헤드 토큰 불러오기
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

    def _expect(self, toktype):
        'Consume next token if it matches toktype or raise SyntaxError'
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    # 문법 규칙
    def expr(self):
        "expression ::= term { ('+'|'-') term }*"

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
        "term ::= factor { ('*'|'/') factor }*"

        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            if op == 'TIMES':
                termval *= right
            elif op == 'DIVIDE':
                termval /= right
        return termval

    def factor(self):
        "factor ::= NUM | ( expr )"

        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')


class ExpressionTreeBuilder(ExpressionEvaluator):
    def expr(self):
        "expression ::= term { ('+'|'-') term }"

        exprval = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.tok.type
            right = self.term()
            if op == 'PLUS':
                exprval = ('+', exprval, right)
            elif op == 'MINUS':
                exprval = ('-', exprval, right)
        return exprval

    def term(self):
        "term ::= factor { ('*'|'/') factor }"

        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            if op == 'TIMES':
                termval = ('*', termval, right)
            elif op == 'DIVIDE':
                termval = ('/', termval, right)
        return termval

    def factor(self):
        'factor ::= NUM | ( expr )'

        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')


if __name__ == '__main__':
    e = ExpressionTreeBuilder()
    print(e.parse('2 + 3'))
    print(e.parse('2 + 3 * 4'))
    print(e.parse('2 + (3 + 4) * 5'))
    print(e.parse('2 + 3 + 4'))

'''
--------------------------------------------------------------------------------------
'''

from ply.lex import lex
from ply.yacc import yacc

# Token list
tokens = [ 'NUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN' ]

# Ignored characters
t_ignore = ' \t\n'

# Token specifications (as regexs)
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Token processing functions
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Error handler
def t_error(t):
    print('Bad character: {!r}'.format(t.value[0]))
    t.skip(1)

# Build the lexer
lexer = lex()

# Grammar rules and handler functions
def p_expr(p):
    '''
    expr : expr PLUS term
    | expr MINUS term
    '''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

def p_expr_term(p):
    '''
    expr : term
    '''
    p[0] = p[1]


def p_term(p):
    '''
    term : term TIMES factor
    | term DIVIDE factor
    '''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_factor(p):
    '''
    factor : NUM
    '''
    p[0] = p[1]

def p_factor_group(p):
    '''
    factor : LPAREN expr RPAREN
    '''
    p[0] = p[2]

def p_error(p):
    print('Syntax error')

parser = yacc()

print(parser.parse('2'))
print(parser.parse('2+3'))
print(parser.parse('2+(3+4)*5'))





'''
--------------------------------------------------------------------------------------
2.20 바이트 문자열에 텍스트 연산 수행

문제 : 바이트 문자열에 일반적인 텍스트 연산(잘라내기, 검색, 치환 등)을 수행
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 바이트 문자열도 텍스트 문자열과 마찬가지로 대부분의 연산을 내장
--------------------------------------------------------------------------------------
'''

data = b'Hello World'

print(data[0:5])
print(data.startswith(b'Hello'))
print(data.split())
print(data.replace(b'Hello',b'Hello Curel'))

'''
--------------------------------------------------------------------------------------
- 바이트 배열에서도 사용 가능
--------------------------------------------------------------------------------------
'''

data = bytearray(b'Hello World')

print(data[0:5])
print(data.startswith(b'Hello'))
print(data.split())
print(data.replace(b'Hello',b'Hello Curel'))

'''
=> 바이트 문자열 패턴 매칭에 정규 표현식 사용 가능
   (하지만, 패턴 자체도 바이트로 나타내야 한다)
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 바이트 문자열에 인덱스를 사용하면 개별 문자가 아니라 정수를 가리킨다
--------------------------------------------------------------------------------------
'''

a = 'Hello World'   # 텍스트 문자열
b = b'Hello World'  # 바이트 문자열

print(a[0])
print(a[1])
print(b[0])
print(b[1])

'''
--------------------------------------------------------------------------------------
- 바이트 문자열을 보기 좋은 표현식을 지원하지 않으며 텍스트 문자열로 변환하지 않으면 깔끔하게 출력 X
--------------------------------------------------------------------------------------
'''

s = b'Hello World'

print(s)
print(s.decode('ascii'))

'''
--------------------------------------------------------------------------------------
- 바이트 문자열을 서식화(formatting)를 지원 X
  (바이트 문자열에 서식화를 적용하고 싶으면 일반 텍스트 문자열과 인코딩 사용)
--------------------------------------------------------------------------------------
'''

print('{:10s} {:10d} {:10.2f}'.format('ACME', 100, 490.1).encode('ascii'))





'''
--------------------------------------------------------------------------------------
Chapter 3 숫자, 날짜, 시간
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
3.1 반올림

문제 : 부동 소수점 값을 10진수로 반올림하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 반올림은 내장함수인 round(value, ndigits) 함수 사용
--------------------------------------------------------------------------------------
'''

print(round(1.23, 1))
print(round(1.27, 1))
print(round(-1.27, 1))
print(round(1.25361, 3))

'''
--------------------------------------------------------------------------------------
- round()에 전달하는 자릿수는 음수가 될 수 있다. 아래의 경우 10의 자리 ,100자리 등의 순으로 자릿수 결정
--------------------------------------------------------------------------------------
'''

a = 1627731

print(round(a, -1))
print(round(a, -2))
print(round(a, -3))

'''
--------------------------------------------------------------------------------------
- 특정 자릿수까지 숫자를 표현하는 것이 목적이라면 round() 사용 X
  서식화를 위한 자릿수를 명시하기만 하면된다
--------------------------------------------------------------------------------------
'''

x = 1.23456

print(format(x, '0.2f'))
print(format(x, '0.3f'))
print('value is {:0.3f}'.format(x))





'''
--------------------------------------------------------------------------------------
3.2 정확한 10진수 계산

문제 : 정확한 10진수 계산을 해야 하고, 부동 소수점을 사용할 때 발생하는 작은 오류 피하기  
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 부동 소수점 값에는 10진수를 아주 정확하게 표현하지 못한다는 문제 
--------------------------------------------------------------------------------------
'''

a = 4.2
b = 2.1

print(a+b)
print((a+b) == 6.3)

'''
=> 이런 오류는 CPU와 IEEE 754로 부동 소수점 숫자 계산을 할 때 필연적으로 발생한다

=> 파이썬의 부동 소수점 값이 이 표현식을 사용하기 때문에 float를 사용해서는 이 오류를 피할 수 없다
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- decimal 모듈을 사용(더 정확한 계산, 하지만 성능 측면을 희생)
--------------------------------------------------------------------------------------
'''

from decimal import Decimal

a = Decimal('4.2')
b = Decimal('2.1')

print(a+b)
print((a+b) == Decimal('6.3'))

'''
--------------------------------------------------------------------------------------
- decimal의 중요한 기능으로는 반올림 자릿수와 같은 계산적 측면 조절
--------------------------------------------------------------------------------------
'''

from decimal import localcontext

a = Decimal('1.3')
b = Decimal('1.7')

print(a/b)

with localcontext() as ctx:
    ctx.prec = 3
    print(a/b)

with localcontext() as ctx:
    ctx.prec = 50
    print(a/b)

'''
--------------------------------------------------------------------------------------
- 오류의 경우
--------------------------------------------------------------------------------------
'''

nums = [1.23e+18, 1, -1.23e+18]

print(sum(nums))

'''
=> 합이 1이 되어야 하지만 합이 0으로 출력(오류!)
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 위의 오류 해결 코드
--------------------------------------------------------------------------------------
'''

import math

nums = [1.23e+18, 1, -1.23e+18]

print(math.fsum(nums))





'''
--------------------------------------------------------------------------------------
3.3 출력을 위한 숫자 서식화

문제 : 출력을 위해 자릿수, 정렬, 천 단위 구분 등 숫자 서식화 하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- format() 함수를 이용해 숫자 서식화 하기
--------------------------------------------------------------------------------------
'''

x = 1234.56789

print(format(x, '0.2f'))    # 소주점 둘째 자리 정확도
print(format(x, '>10.1f'))  # 소수점 한 자리 정확도 문자 10개 기준 오른쪽 정렬
print(format(x, '<10.1f'))  # 소수점 한 자리 정확도 문자 10개 기준 왼쪽 정렬
print(format(x, '^10.1f'))  # 소수점 한 자리 정확도 문자 10개 기준 가운데 정렬
print(format(x, ','))       # 천 단위 구분자 넣기
print('The Value is {:0,.2f}'.format(x))

'''
--------------------------------------------------------------------------------------
- 자릿수를 제한하면 round() 함수와 동일한 규칙으로 반올림
--------------------------------------------------------------------------------------
'''

x = 1234.56789

print(format(x, '0.1f'))
print(format(-x, '0.1f'))

'''
--------------------------------------------------------------------------------------
- 천 단위 구분자는 지역 표기법을 따르지 않는데 이를 염두에 둔다면 
  local 모듈의 함수의 문자열의 translate() 메소드 사용
--------------------------------------------------------------------------------------
'''

x = 1234.56789
swap_separator = { ord('.'):',', ord(','):'.'}

print(format(x, ',').translate(swap_separator))





'''
--------------------------------------------------------------------------------------
3.4 2진수, 8진수, 16진수 작업

문제 : 숫자를 2진수, 8진수, 16진수로 출력하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 정수를 2진수, 8진수, 16진수 문자열로 변환하려면 bin(), oct(), hex() 사용
--------------------------------------------------------------------------------------
'''

x = 1234

print(bin(x))
print(oct(x))
print(hex(x))

'''
--------------------------------------------------------------------------------------
- 부호가 없는 값을 사용하려면 최대값을 더해서 비트 길이 설정(예:32비트)
--------------------------------------------------------------------------------------
'''

x = -1234

print(format(2**32 + x, 'b'))
print(format(2**32 + x, 'x'))

'''
--------------------------------------------------------------------------------------
- 다른 진법의 숫자를 정수형으로 변환하려면 int() 함수에 적절한 진수 전달
--------------------------------------------------------------------------------------
'''

print(int('4d2', 16))
print(int('10011010010'))

'''
=> 8진법 값 앞에는 0o 를 붙여야 한다!
--------------------------------------------------------------------------------------
'''





'''
--------------------------------------------------------------------------------------
3.9 큰 배열의 계산

문제 : 배열이나 그리드(grid)와 같이 커다란 숫자 데이터세트(dataset)에 계산 하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- 배열이 관련된 커다란 계산을 하려면 Numpy 라이브러리 사용
--------------------------------------------------------------------------------------
'''

import numpy as np

ax = np.array([1, 2, 3, 4])
ay = np.array([5, 6, 7, 8])

print(ax*2)
print(ax+10)
print(ax+ay)
print(ax*ay)

'''
--------------------------------------------------------------------------------------
- 매우 빠르고 쉬운 배열 계산을 할 수 있다(다항식 계산)
--------------------------------------------------------------------------------------
'''

def f(x):
    return 3*x**2 - 2*x + 7

ax = np.array([1, 2, 3, 4])

print(f(ax))

'''
--------------------------------------------------------------------------------------
- 소수를 담는 10x10 2차원 그리드 만들기(마찬가지로 모든 연산은 모든 요소에 동시 적용)
--------------------------------------------------------------------------------------
'''

import numpy as np

grid = np.zeros(shape=(10,10), dtype=float)

print(grid)

grid += 10

print(grid)
print(np.sin(grid))

'''
--------------------------------------------------------------------------------------
- 다차원 배열의 인덱싱 기능 확장
--------------------------------------------------------------------------------------
'''

import numpy as np

a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])

print(a)
print(a[1])         # 첫 번째 행 선택
print(a[:,1])       # 첫 번째 열 선택
print(a[1:3, 1:3])  # 지역을 선택 후 변경

a[1:3, 1:3] += 10

print(a)
print(a + [100, 101, 102, 103])     # 행 백터를 모든 행 연산에 적용
print(np.where(a < 10, a, 10))      # 조건이 있는 할당





'''
--------------------------------------------------------------------------------------
3.10 행렬과 선형 대수

문제 : 행렬 곱셈, 행렬식 찾기, 선형 방정식 풀기 등 행렬이나 선형 대수 계산 하기
--------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------
- matrix 객체가 있는데 계산할 때는 선형 대수 계산법을 따른다
--------------------------------------------------------------------------------------
'''

import numpy as np

m = np.matrix([[1,-2,3], [0,4,5], [7,8,-9]])
v = np.matrix([[2], [3], [4]])    # 벡터 만들기


print(m)
print(m.T)  # 전치 행렬
print(m.I)  # 역행렬

print(v)
print(m*v)

'''
--------------------------------------------------------------------------------------
- numpy.linalg 서브 패키지
--------------------------------------------------------------------------------------
'''

import numpy.linalg

m = np.matrix([[1,-2,3], [0,4,5], [7,8,-9]])
x = numpy.linalg.solve(m, v)    # v에서 x 풀기

print(numpy.linalg.det(m))
print(numpy.linalg.eigvals(m))

print(x)
print(m*x)
print(v)