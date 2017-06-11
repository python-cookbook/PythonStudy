# 6.5 딕셔너리를 XML로 바꾸기
# 문제
# 파이썬 딕셔너리 데이터를 받아서 XML로 바꾸고 싶다
# 해결
# xml.etree.ElementTree 라이브러리는 파싱에 일반적으로 사용하지만, XML 문서를 생성할 때 사용하기도 한다. 예를 들어 다음 함수를 고려해보자
from xml.etree.ElementTree import Element
def dict_to_xml(tag,d):
    ''' 간단한 dict를 XML로 변환하기'''
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        elem.append(child)
    return elem
# 예제는 다음과 같다
s = { 'name' : 'GOOG', 'shares':100,'price':490.1}
e = dict_to_xml('stock',s)
print(e) # <Element '# stock' at 0x000002353CD959F8> 출력
# 이 변환의 결과로 Element 인스턴스가 나온다.
# I/O 를 위해서 xml.etree.ElementTree의 tostring() 함수로 이를 바이트 문자열로 변환하기는 어렵지 않다.
# from xml.etree.ElementTree import tostirng
# tostring(e)
# 요소에 속성을 넣고 싶으면 set() 메소드를 사용한다
e.set('_id','1234')
# tostirng(e)
# 요소의 순서를 맞추어야 한다면 일반 딕셔너리를 사용하지 않고 OrderedDict 를 사용한다.
# 토론
# XML을 생성할 때 단순히 문자열을 사용하고 싶을 수도 있다
def dict_to_xml_str(tag,d):
    '''간단한 dict를 XML로 변환하기'''
    parts=['<{}>'.format(tag)]
    for key, val in d.items():
        parts.append('<{0}>{1}</{0}>'.format(key,val))
    parts.append('</{}>'.format(tag))
    return ''.join(parts)
# 하지만 이 작업을 수동으로 하면 코드가 엄청나게 복잡해질 수 있다. 예를 들어 딕셔너리에 다음과 같이 특별 문자가 포함되어 있다면 어떨까?
d = { 'name' : '<spam>'}
# 문자열 생성
print(dict_to_xml_str('item',d)) # <item><name><spam></name></item> 생성
# 올바른 XML 생성
e = dict_to_xml('item',d)
tostring(e)
# 올바른 출력을 만드는 것 외에도 문자열 대신 Element 인스턴스를 만드는 것이 좋은 이유는 이들을 더 쉽게 합쳐 큰 문서를 만들 수 있기 떄문이다.
# 결과 Element 인스턴스는 XML 파싱에 대한 염려 없이 여러 방법으로 처리할 수 있다.
# 사실 모든 데이터 처리를 상위 레벨 형식으로 할 수 있고, 마지막에는 문자열로 출력도 가능하다

# 6.6 XML 파싱,수정,저장
# 문제
# XML 문서를 읽고, 수정하고, 수정내용을 XML 에 반영하고 싶다
# 해결
# xml.etree.ElementTree 모듈로 이 문제를 간단히 해결할 수 있다.
# 우선 일반적인 방식으로 문서 파싱부터 시작한다.
# 예를 들어 pred.xml 파일이 있다고 가정해보자
# <?xml version="1.0"?>
# <stop>
#     <id>14791</id>
#     <nm>Clark &amp; Balmoral</nm>
#     <sri>
#         <rt>22</rt>
#         <d>North Bound</d>
#         <dd>North Bound</dd>
#         </sri>
#         <cr>22</cr>
#         <pre>
#             <pt>5 MIN</pt>
#             <fd>Howard</fd>
#             <v>1378</v>
#             <rn>22</rn>
#     </pre>
#     <pre>
#         <pt>15 MIN</pt>
#         <fd>Howard</fd>
#         <v>1867</v>
#         <rn>22</rn>
#            </pre>
#     </stop>
# ElemetTree로 이 문서를 읽고 수정하는 방법은 다음과 같다
from xml.etree.ElementTree import parse, Element
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
# 파일에 쓰기
a = doc.wirte('newpred.xml',xml_declaration=True)
print(a)
결과적으로 생성된 XML은 다음과 같다
<?xml version'1.0' encoding='us-ascii'?>
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
        <pt>15 MIN,/pt>
        <fd>Howard</fd>
        <v>1867</v>
        <rn>22</rn>
    </pre>
</stop>
토론
XML 문서의 구조를 수정하는 것은 어렵지 않지만 모든 수정 사항은 부모 요소에도 영향을 미쳐 리스트인 것처럼 다루어진다는 점을 기억해야 한다.
예를 들어 어떤 요소를 제거하면 부모의 remove() 메소드를 사용해 바로 위에 있는 부모로부터 제거된다
새로운 요소를 추가하면 부모에 대해서 insert() 와 append() 메소드를 사용하게 된다
그리고 모든 요소는 element[i] 또는 elemnet[i:j] 와 같이 인덱스와 슬라이스 명령으로도 접근할 수 있다.
새로운 요소를 만들려면 이번 레시피의 해결책에 나온 것처럼 Element 클래스를 사용한다

# 6.7 네임스페이스로 XML 문서 파싱
# 문제
# XML 문서를 파싱할 때 XML 네임스페이스 를 사용하고 싶다
# 해결
# 다음과 같이 네임스페이스를 사용하는 문서를 고려해 보자
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
# 이 문서를 파싱하고 일반적인 쿼리를 실행하면 모든 것이 너무 장황해서 그리 쉽게 동작하지 않는다는 것을 알 수 있다
#동작하는 쿼리
# doc.findtext('author') #'David Beazley'
# doc.find('content') #<Element 'content' at 0x10076ec0>
#네임 스페이스 관련 쿼리(동작하지 않음)
# doc.find('content/html')
#조건에 맞는 경우에만 동작
# doc.find('content/{http://www.w3.org/1999/xhtml}html')
#동작하지 않음
# doc.findtext('content/{http://www.w3.org/1999/xhtml}html/head/title')
#조건에 일치함
# doc.findtext('content/{http://www.w3.org/1999/xhtml}html/'
# ... '{http://www.w3.org/1999/xhtml}head/{http://www.w3.org/1999/xhtml}title') 'Hello World'
# 유틸리티 클래스로 네임스페이스를 감싸 주면 문제를 더 단순화할 수 있다
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
doc.find(ns('content/{html}html')) #<Element '{http://www.w3.org/1999/xhtml}html' at 0x1007767e0> 출력
doc.findtext(ns('content/{html}html/{html}head/{html}title')) #'Hello World' 출력
# 토론
# 네임스페이스를 포함한 XML 문서를 파싱하기는 꽤나 복잡하다
# XMLNamespaces 클래스는 짧게 줄인 네임스페이스 이름을 쓸 수 있도록 해서 코드를 정리해준 뿐이다.
# 하지만 iterparse() 함수를 사용한다면 네임스페이스 처리의 범위에 대해서 정보를 조금 더 얻을 수는 있다
from xml.etree.ElementTree import iterparse
for evt,elem in iterparse('ns2.xml',('end','start-ns','end-ns')):
    print(evt,elem)

# 6.8 관계형 데이터베이스 작업
# 문제
# 관계형 데이터베이스에 선택,삽입,행 삭제 등의 작업을 하고 싶다
# 해결
# 파이썬에서 데이터 행을 나타내는 표준은 튜플 시퀀스이다
stocks = [ ('GOOG',100,490.1),
           ('AAPL',50,545.75),
           ('FB',150,7.45),
           ('HPQ',75,33.2),]
# 주어진 형식을 통해, 파이썬의 표준 데이터베이스 API 를 사용하면 관계형 데이터베이스 작업을 하는 것은 간단하다
# 입력이나 출력 데이터의 행은 튜플로 표현한다
# 파이썬의 sqlite3 모듈을 사용한다
# 첫번째 단계는 데이터베이스를 연결하는 것이다.
# 일반적으로 connect() 함수에 데이터베이스 이름, 호스트 이름, 사용자 이름, 암호 등 필요한 정보를 넣는다.
import sqlite3
db = sqlite3.connect('database.db')
# 데이터 관련 작업을 하기 위해서는 커서를 만들어야 한다.
# 커서를 만든 후에 SQL 쿼리를 실행 할 수 있다
c = db.cursor()
c.execute('create table portfolio (symbol text, shares integer, price real)')
db.commit()
# 데이터에 행의 시퀀스를 삽입하려면 다음 구문을 사용한다
c.executemany('insert into portfolio values (?,?,?)',stocks)
db.commit()
# 쿼리를 수행하려면 다음 구문을 사용한다
for row in db.execute('select * from portfolio'):
    print(row)
# 사용자가 입력한 파라미터를 받는 쿼리를 수행하려면 ?를 사용해 파라미터를 이스케이핑해야 한다
min_price=100
for row in db.execute('select * from portfolio where price >= ?', (min_price,)):
    print(row)
# 토론
# SQLAlchemy와 같은 라이브러리는 데이터베이스 테이블을 파이썬 클래스로 표현하게 해 주고 기반 SQL을 숨긴 상태로 데이터베이스 작업을 하도록 도와준다

# 6.9 16진수 인코딩, 디코딩
# 문제
# 문자열로 된 16진수를 바이트 문자열로 디코딩하거나, 바이트 문자열을 16진법으로 인코딩해야 한다
# 해결
# 문자열을 16진수로 인코딩하거나 디코딩하려면 binascii 모듈을 사용한다
#최초 바이트 문자열
s= b'hello'
#16진법 인코딩
import binascii
h=binascii.b2a_hex(s)
print(h) #b'68656c6c6f' 출력
#바이트로 디코딩
a = binascii.a2b_hex(h)
print(a) #b'hello' 출력
#base64 모듈에도 유사한 기능이 있다
import base64
h=base64.b16encode(s)
print(h) #b'68656C6C6F' 출력
a = base64.b16decode(h)
print(a) # b'hello' 출력
# 토론
# 앞에 나온 함수를 사용하면 16진법 전환은 그리 어렵지 않게 수행할 수 있다
# binascii는 대소문자를 가리지 않는다
# 또한 인코딩 함수가 만들 출력미ㅜㄹ은 언제나 바이트 문자열이라는 점이 중요하다

# CHAPTER 7 - 함수
# 7.1 매개변수 개수에 구애 받지 않는 함수 작성
# 문제
# 입력 매개변수 개수에 제한이 없는 함수를 작성하고 싶다.
# 해결
# 위치 매개변수의 개수에 제한이 없는 함수를 작성하려면 * 인자를 사용한다
def avg(first, *rest):
    return (first + sum(rest)) / (1 + len(rest))
# 샘플
a = avg(1,2) # 1.5 출력
b = avg(1,2,3,4) # 2.5 출력
print(a,b)
import html
def make_element(name,value,**attrs):
    keyvals = [ ' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(name=name, attrs=attr_str,value=html.escape(value))
    return element
# 예제
make_element('item','Albatros',size='large',quantity=6) # '<item size="large" quantity="6">Albatros</item>' 생성
make_element('p','<spam>') # '<p>&lt;spam&gt;</p>' 생성
# attrs은 전달 받은 키워드 매개변수(있다면)를 저장하는 딕셔너리이다
# 위치 매개변수와 키워드 매개변수를 동시에 받는 함수를 작성하려면, *와 **를 함께 사용하면 된다
def anyargs(*args,**kwargs):
    print(args) # 튜플로 받는다
    print(kwargs) # 딕셔너리로 받는다
# 토론
# *는 함수 정의의 마지막 위치 매개변수 자리에만 올 수 있다.
# **는 마지막 매개변수 자리에만 올 수 있다
# 그리고 *뒤에도 매개변수가 또 나올 수 있다는 것이 함수 정의 미묘한 점이다
def a(x, *args,y):
    pass
def b(x,*args,y,**kwargs):
    pass
# 이런 매개변수는 키워드로만 넣을 수 있는(keyword-only) 인자로 부른다

# 7.2 키워드 매개변수만 받는 함수 작성
# 문제
# 키워드로 지정한 특정 매개변수만 받는 함수가 필요하다
# 해결
# 이 기능은 키워드 매개변수를 * 뒤에 넣거나 이름 없이 *만 사용하면 간단히 구현할 수 있다
def recv(maxsize,*,block):
    'Receives a message'
    pass
# recv(1024,True) # TypeError 가 뜬다 1 argument를 써라
print(recv(1024,block=True)) # None 출력
# 이 기술로 숫자가 다른 위치 매개변수를 받는 함수에 키워드 매개변수를 명시할 때 사용할 수도 있다
def recv(maxsize, * , block):
    'Recieves a message'
    pass
recv(1024,block=True)
def minimum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m
minimum(1,5,2,-5,10) # -5 출력
minimum(1,5,2,-5,10, clip=0) # 0 출력
# 토론
# 키워드로만 넣을 수 있는 인자는 추가적 함수 인자를 명시할 때 코드의 가독성을 높이는 좋은 수단이 될 수 있다

# 7.3 함수 인자에 메타데이터 넣기
# 문제
# 함수를 작성했고 인자에 정보를 추가해서 다른 사람이 함수를 어떻게 사용해야 하는지 알 수 있도록 하고 싶다
# 해결
# 함수 인자 주석으로 프로그래머에게 이 함수를 어떻게 사용해야 할지 정보를 줄 수 있다. 예를 들어 다음과 같이 주석이 붙는 함수를 살펴보자
def add(x:int, y:int) -> int:
    return x + y
# 파이썬 인터프리터는 주석에 어떠한 의미도 부여하지 않는다
# 단지 소스 코드를 읽는 사람이 이해하기 쉽도록 설명을 할 뿐이다
help(add)
# Help on function add in module __main__:
add(x : int, y : int) -> int
# 토론
# 함수 주석은 함수의 __annotations__ 속성에 저장된다
# 주석을 활용할 수 있는 방법은 많지만, 기본적으로는 문서화에 도움을 주기 위해 사용한다
# 파이썬이 타입 선언을 지원하지 않아서 소스 코드만 읽어서는 함수에 어떤 타입을 넣어야 할지 알기 어렵다
# 이때 주석이 도움을 준다

# 7.4 함수에서 여러 값을 반환
# 문제
# 함수에서 값을 여러개 반환하고 싶다
# 해결
# 함수에서 값을 여러 개 반환하고 싶다면 간단히 튜플을 사용하면 된다
def myfun():
    return 1,2,3
a,b,c=myfun()
print(a,b,c) # 1 2 3 출력
# 토론
# myfun() 이 값을 여러 개 반환하는 것처럼 보이지만, 사실은 튜플 하나를 반환한 것이다.
# 조금 이상해 보이지만 실제로 튜플을 생성하는 것은 쉼표지 괄호가 아니다.
a = (1,2)
print(a) # (1,2) 출력
b = 1,2
print(b) # (1,2) 출력
# 튜플을 반환하는 함수를 호출할 때, 결과 값을 여러 개의 변수에 넣는 것이 일반적이다
# 반환 값을 변수 하나에 할당할 수 도 있다
x = myfun()
print(x) # (1,2,3) 출력

# 7.5 기본 인자를 사용하는 함수 정의
# 문제
# 함수나 메소드를 정의할 때 하나 혹은 그 이상 인자에 기본 값을 넣어 선택적으로 사용할 수 있도록 하고 싶다
# 해결
# 표면적으로 선택적 인자를 사용하는 함수를 정의하기는 쉽다.
# 함수 정의부에 값을 할당하고 가장 뒤에 이를 위치시키기만 하면 된다
def spam(a,b=42):
    print(a,b)
spam(1) # 1 42 출력
spam(1,2) # 1 2 출력
# 기본값이 리스트,세트,딕셔너리 등 수정가능한 컨테이너여야 한다면 None을 사용해 다음과 같은 코드를 작성한다
def spam(a,b=None):
    if b is None:
        b = []
# 기본 값을 제공하는 대신 함수가 받은 값이 특정 값인지 아닌지 확인하려면 다음 코드를 사용한다
_no_value = object()
def spam(a,b=_no_value):
    if b is _no_value:
        print('No b value supplied')
    ...
spam(1) # No b value supplied 출력
spam(1,2)
spam(1,None)
# 신경 써야 할 부분은 할당하는 기본값은 함수를 정의할 때 한번만 정해지고 그 이후에는 변하지 않는다
x =42
def sapm(a,b=x):
    print(a,b)
spam(1,2) # 1 42 출력
x = 23
spam(1) # 1 42 출력 즉, 효과없음

def spam(a,b=[]):
    print(b)
    return b
x = spam(1)
x.append(99)
x.append('Yow!')
spam(1) # [99, 'Yow1'] 출력

# 7.6 이름 없는 함수와 인라인 함수 정의
# 문제
# SORT() 등에 사용할 짧은 콜백 함수를 만들어야 하는데 한줄짜리 함수를 만들면서 def 구문까지 사용하고 싶지는 않다.
# 그 대신 인라인이라 불리는 짧은 함수를 만들고 싶다
# 해결
# 표현식 계산 외에 아무 일도 하지 않는 간단한 함수는 lambda로 치환할 수 있다
add = lambda x,y : x+y
add(2,3) # 5 출력
add('hello','world') # 'helloworld' 출력
# 일반적으로 lambda는 정렬이나 데이터 줄이기 등 다른 작업에 사용할 때 많이 쓴다
names=['David Beazly','Brian Jones','Raymond Hettinger','Ned Batchelder']
a = sorted(names, key= lambda name: name.split()[-1].lower())
print(a)
# ['Ned Batchelder', 'David Beazly', 'Raymond Hettinger', 'Brian Jones'] 출력

# 7.7 이름 없는 함수에서 변수 고정
# 문제
# lambda를 사용해서 이름 없는 함수를 정의했는데, 정의할 때 특정 변수의 값을 고정하고 싶다
# 해결
# 다음 코드의 동작성을 고려해보자
x=10
a=lambda y :x+y
x=20
b=lambda y:x+y
print(a(10),b(10)) # 30 30 출력
# 즉, lambda에서 사용한 x 값은 실행 시간에 달라지는 변수다
# 따라서 람다 표현식의 x의 값은 그 함수를 실행할 때의 값이된다
x=15
print(a(10)) # 25 출력
x=3
print(a(10)) # 13 출력
# 토론
# 즉, 현명하게 사용하려다가 발생하는 경우이다
funcs = [lambda x: x+n for n in range(5)]
for f in funcs:
    print(f(0)) # 4 4 4 4 4 출력

func = [lambda x, n=n:x+n for n in range(5)]
for f in func:
    print(f(0)) # 0 1 2 3 4 출력