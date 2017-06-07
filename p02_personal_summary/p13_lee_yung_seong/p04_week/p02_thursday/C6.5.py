#딕셔너리를 xml로 바꾸기
#문제
#파이썬 딕셔너리 데이터를 받아서 XML로 바꾸고 싶다.
#해결
#xml.etree.Elementtree 라이브러리는 파싱에 일반적으로 사용하지만, xml 문서를 생성할 때 사용하기도 한다.
from xml.etree.ElementTree import Element
def dict_to_xml(tag,d):
    """
    간단한 dict를 xml로 변환
    """
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

#예제는 다음과 같ㄷ.
s={'name' : 'GooG', 'shares' : 100, 'price':490.1}
e=dict_to_xml('stock',s)
e
#이 변환의 결과로 Element 인스턴스가 나온다. I/O를 위해서 xml.etree.ElementTree의 tostring() 함수로 이를 바이트 문자열로 변환하기는 어렵지 않다.
from xml.etree.ElementTree import tostring
tostring(e)
#요소에 속성을 넣고 싶으면 set()메소드
e.set('_id','1234')
tostring(e)
#요소에 순서를 맞추어야 한다면 일반 딕셔너리를 사용하지 않고 ordereddict를 사용한다.
#토론
#xml을 생성할 때 단순히 문자열을 사용하고 싶을 수도 있다.
def dict_to_xml_str(tag,d):
    '''
    간단한 dict를 xml로 변환하기
    '''
    parts = ['<{}>'.format(tag)]
    for key, val in d.items():
        parts.append('<{0}>{1}</{0}>'.format(key,val))
    parts.append('</{}>'.format(tag))
    return ''.join(parts)
#하지만 이 작업을 수동으로 하면 코드가 엄청나게 복잡해 질 수 있다. 예를 들어 딕셔너리에 다음과 같이 특별 문자가 포함되어 있다면 어떨까?
d={'name':'<spam>'}
#문자열 생성
dict_to_xml('item',d)
#올바른 xml 생성
tostring(e)
#마지막 예제에서 <와 > 문자가 %lt;와 &gt;로 치환되었다.
#이런 문자를 수동으로 이스케이핑 하고 싶다면 xml.sax.saxutil의 escape()와 unescape() 함수를 사용한다.
from xml.sax.saxutils import escape, unescape
escape('<spam>')
unescape(_)
#올바른 출력을 만드는 것 외엗 ㅗ문자열 대신 element 인스턴스를 만드는 것이 좋은 이유는 이들을 더 쉽게 합쳐 큰 문서를 만들 수 있기 때문이다.
#결과 element 인스턴스는 xml 파싱에 대한 염려 없이 여러 방법으로 처리할 수 있다. 사실 모든 데이터 처리를 상위 레벨 형식으로 할 수 있고, 마지막에는 문자열로 출력도 가능하다.
