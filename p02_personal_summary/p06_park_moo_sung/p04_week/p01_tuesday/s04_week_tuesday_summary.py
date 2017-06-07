#########################################################

#5.14 파일 이름 인코딩 우회

# 기본 : sys.getfilesystemencoding() 이 반환하는 텍스트 인코딩 값으로 디코딩 or 인코딩 돼있음

import sys
print(sys.getfilesystemencoding())

# 우회 : raw 바이트 문자열로 파일 이름 명시

with open('jalape\xf1o.txt' , 'w') as f: # 유니코드로 파일이름 쓰기
    f.write('spicy!')

import os  # 디렉터리 리스트(디코딩됨)
os.listdir('.')

os.listdir(b'.') # 디코딩되지 않음

with open(b'jalapen\xcc\x83o.txt') as f: # 로우 파일이름으로 파일 열기
    print(f.read())

#########################################################

# 5.15 망가진 파일 이름 출력

# 출처를 알 수 없는 파일이름 출력 시

def bad_filename(fn):
    return repr(fn)[1:-1]

try:
    print(filename)
except UnicodeEncodeError:
    print(bad_filename(filename))

# 대리 인코딩 : UTF-8 이 아닌 Latin-1 로 인코딩

files = ['spam.py', 'b\udce4d.txt', 'foo.txt']
import os
files = os.listdir('.')
print(files)


for name in files: # 파일 이름을 출력할 때만 문제 발생
    print(name)    # why? \udce4 가 잘못된 unicod 이므로

for name in files:
    try:
        print(name)
    except UnicodeEncodeError:
        print(bad_filename(name))

#############################################################

# 5.16 이미 열려있는 파일의 인코딩을 수정하거나 추가하기

# 바이너리 모드로 열린 파일의 Unicode 인코딩 추가 or 변경

import urllib.request
import io

u = urllib.request.urlopen('http://www.python.org')
f = io.TextIOWrapper(u, encoding='utf-8') # 객체를 io.TextIOWrapper() 로 감싸기
text = f.read()

# 텍스트 모드로 열린 파일의 Unicode 인코딩 추가 or 변경
import sys
print(sys.stdout.encoding)

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
sys.stdout.encoding # 단 코드 실행하면 터미널 출력 망가질 수 있음!! 실행 말자!!

# I/O 시스템의 여러 레이어 확인

f = open('sample.txt', 'w')
## <_io.TextIOWrapper name='sample.txt' mode='w' encoding='UTF-8'>
f.buffer
## <_io.BufferedWriter name='sample.txt'>
f.buffer.raw
## <_io.FileIO name='sample.txt' mode='wb'>

f = io.TextIOWrapper(f.buffer, encoding='latin-1') # f의 원본값이 파괴되었으므로 동작 x
f.write('hello')

b = f.detach()
f.write('hello')

f = io.TextIOWrapper(b, encoding='latin-1') # 연결 끊은 후 반환된 결과에 새로운 상단 레이어 추가 가능

# 인코딩 변경 or 라인 처리 or 에러 규칙 처리 등에 사용할 수 있는 기술 ...??

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='ascii', errors='xmlcharrefreplace')


######################################################

# 5.17 텍스트 파일에 바이트 쓰기

# 텍스트 모드로 연 파일에 raw 바이트 쓰고 싶을 때

import sys

sys.stdout.write(b'hello\n')           # 안됨

sys.stdout.buffer.write(b'hello\n')    # buffer 쓰면 됨

#######################################################

# 5.18 기존 파일 디스크립터를 파일 객체로 감싸기

# open()함수를 사용한 파이썬 파일 객체 감싸기

import os # 하위 레벨 파일 디스크립터 열기????
fd = os.open('somefile.txt', os.O_WRONLY | os.O_CREAT)

f = open(fd, 'wt') # 올바른 파일로 바꾸기
f.write('hello world\n')
f.close()

f = open(fd, 'wt', closefd = False) # 파일 객체를 생성 but 사용 끝났을 때 fd 닫지 않으려면
                                    # why? 상위 레벨 파일 객체 닫히거나 파괴되면 하단 파일 디스크립터도 역시 닫히므로 이를 막기위해

# Unix 시스템 상에서 소켓...??

from socket import socket, AF_INET, SOCK_STREAM

def echo_client(client_sock, addr):
    print('Got connection from', addr)

    # 읽기/쓰기를 위해 소켓에 대한 텍스트 모드 파일 래퍼(wrapper) 를 만든다
    client_in = open(client_sock.fileno(), 'rt', encoding = 'latin-1', closefd=False)
    client_out = open(client_sock.fileno(), 'wt', encoding = 'latin-1', closefd=False)

    # 파일 I/O를 사용해 클라이언트에 라인 에코
    for line in client_in :
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

# 이미 열려 있는 파일의 가명(alias)을 만들어 바이너리 데이터 넣기 위한 파일객체 만들기....???

import sys
bstdout = open(sys.stdout.fileno(), 'wb', closefd=False)
bstdout.write(b'hello world\n')
bstdout.flush()

#########################################################

# 5.19 임시 파일과 디렉터리 만들기

# tempfile 모듈

from tempfile import TemporaryFile
with TemporaryFile('w+t') as f:
    # 파일에서 읽기/쓰기
    f.write('hello world\n')
    f.write('testing\n')

    # 처음으로 이동해 데이터 읽기
    f.seek(0)
    data = f.read()

    # 임시 파일 파기

# Unix 시스템에서 temporaryfile() 로 생성한 파일의 이름, 디렉터리 엔트리 갖게 하는 법

from tempfile import NamedTemporaryFile

with NamedTemporaryFile('w+t') as f:
    print('filename is:', f.name)

    # 파일 자동 파기

# 자동 파기 막으려면

with NamedTemporaryFile('w+t',delete=False) as f:
    print('filename is:', f.name)

############################################################

# 6.1 CSV 데이터 읽고 쓰기


####### csv 읽기 ######
# csv 모듈

import csv
with open('file.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        print(row)   # 이때 row 는 튜플이 됨

# named tuple 활용

from collections import namedtuple
with open('file.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for r in f_csv:
        row = Row(*r)

# 딕셔너리 시퀀스 활용

import csv
with open('file.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv :

# 탭으로 나눠진 데이터 읽기

with open('file.csv') as f:
    f_tsv = csv.reader(f, delimiter='\t')
    for row in f_tsv:
        print(row)

# csv 파일 안의 유효하지 않은 식별 문자 처리

import re
with open('file.csv') as f:
    f_csv = csv.reader(f)
    headers = [ re.sub('[^a-zA-z_]', '_', h) for h in next(f_csv)]
    Row = namedtuple('Row', headers)
    for r in f_csv:
        row = Row(*r)

# csv 데이터 추가적인 형식 변환하기

col_types = [str, float, str, str, float, int]
with open('file.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        # 행 아이템에 변환 적용
        row = tuple(convert(value) for convert, value in zip(col_types, row))

# 딕셔너리에서 선택한 필드만 변환하기

print('Reading as dicts with type conversion')
file_types = [ ('price', float),
               ('change', float),
               ('volume', int)]
with open('file.csv') as f:
    for row in csv.DictReader(f):
        row.update((key, conversion(row[key])) for key, conversion in file_types)
    print(row)

# pandas.read_csv() 쓰기

###### csv 쓰기 ######

with open('file.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)

# 딕셔너리 형태일 때

with open('file.csv', 'w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows()

###########################################################

# 6.2 JSON 데이터 읽고 쓰기

# json 모듈 이용한 json 인코딩 or 디코딩

import json # 파이썬 데이터 -> json
data = {
    'name' : 'ACme',
    'shares' : 100,
    'price' : 542.23
    }
json_str = json.dumps(data)

data = json.loads(json_str) # json -> 파이썬

with open('data.json','w') as f: # json 데이터 쓰기
    json.dump(data, f)

with open('data.json', 'r') as f: # 데이터 다시 읽기
    data = json.load(f)

# json은 기본 타입 + 리스트, 튜플, 딕셔너리와 같은 컨테이너 타입 지원

# 파이썬 문법과의 차이 : True -> true, False -> false, None -> null

json.dumps(False)
## false

d= {'a' : True, 'b' : 'Hello', 'c' : None}
json.dumps(d)
## {"b": "Hello", "c" : null, "a" : true}

# OrderedDict 의 순서 지키며 json 데이터 디코딩하기

s= '{"name" : "ACME", "shares":50, "price":490.1}'
from collections import OrderedDict
data = json.loads(s, object_pairs_hook=OrderedDict)

# json 딕셔너리 -> 파이썬 객체

class JSONOBJECT:
    def __init__(self,d):
        self.__dict__ = d

data = json.loads(s, object_hook=JSONOBJECT)
data.name
## 'ACME'
data.shares
## 50
data.price
## 490.1

###########################################################

# 6.3 단순한 XML 데이터 파싱

# xml.entree.ElementTree 모듈

from urllib.request import urlopen
from xml.etree.ElementTree import parse

u = urlopen('http://planet.python.org/rss20.xml') # rss 피드 다운로드, 파싱
doc = parse(u)

for item in doc.iterfind('channel/item') : # 관심있는 태그 뽑아 출력
    title = item.findtext('title')
    date = item.findtext('pubDate')
    line = item.findtext('link')

# get() 메소드로 필요한 요소 얻기

e = doc.find('channel/title')
e.tag
## title
e.text
## planet python
e.get('some_attribute')

#########################################################

# 6.4 매우 큰 xml 파일 증분 파싱

# 증분 데이터 처리 시 --> 이터레이터, 제너레이터

from xml.etree.ElementTree import iterparse

def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    # 뿌리 요소 건너뛰기
    next(doc)

    tag_stack=[]
    elem_stack=[]
    for event, elem in doc:
        if event == 'start' :
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

# zip 코드별로 순위 매기는 스크립트 작성(XML 파일 전체를 읽어 메모리에 넣음)

from xml.etree.ElementTree import parse
from collections import Counter

potholes_by_zip = Counter()
doc = parse('potholes.xml')

for pothole in doc.iterfind('row/row'):
    potholes_by_zip[pothole.findtext('zip')] += 1

for zipcode, num in potholes_by_zip.most_common():
    print(zipcode, num)

# 더 나은 코드..?

from collections import Counter

potholes_by_zip = Counter()

data = parse_and_remove('potholes.xml', 'row/row')

for pothole in data:
    potholes_by_zip[pothole.findtext('zip')] += 1

for zipcode, num in potholes_by_zip.most_common():
    print(zipcode, num)









