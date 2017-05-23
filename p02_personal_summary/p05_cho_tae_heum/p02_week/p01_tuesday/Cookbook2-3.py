# 2.17 HTML과 XML엔티티 처리
import html
s = 'Element ate wrriten as "<tag>text</tag>".'
print(s)
print(html.escape(s))

s = 'Spicy Jalapeno'
print(s.encode('ascii', errors='xmlcharrefreplace'))



text = 'foo = 23 + 42 * 10'
tokens = [('NAME', 'foo'), ('EQ', '='), ('NUM', '23'), ('PLUS', '+'), ('NUM', '42'),
          ('TIMES', '*'), ('NUM', '10')]

import re
NAME  = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM   = r'(?P<NUM>\d+)'
PLUS  = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ    = r'(?P<EQ>=)'
WS    = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))
print(master_pat)

scanner = master_pat.scanner('foo = 42')
scanner.match()



from collections import name
Token = namedtuple('Token', ['type', 'value'])
def generator_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())

for tok in generator_tokens(master_pat, 'foo=42'):
    print(tok)

token = (tok for tok in generator_tokens(master_pat, text) if tok.type != 'WS')
for tok in tokens:
    print(tok)


# 2.19 간단한 재귀 파서작성
expr ::= expr + term
expr ::= expr - term
expr ::= term

expr ::= expr * term
expr ::= expr / term
expr ::= factor

expr ::= (expr)
expr ::= NUM

expr ::= term {(+|-) term }*
term ::= factor {(*|/) factor}*
factor ::= (expr)
    |   NUM


class ExpressionEvaluator:


    def parse(self,text):
        self.tokens = generate_tokens(text)
        self.tok = None             # Last symbol consumed
        self.nexttok = None         # Next symbol tokenized
        self._advance()             # Load first lookahead token
        return self.expr()

    def _advance(self):
        'Advance one token ahead'
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self,toktype):
        'Test and consume the next token if it matches toktype'
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self,toktype):
        'Consume next token if it matches toktype or raise SyntaxError'
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    # Grammar rules follow

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


# 2.20 바이트문자열에 텍스트 연산수행
data = b'Hello World'
data[0:5]
data.startswith(b'Hello')

data.split()
data.replace(b'Hello', b'hello cruel')

data = b'FOO:BAR, SPAM'

import re
re.split(b'[:,]', data)
re.split(b'[:,]', data)

a = 'Hello World'   # 텍스트 문자열
print(a[0])
print(a[1])
b = b'Hello World'  # 바이트 문자열
print(b[0])
print(b[1])         # 바이트 표시

round(1.23, 1)
round(1.27, 1)
round(1.23234, 3)
a = 1238943
print(round(a, -1))

x = 123456
print(round(x, -2))
print(round(x, -3))

a = 1.21254
print(round(a, 2))
print(round(a, 3))

x = 1.23434
print(format(x, '0.2f'))
print(format(x, '0.3f'))

'value is {:0.3f}'.format(x)  # 세자리 빼서 넣기

a = 2.1
b = 4.2
c = a+b
print(c)  # 부동 소수점을 반올림하는 방법도 지양해야 한다. 정확하게 되지 않는다


# 3.2 정확한 10진수 계산

a = 2.1
b = 4.2
print((a + b) == 6.3)

# cpu와 IEEE 754로 부동소수점 숫자 계산을 할때 발생한다. 그냥 이렇게 알고 있어

from decimal import Decimal
a = Decimal('4.2')
b = Decimal('2.1')
print(a + b)       # 정확히 계산하고 싶으면 이렇게

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


# 3.3 출력을 위한 숫자 서식화

x = 1234.2323
format(x, '0.2f')

format(x, '>10.1f')

format(x, '<10.1f')

format(x, '^10.1f')

format(x, ',')
format(x, '0.1f')

format(x, 'e')
format(x, '0.2E')

x
format(x, '0.1f')
format(-x, '0.1f')

print('%0.2f' % x)
print('%10.1f' % x)
print('%-10.1f' % x)


# 3.4 2진수, 8진수, 16진수
x = 1234
print(bin(x))   # 2진수
print(oct(x))   # 8
print(hex(x))   # 16


format(x, 'b')  # 2
format(x, 'o')  # 8
format(x, 'x')  # 16

x = -1234
print(format(x, 'b'))
print(format(x, 'x'))   # 음수 사용하면 음수부호

x = -1234
print(format(2**32 + x, 'b'))
print(format(2**32 + x, 'o'))
print(format(2**32 + x, 'x'))

int('4d2', 16)          # 이거 16진수다,
int('10011010010', 2)   # 이거 2진수다 뜻

x =  [1, 2, 3, 4]
y =  [5, 6, 7, 8]
print(x * 2)
print(x + 10)   # 이건 안된다. 10이 숫자라서
print(x + y)

import numpy as np
ax = np.array([1,2,3,4])
ay = np.array([5,6,7,8])

print(ax*2)
print(ax+10)
print(ax+ay)
print(ax*ay)    # numpy 아주 중요함

def f(x):
    return 3*x**2 - 2*x +7

print(f(ax))  # 아주 신기하구만

import numpy as np

ax = np.array([1,2,3,4])


ay = np.array([5,6,7,8])

print(np.sqrt(ax))

print(np.cos(ax))

grid = np.zeros(shape=(10000,10000), dtype=float)
print(grid)   # 행렬 졸라 쉽게 그리기

grid = np.zeros(shape=(10000,10000), dtype=float)
grid+=10    # 이거 좀 헷갈림
print(grid)

np.sin(grid)
print(grid)


import numpy as np
a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])  # 원래 함수모양이 이렇기 때문에 주의!
print(a)


a[1]

a[:,1]

a[1:3, 1:3]
a[1:3, 1:3] += 10
np.where(a<10, a, 10)


# 3.10 행렬과 선형대수 계산

import numpy as np
m = np.matrix([[1,-2,3],[0,4,5],[7,8,-9]])
print(m)

print(m.T)     # 전치행렬 : 대각선으로 반 갈라서 뒤집은 모양
print(m.I)     # 역행렬

v = np.matrix([[2], [3], [4]])
print(v)
print(m*v)   # 백터를 만들고 곱하기 이게 뭔뜻??

import numpy.linalg   

print(numpy.linalg.det(m))

print(numpy.linalg.eigvals(m))

x = numpy.linalg.solve(m,v)


print(x)

print(m*x)

print(v)
