#문제 : 주어진 문법 규칙에 따라 텍스트를 파싱하고 동작을 수행하거나 입력된 텍스트를 추상 신텍스 트리로 나타내야 한다. 문법은 간단하지만 프레임 워크를 사용하지 않고 직접 작성하고 싶다.
#해결 : 이문제는 특정 문법에 따라 텍스트를 파싱하는 데 집중한다. 우선 문법의 정규 스펙을 BNF나 EBNF로 하는 데서 시작한다. 예를 들어 간단한 산술 표현식을 다음과 같이 나타낼 수 있다.
# expr ::= expr + term
#      |   expr - term
#      |   term
# term ::= term * factor
#      |   term / factor
#      |   factor
# factor ::= (expr)
#        |   NUM

#EBNF에서 {...}*로 감싸는 부분은 선택할 수 있는 부분이다. * 부호는 하나도 없거나 여러번 반복됨을 의미한다.(정규식과 같은의미)
#BNF가 익숙치 않다면, 왼쪽에 있는 심볼이 오른쪽에 있는 심볼로 치환(혹은 그 반대)될 수 있는 규약정도로 생각하자.
#일반적으로 입력받은 텍스트를 BNF를 사용해 여러가지 치환과 확장을 해서 문법에 매칭하는 과정이 파싱에서 일어난다.
#예를들어 3 + 4 * 5 라는 문자열을 파싱한담ㄴ 이 표현식은 2.18에 나온대로 토큰화 해야한다. 그 결과는
#NUM + NUM * NUM
#이제 치환을 통해 입력 토큰을 문법에 매칭하는 것으로 진행된다.
# expr
# expr ::= term {(+|-) term}*
#

#뒤이어 오는 모든 치환 과정은 시간이 조금 걸리지만, 모두 입력을 살펴보고 문법 규칙에 매칭하는 방식이다. 첫번째 입력토큰은 NUM이다. 그러므로 첫번째 치환은
#이 부분 매칭에 집중한다. 매칭이 일어나고 나면 초점은 다음 토큰인 +로 넘어가고 계속해서 이런 식으로 진행이 된다. 특정 부분의 오른쪽(예를 들어 {*/} factor}*)은 다음 토큰에 매칭할수 없다고 판단되면
#사라지기도 한다. 파싱에 성공하면 입력 토큰 스트림ㅇ ㅔ매칭하기 위해 오른쪽 부분이 확장된다.
#재귀 표현식 해석기
import re, collections
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'
master_pat = re.compile('|'.join([NUM,PLUS,MINUS,TIMES,DIVIDE,LPAREN,RPAREN,WS]))
Token = collections.namedtuple('Token',['type','value'])
def generate_tokens(text):
    scanner = master_pat.scanner(text)
    for m in iter(scanner.match,None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok
class ExpressEvaluator:
    '''
    재귀 파서 구현, 모든 메소드는 하나의 문법 규칙을 구현한다.
    현재 룩어헤드 토큰을 받고 테스트하는 용도로 ._accept()를 사용한다.
    입력 받은 내역에 완벽히 매칭하고 다음 토큰을 무시할 때는
    ._expect()를 사용한다(혹시 매칭하지 않는 경우에는 Syntex Error를 발생)
    '''
    def parse(self,text):
        self.tokens = generate_tokens(text)
        self.tok = None
        self.nexttok= None
        self._advance()
        return self.expr
    def _advance(self):
        'Advance one token ahead'
        self.tok, self.nexttok = self.nexttok, next(self.tokens,None)

    def _accept(self,toktype):
        'Test and consume the next token if it matches toktype'
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False
    def _expect(self,toktype):
        'Consume next token if it matches toktype or raise Syntaxerror'
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    def expr(self):
        "expression ::= term {('+'|'-') term}*"

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
        "term ::= factor {('*'|'/') factor}*"

        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            if op == 'TIMES':
                termval += right
            elif op == 'DIVIDE':
                termval /= right
        return termval

    def factor(self):
        "factor ::= NUM | (expr)"
        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected Number or LPAREN')

e = ExpressEvaluator()
e.parse('2')
#순수해석 이상의 일을 하고싶다면 수정해야됨.