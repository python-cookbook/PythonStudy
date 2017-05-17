1.18 시퀀스 요소에 이름 매핑(collections.namedtuple)

•    namedtuple 사용법
from collections import namedtuple

Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('abc@naver.com', '2012-10-19')
print(sub)
# Subscriber(addr='abc@naver.com', joined='2012-10-19')
print(sub.addr)
# abc@naver.com

a, b = sub
print(a)
# abc@naver.com
print(b)
# 2012-10-19

•    활용법
from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price'])


def comput_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total

# 가독성 좋고, 자료의 구조형에 영향 크게 안 받음
# but 수정할 수 없음

•    내용을 바꾸고 싶을때
from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price'])
s = Stock('a', 1, 2)
print(s)
# s.shares = 75 라고 바꾸려 해도 에러남. 수정 불가
s = s._replace(shares=75)
print(s)
# Stock(name='a', shares=75, price=2)
# 바꾸려면 _replace   (이때 _는 1개) 써야함

•    default 값 주고 필요할 때 내용만 추가하려면?
Stock = namedtuple('Stock', ['name', 'shares', 'price', 'date', 'time'])
stock_prototype = Stock('', 0, 0, None, None)


# 프로토타입 만들기
def dict_to_stock(s):
    return stock_prototype._replace(**s)


# 프로토타입에 내용 넣는 함수
a = {'name': 'a', 'price': 1}
print(dict_to_stock(a))
# Stock(name='a', shares=0, price=1, date=None, time=None)

1.19 데이터 변환하며 줄이기

•    신박한 생성자 표현식
nums = [1, 2, 3, 4, 5]
s = sum(x * x for x in nums)
print(s)
# 1*1 + 2*2 + 3*3 + 4*4 + 5*5 와 같음

•    딕셔너리에서 신박한 생성자 표현식
# 이 방법도 있고
portfolio = [{'name': 'a', 'shares': 1}, {'name': 'b', 'shares': 3}, {'name': 'c', 'shares': 5}]
min_shares = min(p['shares'] for p in portfolio)
print(min_shares)
# 1

# 요 방법도 있네!
min_shares = min(portfolio, key=lambda k: k['shares'])
print(min_shares)
# {'name': 'a', 'shares': 1}
print(min_shares['shares'])
# 1

1.20 여러 매핑을 단일 매핑으로 합치기(collections.ChainMap)

•    두 개 이상의 딕셔너리 한번에 검색하기
from collections import ChainMap

a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
c = ChainMap(a, b)
print(c['x'])
# 1
print(c['y'])
# 2
print(c['z'])
# 3 --> a부터 검색하고 없으면 b 검색.(중복키 있을 때는 첫번재 값만 사용)

•    ChainMap 의 값 변경하기(무조건 첫번째 딕셔너리에만 영향 줌)

c['z'] = 10
# 키가 둘다 있어도 첫번째 딕셔너리 value만 변경
c['w'] = 20
print(a)
# {'x': 1, 'z': 10, 'w': 20}
# 키가 둘다 없는 경우 첫번째 딕셔너리 value만 추가
c['y'] = 30
print(b)
# 변화 없음
# 첫 번째 딕셔너리에 없는 키는 바꿀 수 없음.

•    업그레이드 활용법

values = ChainMap()
values['x'] = 1
values = values.new_child()
# new_child()는 새로운 매핑 추가하는 함수
values['x'] = 2
values = values.new_child()
values['x'] = 3
print(values)
# ChainMap({'x': 3}, {'x': 2}, {'x': 1})
# 완전 신기함
print(values['x'])
# 3
# 키가 동일한 경우 마지막으로 넣은 value 값 출력
values = values.parents
# parents는 마지막 매핑 삭제하는 함수
print(values)
# ChainMap({'x': 2}, {'x': 1})

•    Chainmap 대신 update를 활용한 방법

a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
merged = dict(b)
merged.update(a)
print(merged['z'])
# 3. update 된 value가 출력됨
# but ChainMap 과는 달리 원본 딕셔너리 참조x
# 원본 딕셔너리 변경돼도 반영되지 않는 문제



2. 문자열과 텍스트

2.1 여러 구분자로 문자열 나누기(re.split)

• 문자열 나누기
import re

line = 'asdf fjdk; afed, fjek,asdf,    foo'
print(re.split(r'[;,\s]\s*', line))
# ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

line2 = re.split(r'(;|,|\s)\s*', line)
print(line2)
# ['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo']
# (  ) 캡처그룹 사용하면 분리기호도 결과에 포함됨

# 논캡쳐 그룹
print(re.split(r'(?:,|;|\s)\s*', line))
# ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
# (?   ) 이건 not 의 의미. sql 에서 [^ ] 와 같은 듯

• 순서 고려해서 문자열 나누기

line3 = line2[::2]
print(line3)
# ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
# [::2]는 0,2,4,6 번째 리스트 요소를 뽑아내줌

line4 = line2[1::2]
print(line4)
# [1::2]는 1,3,5,7 번째 리스트 요소를 뽑아냄

• 두 리스트 합치기
print(''.join(three + four for three, four in zip(line3, line4)))

2.2 문자열 처음이나 마지막에 텍스트 매칭(startswith, endswith)

• 첫 글자, 끝 글자에 특정 글자가 있는지 체크
a = 'Dabc.txt'
print(a.startswith('D'))
# True
print(a.endswith('txt'))
# True

• os.listdir 함수
import os

filenames = os.listdir('.')
# pythonclass 폴더에 있는 파일들이 나오네
# filenames = os.listdir('/')
# c:\ 에 있는 폴더, 파일들이 나오네
# filenames = os.listdir('..')
# pythonclass 상위폴더에 있는 폴더, 파일들이 나오네
print(filenames)

• 신기한 방법
print([name for name in filenames if name.endswith(('.c', '.zip'))])
# 마지막이 '.c'나 '.zip'으로 끝나는 파일리스트 뽑기
# endswith, startswith 에는 리스트 변수 절대 못 들어감!! 무조건 튜플 변수나 str 변수 들어가야 함.

print(any(name.endswith('.py') for name in filenames))
# 파일이름이 .py 로 끝나는게 하나라도 있으면 True 출력

• 특정 글자 있는지 체크하는 또 다른 방법
a = 'Dabc.txt'
print(a[-4:] == '.txt')
# True


#####################################################

# 2.3 쉘 와일드카드 패턴으로 문자열 매칭

# 텍스트 매칭(fnmatch 는 대소문자 구분x, fnmatchcase 는 구분 o)

from fnmatch import fnmatch, fnmatchcase
print(fnmatch('foo.txt', '*.txt'))
# True
print(fnmatch('foo.txt', '?oo.txt'))
# True
print(fnmatch('Dat45.csv','Dat[0-9]*'))
# True

# 활용

names = ['Data1.csv', 'Dat2.csv', 'config.ini','foo.py']
name_list = [name for name in names if fnmatch(name, 'Dat*.csv')]
print(name_list)
'''['Data1.csv', 'Dat2.csv']'''

# 활용2

addresses = ['5122 N CLARK ST', '1060 W ADDISON ST']
address_list = [address for address in addresses if fnmatchcase(address, '51[0-9][0-9] *CLARK*')]
print(address_list)
'''['5122 N CLARK ST']'''

#############################################################

# 2.4 텍스트 패턴 매칭과 검색

# 복잡한 텍스트 매칭(re 모듈)

text1 = '11/27/2012'
text2 = 'Nov 27, 2012'

import re

if re.match(r'(\d+)/(\d+)/(\d+)', text1):  # \d+ 는 하나 이상의 숫자 의미
    print(True)
else:
    print(False)

# 정규표현식 미리 컴파일해서 객체로 만들기

datapet = re.compile(r'(\d+)/(\d+)/(\d+)')
if datapet.match(text1): # match 는 문자열 처음에서 찾기 시도
    print(True)
else:
    print(False)

text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
print(datapet.findall(text))
'''['11/27/2012', '3/13/2013']'''

# 캡처그룹 사용하기( r'(\d+)/(\d+)/(\d+)' )

m = datapet.match('11/27/2012')
print(m.group(0))
'''11/27/2012'''
print(m.group(1))
'''11'''
print(m.group(2))
'''27'''
print(m.group(3))
'''2012'''
print(m.group())
'''('11', '27', '2012')'''

# findall() 과 finditer()

# 한번에 결과 얻으려면 findall()
# 텍스트 순환하며 (loop 돌며) 결과 얻으려면 finditer()

##########################################################

# 2.5 텍스트 검색과 치환

# 특정 텍스트 패턴을 다른 패턴으로 바꾸기

text = 'yeah, but no, but yeah'
print(text.replace('yeah','yep'))
''' yep, but no, but yep '''

# 좀더 복잡한 패턴 바꾸기

text = 'Today is 11/27/2012. Pycon starts 3/13/2013'
import re
print(re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)) # \3 --> (\d+) 중 3번째 꺼
''' Today is 2012-11-27. Pycon starts 2013-3-13 '''

# 컴파일링 하기

datapet = re.compile(r'(\d+)/(\d+)/(\d+)')
print(datapet.sub(r'\3-\1-\2', text))
''' Today is 2012-11-27. Pycon starts 2013-3-13 '''

# 신기한 콜백 함수

from calendar import month_abbr

text = 'Today is 11/27/2012. Pycon starts 3/13/2013'
datapet = re.compile(r'(\d+)/(\d+)/(\d+)')

def change_date(m):
    mon_name = month_abbr[int(m.group(1))]  # 11/27/2012 에서 group(1) 은 11
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))
print(datapet.sub(change_date, text))

''' Today is 27 Nov 2012. Pycon starts 13 Mar 2013 '''

###########################################################

# 2.6 대소문자 구별하지 않는 검색과 치환

# re 모듈, re.IGNORECASE 를 써야함

text = 'UPP, low, Mixed'
print(re.findall('upp', text, flags=re.IGNORECASE))

''' ['UPP'] '''

print(re.sub('UPP','up', text, flags=re.IGNORECASE))

''' up, low Mixed '''

###########################################################

# 2.7 가장 짧은 매칭 위한 정규 표현식

# 정규표현식은 가장 긴 텍스트를 greedy 하게 찾음

str_pat = re.compile(r'\"(.*)\"') # 이게 무슨 말이지?
text1 = 'Computer says "No." Phone says "Yes."'
print(str_pat.findall(text1))
''' ['No." Phone says "Yes.'] '''  # "No." 보다 " Phone says " 가 더 길어서 이걸 택함

# 가장 짧은 텍스트를 찾게 하려면(*? 를 씀)

str_pad = re.compile(r'\"(.*?)\"')
print(str_pat.findall(text1))
''' ['No." Phone says "Yes.'] ''' ### 왜 안되지??? #######################

############################################################

# 2.8 여러 줄에 걸친 정규 표현식 사용