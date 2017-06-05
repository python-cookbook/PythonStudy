''''''
'''
5장 14절 파일 이름 인코딩 우회 : 시스템의 기본 인코딩으로 디코딩 혹은 인코딩 되지 않은 파일 이름에 입출력 작업ㅇ르 수행해야 할 때 sys.getfilesystemencoding()이 반환하는 텍스트 인코딩 값으로 디코딩 혹은 인코딩 되어 있다.

'''

'''

5장 15절 망가진 파일 이름 출력 : 프로그램에서 디렉터리 리스트를 받아 파일 이름을 출력하려고 할 때 UnocodeEncodeError와 surrogates not allowed 메세지가 발생하면서 프로그램이 사망할 경우 아래 코드로 에러를 방지한다.

def bad_filename(filename):
return repr(filename)[1:-1]

try:
    print(filename)
except UnicodeEncodeError:
    print(bad_filename(filename))

'''

'''

5장 16절 이미 열려있는 파일의 인코딩을 수정하거나 추가하기 : 이미 열려있는 파일을 닫지 않고 유니코드 인코딩을 추가하거나 변경하고 싶을 땐 해당 객체를 io.TextIOWrapper() 객체로 감싼다.


'''

# 예1.
import urllib.request
import io
u = urllib.request.urlopen('http://python.org')
f = io.TextIOWrapper(u, encoding='UTF-8')
text = f.read()

'''

5장 17절 텍스트 파일에 바이트 쓰기 : 텍스트 모드로 연 파일에 로우 바이트를 사용하고 싶은 경우 단순히 바이트 데이터를 buffer에 쓴다.

- sys.stdout은 언제나 텍스트 모드로 열려 있는데 바이너리 데이터를 표준 출력에 출력하는 스크립트를 작성한다면 이 기술을 사용해서 텍스트 인코딩을 우회할 수 있다.

'''

'''
5장 18절 : 기존 파일 디스크립터를 파일 객체로 감싸기 : 운영 체제 상에 이미 열려있는 IO 채널에 일치하는 정수형 파일 디스크립터를 가지고 이를 상위 레벨으 파이썬 파일 객체로 감싸고 싶은 경우 open()함수를 사용한다.

- 유닉스 상에서만 구동된다.

'''

'''
5장 19절 : 임시 파일과 디렉토리 만들기 : 임시 파일이나 디렉토리를 만들어 프로그램에 사용하고 그 뒤 삭제하는 경우 tempfile 모듈을 사용한다.

- 임시파일 : tempfile.TemporaryFile
    w+t : 텍스트 쓰기모드
    w+b : 바이트 쓰기모드
    모드 변경을 위해 파일을 닫으면 임시 파일은 제거된다. TemporaryFile()은 추가적으로 내장 함수 open()과 동일한 인자를 받는다.
'''


# 예2.
from tempfile import TemporaryFile
with TemporaryFile('w+t') as f:
    # 파일 읽기/쓰기
    f.write('Hello World\n')
    f.write('Testine\n')
    # 처음으로 이동해 데이터를 읽는다.
    f.seek(0)
    data = f.read()

ff = TemporaryFile('w+t')
#........
f.close() # 임시파일 삭제


'''

5장 20절 : 시리얼 포트와 통신 : 시리얼 포트를 통해 하드웨어 디바이스와 통신하고 싶은 경우 pySerial 패키지를 사용한다.


'''

# 예3.
import serial
ser = serial.Serial('/dev/tty.usbmoden641', baudrate=9600, bytesize=8, parity='N', stopbits=1)

#####################################################################################################################################################


'''

6장 1절 csv 데이터 읽고 쓰기 : CSV 파일로 인코딩 된 데이터를 읽거나 쓰고싶은 경우 csv 라이브러리를 사용한다.

- csv에 데이터를 쓰는 법 : csv 모듈을 사용해서 쓰기 객체를 생성(open 옵션에 'w'를 준다)하고 헤더와 열(데이터)를 따로 입력한다. 
                        데이터가 딕셔너리 시퀀스로 가지고 있다면 딕셔너리처럼 입력한다.
                        
- csv 데이터 인코딩을 다른 형식으로 바꾸는 방법 : csv.reader()에 delimiter 옵션을 준다. (예 - 탭 구분으로 읽고 싶으면 delimiter='\t' 를 붙여준다)
- csv 데이터 형식 변환 



'''

# 예4.
import csv
with open('aa.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:   # row는 튜플이 된다. 따라서 특정 필드에 접근하려면 인덱스를 사용해야 한다. 예 - row[0](Symbol), row[4](Change)
        a

# 예5.
# 인덱싱이 헷갈리는 경우를 방지하기 위헤 네임드튜플을 사용한다. 아래와 같이 네임드튜플을 사용하면 row.Symbol이나 row.Change와 같은 열 헤더를 사용할 수 있다.
from collections import namedtuple
with open('aa.csv') as f:
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for r in f_csv:
        row = Row(*r)

# 예6.
# 또다른 대안으로 딕셔너리 시퀀스를 사용할 수 있다. 딕셔너리 시퀀스는 각 행의 요소에 접근하기 위해 행 헤더를 사용한다. 예를 들어 row['Symbol'], row['Change'] 등과 같이 사용한다.
import csv
with open('aa.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        d

# 예7.
# 쓰기 객체로 데이터를 입력
headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [('AA', 39.48, '6/11/2007/', '9:36am', -0.18, 181800),
        ('AIG', 71.38, '6/11/2007/', '9:36am', -0.15, 195500),
        ('AXP', 62.58, '6/11/2007/', '9:36am', -0.46, 935000)]

with open('stocks.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)

# 딕셔너리 시퀀스의 경우 입력
headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [{'Symbol':'AA', 'Price':39.48, 'Date':'6/11/2007/', 'Time':'9:36am', 'Change':-0.18, 'Volume':181800},
        {'Symbol':'AIG', 'Price':71.38, 'Date':'6/11/2007/', 'Time':'9:36am', 'Change':-0.15, 'Volume':195500},
        {'Symbol':'AXP', 'Price':62.58, 'Date':'6/11/2007/', 'Time':'9:36am', 'Change':-0.46, 'Volume':935000}]

with open('stocks.csv', 'w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)


# 예8.
with open('stocks.csv') as f:
    f_tsv = csv.reader(f, delimiter='\t')


'''

6장 2절 JSON 데이터 읽고 쓰기 JSON(Java Script Object Notation)으로 인코딩된 데이터를 읽고나 쓰고 싶은 경우 json 모듈을 사용한다.


* json

- Java Script Object Notation 이라는 이름에서 알 수 있듯이 자바스크립트를 위한 것이고 객체 형식으로 자료를 표현하는 것이다.

 JSON 그자체 는 단순히 데이터 포맷일 뿐이다. 어떠한 통신 방법도, 프로그래밍 문법도 아닌 단순히 데이터를 표시하는 표현 방법일 뿐이다.
 간단한 데이터를 xml보다 좀 더 간단하게 표현하기 위해 만든 것이다. 
 XML보다 기능이 적기 때문에 파싱도 빠르고 간단하기 때문에 클라이언트 사이드에서, 특히 모바일에서 더욱 유용하다. 
 사실 서버 입장에서도 더 유용하기 때문에 많은 서비스들이 XML보다는 JSON을 권장한다.
 
 단순히 데이터를 받아서 객체나 변수로 할당해서 사용하기 위한 것이다.
 
 주고 받을 수 있는 자료형은 None, bool, int, float, str과 같은 기본 타입과 리스트, 튜플, 딕셔너리와 같은 컨테이너 타입을 지원한다.
 기본 데이터 배열은 KEY와 VALUE로 구성되어 있으며 중괄호로 감싼다.
 KEY값은 문자열이기 때문에 반드시 "KEYNAME" 이렇게 쌍따옴표를 붙여줘야 하고 VALUE에는 기본 자료형이나 배열, 객체를 넣으면 된다.
 
 파이썬과 상당히 동일한 구조를 가지며 파이썬에서 True, False, None이 JSON에서 true, false, null 이다.
 
 JSON의 기본표현 형태 예
 
 예1
 {
     "age": 29,
     "name": "HIKI",
     "family": {"father": "홍길동", "mother": "심청이"}
 }

 예2
 {
    "member": [
        {
            "id": "hyunc87",
            "blog": "tistory",
            "from": "korea",
            "memo": "HelloWorld"
        },
        {
            "id": "abcd",
            "blog": "tistory.com",
            "from": "korea",
            "memo": "HelloWorld2"
        }
    ]
}

 
- 일반적으로 JSON은 제공받은 데이터로부터 딕셔너리나 리스트를 생성한다. 다른 종류의 객체를 만들고 싶다면 json.loads()에 object_pairs_hook나 object_hook을 넣는다.


'''

# 예9.
import json
data = {
    'name' : 'ACME',
    'shares' : 100,
    'price' : 542.23
}

json_str = json.dumps(data)
data = json.loads(json_str)  # json 인코딩된 문자열을 파이썬 자료 구조로 돌리는 방법

with open('data.json', 'w') as f:   # json 데이터 쓰기
    json.dump(data, f)

with open('data.json', 'r') as f:   # json 데이터 읽기
    data = json.load(f)

# 예10.
json.dumps(False)
# 'false'
d = {'a': True,
     'b': 'Hello',
     'c': None}
json.dumps(d)
# '{"b": "Hello", "c": null, "a": true}'

# 예11.
s = '{"name": "ACME", "shares": 50, "price": 490.1}'
from collections import OrderedDict
data = json.loads(s, object_pairs_hook=OrderedDict)
data

# 예12.
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d   # json 딕셔너리를 파이썬 객체로 바꾼다.


'''

6장 3절 단순한 XML 데이터 파싱 : 단순한 XML 문서에서 데이터를 얻고 싶은 경우 xml.etree.ElementTree 모듈을 사용하면 된다.


'''

# 예13.
from urllib.request import urlopen
from xml.etree.ElementTree import parse
u = urlopen('http://planet.python.org/rss20.xml')   # RSS 피드를 다운로드하고 파싱
doc = parse(u)

for item in doc.iterfind('channel/item'):
    title = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')

'''

6장 4절 매우 큰 XML 파일 증분 파싱하기 : 매우 큰 XML 파일에서 최소의 메모리만 사용하여 데이터를 추출하고 싶은 경우 이터레이터와 제너레이터를 사용해서 사용자함수를 만든다.


'''

from xml.etree.ElementTree import iterparse

def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    next(doc)

    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass
