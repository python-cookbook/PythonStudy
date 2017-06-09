6월 9일
========================================================================================================================
#6.5 딕셔너리를 XML 로 바꾸기
# 파이썬 딕셔너리 데이터를 받아서 XML 로 바꾸고 싶다.
#xml.etree.ElementTree 라이브러리는 파싱에 일반적으로 사용하짐나, XML 문서를 생성할 때 사용

EX1>
from xml.etree.ElementTree import Element
def dict_to_xml(tag, d):
    '''
    간단한 dict를 XML로 변환하기
    '''
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

s = {'name':'GOOG','shares':100,'price':490.1}
e=dict_to_xml('stock',s)
print(e)
#<Element 'stock' at 0x00000000033E93B8>

EX2>
##이 변환의 결과로 Element 인스턴스가 나온다. I/O 를 위해서 xml.etree.ElementTree의
##tostring() 함수로 바이트 문자열로 변환하기
from xml.etree.ElementTree import tostring
print(tostring(e))
#b'<stock><name>GOOG</name><shares>100</shares><price>490.1</price></stock>'


#요소에 속성을 넣고 싶으면 set() 메소드
e.set('_id','1234')
print(tostring(e))
#b'<stock _id="1234"><name>GOOG</name><shares>100</shares><price>490.1</price></stock>'



#XML을 생성 시 단순히 문자열을 사용할 때
def dict_to_xml_str(tag,d):
    '''
    간단한 dict를 XML로 변환하기
    '''
    parts=['<{}>'.format(tag)]
    for key, val in d,items():
        parts.append('<{0}>{1}</{0}>'.format(key,val))
    parts.append('>/{}>'.format(tag))
    return ''.join(parts)
========================================================================================================================





========================================================================================================================
#6.6 XML 파싱, 수정, 저장
#XML 문서를 읽고, 수정하고, 수정 내용을 XML에 반영하고 싶다.
#"xml.etree.ElementTree 모듈"


#pred.xml 파일
<?xml version="1.0"?>
<stop>
    <id>14791</id>
    <nm>Clark &amp; Balmoral</nm>
    <sri>
    <rt>22</rt>
        <d>North Bound<?d>
        <dd>North Bound</dd>
    </sri>
    <cr>22</cr>
    <pre>
        <pt>5 MIN</pt>
        <fd>Howard</fd>
        <v>1378</v>
        <rn>22</rn>
    </pre>
    <pre>
        <pt>15 MIN<pt>
        <fd>Howard</fd>
        <v>1867</v>
        <rn>22</rn>
    </pre>
</stop>

#ElementTree로 이 문서로 읽고 수정하는 방법
from xml.etree.ElemnetTree import parse, Element
doc = parse('pred.xml')
root = doc.getroot()
root

#요소 몇 개 제거하기
root.remove(root.find('sri'))
root.remove(root.fing('cn'))

#<nm>...</nm> 뒤에 요소 몇 개 삽입하기
root.getchidren().index(root.find('nm'))

e=Element('spam')
e.text='This is a test'
root.insert(2, e)

#파일에 쓰기
doc.write('newpred.xml',xml_declaration=True)

#결과적으로 생성될 XML
<?xml version='1.0' encoding='us-ascii'?>
<stop>
    <id>14791</id>
    <nm>Clark &amp; Balmoral</nm>
    <spam>This is a test</spam><pre>
        <pt>5 MIN</pt>
        <fd>Howard</fd>
        <v>1378</v>
        <rn>22</rn>
    </pre>
    <pre>
        <pt>15 MIN<pt>
        <fd>Howard</fd>
        <v>1867</v>
        <rn>22</rn>
    </pre>
</stop>
========================================================================================================================





========================================================================================================================
#6.7 네임스페이스로 XML 문서 파싱
#XML 문서를 파싱할 때 XML 네임스페이스 사용하기
<?xml version="1.0" encoding="utf-8"?>
<top>
    <author>David Beazley</author>
    <content>
        <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <title>Hello World</title>
            </head>
            <body>
                <hl>Hello World!</hl>
            </body>
        </html>
    </content>
</top>

#동작하는 쿼리
doc.findtext('author')

doc.find('content')

#네임스페이스 관련 쿼리(동작X)
doc.find('content/html')

#조건에 맞는 경우에만 동작
doc.find('content/{http://www.w3.org/1999/xhtml}html')

#동작X
doc.findtext('content/{http://www.w3.org/1999/xhtml}html/head/title')

#조건에 일치
doc.findtext('content/{http://www.w3.org/1999/xhtml}html/'
             ... '{http://www.w3.org/1999/xhtml}head/{http://www.w3.org/1999/xhtml}title')


#유틸리티 클래스로 네임스페이스를 감싸서 단순화하기
class XMLNamespaces:
    def __init__(self,**kwargs):
        self.namespaces = {}
        for name, uri in kwargs.items():
            self.register(name,uri)
    def register(self,name,uri):
        self.namespaces[name] = '{'+uri+'}'
    def __call__(self,path):
        return path.format_map(self.namespaces)

ns=XMLNamespaces(html='http://www.w3.org/1999/xhtml')
doc.find(ns('content/{html}html'))

doc.findtext(ns('content/{html}html/{html}head/{html}title'))
========================================================================================================================




========================================================================================================================
#6.8 관계형 데이터베이스 작업
#관계형 데이터베이스에 선택, 삽입, 행 삭제 등의 작업하기

#파이썬에서 데이터 행을 나타내는 표준 = 튜플 시퀀스
stocks=[
    ('GOOG',100, 490.1),
    ('AAPL',50, 545.75),
    ('FB',150, 7.45),
    ('HPQ', 75, 33.2)
]

#주어진 형식을 통해, 파이썬의 표준 데이터베이스 API를 사용하면관계형 데이트베이스 작업을 하기 쉽다.
#입력이나 출력 데이터의 행은 튜플로 표현

#sqlite3 모듈을 통한 예시
#1단계_데이터베이스를 연결하는 것
#일반적으로 connect() 함수에 데이터베이스 이름 ,호스트 이름, 사용자 이름, 암호 등 필요한 정보를 넣는다.
import sqlite3
db=sqlite3.connect('database.db')

#데이터 관련 작업을하기 위해서는 커서(cursor)를 만들어야 한다.
#커서를 만든 후에 SQL쿼리 실행 가능
c=db.cursor()
c.execute('create table popol (symbol text, shares integer, price real)')

db.commit()

#데이터에 행의 시퀀스를 삽입하려면,
c.executemany('insert into popol values (?,?,?)', stocks)

db.commit()

#쿼리 수행 구문
for row in db.execute('select * from popol'):
    print(row)
#stocks=[
#    ('GOOG',100, 490.1),
 #   ('AAPL',50, 545.75),
  #  ('FB',150, 7.45),
   # ('HPQ', 75, 33.2)
#]


#사용자가 입력한 파라미터를 받는 쿼리를 수해하려면 ?를 사용해 파라미터를 이스케이핑해야 한다.
min_price=100
for row in db.execute('select * from popol where price >= ?',(min_price,)):
    print(row)
#('GOOG', 100, 490.1)
#('AAPL', 50, 545.75)
========================================================================================================================





========================================================================================================================
#6.9 16진수 인코딩 디코딩
#문자열로 된 16진수를 바이트 문자열로 디코딩하거나, 바이트 문자열을 16진법으로 인코딩해야 한다.
#"binascii 모듈"

EX1>
#최초 바이트 문자열
s = b'hello'

#16진법으로 인코딩
import binascii
h=binascii.b2a_hex(s)
print(h)
#b'68656c6c6f'

#바이트로 디코딩
binascii.a2b_hex(h)
#b'hello'


EX2>
#base64 모듈로 실행
import base64
h=base64.b16encode(s)
print(h)
#b'68656C6C6F'

base64.b16decode(h)
#b'hello'


#두 함수의 차이점 = 대소문자 구분**
# 대문자 = base64.b16decode() / base64.b16encode()
# 대소문자 구분X = binascii

#인코딩 함수가 만들 출력물은 언제나 바이트 문자열**
#유니코드를 사용하려면 디코딩 과정을 추가해야 한다.
h=base64.b16encode(s)
print(h)
#b'68656C6C6F'

print(h.decode('ascii'))
#68656C6C6F


#16진수를 디코딩할 때 b16decode(0와 a2b_hex() 함수는 바이트 혹은 유니코드 문자열을 받는다.
#하지만 이 문자열에는 반드시 ASCII로 인코딩한 16진수가 포함되어 있어야 한다.
========================================================================================================================







CAHPTER7. 함수
[기본 인자, 인자 수에 구애 받지 않는 함수, 키워드 인자, 주석, 클로저]
[복잡한 컨트롤 플로우의 콜백 함수를 사용한 ㄷ이터 전달 문제]
========================================================================================================================
#7.1 매개변수 개수에 구애 받지 않는 함수 작성
#입력 매개변수 개수에 제한이 없는 함수 작성하기
#"* 함수"

EX1>
def avg(first, *rest):
    return (first + sum(rest)) / (1 + len(rest))

print(avg(1,2))
#1.5
print(avg(1,2,3,4))
#2.5

##rest에 추가적 위치 매개변수가 튜플로 들어간다.



EX2>
#키워드 매개변수 수에 제한이 없는 함수를 작성하려면 **로 시작하는 인자 사용
import html
def make_element(name,value,**attrs):
    keyvals=[' %s="%s" % item for item in attrs.items()']
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(
        name=name,
        attrs=attr_str,
        value=html.escape(value))
    return element

#'<item size="large" quantity="6">Albatross</item>' 생성
print(make_element('item', 'Albatross', size='large', queantity=6))
#<item %s="%s" % item for item in attrs.items()>Albatross</item>

#'<p>&lt;spam&gt;</p>' 생성
print(make_element('p','<spam>'))
#<p %s="%s" % item for item in attrs.items()>&lt;spam&gt;</p>


##attrs은 전달받은 키워드 매개변수를 저장하는 딕셔너리



EX3>
#위치 매개변수와 키워드 매개변수를 동시에 받는함수를 작성하려면,
# * 와 ** 를 함께 사용
def anyargs(*args, **kwargs):
    print(args)    #튜플
    print(kwargs)   #딕셔너리
## 모든 위치 매개변수 => 튜플 args
## 모든 키워드 매개변수 => 딕셔너리 kwargs



EX4>
#*는 함수 정의의 마지막 위치 매개변수 자리에만 올 수 있다.
# **는 마지막 매개변수 자리에만 올 수 있다.
# 그리고 * 뒤에도 매개변수가 또 나올 수 있다
def a(x, *args, y):
    pass

def b(x, *args, y, **kwargs):
    pass
##d위의 매개변수는 키워드로만 넣을 수 있는(keyword-noly) 인자라고 부른다.
========================================================================================================================





========================================================================================================================
#7.2 키워드 매개변수만 받는 함수 작성
#키워드로 지정한 특정 매개변수만 받는 함수가 필요할 때
#키워드 매개변수를 * 뒤에 넣기 또는 이름 없이 *만 사용하기
EX1>
def recv(maxsize, *, block):
    'Receuves a message'
    pass

print(recv(1024,True))
#TypeError: recv() takes 1 positional argument but 2 were given
print(recv(1024,block=True))
#None

EX1_1>
#이 기술로 숫자가 다른 위치 매개변수를 받는 함수에 키워드 매개변수를 명시할 때 사용가능
def mininum(*values,clip=None):
    m=min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m
print(mininum(1, 5, 2, -5, 10))
#-5

print(mininum(1, 5, 2, -5, 10, clip=0))
#0



#키워드로만넣을 수 있는(keysord-only) 인자는 추가적 함수 인자를 명시할 때 코드의 가독성을 높인다.
msg = recv(1024,False)
##False 인자가 무엇을 의미하는지 호출할 때 표시해주기
msg = recv(1024,block=False)



#키워드로만 넣을 수 있는 인자는 **kwargs와 관련된 것에 사용자가 도움을 요청하면 도움말 화면에 나타난다.
help(recv)
#Help on function recv:
#recv(maxsize, *, block)
#    Receuves a message
========================================================================================================================





========================================================================================================================
#7.3 함수 인자에 메타데이터 넣기
#함수를 작성했을 때 인자에 정보를 추가해서 다른 사람이 함수를 어떻게 사용해야 하는지 알 수 있도록 하기

EX1>
#함수 인자 주석으로 프로그래머에게 이 함수를 어떻게 사용해야 할지 정보를 줄 수 있다.
def add(x:int, y:int) -> int:
    return x + y
#파이썬 인터프리터는 주석에 의미 부여하지 X
#타입을 확인하지 X, 파이썬의 실행 방식이 달라지지 X
#ㅅ이해하기 쉽게
# 서드파티 도구와 프레임워크에도 주석
help(add)
#Help on function add:
#add(x:int, y:int) -> int
#어떠한 객체도 함수에 주석으로 붙일 수 있지만 (EX, 숫자, 문자열, 인스턴스), 대개 클래스나 문자열이 타당하다.



EX2>
#함수 주석은 함수의 "__annotations__속성"에 저장됨
add.__annotations__
{'y': <class 'int'>, 'return': <class 'int'>, 'x': <class 'int'>}
## 문서화에 도움을 주기 위해 주석 활용
## 파이썬이 타입 선언을 지원하지 않아서 소스 코드만 읽어서는 함수에 어떤 타입을 넣어야 할지 알기 어려울 때 >> 주석
========================================================================================================================





========================================================================================================================
#7.4 함수에서 여러 값을 반환
#"튜플"
EX1>
def myfun():
    return 1, 2, 3

a, b, c = myfun()
print(a)
#1
print(b)
#2
print(c)
#3


#myfun()이 값을 여러 개 반환하는 것처럼 보이지만, "튜플 하나 반환"
#실제 튜플 생성 = 쉼표 O, 괄효 X
a=(1,2)    #괄호 사용
print(a)
#(1, 2)

b=1,2   #괄효 미사용
print(b)
#(1, 2)



#튜플을 반환하는 함수를 호출할 대, 결과 값을 여러 개의 변수에 넣는 것이 일반적 = 튜플 언패킹
#반환 값을 변수 하나에 할당 가능
x=myfun()
print(x)
#(1, 2, 3)
========================================================================================================================





========================================================================================================================
#7.5 기본 인자를 사용하는 함수 정의
#함수나 메소드를 정의할 때 하나 또는 그 이상 인자에 기본 값을 넣어 선택적으로 사용할 수 있도록
#함수 정의부에 값을 할당하고 가장 뒤에 위치시키기 = 선택적 인자를 사용하는 함수 정의
EX1>
def spam(a,b=42):
    print(a,b)
spam(1)    #OK. a=1, b=42
#1 42
spam(1,2)   #OK. a=1, b=2
#1 2


#기본값이 리스트, 세트, 딕셔너리 등 수정 가능한 컨테이너여야 한다면 None 사용하기
EX2>
#기본값으로 리스트 사용
def spam(a, b=None):
    if b is None:
        b=[]
    ...


EX3>
#기본값을 제공하는 대신 함수가 받은 값이 특정 값인지 아닌지 확인하려면,
_no_value=object()
def spam(a, b=_no_value):
    if b is _no_value:
        print('No b value supplied')

spam(1)
#No b value supplied

spam(1,2)   #b=2
spam(1,None)    #b=None
##아무런 값을 전달하지 않았을 때와 None값을 전달했을 때의 차이



#기본 인자를 가지는 함수 정의할 때 주의할 점
#1_할당하는 기본 값은 함수를 정의할 때 한 번만 정해지고 그 이후에는 변하지 X
EX4>
x=42
def spam(a,b=x):
    print(a,b)
spam(1)
#1 42

x-23    #효과 없음
spam(1)
#1 42

## 변수 x(기본 값으로 사용했다)의 값을 바꾸어도 그 이후에 기본 값이 변하지 X
## 기본 값은 함수를 정의할 때 정해지기 때문에

EX4_1>
#2_기본 값으로 사용하는 값은 None, True, False, 숫자, 문자열 같이 항상 변하지 않는 객체를 사용해야 한다/
#특히 아래같은 코드 절대 사용XX
def spam(a,b=[]):   #NO!
    ...
##기본 값이 함수를 벗어나서 수정되는 순간 많은 문제 발생
##값이 변하면 기본 값이 변하게 되고 추후 함수 호출에 영향을 준다.

def spam(a,b=[]):
    print(b)
    return b
x=spam(1)
#[]

x.append(99)
x.append('Yow')
print(x)
#[99, 'Yow']

spam(1)
#\[99, 'Yow']   #수정된 리스트 반환

EX4_2>
##부작용을 피하려면 앞의 예제에서 나왔듯이 기본 값으로 None을 할당하고 함수 내부에서 확인하기
#None을 확인할 때 is 연산자를 사용하는 것이 중요하다.
def spam(a,b=None):
    if not b:   #주의! 'b is None'을 사용해야 한다!!
        b=[]
    ...

##None이 False로 평가되지만, 그 외에 다른 객체(길이가 0인 문자열, 리스트, 튜플, 딕셔너리 등)도 False로 평가된다.
##따라서 특정 입력을 없다고 판단하게 된다.
spam(1)     #올바름
x=[]
spam(1, x)   #에러. x 값이 기본으로 덮어쓰여진다.
spam(1, 0)   #에러. 0이 무시된다.
spam(1, '')    #에러. ''이 무시된다.
========================================================================================================================




========================================================================================================================
#7.6 이름 없는 함수와 인라인 함수 정의
#sort() 등에 사용할 짧은 콜백 함수를 만들어야 하는데, 한 줄짜리 함수를 만들면서 def 구문사용하지 않기
#대신 "인라인(in line)"이라 불리는 짧은 함수를 만들고 싶을 때

EX1>
#표현식 계산 외에 아무 일도 하지 않는 간단한 함수
#"lambda로 치환"
add=lambda x, y: x + y
print(add(2,3))
#5

print(add('Hello','world'))
#Helloworld

def add(x,y):
    return x + y
print(add(2,3))
#5


EX2>
#일반적으로 lambda는 정렬이나 데이터 줄이기 등 다른 작업에 사용할 때 많이 쓴다.
names = ['David Beazley', 'Brian Jones', 'Raymond Hettigner', 'Ned Batchelder']
print(sorted(names, key=lambda name : name.split()[-1].lower()))
#['Ned Batchelder', 'David Beazley', 'Raymond Hettigner', 'Brian Jones']

##lambda를 사용해서 간단한 함수를 정의할 수 있지만, 제약이 많다.
##우선 표현식을 하나마나 사용해야 하고 그 결과가 반환 값이 된다.
#따라서 명령문을 여러 개 쓴다거나 조건문, 순환문, 에러 처리 등을 넣을 수 없다.
========================================================================================================================





========================================================================================================================
#7.7 이름 없는 함수에서 변수 고정
#lambda를 사용해서 이름없는 함수를 정의했는데, 정의할 때 특정 변수의 값 고정하기
EX1>
x=10
a=lambda y: x + y
x = 20
b=lambda y: x + y

print(a(10))
#30
print(b(10))
#30



EX2>
#위의 식의 문제는 lambda에서 사용한 x 값이 실행 시간에 달라지는 변수
#따라서 람다 표혀식의 x의 값은 그 함수를 실행할 때의 값이 된다.
x = 15
print(a(10))
#25

x=3
print(a(10))
#13


EX3>
#이름없는 함수를 정의할 때 특정 값을 고정하고 싶으면 그 값을 기본 값으로 지정하면 된다.
x=10
a=lambda y, x=x: x + y
x = 20
b = lambda y, x=x: x + y
print(a(10))
#20
print(b(10))
#30
========================================================================================================================