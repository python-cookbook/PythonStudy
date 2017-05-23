#  2.17 HTML 과 XML 엔티티 처리
#  ▣ 문제 : &entity; 나 &#code; 와 같은 HTML, XML 엔터티를 이에 일치하는 문자로 치환하고 싶다.
#           혹은 텍스트를 생성할 때 특정 문자(<, >, & 등)를 피하고 싶다.
#  ▣ 해결 : 텍스트를 생성할 때 <나>와 같은 특수 문자를 치환하는 것은 html.escape() 함수를 사용하면 상대적으로 간단히 처리할 수 있다.
s = 'Elements are written as "<tag>text</tag>".'
import html
print(s)
print(html.escape(s))

#   - 따옴표는 남겨 두도록 지정
print(html.escape(s, quote=False))

#   - 텍스트를 아스키로 만들고 캐릭터 코드를 아스키가 아닌 문자에 끼워 넣고 싶으면 errors='xmlcharrefreplace' 인자를 입출력 관련 함수에 사용한다.
s = 'Spicy Jalapeño'
print(s.encode('ascii', errors='xmlcharrefreplace'))

#   - 수동으로 치환을 해야 한다면 HTML, XML 파서에 내장되어 있는 여러 유틸리티 함수나 메소드를 사용한다.
s = 'Spicy &quot;Jalape&#241;o&quot.'
from html.parser import HTMLParser
p = HTMLParser()
print(p.unescape(s))  # 파이썬 3.5 버전부터 deprecated 됨.
print(html.unescape(s))

t = 'The prompt is &gt;&gt;&gt;'
from xml.sax.saxutils import unescape
print(unescape(t))

#  ▣ 토론 : HTML, XML 을 생성할 때 특수 문자를 제대로 이스케이핑하는 과정을 간과하기 쉽다.
#            print() 로 결과물을 생성하거나 기본적인 문자열 서식 기능을 사용할 때 특히 더 그렇다.
#            가장 쉬운 해결책은 html.escape() 와 같은 유틸리티 함수를 사용하는 것이다.


#  2.18 텍스트 토큰화
#  ▣ 문제 : 문자열을 파싱해서 토큰화하고 싶다.
#  ▣ 해결 : 정규 표현식과 scanner() 메소드를 사용한다.

#   - 정규 표현식을 사용.(이름 있는 캡처 그룹)
text = 'foo = 23 + 42 * 10'

import re
NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))

#   - scanner() 메소드를 사용.
scanner = master_pat.scanner('foo = 42')
scanner.match()
print(_.lastgroup, _.group())  # _ 는 파이썬 2.x 버전에서 사용 가능함.
scanner.match()
print(_.lastgroup, _.group())
scanner.match()
print(_.lastgroup, _.group())
scanner.match()
print(_.lastgroup, _.group())
scanner.match()
print(_.lastgroup, _.group())

#   - 이 기술을 사용해 간결한 생성자를 만들 수 있다.
from collections import namedtuple
Token = namedtuple('Token', ['type', 'value'])

def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())

for tok in generate_tokens(master_pat, 'foo = 42'):
    print(tok)

tokens = (tok for tok in generate_tokens(master_pat, text) if tok.type != 'WS')
for tok in tokens:
    print(tok)

#  ▣ 토론 : 보통 더 복잡한 텍스트 파싱이나 처리를 하기 전에 토큰화를 한다.
#            매칭할 때 re 는 명시한 순서대로 패턴을 매칭한다. 따라서 한 패턴이 다른 패턴의 부분이 되는 경우가 있다면
#            항상 더 긴 패턴을 먼저 넣어야 한다.
LT = r'(?P<LT><)'
LE = r'(?P<LE><=)'
EQ = r'(?P<EQ>=)'

master_pat = re.compile('|'.join([LE, LT, EQ]))  # 올바름
master_pat = re.compile('|'.join([LT, LE, EQ]))  # 틀림

for tok in generate_tokens(master_pat, '<='):
    print(tok)

#   - 패턴이 부분 문자열을 형성하는 경우도 조심해야 한다.
PRINT = r'(?P<PRINT>print)'
NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'

master_pat = re.compile('|'.join([PRINT, NAME]))

for tok in generate_tokens(master_pat, 'printer'):
    print(tok)


#  2.19 간단한 재귀 파서 작성
#  ▣ 문제 : 주어진 문법 규칙에 따라 텍스트를 파싱하고 동작을 수행하거나 입력된 텍스트를 추상 신택스 트리로 나타내야 한다.
#            문법은 간단하지만 프레임워크를 사용하지 않고 파서를 직접 작성하고 싶다.
#  ▣ 해결 : 이 문제는 특정 문법에 따라 텍스트를 파싱하는 데 집중한다.
#            우선 문법의 정규 스펙을 BNF 나 EBNF 로 하는 데서 시작한다.
import re
import collections

#   - 토큰 스펙화.
NUM    = r'(?P<NUM>\d+)'
PLUS   = r'(?P<PLUS>\+)'
MINUS  = r'(?P<MINUS>-)'
TIMES  = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS     = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS]))

#   - 토큰화.
Token = collections.namedtuple('Token', ['type', 'value'])

def generate_tokens(text):
    scanner = master_pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok

#   - 파서.
class ExpressionEvaluator:
    '''
        재귀 파서 구현, 모든 메소드는 하나의 문법 규칙을 구현한다.
        현재 룩어헤드 토큰을 받고 테스트하는 용도로 ._accept()를 사용한다.
        입력 받은 내역에 완벽히 매칭하고 다음 토큰을 무시할 때는
        ._expect()를 사용한다. (혹시 매칭하지 않는 경우에는 SyntaxError 를 발생한다.)
    '''

    def parse(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None        # 마지막 심볼 소비
        self.nexttok = None    # 다음 심볼 토큰화
        self._advance()         # 처음 룩어헤드 토큰 불러오기
        return self.expr()

    # generate_tokens() 메서드에서 가져온 토큰을 순차적으로 설정하는 함수
    def _advance(self):
        'Advance one token ahead'
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)  # next 함수는 iterator 를 순차적으로 리턴시켜주는 함수

    # 다음 토큰이 원하는 토큰인 경우 self.tok 에 다음 토큰을 담고 True 를 리턴하는 함수
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

    #   - 문법 규칙.
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

e = ExpressionEvaluator()
print(e.parse('2'))
print(e.parse('2 + 3'))
print(e.parse('2 + 3 * 4'))
print(e.parse('2 + (3 + 4) * 5'))
# print(e.parse('2 + (3 + * 4)'))


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

e = ExpressionTreeBuilder()
print(e.parse('2 + 3'))
print(e.parse('2 + 3 * 4'))
print(e.parse('2 + (3 + 4) * 5'))
print(e.parse('2 + 3 + 4'))

#  ▣ 토론 : 파싱은 컴파일러 과목에서 3주 이상을 할애해서 배우는 쉽지 않은 주제이다.
#            파싱 알고리즘이나 문법과 같은 기본적인 지식을 좀 더 알고 싶다면 우선 컴파일러 책을 한 권 읽어야 한다.
#            재귀 파서의 한 가지 제약으로 좌측 재귀가 포함된 어떠한 문법 규칙에 대해서도 사용할 수 없다.

#   - 정말 복잡한 문법이 있다면 PyParsing 이나 PLY 와 같은 파싱 도구를 사용하는 것이 더 좋다.
from ply.lex import lex
from ply.yacc import yacc

# 토큰 리스트
tokens = ['NUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN']

# 무시 문자
t_ignore = '\t\n'

# 토큰 스펙 (정규 표현식으로)
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

# 렉서(lexer) 만들기
lexer = lex()

# 문법 규칙과 핸들러 함수
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


#  2.20 바이트 문자열에 텍스트 연산 수행
#  ▣ 문제 : 바이트 문자열(byte string)에 일반적인 텍스트 연산(잘라내기, 검색, 치환 등)을 수행하고 싶다.
#  ▣ 해결 : 바이트 문자열도 텍스트 문자열과 마찬가지로 대부분의 연산을 내장하고 있다.
data = b'Hello World'
print(data[0:5])
print(data.startswith(b'Hello'))
print(data.split())
print(data.replace(b'Hello', b'Hello Cruel'))

#   - 바이트 배열에도 사용 가능하다.
data = bytearray(b'Hello World')
print(data[0:5])
print(data.startswith(b'Hello'))
print(data.split())
print(data.replace(b'Hello', b'Hello Cruel'))

#   - 바이트 배열에서도 정규 표현식이 가능하다.
data = b'FOO:BAR,SPAM'
import re
print(re.split(b'[:,]', data))  # 패턴도 바이트로 나타내야 한다.

#  ▣ 토론 : 대개의 경우 텍스트 문자열에 있는 연산 기능은 바이트 문자열에도 내장되어 있다.
#            하지만 주의해야 할 차이점이 몇 가지 있다.

#   - 첫째. 바이트 문자열에 인덱스를 사용하면 개별 문자가 아니라 정수를 가리킨다.
a = 'Hello World'
print(a[0], a[1])

b = b'Hello World'
print(b[0], b[1])

#   - 둘째. 바이트 문자열은 보기 좋은 표현식을 지원하지 않으며, 텍스트 문자열로 변환하지 않으면 깔끔하게 출력할 수도 없다.
s = b'Hello World'
print(s)
print(s.decode('ascii'))

#   - 셋째. 바이트 문자열은 서식화를 지원하지 않는다.
# print(b'%10s %10d %10.2f' %(b'ACME', 100, 490.1))
# print(b'{} {} {}'.format(b'ACME', 100, 490.1))
print('{:10s} {:10d} {:10.2f}'.format('ACME', 100, 490.1).encode('ascii'))

#   - 넷째. 바이트 문자열을 사용하면 특정 연산의 문법에 영향을 주기도 한다.
with open('files/somefile.txt', 'w') as f:
    f.write('spicy')

import os
print(os.listdir('.'))
print(os.listdir(b'.'))
#   ※ 바이트 데이터가 성능상 더 빠르더라도, 코드가 매우 지저분하고 이해하기 어려워지므로 텍스트 데이터를 사용하는 것이 좋다.

# Chapter 3. 숫자, 날짜, 시간
#  3.1 반올림
#  ▣ 문제 : 부동 소수점 값을 10진수로 반올림하고 싶다.
#  ▣ 해결 : 간단한 반올림은 내장 함수인 round(value, ndigits) 함수를 사용한다.
print(round(1.23, 1))  # 소수점 자리 반올림
print(round(1.27, 1))
print(round(-1.27, 1))
print(round(1.25361, 3))
print(round(2.5))

a = 1627731
print(round(a, -1))  # 정수 자리 반올림
print(round(a, -2))
print(round(a, -3))

#  ▣ 토론 : 반올림과 서식화를 헷갈리지 않도록 주의하자. 특정 자리수까지 숫자를 표현하는 것이 목적이라면 round() 를 사용하는 것이 아니라
#           서식화를 위한 자릿수를 명시하기만 하면 된다.
x = 1.23456
print(format(x, '0.2f'))
print(format(x, '0.3f'))
print('value is {:0.3f}'.format(x))

#   - 정확도 문제를 수정하려고 부동 소수점을 반올림하는 방법도 지양해야 한다.
a = 2.1
b = 4.2
c = a + b
print(c)
c = round(c, 2)
print(c)


#  3.2 정확한 10진수 계산
#  ▣ 문제 : 정확한 10진수 계산을 해야 하고, 부동 소수점을 사용할 때 발생하는 작은 오류를 피하고 싶다.
#  ▣ 해결 : 부동 소수점 사용 시 더 정확한 계산을 하고 싶다면, decimal 모듈을 사용해야 한다.
a = 4.2
b = 2.1
print(a + b)
print((a + b) == 6.3)

from decimal import Decimal
a = Decimal('4.2')
b = Decimal('2.1')
print(a+b)
print((a + b) == Decimal('6.3'))

#   - 반올림의 자릿수와 같은 계산적 측면을 조절할 수 있다. (localcontext())
from decimal import localcontext
a = Decimal('1.3')
b = Decimal('1.7')
print(a / b)
with localcontext() as ctx:
    ctx.prec = 3
    print(a / b)

with localcontext() as ctx:
    ctx.prec = 50
    print(a / b)

#  ▣ 토론 : 1. 과학이나 공학, 컴퓨터 그래픽 등 자연 과학 영역을 다룰 때는 부동 소수점 값을 사용하는 것이 더 일반적이다.
#           2. decimal 모듈에 비해 float 의 실행 속도가 확연히 빠르다.
nums = [1.23e+18, 1, -1.23e+18]
print(sum(nums))  # 1이 사라진다.
import math
print(math.fsum(nums))


#  3.3 출력을 위한 숫자 서식화
#  ▣ 문제 : 출력을 위해 자릿수, 정렬, 천 단위 구분 등 숫자를 서식화하고 싶다.
#  ▣ 해결 : 출력을 위해 숫자를 서식화하려면 내장 함수인 format() 을 사용한다.
#   - 소수점 둘째 자리 정확도
x = 1234.56789
print(format(x, '0.2f'))

#   - 소수점 한 자리 정확도로 문자 10개 기준 오른쪽에서 정렬
print(format(x, '>10.1f'))

#   - 왼쪽에서 정렬
print(format(x, '<10.1f'))

#   - 가운데 정렬
print(format(x, '^10.1f'))

#   - 천 단위 구분자 넣기
print(format(x, ','))
print(format(x, '0,.1f'))

#   - 지수 표현법 사용하려면 f 를 e나 E로 바꾸면 된다.
print(format(x, 'e'))
print(format(x, '0.2E'))

print('The Value is {:0,.2f}'.format(x))

#  ▣ 토론 : 출력을 위한 숫자 서식화는 대개 간단하다. 앞에 소개한 기술은 부동 소수점 값과 decimal 모듈의 숫자에 모두 잘 동작한다.
print(format(x, '0.1f'))
print(format(-x, '0.1f'))

#   - 지역 표기법을 따르기 위해 locale 모듈의 함수를 사용한다.
swap_separators = {ord('.'): ',', ord(','): '.'}
print(format(x, ',').translate(swap_separators))

#   - % 연산자로 서식화.
print('%0.2f' % x)
print('%10.1f' % x)
print('%-10.1f' % x)


#  3.4 2진수, 8진수, 16진수 작업
#  ▣ 문제 : 숫자를 2진수, 8진수, 16진수로 출력해야 한다.
#  ▣ 해결 : 정수를 2진수, 8진수, 16진수 문자열로 변환하려면 bin(), oct(), hex() 를 사용한다.
x = 1234
print(bin(x), oct(x), hex(x))
print(format(x, 'b'), format(x, 'o'), format(x, 'x'))

#   - 정수형은 부호가 있는 숫자이므로, 음수를 사용하면 결과물에도 부호가 붙는다.
x = -1234
print(format(x, 'b'), format(x, 'x'))

#   - 부호가 없는 값을 사용하려면 최대값을 더해서 비트 길이를 설정해야 한다.
x = -1234
print(format(2**32 + x, 'b'), format(2**32 + x, 'x'))

#   - 다른 진법의 숫자를 정수형으로 변환하려면 int() 함수에 적절한 진수를 전달한다.
print(int('4d2', 16), int('10011010010', 2))

#  ▣ 토론 : 8 진법을 사용할 때 프로그래머가 주의해야 할 점이 한 가지 있다.
import os
os.chmod('script.py', 0o755)  # 8진법 값 앞에는 0o 를 붙여야 한다. (chmod = 파일 권한 변환)


#  3.5 바이트에서 큰 숫자를 패킹/언패킹
#  ▣ 문제 : 바이트 문자열을 언패킹해서 정수 값으로 만들어야 한다. 혹은 매우 큰 정수 값을 바이트 문자열로 변환해야 한다.
#  ▣ 해결 : int.from_bytes() 메소드를 사용한다.
data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
print(len(data))
print(int.from_bytes(data, 'little'))
print(int.from_bytes(data, 'big'))

#   - 큰 정수 값을 바이트 문자열로 변환하려면 int.to_bytes() 메소드를 사용하고, 바이트 길이와 순서를 명시한다.
x = 94522842520747284487117727783387188
print(x.to_bytes(16, 'big'))
print(x.to_bytes(16, 'little'))

#  ▣ 토론 : 정수형 값과 바이트 문자열 간의 변환은 일반적인 작업이 아니다.
#           하지만 네트워크나 암호화가 필요한 특정 애플리케이션에서 사용하는 경우가 있다.
#           여기서 나온 방법 말고, struct 모듈을 사용할 수도 있다.

#   - struct 로 언패킹할 수 있는 정수형의 크기가 제한적이어서, 언팩을 여러 번 하고 결과 값을 합쳐야 한다.
import struct
hi, lo = struct.unpack('>QQ', data)
print((hi << 64) + lo)

#   - 바이트 순서는 정수형을 이루는 바이트가 가장 작은 것부터 표시되었는지 혹은 가장 큰 것부터 표시되었는지를 나타낸다.
x = 0x01020304
print(x.to_bytes(4, 'big'))
print(x.to_bytes(4, 'little'))

#   - 정수형 값을 바이트 문자열로 변환하려는데 지정한 길이에 다 들어가지 않는 경우에는 에러가 발생하므로, int.bit_length() 메소드로 확인한다.
x = 523 ** 23
print(x.bit_length())
nbytes, rem = divmod(x.bit_length(), 8)  # byte 자리수, 나머지 리턴
if rem:
    nbytes += 1
print(x.to_bytes(nbytes, 'little'))


#  3.6 복소수 계산
#  ▣ 문제 : 최신 웹 인증을 사용하는 코드를 작성하던 도중에 특이점을 발견하고 복소수 평면을 사용할 수 밖에 없는 상황에 처했다.
#           혹은 복소수를 사용하여 계산을 해야 한다.
#  ▣ 해결 : 복소수는 complex(real, imag) 함수를 사용하거나 j를 붙인 부동 소수점 값으로 표현할 수 있다.
a = complex(2, 4)
b = 3 - 5j
print(a, b)

#   - 실수, 허수, 켤레 복소수(허수 부분의 부호를 바꾼 복소수)를 구하는 방법.
print(a.real, a.imag, a.conjugate())

#   - 일반적인 수학 계산하는 방법.
print(a + b)
print(a * b)
print(a / b)
print(abs(a))  # 절대값

#   - 사인, 코사인, 제곱 등을 계산하려면 cmath 모듈을 사용한다.
import cmath
print(cmath.sin(a))
print(cmath.cos(a))
print(cmath.exp(a))

#  ▣ 토론 : 파이썬의 수학 관련 모듈은 대개 복소수를 인식한다. 예를 들어, numpy 를 사용하면 어렵지 않게 복소수 배열을 만들고 계산할 수 있다.
import numpy as np
a = np.array([2+3j, 4+5j, 6-7j, 8+9j])
print(a)
print(a+2)
print(np.sin(a))

#   - 하지만 파이썬의 표준 수학 함수는 기본적으로 복소수 값을 만들지 않는다.
#     따라서 코드에서 이런 값이 예상치 않게 발생하지는 않는다.
import math
print(math.sqrt(-1))
import cmath
print(cmath.sqrt(-1))  # cmath 모듈이 복소수에 대해 지원한다.


#  3.7 무한대와 NaN 사용
#  ▣ 문제 : 부동 소수점 값의 무한대, 음의 무한대, NaN(not a number)을 검사해야 한다.
#  ▣ 해결 : 이와 같은 특별한 부동 소수점 값을 표현하는 파이썬 문법은 없지만 float() 를 사용해서 만들 수는 있다.
a = float('inf')
b = float('-inf')
c = float('nan')
print(a, b, c)

#   - 값을 확인하기 위해 math.isinf() 와 math.isnan() 함수를 사용한다.
print(math.isinf(a), math.isinf(b))
print(math.isnan(c))

#  ▣ 토론 : 앞에 나온 특별한 부동 소수점 값에 대한 더 많은 정보를 원한다면 IEEE 754 스펙을 확인해야 한다.

#   - 무한대 값은 일반적인 수학 계산법을 따른다.
a = float('inf')
print(a + 45)
print(a * 10)
print(10 / a)

#   - 특정 연산자의 계산은 정의되어 있지 않고 NaN 을 발생시킨다.
print(a / a)
b = float('-inf')
print(a + b)

#   - NaN 값은 모든 연산자에 대해 예외를 발생시키지 않는다.
c = float('nan')
print(c + 23)
print(c / 2)
print(c * 2)
print(math.sqrt(c))

#   - NaN 에서 주의해야 할 점은, 이 값은 절대로 비교 결과가 일치하지 않는다는 점이다.
c = float('nan')
d = float('nan')
print(c == d)
print(c is d)


#  3.8 분수 계산
#  ▣ 문제 : 타임머신에 탑승했는데 갑자기 분수 계산을 하는 초등학생이 되어 버렸다.
#           혹은 목공소에서 만든 측량기에 관련된 계산을 하는 코드를 작성해야 한다.
#  ▣ 해결 : 분수 관련 계산을 위해 fractions 모듈을 사용한다.
from fractions import Fraction
a = Fraction(5, 4)
b = Fraction(7, 16)
print(a + b)
print(a * b)

#   - 분자 / 분모 구하기
c = a * b
print(c.numerator)  # 분자
print(c.denominator)  # 분모

#   - 소수로 변환
print(float(c))

#   - 분자를 특정 값으로 제한
print(c.limit_denominator(8))

#   - 소수를 분수로 변환
x = 3.75
y = Fraction(*x.as_integer_ratio())  # x.as_integer_ratio() : float 을 (분자, 분모) 를 쌍으로 가지는 튜플로 리턴한다.
print(y)

#  ▣ 토론 : 프로그램에서 치수 단위를 분수로 받아서 계산을 하는 것이 사용자가 소수로 직접 변환하고 계산하는 것보다 더 편리할 수 있다.


#  3.9 큰 배열 계산
#  ▣ 문제 : 배열이나 그리드와 같이 커다란 숫자 데이터 세트에 계산을 해야 한다.
#  ▣ 해결 : 배열이 관련된 커다란 계산을 하려면 NumPy 라이브러리를 사용한다.
#            NumPy 를 사용하면 표준 파이썬 리스트를 사용하는 것보다 수학 계산에 있어 훨씬 효율적이다.

#   - 파이썬 리스트
x = [1, 2, 3, 4]
y = [5, 6, 7, 8]
print(x * 2)
print(x + 10)  # 수행 안됨

#   - Numpy 배열
import numpy as np
ax = np.array([1, 2, 3, 4])
ay = np.array([5, 6, 7, 8])
print(ax*2)
print(ax + 10)
print(ax + ay)
print(ax * ay)

def f(x):
    return 3*x**2 - 2*x + 7
print(f(ax))

#   - Numpy 는 배열에 사용 가능한 "일반 함수"를 제공한다.
print(np.sqrt(ax))
print(np.cos(ax))
#    ※ 일반 함수는 배열 요소를 순환하며 요소마다 math 모듈 함수로 계산하는 것보다 수백 배 빠르다.

#   - 10,000 x 10,000 2차원 그리드를 만드는 경우.
grid = np.zeros(shape=(10000, 10000), dtype=float)
print(grid)
grid += 10
print(grid)
print(np.sin(grid))

#   - Numpy 는 다차원 배열의 인덱싱 기능을 확장하고 있다.
a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print(a)
print(a[1])
print(a[:, 1])
print(a[1:3, 1:3])
a[1:3, 1:3] += 10
print(a)

#   - 행 벡터를 모든 행 연산에 적용
print(a + [100, 101, 102, 103])
print(a)

#   - 조건이 있는 할당
print(np.where(a < 10, a, 10))

#  ▣ 토론 : Numpy 는 파이썬의 수많은 과학, 공학, 라이브러리의 기초가 된다.
#           또한 광범위하게 사용되는 모듈 중 가장 복잡하고 방대한 것 중 하나이다.


#  3.10 행렬과 선형 대수 계산
#  ▣ 문제 : 행렬 곱셈, 행렬식 찾기, 선형 방정식 풀기 등 행렬이나 선형 대수 계산을 해야 한다.
#  ▣ 해결 : Numpy 라이브러리에 이런 용도로 사용할 수 있는 matrix 객체가 있다.
import numpy as np
m = np.matrix([[1, -2, 3], [0, 4, 5], [7, 8, -9]])
print(m)

#   - 전치 행렬
print(m.T)

#   - 역행렬
print(m.I)

#   - 벡터를 만들고 곱하기
v = np.matrix([[2], [3], [4]])
print(v)
print(m * v)

import numpy.linalg

#   - 행렬식(determinant) : ad-bc
print(numpy.linalg.det(m))

#   - 고유값(eigenvalues) :  한 요인이 설명해 줄 수 있는 변수들의 분산 총합.
print(numpy.linalg.eigvals(m))

#   - mx = v 에서 x 풀기
x = numpy.linalg.solve(m, v)
print(x)
print(m * x)
print(v)

#  ▣ 토론 : 선형 대수의 범위는 너무 방대해서 이 책에서 다 다룰 수 없다.
#           하지만 행렬과 벡터를 다루어야 한다면 Numpy 부터 시작하도록 하자.