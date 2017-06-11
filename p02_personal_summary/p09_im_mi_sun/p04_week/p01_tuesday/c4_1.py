######5.14 파일 이름 인코딩 우회
import sys
sys.getfilesystemencoding() #'utf-8'

#인코딩 우회 시 로우바이트 문자열로 파일 이름을 명시해야 함
#유니코드로 파일 이름을 씀
with open('jalape\xf1o.txt','w') as f:
    f.write('Spicy!')       #아무것도 안나오는데? >>6
#디렉토리 리스트(디코딩됨)
import os
os.listdir('.') #요상한 글자로 잘 나옴

#디렉토리 리스트(디코딩 되지 않음
os.listfir(b'.') #[b'jalape\xcc\x83o.txt'] #바이트 문자열로 나옴

#로우 파일 이름으로 파일 열기
with open(b'jalape\xcc\x83o.txt') as f:
    print(f.read())

#spicy!


#->oepn(), os.listdir()와 같은 파일 관련 함우세엇 바이트 문자열을 넣었을 때 파일 이름 처리는 거의 안변함


######5.15 망가진 파일 이름 출력
def bad_filename(filename):
    return repr(filename)[1:-1]

    try:
        print(filename)
    except UnicodeEncodeError:
        print(bad_filename(filename))

#특정 파일 시스템이 인코딩 규칙을 따르지 않을 경우 사
#대리 인코딩으로 매핑하여 해결
import os
files=os.listdir('.')
files
#['.DS_Store', '.git', '.idea', 'i_wanna', 'jalapeño.txt', 'pingpong', 'portfolio', 'PythonVariable', 'study_materials', 'tictactoe', 'tree', 'webcrawling']

for name in files:
    print(name)
#파일 이름 중에 \udce4와 같이 이상한 unicode면 에러가 나옴 오오!!이거 옛날에 나온 에러야
#UnicodeEncodeError: 'utf-8' codec can't encode character '\udc4' in position1:surrogates not allowed
#\udce4는 반쪽짜리사서 망가진 파일 이름일 경우 교정 작업을 해줘야함
for name in files:
    try:
        print(name)
    except UnicodeEncodeError:
        print(bad_filename(name))

#bad_filename() 함수 처리는 사용자 마음대로
def bad_filename(filename):
    temp = filename.encode(sys.getfilesystemencoding(), errors='surrogetaeescape')
    return temp.decode('latin-1')

#위 코드 사용 시 다음과 같이 출력됨
for name in files:
    try:
        print(name)
    except UnicodeEncodeError:
        print(bad_filename(name)) ##이거쓰면 \이런거 들어간 문자가 독일어 위에 땡땡처럼 잘 나옴

######5.16 이미 열려있는 파일의 인코딩을 수정하거나 추가하기
#이미 열려있는 파일을 닫지 않고 Unicode인코딩을 추가하거나 변경
#io.TextIOWrapper()사용
import urllib.request
import io

u=urllib.request.urlopen('http://python.org')
f=io.TextIOWrapper(u,encoding='utf-8')
text=f.read()

#텍스트 모드로 열린 파일의 인코딩 변경시 detach()메소드로 텍스트 인코딩 레이어를 제거하고 다른 것으로 치환
import sys
sys.stdout.encoding #utf-8
sys.stdout=io.TextIOWrapper(sys.stdout.detach(),encoding='latin-1')
sys.stdout.encoding #latin-1

#코드 실행시 터미널의 출력이 만들어질 수 있음(나는 하지말자...)
#I/O시스템은 여러 레이어로 구성(무슨말인지 모르겠음 스킵....똑똑해지면 보장ㅠㅠ)

#인코딩 변경하는 방법이지만 라인처리,에러큐긱 등 파일처리의 다른 측면에 활용 가능
sys.stdout=io.TextIOWrapper(sys.stdout.detach(),encoding='ascii',errors='xmlchrrefreplace')
print('Jalape\u00f1o') #ascii 문자 아닌게 이상하게 나옴 ?뭐어따쓰는겨

######5.17 텍스트 파일에 바이트 쓰기
#텍스트 모드로 연 파일에 로우 바이트 쓰기
#buffer

import sys
sys.stdout.write(b'Hello\n') #에러남
sys.stdoudt.buffer.write(b'Hello\n') #뭔지 모르겠음

######5.18 기존 파일 디스크립터를 파일 객체로 감싸기
#무슨 말인지 1도 모르겠어...
#하위레벨 파일 디스크립터 열기
import os
fd=os.open('somefile.txt', os.O_WRONLY | os.O_CREAT)

#올바른 파일로 바꾸기
f= open(fd,'wt')
f.write('hello world \n')
f.close()
######5.19 임시 파일과 디렉토리 만들기
#임시 파일이나 디렉터리를 만들어 프로그램 사용. 그 후에 파일이나 디렉토리 삭제
#tempfile.TemporartFile

from tempfile import TemporaryFile

with TemporaryFile('w+t') as f:
    #파일에서 읽기 쓰기
    f.write('hello world\n')
    f.wirte('testing\n')

    #처음으로 이동해 데이턱 읽음
    f.seek(0)
    data=f.read()
#데이터 파기

f=TemporaryFile('w+t')
#임시 파일 사용
#..
f.close() #파일 파기

##->text모드에서는 w+t, 바이너리 모드에서는 w+b 사용
#unix시스텡ㅁ에서 Temporaryfile()로 생성한 파일에 이름이 없고 디렉터리 엔트리고 갖지 않는데 이게 싫으면 NamedTemporarygile() 사용
from tempfile import NamedTemporaryFile
with NamedTemporaryFile('w+t') as f:
    print('filename is:',f.name)
#파일 자동으로 파기

#f.name 속성에 임시 파일의 이름이 담겨 있음 자동 삭제를 원하지 않는 경우 delete=False키워드 인자 사용
with NamedTemporaryFile('w+t',delete=False) as f:
    print('filename is:',f.name)
#임시 디렉토리 생성시
from tempfile import TemporaryDirectory
with TemporaryDirectory() as dirname:
    print('dirname is:', dirname)
#디렉토리와 모든 내용 파기

#더 하위 레벨로 내려가면 mkstemp(), mkdtemp()로 임시 파일과 디렉터리 생성 가능
import tempfile
tempfile.mkstemp()
tempfile.mkdtemp()
#단순히 로우 os파일 스트립터를 반환할 뿐 올바른 파일로 바꾸는 거나 제거는 내가 해야 함
#임시파일은 /var/temp에 생성
#위치 찾을 경우
tempfile.gettempdir()
#모든 임시파일 관련 함수는 디렉터리와 이름 규칙을 오버라이드 해야함
#prefix,suffix,dir 사용
f=NamedTemporaryFile(prefix='mytemp',suffix='.txt',dir='/tmp')
f.name #'/tmp/mytemp8ee899.txt'
#tempfile () 은 가장 안전한 방식으로 파일 생성(접근할 수 있는 권한을 현재 사용자에게만 줌)
##########Chapter6. 데이터 인코딩과 프로세싱

######6.1 csv 데이터 읽고 쓰기
#csv파일로 인코딩한 데이터를 읽거나 쓰고 싶은 경우 csv 라이브러리 사용
import csv
with open('stocks.csv') as f:
    f_csv=csv.reader(f)
    headers=next(f_csv)
    for row in f_csv:
        #행처리 ....??????
#row는 튜플이 됨 특정 필드에 접근시 row[0](Symbol), row[4](컬럼이름)과 같이 인덱스 사용
#1)인덱스 사용 헷갈리기 때문에 named tuple도 고려하는게 좋음
from collections import namedtuple
with open('stocks.csv') as f:
    f_csv=csv.reader(f)
    headings=next(f_csv)
    Row=namedtuple('Row',headings)
    for r in f_csv:
        row=Row(*r)
    #행처리
    #..
#row.컬럼이름 과 같이 열헤덜 사용 가능

#2)데이터를 딕셔너리 시퀀스로 읽을 수도 있음
import csv
with open('stocks.csv') as f:
    f_csv= csv.DictReader(f)
    for row in f_csv:
        #행처리
#각 행의 요소에 접근하기 위해 행 헤더 사용 row['컬럼이름'] 사용

#csv데이터를 쓰려면 csv모듈을 사용해서 객체  생성
headers=['colA','colB','colC']
rows=[('aa',11,'17/12/12'), ('bb',22,'17/12/13'),('cc',33,'17/12/14')]
with open('stocks.csv','w') as f:
    f_csv=csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerow(rows)

#딕셔너리 시퀀스일 경우 다음과 같이 함
rows=[{'colA':aa,'colB':'11','colC': '17/12/12'},{'colA':'bb','colB':'22','colC': '17/12/13'},{'colA':'cc','colB':'33','colC': '17/12/14'}]
with open('stocks.csv','w') as f:
    f_csv=csv.DictWriter(f,headers)
    f_csv.writeheader()
    f_csv.writerow(rows)

#csv사용시 모듈사용
#탭 구분 파일 경우
with open('stock.csv') as f:
    f_tsv=csv.reader(f,delimiter='\t')
    for row in f_tsv:
    #행처리
#csv데이터를 namedtuple로 변환시 열 헤더 검증에 주의
#유효하지 않은 문자가 들어있을 때 우선 헤더를 처리해야함
#유효하지 않는 문자를 정규식으로 치환
import re
with open('stock.csv') as f:
    f_csv=csv.header(f)
    headers=[re.sub('[^a-zA-z_]','_',h) for h in next(f_csv)]
    Row=namedtuple('Row',headers)
    for r in f_csv:
        row = Row(*r)

#csv데이터를 해석하려 하거나 문자열이 아닌 형식으로 변환은 프로그래머가 알아서 하셈

col_types=[str,float,str,str,float,int]
with open('stocks.csv') as f:
    f_csv=csv.reader(f)
    headers=next(f_csv)
    for row in f_csv:
        #행 아이템에 변환 적용
        row=tuple(convert(value) for conver, value in zip(col_types,row))
#딕셔러니에서 선택한 필드만 변환하는 경우 아래와 같음
print('Reading as dicts with type conversion')
field_types=[('price',float),('change',float),('volume',int)]
with open('stocks.csv') as f:
    for row in csv.DictReader(f):
        row.update((key,conversion(row[key]))
            for key,consversion in field_types)
        print(row)
#웬만하면 걍 쓰셈

######6.2 json데이터 읽고 쓰기
#json(javascropt object notation)인코딩한 데이터 읽고 쓰기
#json모듈 사용
#json.dumps(), json.loads()
#pickle과 같은 직렬화 라이브러리에서 사용한 것과 인터페이스틑동일함
#파이썬데이터>json데이터로 변환
import json
data={'name':'ACME','shares':100,'price':542.23}
json_str=json.dumps(data)
#json인코딩>python
data=json.loads(json_str)

#문자열이 아닌 파일로 작업 시 json.dump()와 json.load()를 사용하여 json데이터를 인코딩/디코딩 함
#json데이터 쓰기
with open('data.json','w') as f:
    json.dump(data,f)
#데이터 다시 읽기
with open('data.json','r') as f:
    data=json.load(f)
#json인코딩은 기본타입(None, bool,int,float,str)과 함께 리스트,튜플딕셔너리와 같은 컨테이터 타입 지원
#딕셔너리의 경우 키는 문자열로 가정
#웹 애플리케이션이 경우 사우이 레벨 객체는 딕셔너리로 하는 것이 표준임
#json인코딩 포맷은 파이썬하고 거의 동일
#True>true, False>false,None>null

#중첩 필드가 많은 경우 pprint() (알바벳 나열 ,딕셔너리를 보기 좋게 출력)
#트위터

from urllib.request import urlopen
import json
u = urlopen('http://search.twitter.com/search.json?q=python&rpp=5')
resp = json.loads(u.read().decode('utf-8'))
from pprint import pprint
pprint(resp)
# {'completed_in': 0.074,
#      'max_id': 264043230692245504,
#      'max_id_str': '264043230692245504',
#      'next_page': '?page=2&max_id=264043230692245504&q=python&rpp=5',
#      'page': 1,
#      'query': 'python',
#      'refresh_url': '?since_id=264043230692245504&q=python',
#      'results': [{'created_at': 'Thu, 01 Nov 2012 16:36:26 +0000',
#                   'from_user': ...
#                  },
#                  {'created_at': 'Thu, 01 Nov 2012 16:36:14 +0000',
#                   'from_user': ...
#                  },
#                  {'created_at': 'Thu, 01 Nov 2012 16:36:13 +0000',
#                   'from_user': ...
#                  },
#                  {'created_at': 'Thu, 01 Nov 2012 16:36:07 +0000',
#                   'from_user': ...
#                  }
#                  {'created_at': 'Thu, 01 Nov 2012 16:36:04 +0000',
#                   'from_user': ...
#                  }],
# 'results_per_page': 5,
#      'since_id': 0,
#      'since_id_str': '0'}

#json 디코딩은 제공받은 데이터로 부터 딕셔너리나 리스트 생
#다른 종류의 객체를 생성하고 싶은 경우 json.loads()에 object_pairs_hook이나 object_hook추가
#OrderedDict순서를 지키면서 json데이터 디코딩 시 아래와 가음
s = '{"name": "ACME", "shares": 50, "price": 490.1}'
from collections import OrderedDict
data = json.loads(s, object_pairs_hook=OrderedDict)
data  #OrderedDict([('name', 'ACME'), ('shares', 50), ('price', 490.1)])

#json딕셔너리를 > 파이썬 객체로
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

data = json.loads(s, object_hook=JSONObject)
data.name #'ACME'
data.shares #50
data.price #490.1
# 위에서 json데이터를 디코딩해여 생성한 딕셔너리를 __init__()인자에 전달함
#객체의 딕셔너리 인스턴스인것처럼 자유롭게 사용 가능

#######json인코딩 시 유용팁
#출력 : json.dumps() 에 indent . pprint같은 효과
print(json.dumps(data))
# {"price": 542.23, "name": "ACME", "shares": 100}
print(json.dumps(data, indent=4)) #올 좋은데
# {
#         "price": 542.23,
#         "name": "ACME",
#         "shares": 100
#}
#키 정렬시 sort_keys사용
print(json.dumps(data,sort_key=True)) #?똑같이 나오는데 무슨 기준으로 정렬하는겨

#인스턴스는 일바적으로 json을 직렬화하지 않음
class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
p=Point(2,3)
json.dumps(p)

# Traceback (most recent call last):
#       File "<stdin>", line 1, in <module>
#       File "/usr/local/lib/python3.3/json/__init__.py", line 226, in dumps
# return _default_encoder.encode(obj)
# File "/usr/local/lib/python3.3/json/encoder.py", line 187, in encode
#         chunks = self.iterencode(o, _one_shot=True)
#       File "/usr/local/lib/python3.3/json/encoder.py", line 245, in iterencode
# return _iterencode(o, 0)
# File "/usr/local/lib/python3.3/json/encoder.py", line 169, in default
# raise TypeError(repr(o) + " is not JSON serializable")
# TypeError: <__main__.Point object at 0x1006f2650> is not JSON serializable >>>
#인스턴스 직렬화하는 경우 인스턴스를 입력받아 직렬화 가능한 딕셔너리를 반환하는 함수 사용

def serialize_instance(obj):
    d = { '__classname__' : type(obj).__name__ } d.update(vars(obj))
    return d

#알려지지 않은 클래스에 이름을 매핑하는 딕셔너리
classes = {
        'Point' : Point
}

def unserialize_object(d):
    clsname = d.pop('__classname__', None)
    if clsname:
        cls = classes[clsname]
        obj = cls.__new__(cls) #__init__호출하지 않고 인스턴스 만들기
                    setattr(obj, key, value)
        return obj
    else:
        return d

p = Point(2,3)
s = json.dumps(p, default=serialize_instance)
s #'{"__classname__": "Point", "y": 3, "x": 2}'
a = json.loads(s, object_hook=unserialize_object)
a #<__main__.Point object at 0x1017577d0>
a.x #2
a.y #3

#json모듈에는 숫자,NaN과 가튼 특별 값등 하위 레벨 조절을 위한 옵션이 있음 참고하셈

######6.3 단순한 XML 데이터 파싱
#단순한 XML문서에서 데이터를 얻으려면 xml.etree.ElemetTree 사용
#planet python에서 RSS피드를 받아 파싱해야하는 경우

from urllib.request import urlopen
from xml.etree.ElementTree import parse
#RSS피드 다운 받고 파싱
u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(u)
#관심있는 태그 뽑아서 출력
for item in doc.iterfind('channel/item'):
    title = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')
    print(title)
    print(date)
    print(link)
    print()

##결과 쿡북 카피
# Steve Holden: Python for Data Analysis
# Mon, 19 Nov 2012 02:13:51 +0000
# http://holdenweb.blogspot.com/2012/11/python-for-data-analysis.html
# Vasudev Ram: The Python Data model (for v2 and v3)
# Sun, 18 Nov 2012 22:06:47 +0000
# http://jugad2.blogspot.com/2012/11/the-python-data-model.html
# Python Diary: Been playing around with Object Databases
# Sun, 18 Nov 2012 20:40:29 +0000
# http://www.pythondiary.com/blog/Nov.18,2012/been-...-object-databases.html
# Vasudev Ram: Wakari, Scientific Python in the cloud
# Sun, 18 Nov 2012 20:19:41 +0000
# http://jugad2.blogspot.com/2012/11/wakari-scientific-python-in-cloud.html
# Jesse Jiryu Davis: Toro: synchronization primitives for Tornado coroutines
# Sun, 18 Nov 2012 20:17:49 +0000
# http://feedproxy.google.com/~r/EmptysquarePython/~3/_DOZT2Kd0hQ/


#고급진 애플리케이션 개발중이면 lxml 사용
######6.4 매우 큰 XML파일 증분 파싱하기
#최소한의 메모리만 사용하여 데이터 추출
from xml.etree.ElementTree import iterparse
def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    #뿌리요소 건너뛰기
    next(doc)
    tag_stack = [] elem_stack = []
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

from xml.etree.ElementTree import parse
from collections import Counter
potholes_by_zip = Counter()
doc = parse('potholes.xml')
for pothole in doc.iterfind('row/row'):
    potholes_by_zip[pothole.findtext('zip')] += 1
for zipcode, num in potholes_by_zip.most_common():
    print(zipcode, num)
#파일 전체를 읽어 메모리 저장했음 다음꺼 사용하셈
from collections import Counter
potholes_by_zip = Counter()
data = parse_and_remove('potholes.xml', 'row/row')
for pothole in data:
    potholes_by_zip[pothole.findtext('zip')] += 1
for zipcode, num in potholes_by_zip.most_common():
    print(zipcode, num)
#ㅠㅠ그담은 무슨말인지 1도 모르겠음 책 한번 더 보기

#증분할 경우 속도가 느림. 용랑&속도 중 우선시 되는 거에 따라 사용하기