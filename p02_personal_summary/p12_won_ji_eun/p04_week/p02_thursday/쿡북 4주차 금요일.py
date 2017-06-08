            #6.5 딕셔너리를 XML로 바꾸기

#문제 : xml.etree.ElementTree 사용

from xml.etree.ElementTree import Element 
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
#실행결과 <Element 'stock' at 0x00000000099040E8>

from xml.etree.ElementTree import tostring
print(tostring(e))
#실행결과 b'<stock><name>GOOG</name></stock>'


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

from xml.sax.saxutils import escape, unescape 
e = escape('<spam>')
print(unescape(e))
#실행결과 <spam>


            # 6.6 XML 파싱,수정,저장

#문제: XML 문서 읽고, 수정하고, XML에 수정 반영

from xml.etree.ElementTree import parse, Element
doc = parse('d:/data/pred.xml')
root = doc.getroot()
print(root)

root.remove(root.find('sri')) 
root.remove(root.find('cr'))

root.getchildren().index(root.find('nm')) 
e = Element('spam')
e.text = 'This is a test'
root.insert(2, e)

doc.write('d:/data/newpred.xml', xml_declaration=True) 



            #6.7 네임스페이스로 XML 문서 파싱

#문제: XMl 네임스페이스 사용

from xml.etree.ElementTree import parse, Element
doc = parse('d:/data/sample.xml')
# 동작하는 쿼리
print(doc.findtext('author')) 
print(doc.find('content'))

# 네임스페이스 관련 쿼리(동작 안함)
print(doc.find('content/html')) 

# 조건에 맞는 경우 동작
print(doc.find('content/{http://www.w3.org/1999/xhtml}html')) 
# 동작 안함 
print(doc.findtext('content/{http://www.w3.org/1999/xhtml}html/head/title')) 

class XMLNamespaces:
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

# iterparse() 사용
from xml.etree.ElementTree import iterparse
for evt, elem in iterparse('ns2.xml', ('end', 'start-ns', 'end-ns')):
    print(evt, elem)



            # 6.8 관계형 데이터 베이스 작업

#문제: 관계형 데이터베이스에 선택, 삽입, 행 삭제하기

stocks = [
          ('GOOG', 100, 490.1),
          ('AAPL', 50, 545.75),
          ('FB', 150, 7.45),
          ('HPQ', 75, 33.2)
         ]

import sqlite3 
db = sqlite3.connect('database.db')
print(db)
#실행결과  <sqlite3.Connection object at 0x000000000282BC70>

c = db.cursor()
print(c.execute('create table portfolio (symbol text, shares integer, price real)'))
db.commit()
#실행결과 <sqlite3.Cursor object at 0x0000000009874880> 

c.executemany('insert into portfolio values (?,?,?)', stocks) 
db.commit()

for row in db.execute('select * from portfolio'): 
    print(row)
    
#실행결과
('GOOG', 100, 490.1)
('AAPL', 50, 545.75)
('FB', 150, 7.45)
('HPQ', 75, 33.2)

min_price = 100 
for row in db.execute('select * from portfolio where price >= ?',(min_price,)):
    print(row)
#실행결과 
('GOOG', 100, 490.1)
('AAPL', 50, 545.75)


            # 6.9 16진수 인코딩,디코딩

#문제: 16진수로 인코딩, 디코딩

s = b'hello' 

import binascii 
h = binascii.b2a_hex(s)
binascii.a2b_hex(h) 

import base64 
h = base64.b16encode(s)
base64.b16decode(h)




                    # Chapter 7 함수

            #7.1 매개변수 개수에 구애받지 않는 함수 작성
#입력 매개변수에 제한이 없는 함수를 작성하고 싶다,
#해결방법 : * 인자를 사용

def avg(first, *rest) :
    return (first + sum(rest)/ (1 + len(rest)))

#sample
avg(1,2)
#실행결과 1.5
avg(1,2,3,4)
#실행결과 2.5

import html

def make_element(name, value, **attrs):
    keyvals= [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(name = name, attrs=attr_str, value=html.escape(value))
    return element

# 매개변수와 키워드 매개변수를 동시에 받는 함수를 작성하려면 *와 **를 함께 사용하면 된다
def anyargs(*args, **kwargs):
    print(args) #tuple
    print(kwargs) #dictionary
    
         
    
         
             #7.3 함수 인자에 메타데이터 넣기

#문제 함수를 작성할 때 인자에 정보를 추가하고 싶다.
    #해결방법 함수인자주석
    
def add(x:int, y:int) -> int:
    return x+y
    
    
help(add)

# 실행결과 
Help on function add in module __main__:]: 
add(x:int, y:int) -> int
    
    
   
           #7.4 함수에서 여러 값을 반환
           
# 문제 함수에서 값을 여러개 반환하고 싶다,
    # 해결방법
def myfun():
    return 1,2,3

a,b,c = myfun()

a
#실행결과 1
b
#실행결과 2
c
#실행결과 3



            #7.5 기본 인자를 사용하는 함수 정의

#문제 함수나 메소드를 정의할 때 하나 혹은 그 이상 인자에 기본 값을 넣어 선택적으로 사용할 수 있도록 하고 싶다

def spam(a, b=42):
    print(a,b)
    
spam(1)
#실행결과 1 42
spam(1,2)
#실행결과 1 2
def spam(a, b=None):
    if b is None:
        b = []
        

# 함수가 받은 값이 특정 값인지 아닌지 확인하려면 다음 코드를 사용
_no_value = object()

def spam(a,b=_no_value):
    if b is _no_value:
        print ('No b value supplied')
        
spam(1)
No b value supplied
spam(1,2)
spam(1, None)
    
    
    
            #7.6 이름 없는 함수와 인라인 함수 정의

#문제 한줄 짜리 함수를 만들면서 def 구문까지는 사용하고 싶지 않을 때
#해결방법 lambda 함수 사용

add = lambda x, y : x + y
add(2,3)
    
#실행결과 5

add('hello', 'world')
#실행결과 'helloworld'

names = ['David Beazley', 'Brian Jones', 'Raymond Hettinger', 'Ned Batchelder']
sorted(names, key=lambda name: name.split()[-1].lower())
#실행결과 ['Ned Batchelder', 'David Beazley', 'Raymond Hettinger', 'Brian Jones']
    
    
    
            #7.7 이름없는 함수에서 변수 고정
# lambda를 사용해서 이름 없는 함수를 정의했는데, 정의할 때 특정 변수의 값을 고정하고 싶다.

x = 10

a = lambda y : x+y

x= 20

b = lambda y : x+y

a(10)
#실행결과 30
b(10)   
#실행결과 30



# lambda에서 사용한 x값이 실행 시간에 달라지는 변수
x=15
a(10)
#실행결과 25

x=3
a(10)
#실행결과 13

x=10
a = lambda y, x=x: x+y
x=20
b=lambda y, x=x:x+y
a(10)
#실행결과 20
    
b(10)
#실행결과 30

  
    
    
    
    
    