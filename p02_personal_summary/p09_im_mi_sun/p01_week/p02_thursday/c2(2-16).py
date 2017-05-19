# #####1.18 시퀀스 요소에 이름 매핑
# from collections import namedtuple
# Subscriber = namedtuple('Subscriber',['addr','joined'])
# sub = Subscriber('jonesy@example.com','2012-10-19')
# print(sub)          #>>> Subscriber(addr='jonesy@example.com', joined='2012-10-19')
# print(sub.addr)     #>>> jonesy@example.com
# print(sub.joined)   #>>> 2012-10-19
#
# len(sub)
# addr, joined = sub
# print(addr)     #>>>jonesy@example.com
# print(joined)   #>>>2012-10-19
#
# def compute_cost(records):
#     total =0.0
#     for rec in records:
#         total += rec[1] * rec[2]
#     return total
#
# from collections import namedtuple
# Stock = namedtuple('Stock', ['name','shares','price'])
# def compute_cost(records):
#     total = 0.0
#     for rec in records:
#         s = Stock(*rec)
#         total += s.shares * s.price
#     return total
#
# s= Stock('ACME',100,123.45)
# print(s) #S>>> tock(name='ACME', shares=100, price=123.45)
# s.share = 75
#
# s = s._replace(shares=75)
# print(s) #Stock(name='ACME', shares=75, price=123.45)
#
# from collections import namedtuple
# Stock = namedtuple('Stock', ['name','shares','price','date','time'])
# #프로토타입 인스턴스 생성
# stock_prototype = Stock('',0,0.0,None,None)
# #딕셔너리를 Stock으로 변환하는 함수
# def dict_to_stock(s):
#     return stock_prototype._replace(**s)
#
# a = {'name':'ACME', 'shares':100, 'price' :123.45}
# print ( dict_to_stock(a))         #Stock(name='ACME', shares=100, price=123.45, date=None, time=None)
# b = {'name':'ACME', 'shares':100, 'price' : 123.45, 'date':'12/17/2012'}
# print(dict_to_stock(b))           #Stock(name='ACME', shares=100, price=123.45, date='12/17/2012', time=None)
#
# nums = [1,2,3,4,5]
# s = sum(x * x for x in nums)
# print(s) # >>> 55
#
# #디렉토리에 또다른 .py파일이 있는지 살펴봄
# import os
# files = os.listdir('dirname')
# if any(name.endswith('.py') for name in files):
#     print( 'there be python')
# else:
#     print('sorry. no python')
#
# #튜플을 csv로 출력
# s = ('ACME',50,123.45)
# print( ','.join(str(x) for x in s))
#
# #자료 구조의 필드를 줄인다
# portfolio = [
#     {'name':'GOOD', 'shares':50},
#     {'name':'YHOO', 'shares':75},
#     {'name':'AOL', 'shares':20},
#     {'name':'SCOX', 'shares':65}
# ]
# min_shares = min( s['shares'] for s in portfolio )
#
# s = sum( ( x* x for x in nums))
# s = sum( x * x for x in noms )
#
# # 원본: 20을 반환
# min_shares = min(s['shares'] for s in portfolio)
# # 대안 : {'name': 'AOL', 'shares' : 20 }
# min_shares = min(portfolio, key=lamdba s: s['shares'])
#
# #####1.20 여러 매핑을 단일 매핑으로 합치기
# a = {'x':1, 'z':3}
# b = {'y':2, 'z':4}
#
# from collections import ChainMap
# c = ChainMap(a,b)
# print(c) #ChainMap({'x': 1, 'z': 3}, {'y': 2, 'z': 4})
# print( c['x']) #>>>1
# print( c['y']) #>>>2
# print( c['z']) #>>>3
#
# len(c) #>>>3
# list(c.keys())  #>>>['y', 'x', 'z']
# list(c.values()) #>>> [2, 1, 3]
#
# c['z'] = 10
# c['w'] = 40
# del c['x'] #{'z': 10, 'w': 40}
# print(a)
# #del c['y'] #오류남
#
#
# #새로운 매핑 추가
# values = values.new_child()
# values['x'] = 3
#
# print(values) #ChainMap({'x': 3},{'x':2}, {'x': 1})
# values['x']  #>>>3
#
# #마지막 매핑 삭제
# values = values.parents
# values['x'] #>>>2
#
# #마지막 매핑 삭제
# values = values.parents
# values['x'] #>>>1
#
# print(values) #>>>ChainMap({'x': 1})
#
# a = {'x':1, 'z':3}
# b = {'y':2, 'z':4}
# merged = dict(b)
# merged.update(a) #업데이트에 들어가는 애 기준이구만
# print(merged) #{'y': 2, 'z': 3, 'x': 1}
# merged['x'] #>>>1
# merged['y'] #>>>2
# merged['z'] #>>>3
#
# a['x'] =13
# merged['x'] #>>>1
#
# a = {'x':1, 'z':3}
# b = {'y':2, 'z':4}
# merged = ChainMap(a,b)
# merged['x'] #>>>1
# a['x'] = 42
# merged['x'] #>>>42
#
# #####2.1 여러 구분자로 문자열 나누기
# line = 'asdf fjdk; afed, fjek,asdf,     foo'
# import re
# re.split(r'[;,\s]\s*', line) #>>>>['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
#
# fields = re.split(r'(;|,|\s)\s*',line)
# fields #>>>['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo']
#
# values = fields[::2]
# delimiters = fields[1::2] + ['']
# print(values) #>>> ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
# print(delimiters) #>>>[' ', ';', ',', ',', ',', '']
#
# #동일한 구분자로 라인을 구성
# print ( ''.join(v+d for v,d in zip(values, delimiters)) ) #>>>asdf fjdk;afed,fjek,asdf,foo
#
# re.split(r'(?:,|;|\s)\s*',line) #>>>['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
#
#
#
# #####2.2 문자열 처음이나 마지막에 텍스트 매칭
# filename = 'spam.txt'
# filename.endswith('.txt') #>>>True
# filename.startwith('file:') #>>>False
# url = 'http://www.python.org'
# url.startswith('http://') #>>>True
#
# import os
# filenames = os.listdir('.')
# print( filenames) #>>>['.DS_Store', '.git', '.idea', 'i_wanna', 'pingpong', 'PythonVariable', 'study_materials', 'tictactoe', 'webcrawling']
# [name for name in filenames if name.endswith( ('.c', '.h'))] #업쒀
# any(name.endswith('.py') for name in filenames) #>>> True / False 반환
#
# from urllib.request import urlopen
#
# def read_data(name):
#     if name.startswitch( ('http://','http:','ftp:')):
#         return urlopen(name).read()
#     else:
#         with open(name) as f:
#             return f.read()
#
# choices = ['http://','ftp:']
# url = 'http://www.python.org'
# url.startswith(choices) # 오류남 --> 튜플로 먼저 변환해줘야함
# usl.startswith(tuple(choices)) #True
#
#
# filename = 'spam.txt'
# filename[-4:] =='.txt' #>>>True
# url = 'http://www.python.org'
# url[:5] == 'http:' or url[:6] == 'https:' or url[:4] == ' ftp' #>>>True
#
# import re
# url = 'http://www.python.org'
# print( re.match('http:|https:|ftp:', url) )  #책이랑 다르게 나옴 <_sre.SRE_Match object; span=(0, 5), match='http:'>
#
# #if any(name.endswith('.c','.h') for name in listdir(dirname)):

#####2.4 텍스트 패턴 매칭과 검색
text = "yeah, but, no, but no, but yeah" #정확한 매칭

text == 'yeah'  #>>>False

#처음이나 끝에 매칭
text.startswith('yeah') #>>True
text.endswith('no') #>>False

#처음 나타난 곳 검색
text.find('no') #10

text1 = '11/27/2012'
text2 = 'Nov 27, 2012'
import re
#간단한 매칭: \d+는 하나 이상의 숫자를 의미
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

datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')

if datepat.match(text2):
    print('yes')
else:
    print('no')

text = 'Today is 11/27/2012. PyCon starts 3/13/2013'
datepat.findall(text) #['11/27/2012', '3/13/2013']

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
m = datepat.match('11/27/2012')
print(m) #<_sre.SRE_Match object; span=(0, 10), match='11/27/2012'>

#각 그룹에서 내용 추출
m.group(0) #11/27/2012
m.group(1) #11
m.group(2) #27
m.group(3) #2012
m.groups() #('11','27','2012')
month, day, year = m.groups()

#전체 매칭 찾기(튜플로 나눈다)
text
datepat.findall(text) #[('11', '27', '2012'), ('3', '13', '2013')]

for month, day, year in datepat.findall(text):
    print('{}-{}-{}'.format(year, month, day))
#2012-11-27
#2013-3-27


for m in datepat.findinter(text):
    print(m.groups())

m = datepat.match('11/27/2012abcdef')
print( m) #<_sre.SRE_Match object; span=(0, 10), match='11/27/2012'>
print( m.group())

datepat = re.compile(r'(\d+)/(\d+)/(\d+)$')
datepat.match('11/27/2012abcdef')
datepat.match('11/27/2012')

re.findall(r'(\d+)/(\d+)/(\d+)', text) #[('11', '27', '2012'), ('3', '13', '2013')]

#####2.5 텍스트 검색과 치환
text = "yeah, but, no, but no, but yeah"
text.replace('yeah','yep')
text #'yeah, but, no, but no, but yeah'

text = 'Today is 11/27/2012. PyCon starts 3/13/2013'
import re
re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text) #>>>'Today is 2012-11-27. PyCon starts 2013-3-13'

import re
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
datepat.sub(r'\3-\1-\2',text) #>>>'Today is 2012-11-27. PyCon starts 2013-3-13'


from calendar import month_abbr
def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3)) #re.compile 순서대로

datepat.sub(change_date, text) #'Today is 27 Nov 2012. PyCon starts 13 Mar 2013'

newtext, n = datepat.subn(r'\3-\2-\1', text)
newtext #'Today is 2012-27-11. PyCon starts 2013-13-3'

#####2.6 대소문자를 구별하지 않는 검색과 치환
text = 'UPPER PYTHON, lower python, Mixed Python'
re.findall('python', text, flags = re.IGNORECASE) #['PYTHON', 'python', 'Python']
re.sub('python','snake',text,flags =re.IGNORECASE) #'UPPER snake, lower snake, Mixed snake'

def matchcase(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper(): #첫글자만 대문자 나머지는 소문자
            return word.capitalize()
        else:
            return word
    return replace

re.sub('python',matchcase('snake'),text, flags=re.IGNORECASE)
#'UPPER SNAKE, lower snake, Mixed Snake'

#####2.7 가장 짧은 매칭을 위한 정규 표현식
str_pat = re.compile(r'\"(.*)\"')
text1 = 'Computer says "no."'
str_pat.findall(text1) #['no.']
text2 = 'Computer says "no." Phone says "yes."'
str_pat.findall(text2) #['no." Phone says "yes.']


str_pat = re.compile(r'\"(.*?)\"')
text2 = 'Computer says "no." Phone says "yes."'
str_pat.findall(text2) #['no.', 'yes.']

######2.8 여러 줄에 걸친 정규 표현식 사용
comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = '''/*this is a
                multiline comment */
'''
comment.findall(text1)  #[' this is a comment ']
comment.findall(text2)  #[]

comment = re.compile(r'/\*((?:.|\n)*?)\*/')
comment.findall(text2) #['this is a\n                multiline comment ']

comment = re.compile(r'/\*((?:.|\n)*?)\*/',re.DOTALL)
comment.findall(text2) #['this is a\n                multiline comment ']

#####2.11 문자열에서 문자 잘라내기
#공백문 잘라내기
s = '     hello world \n'
s.strip() #'hello world'
s.lstrip() #'hello world \n'
s.rstrip() #'     hello world'

t = '-----hello===='
t.lstrip('-') #'hello===='
t.strip('-=') #'hello'

s = '     hello     world   \n'
s = s.strip()
s #'hello    world'

s.replace(' ','') #'helloworld'
import re
re.sub('\s+', ' ',s)

with open(filename) as f:
    lines = (line.strip() for line in f)
    for line in lines:

#####2.12 텍스트 정리
s = 'pýtĥöñ\fis\tawesome\r\n'
s #'pýtĥöñ\x0cis\tawesome\r\n'
remap = {
    ord('\t') : ' ',
    ord('\f') : ' ',
    ord('\r') : None #삭제됨
}
a = s.translate(remap)
a #'pýtĥöñ is awesome\n'

import unicodedata
import sys
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
b = unicodedata.normalize('NFD',a)
b #'pýtĥöñ is awesome\n'
b.translate(cmb_chrs) #'python is awesome\n'

digitmap = { c: ord('0') + unicodedata.digit(chr(c)) for c in range(sys.maxunicode) if unicodedata.category(chr(c)) == 'Nd' }
len(digitmap) #460
# 아라비아 숫자
x = '\u0661\u0662\u0663'
x.translate(digitmap) #>>>'123'

a #'pýtĥöñ is awesome\n'
b = unicodedata.normalize('NFD', a)
b.encode('ascii', 'ignore').decode('ascii') #'python is awesome\n'

def clean_spaces(s):
    s = s.replace('\r','')
    s = s.replace('\t',' ')
    s = s.replace('\f',' ')
    return s

#####2.13 텍스트 정렬
text = 'Hello World'
text.ljust(20)
text.rjust(20)
text.center(20)

text.ljust(20,'=')
text.center(20,'*')

format(text,'>20')
format(text,'<20')
format(text,'^20')

format(text,'=>20')
format(text,'*^20')

'{:>10s} {:>10s}'.format('Hello','World') #'     Hello      World'

x = 1.2345
format(x, '>10')
format(x,'^10.2f')

####2.14 문자열 합치기
parts = ['Is','Chicago', 'Not', 'Chicago?']
' '.join(parts) #'Is Chicago Not Chicago?'

a = 'Is Chicago'
b = 'Not Chicago'
print('{} {}'.format(a,b))

#소스 코드에서 문자열을 합치려고 할 때는 단순히 옆에 붙여 놓여 놓기만 해도 됨
a = 'Hello' 'World'
a

s = ''
for p in parts:
    s += p

#생성자 표현식
data = ['ACME', 50, 91.1]
','.join(str(d) for d in data) #'ACME,50,91.1'

print( a,b,c,sep=':')

####2.15 문자열에 변수 사용
s = '{name} has {n} messages.'
s.format(name='Guido', n=37)

name = 'Guido'
n = 37
s.format_map( vars() )

class Info:
    def __init__(self,name,n):
        self.name = name
        self.n = n
a = Info('Guido',37)
s.format_map(vars(a)) #'Guido has 37 messages.'

s.format(name='Guido')

class safesub(dict):
    def __missing__(self,key):
        return '{' + key + '}'
del n # n이 정의되지 않도록 함
s.format_map(safesub(vars())) #'Guido has {n } messages.'

import sys
def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))
name = 'Guido'
n =37
print( sub('Hello {name}')) #Hello Guido
print(sub('You have {n} messages.')) #You have 37 messages.
print(sub('Your favorite color is {color}')) #Your favorite color is {color }

######2.16 텍스트 열의 개수 고정
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
#     Look into my eyes, look into my
# eyes, the eyes, the eyes, the eyes, not
# around the eyes, don't look around the
# eyes, look into my eyes, you're under.

print(textwrap.fill(s, 40, subsequent_indent='    '))
# Look into my eyes, look into my eyes,
#     the eyes, the eyes, the eyes, not
#     around the eyes, don't look around
#     the eyes, look into my eyes, you're
#     under.

