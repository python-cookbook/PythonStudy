####################################################################################################
# 2.18] 텍스트 토큰화
#   * 문자열을 파싱해서 토큰화하고 싶다!
#
#   * 주의사항 : 한 패턴이 다른 패턴의 부분이 되는 경우가 있다면 항상 더 긴 패턴을 먼저 넣어야 한다!
####################################################################################################
from collections import namedtuple
import re

# 패턴에 이름을 붙이기 위해 이름 있는 캡쳐 그룹을 사용하는 정규 표현식 사용
NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'
master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))

Token = namedtuple('Token', ['type','value'])

def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())


for tok in generate_tokens(master_pat, 'foo = 42'):
    print(tok)
    ###
    # Token(type='NAME', value='foo')
    # Token(type='WS', value=' ')
    # Token(type='EQ', value='=')
    # Token(type='WS', value=' ')
    # Token(type='NUM', value='42')
    ###