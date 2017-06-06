# # 5.14 파일 이름 인코딩 우회
# # 문제
# # 시스템의 기본 인코딩으로 디코딩 혹은 인코딩되지 않은 파일 이름에 입출력 작업을 수행해야 한다
# # 해결
# # 기본적으로 모든 파일 이름은 sys.getfilesystemencoding()이 반환하는 텍스트 인코딩 값으로 디코딩 혹은 인코딩되어 있다
# import sys
# print(sys.getfilesystemencoding()) # mbcs 출력
# # 하지만 이 인코딩을 위회하길 바란다면 로우(raw) 바이트 문자열로 파일 이름을 명시해야 한다
# # ㅇ니코드로 파일 이름을 쓴다.
# with open('jalape/xflo.txt','w') as f:
#     f.write('Spicy!')
# # 디렉토리 리스트(디코딩됨)
# import os
# os.listdir('.') #['jalapeno.txt'] 출력
# # 디렉토리 리스트( 디코딩 되지 않음 )
# os.listdir(b',') # [b'jalapen/xcc/x83o.txt'] 출력
# # 로우 파일 이름으로 파일 열기
# with open(b'jalapen/xcc/x83o.txt') as f:
#     print(f.read()) # Spicy! 출력
# # 마지막 두 작업에 나온 것처럼, open() 이나 os.listdir()와 같은 파일 관련 함수에 바이트 문자열을 넣었을때 이름 처리는 거의 변하지않음
# # 토론
# # 일반적인 환경에서 파일 이름 인코딩, 디코딩에 대해 걱정할 필요는 없다.
# # 대부분의 경우에는 무리 없이 잘 동작한다
# # 하지만 많은 운영 체제에서 사용자는 실수로 혹은 악의적으로 인코딩 규칙을 따르지 않는 파일 이름을 생성할 수 있다
# # 이런 파일 이름은 많은 파일을 다루는 파이썬 프로그램을 망가트 릴 수 있다
# # 파일 이름과 디렉토리를 읽을 때 디코딩되지 않은 로우 바이트를 이름으로 사용하면 프로그래밍 과정은 조금 귀찮겠지만
# # 이런 문제점을 피해 갈 수 있다
# # 디코딩되지 않은 파일 이름을 출력하는 방법을 레시피 5.15에서 알아본다

# 5.15 망가진 파일 이름 출력
# # 문제
# # 프로그램에서 디렉토리 리스트를 받아 파일 이름을 출력하려고 할 때, UnicodeEncodeError 예외와
# # "surrogaes not allowed" 메시지가 발생하면서 프로그램이 죽어 버린다
# # 해결
# # 출처를 알 수 없는 파일 이름을 출력할 때, 다음 코드로 에러를 방지한다
# # def bad_filename(filename):
# #     return repr(filename)[1:-1]
# # try:
# #     print(filename)
# # except UnicodeEncodeError:
# #     print(bad_filename(filename)
# # 토론
# # 이번 레시피는 자주 발생하지는 않지만 파일 시스템에 발생할 수 있는 아주 귀찮은 문제를 다루었다.
# # 기본적으로 파이썬은 모든 파일이름이 sys.getfilesystemencoding()이 반환하는 값으로 인코딩되어 있다고 가정한다
# # 하지만 특정 파일 시스템은 인코딩 규칙을 따르도록 강제하지 않아서 올바르지 않은 인코딩을 사용한 파일 이름이 생기기도 한다
# import os
# files = os.listdir('.')
# print(files)
# # ['CookBook-1Weekly_Thur.py', 'CookBook-1Weekly_Tue.py', 'CookBook-2Weekly_Tue.py', 'Cookbook-4Weekly-Tue.py'] 출력
# # 파일 이름을 다루거나 open()과 가은 함수에 전달하는 코드가 있따면 모두 정상적으로 동작한다
# for name in files:
#     print(name)
# # CookBook-1Weekly_Thur.py
# # CookBook-1Weekly_Tue.py
# # CookBook-2Weekly_Tue.py
# # Cookbook-4Weekly-Tue.py 출력

# # 5.16 이미 열려 있는 파일의 인코딩을 수정하거나 추가하기
# # 문제
# # 이미 열려있는 파일을 닫지 않고 Unicode 인코딩을 추가하거나 변경하고 싶다
# # 해결
# # 바이너리 모드로 이미 열려 있는 파일 객체를 닫지 않고 Unicod 인코딩/디코딩을 추가하고 싶다면
# # 그 객체를 io.TextIOWrapper() 객체로 감싼다
# import urllib.request
# import io
# u = urllib.request.urlopen('http://www.python.org')
# f = io.TextIOWrapper(u,encoding='utf-8')
# text = f.read()
# print(text)
# # 텍스트 모드로 열린파일의 인코딩을 변경하려면 detach() 메소드로 텍스트 인코딩 레이어를 제거하고 다른것으로 치환한다.
# # sys.stdout의 인코딩을 바꾸는 방법을 보자
# import sys
# print(sys.stdout.encoding) # UTF-8 출력
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(),encoding='latin-1')
# print(sys.stdout.encoding) # latin-1 출력
# # 이 코드를 실행하면 터미널의 출력이 망가질 수도 있다
# # 토론
# # I/O 시스템은 여러 레이어로 만들어져 있다. 다음 간단한 코드를 통해 레이어를 볼 수 있다
# f = open(r"C:\Users\Won Tae CHO\Desktop\Python 알고리즘.txt",'w')
# print(f)
# # 이 예제에서 io.TextIOWrapper는 Unicode 를 인코딩/디코딩하는 텍스트 처리 레이어 io.BufferedWriter는 바이너리 데이터를 처리하는 버퍼 I/O
# # 레이어, io.FileIO는 운영체제에서 하위 레벨 파일 디스크립터를 표현하는 로우 파일이다
# # 텍스트 인코딩의 추가,수정에는 최상단 레이어인 io.TextIOWrapper의 추가, 수정이 포함된다

# # 5.17 텍스트 파일에 바이트 스기
# # 문제
# # 텍스트 모드로 연 파일에 로우 바이트를 쓰고 싶다
# # 해결
# # 단순히 바이트 데이터를 buffer에 쓴다
# import sys
# # a = sys.stdout.write(b'Hello')
# # print(a)
# # Traceback (most recent call last):
# #   File "C:/Users/Won Tae CHO/PycharmProjects/Source/CookBook-Master/Cookbook-4Weekly-Tue.py", line 91, in <module>
# #     a = sys.stdout.write(b'Hello')
# # TypeError: write() argument must be str, not bytes 출력
# print(sys.stdout.buffer.write(b'Hello\n')) # Hello 6 출력
# # 이와 유사하게, 텍스트 파일의 buffer 속성에서 바이너리 데이터를 읽을 수도 있다
# # 토론
# # I/O 시스템은 레이어로부터 만들어진다.
# # 텍스트 파일은 버퍼 바이너리 모드 파일 상단에 Unicode 인코딩/디코딩 레이어를 추가해서 생성된다
# # buffer 속성은 바로 이 파일 아래 부분을 가리킨다.
# # 여기에 접근하면 텍스트 인코딩/디코딩 레이어를 우회할 수 있다
# # 바이너리 데이터를 표준 출력에 출력하는 스크립트를 작성한다면 이 기술을 사용해 텍스트 인코딩을 우회할 수 있다

# # 5.18 기존 파일 디스크립터를 파일 객체로 감싸기
# # 문제
# # 운영체제 상에 이미 열려있는 I/O 채널에 일치하는 정수형 파일 디스크립터를 가지고 있고, 이를 상위 레벨 파이썬파일객체로 감싸고싶다
# # 해결
# # 파일 디스크립터는 운영 체제가 할당한 정수형 핸들로 시스템 I/O 채널등을 참조하기 위한 목적으로써 일반파일과는 다르다
# # 파일 디스크립터가 있을 때 open() 함수를 사용해 파이썬 파일 객체로 감쌀 수 있다
# # 하지만 이때 파일 이름 대신 정수형 파일 디스크립터를 먼저 전달해야 한다
# # 하위 레벨 파일 디스크립터 열기
# import os
# df = os.open(r"C:\Users\Won Tae CHO\Desktop\Python 알고리즘.txt",os.O_WRONGLY | os.O_CREAT)
# # 올바른 파일로 바꾸기
# f = open(df, 'wt')
# f.write('hello world\n')
# f.close()
# # 상위 레벨 파일 객체가 닫혔거나 파괴되었다면, 그 하단 파일 디스크립터 역시 닫힌다.
# # 이런 동작을 원하지 않는다면 closedf=False 인자를 open()에 전달해야 한다
# # 파일 객체를 생성하지만, 사용이 끝났을 때 df를 닫지 않는다
# f = open(df, 'wt', closedf=False)
# ...
# # 토론
# # Unix 시스템 상에서 이 기술을 사용하면 기존의 I/O 채널을 감싸 파일과 같은 인터페이스로 사용할 수 있는 쉬운 길이 열린다
# # 소켓과 관련 있는 다음 예를 보자
# from socket import socket, AF_INET, SOCK_STREAM
# def echo_client(client_sock,addr):
#     print('Got connection from',addr)
#     # 읽기/쓰기를 위해 소켓에 대한 텍스트 모드 파일 래퍼(wrapper)를 만든다
#     client_in = open(client_sock.fileno(),'rt',encoding='latin-1',closedf=False)
#     client_out = open(client_sock.fileno(),'wt',encoding='latin-1', closedf=False)
#     # 파일 I/O를 사용해 클라이어느에 라인을 에코한다
#     for line in client_in:
#         client_out.write(line)
#         client_out.flush()
#     client_sock.close()
# def echo_server(address):
#     sock = socket(AF_INET, SOCK_STREAM)
#     sock.bind(address)
#     sock.listen(1)
#     while True:
#         client,addr = sock.accept()
#         echo_client(client.addr)
# # 앞에 나온 예제는 내장 함수 open()의 기능을 보이기 위한 목적으로 작성한 것이고
# # Unix 기반 시스템에서만 동작한다. 소켓에 대한 파일 같은 인터페이스가 필요하고 크로스 플랫폼 코드가 필요하다면
# # makefile() 메소드를 사용해야 한다. 하지만 이식성을 신경쓰지 않는다면 makefile()을 사용하는 것보다
# # 앞에 나온 예제가 성능 면에서 훨씬 뛰어나다.
# # 이미 열려 있는 파일을 가리키는 가명(alias)을 만들어 처음과 조금 다른 방법으로 사용하는데 이 기술을 사용할 수도 있다
# # 예를 들어 stdout(일반적으로 텍스트 모드로 열려 있다)에 바이너리 데이터를 넣기위한 파일객체를 만드는 방법을 보자
# import sys
# # stdout에 대한 바이너리 모드 파일 만들기
# bstdout = open(sys.stdout.fileno(),'wb',closedf=False)
# bstdout.write(b'Hello World\n')
# bstdout.flush()
# # 기존 파일 디스크립터를 파일로 감싸는 것도 가능하지만, 모든 파일 모드를 지원하지 않을 수 있고, 이런 파일 디스크립터에
# # 예상치 못한 부작용이 생길 수 있다. 또한 동작성이 운영체제에 따라 달라지기도 한다
# # 예를 들어 앞에 나온 모든 예제는 Unix가 아닌 시스템에서 아마도 동작하지 않을 것이다
# # 결과적으로 모든 구현물이 잘 동작하는지 꼼꼼히 테스트 해보는 수 밖에 없다

# # 5.19
# # 문제
# # 임시 파일이나 디렉토리를 만들어 프로그램에 사용해야 한다
# # 그 후에 파일이나 디렉토리는 아마도 파기할 생각이다
# # 해결
# # tempfile 모듈에 이런 목적의 함수가 많이 있다
# # 이름 없는 임시 파일을 만들기 위해서 tempfile.TemporaryFile을 사용한다
# from tempfile import TemporaryFile
# with TemporaryFile('w+t') as f:
#     # 파일에서 읽기/쓰기
#     f.write('Hello World\n')
#     f.write('Testing\n')
#     # 처음으로 이동해 데이터를 읽는다
#     f.seek(0)
#     data = f.read()
# # 임시파일은 파기된다
# # TemparyFile()에 전달하는 첫 번째 인자는 파일 모드이고, 텍스트 모드에는 대개 w+t를,
# # 바이너리 모드에는 w+b를 사용한다
# # 이모드는 읽기와 쓰기를 동시에 지원하기 때문에 모드 변경을 위해 파일을 닫으면 실제로 파기하므로 유용하다
# # 대개 유닉스시스템에서 TemporaryFile()로 생성한 파일에 이름이 없고 디렉토리 엔트리도 갖지 않는다
# # 이 제한을 없애고 싶으면 NamedTemporaryFile()을 쓰면 된다
# from tempfile import NamedTemporaryFile
# with NamedTemporaryFile('w+t') as f:
#     print('filename is :',f.name)
#     ...
# # 파일이 자동으로 파기된다
# # f.name 속성에 임시 파일의 파일 이름이 담겨있다. 다른 코드에 이 파일을 전달해야 할 필요가 생겼을때 이 속성을 유용하게
# # 사용할 수 있다. 사용이 끝났을 때 자동으로 삭제된다
# # 이런 동작을 원하지 않는다면  delete=False 키워드 인자를 사용하면 된다.
# # 토론
# # 임시 파일과 디렉토리를 만들때 TemporaryFile(), NamedTemporaryFile(), TemporaryDirectory() 함수가 가장 쉬운 방법이다.

# CHAPTER 6. 데이터 인코딩과 프로세싱
# 6.1 CSV 데이터 읽고 쓰기
# 문제
# CSV 파일로 인코딩된 데이터를 읽거나 쓰고 싶다
# 해결
# 대부분의 CSV 데이터는 csv 라이브러리를 사용한다.
# 예를 들어, stocks.csv 파일에 담겨있는 주식 시장 정보가 있다고 가정해보자
# Symbol,Price,Date,Time,Change,Volume
# "AA",39.48,"6/11/2007","9:36am",-0.18,181800
# "AIG",71.38,"6/11/2007","9:36am",-0.15,195500
# "AXP",62.58,"6/11/2007","9:36am",-0.46,935000
# "BA",98.31,"6/11/2007","9:36am",+0.12,104800
# "C",53.08,"6/11/2007","9:36am",-0.25,360900
# "CAT",78.29,"6/11/2007","9:36am",-0.23,225400
# 다음코르도 데이터를 읽어 튜플 시퀀스에 넣을 수 있다
import csv
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        # 행처리
        ...
# 앞에 나온 코드에서 row는 ㅠ플이 된다
# 따라서 특정 필드에 접근하려면 row[0](Symbol), row[4] (Change)와 같이 인덱스를 해야 한다.
# 인덱스 사용이 때때로 헷갈리기 때문에 네임드 튜플을 고려하는 것도 좋다
from collections import namedtuple
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for r in f_csv:
        row = Row(*r)
        #행처리
        ...
# 이렇게 하면 row.Symbol 이나 row.Change와 같이 열 헤더를 사용할 수 있다
# 다만 열 헤더가 유효한 파이썬 식별자여야 한다
# 그렇지 않으면 초기 헤딩에 메시지를 보내서 식별자가 아닌 문자를 밑줄이나 유사한 것으로 변경해야 할지도 모른다
# 또 다른 대안으로 데이터를 딕셔너리 시퀀스로 읽을 수도 있다
import csv
with open('stocks.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
    #행처리
    ...
# CSV 데이터를 쓰려면, csv모듈을 사용해서 쓰기 객체를 생성한다
headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
         ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
         ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
       ]
with open('stocks.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
# 데이터를 딕셔너리 시퀀스로 가지고 있다면 다음과 같이 한다
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


#탭으로 구분한 값 읽기 예제
with open('stock.tsv') as f:
    f_tsv = csv.reader(f, delimiter='\t')
    for row in f_tsv:
        ...
# CSV 데이터에 대해서 추가적인 형식 변환을 하는 예
col_types = [str, float, str, str, float, int]
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        #행 아이템에 변환 적용
        row = tuple(convert(value) for convert, value in zip(col_types, row))
# 딕셔너리에서 선택한 필드만 변환하는 예제는 다음과 같다
print('Reading as dicts with type conversion')
field_types = [ ('Price', float),
                ('Change', float),
                ('Volume', int) ]
with open('stocks.csv') as f:
    for row in csv.DictReader(f):
        row.update((key, conversion(row[key]))
                for key, conversion in field_types)
        print(row)
# 6.2 JSON 데이터를 읽고 쓰기
# 문제
# JSON으로 인코딩된 데이터를 읽거나 쓰고 싶다
# 해결
# JSON으로 디에터를 인코딩, 디코딩 하는 쉬운 방법은 json 모듈을 사용하는 것이다.
import json
data = {
    'name': 'ACME',
    'shares': 100,
    'price': 542.23
}
json_str = json.dumps(data)
# 다음은 JSON 인코딩된 문자열을 파이썬 자료 구조로 돌리는 방법
data = json.loads(json_str)
# JSON 데이터 쓰기
with open('data.json', 'w') as f:
    json.dump(data, f)
# 데이터 다시 읽기
with open('data.json', 'r') as f:
    data = json.load(f)
# 토론
# JSON인코딩은 None,bool,int,float,str과 같은 기본 타입과 함꼐 리프트, 튜플, 딕셔너리와 같은 컨테이너 타입을 지원한다
json.dumps(False)
'false'
d = {'a': True,
     'b': 'Hello',
     'c': None}
json.dumps(d)
'{"b": "Hello", "c": null, "a": true}'
False -> false, True -> true, None -> null

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
s = '{"name": "ACME", "shares": 50, "price": 490.1}'
from collections import OrderedDict
data = json.loads(s, object_pairs_hook=OrderedDict)
data
OrderedDict([('name', 'ACME'), ('shares', 50), ('price', 490.1)])
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d
data = json.loads(s, object_hook=JSONObject)
data.name
# 'ACME'
data.shares
# 50
data.price
# 490.1

