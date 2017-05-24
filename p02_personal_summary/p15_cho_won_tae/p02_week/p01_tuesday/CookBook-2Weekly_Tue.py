# 2.17 HTML과 XML 엔티티 처리!
# 문제
# &entity; 나 &#code;와 같은 HTML, XML 엔티티를 이에 일치하는 문자로 치환하고 싶다
# 혹은 텍스트를 생성할 때 특정문자(<,>,& 등)를 피하고 싶다
# 해결
# 텍스트를 생성할 때 <나> 와 같은 특수 문자를 치환하는 것은 html.escape() 함수를 사용하면 상대적으로 간단히 처리가능!
s = 'Elements are written as "<tag>text</tag>".'
import html
print(s) # Elements are written as "<tag>text</tag>" 출력
print(html.escape(s)) # Elements are written as &quot;&lt;tag&gt;text&lt;/tag&gt;&quot; 출력
# 따옴표는 남겨 두도록 지정
print(html.escape(s,quote=False)) # Elements are written as "&lt;tag&gt;text&lt;/tag&gt;" 출력
# 텍스트를 아스키코드로 만들고 캐릭터 코드를 아스키가 아닌 문자에 끼워 넣고 싶으면
# errors='xmlcharrefreplace' 인자를 입출력 관련 함수에 사용한다
s = 'Spicy Jalapeno'
a = s.encode('ascii',errors='xmlcharrefreplace')
print(a) # b'Spicy Jalapeno' 출력
# 텍스트의 엔티티를 치환하면 또 다른 처리를 해야 한다.
# 실제로 HTML,XML을 처리할 예정이면 우선 올바른 HTML,XML 파서를 사용해야 한다
# 일반적으로 이런 도구는 파싱하는 동안 자동으로 값을 치환해 준다
# 하지만 어째서인지 자동으로 처리되지 않았고 수동으로 치환을 해야한다면 HTML,XML파서에 내장되어 있는 여러 유틸리티 함수나 메소드를 사용
s = 'Spicy &quot;Jalape&#241;o&quot.'
from html.parser import HTMLParser
p = HTMLParser()
a = p.unescape(s)
print(a) # Spicy "Jalapeño" 출력
# 토론
# HTML, XML을 생성할 때 특수문자를 제대로 이스케이핑 하는 과정을 간과하기 쉽다.
# print()로 결과물을 생성하거나 기본적인 문자열 서식 기능을 사용할 때 특히 더 그렇다
# 가장 쉬운 해결책은 html.escape()와 같은 유틸리티 함수를 사용하는 것이다

# 2.18 텍스트 토큰화
# 문제
# 문자열을 파싱해서 토큰화하고 싶다
# 해결
# 다음과 같은 문자열이 있다
text = 'foo = 23+42*10'
# 문자열을 토큰화하려면 패턴 매칭 이상의 작업이 필요하다
# 패털을 확인할 방법을 가지고 있어야 한다
# 예를 들어, 문자열을 다음과 같은 페어 시퀀스로 바꾸고 싶다
tokens=[('NAME','foo'),('EQ','='),('NUM','23'),('PLUS','+'),('NUM','42'),('TIMES','*'),('NUM','10')]
# 이런 나누기 작업을 하기 위해서는 공백을 포함해서 가능한 모든 토큰을 정의해야 한다
# 다음 코드에서는 이름 있는 캡처 그룹을 사용하는 정규 표현식을 사용한다
import re
NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'
master_pat = re.compile('|'.join([NAME,NUM,PLUS,TIMES,EQ,WS]))
# re 패턴에서, 패턴에 이름을 붙이기 위해 ?P<TOKENNAME>을 사용하고 있다.
# 다음으로 토큰화를 위해서 패턴 객체의 잘 알려지지 않은 scanner() 메소드를 사용한다
# 이 메소드는 스캐너 객체를 생성하고 전달 받은 텍스트에 match() 를 반복적으로 하나씩 호출한다
# 스캐너 객체가 동작하는 모습을 다음 예제를 통해 살펴본다
# 예제1)
scanner = master_pat.scanner('foo = 42')
a = scanner.match()
print(a)
# 토론
# 보통 더 복잡한 텍스트 파싱이나 처리를 하기 전에 토큰화를 한다.
# 앞에서 나온 스캔 기술을 사용하려면 다음 몇가지 중요한 사항을 기억하자
# 우선 입력부에 나타나는 모든 텍스트 시퀀스를 re 패턴으로 확인해야 한다
# 매칭하지 않는 텍스트가 하나라도 있으면 스캐닝이 거기서 멈춘다
# 마스터 정규 표현식의 토큰 순서도 중요하다
# 매칭할 때 re는 명시한 순서대로 패턴을 매칭한다
# 따라서 한 패턴이 다른 패턴의 부분이 되는 경우가 있다면 항상 더 긴 패턴을 먼저 넣어야 한다

# 2.19 간단한 재귀 파서 작성
# 문제
# 주어진 문법 규칙에 따라 텍스트를 파싱하고 동작을 수행하거나 입력된 텍스트를 추상 신택스 트리로 나타내야 한다
# 문법은 간단하지만 프레임워크를 사용하지 않고 파서를 직접 작성하고 싶다
# 해결
# 이 문제는 특정 문법에 따라 텍스트를 파싱하는데 집중한다.
# 우선 문법의 정규 스펙을 BNF나 EBNF로 하는데서 시작한다.
# 예를 들어 산술표현식을 다음과 같이 나타낼 수 있다
expr ::= expr + term
        | expr = term
        | term
term ::= term * factor | term / factor | factor
factor ::= (expr) | NUM
# 혹은 EBNF 형식으로 나타낸다
expr ::= term { (+|-) term}*
term ::= factor { (*|/) factor}*
factor ::= (expr) | NUM
# EBNF에서 { ... }* 로 감싸는 부분은 선택할 수 있는 부분이다.
# * 부호는 하나도 없거나 여러번 반복됨을 의미한다
# BNF가 익숙하지 않다면, 왼쪽에 있는 심볼이 오른쪽에 있는 심볼로 치환될 수 있는 규약 정도로 생각하자
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
e = ExpressionEvaluator()
print(e.parse('2')) # 2 출력
print(e.parse('2 + 3')) # 5 출력
print(e.parse('2 + 3 * 4')) # 14 출력
print(e.parse('2 + (3 + 4) * 5')) # 35 출력
print(e.parse('2 + (3 + * 4)'))
# Traceback (most recent call last):
#     File "<stdin>", line 1, in <module>
#     File "exprparse.py", line 40, in parse
#     return self.expr()
#     File "exprparse.py", line 67, in expr
#     right = self.term()
#     File "exprparse.py", line 77, in term
#     termval = self.factor()
#     File "exprparse.py", line 93, in factor
#     exprval = self.expr()
#     File "exprparse.py", line 67, in expr
#     right = self.term()
#     File "exprparse.py", line 77, in term
#     termval = self.factor()
#     File "exprparse.py", line 97, in factor
#     raise SyntaxError("Expected NUMBER or LPAREN")
#     SyntaxError: Expected NUMBER or LPAREN 출력
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

# 2.20 바이트 문자열에 텍스트 연산 수행
# 문제
# 바이트 문자열(byte string)에 일반적인 텍스트 연산(잘라내기, 검색, 치환 등)을 수행하고 싶다
# 해결
# 바이트 문자열도 텍스트 문자열과 마찬가지로 대부분의 연산을 내장하고 있다
data = b'Hello World'
print(data[0:5]) # b'Hello' 출력
a = data.startswith(b'Hello')
print(a) # True 출력
a = data.split()
print(a) # [b'Hello', b'World'] 출력
a = data.replace(b'Hello',b'Hello Cruel')
print(a) # b'Hello Cruel World' 출력
# 이런 동작은 바이트 배열에도 사용할 수 있다
data = bytearray(b'Hello World')
print(data[0:5]) # bytearray(b'Hello') 출력
a = data.startswith(b'Hello')
print(a) # True 출력
a = data.split()
print(a) # [bytearray(b'Hello'), bytearray(b'World')] 출력
# 바이트 문자열 패턴 매칭에 정규 표현식을 적용할 수 있다
# 하지만 패턴 자체도 바이트로 나타내야 한다
data = b'FOO:BAR,SPAM'
import re
# a = re.split('[:,]',data)
# print(a)
# Traceback (most recent call last):
#   File "C:/Users/Won Tae CHO/PycharmProjects/Source/CookBook-Master/CookBook-2Weekly_Tue.py", line 285, in <module>
#     a = re.split('[:,]',data)
#   File "C:\Users\Won Tae CHO\AppData\Local\Programs\Python\Python35\lib\re.py", line 203, in split
#     return _compile(pattern, flags).split(string, maxsplit)
# TypeError: cannot use a string pattern on a bytes-like object 출력
a = re.split(b'[:,]',data)
print(a) # [b'FOO', b'BAR', b'SPAM'] 출력
# 토론
# 대개의 경우 텍스트 문자열에 있는 연산 기능은 바이트 문자열에도 내장되어 있다.
# 하지만 주의해야 할 차이점이 몇 가지 있다 1. 바이트 문자열에 인덱스를 사용하면 개별문자가 아니라 정수를 가리킨다
a = 'Hello World'
print(a[0]) # H 출력
print(a[1]) # e 출력
b = b'Hello World'
print(b[0]) # 72 출력
print(b[1]) # 101 출력
# 이 차이로 인해 캐릭터 기반의 데이터를 바이트 기준으로 접근하는 프로그램에 영향을 주기도 한다
# 2. 바이트 문자열은 보기 좋은 표현식을 지원하지 않고 텍스트 문자열로 변환하지 않으면 깔끔히 출력할 수 없다
s = b'Hello World'
print(s) # b'Hello World' 출력
print(s.decode('ascii')) # Hello World 출력
# 또한 바이트 문자열은 서식화를 지원하지 않는다
a = b'%10s %10d %10.2f' %(b'ACME',100,490.1)
print(a)

# CHAPTER3 - 숫자,날짜,시간
# 파이썬에서 정수와 소수점을 써서 수학적으로 계산하기는 어렵지 않다.
# 하지만 분수,배열,날짜,시간 계싼은 조금 복잡하다. 그러기에 이러한 복잡한 계산에 대해 알아보자!
# 3.1 반올림
# 문제
# 부동 소수점 값을 10진수로 반올림하고 싶다
# 해결
# 간단한 반올림은 내장 함수인 round 함수를 사용한다
print(round(1.23,1)) # 1.2 출력
print(round(1.26,1)) # 1.3 출력
print(round(-1.27,1)) # -1.3 출력
print(round(1.25361,3)) # 1.254 출력
# 값이 정확히 두 선택지의 가운데 있으면 더 가까운 짝수가 된다.
# 예를 들어 1.5와 2.5는 모두 2가 된다
# round()에 전달하는 자릿수는 음수가 될 수 있다.
# 이 경우에는 10의자리, 100의 자리 등의 순으로 자릿수가 결정된다
a = 1627731
print(round(a,-1)) # 1627730 출력
print(round(a,-2)) # 1627700 출력
print(round(a,-3)) # 1627800 출력
# 토론
# 반올림과 서식화를 헷갈리지 않도록 주의하자
# 특정 자릿수까지 숫자를 표현하는 것이 목적이라면 round()를 사용하는 것이 아니라 서식화를 위한 자릿수를 명시하기만 하면 된다
x = 1.23456
print(format(x,'.2f')) # 1.23 출력
print(format(x,'.3f')) # 1.235 출력(반올림해줌)
a = 'value is {:.3f}'.format(x)
print(a) # value is 1.235 출력
# 또한 정확도 문제를 수정하려고 부동 소수점을 반올림하는 방법도 지양해야 한다
# 예를 들어 다음과 같은 코드를 사용하고 싶을지 모른다
a = 2.1
b = 4.2
c = a + b
print(c) # 6.300000000000001 출력
c = round(c,2)
print(c) # 6.3 출력

# 3.2 정확한 10진수 계산
# 문제
# 정확한 10진수 계싼을 해야 하고, 부동 소수점을 사용할 때 발생하는 작은 오류를 피하고 싶다
# 해결
# 부동 소수점 값에는 10진수를 아주 정확히 표현하지 못한다는 문제가 있다.
# 심지어 아주 작은 계산을 하더라도 오류가 발생하기도 한다
a = 4.2
b = 2.1
c = a+b
print(c) # 6.300000000000001 출력
print(c == 6.3) # False 출력
# 이런 오류는 CPU와 IEEE 754로 부동 소수점 숫자 계싼을 할때 필연적으로 발생한다
# 파이썬의 부동 소수점 값이 바로 이 표현식을 사용하기 떄문에 float를 사용해서는 이 오류를 피할수있는 방법이 없다
# 하지만 더 정확한 계산을 하고 싶다면 decimal 모듈을 사용해야한다
from decimal import Decimal
a = Decimal('4.2')
b = Decimal('2.1')
print(a+b) # 6.3 출력
print(a+b == Decimal('6.3')) # True 출력
# 이처럼 Decimal 객체는 우리가 기대하는 모든 동작을 정확히 수행한다
# 문자열 서식화 함수에 사용하거나 출력하면 마치 일반적인 숫자인 것처럼 보인다
# decimal의 ㅈㅇ요한 기능으로 반올림의 자릿수와 같은 계산적 측면을 조절할 수 있따는 점이 있다
from decimal import Decimal
a = Decimal('1.3')
b = Decimal('1.7')
print(a/b) # 0.7647058823529411764705882353 출력
with localcontext() as ctx:
    ctx.prec = 3
    print(a/b) # localcontext() -> 몇자리수 까지 출력??
               # 0.765 출력
with localcontext() as ctx:
    ctx.prec = 50
    print(a/b) # 0.7647058823529411764705882353.. 출력
# 토론
# decimal 모듈은 IBM의 "General Decimal Arithmetic Specification"을 구현한다
# 파이썬 입문자라면 float의 정확도 문제를 피하기 위해 decimal 모듈을 사용하고 싶어할 것이다
# 그렇다고 개발중인 애플리케이션의 영역을 먼저 생각해보는것이 중요하다
nums = [1.23e+18,1,-1.23e+18]
a = sum(nums)
print(a) # 0.0 출력
# 앞에 나온 예제는 math.fsum()을 사용하면 더 정확한 계산을 할 수 있다
import math
print(math.fsum(nums)) # 1.0 출력
# decimal 모듈을 사용하는 가장 큰 이유는 앞에 설명한 여러 문제를 피하기 위해서이다
# 금융 데이터를 다룰때 많이 사용한다

# 3.3 출력을 위한 숫자 서식화
# 문제
# 출력을 위해 자릿수, 정렬, 천 단위 구분 등 숫자를 서식화하고 싶다
# 해결
# 출력을 위해 숫자를 서식화하려면 내장 함수인 format()을 사용한다
x = 1234.56789
# 소수점 둘째 자리 정확도
a = format(x,'.2f')
print(a) # 1234.57 출력(반올림)
# 소수점 한 자리 정확도로 문자 10개 기준 오른쪽에서 정렬
a = format(x, '>10.1f')
print(a) #     1234.6 출력
# 왼쪽에서 정렬
a = format(x, '<10.1f')
print(a) # 1234.6    출력
# 가운데에서 정렬
a = format(x, '^10.1f')
print(a) #   1234.6   출력
# 천 단위 구분자 넣기
a = format(x,',')
print(a) # 1,234.56789 출력
a = format(x,',.1f')
print(a) # 1,234.6 출력
# 지수 표현법을 사용하려면 f를  e나 E로 바꾸면된다
a = format(x,'e')
print(a) # 1.234568e+03
# 너비와 자릿수를 나타내는 일반적인 형식은 '[<>^]?너비[,]?(.자릿수)?' 이다
# 이때 너비와 자릿수는 정수형으로 표시하고 ?는 선택 사항임을 의미한다
print('The value is {:,.2f}'.format(x)) # The value is 1,234.57 출력
# 토론
# 출력을 위한 숫자 서식화는 대개 간단하다.
# 자릿수를 제한하면 round() 함수와 동일한 규칙으로 반올림된다
# 많은 파이썬 코드에서 숫자를 % 연산자로 서식화한다
a = '%.2f' %x
print(a) # 1234.57 출력
a = '%.10f' %x
print(a) # 1234.5678900000 출력
a = '%10.1f' %x # 10칸짜리에서 오른쪽으로 정렬
print(a) #     1234.6 출력
a = '%-10.1f' %x # 10칸짜리에서 왼쪽으로 정렬
print(a) # 1234.6     출력

# 3.4 2진수, 8진수, 16진수 작업
# 문제
# 숫자를 2진수, 8진수, 16진수로 출력해야 한다
# 해결
# 정수를 2진수, 8진수, 16진수 문자열로 변환하려면 bin(),oct(),hex() 를 사용한다
x = 1234
print(bin(x)) # 0b10011010010 출력
print(oct(x)) # 0o2322 출력
print(hex(x)) # 0x4d2 출력
# 앞에 0b, 0o, 0x가 붙는 것이 싫으면 format()함수를 사용해도 된다
print(format(x,'b')) # 10011010010 출력
print(format(x,'o')) # 2322 출력
print(format(x,'x')) # 4d2 출력
# 부호가 없는 값을 사용하려면 최대값을 더해서 비트 길이를 설정해야 한다
# 예를 들어 32비트 값을 보여주려면 다음과 같이 한다
x = -1234
a = format(2**32 + x,'b')
print(a) # 1111111111111111111101100101110 출력
a = format(2**32 + x,'x')
print(a) # fffffb2e 출력
# 다른 진법의 숫자를 정수형으로 변환하려면 int() 함수에 적절한 진수를 전달한다
a = int('4d2',16)
print(a) # 1234 출력
a = int('10011010010',2)
print(a) # 1234 출력
# 토론
# 2진수, 8진수, 16진수 변환은 대개 간단히 해결할 수 있다.
# 숫자와 문자 표현식 사이의 변환을 위해 이러한 변환법이 존재한다는 점만 기억하면 된다
# 기본적으로는 모두 단일 정수형이다
# 마지막으로 8진법을 사용할 때 프로그래머가 주의해야 할 점이 한가지 있다
# 파이썬이 8진법을 나타내는 방식은 다른 언어와 약간 다르다
# 예를 들어 다음과 같은 코드를 실행하면 구문에러가 발생한다
import os
a = os.chmod('script.py',0755)
print(a)
#     a = os.chmod('script.py',0755)
#                                 ^
# SyntaxError: invalid token 출력

# 즉, 8진법 앞에는 0o를 붙여야 한다
import os
a = os.chmod('script.py',0o755)
print(a)

# 3.9 큰 배열 계산
# 문제
# 배열이나 그리드와 같이 커다란 숫자 데이터세트에 계산을 해야 한다
# 해결
# 배열이 관련된 커다란 계산을 하려면 NumPy 라이브러리를 사용한다. NumPy를 사용하면
# 표준 파이썬 리스트를 사용하는 것보다 수학 계산에 있어 훨씬 효율적이다
# 파이썬 리스트와 NumPy의 차이점을 보여주는 간단한 예를 준비했다
# 파이썬 리스트 ---
x = [1,2,3,4]
y = [5,6,7,8]
print( x*2) # [1, 2, 3, 4, 1, 2, 3, 4] 출력
# print(x+10)
# Traceback (most recent call last):
#   line 493, in <module>
#     print(x+10)
# TypeError: can only concatenate list (not "int") to list 출력
print(x+y) # [1, 2, 3, 4, 5, 6, 7, 8] 출력

# NumPy 배열 ---
import numpy as np
ax = np.array([1,2,3,4])
ay = np.array([5,6,7,8])
print(ax * 2) # [2 4 6 8] 출력
print(ax + 10) # [11 12 13 14] 출력
print(ax+ay) # [ 6  8 10 12] 출력
print(ax*ay) # [ 5 12 21 32] 출력
# 앞에 나온대로 기본적인 수학 계산에 있어 많은 차이를 보인다.
# 특히 스칼라 연산이 요소 기반으로 적용된다.
# 또한 배열과 배열 간 계산을 하면 연산자가 모든 요소에 적용되고 새로운 배열을 생성한다
# 수학 연산이 모든 요소에 동시 적용된다는 점으로 인해 매우 빠르고 쉬운 배열 계산을 할 수 있다
# 다항식 예제)
def f(x):
    return 3*x**2 - 2*x +7
print(f(ax)) # [ 8 15 28 47] 출력
# NumPy는 배열에 사용 가능한 일반 함수를 제공한다.
# math 모듈이 제공하는 함수와 비슷하다
print(np.sqrt(ax)) # [ 1.          1.41421356  1.73205081  2.        ] 출력
print(np.cos(ax)) # [ 0.54030231 -0.41614684 -0.9899925  -0.65364362] 출력
# 일반함수는 배열 요소를 순환하며 요소마다 math 모듈 함수로 계산하는 것보다 수백배빠르다
# 예제1) 소수를 담는 10,000 x 10,000 2차원 그리드
grid = np.zeros(shape=(10000,10000), dtype=float)
print(grid)
# [[ 0.  0.  0. ...,  0.  0.  0.]
#  [ 0.  0.  0. ...,  0.  0.  0.]
#  [ 0.  0.  0. ...,  0.  0.  0.]
#  ...,
#  [ 0.  0.  0. ...,  0.  0.  0.]
#  [ 0.  0.  0. ...,  0.  0.  0.]
#  [ 0.  0.  0. ...,  0.  0.  0.]] 출력
# 또한 모든 연산은 모든 요소에 동시 적용된다!!

# ★ 중요한 2차원 배열의 예시1)
a = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
# 첫번째 행 선택
print(a[1]) # [5 6 7 8] 출력
# 첫번째 열 선택
print(a[:,1]) # [ 2  6 10] 출력
# 열을 뽑을려면 [:,?]을 기억하자 [:,?][:,?][:,?][:,?][:,?][:,?]
# 지역을 선택 후 변경
a[1:3,1:3] += 10
print(a)
# [[ 1  2  3  4]
#  [ 5 16 17  8]
#  [ 9 20 21 12]] 출력
# 행 벡터를 모든 행 연산에 적용
b = a+[100,101,102,103]
print(b)
# [[101 103 105 107]
#  [105 117 119 111]
#  [109 121 123 115]] 출력
# 조건 할당
b = np.where(a < 10,a,10) # a<10 이면 a를 출력 아니면 10 출력
print(b)
# [[ 1  2  3  4]
#  [ 5 10 10  8]
#  [ 9 10 10 10]] 출력

# 3.10 행렬과 선형 대수 계산
# 문제
# 행렬 곱셈,행렬식 찾기, 선형 방정식 풀기 등 행렬이나 선형 대수 계산을 해야 한다
# 해결
# NumPy 라이브러리에 이런 용도로 사용할 수 있는 matrix 객체가 있다.
import numpy as np
m = np.matrix([[1,-2,3],[0,4,5],[7,8,-9]])
# 전치 행렬
print(m.T)
# [[ 1  0  7]
#  [-2  4  8]
#  [ 3  5 -9]] 출력
# 역행렬
print(m.I)
# [[ 0.33043478 -0.02608696  0.09565217]
#  [-0.15217391  0.13043478  0.02173913]
#  [ 0.12173913  0.09565217 -0.0173913 ]] 출력
# 벡터를 만들고 곱하기
v = np.matrix([[2],[3],[4]])
print(v)
# [[2]
#  [3]
#  [4]] 출력
print(m*v)
# [[ 8]
#  [32]
#  [ 2]] 출력
# numpy.linalg 서브패키에 더 많은 연산이 있다
import numpy.linalg
#Determinant
a = numpy.linalg.det(m)
print(a) # -230.0 출력
