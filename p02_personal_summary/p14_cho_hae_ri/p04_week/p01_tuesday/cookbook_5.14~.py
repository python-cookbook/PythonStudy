



########## 5. 14. 파일 이름 인코딩 우회 ##########

# 문제
# 시스템의 기본 인코딩으로 디코딩 혹은 인코딩되지 않은 파일 이름에 입출력 작업을 수행해야 한다.

# 해결
# 기본적으로 모든 파일 이름은 sys.getfilesystemencoding() 이 반환하는 텍스트 인코딩 값으로 디코딩 혹은 인코딩 되어 있다.

import sys
sys.getfilesystemencoding()
#'utf-8'

# 하지만 이 인코딩을 우회하길 바란다면 row 바이트 문자열로 파일 이름을 명시해야 한다.

# 유니코드로 파일 이름을 쓴다.
with open('jalape\xf1o.txt', 'w') as f:
    f.write('Spicy!')

# 디렉토리 리스트(디코딩됨)
import os
os.listdir('.')
#['jalapeño.txt']

# 디렉토리 리스트(디코딩되지 않음)
os.listdir(b'.') # 바이트 문자열
#[b'jalape\xc3\xb1o.txt']

# 로우 파일 이름으로 파일 열기
with open(b'jalapen\xcc\x83o.txt') as f:
    print(f.read())
#Spicy!





########## 5. 15. 망가진 파일 이름 출력 ##########

# 문제
# 프로그램에서 디렉토리 리스트를 받아 파일 이름을 출력하려고 할 때 UnicodeEncodeError 예외와 "surrorates not allowed" 메시지가
# 발생하면서 프로그램이 죽어 버린다.

# 해결
# 출처를 알 수 없는 파일 이름을 출력할 떄 다음 코드로 에러를 방지한다.

def bad_filename(filename):
    return repr(filename)[1:-1]

try:
    print(filename)
except UnicodeEncodeError:
    print(bad_filename(filename))




# >>> for name in files:
# ...     print(name)
# ...
# spam.py
# Traceback (most recent call last):
#     File "<stdin>", line 2, in <module>
# UnicodeEncodeError: 'utf-8' codec can't encode character '\udce4' in
# position 1: surrogates not allowed


# >>> for name in files:
# ... try:
# ...     print(name)
# ... except UnicodeEncodeError:
# ...     print(bad_filename(name))
# ...
# spam.py
# b\udce4d.txt
# foo.txt


# 재인코딩

def bad_filename(filename):
    temp = filename.encode(sys.getfilesystemencoding(), errors='surrogateescape')
    return temp.decode('latin-1')






########## 5. 16. 이미 열려 있는 파일의 인코딩을 수정하거나 추가하기 ##########

# 문제
# 이미 열려 있는 파일을 닫지 않고 unicode 인코딩을 추가하거나 변경하고 싶다.

# 해결
# 바이너리 모드로 이미 열려 있는 파일 객체를 닫지않고 unicode 인코딩/디코딩을 추가하고 싶다면 그 객체를 io.TextIOWrapper() 객체로 감싼다.

import urllib.request
import io

u = urllib.request.urlopen('http://www.python.org')
f = io.TextIOWrapper(u, encoding='utf-8')
text = f.read()

# 텍스트 모드로 열린 파일의 인코딩을 변경하려면 detach() 메소드로 텍스트 인코딩 레이어를 제거하고 다른 것으로 치환한다.
# sys.stdout 의 인코딩을 바꾸는 방법을 알아보자

import sys
sys.stdout.encoding
# 'UTF-8'
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
sys.stdout.encoding
# 'latin-1'




f = open('sample.txt','w')
f
# <_io.TextIOWrapper name='sample.txt' mode='w' encoding='UTF-8'>
f.buffer
# <_io.BufferedWriter name='sample.txt'>
f.buffer.raw
# <_io.FileIO name='sample.txt' mode='wb'>


# 이 예제에서 io.TextIOWrapper는 유니코드를 인코딩/디코딩하는 텍스트 처리 레이어,
# io.BufferedWriter 는 바이너리 데이터를 처리하는 버퍼 I/O 레이어,
# io.FileIO 는 운영 체제에서 하위 레벨 파일 디스크립터를 표현하는 로우 파일이다.


# 일반적으로 앞에 나타난 속성에 접근해 헤이어를 직접 수정하는 것은 안전하지 않다.
# 예를 들어 이 기술을 사용해 인코딩을 변경했을 때 무슨일이 발생하는지 살펴보자.

f
# <_io.TextIOWrapper name='sample.txt' mode='w' encoding='UTF-8'>
f = io.TextIOWrapper(f.buffer, encoding='latin-1')
f
# <_io.TextIOWrapper name='sample.txt' encoding='latin-1'>
f.write('Hello')
# Traceback (most recent call last):
#     File "<stdin>", line 1, in <module>
# ValueError: I/O operation on closed file.

# F의 원본 값이 파괴되고 프로세스의 기저 파일을 닫았기 때문에 제대로 동작하지 않는다.
# detach 메소드는 파일의 최상단 레이어를 끊고 그 다음 레이어를 반환한다.
# 그 다음에 상단 레이어를 더 이상 사용할 수 없다.



# 하지만 연결을 끊은 후에는 반환된 결과에 새로운 상단 레이어를 추가할 수 있다.

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='ascii',  errors='xmlcharrefreplace')
print('Jalape\u00f1o')
#Jalape&#241;o




########## 5. 17. 텍스트 파일에 바이트 쓰기 ##########

# 문제
# 텍스트 모드로 연 파일에 로우 바이트를 쓰고 싶다.

# 해결
# 단순히 바이트 데이터를 buffer 에 쓴다.


import sys
# sys.stdout.write(b'Hello\n')
#
# Traceback (most recent call last):
#     File "<stdin>", line 1, in <module>
# TypeError: must be str, not bytes

sys.stdout.buffer.write(b'Hello\n')
# Hello
# 5





########## 5. 18. 기존 파일 디스크립터를 파일 객체로 감싸기 ##########

# 문제
# 운영 체제 상에 이미 열려 있는 I/O 채널에 일치하는 정수형 파일 디스크립터를 가지고 있고 (file, pipe, socket 등)
# 이를 상위 레벨 파이썬 파일 객체로 감싸고 싶다

# 해결
# 파일 디스크립터가 있을 때 open() 함수를 사용해 파이썬 객체로 감쌀 수 있다.
# 하지만 이 때 파일 이름 대신 정수형 파일 디스크립터를 먼저 전달해야 한다.

# 하위 레벨 파일 디스크립터 열기
import os
fd = os.open('somefile.txt', os.O_WRONLY | os.O_CREAT)

# 올바른 파일로 바꾸기기
f = open(fd, 'wt')
f.write('hello world\n')
f.close()


# 상위 레벨 파일 객체가 닫혔거나 파괴되었다면, 그 하단 파일 디스크립터 역시 닫힌다.
# 이런 동작을 원치 않는다면 close=False 인자를 open() 에 전달해야 한다.

f = open(fd, 'wt', closefd=False)


# 토론

# 유닉스 시스템 상에서 이 기술을 사용하면 기존의 I/O 채널을 감싸 파일과 같은 인터페이스로 사용할 수 있는 쉬운 길이 열린다.
# 소켓과 관련있는 다음 예를 보자.

from socket import socket, AF_INET, SOCK_STREAM

def echo_client(client_sock, addr):
    print('Got connection from', addr)

    # Make text-mode file wrappers for socket reading/writing
    client_in = open(client_sock.fileno(), 'rt', encoding='latin-1',
                closefd=False)

    client_out = open(client_sock.fileno(), 'wt', encoding='latin-1',
                closefd=False)

    # Echo lines back to the client using file I/O
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






########## 5. 19. 임시 파일과 디렉토리 만들기 ##########

# 문제
# 임시 파일이나 디렉토리를 만들어 프로그램에 사용해야 한다.
# 그 후에 파일이나 디렉토리는 아마도 파기할 생각이다.

# 해결
# tempfile 모듈에 이런 목적의 함수가 많이 있다. 이름 없는 임시 파일을 만들기 위해서 tempfile.TemporaaryFile 을 사용한다.

from tempfile import TemporaryFile

with TemporaryFile('w+t') as f:
    # 파일에서 읽기/쓰기
    f.write('Hello World\n')
    f.write('Testing\n')

    # 처음으로 이동해 데이터를 읽는다
    f.seek(0)
    data = f.read()

    # 임시 파일은 파기된다.

# 혹은 원한다면 다음과 같이 파일을 사용할 수도 있다.

f = TemporaryFile('w+t')
# Use the temporary file
...
f.close()
# File is destroyed


# TemporaryFile 은 추가적으로 내장함수 open()과 동일한 인자를 받는다.

with TemporaryFile('w+t', encoding='utf-8', errors='ignore') as f:
    ...


# 대개 유닉스 시스템에서 TemporaryFile()로 생성한 파일에 이름이 없고 디렉토리 엔트리도 갖지 않는다.
# 이러한 제한을 없애고 싶다면 아래와 같이....

from tempfile import NamedTemporaryFile

with NamedTemporaryFile('w+t') as f:
    print('filename is:', f.name)
    ...


# 임시 디렉토리를 만들기 위해서는  TemporaryDirectory()를 사용한다.

from tempfile import TemporaryDirectory

with TemporaryDirectory() as dirname:
    print('dirname is:', dirname)
    # Use the directory
    ...
# Directory and all contents destroyed






################################################################
# 6장. 데이터 인코딩과 프로세싱
################################################################


# 이번 장에서는 파이썬을 사용해 csv, json, xml, 바이너리 레코드 등으로 표현된 데이터를 다루는 방법을 알아본다.
# 자료 구조를 다룬 장과는 다르게, 이번 장에서는 특정 알고리즘이 아닌 프로그램에 데이터를 넣고 빼는 방법에 집중한다.




############### 6.1. csv 데이터 읽고 쓰기 ################

# 문제 - csv 파일로 인코딩된 데이터를 읽거나 쓰고 싶다.

# 해결
# 대부분의 csv 데이터는 csv 라이브러리를 활용한다. 예를 들어 stocks.csv 파일에 담겨 있는 주식 시장 정보가 있다고 가정해보자.
#
# Symbol,Price,Date,Time,Change,Volume
# "AA",39.48,"6/11/2007","9:36am",-0.18,181800
# "AIG",71.38,"6/11/2007","9:36am",-0.15,195500
# "AXP",62.58,"6/11/2007","9:36am",-0.46,935000
# "BA",98.31,"6/11/2007","9:36am",+0.12,104800
# "C",53.08,"6/11/2007","9:36am",-0.25,360900
# "CAT",78.29,"6/11/2007","9:36am",-0.23,225400

# 다음 코드로 데이터를 읽어 튜플 시퀀스에 넣을 수 있다.

import csv
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        # Process row
        ...

# 이 코드에서 row 은 튜플이 된다. 따라서 특정 필드에 접근하려면 row[0](symbol), row[4](change) 와 같이 인덱스를 사용해야 한다.

# 인덱스 사용이 때때로 헷갈리기 때문에 named tuple 을 고려하는 것도 좋다.

from collections import namedtuple
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for r in f_csv:
        row = Row(*r)
        # Process row
        ...

# 이렇게 하면 row.Symbol 이나 row.Change 와 같이 열 헤더를 사용할 수 있다.

# 또는 데이터를 딕셔너리 시퀀스로 읽을 수도 있다.

import csv
with open('stocks.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        # process row
        ...

# 이 버전의 경우, 각 행의 요소에 접근하기 위해서 행 헤더를 사용한다.

# csv 데이터를 쓰려면 csv 모듈을 사용해서 쓰기 객체를 생성한다.

headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
         ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
         ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
       ]

with open('stocks.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)



# 데이터를 딕셔너리 시퀀스로 가지고 있다면 다음과 같이 한다.

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




# 토론

# csv 데이터를 수동으로 다루는 프로그램을 작성하기 보다는 csv 모듈을 사용하는 것이 훨씬 나은 선택이다.

with open('stocks.csv') as f:
    for line in f:
        row = line.split(',')
        # process row
        ...

# 이 코드는 일일이 프로그래머가 따옴표를 잘라내야 한다거나 /  인용필드에 쉼표가 있는 경우 행 크기를 잘못 인식해 코드가 망가지는 등
# 신경써야 할 부분이 굉장히 많다.


# 탭으로 나누어진 데이터를 읽고 싶으면 아래와 같이 한다.
# 탭으로 구분한 값 읽기 예제
with open('stock.tsv') as f:
    f_tsv = csv.reader(f, delimiter='\t')
    for row in f_tsv:
        # Process row
        ...


# csv 파일에 다음과 같이 유효하지 않은 식별 문자가 들어 있다면

# Street Address,Num-Premises,Latitude,Longitude 5412 N CLARK,10,41.980262,-87.668452

# namedtuple 을 사용하려고 하면 valueError 가 발생한다.
# 이 예외를 피하기 위해서는 우선 헤더 처리를 해야 한다.
# 다음과 같이 정규식을 사용해 유효하지 않은 문자를 걸러낸다.

import re
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headers = [ re.sub('[^a-zA-Z_]', '_', h) for h in next(f_csv) ]
    Row = namedtuple('Row', headers)
    for r in f_csv:
        row = Row(*r)
        # Process row
        ...


# 또한 csv 는 데이터를 해석하려 하거나 문자열이 아닌 형식으로 변환하려 하지 않는다는 점이 중요하다.
# 추가적인 형식변환을 하는 예제

col_types = [str, float, str, str, float, int]
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        # Apply conversions to the row items
        row = tuple(convert(value) for convert, value in zip(col_types, row))
        ...

# 딕셔너리에서 선택한 필드만 변환하는 예제는 다음과 같다.
print('Reading as dicts with type conversion')
field_types = [ ('Price', float),
                ('Change', float),
                ('Volume', int) ]

with open('stocks.csv') as f:
    for row in csv.DictReader(f):
        row.update((key, conversion(row[key]))
                for key, conversion in field_types)
        print(row)





############### 6.2. JSON 데이터 읽고 쓰기 ################

#문제
#json(javascript object notation) 로 인코딩된 데이터를 읽거나 쓰고 싶다

# 해결
# json으로 데이터를 인코딩, 디코딩하는 쉬운 방법은 json 모듈을 사용하는 것이다.
# 주요 함수는 json.dumps() 와 json.loads() 이고 pickle 과 같은 직렬화 라이브러리에서 사용한 것과 인터페이스는 동일하다
# 파이썬 데이터를 json으로 변환하는 코드를 보자

import json

data = {
    'name' : 'ACME',
    'shares' : 100,
    'price' : 542.23
}

json_str = json.dumps(data)


# json 으로 인코딩된 문자열을 파이썬 자료 구조로 돌리는 방법
data = json.loads(json_str)

# 문자열이 아닌 파일로 작업한다면  json.dumps() 와 json.loads() 를 사용해서 json 데이터를 인코딩/디코딩 한다.

# Writing JSON data
with open('data.json', 'w') as f:
    json.dump(data, f)

# Reading data back
with open('data.json', 'r') as f:
    data = json.load(f)

# 토론
# json 인코딩은 none, bool. int, float, str 과 같은 기본 타입과 함께 리스트, 튜플, 딕셔너리와 같은 컨테이너 타입을 지원한다.

#  json 인코딩 포맷은 약간의 차이를 제외하고는 파이썬 문법과 거의 동일하다.
# 어떤 식으로 인코딩되는지는 다음코드를 참고한다.

json.dumps(False)
#'false'
d = {'a': True,
     'b': 'Hello',
     'c': None}
json.dumps(d)
#'{"b": "Hello", "c": null, "a": true}'



# 아래의 코드는 트위터의 검색 결과를 더 예쁘게 출력하는 방법!!

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


# 일반적으로 json 디코딩은 제공받은 데이터로부터 딕셔너리나 리스트를 생성한다.
# 다른 종류의 객체를 만들고 싶다면.... json.loads() 에 object_pairs_hook 이나 object_hook 을 넣는다.

# 예를 들어 orderedDict 의 순서를 지키면서 json 데이터를 디코딩하려면 다음과 같이
s = '{"name": "ACME", "shares": 50, "price": 490.1}'
from collections import OrderedDict
data = json.loads(s, object_pairs_hook=OrderedDict)
data
#OrderedDict([('name', 'ACME'), ('shares', 50), ('price', 490.1)])


# 다음은 json 데이터를 파이썬 객체로 바꾸는 예시이다.

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



# 인스턴스를 직렬화 하고 싶다면 인스트를 입력으로 받아 직렬화가능한 딕셔너리를 반환하는 함수를 제공해야 한다.

def serialize_instance(obj):
    d = { '__classname__' : type(obj).__name__ }
    d.update(vars(obj))
    return d

# 인스턴스를 돌려받고 싶다면 다음과 같은 코드를 작성한다.

# Dictionary mapping names to known classes
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




################# 6.3. 단순한 XML 데이터 파싱 ###############

# 문제
# 단순한 XML 문서에서 데이터를 얻고 싶다.

# 해결
# 단순한 XML 문서에서 데이터를 얻기 위해 xml.etree.ElementTree 모듈을 사용하면 됨.

# 스크립트는 다음과 같다.

from urllib.request import urlopen
from xml.etree.ElementTree import parse

# Download the RSS feed and parse it
u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(u)

# Extract and output tags of interest
for item in doc.iterfind('channel/item'):
    title = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')

    print(title)
    print(date)
    print(link)
    print()




################# 6.4. 매우 큰 xml 파일 증분 파싱하기 ###############

# 문제
# 매우 큰 xml 파일 에서 최소의 메모리만 사용하여 데이터를 추출하고 싶다면

# 해결
# 증분 데이터 처리에 직면할 때면 언제나 이터레이터와 제너레이터를 떠올려야 한다.
# 아래의 함수를 보자.

from xml.etree.ElementTree import iterparse

def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    # Skip the root element
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



# 위 함수를 테스트하려면 매우 큰 xml 파일이 필요한데...


from xml.etree.ElementTree import parse
from collections import Counter

potholes_by_zip = Counter()

doc = parse('potholes.xml')
for pothole in doc.iterfind('row/row'):
    potholes_by_zip[pothole.findtext('zip')] += 1
for zipcode, num in potholes_by_zip.most_common():
    print(zipcode, num)


# 요렇게 하면 메모리를 적게 쓰면서 데이터를 추출할 수 있당!!!


