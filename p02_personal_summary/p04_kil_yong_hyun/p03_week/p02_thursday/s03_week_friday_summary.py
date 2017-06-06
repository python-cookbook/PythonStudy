# Chapter 5. 파일과 입출력
#  5.1 텍스트 데이터 읽고 쓰기
#  ▣ 문제 : 텍스트 데이터를 읽거나 써야 하는데 ASCII, UTF-8, UTF-16 과 같이 서로 다른 인코딩을 사용해야 한다.
#  ▣ 해결 :
with open('files/somefile.txt', 'rt') as f:  # 파일 전체를 하나의 문자열로 읽음
    data = f.read()

with open('files/somefile.txt', 'rt') as f:  # 파일의 줄을 순환
    for line in f:
        print(line)

with open('files/somefile.txt', 'wt') as f:
    f.write('text1')
    f.write('text2')

with open('files/somefile.txt', 'wt') as f:
    print('text1', file=f)
    print('text2', file=f)
#   - 기본적으로 파일을 읽고 쓸 때 sys.getdefaultencoding() 으로 확인할 수 있는 시스템 기본 인코딩을 사용한다.

#  ▣ 토론 : 예제에서 사용한 with 문이 파일을 사용할 콘텍스트를 만든다.
#           컨트롤이 with 블록을 떠나면 파일이 자동으로 닫힌다.
#           with 문을 꼭 사용하지 않아도 되지만, 그럴 때는 반드시 파일을 닫아야 한다.
f = open('files/somefile.txt', 'rt')
data = f.read()
f.close()

with open('files/somefile.txt', 'rt', newline='') as f:  # 줄 바꿈 변환 없이 읽기
    f.read()

#   - 인코딩 에러가 나는 경우(errors 로 처리)
f = open('files/somefile.txt', 'rt', encoding='ascii', errors='replace')  # errors='replace' : 치환
f = open('files/somefile.txt', 'rt', encoding='ascii', errors='ignore')  # errors='ignore' : 무시


#  5.2 파일에 출력
#  ▣ 문제 : print() 함수의 결과를 파일에 출력하고 싶다.
#  ▣ 해결 : print() 에 file 키워드 인자를 사용한다.
with open('PythonCookBook/files/somefile.txt', 'wt') as f:
    print('Hello World!', file=f)

#  ▣ 토론 : 파일을 텍스트 모드로 열었는지 꼭 확인해야 한다.
#           바이너리 모드로 파일을 열면 출력에 실패한다.


#  5.3 구별자나 종단 부호 바꾸기
#  ▣ 문제 : print() 를 사용해 데이터를 출력할 때 구분자나 종단 부호를 바꾸고 싶다.
#  ▣ 해결 : print() 에 sep 과 end 키워드 인자를 사용한다.
print('ACME', 50, 91.5)
print('ACME', 50, 91.5, sep=',')
print('ACME', 50, 91.5, sep=',', end='!!\n')

#   - 출력의 개행 문자를 바꿀 때도 end 인자를 사용한다.
for i in range(5):
    print(i)

for i in range(5):
    print(i, end=' ')

#  ▣ 토론 : print() 로 출력 시 아이템을 구분하는 문자를 스페이스 공백문 이외로 바꾸는 가장 쉬운 방법은 구별자를 지정하는 것이다.
print(','.join(['ACME', '50', '91.5']))  # str.join() 은 문자열에만 동작한다는 문제점이 있다.

#   - 문자열이 아닌 데이터에 사용하는 경우
row = ('ACME', 50, 91.5)
print(','.join(row))
print(','.join(str(x) for x in row))
print(*row, sep=',')  # 구별자를 사용


#  5.4 바이너리 데이터 읽고 쓰기
#  ▣ 문제 : 이미지나 사운드 파일 등 바이너리 데이터를 읽고 써야 한다.
#  ▣ 해결 : open() 함수에 rb 와 wb 모드를 사용해서 바이너리 데이터를 읽거나 쓴다.
with open('files/somefile.bin', 'rb') as f:  # 파일 전체를 하나의 바이트 문자열로 읽기
    data = f.read()

with open('files/somefile.bin', 'wb') as f:
    f.write(b'Hello World')

#  ▣ 토론 : 바이너리 데이터를 읽을 때, 바이너리 문자열과 텍스트 문자열 사이에 미묘한 문법 차이가 있다.
#           데이터에 인덱스나 순환으로 반환한 값은 바이트 문자열이 아닌 정수 바이트 값이 된다.
#   - 텍스트 문자열
t = 'Hello World'
print(t[0])  # 문자

for c in t:
    print(c)

#   - 바이트 문자열
b = b'Hello World'
print(b[0])  # 정수 바이트

for c in b:
    print(c)

#   - 바이너리 모드 파일로부터 텍스트를 읽거나 쓰려면 인코딩이나 디코딩 과정이 필요하다.
with open('files/somefile.bin', 'rb') as f:
    data = f.read(16)
    text = data.decode('utf-8')  #

with open('files/somefile.bin', 'wb') as f:
    text = 'Hello World'
    f.write(text.encode('utf-8'))

#   - 배열이나 C 구조체와 같은 객체를 bytes 객체로 변환하지 않고 바로 사용
import array
nums = array.array('i', [1, 2, 3, 4])
with open('PythonCookBook/files/data.bin', 'wb') as f:
    f.write(nums)

import array
a = array.array('i', [0, 0, 0, 0, 0, 0, 0, 0])
with open('PythonCookBook/files/data.bin', 'rb') as f:
    print(f.readinto(a))
print(a)


#  5.5 존재하지 않는 파일에 쓰기
#  ▣ 문제 : 파일이 파일 시스템에 존재하지 않을 때, 데이터를 파일에 쓰고 싶다.
#  ▣ 해결 : open() 에 x 모드를 사용해서 해결할 수 있다. w 모드와 다르게 x 모드는 잘 알려져 있지 않다.
with open('files/somefile.txt', 'wt') as f:
    f.write('Hello\n')

try:
    with open('files/somefile.txt', 'xt') as f:  # 존재하면 write 가 안된다.
        f.write('Hello\n')
except Exception as e:
    print(e)

#  ▣ 토론 : 이 레시피는 파일을 쓸 때 발생할 수 있는 문제점(실수로 파일을 덮어쓰는 등)을 아주 우아하게 피해 가는 법을 알려준다.
#           혹은 파일을 쓰기 전에 파일이 있는지 확인하는 방법도 있다.
import os
if not os.path.exists('files/somefile.txt'):
    with open('files/somefile.txt', 'wt') as f:
        f.write('Hello\n')
else:
    print('File already exists!')


#  5.6 문자열에 입출력 작업하기
#  ▣ 문제 : 파일 같은 객체에 동작하도록 작성한 코드에 텍스트나 바이너리 문자열을 제공하고 싶다.
#  ▣ 해결 : io.StringIO() 와 io.BytesIO() 클래스로 문자열 데이터에 동작하는 파일 같은 객체를 생성한다.
import io
s = io.StringIO()
s.write('Hello World\n')
print('This is a test', file=s)
print(s.getvalue())  # 기록한 모든 데이터 얻기

s = io.StringIO('Hello\nWorld\n')
print(s.read(4))
print(s.read())

#   - io.StringIO() 클래스는 텍스트에만 사용해야 한다. 바이너리 데이터를 다룰 때는 io.BytesIO() 클래스를 사용한다.
s = io.BytesIO()
s.write(b'binary data')
print(s.getvalue())

#  ▣ 토론 : 일반 파일 기능을 흉내 내려 할 때 StringIO() 와 BytesIO() 클래스가 가장 유용하다.
#           예를 들어 유닛 테스트를 할 때, StringIO() 로 테스트 데이터를 담고 있는 객체를 만들어 일반 파일에 동작하는 함수에 사용할 수 있다.
#           StringIO 와 BytesIO 인스턴스가 올바른 정수 파일 디스크립터를 가지고 있지 않다는 점을 기억하자.
#           따라서 file, pipe, socket 등 실제 시스템 레벨 파일을 요구하는 코드에는 사용할 수 없다.


#  5.7 압축된 데이터 파일 읽고 쓰기
#  ▣ 문제 : gzip 이나 bz2 로 압축한 파일을 읽거나 써야 한다.
#  ▣ 해결 : gzip 과 bz2 모듈을 사용하면 간단히 해결 가능하다.
#           이 모듈은 open() 을 사용하는 구현법의 대안을 제공한다.
#   - gzip 압축 데이터 읽기
import gzip
with gzip.open('files/somefile.gz', 'rt') as f:
    text = f.read()

#   - bz2 압축 데이터 읽기
import bz2
with bz2.open('files/somefile.bz2', 'rt') as f:
    text = f.read()

#   - gzip 압축 데이터 쓰기
import gzip
with gzip.open('files/somefile.gz', 'wt') as f:
    f.write(text)

#   - bz2 압축 데이터 읽기
import bz2
with bz2.open('files/somefile.bz2', 'wt') as f:
    f.write(text)

#  ▣ 토론 : 압축한 데이터를 읽거나 쓰기가 어렵지는 않다. 하지만, 올바른 파일 모드를 선택하는 것은 상당히 중요하다.
#           모드를 명시하지 않으면 기본적으로 바이너리 모드가 된다.
#           gzip.open() 과 bz2.open() 은 encoding, errors, newline 과 같이 내장 함수 open() 과 동일한 인자를 받는다.
#           압축한 데이터를 쓸 때는 compresslevel 인자로 압축 정도를 지정할 수 있다.
#           기본 레벨은 9로, 가장 높은 압축률을 가리킨다. 레벨을 내리면 속도는 더 빠르지만 압축률은 떨어진다.

#   - gzip.open() 과 bz2.open() 을 기존에 열려 있는 바이너리 파일의 상위에 위치시킨다.
#     gzip 과 bz2 모듈이 파일 같은 객체와 같이 작업할 수 있다.
import gzip

f = open('files/somefile.gz', 'rb')
with gzip.open(f, 'rt') as g:
    text = g.read()


#  5.8 고정 크기 레코드 순환
#  ▣ 문제 : 파일을 줄 단위로 순환하지 않고, 크기를 지정해서 그 단위별로 순환하고 싶다.
#  ▣ 해결 : iter() 함수와 functools.partial() 을 사용한다.
from functools import partial
RECORD_SIZE = 32
with open('PythonCookBook/files/winter.txt', 'rt') as f:
    records = iter(partial(f.read, RECORD_SIZE), '')  # partial 함수를 통해 RECORD_SIZE 만큼 부분적으로 만든다음
    for r in records:
        print(r)

#  ▣ 토론 : iter() 함수에 잘 알려지지 않은 기능으로, 호출 가능 객체와 종료 값을 전달하면 이터레이터를 만드는 것이 있다.
#           그 이터레이터는 제공 받은 호출 가능 객체를 반복적으로 호출하며 종료 값을 반환할 때 순환을 멈춘다.
#           고정 크기 단위로 파일을 읽는 작업은 주로 바이너리 모드에서 사용한다.


#  5.9 바이너리 데이터를 수정 가능한 버퍼에 넣기
#  ▣ 문제 : 바이너리 데이터를 읽어 수정 가능 버퍼에 넣을 때 어떠한 복사 과정도 거치고 싶지 않다.
#           그리고 그 데이터를 변형한 후 파일에 다시 써야 할지도 모른다.
#  ▣ 해결 : 데이터를 읽어 수정 가능한 배열에 넣으려면 readinto() 메소드를 사용한다.
import os.path

def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return buf

with open('PythonCookBook/files/sample.bin', 'wb') as f:
    f.write(b'Hello World')

buf = read_into_buffer('PythonCookBook/files/sample.bin')
buf[0:5] = b'Hallo'
print(buf)

with open('PythonCookBook/files/newsample.bin', 'wb') as f:
    f.write(buf)

#  ▣ 토론 : readinto() 메소드를 사용해서 미리 할당해 놓은 배열에 데이터를 채워 넣을 수 있다.
#           이때 array 모듈이나 numpy 와 같은 라이브러리를 사용해서 생성한 배열을 사용할 수도 있다.
#           새로운 객체를 할당하고 반환하는 일반적인 read() 메소드와는 다르게 readinto() 메소드는 기존의 버퍼에 내용을 채워 넣는다.
#           따라서 불필요한 메모리 할당을 피할 수 있다. 예를 들어 레코드 크기가 고정적인 바이너리 파일을 읽는다면 다음과 같은 코드를 작성할 수 있다.
record_size = 32

buf = bytearray(record_size)
with open('PythonCookBook/files/sample.bin', 'rb') as f:
    while True:
        n = f.readinto(buf)
        print(buf)

        if n < record_size:
            break

#   - 기존 버퍼의 제로-카피 조각을 만들 수 있고 기존의 내용은 수정하지 않는 메모리뷰를 사용
print(buf)
m1 = memoryview(buf)
m2 = m1[-5:]
print(m2)
m2[:] = b'WORLD'
print(buf)
#   - f.readinto() 를 사용할 때 반환 코드를 반드시 확인해야 한다. 반환 코드는 실제로 읽은 바이트 수가 된다.
#     "into" 형식의 다른 함수에도 관심을 갖도록 하자.(recv_into(), pack_into() 등)
#     파이썬에는 readinto() 외에도 직접 입출력 혹은 배열, 버퍼를 채우거나 수정하는 데 사용할 수 있도록 데이터에 대한 접근을 지원하는 것이 많다.


#  5.10 바이너리 파일 메모리 매핑
#  ▣ 문제 : 바이너리 파일을 수정 가능한 바이트 배열에 매핑하고, 내용에 접근하거나 수정하고 싶다.
#  ▣ 해결 : mmap 모듈을 사용해서 파일을 메모리 매핑한다.
import os
import mmap

def memory_map(filename, access=mmap.ACCESS_WRITE):  # 이 함수를 사용하려면, 데이터로 채워진 파일이 있어야 한다.
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)

size = 1000000
with open('PythonCookBook/files/sample.bin', 'wb') as f:
    f.seek(size-1)
    f.write(b'\x00')

m = memory_map('PythonCookBook/files/sample.bin')  # memory_map() 함수로 메모리 매핑 수행
print(len(m))
print(m[0:10], m[0])
m[0:11] = b'Hello World'  # 슬라이스 재할당
m.close()

with open('PythonCookBook/files/sample.bin', 'rb') as f:
    print(f.read(11))

with memory_map('PythonCookBook/files/sample.bin') as m:  # 컨텍스트 매니저를 사용
    print(len(m))
    print(m[0:10])

m1 = memory_map('PythonCookBook/files/sample.bin', mmap.ACCESS_READ)  # 읽기 전용으로 파일 오픈
m2 = memory_map('PythonCookBook/files/sample.bin', mmap.ACCESS_COPY)  # 지역 레벨에서 수정하고, 원본에는 영향을 주고 싶지 않을 경우

#  ▣ 토론 : mmap 으로 파일을 메모리에 매핑하면 파일 내용에 매우 효율적으로 무작위로 접근할 수 있다.
#           예를 들어 파일을 열고 seek(), read(), write() 호출을 번갈아 가며 해야 할 일을 파일에 매핑해 놓고 자르기 연산으로 쉽게 해결할 수 있다.
m = memory_map('PythonCookBook/files/sample.bin')
v = memoryview(m).cast('I')  # unsigned integer 의 메모리뷰
v[0] = 7
print(m[0:4])
m[0:4] = b'\x07\x01\x00\x00'
print(v[0])


#  5.11 경로 다루기
#  ▣ 문제 : 기본 파일 이름, 디렉터리 이름, 절대 경로 등을 찾기 위해 경로를 다루어야 한다.
#  ▣ 해결 : 경로를 다루기 위해서 os.path 모듈의 함수를 사용한다. 몇몇 기능을 예제를 통해 살펴보자
import os
path = '/Users/beazley/Data/data.csv'
print(os.path.basename(path))  # 경로의 마지막 부분 구하기
print(os.path.dirname(path))  # 디렉터리 이름 구하기
print(os.path.join('tmp', 'data', os.path.basename(path)))  # 각 부분을 합치기
path = '~/Data/data.csv'
print(os.path.expanduser(path))  # 사용자의 홈 디렉토리 펼치기
print(os.path.splitext(path))  # 파일 확장자 나누기
print(os.path.split(path))  # 디렉토리와 파일 나누기

#  ▣ 토론 : 파일 이름을 다루기 위해서 문자열에 관련된 코드를 직접 작성하지 말고 os.path 모듈을 사용해야 한다.
#           os.path 모듈은 Unix 와 Windows 의 차이점을 알고 Data/data.csv 와 Data\data.csv 의 차이점을 자동으로 처리한다.


#  5.12 파일 존재 여부 확인
#  ▣ 문제 : 파일이나 디렉터리가 존재하는지 확인해야 한다.
#  ▣ 해결 : 파일이나 디렉터리의 존재 여부를 확인하기 위해서 os.path 모듈을 사용한다.
import os
print(os.path.exists('PythonCookBook/files/somefile.txt'))  # 파일 존재 여부
print(os.path.exists('PythonCookBook/files'))  # 디렉터리 존재 여부

#   - 파일의 종류가 무엇인지 확인
print(os.path.isfile('PythonCookBook/files/somefile.txt'))  # 일반 파일인지 확인
print(os.path.isdir('PythonCookBook/files/somefile.txt'))  # 디렉터리인지 확인
print(os.path.islink('PythonCookBook/files/somefile.txt'))  # 심볼릭 링크인지 확인
print(os.path.realpath('PythonCookBook/files/somefile.txt'))  # 절대 경로 얻기

#   - 메타데이터(파일 크기, 수정 날짜) 등이 필요할 때도 os.path 모듈을 사용한다.
print(os.path.getsize('PythonCookBook/files/somefile.txt'))  # 파일 크기
print(os.path.getmtime('PythonCookBook/files/somefile.txt'))  # 수정 날짜

import time
print(time.ctime(os.path.getmtime('PythonCookBook/files/somefile.txt')))

#  ▣ 토론 : os.path 를 사용하면 파일 테스팅은 그리 어렵지 않다. 유의해야 할 점은 아마도 파일 권한에 관련된 것뿐이다.


#  5.13 디렉터리 리스팅 구하기
#  ▣ 문제 : 디렉터리나 파일 시스템 내부의 파일 리스트를 구하고 싶다.
#  ▣ 해결 : os.listdir() 함수로 디렉터리 내에서 파일 리스트를 얻는다.
import os
names = os.listdir('PythonCookBook/files/')  # listdir() : 디렉터리 내에서 파일 리스트를 출력
print(names)

#   - 데이터를 걸러 내야 한다면 os.path 라이브러리의 파일에 리스트 컴프리헨션을 사용한다.
import os.path
names = [name for name in os.listdir('PythonCookBook/files/') if os.path.isfile(os.path.join('PythonCookBook/files/', name))]  # 일반 파일 모두 구하기
print(names)

dirnames = [name for name in os.listdir('PythonCookBook/') if os.path.isdir(os.path.join('PythonCookBook', name))]  # 디렉터리 모두 구하기
print(dirnames)

#   - 문자열의 startswith() 와 endswith() 메소드를 사용하면 디렉터리의 내용을 걸러 내기 유용하다.
pyfiles = [name for name in os.listdir('PythonCookBook/files/') if name.endswith('.py')]

#   - 파일 이름 매칭을 하기 위해 glob 이나 fnmatch 모듈을 사용한다.
import glob
binfiles = glob.glob('PythonCookBook/files/*.bin')
print(binfiles)

from fnmatch import fnmatch
pyfiles = [name for name in os.listdir('PythonCookBook/') if fnmatch(name, '*.py')]
print(pyfiles)