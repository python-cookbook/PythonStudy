'''
2.17-3.10
'''


'''

2.17 HTML과 XML 엔티티 처리 : &entity;나 &#code;와 같은 HTML, XML 엔티티를 일치하는 문자로 치환하고 싶은 경우 혹은 텍스트에서 특정 문자를 피하고 싶은 경우 
                            html.escape()를 사용한다.
- 텍스트를 ASCII로 만들고 캐릭터 코드를 아스키가 아닌 문자로 넣고 싶으면 errors = 'xmlcharrefreplace' 인자를 입출력 함수에 사용한다.

* 파싱(Parsing)

파싱이란 무엇인가? 파싱이란 의미를 추출하기 위해 일련의 심벌을 처리하는 것을 말한다. 
전형적으로 이것은 문장에서 단어를 읽어 이로부터 의미를 끌어내는 것을 의미한다. 
응용프로그램이 텍스트로 된 데이터를 처리해야 할 때 파싱로직 형태의 뭔가를 사용해야 한다. 
이 로직은 텍스트 문자와 문자 그룹(단어)를 스캔하며 정보나 명령을 추출하기 위해 문자 그룹을 인지한다. 

소프트웨어 파서는 일반적으로 특정 형태의 텍스트를 처리하기 위해 만들어진 특수 목적의 프로그램이다. 
이 텍스트는 보험이나 의료계에서 사용하는 알 수 없는 기호로 이루어진 문자 일수도 있고, C 헤더 파일에 있는 함수 선언, 그래프의 상호간 연결을 보여주는 node-edge에 대한 설명, 
웹페이지의 HTML태그, 혹은 네트워크 설정을 위한 명령어, 3D 이미지 수정이나 회전을 위한 명령어 일 수 있다. 

각각의 경우 파서는 문자 그룹과 패턴의 특정 집합을 처리한다. 이 패턴 집합을 파서의 문법이라 한다. 

예를 들면, 문자 Hello, World!를 파싱할 때 일반적인 패턴을 따르는 인사말을 파싱하고 싶을 것이다. 
Hello, World!는 인사말 단어 Hello로 시작한다. 
아주 많은 인사말이 있다. Howdy, Greetings, Aloha, G’day등. 
그러므로 단지 한 단어의 인사말로 시작하기 위해서는 아주 좁은 의미의 인사말 문법을 정의 할 수 있다. 
콤마 문자가 뒤에 온 다음 인사말과 인사하는 대상이 한 단어로 온다. 마지막으로 감탄부호와 같은 종료 구두점이 인사말을 끝낸다. 
이 인사 문법은 대략 아래와 같다.(::는 ~로 구성되어 있다는 의미이다)

word           :: group of alphabetic characters
salutation     :: word
comma          :: ","
greetee        :: word
endPunctuation :: "!"
greeting       :: salutation comma greetee endPunctuation

이것은 BNF형태이다. 기호를 표현하는 데는 아주 많은 방법이 있다. 

BNF형태의 내용으로 원하는 문법을 정의 했으면 실행 가능한 형태로 이 것을 변환해야 한다. 
일반적인 방법이 재귀 하향 파서를 만드는 것이다. 
이 파서는 저 수준의 함수를 호출하는 고 수준의 함수와 문법의 터미널을 읽어 들이는 기능을 정의한다. 
함수는 현 파싱 위치에서 일치하는 패턴이 있으면 일치하는 토큰을 리턴하고 실패하는 경우 예외를 발생시킨다. 

Pyparsing이란? 

Pyparsing은 재귀 하향 파서를 쉽고 빠르게 작성하도록 돕는 파이썬 클래스 라이브러리 이다. 아래에 Hello, World!보기에 대한 파싱 보기가 있다.

from pyparsing import Word, Literal, alphas

salutation     = Word( alphas + """ )
comma          = Literal(",")
greetee        = Word( alphas )
endPunctuation = Literal("!")

greeting = salutation + comma + greetee + endPunctuation

Pypasring의 여러 기능은 개발자가 텍스트 파싱 기능을 빠르게 개발하도록 돕는다.
문법은 파이썬을 따른다. 그러므로 문법을 정의한 별도의 파일이 필요치 않다.
추가적인 어떤 문법도 필요없다. And에 대한 +, Or에 대한 ^, 첫 매치에 대한 | 그리고 Not에 대한 ~은 예외이다.
어떤 특별한 코드 생성 단계도 없다.
파서 요소 사이에 나타나는 스페이스와 주석은 암묵적으로 아무 처리도 하지 않는다. 무시 가능한 텍스트에 표시를 해서 문법을 복잡하게 할 필요가 없다.
pyparsing문법은 Hello, World!뿐만 아니라 아래의 문장 중 그 어느 것도 파싱을 한다.

Hey, Jude!
Hi, Mom!
G"day, Mate!
Yo, Adrian!
Howdy, Pardner!
Whattup, Dude!

예제1은 완전한 Hello, World!파서와 파싱된 결과를 보여주고 있다. 

예제 1
from pyparsing import Word, Literal, alphas

salutation     = Word( alphas + """ )
comma          = Literal(",")
greetee        = Word( alphas )
endPunctuation = Literal("!")

greeting = salutation + comma + greetee + endPunctuation

tests = ("Hello, World!", 
"Hey, Jude!",
"Hi, Mom!",
"G"day, Mate!",
"Yo, Adrian!",
"Howdy, Pardner!",
"Whattup, Dude!" )

for t in tests:
        print t, "->", greeting.parseString(t)

===========================
Hello, World! -> ["Hello", ",", "World", "!"]
Hey, Jude! -> ["Hey", ",", "Jude", "!"]
Hi, Mom! -> ["Hi", ",", "Mom", "!"]
G"day, Mate! -> ["G"day", ",", "Mate", "!"]
Yo, Adrian! -> ["Yo", ",", "Adrian", "!"]
Howdy, Pardner! -> ["Howdy", ",", "Pardner", "!"]
Whattup, Dude! -> ["Whattup", ",", "Dude", "!"]

Pyparsing은 조합자(Combinator)이다 

pyparsing모듈로 먼저 문법의 기본적인 것들을 정의한다. 그 다음 전체 문법 문장에 대한 다양한 분기를 위해 좀더 복잡한 파서 표현으로 이것들을 조합한다. 
다음과 같이 관계를 정의하여 이것들을 조합한다.
문법 내에서 어떤 표현이 뒤 따라야 하는가? 예를 들면 키워드 if 다음에는 괄호로 묶여진 불리언 표현식이 뒤 따른다.
문법 내에서 어떤 표현이 특정 지점에서 올바른 대체표현인가? 예를 들면 SQL 명령어는 SELECT, INSERT, UPDATE, 혹은 DELETE로 시작할 수 있다.
어떤 표현이 선택적인 표현인가? 예를 들면 전화번호는 선택적으로 괄호로 된 지역번호 뒤에 올 수 있다.
어떤 표현이 반복적인가? 예를 들면 XML태그는 0혹은 그 이상의 속성을 가질 수 있다.
복잡한 문법이 수십 개 혹은 수백 개의 문법 조합을 포함하고 있다 할지라도 대부분의 파싱은 단지 몇 개의 정의로 쉽게 수행된다. 
생각을 조직화 하고 파서를 디자인 하는데 BNF형태로 문법을 기술하는 것이 도움이 된다. 
이것은 또한 pyparing의 함수와 클래스로 문법을 구현하는 당신의 작업을 추적하는 데도 도움을 준다. 

간단한 문법 정의하기 

대부분의 문법 중 가장 작은 부분을 차지하는 것은 전형적으로 문자열에 대한 정확한 매칭이다. 아래에 전화번호 파싱을 위한 간단한 BNF가 있다.

number      :: "0".. "9"*
phoneNumber :: [ "(" number ")" ] number "-" number
이것은 전화번화 내에서 괄호와 대시(-)를 찾기 때문에 이 구두점 표시를 위해 간단한 토큰을 정의 할 수 있다.
dash   = Literal( "-" )
lparen = Literal( "(" )
rparen = Literal( ")" )
전화번호 내에서 숫자를 정의하기 위해서 다양한 길이의 문자열을 처리할 필요가 있다. 이를 위해서는 Word토큰을 사용하라
digits = "0123456789"
number = Word( digits )
숫자 토큰은 숫자로 나열되는 문자로 구성된 연속된 열과 일치할 것이다. 즉 이것은 숫자로 구성된 단어이다.
(알파벳으로 구성되는 전형적인 단어와는 반대로) 이제 전화번호에 대한 각각의 문자열을 얻었으므로 이제 And 클래스를 사용하여 이것들을 문자열로 만들 수 있다.

phoneNumber = 
    And( [ lparen, number, rparen, number, dash, number ] )
    
이것은 읽기에 자연스럽지 않다. 다행히도 pyparsing모듈은 좀더 쉽게 각 파서 요소를 조합하기 위한 연산자 메서드를 정의한다. 좀더 읽기 쉬운 정의는 And를 위해 +를 사용한다.

phoneNumber = lparen + number + rparen + number + dash + number

좀더 쉽게 하기 위해 +연산자는 묵시적으로 문자 그대로 변환되는 파서 요소와 문자를 묶는다. 이것이 읽기에 더 쉽다.

phoneNumber = "(" + number + ")" + number + "-" + number

최종적으로 전화번호의 첫 부분에 지역 번호가 선택적임을 나타내기 위해 pyparsing의 Optional클래스를 사용한다.

phoneNumber = Optional( "(" + number + ")" ) + number + "-" + number

문법 사용하기 

문법을 정의한 후 다음 단계는 파싱할 텍스트에 적용하는 것이다. 

pyparsing표현은 주어진 문법으로 입력 텍스트를 처리하기 위해 3가지의 메서드를 지원한다.

parseString - 입력 문자열의 내용을 판독하고 문자열을 파싱하고, 그리고 각 문법 구조에 대한 하위 문자열과 문자열의 조합을 리턴하는 문법을 사용한다.
scanString - 단지 입력 문자열과 일치할 수 있는 문법을 사용하며 이 문법은 일치 검사를 위해 문자열을 스캔하고 입력 문자열 내에 시작점과 마지막 지점 
             그리고 일치된 토큰을 포함하는 튜플을 리턴한다.
transformStirng - scanString의 변종이다. 이것은 일치할 때 마다 수정되는 일치한 토큰의 변화에 대응하며 최초 입력 텍스트가 표현하는 하나의 문자열을 리턴한다.

Hello, World!파서는 parseString을 호출하고 바로 파싱된 결과인 토큰을 리턴한다.
Hello, World! -> ["Hello", ",", "World", "!"]

비록 이것이 토큰 문자열의 간단한 리스트로 보이긴 하지만 pyparsing은 ParseResults 오브젝트를 사용하여 데이터를 리턴한다. 
위 예제에서 결과 값들은 파이썬의 리스트 데이터처럼 보인다. 사실 리스트 데이터처럼 단지 결과에 순서를 붙일 수도 있다.

print results[0]
print results[-2]

는 다음과 같이 나타난다.

Hello
World

parseResult를 이용하여 각 문장에 이름을 정의할 수도 있다. 이것은 파싱된 텍스트와 비트열을 반복적으로 검사하는 것을 더욱 쉽게 해 준다. 
이것은 특히 문법이 선택적인 부분을 포함하고 있을 때 유용하다. 이 문법은 리턴된 토큰 리스트의 길이와 오프셋을 변경할 수 있다.

salute  = Word( alphas+""" ).setResultsName("salute")
greetee = Word( alphas ).setResultsName("greetee")

마치 리턴된 결과의 속성인 것처럼 대응되는 토큰을 참조할 수 있다.

print hello, "->", results    
print results.salute
print results.greetee

위의 내용은 다음과 같이 나타난다.
G"day, Mate! -> ["G"day", ",", "Mate", "!"]
G"day
Mate

위 결과는 당신이 작성한 파싱 프로그램의 가독성과 유지 보수성을 향상 시키는데 커다란 도움을 준다. 

전화번호 문법의 경우 차례대로 전화번호 리스트를 가지고 있는 입력 문자열을 파싱한다. 다음과 같다.

phoneNumberList = OneOrMore( phoneNumber )
data            = phoneNumberList.parseString( inputString )

이것은 pyparsing의 ParseResult 오브젝트 형태로 데이터를 리턴할 것이고 이 오브젝트는 입력 전화번호의 모든 리스트를 가지고 있다. 

Pyparsing은 delimitedList와 같은 유용한 표현을 가지고 있으며 입력이 콤마로 구분되는 전화번호 리스트인 경우 간단하게 phoneNumberList를 다음과 같이 변경할 수 있다

phoneNumberList = delimitedList( phoneNumber )

이것은 전과 같은 전화번호 리스트를 리턴한다. dellimiteList는 모든 표현식과 문자열을 지원한다. 콤마 구분자가 가장 일반적이어서 기본으로 사용된다. 

단지 전화번호만 가지고 있는 문자열 대신 우편번호, 주소, 메일주소, 전화번호를 가지고 있는 경우 scanString을 사용하는 전화번호로 확장해야 한다. 
scanString은 파이썬 생성 함수이며 for 루프, 리스트 , 생성 표현식 내에서 이것을 사용해야 한다.

for data,dataStart,dataEnd in 
    phoneNumber.scanString( mailingListText ):
    .
    .
    # 전화번호 토큰으로 뭔가를 한다, 
    # data변수에 리턴된다
    .
    .
    
마지막으로 같은 메일링 리스트를 가지고는 있지만 잠재저인 전화 판매원으로부터 전화번호를 숨기고자 하는 경우 
모든 전화번호를 (000)000-0000문자열로 변환하는 파서 동작을 추가하여 문자열을 변환 할 수 있다.

phoneNumber.setParseAction( replaceWith("(000)000-0000") )
sanitizedList = 
    phoneNumber.transformString( originalMailingListText )

적절한 입력에 대한 동작이 정의 되지 않은 경우 

Pyparsing은 주어진 파서 요소에 대해 일치하는 텍스트가 없어질 때까지 입력을 처리한다. 
예상치 못한 토큰이나 문자를 만나고 이에 적절한 처리가 없는 경우 pyparsing은 parseException을 발생 시킨다. 
parseException은 기본으로 진단 메시지를 출력하며 이 메시지에는 라인번호, 칼럼, 텍스트 라인과 주석문이 포함된다. 

파서에 Hello, World?라는 문장이 입력되는 경우 다음과 같은 예외를 만나게 된다.
pyparsing.ParseException: Expected "!" (at char 12), (line:1, col:13)
이를 바탕으로 입력문자열을 수정하거나 문장에 대해 좀더 관대한 문법을 작성할 수 있다. 위의 경우에 올바른 문장 종결자로 물음표를 지원하면 된다


* 3.3까지 HTMLparser().unescape()로 사용했지만 3.6에선 기본으로 html.unescape()로 지원한다.

- html.parser나 xml.etree.ElementTree와 같은 파싱 모듈을 사용하면 기본적인 내용을 알아서 처리해준다.


'''

# 예1.
s = 'Elements are written as "<tag>text</tag>".'
import html
print(s)
# Elements are written as "<tag>text</tag>".
print(html.escape(s))
# Elements are written as &quot;&lt;tag&gt;text&lt;/tag&gt;&quot;.

# 예2.
s = 'Spicy Jalapeno'
s.encode('ascii', errors='xmlcharrefreplace')

# 예3.
s = 'Spicy &quot;Jalape&#241;o&quot.'
html.unescape(s)

'''

2장 18절 텍스트 토큰화 : 문자열을 파싱해서 토큰화 하고 싶은 경우 

* http://excelsior-cjh.tistory.com/entry/Chap01-Tokenizing-Text-and-WordNet-Basics-Part1 참조

* 토큰과 토큰화
토큰화란 문자열을 여러개의 조각, 즉 여러 개의 Token(토큰)들로 쪼개는 것을 말한다. 토큰은 문자열의 한 조각으로 하나의 단어가 하나의 토큰이라고 할 수 있다.

- 토큰화 할 때 re는 명시한 순서대로 패턴을 매칭하므로 한 패턴이 다른 패턴의 부분이 되는 경우가 있다면 항상 긴 패턴을 먼저 입력해야 한다.
- 패턴이 부분 문자열을 형성하는 경우도 조심해야 한다.

'''

# 예4.
import re
NAME = r'(?P<NAME>[a-zA-z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))

scanner = master_pat.scanner('foo=42')
scanner.match()
# <_sre.SRE_Match object; span=(0, 3), match='foo'>
_.lastgroup, _.group()
# _.lastgroup, _.group()
scanner.match()
# <_sre.SRE_Match object; span=(4, 6), match='42'>
_.lastgroup, _.group()

# 예5.
from collections import namedtuple
Token = namedtuple('Token', ['type', 'value'])
def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())

for tok in generate_tokens(master_pat, 'foo = 42'):
    print(tok)

# Token(type='NAME', value='foo')
# Token(type='WS', value=' ')
# Token(type='EQ', value='=')
# Token(type='WS', value=' ')
# Token(type='NUM', value='42')

'''

2장 19절 간단한 재귀 파서 작성 : 주어진 문법 규칙에 따라 텍스트를 파싱하고 동작을 수행하거나 입력된 텍스트를 추상 신택스 트리로 나타내야 한다.
                             혹은 문법은 간단하지만 프레임워크를 사용하지 않고 파서를 직접 작성하고 싶은 경우 일단 문법의 정규 스펙을 BNF나
                             EBNF로 하는데서 시작한다.

- BNF
BNF는 프로그래밍 언어를 정의하기 위한 최초의 메타 언어였다. 
BNF는 구문 요소를 나타내는 기호 < >, 둘 중 하나의 선택을 의미하는 기호 ∥, 좌변은 우변에 의해 정의됨을 의미하는 기호 ::= 등의 메타 기호들을 사용하여 규칙을 표현한다.

BNF 표기법
1. 언어 구문의 형식 정의 (formal definition)
    언어를 가지고 정상적인 프로그램을 작성하는 규율들의 집합
    일반적으로 형식 정의에서 이 규율들은 그대로 적용되는 공식이나 순서도(flowchart)를 가지고 표현
2. BNF(Backus-Naur Form)표기법
    구문 형식을 정의하는 가장 보편적인 기법
    →ALGOL을 정의할 때 최초로 사용
    한 언어의 구문에 대한BNF의 정의는 생성규칙(production rule) 들의 집합
    생성 규칙은 구문 규율
    ·생성규칙은 하나의 정의를 이루는데, 규칙의 왼쪽에는 정 의될 대상(object)을, 오른쪽에는 그 대상에 대한정의를 표현
    언어를 가지고 정상적인 프로그램을 작성하는 규율들의 집합
    일반적으로 형식 정의에서 이 규율들은 그대로 적용되는 공식이나 순서도(flowchart)를 가지고 표현
3. BNF의 형식
    BNF는 하나의 수학적인 게임 같은 종류이다. 
    즉 당신은 하나의 symbol(s라는 이름으로 약속된 start symbol이 호출되어)과 이 symbol과 함께 위치 할 수 있는 주어진 규칙으로 시작한다. 
    BNF에 의해 정의된 그 언어는 오직 다음의 이들 규칙(production rule)들에 의해 제공할 수 있는 모든 문자열의 집합이다.
    
    symbol := alternative1 | alternative2 ....
                       또는 
<identifire> ::=<letter> | <identifire><letter> | <identifire><digit> ....

 예)
 
 <identifier> ::== <letter>|<identifier><letter>|<identifier><digit>
 <letter> ::== A|B|C| ... |X|Y|Z
 <digit>  ::== 0|1|2| ... |7|8|9

    - BNF 표기법에 의한 식별자 정의
    비 단말 기호 : - 각 괄호(<>)로 묶인 기호(재 정의 될 대상이라는 의미)
    단말 기호 : 각 괄호로 묶이지 않은 기호(알파벳 문자 집합, 예약어)
    메타 기호 : 특수기호(::==, |, <> 등)와 같이 언어를 표현하기 위해 사용되는 특수 기호들.
               ::== <- 정의된다 / | <- 택 일
               
               
               
    production rule은 간단하게 ":="의 왼쪽 부분에 있는 symbol이 오른쪽에 있는 alternative 중에 하나와 대체되어야 한다고 말한다. 
    alternative emfdms "|"에 의해서 구별되고, 나누어진다(참고로 ":=" 대신 "::="이 사용되기도 하는데, 의미는 동일하다.). 
    Alternative들은 일반적으로 terminal(단말기호)이라고 불리는 것과 symbol(비단말기호)로 구성된다. Terminal들은 간단하게 symbol들이 아닌 마지막 문자열의 조각들이다. 
    그들은 production rule에 적용되지 않기 때문에 terminal들이라고 부른다.(Symbol들을 종종 Non-terminal이라고도 부른다.) 
    BNF에서 다른 변동은 symbol들로부터 그들을 분류하기 위해 인용부호로 terminal들을 동봉한다. 
    몇몇 BNF 문법에서는 공백이 그것에 대해 symbol을 가지는 것을 허락하는 장소나 다른 문법들을 읽는 자가 암시하게 이것을 남겨놓는 장소를 분명하게 보여준다.

4. BNF 형식 사용예

<sentence:문장> ::= <noun-phrase:명사구><verb-phrase:동사구>.
<noun-phrase> ::= <article:관사><noun:명사>
<article> ::= a | the
<noun> ::= girl | dog
<verb-phrase> ::= <verb><noun-phrase>
<verb:동사> ::= sees | pets
<sentence>로부터 문장 생성의 예
<sentence>-> <noun-phrase><verb-phrase>.
           -> <article><noun><verb-phrase>.
           -> the <noun><verb-phrase>.
           -> the girl <verb-phrase>.
           -> the girl <verb><noun-phrase>.
           -> the girl sees <noun-phrase>.
           -> the girl sees <article><noun>.
           -> the girl sees a <noun>.
           -> the girl sees a dog.


- EBNF
BNF 표기법으로 모든 프로그래밍 언어를 표기할 수 있지만, 보다 읽기 쉽고 간결하게 표현 할 수 있는 확장된 EBNF(Extended BNF)를 사용하기도 한다. 
EBNF는 특수한 의미를 갖 는 메타 기호를 더 사용하여 반복되는 부분이나 선택적인 부분을 간결하게 표현할 수 있으 며, 반복되는 부분을 나타내려면 { }를 사용한다.
즉, {a}는 a가 0번 이상 반복될 수 있음 을 의미한다.

              
               
'''

