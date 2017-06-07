#매우 큰 xml파일 증분 파싱하기
#문제
#매우 큰 xml 파일에서 최소의 메모리만 사용하여 데이터를 추출하고 싶다.
#해결
#증분 데이터 처리에 직면할 때면 언제나 이터레이터와 제너레이터를 떠올려야 한다. 여기 아주 큰 xml 파일을 증분적으로 처리하며 메모리 사용은 최소로 하는 함수를 보자.
from xml.etree.ElementTree import iterparse
def parse_and_remove(filename,path):
    path_parts = path.split('/')
    doc = iterparse(filename,('start','end'))
    next(doc)#뿌리요소 건너뛰기

    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem)
        elif event == 'end'
            if tag_stack == path_parts:
                yield elem
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass
#함수를 테스트 하기 위해 커다란 xml 파일이 필요.
#도로의 움푹 패안 곳의 숫자를 사용하여 zip코드별로 순위를 매기는 스크립트를 작성한다고 가정해보자
from xml.etree.ElementTree import parse
from collections import Counter

potholes_by_zip = Counter()
doc = parse('potholes.xml')
for pothole in doc.iterfind('row/row'):
    potholes_by_zip.findtext('zip')] += 1

for zipcode, num in potholes_by_zip.most_common():
    print(zipcode,num)

#이 메모리는 7mb만 소비

#토론
#이번 레시피는 elementtree 모듈의 두 가지 필수 기능에 의존하고 있다. 첫번째는 iterparse() 메소드로 xml ㅜㅁㄴ서를 증분 파싱할 수 있게 한다.
#이 메소드를 사용하기 위해서는 파일 이름과 start,end,start-ns, end-ns 중 하나 이상을 포함한 이벤트 리스트를 넘겨 주어야 한다. iterparse()가 생성한 이터레이터는
#(event,elem)으로 구성된 튜플을 만드는데, 이벤트는 리스팅 된 이벤트 중 하나이고 elem은 결과로 나온 xml 요소이다.
data = iterparse('potholes.xml',('start','end'))
next(data)

#start 이벤트는 요소가 처음 생성디ㅗ었지만 다른 데이터를 만들지 않았을 때 생성된다, end 이벤트는 요소를 마쳤을 때 생성된다.
#이번 레시피에 나오지는 않지만 start-ns end-ns 이벤트는 xml 네임스페이스 선언을 처리하기 위해 사용한다.
#메모리 소비가 우선시 되는 상황이면 증분식 코드가 훨씬유리.

