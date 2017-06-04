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