'''
'''

'''

6장 5절 딕셔너리를 XML로 바꾸기 : 파이썬 딕셔너리 데이터를 받아서 XML로 바꾸고 싶은 경우 xml.etree.ElementTree 라이브러리는 일반적으로 파싱에 사용하지만 XML문서를
                              작성할 때도 사용한다.

- 파싱 : 파싱(parsing)은 일련의 문자열을 의미있는 토큰(token)으로 분해하고 이들로 이루어진 파스 트리(parse tree)를 만드는 과정을 말한다.
        컴퓨팅에서 파서(parser)는 인터프리터나 컴파일러의 구성 요소 가운데 하나로, 입력 토큰에 내재된 자료 구조를 빌드하고 문법을 검사한다. 
        파서는 일련의 입력 문자로부터 토큰을 만들기 위해 별도의 낱말 분석기를 이용하기도 한다. 
        파서는 수작업으로 프로그래밍되며 도구에 의해 (일부 프로그래밍 언어에서) (반)자동적으로 만들어질 수 있다.
        
        가공되지 않은 데이터에서 원하는 특정 문자열을 빼내는 작업을 얘기한다.
        
        파싱을 하는 프로그램, 스크립트 등을 파서(Parser)라고 한다.
        
        
- XML : XML(Extensible Markup Language)은 W3C에서 개발된, 다른 특수한 목적을 갖는 마크업 언어를 만드는데 사용하도록 권장하는 다목적 마크업 언어이다. 
        XML은 SGML의 단순화된 부분집합으로, 다른 많은 종류의 데이터를 기술하는 데 사용할 수 있다. 
        XML은 주로 다른 종류의 시스템, 특히 인터넷에 연결된 시스템끼리 데이터를 쉽게 주고 받을 수 있게 하여 HTML의 한계를 극복할 목적으로 만들어졌다.
        XML은 문서를 사람과 기계 모두가 읽을 수 있는 형식을 갖도록 규정하고 있다. 
        W3C가 만든 XML 1.0 Specification과 몇몇 다른 관련 명세들과 모든 자유 개방형 표준에서 정의되었다
        
        XML에서의 기본 개념에는 10가지가 있다.

        - XML은 구조적인 데이터를 위한 것이다.
        - XML은 다소 HTML 같이 보인다.
        - XML은 텍스트이며, 읽히는 것만을 뜻하지 않는다.
        - XML은 크기가 커진다.
        - XML은 기술의 집합이다.
        - XML은 새로운 기술이 아니라 발전한 기술이다.
        - XML은 HTML에서 XHTML로 이끌었다.
        - XML은 모듈식이다.
        - XML은 RDF와 시맨틱 웹의 토대이다.
        - XML은 라이선스 제약이 없으며, 플랫폼이 독립적이고, 많은 지원이 있다.

        XML 기반 언어는 다음과 같다.

        - RDF
        - RSS
        - Atom
        - MathML
        - XHTML
        - SVG
            
        XML에서 사용하는 주요 용어
            
        - (유니코드) 문자 : 정의 상, XML 문서는 문자로 이루어진 문자열이다. 거의 모든 올바른 유니코드 문자는 XML 문서에 나타날 수 있다.
        - 프로세서(processor)와 애플리케이션(application) : 프로세서는 마크업을 분석하고 구조화된 정보를 애플리케이션에 넘긴다. 
                                                        이 명세는 XML 프로세서가 무엇을 해야하고 하지 말아야 하는지 제시하지만, 
                                                        애플리케이션에 대해서는 다루지 않는다. 이 프로세서(명세가 부르기를)는 흔히 XML parser라 불린다.
        - 마크업(markup)과 내용(content) : XML 문서를 구성하는 문자들은 마크업과 내용으로 나뉘는데, 그 구분은 간단한 문법 규칙으로 이루어진다. 
                                         마크업을 구성하는 문자열은 < 나 &로 시작, > 나 ;로 끝나며, 마크업이 아닌 문자열은 내용이다. 
                                         그러나, CDATA 절에서, 구분자 <![CDATA[와 ]]>는 마크업으로 분류되고, 그들 사이의 텍스트는 내용으로 구분된다. 
                                         추가로, 가장 바깥 엘리먼트의 앞과 뒤의 공백(whitespace)은 마크업으로 분류된다.
        - 태그(tag) : <로 시작하여 >로 끝나는 마크업 구조. Tags come in three flavors
                    시작 태그(start-tag); 예: <section>
                    끝 태그(end-tag); 예: </section>
                    빈 엘리먼트(empty-element) 태그; 예: <line-break />
        - 엘리먼트(element) : 문서의 논리 요소로서, 시작 태그로 시작하여 짝이 되는 끝 태그로 끝나거나, 빈 엘리먼트 태그만으로 이루어진다. 
                             시작 태그와 끝 태그 사이의 문자들은(있다면) 엘리먼트의 내용이고, 마크업을 포함할 수 있다. 
                             이 마크업은 자식 엘리먼트(child elements)라 부르는 다른 엘리먼트들을 포함할 수도 있다. 
                             엘리먼트의 예는 <Greeting>Hello, world.</Greeting> (see hello world). 다른 예는 <line-break />.
        - 애트리뷰트(Attribute) : 이름/값 짝으로 이루어진 마크업 구조로 시작 태그 또는 빈 엘리먼트 태그 속에 위치한다.
                                 예)
                                    <img src="madonna.jpg" alt='Foligno Madonna, by Raphael'/>
                                         img 엘리먼트는 어트리뷰트 src와 alt를 갖고있다.
                                          
- XML을 생성할 떄 딕셔너리에 특별 문자가 있는 것 처럼 단순히 문자열 그 자체만을 사용하고 싶을 때 자동치환(<가 &lt로 바뀌는 것 등)을 방지하려면 xml.sax.saxutils의
  escape()와 unescape() 함수를 사용한다.
        
'''

# 예1.
from xml.etree.ElementTree import Element

def dict_to_xml(tag, d):
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

s = {'name' : 'GOOG', 'shares' : 100, 'price' : 490.1}
e = dict_to_xml('shock', s)
e
# <Element 'shock' at 0x1004b64c8>    # Element 인스턴스가 나왔다. tostring() 함수로 바이트 문자열을 읽을 수 있게 변환하면 다음과 같다.
from xml.etree.ElementTree import tostring
tostring(e)
# b'<shock><name>GOOG</name><shares>100</shares><price>490.1</price></shock>'

#.set() 메소드를 사용해서 요소(stock)에 속성을 넣을 수 있다.
e.set('_id', '1234')
tostring(e)
# b'<shock _id="1234"><name>GOOG</name><shares>100</shares><price>490.1</price></shock>'


# 예2.
from xml.sax.saxutils import  import escape, unescape
escape('<spam>')
#'&lt;spam&gt;'
unescape(_)
'<spam>'

'''

6장 6절 XML 파싱, 수정, 저장 : XML 문서를 읽고 수정하고 수정 내용을 XML에 반영하고 싶은 경우 xml.etree.ElementTree 모듈로 해결할 수 있다.
                            문서작업을 하려면 일단 파싱을 해야된다.

- 모든 수정 사항은 리스트처럼 부모 요소에도 영향을 미친다. 한 요소를 제거하면 부모의 remove() 메소드를 사용해 바로 위 부모로부터 해당 요소가 제거된다.
  새로 요소를 추가하면 부모에 대해서도 insert()와 append() 메소드를 사용하게 된다. 모든 요소는 element[i], element[i:j] 처럼 인덱스와 슬라이스가 가능하다.


'''

# 예3.
from xml.etree.ElementTree import parse, Element
doc = parse('docname.xml')
root = doc.getroot()
root

root.remove(root.find('sri'))   # 요소 sri 제거
root.remove(root.find('cr'))    # 요소 cr 제거

root.getchildren().index(root.find('nm'))   # <nm> </nm> 뒤에 요소를 삽입하기
e = Element('spam')
e.text = 'This is a test'
root.insert(2, e)

doc.write('newdocname.xml', xml_declaration=True)


'''

6장 7절 네임스페이스로 XML 문자 파싱 : XML문자를 파싱할 때 XML 네임스페이스를 사용하고 싶은 경우 

- xml 네임스페이스(namespace)
    XML 문서 내에서 유일한 엘리먼트 이름이나 속성 이름을 제공하기 위해 사용된다.
    XML은 사용자가 자유롭게 엘리먼트를 정의할 수 있는 장점을 가지고 있지만 사용되는 엘리먼트가 XML 문서에서 중복될 수도 있다.
    이름이 같은 엘리먼트에 의해 발생할 수 있는 이름 충돌을 해결하기 위해 사용되는 것이 namespace이다.
    네임스페이스를 사용하기 위해 "xmlns"라는 속성을 사용한다.
    "xmlns" 속성값은 네임스페이스를 식별하기 위한 네임스페이스 이름이며, XML문서 내에서는 유일해야 한다.

    <엘리먼트이름 xmlns=”URI_Reference”>
    
    엘리먼트 이름은 기본 네임스페이스를 선언하는 엘리먼트 명을 지정하고 xmlns 속성은 기본 네임스페이스를 지정하기 위한 속성이다. 
    기본 네임스페이스는 접두어를 따로 기술하지 않고 기본 네임스페이스를 지정하면 해당 엘리먼트와 하위 엘리먼트가 모두 네임스페이스에 속하게 된다.
    기본 네임스페이스는 네임스페이스 접두어를 붙이지 않은 엘리먼트에만 적용되고 네임스페이스 접두어가 있는 속성에는 적용되지 않는다.
    
    예)
        기본 네임스페이스와 prof 네임스페이스를 사용한 xml
        
        <?xml version="1.0" encoding="euc-kr" standalone="yes"?>
        <school xmlns="http://www.hankook.ac.kr/student" 
	        xmlns:prof="http://www.hankook.ac.kr/professor">
	        <student>
		        <name>kyu</name>
		        <email>xml@test.com</email>
		        <address>방이동</address>
	        </student>
	        <professor>
		        <prof:name>tom</prof:name>
		        <prof:email>xml1@test.com</prof:email>
		        <prof:address>성내동</prof:address>
	        </professor>
        </school>
    

- 네임스페이스를 포함한 XML문서를 파싱하는 것은 복잡하다. 아래 예에서 생성한 XMLNamespaces 클래스는 짧게 줄인 네임스페이스 이름을 쓸 수 있도록 코드 정리만 해 줄 뿐이다.
  iterparse() 함수를 사용하면 네임스페이스 처리 범위에 대한 정보를 더 얻을 수 있다.
  파싱하려는 텍스트가 네임스페이스나 고급 XML 기능을 다수 포함하고 있으면 ElementTree보다 lxml 라이브러리를 사용해야 한다.
    
'''

# 예4.
class XMLNamespaces:
    def __init__(self, **kwargs):
        self.namespaces = {}
        for name, uri in kwargs.items():
            self.register(name, uri)

    def register(self, name, uri):
        self.namespaces[name] = '{'+uri+'}'

    def __call__(self, path):
        return path.format_map(self.namespaces)

ns = XMLNamespaces(html='http://w3.org/1999/xhtml')
doc.find(ns('content/{html}html'))
# <Element '{http://www.w3.org/1999/xhtml}html' at 0x1007767e0>
doc.findtext(ns('content/{html}html/{html}head/{html}title'))

'''

6장 8절 관계형 데이터베이스 작업 : 관계형 데이터베이스에 선택, 삽입, 행 삭제등의 작업을 하고 싶은 경우 sqlite3 모듈을 사용한다.
                              우선 connect() 함수에 데이터베이스 이름, 호스트 이름, 사용자 이름, 암호 등을 넣어서 데이터베이스와 연결한다.
                              그 다음 작업을 하기 위한 커서(Cursor)를 만들면 커서 내에서 SQL 쿼리를 실행할 수 있다.


'''

# 예5.
import sqlite3
db = sqlite3.connect('database.db')
c = db.cursor()
c.excute('Create table portfolio (symbol text, shares integer, price real)')
db.commit()

# 예6.
c.executemany('insert into portfolio values (a,b,c)', stocks)
db.commit()

# 예7.
for row in db.excute('select * from portfolio'):
    print(row)

# 예8.
min_price = 100
for row in db.execute('select * from portfolio where price >= aa', (min_price,)):
    print(row)


'''

7장 1절 매개변수 개수에 구애 받지 않는 함수 작성 : 입력 매개변수 개수에 제한이 없는 함수를 작성하고 싶은 경우 * 인자를 사용한다.

- *args : 위치인자들을 개수에 제한없이 args에 튜플형으로 받는다.
- **kwargs : 키워드 매개변수들을 개수에 제한 없이 kwargs에 딕셔너리형으로 받는다.

- *은 마지막 위치 매개 변수에만 사용 가능하고 마찬가지로 **도 마지막 매개변수 자리에만 올 수 있다.

'''


'''

7장 2절 키워드 매개변수만 받는 함수 작성 : 키워드로 지정한 특정 매개변수만 받는 함수가 필요하면 키워드 매개변수를 * 뒤에 넣거나 변수명 없이 *만 사용하면 된다.


'''

# 예9.
def recv(maxsize, *, block):
    'Recieves a message'
    pass

recv(1024,True)
# TypeError
recv(1024, block=True)

# 예10.
def mininum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m

mininum(1 ,5, 2, -5, 10)
# -5
mininum(1, 5, 2, -5, 10, clip=0)
# 0

'''

7장 3절 함수 인자에 메타데이터 넣기 : 함수를 작성하고 인자에 정보를 추가해서 다른 사람이 함수를 어떻게 사용해야 하는지 알 수 있도록 하고 싶으면 함수 인자 주석을 사용한다.

- 함수 인자에 :를 붙이고 주석을 넣을 수 있다.
- 주석은 __annotations__ 속성에 저장된다. 함수명.__annotations__ 를 실행하면 확인할 수 있다.
- 어떤 객체(숫자, 문자열, 인스턴스)도 함수에 주석으로 붙일 수 있지만 대개 클래스나 문자열을 사용한다.

'''

# 예11.
def add(x:int, y:int) -> int:
    return x + y

add.__annotations__
# {'return': int, 'x': int, 'y': int}


'''

7장 4절 함수에서 여러 값을 반환 : 함수에서 값을 여러개 반환하고 싶으면 튜플을 사용하면 된다.

- 실제 튜플을 생성하는건 괄호가 아니라 쉼표이다.
a = (1,2)
b = 1, 2

a
# (1, 2)
b
# (1, 2)

'''

# 예12.
def myfun():
    return 1, 2, 3

a, b, c = myfun()
a
# 1
b
# 2
c
# 3

'''

7장 5절 기본인자를 사용하는 함수 정의 : 함수나 메소드를 정의할 때 하나 혹은 그 이상 인자에 기본 값을 넣어 선택적으로 사용할 수 있도록 하고 싶은 경우 함수 정의부에 값을 할당
                                   하고 가장 뒤에 이를 위치시키면 된다.

- 할당하는 기본값은 함수를 정의할 때 한번만 정해지고 그 이후에는 변하지 안흔ㄴ다.
- 기본값으로 사용하는 값은 None, True, False, 숫자, 문자열 같이 항상 변하지 않는 객체를 사용해야 한다.
  부작용을 피하기 위해 기본 값으로 None을 할당하고 함수 내부에서 이를 확인하는편이 좋다.

'''

# 예13.
def spam(a, b=42):
    print(a, b)

spam(1)
spam(1, 2)

def spam1(a, b=None):
    if b is None:
        b=[]


'''

7장 6절 이름없는 함수와 인라인 함수 정의 : 한줄짜리 짧은 함수를 def 구문을 사용하지 않고 짧게 만들 때 lambda(익명함수)를 사용하면 된다.

- 인라인함수는 간단하지만 표현식을 하나만 사용해야하고 명령문을 여러개 쓰거나 조건, 순환문, 예외처리등을 넣을 수 없다.

'''

add = lambda x, y: x + y
add(2,3)
# 5


'''

7장 7절 이름 없는 함수에서 변수 고정 : lambda를 사용해서 이름 없는 함수를 정의헀는데, 정의할 떄 특정 변수의 값을 고정하고 싶은 경우 특정 값으로 고정하고 싶으면 그 값을 
                                  기본값으로 지정하면 된다. 람다 표현식에서 x값은 그 함수를 실행할 때의 값이다.

'''

x = 10
a = lambda y, x=x: x+y
x = 20
b = lambda y, x=x: x+y
a(10)
# 20
b(10)
# 30
