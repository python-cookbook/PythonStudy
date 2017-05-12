#  1.18 시퀀스 요소에 이름 매핑
#  ▣ 문제 : 리스트나 튜플의 요소에 이름으로 접근 가능하도록 수정하고 싶다.
#  ▣ 해결 : collections.namedtuple() 을 사용하면 일반적인 튜플 객체를 사용하는 것에 비해 그리 크지 않은 오버헤드로 이 기능을 구현한다.
#            collections.namedtuple() 은 실제로 표준 파이썬 tuple 타입의 서브클래스를 반환하는 팩토리 메소드이다.
from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com', '2012-10-19')
print(sub)
print(sub.addr, sub.joined)

#   - namedtuple 의 인스턴스는 일반적인 클래스 인스턴스와 비슷해 보이지만 튜플과 교환이 가능하고, 인덱싱이나 언패킹과 같은 튜플의
#     일반적인 기능을 모두 지원한다.
print(len(sub))
addr, joined = sub  # 언패킹
print(addr, joined)

#   - 일반적인 튜플을 사용하는 코드
def compute_cost(records):
    total = 0.0
    for rec in records:
        total += rec[1] * rec[2]
    return total

#   - namedtuple 을 사용한 코드
from collections import namedtuple
Stock = namedtuple('Stock', ['name', 'shares', 'price'])
def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total

#  ▣ 토론 : namedtuple 은 저장 공간을 더 필요로 하는 딕셔너리 대신 사용할 수 있다.
#            딕셔너리를 포함한 방대한 자료 구조를 구상하고 있다면 namedtuple 을 사용하는 것이 더 효율적이다.
#            하지만 딕셔너리와는 다르게 네임드 튜플은 수정할 수 없다.
s = Stock('ACME', 100, 123.45)
print(s)
s.shares = 75

#   - 속성을 수정해야 한다면 namedtuple 인스턴스의 _replace() 메소드를 사용해야 한다.
s = s._replace(shares=75)
print(s)

#   - _replace() 메소드를 사용해서 옵션이나 빈 필드를 가진 네임드 튜플을 간단히 만들 수 있다.
from collections import namedtuple
Stock = namedtuple('Stock', ['name', 'shares', 'price', 'date', 'time'])

stock_prototype = Stock('', 0, 0.0, None, None)  # prototype instance 생성

def dict_to_stock(s):  # dictionary 를 Stock 으로 변환하는 함수
    return stock_prototype._replace(**s)

a = {'name': 'ACME', 'shares': 100, 'date': '2012-02-22'}
print(dict_to_stock(a))


#  1.19 데이터를 변환하면서 줄이기
#  ▣ 문제 : 감소 함수(sum, min, max)를 실행해야 하는데, 먼저 데이터를 변환하거나 필터링해야 한다.
#  ▣ 해결 : 생성자 표현식을 사용해서 처리한다.
nums = [1, 2, 3, 4, 5]
s = sum(x * x for x in nums)
print(s)

#   - 디렉터리에 또 다른 .py 파일이 있는지 살펴본다.
import os
files = os.listdir('./files')
if any(name.endswith('.py') for name in files):
    print('There be python!')
else:
    print('Sorry, no python.')

#   - 튜플을 CSV 로 출력한다.
s = ('ACME', 50, 123.45)
print(','.join(str(x) for x in s))

#   - 자료 구조의 필드를 줄인다.
portfolio = [{'name': 'GOOG', 'shares': 50},
             {'name': 'YHOO', 'shares': 75},
             {'name': 'AOL', 'shares': 20},
             {'name': 'SCOX', 'shares': 65}]
min_shares = min(s['shares'] for s in portfolio)

#  ▣ 토론 : 위의 코드는 함수에 인자로 전달된 생성자 표현식의 문법적인 측면을 보여준다.
s = sum((x * x for x in nums))
s = sum(x * x for x in nums)
#   ※ 위의 두 식은 같다.

#   - min, max 같은 함수는 key 라는 여러 상황에 유용한 인자를 받기 때문에 생성자 방식을 사용해야 하는 이유를 더 만들어 준다.
min_shares = min(s['shares'] for s in portfolio)
min_shares = min(portfolio, key=lambda v: v['shares'])
from operator import itemgetter
min_shares = min(portfolio, key=itemgetter('shares'))
print(min_shares)


#  1.20 여러 매핑을 단일 매핑으로 합치기
#  ▣ 문제 : 딕셔너리나 매핑이 여러 개 있고, 자료 검색이나 데이터 확인을 위해서 하나의 매핑으로 합치고 싶다.
#  ▣ 해결 : collections 모듈의 ChainMap 클래스를 사용하면 된다.
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
from collections import ChainMap
c = ChainMap(a, b)
print(c)
print(c['x'])
print(c['y'])
print(c['z'])

#  ▣ 토론 : ChainMap 은 매핑을 여러 개 받아서 하나처럼 보이게 한다.
#            하지만 그렇게 보이는 것일뿐 하나로 합치는 것은 아니다. 단지 매핑에 대한 리스트를 유지하면서 리스트를 스캔하도록
#            일반적인 딕셔너리 동작을 재정의한다.
print(len(c))
print(list(c.keys()), list(c.values()))

#   - 매핑의 값을 변경하는 동작은 언제나 리스트의 첫 번째 매핑에 영향을 준다
c['z'] = 10
c['w'] = 40
del c['z']
print(a)
del c['y']  # 두 번째 매핑에 있는 값이므로 변경이 안된다.

#   - ChainMap 은 프로그래밍 언어의 변수와 같이 범위가 있는 값(전역변수, 지역변수)에 사용하면 유용하다.
values = ChainMap()
values['x'] = 1
values = values.new_child()  # 새로운 매핑 추가
values['x'] = 2
values = values.new_child()
values['x'] = 3
print(values)
print(values['x'])
values = values.parents  # 마지막 매핑 삭제
print(values['x'])
values = values.parents
print(values['x'])
print(values)

#   - ChainMap 의 대안으로 update() 를 사용해 딕셔너리를 하나로 합칠 수도 있다.
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
merged = dict(b)
merged.update(a)
print(merged['x'], merged['y'], merged['z'])
a['x'] = 13
print(merged['x'])

#   - ChainMap 은 원본 딕셔너리를 참조하기 때문에 이와 같은 문제가 발생하지 않는다.
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
merged = ChainMap(a, b)
print(merged['x'])
a['x'] = 42
print(merged['x'])


# Chapter 2. 문자열과 텍스트
#  2.1 여러 구분자로 문자열 나누기
#  ▣ 문제 : 문자열을 필드로 나누고 싶지만 구분자가 문자열에 일관적이지 않다.
#  ▣ 해결 : 문자열 객체의 split() 메소드는 아주 간단한 상황에 사용하도록 설계되었고 여러 개의 구분자나 구분자 주변의
#            공백까지 고려하지는 않는다. 좀 더 유연해져야 할 필요가 있다면 re.split() 메소드를 사용한다.
line = 'asdf fjdk; afed,  fjek,asdf,      foo'
import re
print(re.split(r'[;,\s]\s*', line))

#  ▣ 토론 : re.split() 함수는 분리 구문마다 여러 패턴을 명시할 수 있다는 점이 유리하다.
#   - re.split() 을 사용할 때는 괄호 안에 묶인 정규 표현식 패턴이 캡처 그룹이 된다.
fields = re.split(r'(;|,|\s)\s*', line)
print(fields)

#   - 구분 문자만 출력하는 경우.
values = fields[::2]
delimiters = fields[1::2] + ['']
print(values, delimiters)

#   - 동일한 구분자로 라인을 구성한다.
print(''.join(v+d for v, d in zip(values, delimiters)))

#   - 분리 구문을 결과에 포함시키고 싶지 않지만 정규 표현식에 괄호를 사용해야 할 필요가 있다면 논캡처 그룹을 사용한다.
print(re.split('(?:,|;|\s)\s*', line))


#  2.2 문자열 처음이나 마지막에 텍스트 매칭
#  ▣ 문제 : 문자열의 처음이나 마지막에 파일 확장자, URL scheme 등 특정 텍스트 패턴이 포함되었는지 검사하고 싶다.
#  ▣ 해결 : 문자열의 처음이나 마지막에 패턴이 포함되었는지 확인하는 간단한 방법으로 str.startswith() 나 str.endswith() 메소드가 있다.
filename = 'spam.txt'
print(filename.endswith('.txt'))
print(filename.startswith('file:'))
url = 'http://www.python.org'
print(url.startswith('http:'))

#   - 여러 개의 선택지를 검사해야 한다면 검사하고 싶은 값을 튜플에 담아 startswith() 나 endswith() 에 전달한다.
import os
filenames = os.listdir('.')
print(filenames)
print([name for name in filenames if name.endswith(('.c', '.h'))])

from urllib.request import urlopen

def read_data(name):
    if name.startswith(('http:', 'https:', 'ftp:')):
        return urlopen(name).read()
    else:
        with open(name) as f:
            return f.read()

#   - startswith() 메소드는 튜플만을 입력으로 받는다.
choices = ['http:', 'ftp:']
url = 'http://www.python.org'
url.startswith(choices)
url.startswith(tuple(choices))

#  ▣ 토론 : startswith() 와 endswith() 메소드는 접두어와 접미어를 검사할 때 매우 편리하다.
#            슬라이스를 사용하면 비슷한 동작을 할 수 있지만 코드의 가독성이 많이 떨어진다.
filename = 'spam.txt'
print(filename[-4:] == '.txt')
url = 'http://www.python.org'
print(url[:5] == 'http:' or url[:6] == 'https:' or url[:4] == 'ftp:')

#   - 정규 표현식을 사용해도 된다.
import re
url = 'http://www.python.org'
print(re.match('http:|https:|ftp:', url))

#   - startswith() 와 endswith() 메소드는 일반적인 데이터 감소와 같은 다른 동작에 함께 사용하기에도 좋다.
if any(name.endswith(('.c', '.h')) for name in os.listdir('.')):
    pass


#  2.3 쉘 와일드카드 패턴으로 문자열 매칭
#  ▣ 문제 : Unix 쉘에 사용하는 것과 동일한 와일드카드 패턴을 텍스트 매칭에 사용하고 싶다.(예: *.py, Dat[0-9]*.csv 등)
#  ▣ 해결 : fnmatch 모듈에 두 함수 fnmatch() 와 fnmatchcase() 를 사용하면 된다.
from fnmatch import fnmatch, fnmatchcase
print(fnmatch('foo.txt', '*.txt'))
print(fnmatch('foo.txt', '?oo.txt'))
print(fnmatch('Dat45.csv', 'Dat[0-9]*'))
names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']
print([name for name in names if fnmatch(name, 'Dat*.csv')])

#   - 일반적으로 fnmatch() 는 시스템의 파일 시스템과 동일한 대소문자 구문 규칙을 따른다.
print(fnmatch('foo.txt', '*.TXT'))  # Mac    : True
print(fnmatch('foo.txt', '*.TXT'))  # window : True

#   - 이런 차이점이 없는 것을 사용하려면 fnmatchcase() 를 사용한다.
print(fnmatchcase('foo.txt', '*.TXT'))

#   - 파일 이름이 아닌 데이터 프로세싱에도 사용할 수 있다.
addresses = ['5412 N CLARK ST',
             '1060 W ADDISON ST',
             '1039 W GRANVILLE AVE',
             '2122 N CLARK ST',
             '4802 N BROADWAY']
from fnmatch import fnmatchcase
print([addr for addr in addresses if fnmatchcase(addr, '* ST')])
print([addr for addr in addresses if fnmatchcase(addr, '54[0-9][0-9] *CLARK*')])

#  ▣ 토론 : fnmatch 가 수행하는 매칭은 간단한 문자열 메소드의 기능과 정규 표현식의 중간쯤 위치하고 있다.
#           데이터 프로세싱을 할 때 간단한 와일드카드를 사용할 생각이라면 이 함수를 사용하는 것이 괜찮은 선택이다.


#  2.4 텍스트 패턴 매칭과 검색
#  ▣ 문제 : 특정 패턴에 대한 텍스트 매칭이나 검색을 하고 싶다.
#  ▣ 해결 : 매칭하려는 텍스트가 간단하다면 str.find(), str.endswith(), str.startswith() 와 같은 기본적인 문자열 메소드만으로도
#           충분하다.
text = 'yeah, but no, but yeah, but no, but yeah'

#   - 정확한 매칭
print(text == 'yeah')

#   - 처음이나 끝에 매칭
print(text.startswith('yeah'))
print(text.endswith('no'))

#   - 처음 나타난 곳 검색
print(text.find('no'))  # 해당 값이 처음 나온 인덱스를 리턴.

#   - 좀 더 복잡한 매칭을 위해 정규 표현식과 re 모듈을 사용한다.
#     match() : 항상 문자열 처음에서 찾기를 시도.
#     findall() : 텍스트 전체에 걸쳐 찾기를 시도.
text1 = '11/27/2012'
text2 = 'Nov 27, 2012'

import re
#   - 간단한 매칭: \d+는 하나 이상의 숫자를 의미
if re.match(r'\d+/\d+/\d+', text1):
    print('yes')
else:
    print('no')

if re.match(r'\d+/\d+/\d+', text2):
    print('yes')
else:
    print('no')

#   - 동일한 패턴으로 매칭을 많이 수행할 예정이라면 정규 표현식을 미리 컴파일해서 패턴 객체로 만들어 놓는다.
datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')

if datepat.match(text2):
    print('yes')
else:
    print('no')

#   - 텍스트 전체에 걸쳐 패턴을 찾으려면 findall() 메소드를 사용한다.
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
print(datepat.findall(text))

#   - 정규 표현식을 정의할 때 괄호를 사용해 캡처 그룹을 만드는 것이 일반적이다.
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
m = datepat.match('11/27/2012')
print(m.group(0), m.group(1), m.group(2), m.group(3), m.groups())  # 그룹별로 출력 가능 (0 은 전체 출력)
month, day, year = m.groups()
for month, day, year in datepat.findall(text):
    print('{}-{}-{}'.format(year, month, day))

#   - 한 번에 결과를 얻지 않고 텍스트를 순환하며 찾으려면 finditer() 를 사용한다.
for m in datepat.finditer(text):
    print(m.groups())

#  ▣ 토론 : 핵심이 되는 기능은 re.compile() 을 사용해 패턴을 컴파일하고 그것을 match(), findall(), finditer() 등에 사용한다.
#           패턴을 명시할 때 r'(\d+)/(\d+)/(\d+)'와 같이 raw string 을 그대로 쓰는것이 일반적이다.
#           이 형식은 백슬래시 문자를 해석하지 않고 남겨 두기 때문에 정규 표현식과 같은 곳에 유용하다.

#   - match() 메소드는 문자열의 처음만 확인하므로, 예상치 못한 것에 매칭할 확률도 있다.
m = datepat.match('11/27/2012abcdef')
print(m)
print(m.group())

datepat = re.compile(r'(\d+)/(\d+)/(\d+)$')
print(datepat.match('11/27/2012abcdef'))
print(datepat.match('11/27/2012'))


#  2.5 텍스트 검색과 치환
#  ▣ 문제 : 문자열에서 텍스트 패턴을 검색하고 치환하고 싶다.
#  ▣ 해결 : 간단한 패턴이라면 str.replace() 메소드를 사용한다.
#           조금 더 복잡한 패턴을 사용하려면 re 모듈의 sub() 함수/메소드를 사용한다.
text = 'yeah, but no, but yeah, but no, but yeah'
print(text.replace('yeah', 'yep'))

text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
import re
print(re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text))

#   - 동일한 패턴을 사용한 치환을 계속해야 한다면 성능 향상을 위해 컴파일링을 고려해 보는 것이 좋다.
import re
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
print(datepat.sub(r'\3-\1-\2', text))

#   - 더 복잡한 치환을 위한 콜백 함수 명시.
from calendar import month_abbr
def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))

print(datepat.sub(change_date, text))

#   - 치환이 몇 번 발생했는지 알고 싶다면 re.subn() 을 사용한다.
newtext, n = datepat.subn(r'\3-\1-\2', text)
print(newtext, n)

#  ▣ 토론 : 앞서 살펴본 sub() 메소드에 정규 표현식 검색과 치환 이외에 어려운 것은 없다.


#  2.6 대소문자를 구별하지 않는 검색과 치환
#  ▣ 문제 : 텍스트를 검색하고 치환할 때 대소문자를 구별하지 않고 싶다.
#  ▣ 해결 : 텍스트 관련 작업을 할 때 대소문자를 구별하지 않기 위해서는 re 모듈을 사용해야 하고 re.IGNORECASE 플래그를 지정해야 한다.
text = 'UPPER PYTHON, lower python, Mixed Python'
print(re.findall('python', text, flags=re.IGNORECASE))
print(re.sub('python', 'snake', text, flags=re.IGNORECASE))

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

print(re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE))

#  ▣ 토론 : 대개의 경우 re.IGNORECASE 를 사용하는 것만으로 대소문자를 무시한 텍스트 작업에 무리가 없다.
#            하지만 유니코드가 포함된 작업을 하기에는 부족할 수도 있다.


#  2.7 가장 짧은 매칭을 위한 정규 표현식
#  ▣ 문제 : 정규 표현식을 사용한 텍스트 매칭을 하고 싶지만 텍스트에서 가장 긴 부분을 찾아낸다.
#            만약 가장 짧은 부분을 찾아내고 싶다면 어떻게 해야 할까?
#  ▣ 해결 : * 뒤에 ? 를 붙이면 된다.
import re
str_pat = re.compile(r'\"(.*)\"')
text1 = 'Computer says "no."'
print(str_pat.findall(text1))
text2 = 'Computer says "no." Phone says "yes."'
print(str_pat.findall(text2))
str_pat = re.compile(r'\"(.*?)\"')
print(str_pat.findall(text2))

#  ▣ 토론 : 패턴에서 점은 개행문을 제외한 모든 문제에 매칭하므로, ? 를 * 나 + 뒤에 붙여준다.


#  2.8 여러 줄에 걸친 정규 표현식 사용
#  ▣ 문제 : 여러 줄에 걸친 정규 표현식 매칭을 사용하고 싶다.
#  ▣ 해결 : 패턴에서 (?:.|\n)인 논캡처 그룹을 명시한다.
comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = '''/* this is a
              multiline comment */
'''
print(comment.findall(text1))
print(comment.findall(text2))
comment = re.compile(r'/\*((?:.|\n)*?)\*/')
print(comment.findall(text2))

#  ▣ 토론 : re.compile() 함수에 re.DOTALL 이라는 유용한 플래그를 사용할 수 있다.
comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)
print(comment.findall(text2))


#  2.9 유니코드 텍스트 노멀화
#  ▣ 문제 : 유니코드 모든 문자열에 동일한 표현식을 갖도록 보장해주자.
#  ▣ 해결 : unicodedata 모듈로 텍스트를 노멀화해서 표준 표현식으로 바꿔야 한다.
s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'
print(s1, s2)
print(s1 == s2, len(s1), len(s2))

#   - 위의 경우 같은 문자이지만 표현 방식이 달라 다른 문자열로 인식하였다.
#     따라서. 텍스트 노멀화를 통해 표준 표현식으로 변경해주어야 한다.
import unicodedata
t1 = unicodedata.normalize('NFC', s1)
t2 = unicodedata.normalize('NFC', s2)
print(t1 == t2)
print(ascii(t1))

t3 = unicodedata.normalize('NFD', s1)
t4 = unicodedata.normalize('NFD', s2)
print(t3 == t4)
print(ascii(t3))

#   - 파이썬은 특정 문자를 다룰 수 있도록 추가적인 호환성을 부여하는 NFKC 와 NFKD 노멀화도 지원한다.
s = '\ufb01'
print(s)
print(unicodedata.normalize('NFD', s))
print(unicodedata.normalize('NFKD', s))  # 개별 문자로 분리
print(unicodedata.normalize('NFKC', s))  # 개별 문자로 분리

#  ▣ 토론 : 일관적이고 안전한 유니코드 텍스트 작업을 위해서 노멀화는 아주 중요하다.
#            특히 인코딩을 조절할 수 없는 상황에서 사용자에게 문자열 입력을 받는 경우에는 특히 조심해야 한다.
t1 = unicodedata.normalize('NFD', s1)
print(''.join(c for c in t1 if not unicodedata.combining(c)))  # combining() 함수는 문자가 결합 문자인지 확인한다.


#  2.10 정규 표현식에 유니코드 사용
#  ▣ 문제 : 텍스트 프로세싱에 정규 표현식을 사용 중이다. 하지만 유니코드 문자 처리가 걱정된다.
#  ▣ 해결 : 기본적인 유니코드 처리를 위한 대부분의 기능을 re 모듈이 제공한다.
import re
num = re.compile('\d+')
print(num.match('123'))  # 아스키 숫자
print(num.match('\u0661\u0662\u0663'))  # 아라비아 숫자

#   - 특정 유니코드 문자를 패턴에 포함하고 싶으면, 유니코드 문자에 이스케이프 시퀀스를 사용한다.
arabic = re.compile('[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]+')

#   - 대소문자를 무시하는 매칭에 대소문자 변환을 합친 코드는 다음과 같다.
pat = re.compile('stra\u00dfe', re.IGNORECASE)
s = 'straße'
print(pat.match(s))
print(pat.match(s.upper()), s.upper())

#  ▣ 토론 : 유니코드와 정규 표현식을 같이 사용하려면 서드파티 regex 라이브러리를 설치하고 유니코드 대소문자 변환 등을 기본으로
#            제공하는 많은 기능을 이용하는 것이 좋다.


#  2.11 문자열에서 문자 잘라내기
#  ▣ 문제 : 텍스트의 처음, 끝, 중간에서 원하지 않는 공백문 등을 잘라내고 싶다.
#  ▣ 해결 : strip() 메소드를 사용하면 문자열의 처음과 끝에서 문자를 잘라낼 수 있다.
#            기본적으로 공백이나 \n 을 잘라내지만 원하는 문자를 지정할 수도 있다.
s = '     hello world \n'
print(s.strip())
print(s.lstrip())
print(s.rstrip())
t = '-----hello====='
print(t.strip('-'))
print(t.strip('='))
print(t.strip('-='))

#  ▣ 토론 : 데이터를 보기 좋게 만들기 위한 용도로 여러 strip() 메소드를 일반적으로 사용한다.
#            하지만 텍스트의 중간에서 잘라내기를 할 수는 없다.
s = ' hello        world    \n'
print(s.strip())

#   - 중간의 공백을 없애기 위해서는 replace() 메소드나 정규 표현식의 치환과 같은 다른 기술을 사용해야 한다.
print(s.replace(' ', ''))
import re
print(re.sub('\s+', ' ', s).strip())

with open('files\\somefile.txt') as f:  # 파일 전체 compile 해야 경로 인식.
    lines = (line.strip() for line in f)
    for line in lines:
        print(re.sub('\s+', ' ', line).strip())


#  2.12 텍스트 정리
#  ▣ 문제 : 당신의 웹 페이지에 어떤 사람이 장난스럽게 "python" 이라는 특수문자를 입력했다. 이를 정리하고 싶다.
#  ▣ 해결 : 특정 범위의 문자나 발음 구별 구호를 없애려고 할 때는 str.translate() 메소드를 사용해야 한다.
s = 'pýtĥöñ\fis\tawesome\r\n'
print(s)

#   - 우선 문자열에서 공백문을 잘라내기 위해 작은 변환 테이블을 만들어 놓고 translate() 를 사용한다.
remap = {
    ord('\t'): ' ',  # ord() : 하나의 문자열에 대해 유니코드를 나타내는 의미로 변환.
    ord('\f'): ' ',
    ord('\r'): None  # 삭제됨
}
a = s.translate(remap)
print(a)

#   - 결합 문자를 없애는 방법.
import unicodedata
import sys
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))  # combining() : 유니코드 중에 조합된 것을 추출.
print(cmb_chrs)
b = unicodedata.normalize('NFD', a)
print(b)
print(b.translate(cmb_chrs))

#   - 유니코드 숫자 문자를 이와 관련 있는 아스키 숫자에 매핑하도록 변환 테이블을 작성한다.
digitmap = {
    c: ord('0') + unicodedata.digit(chr(c)) for c in range(sys.maxunicode) if unicodedata.category(chr(c)) == 'Nd'
}
print(len(digitmap), digitmap)
x = '\u0661\u0662\u0663'
print(x.translate(digitmap))

#   - 또 다른 텍스트 정리 기술로 I/O 인코딩, 디코딩 함수가 있다. 이 방식은 텍스트를 우선 정리해 놓고 encode() 나 decode() 를
#     실행해서 잘라내거나 변경한다.
print(a)
b = unicodedata.normalize('NFD', a)
print(b.encode('ascii', 'ignore').decode('ascii'))  # ascii 형태로 인코딩 및 디코딩

#  ▣ 토론 : 텍스트 정리를 하다 보면 실행 성능 문제에 직면하기도 한다.
#            간단한 치환을 위해서는 str.replace() 함수를 사용하는 것이 빠르고 복잡한 치환을 하는 경우에는 str.translate() 함수를
#            사용하는 것이 좋다.


#  2.13 텍스트 정렬
#  ▣ 문제 : 텍스트를 특정 형식에 맞추어 정렬하고 싶다.
#  ▣ 해결 : ljust(), rjust(), center() 등이 있다.
text = 'Hello World'
print(text.ljust(20))
print(text.rjust(20))
print(text.center(20))

#   - 세 개의 메소드는 별도의 채워 넣기 문자를 사용할 수 있다.
print(text.rjust(20, '='))
print(text.center(20, '*'))

#   - format() 함수를 사용하면 인자로 <, >, ^ 를 적절하게 사용해 주면 된다.
print(format(text, '>20'))  # rjust 와 동일
print(format(text, '<20'))  # ljust 와 동일
print(format(text, '^20'))  # center 와 동일

#   - 공백 대신 특정 문자를 채워 넣고 싶다면 정렬 문자 앞에 그 문자를 지정한다.
print(format(text, '=>20'))
print(format(text, '*^20'))

#   - 포맷 코드는 format() 메소드에 사용해 여러 값을 서식화할 수도 있다.
print('{:>10} {:>10}'.format('Hello', 'World'))

#   - format() 을 사용하면 문자열뿐만 아니라 숫자 값 등 모든 값에 동작한다.
x = 1.2345
print(format(x, '>10'))  # str 타입으로 변환
print(format(x, '^10.2f'))  # 소수점 자리수 지정 가능

#  ▣ 토론 : 오래된 코드를 보면 % 연산자를 사용해 텍스트를 서식화하기도 했다.
print('%-20s ' % text)
print('%20s ' % text)


#  2.14 문자열 합치기
#  ▣ 문제 : 작은 문자열 여러 개를 합쳐 하나의 긴 문자열을 만들고 싶다.
#  ▣ 해결 : 합치고자 하는 문자열이 시퀀스나 순환 객체 안에 있다면 join() 메소드를 사용하는 것이 가장 빠르다.
parts = ['Is', 'Chicago', 'Not', 'Chicago?']
print(' '.join(parts))
print(','.join(parts))
print(''.join(parts))

#   - 합치려고 하는 문자열의 수가 아주 적다면 + 를 사용하면 된다.
a = 'Is Chicago'
b = 'Not Chicago?'
print(a + ' ' + b)

#   - + 연산자는 조금 더 복잡한 문자열 서식 연산에 사용해도 잘 동작한다.
print('{} {}'.format(a, b))
print(a + ' ' + b)

a = 'Hello' 'World'
print(a)

#  ▣ 토론 : 명심해야 할 부분은, + 연산자로 많은 문자열을 합치려고 하면 메모리 복사와 가비지 컬렉션으로 인해 매우 비효율적이라는 점이다.
s = ''
for p in parts:
    s += p

#   - 생성자 표현식으로 합치는 방법이 있다.
data = ['ACME', 50, 91.1]
print(' '.join(str(v) for v in data))

#   - 불필요한 문자열 합치기를 하고 있지 않은지도 주의하자.
a = 'qwer'
b = 'asdf'
c = 'zxcv'
print(a + ':' + b + ':' + c)  # 좋지 않은 방식
print(':'.join([a, b, c]))  # 개선된 방식
print(a, b, c, sep=':')  # 좋은 방식

#   - 수많은 짧은 문자열을 하나로 합쳐 문자열을 만드는 코드를 작성한다면, yeild 를 사용한 생성자 함수를 고려하자.
def sample():
    yield 'Is'
    yield 'Chicago'
    yield 'Not'
    yield 'Chicago?'

text = ''.join(sample())
print(text)

#   - 문자열을 입출력(I/O)으로 리다이렉트 할 수 있다.
for part in sample():
    f.write(part)

#   - 입출력을 조합한 하이브리드 방식 구현도 가능하다.
f = open('D:\\KYH\\02.PYTHON\\data\\combine.txt', 'a')

def combine(source, maxsize):
    parts = []
    size = 0
    for part in source:
        parts.append(part)
        size += len(part)
        if size >= maxsize:
            yield ''.join(parts)
            parts = []
            size = 0
    yield ''.join(parts)

for part in combine(sample(), 32768):
    f.write(part)


#  2.15 문자열에 변수 사용
#  ▣ 문제 : 문자열에 변수를 사용하고 이 변수에 맞는 값을 채우고 싶다.
#  ▣ 해결 : 파이썬 문자열에 변수 값을 치환하는 간단한 방법은 존재하지 않는다.
#            하지만 format() 메소드를 사용하면 비슷하게 흉내 낼 수 있다.
s = '{name} hash {n} messages.'
print(s.format(name='Guido', n=37))

#   - 치환할 값이 변수에 들어 있다면 format_map() 과 vars() 를 함께 사용하면 된다.
name = 'Guido'
n = 37
print(s.format_map(vars()))

#   - vars() 에는 인스턴스를 사용할 수도 있다.
class Info:
    def __init__(self, name, n):
        self.name = name
        self.n = n

a = Info('Guido', 37)
print(s.format_map(vars(a)))

#   - format() 또는 format_map() 사용시 빠진 값은 __missing__() 메소드가 있는 딕셔너리 클래스를 정의해서 피할 수 있다.
class safesub(dict):
    def __missing__(self, key):
        return '{' + key + '}'

del n
print(s.format_map(safesub(vars())))

#   - 코드에서 변수 치환을 빈번히 사용할 것 같다면 치환하는 작업을 유틸리티 함수에 모아 놓고 소위 "프레임 핵(frame hack)"으로 사용할 수 있다.
import sys

def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))

name = 'Guido'
n = 37
print(sub('Hello {name}'))
print(sub('You have {n} messages.'))
print(sub('Your favorite color is {color}'))

#  ▣ 토론 : 파이썬 자체에서 변수 보간법이 존재하지 않아서 다양한 대안이 생겼다.
name = 'Guido'
n = 37
print('%(name) has %(n) messages.' % vars())

import string
s = string.Template('$name has $n messages.')
print(s.substitute(vars()))


#  2.16 텍스트 열의 개수 고정
#  ▣ 문제 : 긴 문자열의 서식을 바꿔 열의 개수를 조절하고 싶다.
#  ▣ 해결 : textwrap 모듈을 사용해서 텍스트를 재서식화 한다.
s = 'Look into my eyes, look into my eyes, the eyes, the eyes,' \
    "the eyes, not around the eyes, don't look around the eyes," \
    "look into my eyes, you're under."
import textwrap
print(textwrap.fill(s, 70))
print(textwrap.fill(s, 40))
print(textwrap.fill(s, 40, initial_indent='       '))
print(textwrap.fill(s, 40, subsequent_indent='       '))

#  ▣ 토론 : 텍스트를 출력하기 전에 textwrap 모듈을 사용하면 깔끔하게 서식을 맞출 수 있다.
#           특히 터미널에 사용할 텍스트에 적합하다.
#           터미널의 크기를 얻으려면 os.get_terminal_size() 를 사용한다.
import os
print(os.get_terminal_size().columns)