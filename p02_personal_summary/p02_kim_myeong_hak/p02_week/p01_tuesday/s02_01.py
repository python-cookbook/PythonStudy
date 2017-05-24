#2.17 HTML과 XML 엔티티 처리

#Q &entity; 나 &#code; 와 같은 HTML, XML 엔티티를 이에 일치하는 문자로 치환하고 싶다. 혹은 텍스트를 생성할 때 특정문자(<,>,& 등)을 피하고싶다

#A 텍스트를 생성할때 <나>와 같은 특수문자를 치환 하는 것은 html.escape() 함수를 사용하면 상대적으로 간단히 처리할 수 있다.

s = 'Elements are written as "<tag>text</tag>".'
import html
print(s)
#Elements are written as "<tag>text</tag>".
print(html.escape(s))
#Elements are written as &quot;&lt;tag&gt;text&lt;/tag&gt;&quot;.

#따옴표는 남겨 두도록 지정
print(html.escape(s, quote=False))
#Elements are written as "&lt;tag&gt;text&lt;/tag&gt;".



#텍스트를 아스키(ASCII) 로 만들고 캐릭터 코드를 아스키가 아닌 문자에 끼워 넣고 싶으면 errors='xmlcharrefreplace' 인자를 입출력 관련 함수에 사용한다.

s = 'Spicy Jalapeño'
print(s.encode('ascii', errors='xmlcharrefreplace'))
#b'Spicy Jalape&#241;o'


#텍스트의 엔티티를 치환하면 또 다른 처리를 해야한다. 실제로 HTML,  XML 을 처리할 예정이면 우선 올바른 HTML, XML 파서를 사용하도록 한다. .
#일반적으로 이런 도구는 파싱 하는 동안 자동으로 값을 치환해 준다.
#하지만 어째서 인지 자동으로 처리되지 않았고 수동으로 치환을 해야 한다면 HTML, XML 파서에 내장되어 있는 여러 유틸리티 함수나 메소드를 사용한다.

s = 'Spicy &quot;Jalape&#241;o&quot.'
from html.parser import HTMLParser
p = HTMLParser()
print(p.unescape(s))
#'Spicy "Jalapeño".'

t = 'The prompt is &gt;&gt;&gt;'
from xml.sax.saxutils import unescape
print(unescape(t))
#'The prompt is >>>'

#D
#HTML, XML을 생성할때 특수 문자를 제대로 이스케이핑 하는 과정을 간과하기 쉽다. print()로 결과물을 생성하거나 기본적인 문자열 서식 기능을
#사용할 때 특히 더 그렇다. 가장 쉬운 해결책은 html.escqpe()와 같은 유틸리티 함수를 사용하는 것이다.
#또 다른 방식으로 텍스트를 처리하고 싶다면 xml.sax.saxutils.unescape()와 같은 여러 유틸리티 함수가 도움이 된다. 하지만 올바른 파서 사용법을 익히는 것이 훨신 더 중요하다
#예를 들어,html.parser나 xml.etree.ElemenTree와 같은 파싱 모듈로 HTML,XML을 처리하면 엔티티 치환과 같은 기본적인 내용을 알아서 다 처리해 준다.

#2.18

text = 'foo = 23 + 42 * 10'

tokens = [('NAME', 'foo'), ('EQ','='), ('NUM', '23'), ('PLUS','+'),('NUM', '42'), ('TIMES', '*'), ('NUM', '10')]

import re
NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))

'''
scanner = master_pat.scanner('foo = 42')
print(scanner.match())
#<_sre.SRE_Match object at 0x100677738>
_.lastgroup, _.group()
#('NAME', 'foo')
print(scanner.match())
#<_sre.SRE_Match object at 0x100677738>
_.lastgroup, _.group()
#('WS', ' ')
print(scanner.match())
#<_sre.SRE_Match object at 0x100677738>
_.lastgroup, _.group()
#('EQ', '=')
print(scanner.match())
#<_sre.SRE_Match object at 0x100677738>
_.lastgroup, _.group()
#('WS', ' ')
print(scanner.match())
#<_sre.SRE_Match object at 0x100677738>
_.lastgroup, _.group()
#('NUM', '42')
print(scanner.match())
'''
# 위의 코드는 잘 안됨.
#이제 이 기술을 코드에 사용해 보자. 다음과 같이 간결한 생성자를 만들 수 있다.
from collections import namedtuple
Token = namedtuple('Token', ['type', 'value'])

def generate_tokens(pat, text):

    Token = namedtuple('Token', ['type', 'value'])

    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())

# Example use
for tok in generate_tokens(master_pat, 'foo = 42'):
    print(tok)
# Produces output
# Token(type='NAME', value='foo')
# Token(type='WS', value=' ')
# Token(type='EQ', value='=')
# Token(type='WS', value=' ')
# Token(type='NUM', value='42')

#모든 공백문 걸러내는 코드

tokens = (tok for tok in generate_tokens(master_pat, text)
            if tok.type != 'WS')
for tok in tokens:
    print(tok)

#토론
#우선 입력부에 나타나는 모든 텍스트 시퀀스를 re패턴으로 확인해야 한다. 매칭하지 않는 텍스트가 하나라도 있으면 스캐닝이 거기서 멈춘다.
#예제에서 공백(ws) 토큰을 명시할 필요가 있었던 이유도 이과 같다.
#마스터 정규 표현식의 토큰 순서도 중요하다. 매칭할 때 re는 명시한 순서대로 패턴을 매칭한다. 따라서 한 패턴이 다른 패턴의 부분이 되는 경우가 있다면 항상 더 긴 패턴을 먼저 넣어야 한다.

LT = r'(?P<LT><)'
LE = r'(?P<LE><=)'
EQ = r'(?P<EQ>=)'

master_pat = re.compile('|'.join([LE, LT, EQ])) # 올바름
# master_pat = re.compile('|'.join([LT, LE, EQ])) # 틀림


PRINT = r'(?P<PRINT>print)'
NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'

master_pat = re.compile('|'.join([PRINT, NAME]))

for tok in generate_tokens(master_pat, 'printer'):
    print(tok)

# 출력 :
# Token(type='PRINT', value='print')
# Token(type='NAME', value='er')


#2.19 간단한 재귀 파서 작성
#프레임워크를 사용하지 않고 파서를 직접 장성하는 법

expr ::= expr + term
    |   expr - term
    |   term

term ::= term * factor
    |   term / factor
    |   factor

factor ::= ( expr )
    |   NUM


#ebnf ver

expr ::= term { (+|-) term }*

term ::= factor { (*|/) factor }*

factor ::= ( expr )
    |   NUM

#3+4*5  예를 들어 3+ 4 * 5 라는 문자열을 파싱한다고 생각해보자. 이 표현식은
#우선 레시피 2.18에 나온 기술대로 토큰화 해야한다. 그 결과는 아마 다음과 같을 것이다

    NUM + NUM * NUM


expr
expr ::= term { (+|-) term }*
expr ::= factor { (*|/) factor }* { (+|-) term }*
expr ::= NUM { (*|/) factor }* { (+|-) term }*
expr ::= NUM { (+|-) term }*
expr ::= NUM + term { (+|-) term }*
expr ::= NUM + factor { (*|/) factor }* { (+|-) term }*
expr ::= NUM + NUM { (*|/) factor}* { (+|-) term }*
expr ::= NUM + NUM * factor { (*|/) factor }* { (+|-) term }*
expr ::= NUM + NUM * NUM { (*|/) factor }* { (+|-) term }*
expr ::= NUM + NUM * NUM { (+|-) term }*
expr ::= NUM + NUM * NUM


import re
import collections

#토큰 스펙화
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
#토큰화
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
    재귀 파서 구현, 모든 메소드는 하나의 문법 규칙을 구현한다.
      현재 룩어헤드 토큰을 받고 테스트하는 용도로 ._accept()를 사용한다.
        입력 받은 내역에 완벽히 매칭하고 다음 토큰을 무시할 때는
	._expect()를 사용한다 (혹시 매칭하지 않는 경우에는 SyntaxError를 발생한다).
    '''

    def parse(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None  # Last symbol consumed
        self.nexttok = None  # Next symbol tokenized
        self._advance()  # Load first lookahead token
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

    #문법 규칙
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


#ExpressionEvaluator 클래스를 사용하는 방법은 다음과 같다.


def descent_parser():
    e = ExpressionEvaluator()
    print(e.parse('2'))
    print(e.parse('2 + 3'))
    print(e.parse('2 + 3 * 4'))
    print(e.parse('2 + (3 + 4) * 5'))
    # print(e.parse('2 + (3 + * 4)'))
    # Traceback (most recent call last):
    #    File "<stdin>", line 1, in <module>
    #    File "exprparse.py", line 40, in parse
    #    return self.expr()
    #    File "exprparse.py", line 67, in expr
    #    right = self.term()
    #    File "exprparse.py", line 77, in term
    #    termval = self.factor()
    #    File "exprparse.py", line 93, in factor
    #    exprval = self.expr()
    #    File "exprparse.py", line 67, in expr
    #    right = self.term()
    #    File "exprparse.py", line 77, in term
    #    termval = self.factor()
    #    File "exprparse.py", line 97, in factor
    #    raise SyntaxError("Expected NUMBER or LPAREN")
    #    SyntaxError: Expected NUMBER or LPAREN


if __name__ == '__main__':
    descent_parser()


#순수 해석 이상의 일을 하고 싶다면 ExpressionEvaluator 클래스를 수정해야 한다.
#예를들어, 간단하 파싱트리를 만드는 구현식을 살펴보자.

class ExpressionTreeBuilder(ExpressionEvaluator):
    def expr(self):
        "expression ::= term { ('+'|'-') term}"

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
        "term::= facotr { ('*'|'/') factor}"

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
        "factor ::= NUM | ( expr )"
        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')

#사용법은 다음과 같다:

e = ExpressionTreeBuilder

print(e.parse('2'))
print(e.parse('2 + 3'))
print(e.parse('2 + 3 * 4'))
print(e.parse('2 + (3 + 4) * 5'))


expr ::= term { ('+'|'-') term }*

term ::= factor { ('*'|'/') factor }*

factor ::= '(' expr ')'
    | NUM


items ::= items ',' item
    | item

def items(self):
    itemsval = self.items()
    if itemsval and self._accept(','):
        itemsval.append(self.item())
    else:
        itemsval = [ self.item() ]


expr ::= factor { ('+'|'-'|'*'|'/') factor }*
 
factor ::= '(' expression ')'
    | NUM


from ply.lex import lex
from ply.yacc import yacc

# 토큰 리스트
tokens = [ 'NUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN' ]
# 무시 문자
t_ignore = ' \t\n'
# 토큰 스펙(정규 표현식으로)
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# 토큰화 함수
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# 에러 핸들러
def t_error(t):
    print('Bad character: {!r}'.format(t.value[0]))
    t.skip(1)

#렉서 만들기
lexer = lex()

#문법 규칙과 핸들러 함수
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


#파서 객체 사용하는 예
parser.parse('2')
#2
parser.parse('2+3')
#5
parser.parse('2+(3+4)*5')
#37



#챕터 2.20 바이트 문자열에 텍스트 연산 수행

data = b'Hello World'
data[0:5]
#b'Hello'
data.startswith(b'Hello')
#True
data.split()
#[b'Hello', b'World']
data.replace(b'Hello', b'Hello Cruel')
#b'Hello Cruel World'

#이런 동작은 바이트 배열에도 사용할 수 있다.

data = bytearray(b'Hello World')
print(data[0:5])
#bytearray(b'Hello')
print(data.startswith(b'Hello'))
#True
print(data.split())
#[bytearray(b'Hello'), bytearray(b'World')]
print(data.replace(b'Hello', b'Hello Cruel'))
#bytearray(b'Hello Cruel World')



data = b'FOO:BAR,SPAM'
import re
re.split('[:,]',data)

#Traceback (most recent call last):
#File "<stdin>", line 1, in <module>
#File "/usr/local/lib/python3.3/re.py", line 191, in split
#return _compile(pattern, flags).split(string, maxsplit)
#TypeError: can't use a string pattern on a bytes-like object
print(re.split(b'[:,]',data)) # 주의 패턴도 바이트로 나타냄
#[b'FOO', b'BAR', b'SPAM']


 a = 'Hello World' #텍스트 문자열
Print( a[0])
#'H'
Print(a[1])
#'e'
b = b'Hello World' # 바이트 문자열
Print(b[0])
#72
Print( b[1])
#101


s = b'Hello World'
print(s)
#b'Hello World' # b'...' 형식으로 출력된다.
print(s.decode('ascii'))
#Hello World


b'%10s %10d %10.2f' % (b'ACME', 100, 490.1)
#Traceback (most recent call last):
#    File "<stdin>", line 1, in <module>
#TypeError: unsupported operand type(s) for %: 'bytes' and 'tuple'
b'{} {} {}'.format(b'ACME', 100, 490.1)
#Traceback (most recent call last):
#    File "<stdin>", line 1, in <module>
#AttributeError: 'bytes' object has no attribute 'format'


print('{:10s} {:10d} {:10.2f}'.format('ACME', 100, 490.1).encode('ascii'))
#b'ACME 100 490.10'


# UTF-8 파일 이름 작성
with open('jalape\xf1o.txt', 'w') as f:
...     f.write('spicy')
...

# 디렉터리 리스트 구하기
import os
os.listdir('.') # 텍스트 문자열 (이름이 디코딩된다.)
#['jalapeño.txt']
os.listdir(b'.') # 바이트 문자열 (이름이 바이트로 남는다.)
#[b'jalapen\xcc\x83o.txt']


#3장 1 반올림

round(1.23, 1)
#1.2
round(1.27, 1)
#1.3
round(-1.27, 1)
#-1.3
round(1.25361,3)
#1.254



a = 1627731
round(a, -1)
#1627730
round(a, -2)
#1627700
round(a, -3)
#1628000


x = 1.23456
format(x, '0.2f')
#'1.23'
format(x, '0.3f')
#'1.235'
'value is {:0.3f}'.format(x)
#'value is 1.235'


a = 2.1
b = 4.2
c = a + b
print(c)
#6.300000000000001
c = round(c, 2) # "Fix" result (???)
print(c)
#6.3

#3.2정확한 10진수 계산

a = 4.2
b = 2.1
print(a + b)
#6.300000000000001
print((a + b) == 6.3)
#False

#decimal 모듈 사용

from decimal import Decimal
a = Decimal('4.2')
b = Decimal('2.1')
a + b
#Decimal('6.3')
print(a + b)
6.3
print((a + b) == Decimal('6.3'))
#True


#Decimal 의 중요한 기능으로 반올림의 자릿수와 같은 계산적 측면을 조절할 수 있다는 점 이 있다.

from decimal import localcontext
a = Decimal('1.3')
b = Decimal('1.7')
print(a / b)
#0.7647058823529411764705882353

with localcontext() as ctx:
    ctx.prec = 3
    print(a / b)
#0.765
with localcontext() as ctx:
    ctx.prec = 50
    print(a / b)
#0.76470588235294117647058823529411764705882352941176


nums = [1.23e+18, 1, -1.23e+18]
sum(nums) # 1이 사라진다.
#0.0

import math
math.fsum(nums)
#1.0

#3.3 출력을 위한 숫자 서식화

x = 1234.56789

#소수점 둘째 자리 정확도
print(format(x, '0.2f'))
#'1234.57'

#소수점 한 자리 정확도로 문자 10개 기준 오른쪽에서 정렬
print(format(x, '>10.1f'))
'    1234.6'

#왼쪽에서 정렬
format(x, '<10.1f')
'1234.6    '

#가운데서 정렬
print(format(x, '^10.1f'))
'  1234.6  '

#천 단위 구분자 넣기
format(x, ',')
#'1,234.56789'
format(x, '0,.1f')
#'1,234.6'

#지수 표현법을 사용하려면 f를 e나 E로 바꾸면 된다.

format(x, 'e')
#'1.234568e+03'
format(x, '0.2E')
#'1.23E+03'


print('The value is {:0,.2f}'.format(x))
#'The value is 1,234.57'

print(x)
#1234.56789
print(format(x, '0.1f'))
#'1234.6'
print(format(-x, '0.1f'))
#'-1234.6'

swap_separators = { ord('.'):',', ord(','):'.' }
print(format(x, ',').translate(swap_separators))
#'1.234,56789'

#숫자를 % 연산자로 서식화 한다.

print('%0.2f' % x)
#'1234.57'
print('%10.1f' % x)
#'    1234.6'
print('%-10.1f' % x)
#'1234.6    '

x = 1234
print(bin(x))
#'0b10011010010'
print(oct(x))
#'0o2322'
print(hex(x))
#'0x4d2'

#0뒤에 붙는 문자를 제거하기 위한 포맷 함수 사용

format(x, 'b')
#'10011010010'
format(x, 'o')
#'2322'
format(x, 'x')
#'4d2'

#정수형 부호
x = -1234
format(x, 'b')
#'-10011010010'
format(x, 'x')
#'-4d2'


x = -1234
print(format(2**32 + x, 'b'))
#'11111111111111111111101100101110'
print(format(2**32 + x, 'x'))
#'fffffb2e'

#다른 진법의 숫자를 정수형으로 변환 하려면 int() 함수에 적절한 진수를 전달한다.

int('4d2', 16)
#1234
int('10011010010', 2)
#1234

#8진법 사용시 주의사항

import os
os.chmod('script.py', 0755)
#    File "<stdin>", line 1
#        os.chmod('script.py', 0755)
#                            ^
#SyntaxError: invalid token

#8진법 앞에는 0o를 붙여야한다.

os.chmod('script.py', 0o755)


#3.9 큰 배열 계산
#파이썬 리스트와 넘파이의 차이점을 보여준는 예


# 파이썬 리스트
x = [1, 2, 3, 4]
y = [5, 6, 7, 8]
x * 2
#[1, 2, 3, 4, 1, 2, 3, 4]
x + 10
#Traceback (most recent call last):
#    File "<stdin>", line 1, in <module>
#TypeError: can only concatenate list (not "int") to list
x + y
#[1, 2, 3, 4, 5, 6, 7, 8]

# 넘파이 배열
import numpy as np
ax = np.array([1, 2, 3, 4])
ay = np.array([5, 6, 7, 8])
print(ax * 2)
#array([2, 4, 6, 8])
ax + 10
#array([11, 12, 13, 14])
print(ax + ay)
#array([ 6, 8, 10, 12])
print(ax * ay)
#array([ 5, 12, 21, 32])

def f(x):
    return 3*x**2 - 2*x + 7

f(ax)
#array([ 8, 15, 28, 47])



np.sqrt(ax)
#array([ 1. , 1.41421356, 1.73205081, 2. ])
np.cos(ax)
#array([ 0.54030231, -0.41614684, -0.9899925 , -0.65364362])


grid = np.zeros(shape=(10000,10000), dtype=float)
grid
array([[ 0., 0., 0., ..., 0., 0., 0.],
[ 0., 0., 0., ..., 0., 0., 0.],
[ 0., 0., 0., ..., 0., 0., 0.],
...,
[ 0., 0., 0., ..., 0., 0., 0.],
[ 0., 0., 0., ..., 0., 0., 0.],
[ 0., 0., 0., ..., 0., 0., 0.]])

#연산은 모든 요소에 동시 적용된다

grid += 10
grid
array([[ 10., 10., 10., ..., 10., 10., 10.],
    [ 10., 10., 10., ..., 10., 10., 10.],
    [ 10., 10., 10., ..., 10., 10., 10.],
    ...,
    [ 10., 10., 10., ..., 10., 10., 10.],
    [ 10., 10., 10., ..., 10., 10., 10.],
    [ 10., 10., 10., ..., 10., 10., 10.]])
np.sin(grid)
array([[-0.54402111, -0.54402111, -0.54402111, ..., -0.54402111,
        -0.54402111, -0.54402111],
       [-0.54402111, -0.54402111, -0.54402111, ..., -0.54402111,
        -0.54402111, -0.54402111],
       [-0.54402111, -0.54402111, -0.54402111, ..., -0.54402111,
        -0.54402111, -0.54402111],
       ...,
       [-0.54402111, -0.54402111, -0.54402111, ..., -0.54402111,
         -0.54402111, -0.54402111],
       [-0.54402111, -0.54402111, -0.54402111, ..., -0.54402111,
        -0.54402111, -0.54402111],
       [-0.54402111, -0.54402111, -0.54402111, ..., -0.54402111,
        -0.54402111, -0.54402111]])


#2차원 배열 예제

a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
a
array([[ 1, 2, 3, 4],
[ 5, 6, 7, 8],
[ 9, 10, 11, 12]])

# 첫번째 행 선택
print(a[1])
#array([5, 6, 7, 8])

# 첫 번째 열 선택
print(a[:,1])
#array([ 2, 6, 10])

# 지역을 선택 후 변경
print(a[1:3, 1:3])
#array([[ 6, 7],
#        [10, 11]])

a[1:3, 1:3] += 10
print(a)
#array([[ 1, 2, 3, 4],
#       [ 5, 16, 17, 8],
#       [ 9, 20, 21, 12]])

# 행 벡터를 모든 행 연산에 적용
a + [100, 101, 102, 103]
array([[101, 103, 105, 107],
       [105, 117, 119, 111],
       [109, 121, 123, 115]])
print(a)
array([[ 1, 2, 3, 4],
        [ 5, 16, 17, 8],
        [ 9, 20, 21, 12]])

# 조건이 있는 할당
np.where(a < 10, a, 10)
array([[ 1, 2, 3, 4],
        [ 5, 10, 10, 8],
        [ 9, 10, 10, 10]])


#3.10 행렬과 선형 대수 계산

import numpy as np
m = np.matrix([[1,-2,3],[0,4,5],[7,8,-9]])
print(m)
#matrix([[ 1, -2, 3],
#        [ 0, 4, 5],
#        [ 7, 8, -9]])

# 전치행렬
print(m.T)
#matrix([[ 1, 0, 7],
#        [-2, 4, 8],
#        [ 3, 5, -9]])

# 역행렬
m.I
#matrix([[ 0.33043478, -0.02608696, 0.09565217],
#        [-0.15217391, 0.13043478, 0.02173913],
#        [ 0.12173913, 0.09565217, -0.0173913 ]])

# 벡터를 만들고 곱하기
v = np.matrix([[2],[3],[4]])
print(v)
#matrix([[2],
#        [3],
#        [4]])
print(m * v)
#matrix([[ 8],
#        [32],
#        [ 2]])

#Numpy.linalg 패키지

import numpy.linalg

# Determinant
numpy.linalg.det(m)
#-229.99999999999983

# Eigenvalues
numpy.linalg.eigvals(m)
#array([-13.11474312, 2.75956154, 6.35518158])

# mx = v에서 x 풀기
x = numpy.linalg.solve(m, v)
print(x)
#matrix([[ 0.96521739],
#        [ 0.17391304],
#        [ 0.46086957]])
print(m * x)
#matrix([[ 2.],
#        [ 3.],
#        [ 4.]])
print(v)
matrix([[2],
        [3],
        [4]])
