#2.18 텍스트 토큰화
#문제 문자열을 파싱해서 토큰하고 싶다.
#해결 다음과 같은 문자열ㅇ ㅣ있다.
text = 'foo = 23 + 42 * 10'
#문자열을 토큰화하려면 패턴 매칭 이상의 작업이 필요하다. 패턴을 확인할 방법을 가지고 있어야 한다. 예를 들어 문자열을 다움과 같은 페어 시퀀스로 바꾸고 싶다.
tokens = [('Name','foo'),('EQ','='),('NUM','23'),('PLUS','+')]
#이런 나누기 작업을 하기 위해서는 공백을 포함하여 가능한 모든 토큰을 저으이해야 한다. 다음 코드에서는 이름 있는 캡처 그룹을 사용하는 정규식을 사용한다.
import re
Name = r'(?P<NAME>[a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
master_pat = re.compile('|'.join([Name,NUM]))
#re패턴에서 패턴에 이름을 붙이기 위해 ?P<TOKENNAME>을 사용하고 있다. 이 이름은 나중에 사용한다.
#다음으로 토큰화를 위해서 패턴 객체의 ㅇ잘 알려지지 않은 scanner()메소드를 사용한다. 이 메소드는 스캐너 객체를 생성하고 전달 받은 텍스트에 match()를 반복적으로 하나씩 호출한다.
#스캐너 객체가 동작하는 모습을 다음 예제를 통해 살펴본다.
scanner = master_pat.scanner('foo=42')
scanner.match()
_.lastgroup, _.group() #('NAME', 'foo')
#이것을 코드에 응용해보면 간결한 생성자르 ㄹ만들수 있다.
from collections import namedtuple
Token = namedtuple('Token',['type','value'])
def generate_tokens(pat,text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())
# 사용 예
for tok in generate_tokens(master_pat,'foo=42'):
    print(tok)
#토큰 스크림을 걸러 내고 싶으면 생성자 함수를 더 많이 정의하거나 생성자 표현식을 사용한다. 예를 들어 모든 공백문을 다음과 같이 걸러 낼 수 있다.
tokens = (tok for tok in generate_tokens(master_pat,text) if tok.type != 'NUM')
for tok in tokens:
    print(tok)

#토론 보통 더 복잡한 텍스트 파싱이나 처리를 하기 전에 토큰화를 한다. 앞에서 나온 스캔 기술을 사용하려면 다음 몇가지 중요한 사항을 기억하자.우선 입력부에 나타나는 모든 텍스트 시퀀스를 re패턴으로 확인 해야한다.
#매칭하지 않는 텍스트가 하나랃 ㅗ있으면 스캐닝이 거기서 멈춘다. 예제에서 공백 토큰을 ㅁㅇ시할 필요가 있었던 이유도 이와 같다.
#마스터 정규 표현식의 토큰 순서도 중요하다. 매칭할 때 re는 명시한 순서대로 패턴을 매칭한다. 따랏 ㅓ한 패턴이 다른 패턴의 부분이 되는 경우가 있다면 항상 더 긴 패턴을 먼저 넣어야 한다..
LT =r'(?P<LT><)'
LE =r'(?P<LE><=)'
EQ =r'(?P<EQ>>=)'
master_pat = re.compile('|'.join([LE,LT,EQ]))
#master_pat = re.compile('|'.join([LT,LE,EQ]))
#두번째 패턴의 경우 <= 텍스트를 LT와 EQ라고 매칭할 텐데. 실제로는 LE라고 매칭해야 한다.
#그리고 마지막으로 패턴이 부분 문자열을 형성하는 경우도 조심해야 한다. 다음과 같이 두 패턴이 있다고 가정한다.
PRINT = r'(P<PRINT>print)'
NAME = r'(P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
master_pat = re.compile('|'.join([PRINT,NAME]))
for tok in generate_tokens(master_pat,'printer'):
    print(tok)
#토큰화에 대해 더 자세히 알고 싶다면 pyparsing이나 PLY등의 패키지를 알아보자.