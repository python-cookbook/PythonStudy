
# 6.5 딕셔너리를 xml 로 바꾸기

# 문제 파이썬 딕셔너리 데이터를 받아서 xml 로 바꾸고 싶다.

# 해결 xml.etree.ElementTree  라이브러리는 파싱에 일반적으로 사용하지만, xml 문서를 생성할 때 사용하기도 한다.
# 예를 들어 다음 함수를 고려해보자.


from xml.etree.ElementTree import Element

def dict_to_xml(tag,d):
    '''
    간단한  dict 를 xml 로 변환하기
    '''
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

# 예제는 다음과 같다.

s = { 'name': 'GOOG', 'shares': 100, 'price':490.1 }
e = dict_to_xml('stock', s)

e
#<Element 'stock' at 0x00000232A22769A8>


# 이 변환의 결과로 Element 인스턴스가 나온다. I/O를 위해서 xml.etree.ElementTree의 tostring() 함수로 이를 바이트 문자열로 변환해보자

from xml.etree.ElementTree import tostring

tostring(e)
#b'<stock><name>GOOG</name><shares>100</shares><price>490.1</price></stock>'


# 요소에 속성을 넣고 싶으면 set() 메소드를 사용한다.
e.set('_id', '1234')
tostring(e)
#b'<stock _id="1234"><name>GOOG</name><shares>100</shares><price>490.1</price></stock>'


# 토론 xml을 생성할 때 다눗ㄴ히 문자열을 사용하고 싶을 수도 있다.

def dict_to_xml_str(tag, d):
    '''
    Turn a simple dict of key/value pairs into XML
    '''
    parts = ['<{}>'.format(tag)]
    for key, val in d.items():
        parts.append('<{0}>{1}</{0}>'.format(key,val))
    parts.append('</{}>'.format(tag))
    return ''.join(parts)

# 하지만 이 작업을 수동으로 하면 코드가 엄청나게 복잡해질 수 있다
# 딕셔너리에 다음과 같이 특별한 문자가 포함되어 있다거나 하는 경우에...

d = { 'name' : '<spam>' }

# 문자열 생성
dict_to_xml_str('item',d)
#'<item><name><spam></name></item>'

# 올바른 xml 생성
e = dict_to_xml('item',d)
tostring(e)
#b'<item><name>&lt;spam&gt;</name></item>'


# 마지막 예제에서 <와 > 문자가 &lt; 와 &gt; 로 치환됨

# 이런 문자를 수동으로 이스케이핑하고 싶다면 아래와 같이.
from xml.sax.saxutils import escape, unescape
escape('<spam>')
#'&lt;spam&gt;'



#6.6 xml 파싱, 수정, 저장

# 문제
# xml 문서를 읽고, 수정하고, 수정 내용을 xml 에 반영하고 싶다면?

#해결
# xml.etree.ElementTree 모듈로 이 문제를 간단히 해결할 수 있다.
# 일반적인 방식으로 문서 파싱부터 시작한다.
# pred.xml 이라는 파일이 있다고 가정해보자.

# <?xml version="1.0"?>
# <stop>
#     <id>14791</id>
#     <nm>Clark &amp; Balmoral</nm>
#     <sri>
#         <rt>22</rt>
#         <d>North Bound</d>
#         <dd>North Bound</dd>
#     </sri>
#     <cr>22</cr>
#     <pre>
#         <pt>5 MIN</pt>
#         <fd>Howard</fd>
#         <v>1378</v>
#         <rn>22</rn>
#     </pre>
#     <pre>
#         <pt>15 MIN</pt>
#         <fd>Howard</fd>
#         <v>1867</v>
#         <rn>22</rn>
#     </pre>
# </stop>


# ElementTree로 이 문서를 읽고 수정하는 방법!!

from xml.etree.ElementTree import parse, Element
doc = parse('pred.xml')
root = doc.getroot()
root
#<Element 'stop' at 0x100770cb0>

# 요소 몇 개 제거하기
root.remove(root.find('sri'))
root.remove(root.find('cr'))


# <nm>...</nm> 뒤에 요소 몇 개 삽입하기
root.getchildren().index(root.find('nm'))
#1

e = Element('spam')
e.text = 'This is a test'
root.insert(2, e)

# 파일에 쓰기
doc.write('newpred.xml', xml_declaration=True)


# 결과적으로 생성된 xml 은 다음과 같다.

# <?xml version='1.0' encoding='us-ascii'?>
# <stop>
#     <id>14791</id>
#     <nm>Clark &amp; Balmoral</nm>
#     <spam>This is a test</spam>
#     <pre>
#         <pt>5 MIN</pt>
#         <fd>Howard</fd>
#         <v>1378</v>
#         <rn>22</rn>
#     </pre>
#     <pre>
#         <pt>15 MIN</pt>
#         <fd>Howard</fd>
#         <v>1867</v>
#         <rn>22</rn>
#     </pre>
# </stop>




# 6.7 네임스페이스로 xml 문서 파싱하기

# 문제
# xml 문서를 파싱할 때 xml 네임스페이스를 사용하고 싶다.

# 해결
# 다음과 같이 네임스페이스를 사용하는 문서를 고려해보자.

# <?xml version="1.0" encoding="utf-8"?>
# <top>
#     <author>David Beazley</author>
#     <content>
#         <html xmlns="http://www.w3.org/1999/xhtml">
#             <head>
#                 <title>Hello World</title>
#             </head>
#             <body>
#                 <h1>Hello World!</h1>
#             </body>
#         </html>
#     </content>
# </top>

# 이 문서를 파싱하고 일반적인 쿼리를 실행하면 모든 것이 너무 장황해서 그리 쉽게 동작하지 않는다.

# 동작하는 쿼리
doc.findtext('author')
#'David Beazley'

doc.find('content')
#<Element 'content' at 0x100776ec0>

# 네임스페이스 관련 쿼리(동작하지 않음)
doc.find('content/html')

# 조건에 맞는 경우에만 동작
doc.find('content/{http://www.w3.org/1999/xhtml}html')
#<Element '{http://www.w3.org/1999/xhtml}html' at 0x1007767e0>

# 동작하지 않음
doc.findtext('content/{http://www.w3.org/1999/xhtml}html/head/title')

# 조건에 일치함
# doc.findtext('content/{http://www.w3.org/1999/xhtml}html/'
# # ... '{http://www.w3.org/1999/xhtml}head/{http://www.w3.org/1999/xhtml}title')
# # 'Hello World'



#6.8. 관계형 데이터 베이스 작업

# 문제  관계형 데이터베이스에 선택, 삽입, 행 삭제 등의 작업을 하고 싶다

# 해결 파이썬에서 데이터 행을 나타내는 표준은 튜플 시퀀스이다.

stocks = [
    ('GOOG', 100, 490.1),
    ('AAPL', 50, 545.75),
    ('FB', 150, 7.45),
    ('HPQ', 75, 33.2),
]


# 입력이나 출력 데이터의 행은 튜플로 표현한다.

# 예시를 위해 파이썬의 sqlite3 모듈을 사용한다.

# 첫번째 단계는 데이터베이스를 연결하는 것이다. 일반적으로 connect() 함수에 데이터 베이스 이름, 호스트 이름, 사용자 이름, 암호 등 필요한 정보를 넣는다.

import sqlite3
db = sqlite3.connect('database.db')

# 데이터 관련 작업을 하기 위해서는 커서(cursor)를 만들어야 한다.
# 커서를 만든 후에 sql 쿼리를 실행 할 수 있다.
c = db.cursor()
c.execute('create table portfolio (symbol text, shares integer, price real)')
#<sqlite3.Cursor object at 0x10067a730>
db.commit()


# 데이터에 행의 시퀀스를 삽입하려면 다음 구문을 사용한다.
c.executemany('insert into portfolio values (?,?,?)', stocks)
#<sqlite3.Cursor object at 0x10067a730>
db.commit()

# 쿼리를 수행하려면 다음 구문을 사용한다.
for row in db.execute('select * from portfolio'):
    print(row)
# ('GOOG', 100, 490.1)
# ('AAPL', 50, 545.75)
# ('FB', 150, 7.45)
# ('HPQ', 75, 33.2)


# 사용자가 입력한 파라미터를 받는 쿼리를 수행하려면 ? 를 사용해 파라미터를 이스케이핑해야 한다.

min_price = 100
for row in db.execute('select * from portfolio where price >= ?',
                      (min_price,)):
    print(row)

# ('GOOG', 100, 490.1)
# ('AAPL', 50, 545.75)




#6.9 16진수 인코딩, 디코딩

# 문제 문자열로 된 16진수를 바이트 문자열로 디코딩하거나, 바이트 문자열을 16진법으로 인코딩해야 한다.

# 해결  문자열을 16진수로 인코딩하거나 디코딩하려면 binascii 모듈을 사용한다.

#최초 바이트 문자열
s = b'hello'

# 16진법으로 인코딩
import binascii
h = binascii.b2a_hex(s)
h
#b'68656c6c6f'

# 바이트로 디코딩
binascii.a2b_hex(h)
#b'hello'

# base64 모듈에도 유사한 기능이 있다.

import base64
h = base64.b16encode(s)
h
#b'68656C6C6F'

base64.b16decode(h)
#b'hello'






#chapter 7. 함수


# def 구문으로 함수를 정의하는 것은 모든 프로그램의 기초가 된다.
# 이번 장에서는 좀 더 고급 기능과 잘 사용하지 않는 함수 정의, 사용 패턴에 대해 알아본다
# 기본 인자, 인자 수에 구애받지 않는 함수, 키워드 인자, 주석, 클로저 등이 주제에 포함된다.



## 7.1 매개변수 개수에 구애받지 않는 함수 작성 ##############

# 문제 입력 매개변수 개수에 제한이 없는 함수를 작성하고 싶다

# 해결 위치 매개변수의 개수에 제한이 없는 함수를 작성하려면 * 인자를 사용한다.

def avg(first, *rest):
    return (first + sum(rest)) / (1 + len(rest))

# 샘플
avg(1, 2) # 1.5
avg(1, 2, 3, 4) # 2.5

# 이 예제에서 rest에 추가적 위치 매개변수가 튜플로 들어간다. 코드는 추구 작업에서 이를 하나의 시퀀스로 다룬다.

# 키워드 매개변수 수에 제한이 없는 함수를 작성하려면 **로 시작하는 인자를 사용한다.

import html

def make_element(name, value, **attrs):
    keyvals = [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(
                name=name,
                attrs=attr_str,
                value=html.escape(value))
    return element



#7.2 키워드 매개 변수만 받는 함수 작성

#문제  키워드로 지정한 특정 매개변수만 받는 함수가 필요하다
# 이 기능은 키워드 매개변수를 * 뒤에 넣거나 이름없이 *만 사용하면 간단히 구현할 수 있다

def recv(maxsize, *, block):
    'Receives a message'
    pass

recv(1024, True) # TypeError
recv(1024, block=True) # Ok


#이 기술로 숫자가 다른 위치 매개변수를 받는 함수에 키워드 매개변수를 명시할 때 사용할 수 있다.

def mininum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m

minimum(1, 5, 2, -5, 10) # -5반환
minimum(1, 5, 2, -5, 10, clip=0) # 0반환


# 토론
# 키워드로만 넣을 수 있는 인자는 추가적 함수 인자를 명시할 때 코드의 가독성을 높이는 좋은 수단이 될 수 있다.

msg = recv(1024, False)

msg = recv(1024, block=False)

#위의 식보단 아래의 식이 가독성이 더 좋음
# 키워드로만 넣을 수 있는 인자는 **kwargs 와 관련된 것에 사용자가 도움을 요청하면 도움말 화면에 나타난다!

>>> help(recv)
Help on function recv in module __main__:
recv(maxsize, *, block)
    Receives a message



# 7.3  함수 인자에 메타데이터 넣기
# 문제 함수를 작성했다. 이때 인자에 정보를 추가해서 다른 사람이 함수를 어떻게 사용해야 하는지 알 수 있도록 하고싶다.
# 해결 함수 인자 주석으로 프로그래머에게 이함수를 어떻게 사용해야 할지 정보를 줄 수 있다.


def add(x:int, y:int) -> int:
    return x + y


help(add)
#Help on function add in module __main__:
add(x: int, y: int) -> int

#어떤 객체도 함수에 주석으로 붙일 수 있지만 (ex. 숫자,문자열, 인스턴스) 대개 클래스나 문자열이 타당하다.


# 토론

# 함수의 주석은 __annotations__ 속성에 저장된다.
add.__annotations__
{'y': <class 'int'>, 'return': <class 'int'>, 'x': <class 'int'>}





# 7.4 함수에서 여러값을 반환

# 함수에서 값을 여러개 반환하고 싶다.

# 해결 튜플사용!


def myfun():
#return 1, 2, 3
a, b, c = myfun()
print(a)
#1
print(b)
#2
print(c)
#3




# 토론
# myfun()이 여러개 값을 반환하는 것처럼 보이지만 , 사실은 튜플 하나를 반환한 것이다. 실제로 튜플을 생성하는 것은 쉼표지 괄호가 아니다


a = (1, 2) #괄호 사용
print(a)
#(1, 2)
b = 1, 2   #괄호 미사용시
print(b)
#(1, 2)

# 튜플을 반환하는 함수를 호출할 때, 겨로가 값을 여러개의 변수에 넣는 것이 일반적이다. 이는 레시피 1.1 에 나왔던 튜플 언패킹이다. 반환값을 변수 하나에 할당할 수도 있다.


x = myfun()
print(x)
#(1, 2, 3)



# 7.5 기본 인자를 사용하는 함수 정의

# 문제 함수나 메소드 정의 시 하나 혹은 그 이상 인자에 기본값을 넣어 선택적으로 사용하고 싶을때
# 표면적으로 선택적 인자를 사용하는 함수를 정의하기는 어려움 함수 정의부에 값을 할당하고 가자 뒤에 이를 위치시킨다

def spam(a, b=42):
    print(a,b)
spam(1)   #1 42
spam(1,2) #1 2

#기본값이 리스트,세트, 딕셔너리 등 수정 가능한 컨테이너여야 한다면 None사용해 코드 작성!

#기본 값으로 리스트 사용  기본값을 제공하는 대신 함수가 받은 값이 특정 값인지 아닌지 확인하기 위한 코드

_no_value = object()

def spam(a, b=_no_value):
    if b is _no_value:
        print('No b value supplied')

# 작동!

spam(1)
No b value supplied
spam(1, 2) # b = 2
spam(1, None) # b = None

#위 코드 None값을 전달시와 비전달시 차이점 확인!

# 토론 할당하는 기본 값은 함수를 정의할 때 한번만 정해지고 그 후엔 변하지 않는다

x = 42
def spam(a, b=x):
    print(a,b)
spam(1) # 1 42
x=23    # 효과 없음
spam(1)  # 1 42
# 변수 x 값을 바꾸어도 값 안 바뀜. 기본 값은 함수를 정의할 때 정해지기 때문

# 기본적으로 사용하는 값은 None,True,False,숫자,문자열 같이 항상 변하지 않는 객체 사용
#def spam(a, b=[]) #절대 안됨!!
#기본 값이 함수를 벗어나서 수정되는 순간 많은 문제가 발생  값이 변하면 기본값이 변하게 되고 추후 함수 호출에 영향을 주게된다.

def spam(a,b=[]):
    print(b)
    return b

x = spam(1)
x
x.append(99)
x.append('Yow!')
spam(1) #수정된 리스트가 반환됨

# 이런 부작용을 피하려면 기본값으로 Nond을 할당하고 함수 내부에서 확인해야하는것이 좋다
# None 확인 시 is연산자를 사용하는 것이 매우 중요중요!


def spam(a,b=None):
    if not b: #주의 b is None 사용
        b= []


spam(1) # 바른 코드
x = []
spam(1, x) # 에러. x 값이 기본으로 덮어쓰여진다
spam(1, 0) # 에러. 0이 무시된다.
spam(1, '') # 에러. ''이 무시된다.



# 7.6 이름 없는 함수와 인라인 함수 정의

# 문제 sort() 등에 사용할 짧은 콜백 함수를 만드렁야 하는데, 한 줄짜리 함수를 만들면서 def 구문까지 사용하고 싶지는 않다. 대신 in line 이라 불리는 짧은 함수를 만들고 싶다.

# 해결  표현식 계산 외에 아무일도 하지 않는 간단한 함수는 lambda 로 치환할 수 있다.


add = lambda x, y: x + y
add(2,3)
#5
add('hello', 'world')
#'helloworld'



#앞에 나온 lambda 는 다음 예제 코드와 완전히 동일하다

def add(x, y):
    return x + y
add(2,3)
#5

# 일반적으로 lambda는 정렬이나 데이터 줄이기 등 다른 작업에 사용할 때 많이 쓴다.

names = ['David Beazley', 'Brian Jones',
         'Raymond Hettinger', 'Ned Batchelder']
sorted(names, key=lambda name: name.split()[-1].lower())
#['Ned Batchelder', 'David Beazley', 'Raymond Hettinger', 'Brian Jones']

# 작은 함수를 많이 사용하거나, 콜백 함수를 사용하는 프로그램에서 종종 lambda를 발견하게 된다 .



#7.7 이름 없는 함수에서 변수 고정


x = 10
a = lambda y: x + y
x = 20
b = lambda y: x + y


# a(10) 과 b(10)의 값은 30!

# lambda에서 사용한 x 값이 실행 시간에 달라지는 변수라는 점이다. 따라서 람다 표현식의 x의 값은 그 함수를 실행할 때의 값이 된다.


x = 15
a(10)
#25
x = 3
a(10)
#13

# 이름없는 함수를 정의할때 특정 값을 고정하고 싶으면 그 값을 기본값으로 지정하면 된다.

x = 10
a = lambda y, x=x: x + y
x = 20
b = lambda y, x=x: x + y
a(10)
#20
b(10)
#30


funcs = [lambda x: x+n for n in range(5)]
for f in funcs:
print(f(0))

'''
4
4
4
4
4
'''

#위 아래 식의 차이점을 기억할것.

funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
print(f(0))

'''
0
1
2
3
4
'''