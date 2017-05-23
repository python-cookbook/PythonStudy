####################################################################################################
# 2.19] 간단한 재귀 파서 작성
#   * 주어진 문법 규칙에 따라 텍스트를 파싱하고 동작을 수행하거나,
#     입력된 텍스트를 추상 신택스 트리로 나타내야 한다.
#     문법은 간단하지만 프레임워크를 사용하지 않고 파서를 직접 작성하고 싶다.
####################################################################################################
import re
import collections

## 토큰 스펙화
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS]))

## 토큰화
Token = collections.namedtuple('Token', ['type','value'])

def generate_tokens(text):
    if __name__ == '__main__':
        scanner = master_pat.scanner(text)
        for m in iter(scanner.match, None):
            tok = Token(m.lastgroup, m.group())
            if tok.type != 'WS':
                yield tok

##파서 (사칙연산)
class ExpressionEvaluator:
    '''
    재귀 파서 구현, 모든 메소드는 하나의 문법 규칙을 구현한다.
    현재 룩어헤드 토큰을 받고 테스트하는 용도로, ._accept()를 사용한다.
    입력받은 내역에 완벽히 매칭하고 다음 토큰을 무시할 때는 ._expect()를 사용한다.
    (혹시 매칭하지 않는 경우에는 SyntaxError를 발생시킨다.)
    '''

    def parse(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None     # 마지막 심볼 소비
        self.nexttok = None # 다음 심볼 토큰화
        self._advance()     # 처음 룩어헤드 토큰 불러오기
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
        'Consume next token if it matches toktype or raise SyntaxeError'
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    #문법 규칙
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
        "factor ::= NUM | (expr)"
        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')

e = ExpressionEvaluator()
print(e.parse('2')) # 2
print(e.parse('2 + 3 * 4')) # 14
print(e.parse('2 + (3 + 4) * 5'))   # 37


## 간단한 파싱 트리 구현식
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
print(e.parse('2 + 3')) # ('+', 2, 3)
print(e.parse('2 + (3 + 4) * 5'))   # ('+', 2, ('*', ('+', 3, 4), 5))