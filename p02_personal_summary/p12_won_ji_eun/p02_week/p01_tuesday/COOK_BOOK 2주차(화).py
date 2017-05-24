            #2.17 HTML과 XML 엔티티 처리

#문제: 텍스트를 생성할 때 특정문자를 피하고 싶다.

    #예제 html.escape()
s='Elemnets are written as "<tag>text</tag>".'
import html
print (s)
#실행결과 Elemnets are written as "<tag>text</tag>".

print(html.escape(s))
#실행결과 Elemnets are written as &quot;&lt;tag&gt;text&lt;/tag&gt;&quot;.

print(html.escape(s, quote=False))
#실행결과 Elemnets are written as "&lt;tag&gt;text&lt;/tag&gt;".

s='Spicy Jalapeno'
s.encode('ascii', errors='xmlcharrefreplace')
#실행결과 b'Spicy Jalapeno'

s= 'Spicy &quot;Jalape&#241;o&o&quot.'
from html.parser import HTMLParser
p=HTMLParser()
p.unescape(s)
#실행결과 'Spicy "Jalapeño&o".'

t='The prompt is $pt;&gt;&gt;'
from xml.sax.saxutils import unescape
unescape(t)
#실행결과 'The prompt is $pt;>>'



            #2.18 텍스트 토큰화
#문제 문자열을 파싱해서 토큰화하고 싶다.
    
    #예제1 
text='foo=23+42*10'
tokens =[('NAME','foo'),('EQ','='),('NUM','23'),('PLUS','+'),('NUM','42'),('times','*'),('NUM','10')]

#문장을 조각내고 싶다.
import re
NAME = r'(?P<NAME>[a-zA-Z][a-zA-Z_0-9]*)'  # ? : 0또는 1회 반복      
                                           # * : 0회 이상 반복
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'  # +: 1회 이상 반복

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))

scanner = master_pat.scanner('kjhjkhljkj = 1 + 2 + 4')

scanner.match() # match()를 반복적으로 하나씩 호출
#실행결과 <_sre.SRE_Match object; span=(0, 3), match='foo'>
_.lastgroup, _.group()                                 
#실행결과 ('NAME', 'foo')

scanner.match()
#실행결과 <_sre.SRE_Match object; span=(3, 4), match=' '>

_.lastgroup, _.group()                                   
#실행결과 ('WS', ' ')

scanner.match()
#실행결과  <_sre.SRE_Match object; span=(4, 5), match='='>

_.lastgroup, _.group()  
#실행결과 ('EQ', '=')

scanner.match()
#실행결과 <_sre.SRE_Match object; span=(5, 6), match=' '>

_.lastgroup, _.group()  
#실행결과 ('WS', ' ')

scanner.match()
#실행결과  <_sre.SRE_Match object; span=(6, 8), match='42'>

_.lastgroup, _.group()  
#실행결과 ('NUM', '42')

    #예제 
from collections import namedtuple
Token = namedtuple('Token', ['type', 'value'])

def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token (m.lastgroup, m.group())
        
for tok in generate_tokens(master_pat, 'foo= 42'):
    print(tok)

#실행결과 
Token(type='NAME', value='foo')
Token(type='EQ', value='=')
Token(type='WS', value=' ')
Token(type='NUM', value='42') 

                

            #2.19 간단한 재귀파서 작성
            
    #예제
    
import re
import collections

NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>\+)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>\*)'
LPAREN = r'(?P<LPAREN>\*)'
RPAREN = r'(?P<RPAREN>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'  # +: 1회 이상 반복

master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS]))
Token = collections.namedtuple('Token', ['type', 'value'])

def generate_tokens(text):
    scanner = master_pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok


# 파서
class ExpressionEvaluator:

    def parse(self,text):
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
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self,toktype):
        'Consume next token if it matches toktype or raise SyntaxError'
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    # 문법규칙

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

# Example of building trees

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
#실행결과 5
    print(e.parse('2 + 3 * 4'))
#실행결과 14
    print(e.parse('2 + (3 + 4) * 5'))
#실행결과 Expected NUMBER or LPAREN
    print(e.parse('2 + 3 + 4'))
#실행결과 9



            #2.20 바이트 문자열에 텍스트 연산 수행
            
#문제 : 바이트 문자열에 일반적인 텍스트 연산(잘라내기, 검색, 치환 등)을 수행하고 싶다.

    #예제
data = b'Hello World'
data[0:5]
                          
#실행결과 b'Hello'

data.startswith(b'Hello')

#실행결과 True

data.split()
#실행결과 [b'Hello', b'World']

data.replace(b'Hello', b'Hello Cruel')
#실행결과 b'Hello Cruel World'

data = bytearray(b'Hello World')
data[0:5]
#실행결과 bytearray(b'Hello')

data.startswith(b'Hello')
#실행결과 True

data.split()
#실행결과 [bytearray(b'Hello'), bytearray(b'World')]

data.replace(b'Hello', b'Hello Cruel')
#실행결과 bytearray(b'Hello Cruel World')

data = b'FOO:BAR, SPAM'
import re
re.split(b'[:,]',data)
#실행결과 [b'FOO', b'BAR', b' SPAM']




                        #Chapter 3
                        
                #3.1 반올림
round(1.23,1)
#실행결과 1.2
round(1.27,1)
#실행결과 1.3
round(-1.27,1)
#실행결과 -1.3
round(1.25361,3)
#실행결과 1.254

a= 1627731
round(a,-1)
#실행결과 1627730

round(a,-2)
#실행결과 1627700

round(a,-3)
#실행결과 1628000

x=1.23456
format(x,'0.2f')
#실행결과 '1.23'

format(x,'0.3f')
#실행결과 '1.235'

'value is {:0.3f}'.format(x)
#실행결과 'value is 1.235'



            #3.2 정확한 10진수 계산
    #예제
a=4.2
b=2.1
a+b
#실행결과  6.300000000000001

(a+b)==6.3
#실행결과 False

from decimal import Decimal
a=Decimal('4.2')
b=Decimal('2.1')
a+b
#실행결과 Decimal('6.3')

print(a+b)
#실행결과  6.3

(a+b)==Decimal('6.3')
#실행결과 True

from decimal import localcontext
a=Decimal('1.3')
b=Decimal('1.7')
print(a/b)
#실행결과 0.7647058823529411764705882353

with localcontext() as ctx:
    ctx.prec = 3
    print(a/b)
#실행결과 0.765

with localcontext() as ctx:
    ctx.prec = 50
    print(a/b)

#실행결과 0.76470588235294117647058823529411764705882352941176



            #3.3 출력을 위한 숫자 서식화
            
#자릿수, 정렬, 천단위 구분 등 숫자를 서식화 하고 싶다.

x=1234.56789
format(x,'0.2f') # 소수점 둘째 자리 정확도
#실행결과 '1234.57'

format(x,'>10.1f') # 소숫점 한 자리 정확도로 문자 10개 기준 오른쪽에서 정렬
#실행결과 '    1234.6'

format(x,'<10.1f') #왼쪽에서 정렬
#실행결과 '1234.6    '

format(x,'^10.1f') #가운데 정렬
#실행결과 '  1234.6  '

format(x,',') #천 단위 구분자 넣기
#실행결과 '1,234.56789'
format(x,'0,.1f') 
#실행결과 '1,234.6'

format(x,'e')
#실행결과 '1.234568e+03'
format(x,'0.2E')
#실행결과 1.23E+03'

'The value is {:0,.2f}'.format(x)
#실행결과 'The value is 1,234.57'



            #3.4 2진수, 8진수, 16진수 작업
            
    #예제
x=1234
bin(x)
#실행결과 '0b10011010010'

oct(x)
#실행결과 '0o2322'

hex(x)
#실행결과 '0x4d2'

x=1234
bin(x,'b')
#실행결과 '10011010010'

oct(x,'o')
#실행결과 '2322'

hex(x,'x')
#실행결과 '4d2'

x=-1234
format(x,'b')
#실행결과 '-10011010010'
format(x,'x')
#실행결과 '-4d2'

x=-1234
format(2**32+x,'b')
#실행결과 '11111111111111111111101100101110'
format(2**32+x,'x')
#실행결과 'fffffb2e'

int('4d2',16) #정수로 변환
#실행결과 1234
int('10011010010',2)
#실행결과 1234



            #3.9 큰 배열 계산
            
#문제 : 커다란 숫자 데이터세트에 계산
#해결방법: NumPy 라이브러리 사용    

    #예제 파이썬 리스트와 NumPy 차이점
    
#파이썬 리스트
x=[1,2,3,4] 
y=[5,6,7,8]
x*2
#실행결과 [1, 2, 3, 4, 1, 2, 3, 4]

x+10
#실행결과  can only concatenate list (not "int") to list


#Numpy 배열
import numpy as np
ax=np.array([1,2,3,4])
ay=np.array([5,6,7,8])
ax*2                                
#실행결과 array([2, 4, 6, 8])
ax+10
#실행결과 array([11, 12, 13, 14])
ax+ay
#실행결과  array([ 6,  8, 10, 12])
ax*ay
#실행결과 array([ 5, 12, 21, 32])

def f(x):
    return 3*x**2 - 2*x +7

f(ax)
#실행결과 array([ 8, 15, 28, 47])

np.sqrt(ax)
#실행결과 array([ 1.        ,  1.41421356,  1.73205081,  2.        ])
np.cos(ax)
#실행결과 array([ 0.54030231, -0.41614684, -0.9899925 , -0.65364362])

    #예제 10000*1000의 2차원 그리드를 만들고 싶다
grid = np.zeros(shape=(10000,10000),dtype=float)
grid
#실행결과 
#array([[ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       ..., 
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.]])
    
grid +=10
grid

#실행결과 
array([[ 10.,  10.,  10., ...,  10.,  10.,  10.],
       [ 10.,  10.,  10., ...,  10.,  10.,  10.],
       [ 10.,  10.,  10., ...,  10.,  10.,  10.],
       ..., 
       [ 10.,  10.,  10., ...,  10.,  10.,  10.],
       [ 10.,  10.,  10., ...,  10.,  10.,  10.],
       [ 10.,  10.,  10., ...,  10.,  10.,  10.]])
    
    
np.sin(grid)

#실행결과 
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
    
a = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
a
#실행결과 
array([[ 1,  2,  3,  4],
       [ 5,  6,  7,  8],
       [ 9, 10, 11, 12]])
    
#첫번째 행 선택
a[0]    
#실행결과 array([1, 2, 3, 4])

#첫번째 열 선택
a[:,0]
#실행결과 array([1, 5, 9])


#지역을 선택후 변경
a[1:3, 1:3]  #지역을 선택

#실행결과
#array([[ 6,  7],
#       [10, 11]])
    
    
    
a[1:3, 1:3] +=10 # 변경
a

#실행결과 
#array([[ 1,  2,  3,  4],
#       [ 5, 16, 17,  8],
#       [ 9, 20, 21, 12]])
 
    
#조건이 있는 할당
np.where(a<10, a,10)
#실행결과
array([[ 1,  2,  3,  4],
       [ 5, 10, 10,  8],
       [ 9, 10, 10, 10]])np.where(a<10)   
    

    
            #3.10 행렬과 선형대수계산

#문제 행렬곱셈, 행렬식 찾기, 선형 방정식 풀기 

import numpy as np
m=np.matrix([[1,-2,3],[0,4,5],[7,8,-9]])
m
#실행결과 
matrix([[ 1, -2,  3],
        [ 0,  4,  5],
        [ 7,  8, -9]])
    
#전치행렬
m.T
#실행결과 
matrix([[ 1,  0,  7],
        [-2,  4,  8],
        [ 3,  5, -9]])

#역행렬
m.I
#실행결과 
matrix([[ 0.33043478, -0.02608696,  0.09565217],
        [-0.15217391,  0.13043478,  0.02173913],
        [ 0.12173913,  0.09565217, -0.0173913 ]])
    
#벡터를 만들고 곱하기
v= np.matrix([[2],[3],[4]])
v
#실행결과 
matrix([[2],
        [3],
        [4]])
    
m*v
#실행결과
matrix([[ 8],
        [32],
        [ 2]])
    
    #예제 numpy.linalg 서브패키지
    
import numpy.linalg

numpy.linalg.det(m)
#실행결과 -229.99999999999983

numpy.linalg.eigvals(m)
#실행결과 array([-13.11474312,   2.75956154,   6.35518158])

x=numpy.linalg.solve(m,v)
x

#실행결과 
matrix([[ 0.96521739],
        [ 0.17391304],
        [ 0.46086957]])
    
m*x
#실행결과 
matrix([[ 2.],
        [ 3.],
        [ 4.]])
    
v
#실행결과 
matrix([[2],
        [3],
        [4]])