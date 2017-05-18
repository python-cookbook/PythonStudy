===============================================================================
# 1.18 시퀀스 요소에 이름 매핑
# 리스트나 튜플의 위치로 요소에 접근하는 코드의 가동성 높이기
# 그리고 위치에 의존하는 코드의 구조 -> 이름으로 접근 가능하게 하기
# "collection.namedtuple()"
# 타입 이름과, 포함해야할 필드를 전달하면 인스턴스화 가능한 클래스 반환

EX1>
from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com', '2012-10-19')
sub
#Subscriber(addr='jonesy@example.com', joined='2012-10-19')
sub.addr
#'jonesy@example.com'
sub.joined
#'2012-10-19'

##namedtuple의 인스턴스는 튜플과 교환이 가능하고, 인덱싱이나 언패킹과 같은 튜플의 기능 지원.
len(sub)
#2
addr, joined = sub
addr
#'jonesy@example.com'
joined
#'2012-10-19'


##네임드튜플은 주로 요소의 위치를 기반으로 구현되어 있는 코드를 분리
##튜플이 요소의 위치로 접근하는 코드에서 테이블에 새 열이 추가되는 문제 예방 가능

EX2>
from collections import namedtuple
Stock = namedtuple('Stock', ['name', 'shares', 'price'])
def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total


##네임드튜플은 저장 공간을 더 필요로 하는 딕셔너리 대신 사용 가능하다.
## 하지만 딕셔너리와 다르게 수정 불가능!

EX3>
s = Stock('ACME', 100, 123.45)
s
#Stock(name='ACME', shares=100, price=123.45)

s.shares = 75
#AttributeError: can't set attribute

##속성을 수정하려면 "_replace() 메소드"
s = s._replace(shares=75)
s
#Stock(name='ACME', shares=75, price=123.45)
===============================================================================





===============================================================================
# 1.19 데이터를 변환하면서 줄이기
# 감소함수 (sum(), min(), max())를 실행해야 하는데, 먼저 데이터를 변환하거나 필터링할 때,
# "생성자 표현식"

##정사각형 넓이의 합
nums = [1, 2, 3, 4, 5]
s = sum(x * x for x in nums)
print(s)
#55

## 위의 코드는 반복적인 괄호를 할 필요가 없다.
s = sum((x * x for x in nums))    # 생성자 표현식을 인자로 전달
s = sum(x * x for x in nums)
===============================================================================






===============================================================================
# 1.20 여러 매핑을 단일 매핑으로 합치기
#딕셔너리나 매핑이 여러 개 있고, 자료 검색이나 데이터 확인을 위해서 하나의 매핑으로 합치기
#"collections 모듈의 ChainMap 클래스"

EX1>
a = {'x': 1, 'z': 3 }
b = {'y': 2, 'z': 4 }
#두 딕셔너리가 있는데, a에서 데이터를 검색하고,
#그 후 b에 그 데이터가 있는지 검색할 때,
from collections import ChainMap
c = ChainMap(a,b)
print(c['x'])    #1[a의 1]
print(c['y'])    #2[b의 2]
print(c['z'])    #3[a의 3]

##ChainMap은 매핑을 여러 개 받아서 하나처럼 "보이게" <> 하나로 합치기X
len(c)
#3
list(c.keys())
#['x', 'y', 'z']
list(c.values())
#[1, 2, 3]

## 중복 키가 있으면 첫번째 매핑으 ㅣ값을 사용
## 따라서 예제의 c['z']는 언제나 딕셔너리 a의 값을 참조하며 b의 값을 참조하지 X
## 매핑의 값을 변경한느 동작은 언제나 리스트의 첫번째 매핑에 영향을 준다.
EX2>
c['w'] = 40
del c['x']
a
#{'w': 40, 'z': 10}
del c['y']
#Traceback (most recent call last):
#  File "<ipython-input-79-df3e26fa6544>", line 1, in <module>
#    del c['y']
#  File "C:\Users\ATIV BOOK 9\Anaconda3\lib\collections\__init__.py", line 935, in __delitem__
#    raise KeyError('Key not found in the first mapping: {!r}'.format(key))
#KeyError: "Key not found in the first mapping: 'y'"


###ChainMap의 대안으로 update()를 사용해 딕셔너리를 하나로 합칠 수 있다.
EX3>
a = {'x': 1, 'z': 3 }
b = {'y': 2, 'z': 4 }
merged = dict(b)
merged.update(a)
merged['x']
#1
merged['y']
#2
merged['z']
#3
###잘 동작하지만 ,완전히 별개의 딕셔너리를 객체로 새로 만들어야 하너가 개존 딕셔너리의
### 내용을 변경해야 한다.
### 원본 딕셔너리의 내용이 변경된다 해도 합쳐 놓은 딕셔너리에 반영되지 않는다.
>>>
a['x']=13
merged['x']
#1


####ChainMap 은 원본 딕셔너리를 참조하기 때문에 문제X
a = {'x': 1, 'z': 3 }
b = {'y': 2, 'z': 4 }
merged = ChainMap(a, b)
merged['x']
#1
a['x'] = 42
merged['x']     #합친 딕셔너리에 변경 알림
#42
===============================================================================





#Chapter2_문자열과 텍스트
===============================================================================
# 2.1 여러 구분자로 문자열 나누기
# 문자열을 필드로 나누고 싶자먼 규뷴저(그리고 그 주변의 공백)가 문제열에 일관적이지 않을 때,
# split() 메소드는 간단하게 사용할 때만
# "re.split()"
# = 분리 구문마다 여러 패턴을 명시할 수 있다.


EX1>
line = 'asdf fjdk; afed, fjek,asdf, foo'
import re
re.split(r'[;,\s]\s*', line)
#['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

##분리구문 = 쉼표(,), 세미콜론(;), 공백문자, 뒤이어 나온느 하나 이상의 공백문자
##분리된 부분 모두가 구분자가 된다.
##결과는 필드 리스트로 출력


EX2>
fields = re.split(r'(;|,|\s)\s*', line)
fields
#['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo']


EX3>
values = fields[::2]
delimiters = fields[1::2] + ['']
values
#['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

delimiters
#[' ', ';', ',', ',', ',', '']

##re.strip()을 사용할 때는 괄호 안에 뭈인 정규 표현식 패턴이 캡처 그룹이 된다,
## 캡처 그룹을 사용하면, 매칭된 텍스트에도 결과가 포함된다.


EX4>
re.split(r'(?:,|;|\s)\s*', line)
# ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
## 분리 구문을 결과에 포함시키고 싶지 않지만 정규 표현식에 괄호를 사용해야 한다면,
##"논캡처 그룹"
===============================================================================





===============================================================================
# 2_2 문자열 처음이나 마지막에 텍스트 매칭
# 문자열의 처음이나 마지막에 파일 확장자, URL 스킴 등 특정 텍스트 패턴이 포함되었는지
# 검사하고 싶을 때 "str.startswith()" / "str.endswith()"

EX1>
filename = 'spam.txt'
filename.endswith('.txt')
#True

filename.startswith('file:')
#False

url = 'http://www.python.org'
url.startswith('http:')
#True


#여러 개의 선택지를 검사해야 한다면 검사하고 싶은 값을 튜플에 담아
#startswith() OR endswith()에 전달
EX2>
import os
filenames = os.listdir('.')
filenames
#['.anaconda',
# '.astropy',
# '.condarc',
#...

[name for name in filenames if name.endswith(('.c', '.h')) ]
#[]

any(name.endswith('.py') for name in filenames)
#False

##???다른 결과 출력

#startswith()와 endswith() 메소드는 접두어와 접미어를 검사할 때 편리
EX3>
filename = 'spam.txt'
filename[-4:] == '.txt'
#True
url = 'http://www.python.org'
url[:5] == 'http:' or url[:6] == 'https:' or url[:4] == 'ftp:'
#True

#정규식 사용
import re
url = 'http://www.python.org'
re.match('http:|https:|ftp:', url)
#<_sre.SRE_Match object; span=(0, 5), match='http:'>
===============================================================================

                              
                              
                              
                            
===============================================================================  
# 2.4 텍스트 패턴 매칭과 검색                              
# 텍스트 패턴 매칭과 검색
# 특정 패턴에 대한 텍스트 매칭이나 검색
# "str.find() & str.endswith() & str.startswith()"

EX1>
text = 'yeah, but no, but yeah, but no, but yeah'
# Exact match
text == 'yeah'
#False
# Match at start or end
text.startswith('yeah')
#True
text.endswith('no')
#False
# Search for the location of the first occurrence
text.find('no')
#10


#더 복잡한 매칭
EX2>
text1 = '11/27/2012'
text2 = 'Nov 27, 2012'

import re
# Simple matching: \d+ means match one or more digits
if re.match(r'\d+/\d+/\d+', text1):
    print('yes')
else:
    print('no')
#yes
if re.match(r'\d+/\d+/\d+', text2):
    print('yes')
else:
    print('no')
#no


#동일한 패턴으로 매칭을 많이 수행할 예정이라면 정규 표현식을 미리 컴파일해서
#패턴 객체로 만들어 놓기 >??
EX3>
datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')
#yes

if datepat.match(text2):
    print('yes')
else:
    print('no')
#no


#match()는 항상 문자열 처ㅓ음에서 찾기를 시도한다.
# 텐스트 전체에 걸쳐 패턴을 찾을 때, "findall()"
EX4>
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
datepat.findall(text)
#['11/27/2012', '3/13/2013']


#정규 표현식을 정의할 때 괄호를 사용해 캡처 그룹을 만든는 것이 일반적
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')


EX5>
#캡처 그룹을 사용하면 매칭된 텍스트에 작업할 때 각 그룹을 개별적으로 추출 가능
m = datepat.match('11/27/2012')
m
#<_sre.SRE_Match object; span=(0, 10), match='11/27/2012'>

# 각 그룹에서 내용 추출
m.group(0)
#'11/27/2012'
m.group(1)
#'11'
m.group(2)
#'27'
m.group(3)
#'2012'
m.groups()
#('11', '27', '2012')


month, day, year = m.groups()
#전체 매칭 찾기(튜플로 나눈다.)
text
#'Today is 11/27/2012. PyCon starts 3/13/2013.'
datepat.findall(text)
#[('11', '27', '2012'), ('3', '13', '2013')]
for month, day, year in datepat.findall(text):
    print('{}-{}-{}'.format(year, month, day))
#2012-11-27
#2013-3-13


#findall() 메소드는 텍스트를 검색하고 모든 매칭을 찾아 리스트로 반환
# 한번에 결과를 얻지 않고 텍스트를 순환하며 찾으려면 finditer() 사용
EX6>
for m in datepat.finditer(text):
    print(m.groups())
#('11', '27', '2012')
#('3', '13', '2013')
===============================================================================






===============================================================================
# 2.5 텍스트 검색과 치환
# 문자열에서 텐스트 패턴을 검색하고 치환하고 싶을 때,
# 간단한 패턴 = "str.replace()"
# 복잡한 패턴 = "re모듈의 sub()함수/메소드"

EX1>
text = 'yeah, but no, but yeah, but no, but yeah'
text.replace('yeah', 'yep')
#'yep, but no, but yep, but no, but yep'


EX2>
# 복잡한 패턴 = "re모듈의 sub()함수/메소드"
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
import re
re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
#'Today is 2012-11-27. PyCon starts 2013-3-13.'

#11/27/2012 -> 2012-11-27
#r'(\d+)/(\d+)/(\d+)' = 매칭을 위한 패턴
#r'\3-\1-\2' = 치환을 위한 패턴
#숫자 앞에 백슬래스 = 패턴의 캡처 그룹 참조


EX3>
#더 복잡한 치ㅏ환을 위해서 콜백 함수 명시 가능
from calendar import month_abbr
def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))

datepat.sub(change_date, text)
#Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'
#인자가 되는 치환 콜백은 match()나 find()에서 반환한 매치 객체를 사용
#매치에서 특정 부분을 추출하려면 ".group()" 메소드 [치환된 텍스트 반환]


EX4>
#치환된 텍스트를 받기 전에 치환이 몇 번 발생힜는지 알고 싶을 때, "re.subn()"
newtext, n = datepat.subn(r'\3-\1-\2', text)
newtext
#'Today is 2012-11-27. PyCon starts 2013-3-13.'
n
#2


# 2.6 대소문자를 구별하지 않는 검색과 치환
# 텍스트를 검색하고 치환할 대 대 소문자를 구별하지 않을 때,
# "re모듈" & "re.IGNORECASE"플래그 지정


EX1>
text = 'UPPER PYTHON, lower python, Mixed Python'
re.findall('python', text, flags=re.IGNORECASE)
#['PYTHON', 'python', 'Python']

re.sub('python', 'snake', text, flags=re.IGNORECASE)
#'UPPER snake, lower snake, Mixed snake'


EX2>
#치환된 텍스트의 대소문자와 원본의 대소문자가 일치하게
def matchcase(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
    return replace

re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE)
#'UPPER SNAKE, lower snake, Mixed Snake'
===============================================================================





===============================================================================
#2.7 가장 짧은 매칭을 위한 정규 표현식
EX1>
text2 = 'Computer says "no." Phone says "yes."'
str_pat.findall(text2)

str_pat = re.compile(r'\"(.*?)\"')
str_pat.findall(text2)
#r'\"(.*)\"' = 가장 긴 텍스트
#*뒤에 "?" 붙이기 = r'\"(.*?)\"' = 가장 짧은 텍스트
===============================================================================





                   
===============================================================================                   
# 2.8 여러 줄에 걸친 정규 표현식 사용
EX1>
comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = '''/* this is a
              multiline comment */
'''

comment.findall(text1)
#[' this is a comment ']
comment.findall(text2)
# []

##C스타일 주석을 찾아내지 못할 때, 패턴에 개행문 넣기*
comment = re.compile(r'/\*((?:.|\n)*?)\*/')
comment.findall(text2)
#[' this is a\n              multiline comment ']


#re.compile()함수에 "re.DOTALL플래그"
#정규 표현식의 점(.)이 개행문을 포함한 모든 문자에 매칭
EX2>
comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)
comment.findall(text2)
#[' this is a\n              multiline comment ']
#>>복잡한 패턴에는 정규 표현식 사용하기
===============================================================================





===============================================================================
#2.11 문자열에서 문자 잘라내기
#텍스트의 처음, 끝, 중간에서 원하지 않는 공백이나 문자 잘라내기
#"strip()" = 문자열의 처음과 끝에서 문자를 잘라낸다..
#"lstrip() = 왼쪽 문자" & "rstrip() = 오른쪽 문자"

EX1>
#공백 잘라내기
s = ' hello world \n'
s.strip()
#'hello world'
s.lstrip()
#'hello world \n'
s.rstrip()
#' hello world'

#문자 잘라내기
t = '-----hello====='
t.lstrip('-')
#'hello====='
t.strip('-=')
#'hello'

##s.strip()은 문자열에서 공백문을 없애거나 인용 부호를 삭제할 때,
## 그러나 텍스트의 중간에서 잘라내기X


EX2>
s = ' hello      world   \n'
s = s.strip()
s
#'hello      world'    #중간 공백문 사라지지 X


EX3>
#중간 공백문 없애기 = replace() 메소드/ 정규 표현식의 치환
s.replace(' ', '')
#'helloworld'

import re
re.sub('\s+', ' ', s)
#'hello world'


#데이터 읽어 들이기 + 문자열 잘라내기
EX4>
with open(filename) as f:
    lines = (line.strip() for line in f)    #데이터 변환
    for line in lines:
        ....
===============================================================================





===============================================================================
#2.12 텍스트 정리
#처리하기 어려운 텍스트 정리하기
#"str.upper()" & "str.lower()"
#"str.replace()" & "re.sub()" 치환 = 특정 문자 시퀀스를 없애기 / 바꾸기
#"str.translate()***

EX1>
s = 'pýtĥöñ\fis\tawesome\r\n'
s
#'pýtĥöñ\x0cis\tawesome\r\n'

remap = {
        ord('\t') : ' ',    #공백문 -> 띄어쓰기
        ord('\f') : ' ',    #공백문 -> 띄어쓰기
        ord('\r') : None    #복귀 코드 -> 삭제
        }
a = s.translate(remap)
a
#'pýtĥöñ is awesome\n'


EX1_1>
import unicodedata
import sys
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode)
                        if unicodedata.combining(chr(c)))
            #딕셔너리가 모든 유니코드 결합 문자 -> None 으로 매핑
b = unicodedata.normalize('NFD', a)    #unicodedata.normalize()으로 원본 입력문 노멀화
b
#'pýtĥöñ is awesome\n'
b.translate(cmb_chrs)   #변환함수로 결합문자 없애기
#'python is awesome\n'


EX2>
#유티코드 숫자 문자를 아스키 숫자에 매핑
digitmap = { c: ord('0') + unicodedata.digit(chr(c))
            for c in range(sys.maxunicode)
            if unicodedata.category(chr(c)) == 'Nd' }

len(digitmap)
#580???

#아라비아 숫자
x = '\u0661\u0662\u0663'
x.translate(digitmap)
#'123'


EX3>
#encode() / decode()를 사용한 잘라내기 / 변경하기
a
# 'pýtĥöñ is awesome\n'

b = unicodedata.normalize('NFD', a)     #노멀화 = 원본 텍스트를 개별적인 결합 문자로 나누기
b.encode('ascii', 'ignore').decode('ascii')     #아스키 인코딩/디코딩 = 문자들 한번에 폐기
#'python is awesome\n'
#>> 아스키 표현식만 얻으려 할 때


EX4>
#가장 빠른 치환 = str.replace()
def clean_spaces(s):
    s = s.replace('\r', '')
    s = s.replace('\t', ' ')
    s = s.replace('\f', ' ')
    return s
clean_spaces('abc\fde\tdfghi\r')
#'abc de dfghi'
===============================================================================






===============================================================================
# 2.13 텍스트 정렬
EX1>
text = 'Hello World'
text.ljust(20)
#'Hello World         '

text.rjust(20)
#'         Hello World'

text.center(20)
#'    Hello World     '


EX2>
#채워넣기
text.rjust(20,'=')
#'=========Hello World'

text.center(20,'*')
#'****Hello World*****'


EX3>
#format() 함수 [>.<.^]
format(text,'>20')
#'         Hello World'
format(text,'<20')
#'Hello World         '
format(text,'^20')
#'    Hello World     '


EX3_1>
format(text,'=>20s')
#'=========Hello World'
format(text,'*^20')
#'****Hello World*****'

EX3_2>
#format() 메소드 -> 서식화
'{:>10s} {:>10s}'.format('Hello', 'World')
#'     Hello      World'


EX3_3>
#format은 문자열뿐만 아니라 숫자 값 등 모든 값에 동작
x = 1.2345
format(x, '>10')
# '    1.2345'
format(x, '^10.2f')
#'   1.23   '
===============================================================================






===============================================================================
# 2,14 문자열 합치기
#작은 문자열 여러 개를 합쳐 하나의 긴 문자열 만들기
#합치려는 문자열이 시퀀스나 순환 객체 안에 있디면 "join()" 메소드가 가장 빠름

EX1>
parts = ['Is', 'Chicago', 'Not', 'Chicago?']
' '.join(parts)
#'Is Chicago Not Chicago?'

','.join(parts)
#'Is,Chicago,Not,Chicago?'

''.join(parts)
# 'IsChicagoNotChicago?'

##합치려 하는 객체의 수는 모를 때 구분 문자열을 지정하고 join 메소드


#"+"연산자로 합치지
EX2>
a = 'Is Chicago'
b = 'Not Chicago?'
a + ' ' + b
#'Is Chicago Not Chicago?'


EX3>
print('{} {}'.format(a,b))
#Is Chicago Not Chicago?

print(a + ' ' + b)
#Is Chicago Not Chicago?


#소스코드에서 문자열 합칠 때, "옆에 붙여 놓기"로 합치기 가능
EX4>
a = 'Hello' 'World'
a
#'HelloWorld'


## + 연산자로 많은 문자열 합치기X [새로운 문자열 객체 생성 -> 속도 느림]

##데이터를 문자열로 변환한 다음 생성차 표현식으로 합치기(1.19)
EX5>
data = ['ACME', 50, 91.1]
','.join(str(d) for d in data)
#'ACME,50,91.1'


#많고 짧은 문자열을 하나로 합쳐 문자열 만들기 = "yeild" 생성자 함수
#조각을 어떻게 합칠지 가정하지 않고 join()을 사용해서 합치기 가능
#또는 문자열을 입출력으로 리다이렉트 가능
===============================================================================





===============================================================================
# 2.15 문자열에 변수 사용
# 파이썬 문자열에 변수 값을 치환하는 간단한 방법은 X
# format() 메소드 사용하여 비숫하게 구현

EX1>
s = '{name} has {n} messages.'
s.format(name='Guido', n=37)
#'Guido has 37 messages.'


EX2>
#치환할 값이 변수에 들어 있다면 "format_map()" & "vars()"

name = 'Guido'
n = 37
s.format_map(vars())
#'Guido has 37 messages.'


EX2_1>
#vars()에는 인스턴스 사용 가능
class Info:
    def __init__(self, name, n):
        self.name = name
        self.n = n

a = Info('Guido',37)
s.format_map(vars(a))
#'Guido has 37 messages.'


#format() 과 format_map() 사용할 때 빠진 값이 있다면 제대로 작동X
# -> "__missing__"메소드가 있는 딕셔너리 클래스로 해결
EX3>
s.format(name='Guido')
#Traceback (most recent call last):
#  File "<ipython-input-82-dac1742a40f0>", line 1, in <module>
#    s.format(name='Guido')
#KeyError: 'n'
    
class safesub(dict):
    def __missing__(self, key):
        return '{' + key + '}'

del n   #n이 정이되지 않도록
s.format_map(safesub(vars()))
###########오류


EX4>
#코드에서 변수 치환을 빈번히 사용한다면
#치환하는 작업을 유틸리티 함수에 모아 놓기 "프레임 핵"
import sys
def sub(text):
    return text.format_map(sub(sys._getframe(1).f_locals))

name = 'Guido'
n = 37
print(sub('Hello {name}'))

print(sub('You have {n} messages.'))

print(sub('Your favorite color is {color}'))

##????

#  File "<ipython-input-87-55e30a477bda>", line 8, in <module>
#    print(sub('Hello {name}'))

#  File "<ipython-input-87-55e30a477bda>", line 3, in sub
#    return text.format_map(safesub(sys._getframe(1).f_locals))

#NameError: name 'safesub' is not defined
===============================================================================






===============================================================================
# 2.16 텍스트 열의 개수 고정
# 긴 문자열의 서식을 바꿔 열의 개수를 조절하기
# "textwrap 모듈"을 사용해서 텍스트를 재서식화
EX1>
s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."

import textwrap
print(textwrap.fill(s, 70))
#Look into my eyes, look into my eyes, the eyes, the eyes, the eyes,
#not around the eyes, don't look around the eyes, look into my eyes,
#you're under.

print(textwrap.fill(s, 40))
#Look into my eyes, look into my eyes,
#the eyes, the eyes, the eyes, not around
#the eyes, don't look around the eyes,
#look into my eyes, you're under.

print(textwrap.fill(s, 40, initial_indent=' '))
# Look into my eyes, look into my eyes,
#the eyes, the eyes, the eyes, not around
#the eyes, don't look around the eyes,
#look into my eyes, you're under.

print(textwrap.fill(s, 40, subsequent_indent=' '))
#Look into my eyes, look into my eyes,
# the eyes, the eyes, the eyes, not
# around the eyes, don't look around the
# eyes, look into my eyes, you're under.


##textwrap모듈은 특히 터미널에 사용할 텍스트에 적합
#터미널의 크기를 얻으려먼 "os.get_terminal_size()"
import os
os.get_terminal_size().columns
#OSError: [WinError 6] 핸들이 잘못되었습니다
===============================================================================