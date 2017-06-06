import os


#5.14
#Q 코딩되지 않은 파일 이름에 입출력 작업을 수행해야한다.


#A. 기본적으로 모든 파일 이름은 sys.getfilesystemencoding()이 반환하는 텍스트 인코딩 값으로 디코딩 혹은 인코딩 되어 있다.

sys.getfilesystemencoding()
#'utf-8'


#인코딩 우회법 raw바이트 문자열로 파일 이름을 명시 해야함

#유니코드로 파일 이름을 쓴다
with open('jalape\xf1o.txt', 'w') as f:
    f.write('Spicy!')
#6
#디렉터리 리스트 (디코딩 되지않음)

os.listdir('.')
#['jalapeño.txt']

#디렉터리 리스트 (디코딩되지 않음)
os.listdir(b'.') # Note: byte string
#[b'jalapen\xcc\x83o.txt']

#로우 파일 이름으로 파일 열기
with open(b'jalapen\xcc\x83o.txt') as f:
    print(f.read())
#Spicy!

#마지막 두 작업에 나온 것처럼, open()이나 os.listdir() 과 같은 파일관련 함수에 바이트 문자열을 넣었을 때
#파일 이름 처리는 거의 변하지 않는다.


#5.15
#프로그램에서 디렉터리 리스트를 받아 파일 이름을 출력하려고 할때, unocodeEncodeError예외와
#surrogates not allowed 메세지가 발생하면서 프로그램이 죽어버린다


#출처를 알 수 없는 파일 이름을 출력할때, 다음 코드로 에러를 방지한다.

def bad_filename(filename):
    return repr(filename)[1:-1]

try:
    print(filename)
except UnicodeEncodeError:
    print(bad_filename(filename))


import os
files = os.listdir('.')
files
#['spam.py', 'b\udce4d.txt', 'foo.txt']

#파일 이름을 다루거나 open()과 같은 함수에 전달하는 코드가 있다면 모두 정상적으로 동작한다.


for name in files:
    print(name)
spam.py
#Traceback (most recent call last):
#    File "<stdin>", line 2, in <module>
#UnicodeEncodeError: 'utf-8' codec can't encode character '\udce4' in
#position 1: surrogates not allowed


#프로그램이 실행 안되는 이유는 /udce4 가 잘못된 유니코드 이기 때문

#교정작업을 하기위한 코드

for name in files:
try:
    print(name)
except UnicodeEncodeError:
    print(bad_filename(name))

spam.py
b\udce4d.txt
foo.txt


#bad_filename() 함수를 어떻게 처리할지는 모두 프로그래머에게 달려있다. 혹은 그 값을 다음과 같이 재인코딩 가능

def bad_filename(filename):
    temp = filename.encode(sys.getfilesystemencoding(), errors='surrogateescape')
    return temp.decode('latin-1')

#위코드 출력시
for name in files:
    try:
        print(name)
    except UnicodeEncodeError:
        print(bad_filename(name))
spam.py
bäd.txt
foo.txt


#5.16 이미 열려있는 파일의 인코딩을 수정하거나 추가하기
#이미 열려있는 파일을 unicode 인코딩을 추가하거나 변경하고 싶을때

#바이너리 모드로 이미 열려있는 파일 객체를 닫지 않고 Unocode 인코딩/디코딩을 추가하고 싶다면 그 객체를 io.TextIOWrapper() 객체로 감싼다.

import urllib.request
import io

u = urllib.request.urlopen('http://www.python.org')
f = io.TextIOWrapper(u, encoding='utf-8')
text = f.read()

#텍스트 모드로 열린 파일의 인코딩을 변경시
#detcah() 메소드로 텍스트 인코딩 레이어를 제거하고 다른것으로 치환한다. sys.stdout의 인코딩을 바꾸는 방법

import sys
sys.stdout.encoding
#'UTF-8'
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
sys.stdout.encoding
#'latin-1'

#I/O시스템은 여러 레이어로 만들어져 있다.

f = open('sample.txt','w')
print(f)
#<_io.TextIOWrapper name='sample.txt' mode='w' encoding='UTF-8'>
print(f.buffer)
#<_io.BufferedWriter name='sample.txt'>
print(f.buffer.raw)
#<_io.FileIO name='sample.txt' mode='wb'>



print(f)
#<_io.TextIOWrapper name='sample.txt' mode='w' encoding='UTF-8'>
f = io.TextIOWrapper(f.buffer, encoding='latin-1')
print(f)
#<_io.TextIOWrapper name='sample.txt' encoding='latin-1'>
print(f.write('Hello'))
#Traceback (most recent call last):
#    File "<stdin>", line 1, in <module>
#ValueError: I/O operation on closed file.

#f의 원본값이 파괴되고 프로세스를 종료했기 때문에 제대로 동작하지 않는다.
#detach() 메소드는 파일의 최상단 레이어를 끊고 그 다음 레이어를 반환한다.
#그 다음에 상단 레이어를 더 이상 사용할 수 없다.

f = open('sample.txt', 'w')
print(f)
#<_io.TextIOWrapper name='sample.txt' mode='w' encoding='UTF-8'>
b = f.detach()
print(b)
#<_io.BufferedWriter name='sample.txt'>
print(f.write('hello'))
#Traceback (most recent call last):
#    File "<stdin>", line 1, in <module>
#ValueError: underlying buffer has been detached

#하지만 연결을 끊은 후에는, 반환된 결과에 새로운 상단 레이어를 추가할 수 있다.

f = io.TextIOWrapper(b, encoding='latin-1')
print(f)
#<_io.TextIOWrapper name='sample.txt' encoding='latin-1'>

#인코딩을 변경하는 방법을 보였지만, 이 기술을 라인 처리, 에러 규칙 등 파일 처리의 다른 측면에 활요할 수 있다.

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='ascii', errors='xmlcharrefreplace')
print('Jalape\u00f1o')
#Jalape&#241;o


#5.17 텍스트 파일에 바이트 쓰기
#텍스트 모드로 연 파일에 로우 바이트를 쓰고 싶다.

#해결 방법 . 단순히 바이트 데이터를 buffer에 쓴다.

import sys
sys.stdout.write(b'Hello\n')
#Traceback (most recent call last):
#    File "<stdin>", line 1, in <module>
#TypeError: must be str, not bytes
sys.stdout.buffer.write(b'Hello\n')
#Hello
#5

#이와 유사하게, 텍스트 파일의 buffer 속성에서 바이너리 데이터를 읽을 수도 있다.


#5.18
#운영 차제 상에 이미 열려있는 I/O 채널에 일치하는 정수형 파일 디스크립터를 가지고 있고 ,
#이를 상위 레벨 파이썬 파일 객체로 감싸고 싶을때

#이를 해결하기 위해선 파일이름 대신 정수형 파일 디스크립터를 먼저 전달해야한다


#하위레벨 파일 디스크립터 열기
import os
fd = os.open('somefile.txt', os.O_WRONLY | os.O_CREAT)

#올바른 파일로 바꾸기
f = open(fd, 'wt')
f.write('hello world\n')
f.close()


#하위 레벨 파일 객체가 닫혔거나 파괴 되었다면 , 그 하단 파일 디스크립터 역시 닫힌다
#이런 동작을 원하지 않는다면 closefd=False 인자를 open()에 전달해야 한다


#파일 객체를 생성하지만, 사용이 끝났을 때 fd를 닫지 않는다
f = open(fd, 'wt', closefd=False)


#D
#유닉스 시스템 상에서 이 코드를 사용시 I/O채널을 감싸 파일과 같은 인터페이스로 사용할 수 있는 쉬운 길이 열린다.

from socket import socket, AF_INET, SOCK_STREAM

def echo_client(client_sock, addr):
    print('Got connection from', addr)

    #읽기/쓰기를 위해 소켓에 대한 텍스트 모드 파일 래퍼를 만든다
    client_in = open(client_sock.fileno(), 'rt', encoding='latin-1',
                closefd=False)

    client_out = open(client_sock.fileno(), 'wt', encoding='latin-1',
                closefd=False)

    ##파일 I/O 를 사용해 클라이언트에 라인을 에코한다
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

#open 내장함수 unix기반에서만 작동 (이식성을 생각않는다면 성능은 이쪽이 뛰어남)
#크로스 플랫폼 코드가 필요하다면 소켓의 makefile()메소드를 사용해야 한다.


import sys
#stdout 에 대한 바이너리 모드 파일 만들기
bstdout = open(sys.stdout.fileno(), 'wb', closefd=False)
bstdout.write(b'Hello World\n')
bstdout.flush()



#5.19 임시 파일과 디렉터리 만들기
#임시 파일이나 디렉터리를 만들어 프로그램에 사용해야 한다. 그 후에 파일이나 디렉터리는 파기.

#tempfile 모듈에 이런 목적의 함수가 많이 있다.
#이름 없는 임시 파일을 만들기 위해서 tempfile.TemporaryFile 을 사용한다

from tempfile import TemporaryFile

with TemporaryFile('w+t') as f:
    #파일에서 읽기/ 쓰기
    f.write('Hello World\n')
    f.write('Testing\n')

    #처음으로 이동해 데이터를 읽는다.
    f.seek(0)
    data = f.read()

#임시 파일은 파기된다.


'''
TemporaryFile() 에 전달하는 첫 번째 인자는 파일 모드이고, 텍스트 모드에는 대개 w+t를
바이너리 모드에는 w+b를 사용한다.
이 모드는 읽기와 쓰기를 동시에 지원하기 때문에, 모드 변경을 위해 파일을 닫으면 실제로 파기하므로 유용하다.
TemporaryFile()은 추가적으로 내장 함수 open()과 동일한 인자를 받는다.
'''

with TemporaryFile('w+t', encoding='utf-8', errors='ignore') as f:

'''
대개 unix 시스템에서 TemporaryFile()로 생성한 파일에 이름이 없고 디렉터리 엔트리도 갖지 않는다.
이 제한을 없애고 싶으면 NamedTemporaryFile()을 사용하면 된다.
'''

from tempfile import NamedTemporaryFile

with NamedTemporaryFile('w+t') as f:
    print('filename is:', f.name)


#파일이 자동으로 파기됨.

#f.name 에 속성 임시 파일의 파일 이름이 담겨있다. 다른코드에 이파일을 전달해야 할 필요가 생겼을때 이 속성을 유용하게 사용할 수 있다.

with NamedTemporaryFile('w+t', delete=False) as f:
    print('filename is:', f.name)

#임시 디렉터리를 만들기 위해서는 tempfile.TemporaryDirectory()를 사용한다

from tempfile import TemporaryDirectory

with TemporaryDirectory() as dirname:
    print('dirname is:', dirname)
    # Use the directory

#모든 디렉터리와 내용물 파기

'''
토론

임시 파일과 디렉터리를 만들때 TemporaryFile(), NamedTemporaryFile(), TemporaryDirectory() 함수가 가장 쉬운 방법이다.
더 하위레벨로 내려갈시 mkstemp()와 mkdtemp()로 임시 파일과 디렉터리를 만들 수있다.

import tempfile
tempfile.mkstemp()
(3, '/var/folders/7W/7WZl5sfZEF0pljrEB1UMWE+++TI/-Tmp-/tmp7fefhv')
tempfile.mkdtemp()
'/var/folders/7W/7WZl5sfZEF0pljrEB1UMWE+++TI/-Tmp-/tmp5wvcv6'

일반적으로 임시파일은 /var/tmp와 같은 시스템의 기본 위치에 생성된다. 실제 위치를 찾으려면 tempfile.gettempdir()함수를 사용한다.

tempfile.gettempdir()
'/var/folders/7W/7WZl5sfZEF0pljrEB1UMWE+++TI/-Tmp-'

모든 임시 파일 관련 함수는 디렉터리와 이름 규칙을 오버라이드 할 수 있도록한다.
f = NamedTemporaryFile(prefix='mytemp', suffix='.txt', dir='/tmp')
print(f.name)
#'/tmp/mytemp8ee899.txt'

tempfile()은 가장 안전한 방식으로 파일을 생성한다는 점을 기억하자.
예를 들어 파일에 접근할 수 있는 권한은 현재 사용자에게만 주고, 파일 생성에서 레이스 컨디션이 발생하지 않도록 한다.




'''


#6장 데이터 인코딩과 프로세싱

'''
csv 파일로 인코딩된 데이터를 읽거나 쓰고 싶을때

대부분의 csv 데이터는 csv 라이브러리를 사용한다.

Symbol,Price,Date,Time,Change,Volume
"AA",39.48,"6/11/2007","9:36am",-0.18,181800
"AIG",71.38,"6/11/2007","9:36am",-0.15,195500
"AXP",62.58,"6/11/2007","9:36am",-0.46,935000
"BA",98.31,"6/11/2007","9:36am",+0.12,104800
"C",53.08,"6/11/2007","9:36am",-0.25,360900
"CAT",78.29,"6/11/2007","9:36am",-0.23,225400


다음 코드로 데이터를 읽어 튜플 시퀀스에 넣을 수 있다

import csv
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
    #행처리

앞에 나온 코드에서 row는 튜플이 된다. 따라서 특정 필드에 접근하려면 row[0](Symbol),row[4](change)와 같이 인덱스를 사용해야한다.

from collections import namedtuple
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for r in f_csv:
        row = Row(*r)
        #행처리
    
이렇게 하면 row.Symbol 이나 row.Change 와 같이 열 헤더를 사용할 수 있다.

import csv
with open('stocks.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
    #행처리


headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
         ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
         ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
       ]

with open('stocks.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
    

데이터를 딕셔너리 시퀀스로 가지고 있다면 다음과 같이 한다.

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
    


csv데이터를  수동으로 다루는 프로그램을 작성하기 보다는 csv 모듈을 사용하는 것이 훨씬 나은 선택이다


with open('stocks.csv') as f:
for line in f:
    row = line.split(',')
    #행처리

이 코드를 사용하면 할일이 많아짐.


#탭으로 구분한 값 읽기 예제
with open('stock.tsv') as f:
    f_tsv = csv.reader(f, delimiter='\t')
    for row in f_tsv:


위의 방법을 권장함
csv 데이터를 읽고 네임드 튜플로 변환한다면 열 헤더를 검증할 때 주의해야 한다. 예를 들어 csv 파일에 다음과 같이 유효하지 않은 식별 문자가 들어 있을 수 있다.

Street Address,Num-Premises,Latitude,Longitude 5412 N CLARK,10,41.980262,-87.668452

실제로 나온 데이터를 namedtuple을 만들때 벨류러 발생
정규식을 이용 유효하지 않은 문자를 치환한다

import re
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headers = [ re.sub('[^a-zA-Z_]', '_', h) for h in next(f_csv) ]
    Row = namedtuple('Row', headers)
    for r in f_csv:
        row = Row(*r)
        

또한 csv 는 데이터를 해석하려 하거나 문자열이 아닌 형식으로 변환하려 하지 않는다는 점이 중요하다.

col_types = [str, float, str, str, float, int]
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        #행 아이템에 변환 적용
        row = tuple(convert(value) for convert, value in zip(col_types, row))

딕셔너리에서 선택한 필드만 변환하는 예제

print('Reading as dicts with type conversion')
field_types = [ ('Price', float),
                ('Change', float),
                ('Volume', int) ]

with open('stocks.csv') as f:
    for row in csv.DictReader(f):
        row.update((key, conversion(row[key]))
                for key, conversion in field_types)
        print(row)
    
pandas 추천
'''

#6.2 JSON 데이터 읽고 쓰기
if __name__ == '__main__':
    if __name__ == '__main__':
        if __name__ == '__main__':
            if __name__ == '__main__':
                if '''
                JSON (javascript object notation)으로 인코딩된 데이터를 읽거나 쓰고 싶다.
                
                json 모듈을 이용  (json.dupms(), json.loads()이고 
                pickle 과 같은 직렬화 라이브러리에 사용한 것과 인터페이스는 동일하다.
                
                import json
                
                data = {
                    'name' : 'ACME',
                    'shares' : 100,
                    'price' : 542.23
                }
                
                json_str = json.dumps(data)
                
                
                다음은 json 인코딩된 문자열을 파이썬 자료 구조로 돌리는 방법
                
                data = json.loads(json_str)
                
                
                문자열이 아닌 파일로 작업한다면 json.dump()와 json.load()를 사용해서 JSON 데이터를 인코딩/디코딩한다
                
                #JSON 데이터 쓰기
                with open('data.json', 'w') as f:
                    json.dump(data, f)
                
                #데이터 다시 읽기
                with open('data.json', 'r') as f:
                    data = json.load(f)
                
                
                
                Json 인코딩은 None,bool, int,float,str과 같은 기본 타입과 함께 리스트 , 튜플, 딕셔너리와 같은 컨테이너 타입을 지원한다.
                딕셔너리의 경우 키는 문자열로 가정한다 - 문자열이 아닌 키는 인코딩 과정에서 문자열로 변환된다.
                JSON 스펙을 따르기 위해서 파이썬 리스트와 딕셔너리만 인코딩해야한다.
                
                json.dumps(False)
                'false'
                d = {'a': True,
                    'b': 'Hello',
                    'c': None}
                json.dumps(d)
                '{"b": "Hello", "c": null, "a": true}'
                
                False -> false ,True -> true , None -> null
                
                json 에서 디코딩한 데이터를 조사해야 한다면 단순히 출력해서 구조를 알아내기어렵고
                
                pprint() 모듈의 pprint()함수를 사용해보자 
                
                
                 from urllib.request import urlopen
                import json
                u = urlopen('http://search.twitter.com/search.json?q=python&rpp=5')
                resp = json.loads(u.read().decode('utf-8'))
                from pprint import pprint
                pprint(resp)
                {'completed_in': 0.074,
                'max_id': 264043230692245504,
                'max_id_str': '264043230692245504',
                'next_page': '?page=2&max_id=264043230692245504&q=python&rpp=5',
                'page': 1,
                'query': 'python',
                'refresh_url': '?since_id=264043230692245504&q=python',
                'results': [{'created_at': 'Thu, 01 Nov 2012 16:36:26 +0000',
                            'from_user': ...
                            },
                            {'created_at': 'Thu, 01 Nov 2012 16:36:14 +0000',
                            'from_user': ...
                            },
                            {'created_at': 'Thu, 01 Nov 2012 16:36:13 +0000',
                            'from_user': ...
                            },
                            {'created_at': 'Thu, 01 Nov 2012 16:36:07 +0000',
                            'from_user': ...
                            }
                            {'created_at': 'Thu, 01 Nov 2012 16:36:04 +0000',
                            'from_user': ...
                            }],
                'results_per_page': 5,
                'since_id': 0,
                'since_id_str': '0'}
                
                일반적으로 json 디코딩은 제공받은 데이터로부터 딕셔너리나 리스트를 생성한다
                다른 종류의 객체를 만들고 싶다면 json.loads() object_pairs_hook 나 object_hook을 넣는다
                
                s = '{"name": "ACME", "shares": 50, "price": 490.1}'
                from collections import OrderedDict
                data = json.loads(s, object_pairs_hook=OrderedDict)
                data
                OrderedDict([('name', 'ACME'), ('shares', 50), ('price', 490.1)])
                
                다음은 json 딕셔너리를 파이썬 객체로 바꾸는 예시이다
                
                
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
            
        마지막 에서 json 데이터를 디코딩하여 생성한 딕셔너리를 __init__()에 인자로 전달했다 여기서부턴 객체의 딕셔너리 인스턴스인것처럼 자유롭게 사용해도 괜찮다
        json 인코딩 옵션 (출력을 더 보기 이쁘게 하려면 json.dupms() 에 indent 인자를 사용한다.
        
        print(json.dumps(data))
        {"price": 542.23, "name": "ACME", "shares": 100}
        print(json.dumps(data, indent=4))
        {
            "price": 542.23,
            "name": "ACME",
            "shares": 100
        }
        
        
        출력에서 키를 정렬하고 싶다면 sort_keys 인자를 사용한다
        
        
        print(json.dumps(data, sort_keys=True))
        {"price": 542.23, "name": "ACME", "shares": 100}
        
        
        
        인스턴스는 일반적으로 json 으로 직렬화 하지 않는다
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        p = Point(2, 3)
        json.dumps(p)
        #Traceback (most recent call last):
        #    File "<stdin>", line 1, in <module>
        #    File "/usr/local/lib/python3.3/json/__init__.py", line 226, in dumps
        #        return _default_encoder.encode(obj)
        #    File "/usr/local/lib/python3.3/json/encoder.py", line 187, in encode
        #        chunks = self.iterencode(o, _one_shot=True)
        #    File "/usr/local/lib/python3.3/json/encoder.py", line 245, in iterencode
        #        return _iterencode(o, 0)
        #    File "/usr/local/lib/python3.3/json/encoder.py", line 169, in default
        #        raise TypeError(repr(o) + " is not JSON serializable")
        #TypeError: <__main__.Point object at 0x1006f2650> is not JSON serializable
        
        
    인스턴스를 직렬화하고 싶다면 인스턴스를 입력으로 받아 직렬화 가능한 딕셔너리를 반환하는 함수를 제공해야 한다
    
    def serialize_instance(obj):
        d = { '__classname__' : type(obj).__name__ }
        d.update(vars(obj))
        return d
    
    인스턴스를 돌려받기위한 코드
    
    #알려지지 않은 클래스에 이름을 매핑하는 딕셔너리
    classes = {
        'Point' : Point
    }
    
    def unserialize_object(d):
        clsname = d.pop('__classname__', None)
        if clsname:
            cls = classes[clsname]
            obj = cls.__new__(cls) # Make instance without calling __init__
            for key, value in d.items():
                setattr(obj, key, value)
            return obj
        else:
            return d
    
앞에 나온 함수는 다음과 같이 사용한다

p = Point(2,3)
s = json.dumps(p, default=serialize_instance)
s
#'{"__classname__": "Point", "y": 3, "x": 2}'
a = json.loads(s, object_hook=unserialize_object)
a
<__main__.Point object at 0x1017577d0>
a.x
#2
a.y
#3

'''

#6.3 단순한 XML데이터 파싱
#XML 문서에더 데이터를 얻기 위해
#xml.etree.ElementTree모듈을 사용하면 된다


from urllib.request import urlopen
from xml.etree.ElementTree import parse

#RSS 피드를 다운로드하고 파싱한다.
u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(u)

#관심있는 태그를 뽑아서 출력한다
for item in doc.iterfind('channel/item'):
    title = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')

    print(title)
    print(date)
    print(link)
    print()


'''
많은 app이 XML로 인코딩된 데이터를 다룬다

<?xml version="1.0"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <channel>
        <title>Planet Python</title>
        <link>http://planet.python.org/</link>
        <language>en</language>
        <description>Planet Python - http://planet.python.org/</description>
        <item>
            <title>Steve Holden: Python for Data Analysis</title>
            <guid>http://holdenweb.blogspot.com/...-data-analysis.html</guid>
            <link>http://holdenweb.blogspot.com/...-data-analysis.html</link>
            <description>...</description>
            <pubDate>Mon, 19 Nov 2012 02:13:51 +0000</pubDate>
        </item>
        <item>
            <title>Vasudev Ram: The Python Data model (for v2 and v3)</title>
            <guid>http://jugad2.blogspot.com/...-data-model.html</guid>
            <link>http://jugad2.blogspot.com/...-data-model.html</link>
            <description>...</description>
            <pubDate>Sun, 18 Nov 2012 22:06:47 +0000</pubDate>
        </item>
        <item>
            <title>Python Diary: Been playing around with Object Databases</title>
            <guid>http://www.pythondiary.com/...-object-databases.html</guid>
            <link>http://www.pythondiary.com/...-object-databases.html</link>
            <description>...</description>
            <pubDate>Sun, 18 Nov 2012 20:40:29 +0000</pubDate>
        </item>
        ...
    </channel>
</rss>

xml.etree.ElementTree.parse() 함수가 XML문서를 파싱하고 문서 객체로 만든다.
특정 XML 요소를 찾기 위해 find(), iterfind(), findtext() 와 같은 함수를 사용한다 

doc.iterfind('channel/item') 호출은 channel 요소의 item 요소를 찾는다.

doc
#<xml.etree.ElementTree.ElementTree object at 0x101339510>
e = doc.find('channel/title')
e
#<Element 'title' at 0x10135b310>
e.tag
#'title'
e.text
#'Planet Python'
e.get('some_attribute')

좀더 고급 app엔 lxml 사용을 고려
import 구문만 from lxml.etree import parse로 바꾸면 된다.




'''


#6.4 매우 큰 XML 파일 증분 파싱하기

#최소의 메모리만 사용해서 데이터를 추출하고 싶을때

'''
from xml.etree.ElementTree import iterparse

def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    # 뿌리 요소 건너뛰기
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




<response>
    <row>
        <row ...>
            <creation_date>2012-11-18T00:00:00</creation_date>
            <status>Completed</status>
            <completion_date>2012-11-18T00:00:00</completion_date>
            <service_request_number>12-01906549</service_request_number>
            <type_of_service_request>Pot Hole in Street</type_of_service_request>
            <current_activity>Final Outcome</current_activity>
            <most_recent_action>CDOT Street Cut ... Outcome</most_recent_action>
            <street_address>4714 S TALMAN AVE</street_address>
            <zip>60632</zip>
            <x_coordinate>1159494.68618856</x_coordinate>
            <y_coordinate>1873313.83503384</y_coordinate>
            <ward>14</ward>
            <police_district>9</police_district>
            <community_area>58</community_area>
            <latitude>41.808090232127896</latitude>
            <longitude>-87.69053684711305</longitude>
            <location latitude="41.808090232127896"
            longitude="-87.69053684711305" />
        </row>
        <row ...>
            <creation_date>2012-11-18T00:00:00</creation_date>
            <status>Completed</status>
            <completion_date>2012-11-18T00:00:00</completion_date>
            <service_request_number>12-01906695</service_request_number>
            <type_of_service_request>Pot Hole in Street</type_of_service_request>
            <current_activity>Final Outcome</current_activity>
            <most_recent_action>CDOT Street Cut ... Outcome</most_recent_action>
            <street_address>3510 W NORTH AVE</street_address>
            <zip>60647</zip>
            <x_coordinate>1152732.14127696</x_coordinate>
            <y_coordinate>1910409.38979075</y_coordinate>
            <ward>26</ward>
            <police_district>14</police_district>
            <community_area>23</community_area>
            <latitude>41.91002084292946</latitude>
            <longitude>-87.71435952353961</longitude>
            <location latitude="41.91002084292946"
            longitude="-87.71435952353961" />
        </row>
    </row>
</response>




from xml.etree.ElementTree import parse
from collections import Counter

potholes_by_zip = Counter()

doc = parse('potholes.xml')
for pothole in doc.iterfind('row/row'):
    potholes_by_zip[pothole.findtext('zip')] += 1
for zipcode, num in potholes_by_zip.most_common():
    print(zipcode, num)

#위코드는 파일 전체를 읽어 메모리가 너무 많이 필요함


from collections import Counter

potholes_by_zip = Counter()

data = parse_and_remove('potholes.xml', 'row/row')
for pothole in data:
    potholes_by_zip[pothole.findtext('zip')] += 1
for zipcode, num in potholes_by_zip.most_common():
    print(zipcode, num)


ElementTree ...?


'''