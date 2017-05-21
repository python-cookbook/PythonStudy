### 1.18 시퀀스 요소에 이름 매핑
# collections.namedtuple() : tuple 타입의 서브클래스를 반환하는 팩토리 메소드. 인스턴스화 가능한 클래스를 반환한다.
from collections import namedtuple

Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com', '2017-05-16')
print(sub)  # Subscriber(addr='jonesy@example.com', joined='2017-05-16')
print(sub.addr)  # jonesy@example.com
print(sub.joined)  # 2017-05-16
# namedtuple의 인스턴스는 튜플과 겨환이 가능하고, 인덱싱이나 언패킹과 같은 튜플의 기능들을 지원한다.
# print(len(sub)) # 2
addr, joined = sub
print(addr)  # jonesy@example.com
print(joined)  # 2017-05-16


# 네임드튜플은 주로 요소의 위치를 기반으로 구현되어 있는 코드를 분리한다. db 테이블에 새로운 열이 추가되는 경우 문제가 발생할 수 있다.
# but!! 반환된 튜플을 네임드 튜플로 변환했다면 이런 문제를 방지할 수 있다.
# 일반적인 튜플을 사용하는 코드
def conpute_cost(records):
    total = 0.0
    for rec in records:
        total += rec[1] * rec[2]
    return total


# 네임드 튜플을 사용하는 코드
from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price'])


def conpute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total


# namedtuple은 딕셔너리 대신 사용할 수 있으며 저장공간 측면에서 더 효율적이다. 하지만 딕셔너리와 달리 수정할 수 없다는 점!
s = Stock('ACME', 100, 123.45)
print(s)  # Stock(name='ACME', shares=100, price=123.45)
s.shares = 87  # AttributeError: can't set attribute
# 속성을 수정해야 할 경우 replace() 메소드를 사용해야 한다.
from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price'])


def conpute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total


s = Stock('ACME', 100, 123.45)
s = s._replace(shares=78)
print(s)  # Stock(name='ACME', shares=78, price=123.45)
# _replace 메소드를 사용하면 옵션이나 빈 필드를 가진 네임드 튜플을 간단히 만들 수 있다.
from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price', 'date', 'time'])
# 프로토 타입 인스턴스 생성
stock_prototype = Stock('', 0, 0.0, None, None)


# 딕셔너리를 stock으로 변환하는 함수
def dict_to_stock(s):
    return stock_prototype._replace(**s)


# 이 코드를 사용하는 예는 다음과 같다.
a = {'name': 'ACME', 'shares': 78, 'price': 123.45}
# print(dict_to_stock(a))  # Stock(name='ACME', shares=78, price=123.45, date=None, time=None)
b = {'name': 'ACME', 'shares': 100, 'price': 123.45, 'date': 12 / 13 / 2013}
# print(dict_to_stock(b)) #Stock(name='ACME', shares=100, price=123.45, date=0.00045855783560701593, time=None)
### 1.19. 데이터를 변환하면서 줄이기
# 문제 : 감소함수(sum(), min(), max()) 를 실행해야 하는데, 먼저 데이터를 변환하거나 필터링해야 한다
# 데이터를 줄이면서 변형하는 가장 우아한 방식은 생성자 표현식을 사용하는 것이다. 예를 들어 정사각형 넓이의 합을 계산하려면,
nums = [1, 2, 3, 4, 5]
s = sum(x * x for x in nums)
print(s)  # 55
## 대안으로 다음과 같은 코드도 가능하다
# 디렉토리에 또 다른 .py 파일이 있는지 살펴본다.
import os

files = os.listdir('dirname')
if any(name.endswith('.py') for name in files):
    print('There be python!')
else:
    print('Sorry, no python')
# 튜플을 csv로 출력한다.
s = ('ACME', 50, 123.45)
print(','.join(str(x) for x in s))  # ACME,50,123.45
# 자료 구조의 필드를 줄인다.
portfolio = [
    {'name': 'GOOG', 'shares': 50},
    {'name': 'YHOO', 'shares': 75},
    {'name': 'AOL', 'shares': 20},
    {'name': 'SCOX', 'shares': 65}
]
min_shares = min(s['shares'] for s in portfolio)
print(min_shares)  # 20
s = sum((x * x for x in nums))  # 생성자 표현식을 인자로 전달
s = sum(x * x for x in nums)  # 더 우아한 방식
nums = [1, 2, 3, 4, 5]
s = sum([x * x for x in nums])
print(s)  # 55
# 물론 이 코드도 동작하지만 추가적인 리스트를 생성해야 한다는 번거로움이 있다.
# nums 크기가 방대해지만 한 번 쓰고 버릴 임시 리스트의 크기도 커진다는 단점이 있다.
# 생성자를 사용하면 데이터를 순환 가능하게 변형하므로 메모리 측면에서 훨씬 유리함.
portfolio = [
    {'name': 'GOOG', 'shares': 50},
    {'name': 'YHOO', 'shares': 75},
    {'name': 'AOL', 'shares': 20},
    {'name': 'SCOX', 'shares': 65}
]
# 원본 : 20
# min_shares = min(s['shares'] for s in portfolio)
# 대안 : {'name': 'AOL', 'shares': 20}
min_shares = min(portfolio, key=lambda s: s['shares'])
print(min_shares)
# 1.20 여러 매핑을 단일 매핑으로 합치기!!
# 문제 : 딕셔너리나 매핑이 여러개 있고, 자료 검색이나 데이터 확인을 위해서 하나의 매핑으로 합치고 싶다면??
# 다음과 같은 두 딕셔너리가 있다고 가정해보자.
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
# 두 딕셔너리에 모두 검색을 해야 할 상황이라면?(a에서 데이터 검색 후 b 에서 데이터 검색)
from collections import ChainMap

c = ChainMap(a, b)
print(c['x'])  # Outputs 1 (from a)
print(c['y'])  # Outputs 2 (from b)
print(c['z'])  # Outputs 3 (from a)
# ChainMap 은 매핑을 여러 개 받아서 하나처럼 보이게 만든다. but 하나로 합쳐진 것은 아니다. 매핑에 대한 리스트를 유지하면서 리스트를 스캔하는 것
print(len(c))  # Outputs 3
print(list(c.keys()))  # Outputs ['x', 'z', 'y']
# 중복 키가 있으면 첫번째 매핑의 값을 사용함. 따라서 예제의 c['z'] 는 항상 a 의 값을 참조하며 b의 값은 참조하지 않음.
# 매핑의 값을 변경하는 동작은 언제나 리스트의 첫 번째 매핑에 영향을 준다.
c['z'] = 10
c['w'] = 40
del c['x']
print(a)  # {'z': 10, 'w': 40}
del c['y']  # KeyError: "Key not found in the first mapping: 'y'"
# 체인 맵은 변수와 같이 범위가 있는 값에 사용하면 유용하다. 이 동작을 쉽게 만들어주는 메소드는 아래와 같다
from collections import ChainMap

values = ChainMap()
values['x'] = 1
# 새로운 매핑 추가
values = values.new_child()
values['x'] = 2
# 새로운 매핑 추가
values = values.new_child()
values['x'] = 3
print(values)  # ChainMap({'x': 3}, {'x': 2}, {'x': 1})
print(values['x'])  # 3
# 마지막 매핑 삭제
values = values.parents
print(values['x'])  # 2
# 마지막 매핑 삭제
values = values.parents
print(values['x'])  # 1
print(values)  # ChainMap({'x': 1})
# 체인 맵의 대안으로 update()를 사용해 딕셔너리를 하나로 합칠 수도 있다.
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
merged = dict(b)
merged.update(a)
print(merged['x'])  # 1
print(merged['y'])  # 2
print(merged['z'])  # 3
# 이렇게 해도 잘 동작하지만, 완전히 별개의 딕셔너리 객체를 만들거나 기존 딕셔너리의 내용을 변경해야 한다.
a['x'] = 13
print(merged['x'])  # 1
# chainMap은 원본 딕셔너리를 참조하기 때문에 그와 같은 문제가 발생하지 않는다.
from collections import ChainMap

a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
merged = ChainMap(a, b)
print(merged['x'])  # 1
a['x'] = 42
print(merged['x'])  # 42 # 합친 딕셔너리에 변경 알림
########  CHAPTER2  문자열과 텍스트  ########
# 문자열 나누기, 검색, 빼기, 렉싱, 파싱과 같이 텍스트 처리와 관련있는 일반적인 문제에 초점을 맞춘다.

# 2.1 여러 구분자로 문자열 나누기
# re.split() 메소드 사용하기
line = 'asdf fjdk; afed, fjek,asdf, foo'
import re

print(re.split(r'[;,\s]\s*', line))  # ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# re.split() 함수는 분리 구문마다 여러 개의 패턴을 명시할 수 있다는 점이 유리하다.
# 위의 코드에서는 쉼표(,) 세미콜론(;) 공백문자, 하나이상의 공백문자를 모두 분리 구문으로 사용했다.
# 결과는 리스트 형태로 반환된다.
# 캡처 그룹(capture group) 을 사용하면, 매칭된 텍스트에도 결과가 포함된다.

fields = re.split(r'(;|,|\s)\s*', line)
# print(fields)  # ['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo']
# 구분 문자만 추출해야 할 필요도 있다.
values = fields[::2]
delimiters = fields[1::2] + ['']
# print(values) #['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
# print(delimiters) # [' ', ';', ',', ',', ',', '']

# 동일한 구분자로 라인을 구성한다.
print(''.join(v + d for v, d in zip(values, delimiters)))  # asdf fjdk;afed,fjek,asdf,foo
# 분리 구문을 결과에 포함시키고 싶지 않지만 정규 표현식에 괄호를 사용해야 한다면
# 논캡쳐 그룹을 사용해야 한다.

print(re.split(r'(?:,|;|\s)\s*', line))  # ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

### 2.2 문자열 처음이나 마지막에 텍스트 매칭

# 문자열의 처음 또는 마지막에 패턴이 포함되었는지 확인하는 방법 - str.startswith() / str.endswith() 메소드
filename = 'spam.txt'
print(filename.endswith('.txt'))  # True
print(filename.startswith('file:'))  # False
url = 'http://www.python.org'
print(url.startswith('http:'))  # True
# 여러개의 선택지를 검사해야 할때 검사하고 싶은 값을 튜플에 담아서 startswith() 이나 endswith() 에 전달한다.
import os

filenames = os.listdir('.')
print(filenames)  # ['cookbook_02.py', '__init__.py']
print([name for name in filenames if name.endswith(('.c', '.h'))])  # []
print(any(name.endswith('.py') for name in filenames))  # True
# 또 다른 예제
from urllib.request import urlopen


def read_data(name):
    if name.startswith(('http:', 'https:', 'ftp:')):
        return urlopen(name).read()
    else:
        with open(name) as f:
            return f.read()

# 튜플만을 입력으로 받기 때문에, 입력 값을 리스트나 세트로 가지고 있다면 tuple()을 이용해서 먼저 변환해 주어야 함
choices = ['http:', 'ftp:']
url = 'http://www.python.org'
print(url.startswith(choices))  # Traceback (most recent call last): File "<stdin>", line 1, in <module>

# TypeError: startswith first arg must be str or a tuple of str, not list
print(url.startswith(tuple(choices)))
# True

# startswith() , endswith() 메소드는 접두어와 접미어를 검사할 때 매우 유용하다
# slice() 를 사용하면 비슷한 동작을 할 수 있지만 코드의 가독성이 많이 떨어진다.

filename = 'spam.txt'
print(filename[-4:] == '.txt')  # True
url = 'http://www.python.org'
print(url[:5] == 'http:' or url[:6] == 'https:' or url[:4] == 'ftp:')  # True

# 다음과 같이 정규 표현식을 사용해도 된다.

import re

url = 'http://www.python.org'
print(re.match('http:|https:|ftp:', url))
# output : <_sre.SRE_Match object; span=(0, 5), match='http:'>


if any(name.endswith(('.c', '.h')) for name in listdir(dirname)):
    ...
# 2.3 쉘 와일드카드 패턴으로 문자열 매칭

from fnmatch import fnmatch, fnmatchcase

a = fnmatch('foo.txt', '*.txt')  # True
b = fnmatch('foo.txt', '?oo.txt')  # True
c = fnmatch('Dat45.csv', 'Dat[0-9]*')  # True
names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']
d = [name for name in names if fnmatch(name, 'Dat*.csv')]  # ['Dat1.csv', 'Dat2.csv']
print(a)  # True
print(b)  # True
print(c)  # True
print(d)  # ['Dat1.csv', 'Dat2.csv']

from fnmatch import fnmatch, fnmatchcase

print(fnmatch('foo.txt', '*.TXT'))  # true
# 이런 차이점이 별로라면 fnmatchcase()를 사용한다. 이 메소드는 지정한 소문자 또는 대문자에 정확히 일치하는 값만 찾아낸다.
from fnmatch import fnmatch, fnmatchcase

print(fnmatchcase('foo.txt', '*.TXT'))  # False

addresses = [
    '5412 N CLARK ST',
    '1060 W ADDISON ST',
    '1039 W GRANVILLE AVE',
    '2122 N CLARK ST',
    '4802 N BROADWAY',
]
# 다음과 같이 리스트 컴프리헨션을 사용할 수 있다.
from fnmatch import fnmatchcase

print([addr for addr in addresses if
       fnmatchcase(addr, '* ST')])  # ['5412 N CLARK ST', '1060 W ADDISON ST', '2122 N CLARK ST']
print([addr for addr in addresses if fnmatchcase(addr, '54[0-9][0-9] *CLARK*')])  # ['5412 N CLARK ST']

# 정규 표현식을 할 때 간단한 와일드카드를 사용할 생각이라면 이 함수를 쓰도록 하자!

# 2.4 텍스트 패턴 매칭과 검색

text = 'yeah, but no, but yeah, but no, but yeah'

# 정확한 매칭

print(text == 'yeah')  # False

# 처음이나 끝에 매칭

text.startswith('yeah')  # True
text.endswith('no')  # False

# 처음나타난 곳 검색

print(text.find('no'))  # 10

# 동일한 패턴으로 매칭을 많이 수행할 예정이라면 정규 표현식을 미리 컴파일해서 패턴 객체로 만들어 둔다.

text1 = '11/27/2012'
text2 = 'Nov 27, 2012'
import re

if re.match(r'\d+/\d+/\d+', text1):
    print('yes')
else:
    print('no')

    # yes
if re.match(r'\d+/\d+/\d+', text2):
    print('yes')
else:
    print('no')

    # no
text = 'Today is 11/27/2'
print(datepat.findall(text))  # ['11/27/2012', '3/13/2013']
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')

m = datepat.match('11/27/2012')
print(m)
# <_sre.SRE_Match object at 0x1005d2750>
m.group(0)  # '11/27/2012'
m.group(1)  # '11'
m.group(2)  # '27'
m.group(3)  # '2012'
m.groups()  # ('11', '27', '2012')
month, day, year = m.groups()
print(text)
#'Today is 11/27/2012. PyCon starts 3/13/2013.'
print(datepat.findall(text))
# [('11', '27', '2012'), ('3', '13', '2013')]
for month, day, year in datepat.findall(text):
    print('{}-{}-{}'.format(year, month, day))
# 2012-11-27
# 2013-3-13

 2.5 텍스트 검색과 치환
text = 'yeah, but no, but yeah, but no, but yeah'
print(text.replace('yeah', 'yep'))  # yep, but no, but yep, but no, but yep

text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
import re

print(re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text))  # 'Today is 2012-11-27. PyCon starts 2013-3-13.'
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
import re

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
print(datepat.sub(r'\3-\1-\2', text))


from calendar import month_abbr

def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))


print(datepat.sub(change_date, text))
# 'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'
newtext, n = datepat.subn(r'\3-\1-\2', text)
print(newtext)  # 'Today is 2012-11-27. PyCon starts 2013-3-13.'
print(n)  # 2

# 2.6 대소문자를 구별하지 않는 검색과 치환
import re

text = 'UPPER PYTHON, lower python, Mixed Python'
a = re.findall('python', text, flags=re.IGNORECASE)
print(a)  # ['PYTHON', 'python', 'Python']
b = re.sub('python', 'snake', text, flags=re.IGNORECASE)
print(b)  # 'UPPER snake, lower snake, Mixed snake'

# 치환된 텍스트의 대소문자와 원본의 대소문자와 일치하려면??
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

# UPPER snake, lower snake, Mixed snake
# 2.7 가장 짧은 매칭을 위한 정규 표현식

str_pat = re.compile(r'\"(.*)\"')
text1 = 'Computer says "no."'
a = str_pat.findall(text1)
print(a)  # ['no.']
text2 = 'Computer says "no." Phone says "yes."'
b = str_pat.findall(text2)
print(b)  # ['no." Phone says "yes.']
import re

text2 = 'Computer says "no." Phone says "yes."'
str_pat = re.compile(r'\"(.*?)\"')
a = str_pat.findall(text2)
print(a)  # ['no.', 'yes.']

# 2.8 여러 줄에 걸친 정규 표현식 사용

comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = /* this is a
           multiline comment */
a= comment.findall(text1)
print(a)  #[' this is a comment ']
b = comment.findall(text2)
print(b) #[]
#  2.9 유니코드 텍스트 노멀화
s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'
print(s1)
#'Spicy Jalapeño'
print(s2)
#'Spicy Jalapeño'
print(s1 == s2)  # False
print(len(s1))  # 14
print(len(s2))  # 15

s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'
import unicodedata

t1 = unicodedata.normalize('NFC', s1)
t2 = unicodedata.normalize('NFC', s2)
print(t1 == t2)  # True
print(ascii(t1))  # 'Spicy Jalape\xf1o'
t3 = unicodedata.normalize('NFD', s1)
t4 = unicodedata.normalize('NFD', s2)
print(t3 == t4)  # True
print(ascii(t3))  # 'Spicy Jalapen\u0303o'
# normalize() 의 첫번쨰 인자에는 문자열을 어떻게 노멀화할 것인지를 지정한다.
s = '\ufb01'  # A single character
print(s)  # 'ﬁ'
print(unicodedata.normalize('NFD', s))  # 'ﬁ'
# 합쳐놓은 문자가 어떻게 분리되는지 살펴보자.
print(unicodedata.normalize('NFKD', s))  # 'fi'
print(unicodedata.normalize('NFKC', s))  # 'fi'
# 텍스트에서 발음 구별부호를 모두 제거하고 싶다면 다음과 같이 해야 한다.
t1 = unicodedata.normalize('NFD', s1)
a = ''.join(c for c in t1 if not unicodedata.combining(c))
print(a)  # 'Spicy Jalapeno'
#  2.10 정규 표현식에 유니코드 사용
import re

num = re.compile('\d+')
# ASCII digits
num.match('123')  # <_sre.SRE_Match object at 0x1007d9ed0>
# Arabic digits
num.match('\u0661\u0662\u0663')  # <_sre.SRE_Match object at 0x101234030>
pat = re.compile('stra\u00dfe', re.IGNORECASE)
s = 'straße'
pat.match(s)  # Matches
# <_sre.SRE_Match object at 0x10069d370>
pat.match(s.upper())  # Doesn't match
s.upper()  # Case folds
#'STRASSE'
#  2.11 문자열에서 문자 잘라내기
# strip() 메소드 :  처음과 끝에서 문자를 잘라낼 수 있다.

s = ' hello world \n'
s.strip()
# 'hello world'
s.lstrip()
# 'hello world \n'
s.rstrip()
#' hello world'
t = '-----hello====='
t.lstrip('-')
# 'hello====='
t.strip('-=')
# 'hello'
s = ' hello     world \n'
s = s.strip()
print(s)  # 'hello     world'
s.replace(' ', '')  # 'helloworld'
import re

re.sub('\s+', ' ', s)  # 'hello world'

# 2.12  텍스트 정리

s = 'python\fis\tawesome\r\n'
print(s)  # python is	awesome
# 우선 문자열에서 공백문을 잘라내보자. 이를 위해 작은 변환 테이블을 만들어 놓고 translate()을 사용한다.
remap = {
    ord('\t'): ' ',
    ord('\f'): ' ',
    ord('\r'): None  # Deleted
}
a = s.translate(remap)
print(a)
# python is awesome\n'

import unicodedata
import sys

cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode)
                         if unicodedata.combining(chr(c)))
b = unicodedata.normalize('NFD', a)
print(b)
# python is awesome\n'
b.translate(cmb_chrs)
# 'python is awesome\n'
# dict.fromkeys() 를 사용한 예

import unicodedata
import sys

digitmap = {c: ord('0') + unicodedata.digit(chr(c))
            for c in range(sys.maxunicode)
            if unicodedata.category(chr(c)) == 'Nd'}
print(len(digitmap))  # 580
x = '\u0661\u0662\u0663'
print(x.translate(digitmap))  # '123
# I/O 인코딩, 디코딩 함수 사용해서 텍스트 정리하기
print(a)  #python is awesome\n'
b = unicodedata.normalize('NFD', a)
b.encode('ascii', 'ignore').decode('ascii')  # 'python is awesome\n'


#  2.13 텍스트 정렬

# ljust(), rjust(), center()
text = 'Hello World'
print(text.ljust(20))
# 'Hello World         '
print(text.rjust(20))
# '         Hello World'
print(text.center(20))
# '    Hello World     '

print(text.rjust(20, '='))
# '=========Hello World'
print(text.center(20, '*'))
#'****Hello World*****'
#format 함수를 사용할 수도 있다.
format(text, '>20')
'         Hello World'
format(text, '<20')
'Hello World         '
format(text, '^20')
'    Hello World     '
# 공백대신 특정 문자를 채워넣고 싶다면 이렇게
format(text, '=>20s')
# '=========Hello World'
format(text, '*^20s')
# '****Hello World*****'


#2.14 문자열 합치기
#join() 메소드를 사용한다.
parts = ['Is', 'Chicago', 'Not', 'Chicago?']
print(' '.join(parts))  # 'Is Chicago Not Chicago?'
print(','.join(parts))  # 'Is,Chicago,Not,Chicago?'
print(''.join(parts))  # 'IsChicagoNotChicago?'
# + 를 사용
a = 'Is Chicago'
b = 'Not Chicago?'
print(a + ' ' + b)
#'Is Chicago Not Chicago?'
#+ 연산자는 좀 더 복잡한 문자열 서식 연산에 사용해도 동작한다.
print('{} {}'.format(a, b))
#Is Chicago Not Chicago?
print(a + ' ' + b)
#Is Chicago Not Chicago?
a = 'Hello' 'World'
print(a)  # 'HelloWorld'


# 2.15 문자열에 변수 사용
#format() 메소드를 사용함녀 비슷하게 흉내낼 수 있다.
s = '{name} has {n} messages.'
a = s.format(name='Guido', n=37)
print(a)
#'Guido has 37 messages.'
name = 'Guido'
n = 37
b = s.format_map(vars())
print(b)

# 'Guido has 37 messages.'
class Info:
    def __init__(self, name, n):
        self.name = name
        self.n = n

a = Info('Guido', 37)
b = s.format_map(vars(a))
print(b)
#'Guido has 37 messages.'
s.format(name='Guido')
#Traceback (most recent call last):
#File "<stdin>", line 1, in <module>
#KeyError: 'n'

#이 문제는 __missing__() 메소드가 있는 딕셔너리 클래스를 정의해서 피할 수 있다.
del n  # n 이 정의되지 않도록 한다.
s.format_map(safesub(vars()))
import sys

def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))

name = 'Guido'
n = 37
print(sub('Hello {name}'))
# Hello Guido
print(sub('You have {n} messages.'))
# You have 37 messages.
print(sub('Your favorite color is {color}'))
#Your favorite color is {color}

#2.16. 텍스트의 열의 개수 고정

s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."

import textwrap

print(textwrap.fill(s, 70))
# Look into my eyes, look into my eyes, the eyes, the eyes, the eyes,
# not around the eyes, don't look around the eyes, look into my eyes,
# you're under.

print(textwrap.fill(s, 40))
# Look into my eyes, look into my eyes,
# the eyes, the eyes, the eyes, not around
# the eyes, don't look around the eyes,
# look into my eyes, you're under.

print(textwrap.fill(s, 40, initial_indent='    '))
#    Look into my eyes, look into my
# eyes, the eyes, the eyes, the eyes, not
# around the eyes, don't look around the
# 3eyes, look into my eyes, you're under.

print(textwrap.fill(s, 40, subsequent_indent='    '))
# Look into my eyes, look into my eyes,
# the eyes, the eyes, the eyes, not
# around the eyes, don't look around
# the eyes, look into my eyes, you're
# under.
