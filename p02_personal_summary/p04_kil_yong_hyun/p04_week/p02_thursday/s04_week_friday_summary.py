#  6.5 딕셔너리를 XML 로 바꾸기
#  ▣ 문제 : 파이썬 딕셔너리 데이터를 받아서 XML 로 바꾸고 싶다.
#  ▣ 해결 : xml.etree.ElementTree 라이브러리는 파싱에 일반적으로 사용하지만, XML 문서를 생성할 때 사용하기도 한다.
from xml.etree.ElementTree import Element

def dict_to_xml(tag, d):
    elem = Element(tag)

    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

s = {'name': 'GOOG', 'shares':100, 'price': 490.1}
e = dict_to_xml('stock', s)
print(e)

#   - I/O 를 위해서 xml.etree.ElementTree 의 tostring() 함수로 이를 바이트 문자열로 변환
from xml.etree.ElementTree import tostring
print(tostring(e))

#   - 요소에 속성을 넣고 싶으면 set() 메소드를 사용한다.
e.set('_id', '1234')
print(tostring(e))

#  ▣ 토론 : XML 을 생성할 때 단순히 문자열을 사용하고 싶을 수도 있다.
def dict_to_xml_str(tag, d):
    parts = ['<{}>'.format(tag)]
    for key, val in d.items():
        parts.append('<{0}>{1}</{0}>'.format(key, val))
    parts.append('</{}>'.format(tag))
    return ''.join(parts)

#   - 딕셔너리에 다음과 같이 특별 문자가 포함되어 있는 경우
d = {'name': '<spam>'}
print(dict_to_xml_str('item', d))
print(tostring(dict_to_xml('item', d)))

#   - 마지막 예제에서 < 와 > 문자가 &lt; 와 &gt; 로 치환되었다.
#     이런 문자를 수동으로 이스케이핑하고 싶다면 xml.sax.saxutils 의 escape() 와 unescape() 함수를 사용한다.
from xml.sax.saxutils import escape, unescape
print(escape('<spam>'))
print(unescape('<spam>'))


#  6.6 XML 파싱, 수정, 저장
#  ▣ 문제 : XML 문서를 읽고, 수정하고, 수정 내용을 XML 에 반영하고 싶다.
#  ▣ 해결 : xml.etree.ElementTree 모듈로 이 문제를 간단히 해결할 수 있다.
#            우선 일반적인 방식으로 문서 파싱부터 시작한다.
from xml.etree.ElementTree import parse, Element
doc = parse('PythonCookBook/files/pred.xml')
root = doc.getroot()
print(root)

#   - 요소 몇 개 제거하기
root.remove(root.find('sri'))
root.remove(root.find('cr'))

#   - 특정 태그 뒤에 요소 몇개 삽입하기
print(root.getchildren().index(root.find('nm')))
e = Element('spam')
e.text = 'This is a test'
root.insert(2, e)

#   - 파일에 쓰기
doc.write('PythonCookBook/files/newpred.xml', xml_declaration=True)

#  ▣ 토론 : XML 문서의 구조를 수정하는 것은 어렵지 않지만 모든 수정 사항은 부모 요소에도 영향을 미쳐 리스트인 것처럼 다루어진다는 점을 기억해야 한다.
#            그리고 모든 요소는 element[i] 또는 element[i:j] 와 같이 인덱스와 슬라이스 명령으로도 접근할 수 있다.


#  6.7 네임스페이스로 XML 문서 파싱
#  ▣ 문제 : XML 문서를 파싱할 때 XML 네임스페이스를 사용하고 싶다.
#  ▣ 해결 : 다음과 같이 네임스페이스를 사용하는 문서를 고려해 보자.
from xml.etree.ElementTree import Element, parse
doc = parse('PythonCookBook/files/sample.xml')
root = doc.getroot()

#   - 동작하는 쿼리
print(doc.findtext('author'))
print(doc.find('content'))

#   - 네임스페이스 관련 쿼리(동작하지 않음)
print(doc.find('content/html'))

#   - 조건에 맞는 경우에만 동작
print(doc.find('content/{http://www.w3.org/1999/xhtml}html'))

#   - 동작하지 않음
print(doc.findtext('content/{http://www.w3.org/1999/xhtml}html/head/title'))

#   - 조건에 일치함
print(doc.findtext('content/{http://www.w3.org/1999/xhtml}html/{http://www.w3.org/1999/xhtml}head/{http://www.w3.org/1999/xhtml}title'))

#   - 유틸리티 클래스로 네임스페이스를 감싸 주면 문제를 더 단순화할 수 있다.
class XMLNamespaces:
    def __init__(self, **kwargs):
        self.namespaces = {}
        for name, uri in kwargs.items():
            self.register(name, uri)

    def register(self, name, uri):
        self.namespaces[name] = '{'+uri+'}'

    def __call__(self, path):  # __call__() : 클래스 인스턴스명 자체로 함수처럼 사용할 때 호출된다. 해당 메서드를 정의한 클래스의 인스ㅓㄴ스는 callable(인스턴스) 에 True 를 리턴한다.
        return path.format_map(self.namespaces)  # format_map() : 키 값에 따른 포맷팅 형식을 맞춰준다.

ns = XMLNamespaces(html='http://www.w3.org/1999/xhtml')
print(doc.find(ns('content/{html}html')))
print(doc.findtext(ns('content/{html}html/{html}head/{html}title')))

#  ▣ 토론 : 네임스페이스를 포함한 XML 문서를 파싱하기는 꽤나 복잡하다.
#            XMLNamespaces 클래스는 짧게 줄인 네임스페이스 이름을 쓸 수 있도록 해서 코드를 정리해 줄 뿐이다.
#            하지만 iterparse() 함수를 사용한다면 네임스페이스 처리의 범위에 대해서 정보를 조금 더 얻을 수는 있다.
from xml.etree.ElementTree import iterparse
for evt, elem in iterparse('PythonCookBook/files/sample.xml', ('end', 'start-ns', 'end-ns')):
    print(evt, elem)

#  ※ 파싱하려는 텍스트가 네임스페이스나 여타 고급 XML 기능을 사용한다면 ElementTree 보다는 lxml 라이브러리를 사용하는 것이 좋다.


#  6.8 관계형 데이터베이스 작업
#  ▣ 문제 : 관계형 데이터베이스에 선택, 삽입, 행 삭제 등의 작업을 하고 싶다.
#  ▣ 해결 : 파이썬에서 데이터 행을 나타내는 표준은 튜플 시퀀스이다.
stocks = [('GOOG', 100, 490.1), ('AAPL', 50, 545.75), ('FB', 150, 7.45), ('HPQ', 75, 33.2)]

#   - sqlite3 데이터베이스 연결
import sqlite3
db = sqlite3.connect('database.db')

#   - 데이터 관련 작업을 위한 커서 생성 및 쿼리 실행
c = db.cursor()
c.execute('create table portfolio (symbol text, shares integer, price real)')
db.commit()

#   - 데이터에 행의 시퀀스를 삽입하려면 다음 구문을 사용한다.
c.executemany('insert into portfolio values (?,?,?)', stocks)
db.commit()

#   - 값 추출
for row in db.execute('select * from portfolio'):
    print(row)

#   - 사용자가 입력한 파라미터를 받는 쿼리를 수행하려면 ? 를 사용해 파라미터를 이스케이핑 해야 한다.
min_price = 100
for row in db.execute('select * from portfolio where price >= ?', (min_price,)):
    print(row)

#  ▣ 토론 : 날짜와 같은 자료를 저장할 때 datetime 모듈의 datetime 인스턴스나 타임스탬프를 사용하는 것이 일반적이다.
#            그리고 금융 자료와 같이 숫자를 저장할 때는 decimal 모듈의 Decimal 인스턴스를 사용하는 경우가 많다.
#            하지만 이에 대한 정확한 매핑은 데이터베이스 백엔드에 따라 달라지기 때문에 관련 문서를 잘 읽어 봐야 한다.
#            또, 절대로 파이썬의 서식화 연산자(% 등)나 .format() 메소드로 문자열을 만들면 안 된다.
#            서식화 연산자에 전달된 값이 사용자의 입력에서 오는 것이라면 SQL 주입 공격을 당할 수 있다.


#  6.9 16 진수 인코딩, 디코딩
#  ▣ 문제 : 문자열로 된 16진수를 바이트 문자열로 디코딩하거나, 바이트 문자열을 16진법으로 인코딩해야 한다.
#  ▣ 해결 : 문자열을 16진수로 인코딩하거나 디코딩하려면 binascii 모듈을 사용한다.
s = b'Hello'

import binascii
h = binascii.b2a_hex(s)  # 16진법으로 인코딩
print(h)
print(binascii.a2b_hex(h))  # 바이트로 디코딩

#   - base64 모듈에도 유사한 기능이 있다.
import base64
h = base64.b16encode(s)  # 16진법으로 인코딩
print(h)
print(base64.b16decode(h))  # 바이트로 디코딩

#  ▣ 토론 : 두 기술의 차이점은 바로 대소문자 구분에 있다.
#            base64.b15decode() 와 base64.b16encode() 함수는 대문자에만 동작하지만 binascii 는 대소문자를 가리지 않는다.

#   - 인코딩 함수가 만들 출력물은 언제나 바이트 문자열이지만 반드시 유니코드를 사용해야 한다면 디코딩 과정을 하나 더 추가해야 한다.
h = base64.b16encode(s)
print(h)
print(h.decode('ascii'))
#  ※ 16진수를 디코딩할 때 b16decode() 와 a2b_hex() 함수는 바이트 혹은 유니코드 문자열을 받는다.
#     하지만 이 문자열에는 반드시 ASCII 로 인코딩한 16진수가 포함되어 있어야 한다.


#  6.10 Base64 인코딩, 디코딩
#  ▣ 문제 : Base64 를 사용한 바이너리 데이터를 인코딩, 디코딩해야 한다.
#  ▣ 해결 : base64 모듈에 b64encode() 와 b64decode() 함수를 사용하면 이 문제를 해결할 수 있다.
s = b'hello'

import base64
a = base64.b64encode(s)  # Base64 로 인코딩
print(a)
print(base64.b64decode(a))  # Base64 를 디코딩

#  ▣ 토론 : Base64 인코딩은 바이트 문자열과 바이트 배열과 같은 바이트 데이터에만 사용하도록 디자인되었다.
#            또한 인코딩의 결과물은 항상 바이트 문자열이 된다. Base64 인코딩 데이터와 유니코드 텍스트를 함께 사용하려면
#            추가적인 디코딩 작업을 거쳐야 한다.
a = base64.b64encode(s).decode('ascii')
print(a)


#  6.13 데이터 요약과 통계 수행
#  ▣ 문제 : 커다란 데이터세트를 요약하거나 통계를 내고 싶다.
#  ▣ 해결 : 통계, 시계열 등과 연관 있는 데이터 분석을 하려면 Pandas 라이브러리를 알아봐야 한다.
import pandas

emp = pandas.read_csv('PythonCookBook/files/emp.csv', skip_footer=1)
print(emp)

#   - 특정 필드에 대해 값의 범위를 조사한다.
print(emp['sal'].unique())  # 특정 필드에 대해 유니크한 값을 리스트로 출력

#   - 데이터 필터링
emp_clerks = emp[emp['job'] == 'CLERK']
print(emp_clerks)

#   - 가장 많은 deptno 2개 추출
emp_dept = emp['deptno'].value_counts()[:2]
print(emp_dept)

#   - hiredate 로 그룹 짓기
dates = emp.groupby('hiredate')
print(dates)

#   - 각 날짜에 대한 카운트 얻기
date_counts = dates.size()
print(date_counts[0:10], type(date_counts))

#   - 카운트 정렬
date_counts.sort()  # sort() 는 deprecated 됨
date_counts.sort_values()
print(date_counts[-10:])

#  ▣ 토론 : 웨스 멕킨리의 Python for Data Analysis 에서 더 많은 정보를 얻을 수 있으니 참고하도록 하자.


# Chapter 7. 함수
#  7.1 매개변수 개수에 구애 받지 않는 함수 작성
#  ▣ 문제 : 입력 매개변수 개수에 제한이 없는 함수를 작성하고 싶다.
#  ▣ 해결 : 위치 매개변수 개수에 제한이 없는 함수를 작성하려면 * 인자를 사용한다.
def avg(first, *rest):
    return (first + sum(rest)) / (1 + len(rest))

print(avg(1, 2), avg(1, 2, 3, 4))

#   - 키워드 매개변수 수에 제한이 없는 함수를 작성하려면 ** 로 시작하는 인자를 사용한다.
import html

def make_element(name, value, **attrs):
    keyvals = [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(name=name, attrs=attr_str, value=html.escape(value))
    return element

print(make_element('item', 'Albatross', size='large', quantity=6))
print(make_element('p', '<spam>'))

#   - 위치 매개변수와 키워드 매개변수를 동시에 받는 함수를 작성하려면, * 와 ** 를 함께 사용하면 된다.
def anyargs(*args, **kwargs):
    print(args)  # 튜플 args
    print(kwargs)  # 딕셔너리 kwargs

#  ▣ 토론 : * 는 함수 정의의 마지막 위치 매개변수 자리에만 올 수 있다.
#           ** 는 마지막 매개변수 자리에만 올 수 있다. 그리고 * 뒤에도 매개변수가 또 나올 수 있다는 것이 함수 정의의 미묘한 점이다.
def a(x, *args, y):
    pass

def b(x, *args, y, **kwargs):
    pass


#  7.2 키워드 매개변수만 받는 함수 작성
#  ▣ 문제 : 키워드로 지정한 특정 매개변수만 받는 함수가 필요하다.
#  ▣ 해결 : 이 기능은 키워드 매개변수를 * 뒤에 넣거나 이름 없이 * 만 사용하면 간단히 구현할 수 있다.
def recv(maxsize, *, block):
    print('Receives a message')
    pass

recv(1024, True)
recv(1024, block=True)

#   - 숫자가 다른 위치 매개변수를 받는 함수에 키워드 매개변수를 명시하는 경우.
def mininum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m

print(mininum(1, 5, 2, -5, 10))
print(mininum(1, 5, 2, -5, 10, clip=0))

#  ▣ 토론 : 키워드로만 넣을 수 있는(keyword-only) 인자는 추가적 함수 인자를 명시할 때 코드의 가독성을 높이는 좋은 수단이 될 수 있다.
msg = recv(1024, False)
#  ※ 위의 경우처럼 recv() 가 어떻게 동작하는지 잘 모르는 사람이 있다면 False 인자가 무엇을 의미하는지도 모를 것이다.
#     따라서 호출하는 측에서 다음과 같은 식으로 표시해 준다면 이해하기 훨씬 쉽다.
msg = recv(1024, block=False)

#   - 키워드로만 넣을 수 있는 인자는 **kwargs 와 관련된 것에 사용자가 도움을 요청하면 도움말 화면에 나타난다.
print(help(recv))


#  7.3 함수 인자에 메타데이터 넣기
#  ▣ 문제 : 함수를 작성했다. 이때 인자에 정보를 추가해서 다른 사람이 함수를 어떻게 사용해야 하는지 알 수 있도록 하고 싶다.
#  ▣ 해결 : 함수 인자 주석으로 프로그래머에게 이 함수를 어떻게 사용해야 할지 정보를 줄 수 있다.
def add(x: int, y: int) -> int:
    return x + y

#   - 파이썬 인터프리터는 주석에 어떠한 의미도 부여하지 않는다.
#     타입을 확인하지도 않고, 파이썬의 실행 방식이 달라지지도 않는다.
#     단지 소스 코드를 읽는 사람이 이해하기 쉽도록 설명을 할 뿐이다.
help(add)
print(add(5, 4))

#   - 어떠한 객체도 함수에 주석으로 붙일 수 있지만, 대개 클래스나 문자열이 타당하다.

#  ▣ 토론 : 함수 주석은 함수의 __annotations__ 속성에 저장된다.
print(add.__annotations__)


#  7.4 함수에서 여러 값을 반환
#  ▣ 문제 : 함수에서 값을 여러 개 반환하고 싶다.
#  ▣ 해결 : 함수에서 값을 여러 개 반환하고 싶다면 간단히 튜플을 사용하면 된다.
def myfun():
    return 1, 2, 3

a, b, c = myfun()
print(a, b, c)

#  ▣ 토론 : myfun() 이 값을 여러 개 반환하는 것처럼 보이지만, 사실은 튜플 하나를 반환한 것이다.
#            조금 이상해 보이지만, 실제로 튜플을 생성하는 것은 쉼표지 괄호가 아니다.
a = (1, 2)
print(a)
b = 1, 2
print(b)

#   - 튜플 언패킹시 반환 값을 변수 하나에 할당하는 경우
x = myfun()
print(x)


#  7.5 기본 인자를 사용하는 함수 정의
#  ▣ 문제 : 함수나 메소드를 정의할 때 하나 혹은 그 이상 인자에 기본 값을 넣어 선택적으로 사용할 수 있도록 하고 싶다.
#  ▣ 해결 : 표면적으로 선택적 인자를 사용하는 함수를 정의하기는 쉽다. 함수 정의부에 값을 할당하고 가장 뒤에 이름 위치시키기만 하면 된다.
def spam(a, b=42):
    print(a, b)

spam(1)
spam(1, 2)

#   - 기본 값이 리스트, 세트, 딕셔너리 등 수정 가능한 컨테이너인 경우 None 을 사용해 코드 작성
def spam(a, b=None):
    if b is None:
        b = []

#   - 함수가 받은 값이 특정 값인지 아닌지 확인하는 코드
_no_value = object()

def spam(a, b=_no_value):
    if b is _no_value:
        print('No b value supplied')

spam(1)
spam(1, 2)
spam(1, None)

#  ▣ 토론 : 신경 써야 할 부분.
#   1. 할당하는 기본 값은 함수를 정의할 때 한 번만 정해지고 그 이후에는 변하지 않는다.
x = 42
def spam(a, b=x):
    print(a, b)

spam(1)
x = 23  # x 값이 바뀌어도 x = 42 일때 함수가 정의되었으므로 b = 42 이다.
spam(1)

#   2. 기본 값으로 사용하는 값은 None, True, False, 숫자, 문자열 같이 항상 변하지 않는 객체를 사용해야 한다.
def spam(a, b=[]):
    print(b)
    return b

x = spam(1)
print(x)

x.append(99)
x.append('Yow!')
print(x)
spam(1)
#   ※ 이런 부작용을 피하려면 앞의 예제에 나왔듯이 기본 값으로 None 을 할당하고 함수 내부에서 이를 확인하는 것이 좋다.

def spam(a, b=None):
    if not b:
        b = []

spam(1)      # 올바름
x = []
spam(1, x)   # 에러. x 값이 기본으로 덮어쓰여진다.
spam(1, 0)   # 에러. 0이 무시된다.
spam(1, '')  # 에러. ''이 무시된다.


#  7.6 이름 없는 함수와 인라인 함수 정의
#  ▣ 문제 : sort() 등에 사용할 짧은 콜백 함수를 만들어야 하는데, 한 줄짜리 함수를 만들면서 def 구문까지 사용하고 싶지는 않다.
#            그 대신 "인라인(in line)"이라 불리는 짧은 함수를 만들고 싶다.
#  ▣ 해결 : 표현식 계산 외에 아무 일도 하지 않는 간단한 함수는 lambda 로 치환할 수 있다.
add = lambda x, y: x + y
print(add(2, 3))
print(add('hello', 'world'))

#   - 앞에 나온 lambda 는 다음의 예제 코드와 완전히 동일하다.
def add(x, y):
    return x + y
print(add(2, 3))

#   - 일반적으로 lambda 는 정렬이나 데이터 줄이기 등 다른 작업에 사용할 때 많이 쓴다.
names = ['David Beazley', 'Brian Jones', 'Raymond Hettinger', 'Ned Batchelder']
print(sorted(names, key=lambda name: name.split()[-1].lower()))  # 뒤에 글자로 정렬하는 경우

#  ▣ 토론 : lambda 를 사용해서 간단한 함수를 정의할 수 있지만, 제약이 아주 많다.
#            우선 표현식을 하나만 사용해야 하고 그 결과가 반환 값이 된다.
#            따라서 명령문을 여러 개 쓴다거나 조건문, 순환문, 에러 처리 등을 넣을 수 없다.


#  7.7 이름 없는 함수에서 변수 고정
#  ▣ 문제 : lambda 를 사용해서 이름 없는 함수를 정의했는데, 정의할 때 특정 변수의 값을 고정하고 싶다.
#  ▣ 해결 : 다음 코드의 동작성을 고려해 보자.
x = 10
a = lambda y: x + y
x = 20
b = lambda y: x + y

print(a(10), b(10))  # lambda 에서 사용하는 값은 실행 시간에 따라 달라지는 변수이므로 값은 같다.

#   - 이름 없는 함수를 정의할 때 특정 값을 고정하는 경우
x = 10
a = lambda y, x=x: x + y
x = 20
b = lambda y, x=x: x + y
print(a(10), b(10))

#  ▣ 토론 : 리스트 컴프리핸션이나 반복문에서 람다 표현식을 생성하고 람다 함수가 순환 변수를 기억하려고 할때 문제가 발생한다.
funcs = [lambda x: x+n for n in range(5)]
for f in funcs:
    print(f(0))

#   - 다음 코드와 비교해 보자
funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
    print(f(0))
#   ※ 이제 n 값을 함수를 정의하는 시점의 값으로 고정해 놓고 사용한다.