#xml 파싱, 수정, 저장
#문제
#xml 문서를 읽고, 수정, 수정 내용을 저장학 ㅗ싶다.
#해결
#xml.etree.elementtree 모듈로 이 문제를 간단히 해결 할 수 있다. 우선 일반적인 방식으로 문서 파싱부터 시작한다
#수정방법
from xml.etree.ElementTree import parse, Element
doc = parse('pred.xml')
root = doc.getroot()
root

#요소 몇개 제거하기
root.remove(root.find('sri'))
root.remove(root.find('cr'))
#<nm>...</nm> 뒤에 요소 몇개삽입하기
root.getchildren().index(root.find('nm'))
e = Element('spam')
e.text='this is a test'
root.inset(2,e)
#파일에 쓰기
doc.write('newpred.xml',xml_declaration=True)
#토론
#xml문서의 구조를 수정하는 것은 어렵지 않지만 모든 수정 사항은 부모 요소에도 영향을 미쳐 리스트 인 것처럼 다루어 진다는 점을 기억해야 한다.