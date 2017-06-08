##########################################################################################################
# 6.6] XML 파싱, 수정, 저장
#   * XML 문서를 읽고, 수정하고, 수정 내용을 XML에 반영하고 싶다.
#       : xml.etree.ElementTree 모듈로 이 문제를 간단히 해결할 수 있다.
##########################################################################################################
from xml.etree.ElementTree import parse, Element

doc = parse('pred.xml')
root = doc.getroot()

# 요소 몇개 제거하기
root.remove(root.find('sri'))
root.remove(root.find('cr'))

# <nm>..</nm> 뒤에 요소 몇개 삽입하기
root.getchildren().index(root.find('nm'))
e = Element('spam')
e.text = 'This is a test'
root.insert(2, 3)

# 파일에 쓰기
doc.write('newpred.xml', xml_declaration=True)