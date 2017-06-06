6월 6일
===============================================================================
#5.12 파일 이름 인코딩 우회
#시스템의 기본 인코딩을 ㅗ디코딩 혹은 인코딩되지 않은 파일 이름에 입출력 작업을 수행해야 한다.
#기본적으로 모든 파일 일므은 sys.getfilesystemencoding()이 반호나하는 텍스트 인코딩 값으로
#디코딩 혹은 인코딩되어 있다.
sys.getfilesystemencoding()

#Traceback (most recent call last):
 # File "<ipython-input-1-142462941ec7>", line 1, in <module>
  #  sys.getfilesystemencoding()
#NameError: name 'sys' is not defined


#하지만 이 인코딩을 우회하길 바란다면 로우 바이트 문자열로 파일 이름을 명시해야 한다.
EX1>
#유니코드로 파일 이름을 쓴다.
with open('jalape\xf1o.txt', 'w') as f:
    f.write('Spicy!')
#?????

#디렉토리 리스트 (디코딩됨)
import os
os.listdir('.')
#['.anaconda',
# '.astropy',
#...

#디렉토리 리스트(디코딩되지 않음)
os.listdir(b'.')    #바이트 문자열
#[b'.anaconda',
# b'.astropy',
#...

#로우 파일 이름으로 파일 열기
with open(b'jalapen\xcc\x83o.txt') as f:
    print(f.read())
#Traceback (most recent call last):
 # File "<ipython-input-5-d098c11bdaa7>", line 1, in <module>
 #   with open(b'jalapen\xcc\x83o.txt') as f:
#OSError: [Errno 22] Invalid argument: b'jalapen\xcc\x83o.txt'
===============================================================================
          
          

          
          
  
===============================================================================        
#5.15 망가진 파일 이름 출력
#프로그램에서 디렉토리 리스트를 받아 파일 일믕르 출력하려고 할 때., UnicodeEncodeError 예외와
#"surrogates not allowed" 메세지가 발생하면서 프로그램이 죽어 버린다.

#출처를 알 수 없는 파일 이름을 출력할 때, 다음 코드로 에러를 방지한다.
EX1>
def bad_filename(filename):
    return repr(filename)[1:-1]
try:
    print(filename)
except UnicodeEncodeError:
    print(bad_filename(filename))
    

#기본적으로 파이썬은 모든 파일 이름이 sys.getfilesystemencoding()이 반환하는 값으로
#인코딩되어 있다고 가정하자
#하지만 특정 파일 시스템은 인코딩 규칙을 따르도록 강제하지 ㅇ낳아서 올바르지 않은 인코딩을
#사용한 파일 이름이 생기기도 한다.


#os.listdir() 와 같은 명령을 실행할 때, 망가진 파일 이름ㅇ르 사용함녀 파이썬에 문제가 생긴다.
#이 이름을 올바른 텍스트 문자열로 변환할 수도 없다.
#파이썬의 해결책은 디코딩할 수 ㅇ벗는 바이트 값 \xhh를 Unicode 문자 \udchh로 표현하는
#"대리 인코딩"으로 매핑

#UTF-8이 아닌 Latin-1으로 인코딩한 디렉토리 리스트 예제
EX2>
import os
files = os.listdir('.')
files
#['.anaconda',
# '.astropy',



EX3>
#파일 이름을 다루거나 open()가 같은 함수에 전달하는 코드가 있다면 모두 정상적으로 동작한다.
#이 파일 이름을 출력하려고 할 때만 문제가 발생한다.
#특히 선행 리스트를 출력하려고 하면 프로글매이 비정상적으로 종료
for name in files:
    print(name)
#.anaconda
#.astropy
#????



#프로그램이 죽는 이유는 \udce4가 잘못된 Unicode 이기 때문에
#대리 짝으로 알려진 문자 두 개의 조합
#하지만 첫번째 반쪽이 없기 때문에 올바른 Unicode라 할 수 없다.
#따라서 올바른 출력을 하려면 망가진 파일 일믕르 발견했을 때 교정해야 한다.
#아래 수정 코드
EX4>
for name in files:
    try:
        print(name)
    except UnicodeEncodeError:
        print(bad_filename(name))
#.anaconda
#.astropy
#.condarc
===============================================================================    
    





===============================================================================
#5.16 이미 열려 있는 파일의 인코딩을 수정하거나 추가하기
#바이너리 모드로 이미 열려있는 파일 객체를 닫지 않고 Unicode 인코딩/디코딩을 추가하고 싶다면
#그 객체를 io.TextIOWrapper() 객체로 감싼다..
EX1>
import urllib.request
import io

u = urllib.request.urlopen('http://www.python.org')
f = io.TextIOWrapper(u,encoding='utf-8')
text = f.read()



EX1_1>
#덱스트 모드로 열이나 파일의 인코딩을 변경하려면 detach() 메소드로 텍스트 인코딩 레이어를 제거하고
#다른 것으로 치환한다,
#sys.stdout의 인코딩을 바꾸는 방법
import sys
sys.stdout.encoding
# 'UTF-8'

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
sys.stdout.encoding
############
Traceback (most recent call last):
  File "<ipython-input-7-1c9742653fd4>", line 1, in <module>
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
NameError: name 'io' is not defined
############



#I/O 시스템은 여러 레이어로 만들어져 있다.
EX2>
f=open('sample.txt','w')
f
#<_io.TextIOWrapper name='sample.txt' mode='w' encoding='cp949'>
f.butter
############
Traceback (most recent call last):

  File "<ipython-input-16-1d9e577f82e7>", line 1, in <module>
    f.butter

AttributeError: '_io.TextIOWrapper' object has no attribute 'butter'
############

f.butter.raw
############
Traceback (most recent call last):

  File "<ipython-input-18-1b0c972080e7>", line 1, in <module>
    f.butter.raw

AttributeError: '_io.TextIOWrapper' object has no attribute 'butter'
############



#io.TextIOWrapper는 Unicode를 인코딩/디코딩하는 텍스트 처리 레이어,
#io.BufferedWriter 는 바이너리 데이터를 처리하는 버퍼 I/O 레이어,
#io.FileIO는 운영체제에서 하위 레벨 파일 디스크립터를 표현하는 로우파일이다.
#텍스트 인코딩의 추가,수정에는 최상단 레이어인 io.TextIOWrapper의 추가,수정 포함
#일반적으로 앞에 나타난 속성에 접근해 레이어를 직접 수정하는 것은 안전하지 않다.
EX3>
f
#<_io.TextIOWrapper name='sample.txt' mode='w' encoding='cp949'>
f=io.TextIOWrapper(f.butter, encoding='latin-1')
f
############
Traceback (most recent call last):

  File "<ipython-input-21-42841e066548>", line 1, in <module>
    f=io.TextIOWrapper(f.butter, encoding='latin-1')

NameError: name 'io' is not defined
############
## f의 원본 값이 파괴되고 프로세스의 기저 파일을 닫았기 때문에 제대로 동작X



#detach() 메소드는 파일의 최상단 레이어를 끊고 그 다음 레이어를 반환
#그 상단 레이어를 더 이상 사용할 수 X
EX4>
f=open('sample.txt','w')
f
#<_io.TextIOWrapper name='sample.txt' mode='w' encoding='cp949'>

b=f.detach()
############
Traceback (most recent call last):

  File "<ipython-input-24-ce30ad9954af>", line 1, in <module>
    b=f.detach()

ValueError: underlying buffer has been detached
############

f.write('hello')
############
Traceback (most recent call last):

  File "<ipython-input-25-0ec9cf64e174>", line 1, in <module>
    f.write('hello')

ValueError: underlying buffer has been detached
############


EX4_1>
#하지만 연결을 끊은 후에는, 반호나된 결과에 새로운 상단 레이어 추가 가능
f=io.TextIOWrapper(b,encoding='latin-1')
f
#####
Traceback (most recent call last):

  File "<ipython-input-26-e251d64d2805>", line 1, in <module>
    f=io.TextIOWrapper(b,encoding='latin-1')

NameError: name 'io' is not defined
#####
===============================================================================





===============================================================================
#5.17 텍스트 파일에 바이트 쓰기
#텍스트 모드로 연 파일에 로우 바이트를 쓰고 싶을 때
#buffer()

EX1>
import sys
sys.stdout.write(b'Hello\n')
#Hello

sys.stdout.buffer.write(b'Hello\n')
############
Traceback (most recent call last):
  File "<ipython-input-9-635b121f7e0e>", line 1, in <module>
    sys.stdout.buffer.write(b'Hello\n')

AttributeError: 'OutStream' object has no attribute 'buffer'
############

#텍스트 파일의 buffer 속성에서 바이너리 데이터를 읽을 수도 있다,
===============================================================================






===============================================================================
#5.18 기존 파일 디스크립터를 파일 객체로 감싸기
#운영 체제 상에 이미 열려 있는 I/O 채널에 일치하는 정수형 파일 디스크립터를 가지로
#있고, 이를 상위 레벨 파이썬 파일 객체로 감싸고 싶다.

#파일 디스크립터는 운영 체제가 할당한 정수형 핸들로 시스템 I/O 채널 등을 참조하기 위한
#목적으로써 일반 파일과는 다르다.
#파일 디스크립터가 있을 때 open() 함수를 사용해 파이썬 파일 객체로 감쌀 수 있다.
#하지만 이때 파일 일므 대신 정수형 파일 디스크립터를 먼저 전달해야 한다.

EX1>
#하위 레벨 파일 디스크립터 열기
import os
fd = os.open('somefile.txt', os.O_WRONLY | os.O_CREAT)

#올바른 파일로 바꾸기
f = open(fd, 'wt')
f.write('hello world\n')
f.close()

#상위 레벨 파일 객체가 닫혔거나 파괴되었다면, 그 하단 파일 디스크립터 역시 닫힌다.
#이런 동작을 원하지 ㅇ낳는다면 closefd=False 인자를 open()에 전달해야 한다.

                                        
#파일 객체를 생성하지만, 사용이 끝났을 때 fd를 닫지 않는다.
f = open(fd, 'wt', closefd=False)
....



#Unix 시스템 상에서 이 기술을 사용하면 기존의 I/O 채녈을 감싸 파일과 같은 인터페이스로
#사용할 수 있다.
EX2>
from socket import socket, AF_INET, SOCK_STREAM

def echo_client(client_sock,addr):
    print('Got connection from',addr)
    
    #읽기/쓰기를 위해 소켓에 대한 텍스트 모드 파일 래퍼를 만든다.
    client_in=open(client_sock.fileno(),'rt',encoding='latin-1',closefd=False)
    client_out=open(client_sock.fileno(),'wt',encoding='latin-1',closefd=False)
    
    #파일 I/O를 사용해 클라이언트에 라인을 에코한다.
    for line in client_in:
        client_out.write(line)
        client_out.flush()
        client_sock.close()
        
def echo_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    while True:
        client, addr = sock.accept()
        echo_client(client, addr)
        
##위 예제는 내장 함수 open()의 기능을 보이기 위한 목적으로 작성
#Unix 기반 시스템에서만 동작
===============================================================================





===============================================================================
#5.19 임시 파일과 디렉토리 만들기
#임시 파일이나 디렉토리를 만들어 프로글매에 사용해야 한다.
#그 후에 파일이나 디렉토리 파기
#"tempfile 모듈"

EX1>
#이름 없는 임시 파일을 만들기 위해서 tempfile.TemporaryFile 사용
from tempfile import TemporaryFile
with TemporaryFile('w+t') as f:
    
    #파일에서 읽기/쓰기
    f.write('Hello World\n')
    f.write('Testing\n')
    
    #처음으로 이동해 데이터를 읽는다.
    f.seek(0)
    data = f.read()

#임시 파일은 파기

EX1_1>
f=TemporaryFile('w+t')
#임시 파일 사용
...
f.close()
#파일 파기



#TemporaryFile()에 전달하는 첫번째 인자는 파일 모드이고, 텍스트 모드에는 대개 w+t를,
#바이너리 모드에는 w+b를 사용한다.
#이 모드는 읽기와 쓰기를 동시에 지원하지 때문에, 모드 변경을 위해 파일을 닫으면 실제로 파기
#TemporaryFile()은 추가적으로 내장 함수 open()과 동일한 인자를 받는다.
EX2>
with TemporaryFile('w+t', encoding='utf-8', errors='ignore') as f:
    ...
    
#대개 Unix 시스템에서 TemporaryFile()로 생성한 파일에 이름이 없고 디렉토리 엔트리도
#갖지 않는다.
#이 제한을 없애고 싶으면 NamedTemporaryFile()을 사용하면 된다.
from tempfile improt NamedTemporaryFile

with NamedTemporaryFile('w+t') as f:
    print('filename is:', f.name)
    ...
    
    #파일이 자동으로 파기된다.
    
#f.name 속성에 임시 파일의 파일 이름이 담겨 있다. 다른 코드에 이 파일을 전달해야 할
#필요가 생겼을 때 이 속성 사용
#TemporaryFile()과 마찬가지로 생성된 파일의 사용이 끝났을 때 자동으로 삭제

#이런 동작을 원하지 ㅇ낳을 때는 "delete=False" 키워드 인자 사용
EX3>
with NamedTemporaryFile('w+t',delete=False) as f:
    print('filename is:', f.name)
    ...

#임시 디렉토리를 만들기 위해서는 tempfile.TemporaryDirectiory() tkdyd
from tempfile import TemporaryDirectory
with TemporaryDirectory() as dirname:
    print('dirname is:',dirname)
    #Use the directory
    ...
#디렉토리와 모든 내용물이 파기
===============================================================================






CHAPTER 6.
데이터 인코딩과 프로세싱
[파이썬을 사용해 CSV,JSON,XML,바이너리 레코드 등으로 표현된 데이터를 다루는 방법]
===============================================================================
#6.1 CSV 데이터 읽고 쓰기
#대부분의 CSV 데이터는 csv 라이브러리 사용

EX1>
#예, stocks.csv 파일에 담겨 있는 주식 시장 정보
Symbol,Price,Date,Time,Change,Volume
"AA",39.48,"6/11/2007","9:36am",-0.18,181800
"AIG",71.38,"6/11/2007","9:36am",-0.15,195500
"AXP",62.58,"6/11/2007","9:36am",-0.46,935000
"BA",98.31,"6/11/2007","9:36am",+0.12,104800
"C",53.08,"6/11/2007","9:36am",-0.25,360900
"CAT",78.29,"6/11/2007","9:36am",-0.23,225400

#데이터를 읽어 튜플 시퀀스에 넣기
import csv
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        #행 처리
        ...
        
#앞에 나온 코드에서 row는 튜플이 된다. 따라서 특정 필드에 접근하려면 row[0](Symbol),
#row[4](Change)와 같이 인덱스를 사용해야 한다.
#인덱스 사용이 때때로 헷갈리기 때문에 네임드 튜플
EX2>
from collections import namedtuple
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for r in f_csv:
        row = Row(*r)
        #행 처리
        ...

#row.Symbol 이나 row.Change 와 같이 열 헤더 사용 가능
#다만 열 헤더가 유효한 파이썬 식별자여야 한다.



EX3>
#또 다른 대안으로 데이터를 딕셔너리 시퀀스로 읽을 수도 있다.
import csv
with open('stocks.csv') as f:
    f_csv=csv.DictReader(f)
    for row in f_csv:
        #행 처리
        ...

## 이 버전의 경우, 각 행의 요소에 접근하기 위해서 행 헤더 사용
#예를 들어 row['Symbol'] 또는 row['Change']등과 같이 한다.
#CSV 데이터를 쓰려면, csv 모듈을 사용해서 쓰기 객체 생성
headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
        ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
        ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
        ]
with open('stocks.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)

#데이터를 딕셔너리 시퀀스로 가지고 있다면,
headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
            rows = [{'Symbol':'AA', 'Price':39.48, 'Date':'6/11/2007',
            'Time':'9:36am', 'Change':-0.18, 'Volume':181800},
            {'Symbol':'AIG', 'Price': 71.38, 'Date':'6/11/2007',
            'Time':'9:36am', 'Change':-0.15, 'Volume': 195500},
            {'Symbol':'AXP', 'Price': 62.58, 'Date':'6/11/2007',
            'Time':'9:36am', 'Change':-0.46, 'Volume': 935000},
            ]
with open('stocks.csv','w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)
    
    
    
    
    
    
#6.2 JSON 데이터 읽고 쓰기
#JSON = JavaScript Object Notation
#"json 모듈"
#json.dumps() / json.loads()
#pickle과 같은 직렬화 라이브러리에서 사용한 것과 인터페이스 동일

EX1>
#파이썬 데이터를 JSON으로 변환하는 코드
import json
data = {
        'name' : 'ACME',
        'shares' : 100,
        'price' : 542.23
        }
json_str = json.dumps(data)

#JSON 인코딩된 문자열을 파이썬 자료 구조로 돌리는 방법
data = json.loads(json_str)

#문자열이 아닌 파일로 작업한다면 json.dumps() 나 json.loads()를 사용해서
#JSON 데이터를 인코딩/디코딩한다.
EX2>
#JSON 데이터 쓰기
with open('data.json','w') as f:
    json.dump(data,f)
#데이터 다시 읽기
with open('data.json''r') as f:
    data=json.load(f)
    


#JSON 인코딩은 None,bool.int,float,str과 같은 기본 타입과 함께 리스트, 튜플, 딕셔너리와
#같은 컨테이너 타입을 지원한다.
#딕셔너리의 경우 키는 문자열로 가정한다,
#JSON 스펙을 따르기 위해서 파이선 리스트와 딕셔너리만 인코딩해야 한다.
#JSON 인코딩 포맷은 약간의 차이점을 제외하고는 파이썬 문법과 거의 동일
#예를 들어, True = true // False = false // None = null

EX3>
json.dumps(False)
#NameError: name 'json' is not defined
d = {'a': True,
    'b': 'Hello',
    'c': None}
json.dumps(d)
#NameError: name 'json' is not defined




#JSON에서 디코딩한 데이터를 조사해야 한다면, 단순히 출력해서 구조를 알아내기 쉽지 않다.
#특히 데이터에 중첩이 심하게 된 구조체가 포함되어 있거나 필가 많다면 더 어렵다.
#"pprint모듈의 pprint() 함수"
#키를 알파벳 순으로 나열하고 딕셔너리를 좀 더 보기 좋게 출력
EX4>
#트위터의 검색 결과를 더 예쁘게 출력하는 방법
from urllib.request import urlopen
import json
u = urlopen('http://search.twitter.com/search.json?q=python&rpp=5')
resp = json.loads(u.read().decode('utf-8'))
from pprint import pprint
pprint(resp)

############
Traceback (most recent call last):

  File "<ipython-input-29-2a5f6b4b7a3f>", line 3, in <module>
    u = urlopen('http://search.twitter.com/search.json?q=python&rpp=5')

  File "C:\Users\ATIV BOOK 9\Anaconda3\lib\urllib\request.py", line 223, in urlopen
    return opener.open(url, data, timeout)

  File "C:\Users\ATIV BOOK 9\Anaconda3\lib\urllib\request.py", line 532, in open
    response = meth(req, response)

  File "C:\Users\ATIV BOOK 9\Anaconda3\lib\urllib\request.py", line 642, in http_response
    'http', request, response, code, msg, hdrs)

  File "C:\Users\ATIV BOOK 9\Anaconda3\lib\urllib\request.py", line 570, in error
    return self._call_chain(*args)

  File "C:\Users\ATIV BOOK 9\Anaconda3\lib\urllib\request.py", line 504, in _call_chain
    result = func(*args)

  File "C:\Users\ATIV BOOK 9\Anaconda3\lib\urllib\request.py", line 650, in http_error_default
    raise HTTPError(req.full_url, code, msg, hdrs, fp)

HTTPError: Gone
############



#일반적을 JSON 디코딩은 제공 받은 데이터로부터 딕셔너리나 리스트를 생성
#다른 종류의 객체를 만ㄷㄹ고 싶다면 json.loads()에 object_pairs_hook나
#object_hook를 넣는다
#예를 들어, OrderedDict의 순서를 지키면서 JSON 데이터를 디코딩하려면,
EX5>
s = '{"name": "ACME", "shares": 50, "price": 490.1}'
from collections import OrderedDict
data = json.loads(s, object_pairs_hook=OrderedDict)
data
#OrderedDict([('name', 'ACME'), ('shares', 50), ('price', 490.1)])

#JSON 딕셔너리를 파이썬 객체로 바꾸는 예시
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

data = json.loads(s, object_hook=JSONObject)
data.name
#'ACME'

data.shares
#50

data.price
#490.1
===============================================================================





===============================================================================
#6.3 단순한 XML 데이터 파싱
#"xml.etree.ElementTree 모듈"

EX1>
#Planet Python에서 RSS 피드를 받아 파싱을 해야 한다면,
from urllib.request import urlopen
from xml.etree.ElementTree import parse

# RSS 피드를 다운로드하고 파싱한다,
u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(u)

# 관심 있는 태그를 봅아서 출력한다.
for item in doc.iterfind('channel/item'):
    title = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')
        
    print(title)
    print(date)
    print(link)
    print()

############
Enthought: Press Release: SciPy 2017 Conference to Showcase Leading Edge Developments in Scientific Computing with Python
Mon, 05 Jun 2017 18:18:12 +0000
http://blog.enthought.com/general/press-release-scipy-2017-conference-showcase-leading-edge-developments-scientific-computing-python/

Nikola: Nikola v7.8.7 is out!
Mon, 05 Jun 2017 15:07:46 +0000
https://getnikola.com/blog/nikola-v787-is-out.html

Jean-Paul Calderone: Twisted Web in 60 Seconds: HTTP/2
Mon, 05 Jun 2017 13:56:49 +0000
http://as.ynchrono.us/2016/12/twisted-web-in-60-seconds-http2.html

Caktus Consulting Group: Decorators, Unwrapped: How Do They Work? (PyCon 2017 Must-See Talk 1/6)
Mon, 05 Jun 2017 13:30:00 +0000
https://www.caktusgroup.com/blog/2017/06/05/decorators-unwrapped-how-do-they-work-pycon-2017-must-see-talk-16/

Doug Hellmann: zipfile — ZIP Archive Access — PyMOTW 3
Mon, 05 Jun 2017 13:00:37 +0000
http://feeds.doughellmann.com/~r/doughellmann/python/~3/rPWXwdaYl78/

Mike Driscoll: PyDev of the Week: Andrew Godwin
Mon, 05 Jun 2017 12:30:51 +0000
http://www.blog.pythonlibrary.org/2017/06/05/pydev-of-the-week-andrew-godwin/

Kushal Das: Python 101 session this Sunday
Mon, 05 Jun 2017 11:49:00 +0000
https://kushaldas.in/posts/python-101-session-this-sunday.html

Django Weekly: This week in Django - Issue No 41 - 1 June 2017
Mon, 05 Jun 2017 09:58:25 +0000
http://djangoweekly.com/blog/post/week-django-issue-no-41-1-june-2017

Armin Ronacher: Diversity in Technology and Open Source
Mon, 05 Jun 2017 00:00:00 +0000
http://lucumr.pocoo.org/2017/6/5/diversity-in-technology

Catalin George Festila: The SpeechRecognition python module - part 001.
Sun, 04 Jun 2017 09:32:17 +0000
http://python-catalin.blogspot.com/2017/06/the-speechrecognition-python-module.html

Catalin George Festila: The development with python-instagram .
Sun, 04 Jun 2017 08:42:13 +0000
http://python-catalin.blogspot.com/2017/06/the-development-with-python-instagram.html

François Dion: Readings in Technology
Sat, 03 Jun 2017 22:08:31 +0000
http://raspberry-python.blogspot.com/2017/06/readings-in-technology.html

Weekly Python StackOverflow Report: (lxxvi) stackoverflow python report
Sat, 03 Jun 2017 20:34:00 +0000
http://python-weekly.blogspot.com/2017/06/lxxvi-stackoverflow-python-report.html

qutebrowser development blog: Getting started again
Sat, 03 Jun 2017 19:32:12 +0000
https://blog.qutebrowser.org/getting-started-again.html

Davy Wybiral: Rainbow-powered Raspberry Pi
Sat, 03 Jun 2017 10:58:59 +0000
http://davywybiral.blogspot.com/2017/06/rainbow-powered-raspberry-pi.html

BangPypers: How BangPypers meetup is run
Sat, 03 Jun 2017 08:18:00 +0000
http://bangalore.python.org.in/blog/2017/06/03/how-bangpypers-is-run/

Programming Ideas With Jake: Another Look at Instance-Level Properties in Python
Sat, 03 Jun 2017 05:00:23 +0000


Sandipan Dey: Some NLP: Probabilistic Context Free Grammar (PCFG) and CKY Parsing in Python
Sat, 03 Jun 2017 00:39:44 +0000


François Dion: Raspberry Pi 3 Canakit
Fri, 02 Jun 2017 21:03:56 +0000
http://raspberry-python.blogspot.com/2017/06/raspberry-pi-3-canakit.html

Python Data: Visualizing data  – overlaying charts in python
Fri, 02 Jun 2017 19:54:02 +0000
http://pythondata.com/visualizing-data-overlaying-charts/

Frank Wierzbicki: Jython 2.7.1 release candidate 2 released!
Fri, 02 Jun 2017 19:45:02 +0000
http://fwierzbicki.blogspot.com/2017/06/jython-271-rc2-released.html

PyBites: Flask Sessions
Fri, 02 Jun 2017 13:44:39 +0000
http://pybit.es/flask-sessions.html

Import Python: ImportPython Issue 127 - Python Functions aren't what you think, API checklist and more
Fri, 02 Jun 2017 10:15:03 +0000
http://importpython.com/blog/post/importpython-issue-127-python-functions-arent-what-you-think-api-checklist-and-more

Python Bytes: #28 The meaning of _ in Python
Fri, 02 Jun 2017 08:00:00 +0000
https://pythonbytes.fm/episodes/show/28/the-meaning-of-in-python

Kushal Das: My lightning talk in Django Girls PyCon
Fri, 02 Jun 2017 05:53:00 +0000
https://kushaldas.in/posts/my-lightning-talk-in-django-girls-pycon.html
############
===============================================================================





===============================================================================
#6.4 매우 큰 XML 파일 증분 파싱하기
# 매우 큰 XML 파일에서 최소의 메소리만 사용하여 데이터 추출하기
#증분 데이터 처리 : 이터레이터와 제너레이터
EX1>
#아주 큰 XML 파일을 증분적으로 처리하며 메모리 사용은 최소로 하는 함
from xml.etree.ElementTree import iterparse
def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    #뿌리 요소 건너뛰기
    next(doc)

    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass
===============================================================================