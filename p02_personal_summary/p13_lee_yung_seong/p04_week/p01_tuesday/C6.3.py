#단순한 xml 데이터 파싱
#단순한 xml 문서에서 데이터를 얻고 싶다
#해결
#단순한 xml 문서에서 데이터를 얻기 위해 xml.etree.ElementTree 모듈을 사용하면 된다. planet python에서 rss피드를 받아 파싱을 해야 한다고 가정해보자.
from urllib.request import urlopen
from xml.etree.ElementTree import parse
#rss피드를 다운로드하고 파싱한다.
u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(u)
#관심있는 태그를 뽑아서 출력한다.
for item in doc.iterfind('channel/item'):
    title = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')

print(title)
print(date)
print(link)
#토론
#많은 애플리케이션에서 xmlㄹ 인코딩된 데이터를 다룬다. 인터넷 상에서 데이터를 주고 받을 때 xml을 사용하는 곳이 많기도 하지만, 애플리케이션 데이터(워드 프로세싱, 응막 라이브러리 등)를 저장할 때도
#일반적으로 사용하는 형식이다. 이 뒤로 나오는 토론은 독자가 xml 기본내용에 익숙하다가고 가정함.
#많은 경우 xml이 데이터를 저장할 때 사용되면 문서구조는 단순하고 이해하기 쉽다. 예를 들어 앞에 나온 예제의 rss피드는 아마도 다음과 비슷할 것이다.
#xml.etree.ElementTree.parse()함수가 xml 문서를 파싱하고 문서 객체로 만든다. 여기서부터 특정 xml 요소를 찾기 위해 find(), iterfind(), findtext()와 같은 함수를 사용한다,
#함수에 사용하는 인자는 channel/item 또는 title과 같이 특정 태그의 이름을 사용한다.
#태그를 명시할 때 전체 문서 구조체를 고려해야 한다. 모든 찾기 작업은 시작 요소에 상대적으로 발생한다. 마찬가지로 함수에 전달하는 태그 이름 역시 시작에 상대적이다. 예를 들어,
#doc.iterfind('channel/item')호출은 channel 요소의 item 요소를 찾는다. doc은 문서의 상단을 나타낸다. (상위 레벨 rss요소). 그 이후 item.findtext() 호출은 item 요소를 찾은 곳에서 상대적으로 발생한다.
#ElementTree 모듈이 나타내는 모든 요소는 파싱에 유용하 요소와 메소드를 약간 가지고 있다 tag 요소에는 태그의 이름, text 요소에는 담겨있는 텍스트가 포함되어 있고, 필요 한 경우 get()메소드로 요소를 얻을 수 있다.
#xml 파싱에 xml.etree.ElementTree말고 다른 것을 사용할 수도 있다. 좀 더 고급 애플리케잇ㄴ을 개발 중이라면 lxml사용을 고려해보자.
#elementtree와 동일한 인터페이스를 사용학 ㅣ때문에 이번 레시피에 사용한 예제를 동일하게 사용할 수 있다. 단순히 처음 임포트 구문만 from lxml.etree import parse로 바꾸면 된다.
#lxml은 xml표준과 완벽히 동일한 혜택을 제공한다. 또한 매우 빠르고 검증, xslt, xpath와 같은 모든 기능을 제공한다.