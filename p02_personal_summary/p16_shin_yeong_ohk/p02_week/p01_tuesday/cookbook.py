5월23일
===============================================================================
# 2.17 HTML과 XML 엔티티 처리
# &entity; 나 &code; 와 같은 HTML, XML 엔티티를 이에 일치하는 문자로 치환하기
# 텍스트 생성할 때 특정 문자 (>, < ,& 등) 피하고 싶을 때,
# "excape() 함수"

EX1>
s = 'Elements are written as "<tag>text</tag>".'
import html
print(s)
#Elements are written as "<tag>text</tag>".

print(html.escape(s))
#Elements are written as &quot;&lt;tag&gt;text&lt;/tag&gt;&quot;.

#따옴표는 남겨두도록 지정
print(html.escape(s, quote=False))
#Elements are written as "&lt;tag&gt;text&lt;/tag&gt;".



EX2>
#텍스트를 아스키 문자로 만들고 캐릭터 코드를 아스키가 아닌 문자에 끼워 넣고 싶으면
#errors = 'xmlcharrefreplace'인자를 입출력 관련 함수에 사용

s = 'Spicy Jalapeño'
s.encode('ascii', errors='xmlcharrefreplace')
#b'Spicy Jalape&#241;o'



EX3>
#텍스트의 엔티티를 치환하면 또 다른 처리를 해야한다. 실제로 HTML, XML을 처리할
#예정이면 먼저 올바른 HTML, XML 파서 사용
#일반적으로 이런 도구는 파싱하는 동안 자동으로 값 치환
## 수동으로 치환해야 한다면,
## HTML, XML 파서에 내장되어 있는 여러 유틸리티 함수나 메소드 사용

s = 'Spicy &quot;Jalape&#241;o&quot.'
from html.parser import HTMLParser
p = HTMLParser()
p.unescape(s)
#'Spicy "Jalapeño".'

t = 'The prompt is &gt;&gt;&gt;'
from xml.sax.saxutils import unescape
unescape(t)
#'The prompt is >>>'
===============================================================================







===============================================================================
# 2.18 텍스트 토큰화
# 문자열을 파싱해서 토큰화하기

#토큰화1_문자열을 트큰화하려면 패턴을 확인할 방법을 가지고 있어야 한다.
#예를 들어, 문자열을 다음과 같은 페어 시퀀스로 바꾸고 싶다면,
foo = 'foo = 23 + 42 * 10'

tokens = [('NAME', 'foo'), ('EQ','='), ('NUM', '23'), ('PLUS','+'),('NUM', '42'),
          ('TIMES', '*'), ('NUM', '10')]
#이런 나누기 작업을 하기 위해서는 공백을 포함해서 가능한 모든 토큰을 정의해야 한다.



EX1>
#이름있는 캡처 그룹을 사용하는 정규 표현식 사용
import re
NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))
#re 패턴에서, 패턴에 이름을 붙이기 위해 ?P<TOKENNAME>을 사용


#토큰화2_패턴 객체의 잘 알려지지 않은 scanner() 메소드 사용
#스캐너 객체를 생성하고 전달 받은 텍스트에 match()를 반복적으로 하나씩 호출

scanner = master_pat.scanner('foo = 42')
scanner.match()
#<_sre.SRE_Match object; span=(0, 3), match='foo'>

_.lastgroup, _.group()
#('NAME', 'foo')

scanner.match()
#<_sre.SRE_Match object; span=(3, 4), match=' '>

_.lastgroup, _.group()
#('WS', ' ')

scanner.match()
#<_sre.SRE_Match object; span=(4, 5), match='='>


_.lastgroup, _.group()
#('EQ', '=')

scanner.match()
#<_sre.SRE_Match object; span=(5, 6), match=' '>


_.lastgroup, _.group()
#('WS', ' ')
scanner.match()
#<_sre.SRE_Match object; span=(6, 8), match='42'>

_.lastgroup, _.group()
#('NUM', '42')

scanner.match()

#사용 코드
from collections import namedtuple
Token = namedtuple('Token', ['type','value'])
def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())

for tok in generate_tokens(master_pat, 'foo = 42'):
    print(tok)
    
#Token(type='NAME', value='foo')
#Token(type='WS', value=' ')
#Token(type='EQ', value='=')
#Token(type='WS', value=' ')
#Token(type='NUM', value='42')


EX2>
#토큰 스트림을 걸러 내고 싶으면 생성자 함수를 더 많이 정의하거나
#생성자 표션식을 사용한다


#복잡한 텍스트 파싱이나 처리르 하기 전에 토큰화
# 1)입력부에 나타나는 모든 텍스트 시퀀스를 RE 패턴으로 환인해야 한다.
# 2)매칭하지 않는 텍스트가 하나라도 있으면 스캐닝이 멈춘다.
# 3)매칭할 때 re는 며이한 순서대로 패턴을 매칭한다.
    #->(한 패턴이 다른 패턴의 부분이 되는 경우가 있다면 더 긴 패턴 먼저 넣기)

LT = r'(?P<LT><)'
LE = r'(?P<LE><=)'
EQ = r'(?P<EQ>=)'

master_pat = re.compile('|'.join([LE, LT, EQ])) # 맞음
# master_pat = re.compile('|'.join([LT, LE, EQ])) # 틀림

    
                         
EX3>
#주의!_패턴이 부분 문자열을 형성하는 경우
PRINT = r'(P<PRINT>print)'
NAME = r'(P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
master_pat = re.compile('|'.join([PRINT, NAME]))
for tok in generate_tokens(master_pat, 'printer'):
    print(tok)
## 출력 X??????
===============================================================================





===============================================================================
# 2.19 간단한 재귀 파서 작성
# 주어진 문법 규칙에 따라 텍스트를 파싱하고 동작을 수행하거나 입력된 텍스트를
# 추상 신택스 트리로 나타내야 한다.
# 문법은 간단하지만 프레임워크를 사용ㅎ지 않고 파서를 직접 하용하기!

EX1> BNF
expr ::= expr + term
| expr - term
| term
term ::= term * factor
| term / factor
| factor
factor ::= ( expr )
| NUM
#왼쪽의 심볼이 오른쪽에 있는 심볼로 치환(혹은 반대)
#일반적으로 입력받은 텍스트를 BNF를 사용해 여러가지 치환과 확장을 해서 문법에
#매칭하는 과정이 파싱에서 일어난다.


EX1_1>
expr ::= term { (+|-) term }*
term ::= factor { (*|/) factor }*
factor ::= ( expr )
| NUM
#{......}* = 선택할 수 있는 부분


 
EX2> 3 + 4 * 5 파싱
#1) 토큰화
NUM + NUM * NUM

#2) 치환을 통해 입력 토큰을 문법에 매칭
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

#첫번째 입력 토큰 = NUM
# 첫번째 치환은 매칭에 집중
# 매칭이 일어나고 나면 초점은 다음 토큰인 _로 넘어가고... 반복
# 특정 부분의 오른쪽 (EX. {(*/) factor*} 은 다음 토늠에 매칭할 수 없다고
# 판단됨녀 사라지기도 한다.
# 파싱에 성공하면 입력 토큰 스트림에 매칭하기 위해 오른쪽 부분이 모두 확장됨.



EX3> 재귀 표현식 해석기
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
Token = collections.namedtuple('Token', ['type','value'])
def generate_tokens(text):
    scanner = master_pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok

#파서
class ExpressionEvaluator:
    '''
    재귀 파서 구현, 모든 메소드는 하나의 문법 규칙을 구현한다.
    현재 룩어헤드 토큰을 받고 테스트하는 용도로 ._accept()를 사용한다.
    입력 받은 내역에 완벽히 매칭하고 다음 토큰을 무시할 때는
    ._expect()를 사용한다(혹시 매칭하지 않는 경우에는 SyntaxError를 발생한다).
    '''

def parse(self,text):
    self.tokens = generate_tokens(text)
    self.tok = None    #마지막 심볼 소비
    self.nexttok = None    #다음 심볼 토큰화
    self._advance()    #처음 룩어헤드 토큰 불러오기
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
        

#ExpressionEvaluator() 클래스 사용
e = ExpressionEvaluator()
e.parse('2')
#'ExpressionEvaluator' object has no attribute 'parse'?????

e.parse('2 + 3')
#'ExpressionEvaluator' object has no attribute 'parse'???????

e.parse('2 + 3 * 4')
##'ExpressionEvaluator' object has no attribute 'parse'???????

e.parse('2 + (3 + 4) * 5')
##'ExpressionEvaluator' object has no attribute 'parse'???????

e.parse('2 + (3 + * 4)')
#'ExpressionEvaluator' object has no attribute 'parse'???????



EX4> 간단한 파싱 트리 구현식
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
e.parse('2 + 3')
#'ExpressionTreeBuilder' object has no attribute 'parse'...

e.parse('2 + 3 * 4')
#'ExpressionTreeBuilder' object has no attribute 'parse'

e.parse('2 + (3 + 4) * 5')
#'ExpressionTreeBuilder' object has no attribute 'parse'

e.parse('2 + 3 + 4')
#'ExpressionTreeBuilder' object has no attribute 'parse'


##재귀 판서 만드는 방법
expr ::= term { ('+'|'-') term }*
term ::= factor { ('*'|'/') factor }*
factor ::= '(' expr ')'
| NUM

#메소드로 변형
class ExpressionEvaluator:
    ...
    def expr(self):
        ...
    def term(self):
        ...
    def factor(self):
        ...

##각 메소드가 하는 일
## 문법 규칙을 왼쪽 -> 오른쪽으로 살펴보면서 절차에 따라 토큰 소비
## 메소드의 목적은 규칙을 소비하거나 막혔을 경우 구문 에러 발생하기

###만약 규칙의 다음 심복이 다른 규칙의 이름이라면(EX. term, factor),
### 동일한 이름의 메소드 호출
### "내려오는 부분"
### 이미 실행 중인 메소드에 대한 호출을 포함하는 규칙
### (factor ::='('expr')' 규칙에서 expr 호출)
### = "재귀"

###만약 규칙의 다음 심볼이 특정 심볼(EX. ()가 되어야 한다면, 다음 토큰을 보고
### 정확한 매칭을 확인한다.
### 일치하지 않으면 구문 에러
### =_expect() 메소드

### 만약 규칙의 다음 심볼이 될 수 있는 후보가 적다면(EX. + or -), 다음 토큰을
### 보고 매칭이 이루어졌는지 확인
### =_accept() 메소드
### _except() 메소드와 다른점;
### 일치하는 것이 없을 때 에러를 발생하지 않고 뒤로 간다.
### (그래야 그 이후를 확인하는 작업 가능)

### 문법에 반복되는 부분이 있으면(EX. expr ::= term { ('+'|'-') term}*),
### 반복부는 while 문으로 구현
### 반복문의 몸통에서 더이상 일치하는 아이템이 없을 때까지 수집/진행

###모든 문법 규칙을 소비하고 나면 각 메소드는 호출ㄹ자에게 결과를 반환.
###이 과정을 통해 파싱이 진행되는 동안 값 전달
### EX. 표현식 해석기에서 반환하는 값은 파싱한 표현식의 부분 결과
### 가장 상위 문법 규칙 메소드에서 모두 합친다.



EX5>
#재귀 파서의 한 가지 제약으로 죄측 재귀가 포함된 어떠한 문법 규칙에 대해서도 사용X
items ::= items ',' item
| item

def items(self):
    itemsval = self.items()
    if itemsval and self._accept(','):
        itemsval.append(self.item())
    else:
        itemsval = [ self.item() ]

#>> 작동X = 무한 재귀 에러



EX6> PyParsing / PLY 을 이용한 파싱
from ply.lex import lex
from ply.yacc import yacc

#토큰 리스트
tokens = [ 'NUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN' ]

#무시 문자
t_ignore = ' \t\n'

#토큰 스펙(정규 표현식)
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

#토큰화 함수
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

#에러 핸들러
def t_error(t):
    print('Bad character: {!r}'.format(t.value[0]))
    t.skip(1)

#렉서(lexer) 만들기
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
    2.19
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

parser.parse('2')
#<module '__main__'> is a built-in module....

parser.parse('2+3')
# <module '__main__'> is a built-in modul...

parser.parse('2+(3+4)*5')
# <module '__main__'> is a built-in modul...

>>>
## 토큰화 정규 표현식과 여러 문법 규칙을 매칭할 때 사용할 상위 레벨 핸들링 함수!!
===============================================================================







===============================================================================
#2.20 바이트 문자열에 텍스트 연산 수행
#바이트 문자열에 일반적인 텍스트 연산(잘라내기, 검색, 치환 등)을 수행하기

EX1>
#내장된 바이트 문자열 연산
data = b'Hello World'
data[0:5]
#b'Hello'

data.startswith(b'Hello')
#True

data.split()
#[b'Hello', b'World']

data.replace(b'Hello', b'Hello Cruel')
#b'Hello Cruel World'



EX2>
#바이트 배열
data = bytearray(b'Hello World')
data[0:5]
#bytearray(b'Hello')

data.startswith(b'Hello')
#True

data.split()
#[bytearray(b'Hello'), bytearray(b'World')]

data.replace(b'Hello', b'Hello Cruel')
#bytearray(b'Hello Cruel World')



EX3>
#바이트 문자열 패턴 매칭에 정규 표현식 적용 가능
#하지만 패턴 자체도 바이트로 나타내야 한다.
data = b'FOO:BAR,SPAM'
import re
re.split('[:,]',data)
#Traceback (most recent call last):

#  File "<ipython-input-51-c9e01cc3a1ad>", line 3, in <module>
#    re.split('[:,]',data)

#  File "C:\Users\ATIV BOOK 9\Anaconda3\lib\re.py", line 212, in split
#    return _compile(pattern, flags).split(string, maxsplit)

#TypeError: cannot use a string pattern on a bytes-like object

re.split(b'[:,]',data)    #주의 : 패턴도 바이트로 나타냄
#[b'FOO', b'BAR', b'SPAM']



EX4>
### 주의!
#1)바이트 문자열에 인덱스를 사용하면 개변 문자가 아니라 정수
a = 'Hello World'    #텍스트 문자열
#'H'
a[1]
#'e'

b = b'Hello World'    #바이트 문자열
b[0]
#72
b[1]
#101

#2)바이트 문자열은 표현식과 출력이 가독성이 떨어진다.
## 텍스트 문자열로 변환하면 깔끔하게 출력 가능
s = b'Hello World'
print(s)
#b'Hello World'     #b'...' 형식으로 출력

print(s.decode('ascii'))
#Hello World

##바이트 문자열은 서식화 지원X
b'%10s %10d %10.2f' % (b'ACME', 100, 490.1)
#b'      ACME        100     490.10' ?????

b'{} {} {}'.format(b'ACME', 100, 490.1)
#Traceback (most recent call last):

#  File "<ipython-input-62-0442c2c2ecdc>", line 1, in <module>
#    b'{} {} {}'.format(b'ACME', 100, 490.1)

#AttributeError: 'bytes' object has no attribute 'format'

##바이트 문자열에 서식화를 적용하고 싶으면 일반 텍스트 문자열과 인코딩 사용
'{:10s} {:10d} {:10.2f}'.format('ACME', 100, 490.1).encode('ascii')
#b'ACME              100     490.10'

#3)바이트 문자열을 사용함녀 특정 연산의 문법에 영향을 주기도 한다.
#특히 파일 시스템에 영향이 많다.
#EX.파일 이름을 텍스트 문자열이 아니라 바이트 문자열로 제공하면,
#대개 파일 이름 인코딩/디코딩을 사용할 수 X

#UTF-8 파일 이름 작성
with open('jalape\xf1o.txt', 'w') as f:
    f.write('spicy')

# 디렉토리 리스트 구하기
import os
os.listdir('.')     #텍스틑 문자열(이름이 디코딩된다.)
#['.anaconda',
# '.astropy'...???

os.listdir(b'.')    #바이트 문자열 (이름이 바이트로 남는다,)
#[b'.anaconda',
# b'.astropy', ...??
===============================================================================







#Chapter3_숫자, 날짜, 시간
===============================================================================
#3.1 반올림
#부동 소수점 값을 10진수로 반올림하기
#"round(value,ndigits)

EX1>
round(1.23,1)
#1.2
round(-1.27,1)
#-1.3
round(1.25361,3)
#1.254
## 값이 두 선택지의 가운데 있으면 더 가까운 짝수가 된다.
## 1.5 / 2.5 의 반올림 = 2



EX2>
a = 1627731
round(a, -1)
#1627730
round(a,-2)
#1627700
round(a,-3)
#1628000



EX3>
#반올림과 서식화
#특정 자릿수까지 숫자를 표현하려면 round()X -> 서식화를 위한 자릿수 명시
x = 1.23456
format(x, '0.2f')
#'1.23'
format(x, '0.3f')
#'1.235'
'value is {:0.3f}'.format(x)
#'value is 1.235'
===============================================================================





===============================================================================
#3.2 정확한 10진수 계산
#정확한 10진수 계산, 부동 소수점을 사용할 때 발생하는 작은 오류 피하기
## 부동 소수점 값은 10진수를 아주 정확히 표현하지 못한다.

EX1>
a = 4.2
b = 2.1
a + b
#6.300000000000001
(a + b) == 6.3
#False



##"decimal 모듈"
EX2>
from decimal import Decimal
a = Decimal('4.2')
b = Decimal('2.1')
a + b
#Decimal('6.3')
print(a + b)
#6.3
(a + b) == Decimal('6.3')
#True



EX3>
#반올림의 자릿수 조절 가능
from decimal import localcontext
a = Decimal('1.3')
b = Decimal('1.7')
print(a/b)
#0.7647058823529411764705882353

with localcontext() as ctx:
    ctx.prec = 3
    print(a / b)
#0.765

with localcontext() as ctx:
    ctx.prec = 50
    print(a / b)
#0.76470588235294117647058823529411764705882352941176
===============================================================================






===============================================================================
#3.3 출력을 위한 숫자 서식화
#출력을 위해 자릿수, 정렬, 천 단위 구분 등 숫자를 서식화할 때,
#"format()" 함수

EX1>
x = 1234.56789

# 소수점 둘째 자리 정확도
format(x, '0.2f')
#'1234.57'

# 소수점 한자리 정확도로 문자 10개 기준 오른쪽에서 정렬
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
# '1,234.56789'

format(x, '0,.1f')
#'1,234.6'


#지수표현법
format(x,'e')
#'1.234568e+03'

format(x,'0.2E')
#'1.23E+03'
===============================================================================





===============================================================================
#3.4 2진수, 8진수, 16진수 작업

EX1>
# bin(), oct(), hex()
x = 1234
bin(x)
#'0b10011010010'
oct(x)
#'0o2322'
hex(x)
#'0x4d2'



EX2>
#format()함수
format(x,'b')
#'10011010010'
format(x,'o')
#'2322'
format(x,'x')
#'4d2'



EX3>
#음수 -> 출력 음수로
x=-1234
format(x,'b')
#'-10011010010'
format(x,'x')
#'-4d2'



EX4>
#부호가 없는 값 사용하기 위해서 = 최대값(maximum)을 더해서 비트 길이 선정
x = -1234
format(2**32 + x, 'b')
#'11111111111111111111101100101110'

format(2**32+x,'x')
#'fffffb2e'



EX4_1>
#다른 진법의 숫자를 정수형으로 변환하려면 INT()함수에 적잘한 진수 전달
int('4d2',16)
#1234
int('10011010010',2)
#1234



EX5>
#8진법 사용시 주의
import os
os.chmod('script.py', 0755)
#File "<ipython-input-42-f4751dc2ca20>", line 2
 #   os.chmod('script.py', 0755)
 #                            ^
#SyntaxError: invalid token

#8진법 앞에는 0o붙이기
os.chomd('script.py',0o755)
===============================================================================






===============================================================================
#3.9 큰 배열 계산
#배열이나 그리드(grid)와 같이 커다란 숫자 데이터세트에 계산
#'numpy"라이브러리

EX1>
#파이썬 리스트
x = [1, 2, 3, 4]
y = [5, 6, 7, 8]
x * 2
#[1, 2, 3, 4, 1, 2, 3, 4]
x + 10
#Traceback (most recent call last):

#  File "<ipython-input-45-f51880e8756d>", line 1, in <module>
 #   x + 10

#TypeError: can only concatenate list (not "int") to list

x + y
#[1, 2, 3, 4, 5, 6, 7, 8]


EX1_1>
#Numpy 배열
import numpy as np
ax = np.array([1, 2, 3, 4])
ay = np.array([5, 6, 7, 8])
ax * 2
#array([2, 4, 6, 8])
ax + 10
#array([11, 12, 13, 14])
ax + ay
#array([ 6,  8, 10, 12])
ax * ay
#array([ 5, 12, 21, 32])

##스칼라 연산(ax * 2 또는 ax + 10)이 요소 기반으로 적용
## 배열과 배열 간 계산을 하면 연산자가 모든 요소에 적용되고 새로운 배열 새엇ㅇ

#다항식 계산
EX2>
def f(x):
    return 3*x**2 - 2*x + 7
f(ax)
#array([ 8, 15, 28, 47])



EX3>
#Numpy는 배열에 사용 가능한 "일반 함수"를 제공한다.
np.sqrt(ax)
# array([ 1.        ,  1.41421356,  1.73205081,  2.        ])
np.cos(ax)
#array([ 0.54030231, -0.41614684, -0.9899925 , -0.65364362])



##numpy는 동일한 데이터 타입을 메모리에 연속으로 나열한다.
EX4> 10,000 x 10,000 2차원 그리드
grid=np.zeros(shape=(10000,10000),dtype=float)
grid
#array([[ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       ..., 
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.]])


## 모든 연산은 모든 요소에 동신 적용
grid=np.zeros(shape=(10000,10000),dtype=float)
grid += 10
grid
#array([[ 10.,  10.,  10., ...,  10.,  10.,  10.],
#       [ 10.,  10.,  10., ...,  10.,  10.,  10.],
#       [ 10.,  10.,  10., ...,  10.,  10.,  10.],
#       ..., 
#       [ 10.,  10.,  10., ...,  10.,  10.,  10.],
#       [ 10.,  10.,  10., ...,  10.,  10.,  10.],
#       [ 10.,  10.,  10., ...,  10.,  10.,  10.]])

grid=np.zeros(shape=(10000,10000),dtype=float)
np.sin(grid)
#?????
#array([[ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       ..., 
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.],
#       [ 0.,  0.,  0., ...,  0.,  0.,  0.]])
    
    
    
EX5>numpy가 파이썬의 리스트, 그 중에서도 다차원 배열의 인덱싱 기능을 확장한다.
a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
a
#array([[ 1,  2,  3,  4],
#       [ 5,  6,  7,  8],
#       [ 9, 10, 11, 12]])

#첫번째 행 선택    
a[1]
#array([5, 6, 7, 8])

#첫번째 열 선택
a[:,1]
array([ 2, 6, 10])

#지역을 선택 후 변경
a[1:3, 1:3]
#array([[ 6,  7],
#       [10, 11]]) 

a[1:3, 1:3] += 10
a
#array([[ 1,  2,  3,  4],
#       [ 5, 16, 17,  8],
#       [ 9, 20, 21, 12]])
    
#행 벡터를 모든 행 연산에 적용
a + [100, 101, 102, 103]
#array([[101, 103, 105, 107],
#       [105, 117, 119, 111],
#       [109, 121, 123, 115]])

a
#array([[ 1,  2,  3,  4],
#       [ 5, 16, 17,  8],
#       [ 9, 20, 21, 12]])
    
#조건이 있는 할당
np.where(a < 10, a, 10)
#array([[ 1,  2,  3,  4],
#       [ 5, 10, 10,  8],
#       [ 9, 10, 10, 10]])
===============================================================================
    
    

    
    
    
===============================================================================
#3.10 행렬과 선형 대수 계산
#행렬 곱셈, 행렬식 찾기, 선형 방적식 풀기 등 행렬이나 선형 대수 계산하기
#nnumpy 라이브러리 > "matrix 객체" = 선형 대수 계산법
import numpy as np
m = np.matrix([[1,-2,3],[0,4,5],[7,8,-9]])
m
#matrix([[ 1, -2,  3],
#        [ 0,  4,  5],
#        [ 7,  8, -9]])

# 전치 행렬
m.T
#matrix([[ 1,  0,  7],
#        [-2,  4,  8],
#        [ 3,  5, -9]])

# 역행렬
m.I
#matrix([[ 0.33043478, -0.02608696,  0.09565217],
#        [-0.15217391,  0.13043478,  0.02173913],
#        [ 0.12173913,  0.09565217, -0.0173913 ]])
    
#벡터를 만들고 곱하기
v = np.matrix([[2],[3],[4]])
v
#matrix([[2],
#        [3],
#        [4]])
    
m*v
#matrix([[ 8],
#        [32],
#        [ 2]])
===============================================================================