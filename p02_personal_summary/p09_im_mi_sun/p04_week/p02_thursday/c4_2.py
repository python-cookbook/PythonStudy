#############6.5 딕셔너리를 XML로 바꾸기
#파이썬 딕셔너리 데이터 > XML 변환
# xml.etree.ElementTree ( 파싱에 일반적으로 사용): xml파일 생성 시 사용
from xml.etree.ElementTree import Element

def dict_to_xml(tag,d):
    elem = Element(tag)         #Element : 태그 생성함수 <tag>이렇게 만듦
    for key, val in d.items():
        child = Element(key)
        child.text=str(val)    # <key>val</key>
        elem.append(child)      #<tag><key>val</key></tag>
    return elem

s = {'name':'GOOG','shares':100,'price':490.1}
e= dict_to_xml('stock',s)
print(e) # 결과값으로 Element 인스턴스가 나옴 #I/O를 위해 tostring()함수로 바이트 문자열로 변환
        #<Element 'stock' at 0x1006cd958>
from xml.etree.ElementTree import tostring
print(tostring(e))     #b'<stock><name>GOOG</name><shares>100</shares><price>490.1</price></stock>'
#요소에 속성을 추가하고 싶은 경우 set() 사용
e.set('_id','1234')
print(tostring(e)) #b'<stock _id="1234"><name>GOOG</name><shares>100</shares><price>490.1</price></stock>'

#요소의 순서를 맞춰야한다면 일반 딕셔너리 대신 Ordered Dict 사용

#XML생성 시 단순히 문자열 사용하고 싶은 경우
def dict_to_xml_str(tag,d):
    parts=['<{}>'.format(tag)]
    print('1',parts)                                    #1 ['<item>']
    for key,val in d.items():
        parts.append('<{0}>{1}</{0}>'.format(key,val))
        print('2',parts)                                #2 ['<item>', '<name><spam></name>']
    parts.append('</{}>'.format(tag))
    print('3',parts)                                    #3 ['<item>', '<name><spam></name>', '</item>']
    return ''.join(parts)

d={'name':'<spam>'}
#문자열 생성
dict_to_xml_str('item',d)
#올바른 XML생성
e=dict_to_xml('item',d)
print(tostring(e)) #b'<item><name>&lt;spam&gt;</name></item>'
                    #<>이 문자로 치환됨
                    #문자를 수동으로 이스케이핑 하고 싶은 경우 xml.sax.saxutils escape(), unescape() 사용
from xml.sax.saxutils import escape, unescape
print(escape('<spam>')) #&lt;spam&gt;
print(unescape('<spam>')) #<spam>

        #escape : 데이터중 HTML형식을 가질만한 문자열을 브라우저끼리 약속된 형태의 안전한 예약문자열로 변환하는 것.
        # unescape : escape 된 문자열을 다시 원래 형태의 데이터 문자열로 변환하는 작업

#############6.6 XML파싱, 수정, 저장
#XML문서 읽기,수정, 수정내용 XML반영
#xml.etree.Elementree

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
# </pre>
# <pre>
#     <pt>15 MIN</pt>
#     <fd>Howard</fd>
#     <v>1867</v>
#     <rn>22</rn>
#        </pre>
# </stop>

from xml.etree.ElementTree import parse,Element
doc = parse('/Users/misoni/Desktop/cookbookStudy/pred.xml')
root = doc.getroot()
print(root) #<Element 'stop' at 0x1007cd958>

#요소 몇개 제거하기
root.remove(root.find('sri'))
root.remove(root.find('cr'))
print(root)

#<nm>..</nm> 뒤에 요소 몇개 삽입하기
root.getchildren().index(root.find('nm'))
e=Element('spam')
e.text='This is a test'
root.insert(2,e)

#파일에 쓰기
doc.write('newpred.xml',xml_declaration=True)

#XML수정시 부모 요소에도 영향을 미치기 때문에 리스트처럼 다뤄짐
#요소 제거시 부모의 remove()를 사용해 바로위에 있는 부모로부터 제거
#새로운 요소 추가 시 element[i], element[i:j] 와 같이 인덱스 슬라이스 명령으로 접근 가능 (6.5참고)

#############6.7 네임 스페이스로 XML문서 파싱
# XML문서 파싱 시 XML 네임스페이스 사용
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



########여기서 부터 모르겠음(빠이염)

#동작하는 쿼리
# doc.findtext('author') #'David Beazley'
# doc.find('content') #<Element 'content' at 0x10076ec0>
#
# #네임 스페이스 관련 쿼리(동작하지 않음)
# doc.find('content/html')
# #조건에 맞는 경우에만 동작
# doc.find('content/{http://www.w3.org/1999/xhtml}html')
# #동작하지 않음
# doc.findtext('content/{http://www.w3.org/1999/xhtml}html/head/title')
# #조건에 일치
# doc.findtext('content/{http://www.w3.org/1999/xhtml}html/'
# ... '{http://www.w3.org/1999/xhtml}head/{http://www.w3.org/1999/xhtml}title') 'Hello World'


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
doc.find(ns('content/{html}html')) #<Element '{http://www.w3.org/1999/xhtml}html' at 0x1007767e0>
doc.findtext(ns('content/{html}html/{html}head/{html}title')) #'Hello World'


#############6.8 관계형 데이터 베이스 작업
#관계형 데이터 베이스에 선택,삽입, 행삭제(select,insert,delete row)등의 작업
#파이썬에서 행을 나타내는 표준은 튜플 시퀀스
stocks = [('GOOG',100,490.1),('APPL',50,545.75),('FB',150,7,45),('HPQ',75,33.2)]
#입력/출력 데이터 행은 튜플로 표현
#step1.데이터 베이스 연결 :connect
import sqlite3
db = sqlite3.connect('database.db')

#커서 생성 후 sql문 실행
c = db.cursor()
c.execute('create table portfolio (symbol text, shares integer, price real)')
#<sqlite3.Cursor object at 0x103450810>
db.commit()

#데이터에 행의 시퀀스 삽입
c.executemany('insert into portfolio values (?,?,?)',stocks)
db.commit()

#쿼리 수행
for row in db.execute('select * from portfolio'):
    print(row) #[?]결과가 안나오는디

#사용자가 입력한 파라미터를 받는 쿼리 수행시 파라미터를 이스케이핑 해야함
min_price=100
for row in db.execute('select * from portfolio where price >= ?', (min_price,)):
    print(row) #[?] r결과가 안나와 min_price엔 왜 ,가 붙는거야

#데이터 베이스 자료를 파이썬 타입에 매핑할 때 데이터 타입이 달라지기 때문에 문서를 잘 읽어야함
#SQL구문 문자열의 서식화 (파이썬의 연산자 %, .format()) 메소드로 문자를 만들면 안됨)
#...모르겠어 빠이

#############6.9 16진수 인코딩, 디코딩
#문자열 16진수 > 문자열 디코딩
#바이트 문자열> 16진법 인코딩
#binascii

#최초 바이트 문자열
s= b'hello'
#16진법 인코딩
import binascii
h=binascii.b2a_hex(s)
print(h) #b'68656c6c6f'

#바이트로 디코딩
binascii.a2b_hex(h) #b'hello'

#base64 모듈에도 유사한 기능이 있음
import base64
h=base64.b16encode(s)
print(h) #b'68656C6C6F'
base64.b16decode(h)

#16진법 전환은 쉽게 수행가능
#binascii는 대소문자 상관x ( base64.b16decode(), base64.b16encode() 대문자에만 동작)
#인코딩 함수가 만들 출력물은 언제나 바이트 문자열
#반드시 유니코드를 사용해야 할 경우 디코딩 과정 추가
h=base64.b16encode(s)
print(h) #b'68656C6C6F'
print(h.decode('ascii'))
#16진수 디코딩 시 b16decode()와 a2b_hex()함수는 바이트혹은 유니코드 문자열을 받음 이때 반드시!!ascii로 인코딩한  16진수가 포함되어 있어야함


####7.1매개 변수 개수에 구애 받지 않는 함수 작성
#입력 매개변수 제한 없는 함수 생성
# * 인자 사용
def avg(first, *rest):
    return (first+sum(rest)) / ( 1+len(rest))
avg(1,2,3) #2.0

#키워드 매개변수 수에 제한없는 함수 작성 시 **로 시작되는 인자 사용
import html
def make_element(name,value,**attrs):
    keyvals = [ ' %s="%s"' % item for item in attrs.items()] #[?]잘 이해 안감
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(name=name, attrs=attr_str,value=html.escape(value))
    return element
#attrs : 전달 받은 키워드 매개변수(있다면 저장하는 딕셔너리
#예제
make_element('item','Albatros',size='large',quantity=6) #'<item size="large" quantity="6">Albatros</item>'
make_element('p','<spam>') #'<p>&lt;spam&gt;</p>'

#위치 매개변수,키워드 매개변수를 동시에 받는 함수 작성시 *, ** 사용
def anyargs(*args, **kwargs):
    print(args) #튜플
    print(kwargs) #딕셔너리

#모든 위치 매개변수는 튜플 args에 들어감 & 모든 키워드 매개변수는 딕셔너리 kwargs에 들어감

# *는 함수정의의 마지막 위치 매개변수 자리에만 올수 있음
# **는 마지막 매개변수 자리에만 올 수 있음
# * 뒤에도 매개변수가 또 나올 수 있음
def a(x, *args, y):
    pass
def b(x, *args, y, **kwargs):
    pass
#이런 매개변수는 키워드로만 넣을 수 있는 인자로 부름(7.2)

####7.2 키워드 매개변수만 받는 함수 작성
# 키워드로 지저안 특정 매개변수만 받는 함수가 필요함
# 키워드 매개변수를 * 뒤에 넣거나 이름없이 * 사용하여 구현

def recv(maxsize, * , block):
    'Recieves a message'
    pass
#recv(1024,True) #오류?? 왜 나는거얌
recv(1024,block=True)
#숫자가 다른 위치 매개변수를 받는 함수에 키워드 매개변수를 명시할 때 사용
def minimum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m

minimum(1,5,2,-5,10) #-5
minimum(1,5,2,-5,10, clip=0) #0

#키워드로만 넣을 수 있는(keyword-only)인자는 추가적 함수 인자 명시할 경우 코드 가독성을 높여줌
msg = recv(1024,False)
msg = recv(1024, block= False)
# 키워드로만 넣을 수 있는 인자는 **kwargs와 관련된 것에 사용자가 도움을 요청하면 도움말 화면에 나타남

help(recv)
# recv(maxsize, *, block)
#     Recieves a message

####7.3 함수 인자에 메타데이터 넣기
# 함수 작성시 인자에 정보를 추가해서 다른 사람에게 함수 사용법 알려주고 싶음
# 함수 인자 주석 사용
def add(x:int, y:int) -> int:
    return x+y

help(add)
# Help on function add:
# add(x:int, y:int) -> int
#어떤 객체도 함수에 주석으로 붙일 수 있지만(ex)숫자,문자 인스턴스) 대개 클래스나 문자열이 타당

#함수 주석은 함수의 __annotations__속성에 저장됨
add.__annotations__
#{'x': <class 'int'>, 'y': <class 'int'>, 'return': <class 'int'>}
#주석 활용방법은 많지만 기본적으로는 문서화에 도움을 주기 위해 사용
# 파이썬인 타입 선언을 지원하지 않기 때문에 소스 코드만 읽어서는 함수에 어떤 타임을 넣어야할지 알기 어려움

####### 7.4 함수에서 여러 값을 반환
#함수에서 여러 개 값 반환을 원할 경우 간단히 튜플 사용
def myfun():
    return 1,2,3

a,b,c = myfun()
a #1
b #2
c #3

#myfun()이 값을 여러개 반환하는 것처럼 보이지만 사실은 튜플 하나를 반환한 것
#실제로 튜플을 생성하는 것은 쉼표지 괄호가 아님

a = (1,2)
a #(1, 2)
b = 1,2 #괄호 미사용
b #(1, 2)

#튜플을 반환하는 함수 호출 시 결과 ㅏㅂㅅ을 여러 개의 변수에 넣는 것이 일반적 ( 1.1언패킹
#반환 값을  변수 하나에 할당할 수 있음
x = myfun()
x #(1,2,3)

####### 7.7 기본인자를 사용하는 함수 정의
#함수나 메소드 정의 시 하나 혹은 그 이상 인자에 기본값을 넣어 선택적으로 사용하고 싶음
#표면적으로 선택적 인자를 사용하는 함수를 정의하기는 어려움
# 함수 정의부에 값을 할당하고 가자 뒤에 이를 위치시킴

def spam(a, b=42):
    print(a,b)
spam(1) #1 42
spam(1,2) #1 2

#기본값이 리스트,세트, 딕셔너리 등 수정 가능한 컨테이너여야 한다면 None사용
_no_value = object()
def spam(a, b=_no_value):
    if b is _no_value:
        print('No b value supplied')
spam(1) #1 42
spam(1,2) #1 2
spam(1,None) #No b value supplied
# 아무런 값을 전달하지 않았을 때/ None값 전달 시 차이점에 주목하셈

# 1)할당하는 기본 ㄱ밧은 함수를 정의할 때 한번만 정해지고 그 후엔 안 변함
x = 42
def spam(a, b=x):
    print(a,b)
spam(1) # 1 42
x=23
spam(1)  # 1 42
# 변수 x 값을 바꾸어도 값 안 바뀜. 기본 값은 함수를 정의할 때 정해지기 때문

# 2) 기본적으로 사용하는 값은 None,True,False,숫자,문자열 같이 항상 변하지 않는 객체 사용
#def spam(a, b=[]) #절대 안됨!!
#기본 값이 함수를 벗어나서 수정되는 순간 많은 문제가 발생
# 값이 변하면 기본값이 변하게 되고 추후 함수 호출에 영향을 줌
def spam(a,b=[]):
    print(b)
    return b

x = spam(1)
x
x.append(99)
x.append('Yow!')
spam(1) #수정된 리스트가 반환됨
#이런 부작용을 피하려면 기본값으로 Nond을 할당하고 함수 내부에서 확인
#None 확인 시 is연산자를 사용하는 것이 매우 중요

def spam(a,b=None):
    if not b: #주의 b is None 사용
        b= []

##### 7.6 이름 없는 함수와 인라인 함수 정의
# sort()등에 사용할 짧은 콜백함수를 만드는 경우 짧게 만들고 싶음
# 인라인
#표현식 계신 외에는 lambda
add = lambda x,y : x+y
add(2,3) #5
add('hello','world') #'helloworld'

#일반적으로 lambda는 정렬이나 데이터 줄이기 등 다른 작업에 사용할 때 많이 씀
names=['David Beazly','Brian Jones','Raymond Hettinger','Ned Batchelder']
sorted(names, key= lambda name: name.split()[-1].lower())
#['Ned Batchelder', 'David Beazly', 'Raymond Hettinger', 'Brian Jones']

#lambda를 사용해서 간단한 함수를 정의할 수 있지만 제약이 많음
#표현식을 하나만 사용해야 하고 그 결과가 반환 값이 됨
#명령문 여러개 조건문, 순환문 에러 처리등으 넣을 수 없음

####### 7.7 이름 없는 함수에서 변수 고정
#lambda를 사용해서 이름 없는 함수를 정의했는데 저으이할 때 특정 변수의 값으 고정하고 싶음

x = 10
a =lambda y : x+y
x=20
b= lambda y : x+y
a(10) #30
b(10) #30

#lambda에서 사용한 x값이 실행 시간에 달라지는변수 임 람다 표현식의 x값은 그 함수를 실행할 때의 값이 됨
#이름없는 함수를 정의할 때 특정 값을 고정하고 싶으면 그 값을 기본값으러 지정하면 됨
x = 10
a = lambda y, x=x: x+y
x = 20
b = lambda y, x=x: x+y
a(10)
b(10)

#리스트 컴프리헨션이나 반복문에서 람다 표현식을 생성하고 람다 함수가 순환변수를 기억하려고 할 때 발생하기 쉬움
funcs = [lambda x: x+n for n in range(5)]
for f in funcs:
    print(f(0)

func = [lambda x, n=n:x+n for n in range(5)]
for f in func:
    print(f(0))
# n값을 함수 정의하는 시점의 값으로 고정해 놓고 사용