# 1.18 시퀀스 요소에 이름 매핑

from collections import namedtuple

Subscriber = namedtuple('Subscriber1', ['addr', 'joined'])  # 타입이름, 매핑할 변수명
sub = Subscriber('gh506015@naver.com', '2012.12.12')
sub
sub.addr
sub.joined

addr, joined = sub
addr
joined

Stock = namedtuple('Stock', ['name', 'shares', 'price'])

#123123132


# 매핑할 namedtuple을 만들어 놓고....
def compute_cost(records):
    total = 0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total


records = [['a', 0.75, 10], ['b', 0.25, 12]]
compute_cost(records)  # 이렇게 실행해주시면 됩니다.!!@#@#!

s = Stock('ACME', 100, 123.45)
s
s.shares = 75
# tuple이기 때문에 수정할 수 없다. _replace함수를 이용해 수정하는 방법이 있다.
# 하지만 굳이 따지자면 수정하는 것이 아니라 수정을 한 완전히 새로운 데이터프레임을 만든 것
s._replace(shares=75)  # 튜플 수정

# 1.19 데이터를 변환하면서 줄이기
nums = [1, 2, 3, 4, 5]
s = sum(n ** 2 for n in nums)
s

portfolio = [
    {'name': 'GOOG', 'shares': 50},
    {'name': 'APPL', 'shares': 30},
    {'name': 'SAMS', 'shares': 10},
    {'name': 'LG', 'shares': 5}
]

min_shares = min(s['shares'] for s in portfolio)
min_shares

# 1.20 여러매핑을 단일 매핑으로 합치기
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
from collections import ChainMap

c = ChainMap(a, b)

print(c['x'])
print(c['y'])
print(c['z'])  # 중복값이 있으면 첫번째 key를 받아서 사용한다. a의 z
# ChainMap은 매핑을 여러개 받아서 하나처럼 보이게 만든다. 하지만 실제로 하나로 합친건 아님

# 대부분의 명령이 동작한다.
print(len(c))  # 중복된 것은 제거하고 출력한다.
list(c.keys())
list(c.values())
c
del c['x']
del c['z']  # 첫번째 z가 지워지고 나서 두번째 z는 찾을 수 없다고 예외처리된다.
c
del a['x']
a

values = ChainMap()  # 체인맵 선언한 후에...
values['x'] = 1  # 새로운 매핑 추가
values['y'] = 2
values['x'] = 3
values
values.new_child()  # 실제로 데이터프레임이 바뀌지는 않기 때문에....
values = values.new_child()  # 이렇게 다시 선언!!
values['x'] = 2
values
values = values.new_child()
# 비어있는 딕셔너리에 골라서 넣을 수 없기 때문에 넣을때마다 딕셔너리 추가
# 데이터는 앞으로 들어간다.
values['y'] = 3
values
values = values.parents  # 마지막매핑(딕셔너리)부터 삭제, 스택구조 데이터
values

a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
type(b)
merged = b
merged
merged.update(a)  # update가능
merged
# 딕셔너리를 새로 만드는 것이기 때문에 원본이 변해도 영향을 받지 않는다.
# 하지만@@@@하지만@@@@하지만@@@@하지만@@@@하지만@@@@
merged = ChainMap(a, b)  # 원본을 참조하는 ChainMap의 경우
a['x'] = 42  # 원본이 바뀌면
merged['x']  # ChainMap도 변한다.

a = 'askja. amsa clskd. sk adf jdk ds/ adf  ka;a;dkf'
import re

line = re.split(r'[.,/;:\s]\s*', a)  # 대괄호 안에 있는 것을 제외하고
line  # 바깥에 있는 문자가 붙어있는 경우도 제외

fields = re.split(r'(.|,|/|;|:|\s)\s*', a)
fields

# 2.2 문자열 처음이나 마지막 텍스트 매칭
filename = 'spam.txt'
filename.endswith('.txt')
filename.startswith('file:')

import os

filenames = os.listdir('.')  # listdirectory 디렉토리 보여달라
filenames
any(name.endswith('.py') for name in filenames)

filename = 'spam.txt'
filename[-4:] == '.txt'

# 2.3 쉘 와일드카드 패턴으로 문자열 매칭
from fnmatch import fnmatch, fnmatchcase

a = 'foo.txt'
fnmatch(a, '*.txt')
fnmatch('foo.txt', '*.txt')  # *는 여러문자용 와일드 카드
fnmatch('foo.txt', '?oo.txt')  # ?는 문자 하나용 와일드 카드
fnmatch('Dat45.csv', 'Dat[0-9]*')  # 이건 진짜 좋네요!!!!!!!!!!!!!1
names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']
a = [name for name in names if fnmatch(name, 'Dat*.csv')]
# 아래에서 나오는 fnmatchcase()함수도 사용가능하다.
a

# OS X (Mac)과 Windows의 차이
fnmatch('foo.txt', '*.TXT')
# 여기선 True라고 나오는데 mac os에서는 False로 나온다.
# 이게 싫다면 fnmatchcase를 사용하면 됩니다. 대소문자 정확히 일치하는 것만 찾습니다.
fnmatchcase('foo.txt', '*.TXT')

# 2.4텍스트 패턴 매칭과 검색
text = 'yeah, but no, but yeah, but no, but yeah'
# 정확한 매칭
text == 'yeah'  # False
text.startswith('yeah')
text.find('no')  # 10, 처음 나타난 곳을 검색한다.

text1 = '11/27/2012'
text2 = 'Nov 27, 2012'
import re

# \d+는 하나 이상의 숫자가 있다는 뜻이다.
if re.match(r'\d+/\d+/\d+', text1):
    print('yes')
else:
    print('no')

if re.match(r'\d+/\d+/\d+', text2):
    print('yes')
else:
    print('no')

# compile 잘 모르지만 일단 적음
datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')

# match()는 항상 문자열 처음에서 찾기를 시도한다. 텍스트 전체에 걸쳐 패턴을 찾으려면
# findall() 메소드를 사용한다.
text = 'Today is 11/27/2012. PyCon stars 3/13/2013.'
datepat.findall(text)
# compile하지 않으면 re.findall(r'\d+/\d+/\d+', text) 이렇게

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
m = datepat.match('11/27/2012')
m
m.group(0)
m.group(1)
m.group(2)
m.group(3)
m.group()  # 난 이거 안되는데?
month, day, year = m.group()  # 그래서 이거도 안돼

text
datepat.findall(text)
for month, day, year in datepat.findall(text):
    print('{}-{}-{}'.format(year, month, day))
# findall()메소드는 텍스트를 검색하고 모든 매칭을 찾아서 리스트로 반환한다.

re.findall(r'\d+/\d+/\d+', text)  # 이것은 list의 item으로 반환
re.findall(r'(\d+)/(\d+)/(\d+)', text)  # 이것은 list안의 tuple의 item으로 반환

# 2.5 텍스트 검색과 치환
text = 'yeah, but no, but yeah, but no, but yeah'
text.replace('yeah', 'yep')  # 위치 바꾸기
# 'yep, but no, but yep, but no, but yep'

text = 'today is 11/27/2012. PyCon starts 3/13/2013.'
import re

re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
# 'todayis 11/27/2012. PyCon starts 3/13/2013.'

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
datepat.sub(r'\3-\1-\2', text)

from calendar import month_abbr


def chang_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))


datepat.sub(chang_date, text)

newtext, n = datepat.subn(r'\3-\1-\2', text)
newtext

str_pat = re.compile(r'\"(.*)\"')  # ""에 둘러쌓인 글자 찾기
text1 = 'Computer says "no."'
str_pat.findall(text1)

text2 = 'Computer says "no." Phone says "yes."'  # ""에 둘러쌓인 글자 찾기
str_pat.findall(text2)  # 가장 탐욕스럽게 소비(길게)

str_pat = re.compile(r'\"(.*?)\"')
str_pat.findall(text2)

comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = '''/* this is a comment */'''
comment.findall(text1)
comment.findall(text2)  # 주석표시를 인식하지 못한다.

comment = re.compile(r'/\*((?:.|\n)|*?)\*/')
comment.findall(text2)

# 2.9유니크도 텍스트 노멀화
s1 = 'spicy jalape\u00f1o'
s2 = 'spicy jalapen\u0303o'
s1
s2
# 'spicy jalapeño'
# 'spicy jalapeño'
s1 == s2

import unicodedata

t1 = unicodedata.normalize('NFC', s1)
t2 = unicodedata.normalize('NFC', s2)
t1 == t2
print(ascii(t1))  # 아스키 코드

t3 = unicodedata.normalize('NFD', s1)
t4 = unicodedata.normalize('NFD', s2)  # 첫번째 인자는 문자열을 어떻게 노멀화할 것인지 지정
t3 == t4
print(ascii(t3))
# NFC = 문자를 정확히 구성하도록 지정
# NFD = 문자를 여러개 합쳐서 지정

# 2.11 문자열에서 문자 잘라내기
s = '   hello world \n'
s.strip()  # 공백문자 제거
s.lstrip()
s.rstrip()
t = '------hello====='
t.lstrip('-')
t.rstrip('=')
tt.strip('-=')

s = '  hello   world  \n'
s = s.strip()
s

s.replace(' ', '')
s

import re

re.sub('\s+', ' ', s)  # +s 연속된 space를 ' ' space하나로

# 2.12 텍스트 정리
import unicodedata
import sys

cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
b = unicodedata.normalize('NFD', a)
b

digimap = {c: ord('0') + unicodedata.digit(chr(c))
           for c in range(sys.maxunicode)
           if unicodedata.category(chr(c)) == 'Nd'}
len(digimap)
b  # 왜 난 580나오냐

# 2.13 텍스트 정렬
text = 'hello world'
text.ljust(20)  # 왼쪽으로 붙이고 오른쪽에 20공백
text.rjust(20)
# sql의 pad와 반대로 생각하면 된다.

text.rjust(20, '=')
text.center(20, '*')  # 틱택토

format(text, '>20')  # format함수의 다양한 쓰임새
format(text, '<20')
format(text, '^20')

format(text, '=>20s')
format(text, '*^20s')
#### 문자, 숫자 모두 사용가능!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# 2.14 문자열 합치기
parts = ['is', 'Chicago', 'Nor', 'Chicago?']
' '.join(parts)  # 문자 다 합쳐서 아이템 하나로 만들기

','.join(parts)

''.join(parts)

data = ['ACME', 50, 91.1]
','.join(str(d) for d in data)  # 다 문자열로 바꿔서 ,구분자로 붙여주기


def sample():
    yield 'Is'
    yield 'Chicago'
    yield 'Not'
    yield 'Chicago?'


text = ''.join(sample())

s = '{name} has {n} messages.'
s.format(name='Guido', n=37)
# 'Guido has 37 messages.'

name = 'Guido'
n = 37
s.format_map(vars())


# 'Guido has 37 messages.'

class info:
    def __init__(self, name, n):
        self.name = name
        self.n = n


a = info('Guido', 38)
s.format_map(vars(a))

s.format(name='Guido')


class safesub(dict):
    def __misssing__(self, key):
        return '{' + key + '}'


del n

s.format_map(safesub(vars()))

# 2.16 텍스트 열의 개수 고정

s = "내 눈을 봐, 내 눈을 보라고 임마, 그 눈 ,그 눈, 그 눈, 눈 주변 말고 임마 \
눈 주변을 보지 말라고 임마, 눈 안쪽을 보라고"
import textwrap

print(textwrap.fill(s, 70))
print(textwrap.fill(s, 40))
print(textwrap.fill(s, 40, initial_indent='     '))
print(textwrap.fill(s, 70, subsequent_indent='     '))
import os

os.get_terminal_size().columns  # 안된다 왜 안되는지 나도 모름~~


