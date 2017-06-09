#네임스페이스 xml문서 파싱
#xml문서를 파싱할 때 xml 네임스페이스를 사용하고 싶다.
#해결
#다음과 같이 네임 스페이스를 사용하는 문서를 고려해보자.
#동작하는 쿼리
doc.findtext('authhor')
doc.find('content')

#네임스페이스 관련 쿼리(동작하지 않음)
doc.find('content/html')
#조건에 맞는 경우에만 동작
doc.find('content/{http:....}')
#동작하지 않음
doc.findtext('content/{http://...')
#조건에 일치함
doc.findtext('content/{http://')

#유틸리티 클래스로 네임스페이스를 감싸주면 문제를 더 단순화 할 수 있다.
class XMLNamespaces:
    def __init__(self,**kwargs):
        self.namespaces={}
        for name, uri in kwargs.items():
            self.register(name,uri)
    def register(self,name,uri):
        self.namespace[name] = '{'+uri+'}'
    def __call__(self,path):
        return path.format_map(self.namespaces)

#이 클래스를 사용할면 다음과 같이 한다.
ns = XMLNamespaces(html='http://...')
doc.find(ns('content/{html}html'))
doc.findtext(ns('content..'))

#네임 스페이스를 포함한 xml 문서를 파싱하기는 꽤나 복잡하다. XMLNamespaces 클래스를 짧게 줄인 네임스페이스 이름을 쓸 수 있도록 해서 코드를 정리해줄 뿐이다.
#안타깝게도 elementtree 파서에 네임스페이스에 대한 더 많은 정보를 얻을 수 있는 방법은 없다
#하지만 iterparse() 함수를 사용한다면 네임스페이스 처리의 범위에 대해서 정보를 조금 더 얻을 수는 있다.
from xml.etree.ElementTree import iterparse
for evt, elem in iterparse('ns2.xml',('end','start-ns','end-ns')):
    print(evt,elem)

#마지막으로 파싱하려는 텍스트가 네임 스페이스나 여타 고급 xml 기능을 사용한다면 elemtree보다는 lxml라이브러리를 사용하는 것이 좋다. 예를 들어 lxml은 DTD에 대한 검증을 지원하고
#xpath등 더 많은 기능을 가지고 있다. 이번 레시피는 파싱에 도움을 주기 위한 아주 간단한 수정을 할 뿐이다.