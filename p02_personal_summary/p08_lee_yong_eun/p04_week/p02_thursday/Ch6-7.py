##########################################################################################################
# 6.7] 네임스페이스로 XML 문서 파싱
#   * XML 문서를 파싱할 때 XML 네임스페이스를 사용하고 싶다.
#       : 유틸리티 클래스로 네임스페이스를 감싸준다.
#
#   * 네임스페이스를 포함한 XML 문서를 파싱하기는 꽤나 복잡하다.
#      아래의 XMLNamespaces 클래스는 짧게 줄인 네임스페이스 이름을 쓸 수 있도록 해서 코드를 정리해 줄 뿐이다.
#      안타깝게도 ElementTree 파서에 네임스페이스에 대한 더 많은 정보를 얻을 수 있는 방법은 없다.
#      하지만 iterparse() 함수를 사용한다면 네임스페이스 처리의 범위에 대해 정보를 조금 더 얻을 수는 있다.
#   * 파싱하려는 텍스트가 네임스페이스나 여타 고급 XML 기능을 사용한다면
#      ElementTree보다는 더 많은 기능을 가진 lxml 라이브러리를 사용하는 것이 좋다.
##########################################################################################################

# 유틸리티 클래스로 네임스페이스를 감싸준다
class XMLNamespaces:
    def __init__(self, **kwargs):
        self.namespaces = {}
        for name, uri in kwargs.items():
            self.register(name, uri)

    def register(self, name, uri):
        self.namespaces[name] = '{' + uri + '}'

    def __call__(self, path):
        return path.format_map(self.namespaces)

# 사용 예시
from xml.etree.ElementTree import parse
doc = parse('gg.xml')
ns = XMLNamespaces(html='http://www.w3.org/1999/xhtml')
doc.find(ns('content/{html}html'))
doc.findtext(ns('content/{html}html/{html}head/{html}/title'))