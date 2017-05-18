1.18 시퀀스 요소에 이름 매핑
from collections import namedtuple
Subscriber = namedtuple('subscriber',['addr','joined'])
sub = Subscriber('jonesy@example.com','2012-10-19')
sub
Subscriber(addr='jonesy@example.com',joined='2012-10-19')
sub.addr
sub.joined


len(sub)
addr,joined = sub
addr
joined

from collections import namedtuple
Stock = namedtuple('Stock', ['name', 'shares', 'price'])
def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total
# Some Data
records = [
    ('GOOG', 100, 490.1),
    ('ACME', 100, 123.45),
    ('IBM', 50, 91.15)
]
print(compute_cost(records))

1.19 데이터를 변환하면서 줄이기
nums = [ 1,2,3,4,5]
s = sum(x * x for x in nums)

import os
files=os.listdir('dirname')
if any(name.endswich('.py') for name in files):
    print('There be python!')
else:
    print('Sorry, no python')


s = ('ACME',50,123.45)
print(','.join(str(x) for x in s))

portfolio = [ {'name':'GOOG','shares':50},
             {'name':'YHOO','shares':70},
             {'name':'AOL','shares':20},
             {'name':'SCOX','shares':60}]
min_shares=min(s['shares'] for s in portfolio)
min_shares

1.20 여러 매핑을 단일 매핑으로 합치기
a = {'x':1,'z':3}
b = {'y':2,'z':4}
from collections import ChainMap
c = ChainMap(a,b)
print(c['x'])
print(c['y'])
print(c['z'])   # a의 z값을 출력한다.

len(c)
list(c.keys())
list(c.values())


2.1 여러 구분자로 문자열 나누기
line = 'asdf fjdk; afed,fjek,asdf,        foo'
import re
re.split(r'[;,\s]\s*',line)

fields = re.split(r'(;|,|\s)\s*',line)
fields

values = fields[::2]
delimiters = fields[1::2] +['']
values

delimiters

''.join(v+d for v,d in zip(values,delimiters))

2.2 문자열 처음이나 마지막에 
    텍스트 매칭
자료 없음
2.3 쉘 와이드카드 패턴으로 문자열 매칭
addresses = ['5412 N CLARK ST','1060 W ADDISON ST','1039 W GRANVILLE AVE',
             '2122 N CLARK ST','4802 N BROADWAY']

from fnmatch import fnmatchcase
[addr for addr in addresses if fnmatchcase(addr,'* ST')]
[addr for addr in addresses if fnmatchcase(addr,'54[0-9][0-9] *CLARK*')]

2.4 텍스트 패턴 매칭과 검색
text = ' yeah, but no, but yeah, but no, but yeah'
text == 'yeah'
text.startswith('yeah')
text.endswith('no')
text.find('no')

text1 = '1/27/2012'
text2 = 'Nov 27,2012'
import re
if re.match(r'\d+/\d+/\d+', text1):
    print('yes')
else:
    print('no')

if re.match(r'\d+/\d+/\d+',text2):
    print('yes')
else:
    print('no')

 datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')

if datepat.match(text2):
    print('yes')
else:
    print('no')   
text = 'Today is 11/27/2012. Pycon starts 3/13/2013.'
datepat.findall(text)
2.5 텍스트 검색과 치환
text = ' yeah, but no, but yeah, but no, but yeah'

text.replace('yeah','yep')
text = 'Today is 11/27/2012. Pycon starts 3/13/2013.'
import re
re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2',text)
import re
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
datepat.sub(r'\3-\1-\2',text)
from calendar import month_abbr
def change_date(m):
    mon_name=month_abbr[int(m.group(1))]
    return '{}{}{}'.format(m.group(2),mon_name,m.group(3))
datepat.sub(change_date, text)
2.6 대소문자를 구별하지 않는 
    검색과 치환
import re
text = 'UPPER PYTHON, lower python, Mixed Python'
re.findall('python',text,flags=re.IGNORECASE)

re.sub('python','snake',text,flags = re.IGNORECASE)   

2.7 가장 짧은 매칭을 위한 정규 표현식
import re
str_pat = re.compile(r'\"(.*)\"')
text1='Computer says "no."'
str_pat.findall(text1)

text2='Computer says "no." Phone says "yes."'
str_pat.findall(text2)

str_pat = re.compile(r'\"(.*?)\"')
str_pat.findall(text2)

r’\“(.*)\”’ 패턴은 따옴표에 둘러싸인 텍스트만 찾는다. 그래서 text2에서 원치 않게 인용문 두 개에 동시에 매칭한다. 이 문제를 해결하려면
(.*?)를 붙이면 해결이 된다.
2.8 여러 줄에 걸친 정규 표현식 사용
import re
comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment*/'
text2 = '''/* this is a
              multiline comment */
'''
comment.findall(text1)
comment.findall(text2)

comment = re.compile(r'/\*((?:.|\n)*?)\*/')
comment.findall(text2)
text2에 c 스타일 주석이 포함되어 있지만 이를 찾아내지 못하는데 이 문제를 해결하려면 (r'/\*((?:.|\n)*?)\*/') 이런식으로 개행문 패턴에 넣어야 한다.

comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)
comment.findall(text2)

re.DOTALL 이 플래그를 사용하면 정규 표현식의 점이 개행문을 포함한 모든 문자에 매칭한다.
2.9 유니코드 텍스트 노멀화
s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'
print(s1)
print(s2)
print('s1 == s2', s1 == s2)
print(len(s1), len(s2))

import unicodedata

t1 = unicodedata.normalize('NFC', s1)
t2 = unicodedata.normalize('NFC', s2)
t1 == t2
print(ascii(t1))

t3 = unicodedata.normalize('NFD', s1)
t4 = unicodedata.normalize('NFD', s2)
t3 == t4
print(ascii(t3))

2.10 정규 표현식에 유니코드 사용
import re
num = re.compile('\d+')
num.match('123')

num.match('\u0661\u0662\u0663')

2.11 문자열에서 문자 잘라내기
s= '     hello world \n'
s.strip()
s.lstrip()
s.rstrip()


t = '-------hello======'
t.lstrip('-')
t.strip('-=')

s = ' hello            world       \n'
s = s.strip()
s

import re
re.sub('\s+',' ',s)

2.12 텍스트 정리
s = 'p\xfdt\u0125\xf6\xf1\x0cis\tawesome\r\n'
print(s)

remap = {
    ord('\t') : ' ',
    ord('\f') : ' ',
    ord('\r') : None 
}

a = s.translate(remap)
print('whitespace remapped:', a)

import unicodedata
import sys
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode)
                         if unicodedata.combining(chr(c)))
b = unicodedata.normalize('NFD', a)
c = b.translate(cmb_chrs)
print('accents removed:', c)
d = b.encode('ascii','ignore').decode('ascii')
print('accents removed via I/O:', d)

2.13 텍스트 정렬
text = 'Hello World'
text.ljust(20)
text.rjust(20)
text.center(20)
format(text,'>20')
format(text,'<20')
format(text,'^20')

format(text,'=^20')   # 이렇게도 응용 가능하다.

'{:>10s}{:>10s}'.format('Hello', 'World')

2.14 문자열 합치기
parts = ['Is','Chicago','Not','Chicago?']
' '.join(parts)
''.join(parts)

문자열의 수가 적다면 + 로 합치기가 가능하다.
소스코드에서는 아래와 같이 단순히 붙여놓기만 해도 가능하다.
a = 'Hello' 'World'
a

print(a+':'+b+':'+c)
print(':'.join([a,b,c]))
print(a,b,c,sep=':')
마지막 방법으로 하는 것이 가장 좋은 방법이다.


2.15 문자열에 변수 사용
s = '{name} has {n} message'
s.format(name='Guido',n=37)

name = 'Guido'
n = 37
s.format_map(vars())

2.16 텍스트 열의 개수 고정
s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."

import textwrap
print(textwrap.fill(s, 70)) # 출력시 글 길이를 70으로 제한
print()

print(textwrap.fill(s, 40)) # 출력시 글 길이를 40으로 제한
print()





print(textwrap.fill(s, 40, initial_indent='    ')) 
#글자 길이 40으로 제한하고 첫 문장만 initial_indent = '    ' 넣어 출력
print()


print(textwrap.fill(s, 40, subsequent_indent='    '))
print() 
# 글자 길이 40으로 제한하고 
첫문장 제외 subsequent_indent='    ' 넣어 출력

