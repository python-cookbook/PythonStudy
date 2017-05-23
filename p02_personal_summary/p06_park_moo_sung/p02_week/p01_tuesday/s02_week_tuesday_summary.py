##############################################
#2.17 html 과 xml 엔티티 처리(일단은 패스... 어렵다)

# 특수문자 피하기

import html
s = 'Elements "<tag>text</tag>"'
print(s)
'''Elements "<tag>text</tag>"'''

print(html.escape(s))
'''Elements &quot;&lt;tag&gt;text&lt;/tag&gt;&quot;'''  # 뭐지..

print(html.escape(s, quote=False)) # 큰 따옴표는 남기고 싶을 때
'''Elements "&lt;tag&gt;text&lt;/tag&gt;"'''

# 텍스트를 아슼키로 만들고, 캐릭터 코드를 다른 문자에 끼워넣고 싶을때(....?)

s = 'Spicy Jalapeno'
print(s.encode('ascii', errors = 'xmlcharrefreplace'))
# b'Spicy Jalapeno    #  b가 생겼네?

###############################################

# 2.18 텍스트 토큰화

# 문자열 파싱

text = 'foo = 23 + 42 * 10'
tokens = [('NAME','foo') ,('EQ', '='), ('NUM','23'), ('PLUS', '+'), ('NUM', '42'), ('TIMES', '*'), ('NUM', '10')]

import re
NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))
scanner = master_pat.scanner('foo = 42')
print(scanner.match())
'''<_sre.SRE_Match object; span=(0, 3), match='foo'>'''

'''_.lastgroup( ????? )'''


# 생성자 만들기

from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())

for tok in generate_tokens(master_pat, 'foo'):
    print(tok)
'''Token(type='NAME', value='foo')'''  # 근데 이걸 어디에 쓰는거지 ?

##############################################

# 2.19 간단한 ?!?!?! 재귀 파서 작성

# 어려운 재귀 표현식 해석기 만들기
import re
import collections

    # 토큰 스펙화
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS]))

    # 토큰화
Token = collections.namedtuple('Token', ['type','value'])

def generate_tokens(text):
    scanner = master_pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup. m.group())
        if tok.type != 'WS' :
            yield tok

    # 파서
class ExpressionEvaluator :
    def parse(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None
        self.nexttok = None
        self._advance()
        return self.expr()
    def _advance(self):
        'Advance one token ahead'
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self,toktype):
        'Test and consume the next token if it matches toktype'
        if self.nexttok and self.nexttok.type == toktype :
            self._advance()
            return True
        else :
            return False
    def _expect(self,toktype):
        'Consume next token if it matches toktype or raise SyntaxError'
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    # 문법 규칙

    def expr(self):
        'expression :: = term { ('+' | '-') term |* '

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
        'term ::= factor { ('*' | '/') factor |*'

        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            if op == 'TIMES' :
                termval *= right
            elif op == 'DIVIDE' :
                termval /= right
        return termval

    def factor(self):
        'factor ::= NUM | (expr)'
        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else :
            raise SyntaxError('Expected NUMBER or LPAREN')

e = ExpressionEvaluator()
print(e.parse('2'))
print(e.parse('2 + 3'))
print(e.parse('2 + (3 + *4)'))
###### 일단 적어놓기... ######

# ply 를 활용한 예

from ply.lex import lex
from ply.yacc import yacc

    # 토큰 리스트
tokens = ['NUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN']

    # 무시 문자
t_ignore = ' \t\n'

    # 토큰 스펙(정규식으로)
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
    print('Bad character : {!r}'.format(t.value[0]))
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
    expr :term
    :param p: 
    :return: 
    '''
    p[0] = p[1]

def p_term(p):
    '''
    term : term TIMES factor
         | term DIVIDE factor
    :param p: 
    :return: 
    '''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_term_factor(p):
    '''
    term : factor
    :param p: 
    :return: 
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
    print('Systax error')

parser = yacc()

# 무슨 말인지...


##############################################

# 2.20 바이트 문자열에 텍스트 연산 수행

data = b'hello world'
print(data[0:5])
## b'hello

print(data.startswith(b'hello'))
## True

datas = data.split()
print(datas)
## [b'hello', b'world']

cruelworld = data.replace(b'hello', b'hello cruel')
print(cruelworld)
## b'hello cruel world'

# 정규식 쓸 때(패턴 자체도 바이트로 나타내야 함)

import re
data = b'Foo:Bar,Spam'
datas = re.split(b'[:,]',data)  # b를 앞에 붙여줘서 바이트로 나타내야 함
print(datas)
## [b'Foo', b'Bar', b'Spam']

# 텍스트 문자열과 다른 바이트 문자열의 특징

## 바이트 문자열에 인덱스 사용시 개별 문자가 아닌 정수 가리킴

a = 'hello'  # 텍스트 문자열
print(a[0])
## h

b = b'hello' # 바이트 문자열
print(b[0])
## 104

## 깔끔한 출력 x

s= b'hello'               # 깔끔 x
print(s)
## b'hello'
print(s.decode('ascii'))  # 텍스트 문자열로 변환
## hello

## 서식화 지원(format) x --> 출력하려면 format(텍스트 문자열).encode('ascii') 해줘야 함

## 파일 시스템에 영향(파일 이름을 바이트 문자열로 줄 경우 대개 파일 이름 인코딩/디코딩 x)

################################################

# 3.1 반올림

# round(x, 3) --> 소수점 3자리까지 표시

# round(x, -1) --> 10의 자리부터 표시(1의 자리 반올림)

# 반올림 vs 서식화 --> 단지 특정 자리까지 표현만 하고 싶다면 데이터 변경하는 반올림 대신 서식화 ㄱㄱ

x = 1.23456

print(format(x, '0.2f'))
## 1.23

print('value is {:0.3f}'.format(x))
## value is 1.235

##################################################

# 3.2 정확한 10진수 계산

# 부동 소수점 값의 문제점(10진수 정확히 표현 x)

a = 4.2
b = 2.1
print(a+b)
## 6.30000000001
print((a+b) == 6.3)
## False

# 더 정확히 계산하기 위해서는 but 속도 떨어짐(decimal 모듈 사용)

from decimal import Decimal

a= Decimal('4.2')     # 정확한 10진수 표현 가능
b= Decimal('2.1')
print(a+b)
## 6.3

from decimal import localcontext
a = Decimal('1.3')
b = Decimal('1.7')
print(a/b)
## 0.7647058823529411764705882353

with localcontext() as ctx:   # 이게 뭐지
    ctx.prec = 3              # 값을 원하는 소수점 자리만큼 출력하는 함수인듯
    print(a/b)
## 0.765

# 수학 연산의 오류 및 방지법

nums = [1.23e+18, 1, -1.23e+18]
print(sum(nums))
## 1 이어야 하는데 0 나옴

import math
print(math.fsum(nums))
## 값이 정확히 나옴



##############################################

# 3.3 출력을 위한 숫자 서식화

# format()

x = 1234.56789

print(format(x, '0.2f'))  # 소수점 둘째 자리 정확도
## 1234.57
print(format(x, '>10.1f'))  # 소수점 첫 자리 정확도. 문자 10개 기준 오른쪽에서 정렬
##     1234.6
print(format(x, '<10.1f'))  # 소수점 첫 자리 정확도. 문자 10개 기준 왼쪽에서 정렬
## 1234.6
print(format(x, '^10.1f'))  # 소수점 둘째 자리 정확도
##   1234.6
print(format(x, ','))  # 숫자 천 단위 구분자
## 1,234.56789
print(format(x, '0,.1f'))  # 숫자 천 단위 구분자 + 소수점 첫 자리 정확도
## 1,234.6
print(format(x,'e')) # 지수 표현식
## 1.234568e+03
print(format(x,'0.2e'))  # 지수표현식 소수점 둘째 자리까지
## 1.23e+03
print('the value is {:0,.2f}'.format(x))
## the value is 1,234.57

# 이건 뭐지?

swap_separators = { ord('.'):',', ord(','):'.'} # . 쓰여야할 때 , 를 쓰고, , 쓰여야할 때 . 쓰도록 함
print(format(x, ',').translate(swap_separators))
## 1.234,56789


# 숫자 % 연산자

print('%0.2f' % x)  # 숫자를 % 연산자로 서식화할 수 있음
## 1234.57

print('%10.1f' % x)  # print(format(x, '>10.1f')) 과 일치
##     1234.6

print('%-10.1f' % x)  # print(format(x, '<10.1f')) 과 일치
## 1234.6

################################################

# 3.4 2진수, 8진수, 16진수

# 2진수( bin() ), 8진수( oct() ), 16진수( hex() )

x = 1234
print(bin(x))      # 0b 없애려면 ? print(format(x, 'b'))
## 0b10011010010
print(oct(x))      # 0o 없애려면 ? print(format(x, 'o'))
## 0o2322
print(hex(x))      # 0x 없애려면 ? print(format(x, 'x'))
## 0x4d2

# 다시 정수로 바꾸고 싶다면?

print(int('4d2', 16)) # 16진법을 10진법으로 바꾸기

# 주의사항 --> 8진법 값 앞에는 0o 를 붙여야 에러 안남

#################################################

# 3.9 큰 배열 계산(중요!!!!!)

# 파이썬 리스트(아마 문자열 계산처럼 되는듯?)

x= [1,2,3,4]
print(2*x)
## [1, 2, 3, 4, 1, 2, 3, 4]
print(x+x)
## [1, 2, 3, 4, 1, 2, 3, 4]

# numpy array(행렬 계산이 되네)

import numpy as np
ax = np.array([1,2,3,4])
print(ax * 2)
## [2 4 6 8]
print(ax + ax)
## [2 4 6 8]

# 간단한 연산(빠름)

print(np.sqrt(ax))
## [ 1.          1.41421356  1.73205081  2.        ]
print(np.cos(ax))
## [ 0.54030231 -0.41614684 -0.9899925  -0.65364362]

# 거대한 2차원 배열 만들고 연산하기

grid = np.zeros(shape=(10000,10000), dtype=float)
print(grid)
grid += 10  # 모든 행렬에 동시 적용

# 인덱싱 기능(중요!!!)

a = np.array([[i + 4*j for i in range(4)] for j in range(4)])
print(a)
'''
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]
 [12 13 14 15]]
'''

print(a[1])
## [4 5 6 7]

print(a[:,1])
## [ 1  5  9 13]

print(a[1:3, 1:3])
'''
[[ 5  6]
 [ 9 10]]
'''

a[1:3, 1:3] += 10
print(a[1:3, 1:3])
'''
[[15 16]
 [19 20]]
'''

a += [100, 101, 102, 103]
print(a)
'''
[[100 102 104 106]
 [104 116 118 110]
 [108 120 122 114]
 [112 114 116 118]]
'''

a -= [100, 101, 102, 103]
print(a)
'''
[[ 0  1  2  3]
 [ 4 15 16  7]
 [ 8 19 20 11]
 [12 13 14 15]]
'''
b = np.where(a>10, a, 0) ##### 신기하네 #####
print(b)
'''
[[ 0  0  0  0]
 [ 0 15 16  0]
 [ 0 19 20 11]
 [12 13 14 15]]
'''

#################################################

# 3.10 행렬과 선형대수계산(중요!!!!!!!!!!!!!!!!!!!!!!)

# numpy matrix(numpy array와 비슷하나 선형대수 계산법 따름)

import numpy as np
m = np.matrix([[1,-2,3],[0,4,5],[7,8,-9]])
print(m)
'''
[[ 1 -2  3]
 [ 0  4  5]
 [ 7  8 -9]]
'''

# transpose

print(m.T)
'''
 [[ 1  0  7]
 [-2  4  8]
 [ 3  5 -9]]
'''

# inverse

print(m.I)
'''
[[ 0.33043478 -0.02608696  0.09565217]
 [-0.15217391  0.13043478  0.02173913]
 [ 0.12173913  0.09565217 -0.0173913 ]]
'''

# 벡터 만들기

v = np.matrix([[2],[3],[4]])
print(v)
'''
[[2]
 [3]
 [4]]
 '''

# 행렬 곱

print(m * v)
'''
[[ 8]
 [32]
 [ 2]]
'''

# numpy.linalg

import numpy.linalg

# determinant(행렬식)

print(numpy.linalg.det(m))
## -230.0


# eigenvalues(아이겐밸류)

print(numpy.linalg.eigvals(m))
## [-13.11474312   2.75956154   6.35518158]

# mx = v 에서 해(x) 구하기

print(numpy.linalg.solve(m,v))
'''
[[ 0.96521739]
 [ 0.17391304]
 [ 0.46086957]]
'''

