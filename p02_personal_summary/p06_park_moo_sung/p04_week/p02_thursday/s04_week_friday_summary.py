##########################################################

# 6.5 딕셔너리를 XML로 바꾸기

# xml.etree.ElementTree 라이브러리

from xml.etree.ElementTree import Element # 요소 순서 맞출 때는 OrderedDict 사용하기(1.7)
def dict_to_xml(tag, d):
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
        return elem
s = {'name': 'GOOG', 'shares': 100, 'price': 490.1}
e = dict_to_xml('stock', s)
print(e)

from xml.etree.ElementTree import tostring
print(tostring(e))


# 단순히 문자열을 사용하고 싶을 때

def dict_to_xml_str(tag, d):
    parts = ['<{}>'.format(tag)]
    for key, val in d.items():
        parts.append('<{0}>{1}</{0}>'.format(key,val))
        parts.append('</{}>'.format(tag))
        return ''.join(parts)
d = {'name': '<spam>'}
dict_to_xml_str('item',d)
e = dict_to_xml('item',d)
print(tostring(e))

from xml.sax.saxutils import escape, unescape # 수동으로 이스케이핑하고 싶을 때
e = escape('<spam>')
print(unescape(e))

#############################################################

# 6.6 XML 파싱,수정,저장

# XML 문서 읽고, 수정하고, XML에 수정 반영

from xml.etree.ElementTree import parse, Element
doc = parse('d:/data/pred.xml')
root = doc.getroot()
print(root)

root.remove(root.find('sri')) # 요소 제거
root.remove(root.find('cr'))

root.getchildren().index(root.find('nm')) # 뒤에 요소 삽입
e = Element('spam')
e.text = 'This is a test'
root.insert(2, e)

doc.write('d:/data/newpred.xml', xml_declaration=True) # 파일 쓰기

###############################################################

# 6.7 네임스페이스로 XML 문서 파싱

# XMl 네임스페이스 사용하기

from xml.etree.ElementTree import parse, Element
doc = parse('d:/data/sample.xml')
print(doc.findtext('author')) # 동작하는 쿼리
print(doc.find('content'))

print(doc.find('content/html')) # 네임스페이스 관련 쿼리(동작 x)

print(doc.find('content/{http://www.w3.org/1999/xhtml}html')) # 조건에 맞는 경우 동작
print(doc.findtext('content/{http://www.w3.org/1999/xhtml}html/head/title')) # 동작 x

class XMLNamespaces: # 클래스 만들기
    def __init__(self, **kwargs):
        self.namespaces = {}
        for name, uri in kwargs.items():
            self.register(name, uri)
    def register(self, name, uri):
        self.namespaces[name] = '{'+uri+'}'
    def __call__(self, path):
        return path.format_map(self.namespaces)

ns = XMLNamespaces(html='http://www.w3.org/1999/xhtml')
print(doc.find(ns('content/{html}html')))
print(doc.findtext(ns('content/{html}html/{html}head/{html}title')))

# iterparse() 사용해서 네임스페이스 처리 범위 정보 얻기

from xml.etree.ElementTree import iterparse
for evt, elem in iterparse('ns2.xml', ('end', 'start-ns', 'end-ns')):
    print(evt, elem)

###########################################################

# 6.8 관계형 데이터 베이스 작업

# 관계형 데이터베이스에 선택, 삽입, 행 삭제하기

stocks = [
          ('GOOG', 100, 490.1),
          ('AAPL', 50, 545.75),
          ('FB', 150, 7.45),
          ('HPQ', 75, 33.2)
         ]

import sqlite3 # 데이터베이스에 연결
db = sqlite3.connect('database.db')
print(db)

c = db.cursor() # 커서 먼저 만들어야 함
print(c.execute('create table portfolio (symbol text, shares integer, price real)'))
db.commit()

c.executemany('insert into portfolio values (?,?,?)', stocks) # 행의 시퀀스 삽입
db.commit()

for row in db.execute('select * from portfolio'): # 쿼리 수행
    print(row)

min_price = 100 # 입력한 파라미터를 받는 쿼리 수행 위해서는 ? 이용해 파라미터 이스케이핑 해야 함
for row in db.execute('select * from portfolio where price >= ?',(min_price,)):
    print(row)

####################################################

# 6.9 16진수 인코딩,디코딩

# 16진수로 인코딩하고 디코딩하기

s = b'hello' # 최초 바이트 문자열

import binascii # 16진법으로 인코딩
h = binascii.b2a_hex(s)

binascii.a2b_hex(h) # 바이트로 디코딩

import base64 # base64 모듈 사용
h = base64.b16encode(s)

base64.b16decode(h)

#####################################################

# 7.1 매개변수 개수에 구애받지 않는 함수 작성

# 입력 매개변수 개수에 제한 없는 함수(* 인자 사용)

def avg(first, *rest):
    return (first + sum(rest)) / (1 + len(rest))

print(avg(1, 2))
print(avg(1, 2, 3, 4))

# 키워드 매개변수 수에 제한 없는 함수(** 인자 사용)

import html

def make_element(name, value, **attrs):
    keyvals = [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(name=name,attrs=attr_str,value=html.escape(value))
    return element

print(make_element('item', 'Albatross', size='large', quantity=6))
print(make_element('p', '<spam>'))

# 위치 매개변수, 키워드 매개변수 동시 사용 함수

def anyargs(*args, **kwargs):
    print(args) # 튜플
    print(kwargs) # 딕셔너리

####################################################

# 7.2 키워드 매개 변수만 받는 함수 작성

def recv(maxsize, *, block):
    'Receives a message'
    pass

print(recv(1024, True)) # 타입 에러
print(recv(1024, block=True)) # 가능

def mininum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m

print(mininum(1, 5, 2, -5, 10))  # -5 리턴
print(mininum(1, 5, 2, -5, 10, clip=0)) # 0 리턴


##################################################

# 7.3 함수 인자에 메타데이터 넣기

# 인자에 정보 추가하기

def add(x:int, y:int) -> int: # 실행에 아무런 영향 x. 단지 소스 코드 이해에 도움 줄 뿐
    return x + y

# 함수 주석은 함수의 __annotations__ 속성에 저장됨


####################################################

# 7.4 함수에서 여러 값을 반환

def myfun():
    return 1, 2, 3
a, b, c = myfun()
print(a)
print(b)
print(c)

a = (1,2) # 괄호 사용
print(a)

b = 1,2   # 괄호 미사용 --> 튜플을 생성하는 것은 쉼표이므로 튜플 형태로 출력됨 !!!
print(b)

x = myfun()
print(x)

#############################################################

# 7.5 기본 인자를 사용하는 함수 정의

# 하나 혹은 그 이상 인자에 기본 값 넣어 선택적으로 사용하는 방법

def spam(a, b=42):
    print(a, b)
spam(1)    # a=1, b=42
spam(1, 2) # a=1, b=2

# 기본값 수정 가능한 컨테이너여야 하는 경우(None 사용)

def spam(a, b=None):
    if b is None:
        b = []

# 기본값을 제공하는 대신 함수가 받은 값이 특정 값인지 아닌지 확인하는 경우

_no_value = object()

def spam(a, b=_no_value):
    if b is _no_value:
        print('No b value supplied')

print(spam(1))
## No b value supplied
print(spam(1,2))
## b = 2
print(spam(1,None))
## b=None

# 주의사항 1. 할당하는 기본값은 한번만 정해지고 변하지 않음

x = 42
def spam(a, b=x):
    print(a, b)

print(spam(1))

x = 23
print(spam(1)) # x=23으로 변경해도 1 42으로 출력됨

# 주의사항 2. 기본값은 None, True, False, 숫자, 문자열 등 항상 변하지 않는 값으로 해야 함

def spam(a, b=[]): # [] 처럼 변하는 값으로 해서는 X
    print(b)
    return b
x = spam(1)
print(x)

x.append(99)
x.append('Yow!')

print(x)
print(spam(1))
## [99, 'Yow!'] 라고 수정된 리스트 반환 .... 이해가 잘 안되네..

######################################################

# 7.6 이름 없는 함수와 인라인 함수 정의

# lambda

add = lambda x, y: x + y
print(add(2,3))
print(add('hello', 'world'))

# lambda 는 정렬, 데이터 줄일 때 많이 사용

names = ['David Beazley', 'Brian Jones','Raymond Hettinger', 'Ned Batchelder']
print(sorted(names, key = lambda name : name.split()[-1].lower()))

#########################################################

# 7.7 이름 없는 함수에서 변수 고정

x = 10
a = lambda y: x + y

x = 20
b = lambda y: x + y

print(a(10))
print(a(10)) # 둘다 x=20 일 때의 값으로 출력(람다 표현식의 x 값은 그 함수를 실행할 때의 값이 됨

# 특정 값 고정하기

x = 10
a = lambda y, x=x : x + y

x = 20
b = lambda y, x=x : x + y

print(a(10)) # x=10일 때의 값
print(b(10)) # x=20일 때의 값

# 고급 활용법(이터레이터)

funcs = [lambda x : x+n for n in range(5)]
for f in funcs:
    print(f(0)) # 이러면 람다 함수는 가장 마지막 n(n=4)을 사용함

# 중요!!!!! n 값을 함수 정의하는 시점의 값으로 고정해놓고 사용해야 함!!!!!
funcs = [lambda x, n=n : x+n for n in range(5)]
for f in funcs:
    print(f(0))

