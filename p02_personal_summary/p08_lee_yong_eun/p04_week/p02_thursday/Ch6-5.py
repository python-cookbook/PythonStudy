##########################################################################################################
# 6.5] 딕셔너리를 XML로 바꾸기
#   * 파이썬 딕셔너리 데이터를 받아서 XML로 바꾸고 싶다.
#       : xml.etree.ElementTree
#           일반적으로 파싱에 사용하지만, XML 문서를 생성할 때도 사용할 수 있다.
#       * 단순히 문자열을 나열해서 XML 문서를 만들 수도 있지만, 코드가 엄청나게 복잡해질 뿐더러
#         <나 > 등의 특별 문자가 포함되어있는 경우엔 또 다른 처리가 필요하다.
#         또한, 문자열 대신 Element 인스턴스를 만드는 것이 좋은 이유는 이들을 더 쉽게 합쳐 큰 문서를 만들 수 있기 때문이다.
#         Element 인스턴스는 XML 파싱에 대한 염려 없이 여러 방식으로 처리할 수 있다.
#
#   * 딕셔너리 데이터의 순서를 맞춰야 한다면 OrderedDict를 사용하자.(1.7 참조)
##########################################################################################################
from xml.etree.ElementTree import Element

# 간단한 dict를 XML로 변환하기
def dict_to_xml(tag, d):
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

# 예제
s = {'name': 'GOOG', 'shares': 100, 'price': 490.1}
e = dict_to_xml('stock', s)
print(e)    # <Element 'stock' at 0x0123D8D0>

# 내용 확인
from xml.etree.ElementTree import tostring
print(tostring(e))  # b'<stock><name>GOOG</name><shares>100</shares><price>490.1</price></stock>'

# 속성 추가
e.set('_id', '1234')
print(tostring(e))  # b'<stock _id="1234"><name>GOOG</name><shares>100</shares><price>490.1</price></stock>'