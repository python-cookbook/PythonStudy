'''
'''
'''

5장 1절 텍스트 데이터 읽고 쓰기 : 텍스트 데이터를 읽고 쓸 때 ASCII, UTF-8, UTF-16 등 서로 다른 인코딩을 사용해야 할 때 open() 함수에 rt 모드를 사용한다.

- open() :  파일 객체 = open(파일 이름, 파일 열기 모드)
    r	읽기모드 - 파일을 읽기만 할 때 사용
    w	쓰기모드 - 파일에 내용을 쓸 때 사용
    a	추가모드 - 파일의 마지막에 새로운 내용을 추가 시킬 때 사용

    파일을 읽고 쓸 때 sys.getdefaultencoding() 으로 파일의 인코딩이 어떻게 되어있나 확인 할 수 있다. 대부분 UTF-8로 인코딩 되어 있지만 다를경우 인코딩 옵션을 지정해준다.
    ex) with open('somefile.txt', 'rt', encoding='latin-1') as f:
    
    UTF-8이 기본적으로 안전한 방식이고 ascii는 U+0000에서 U+007F 까지 7비트 문자에 일치한다. 
    
    아래 예제에서 사용한 with문은 파일을 사용할 콘텍스트를 만드는데 컨트롤이 with 블록을 떠나면 파일이 자동으로 닫힌다. with문을 사용하지 않는 경우 파일을 수동으로 닫아야한다.
    ex) f.open('somefile.txt', 'rt')
        data = f.read()
        f.close()
        
        
 유닉스와 윈도우에선 \n과 \r\n은 기본적으로 줄바꿈을 의미한다.



'''

# 예1.
with open('somefile.txt', 'rt') as f:
    data = f.read()

with open('somefile.txt', 'rt') as f:
    for line in f:
        ...


# 예2.
with open('somefile.txt', 'wt') as f:
    f.write(text1)
    f.write(text2)

# 예3.
f = open('hello.txt', 'rt')
f.read()
# 'hello world!\n

f = open('hello.txt', 'rt', newline='')
f.read()
# 'hello world!\r\n

'''

5장 2절 파일에 출력 : print() 결과를 파일에 출력하고 싶으면 file 키워드 인자를 사용한다.



'''

# 예4.
with open('somefile.txt', 'rt') as f:
    print('Hello World!', file=f)

'''

5장 3절 구별자나 종단 부호 바꾸기 : print()를 사용해 데이터를 출력할 때 구분자나 종단 부호(문장 끝맺음 부호)를 바꾸고 싶은 경우 print()에 sep나 end 키워드를 사용한다.


'''

# 예5.
print('ACME', 50, 91.5)
# ACME 50 91.5
print('ACME', 50, 91.5, sep=',')
# ACME,50,91.5
print('ACME', 50, 91.5, sep=',', end='!!\n')
# ACME,50,91.5!!
#

'''

5.4 바이너리 데이터 읽고 쓰기 : 이미지나 사운드 파일 등 바이너리 데이터를 읽고 써야하는 경우 open() 함수에 rb와 wb 모드를 사용한다.

- 바이너리를 읽을 때 반환된 모든 데이터가 텍스트 문자열이 아니라 바이트 문자열이 된다. 데이터를 쓸 때도 바이트로 표현되는 객체를 사용해야 한다(bytearray 등)
- 바이너리 모드 파일로부터 텍스트를 읽거나 쓰려면 인코딩/디코딩이 꼭 필요하다.
- 버퍼 인터페이스로 구현된 객체는 모두 기반 메모리버퍼를 작업에 노출시켜 작업이 가능한데 각각의 구현법이 플랫폼에 따라 다르거나 
  단어의 크기와 바이트 순서에 의존하기 때문에 주의해야 한다.
  
  * 엔디안
  
  엔디언(Endianness)은 컴퓨터의 메모리와 같은 1차원의 공간에 여러 개의 연속된 대상을 배열하는 방법을 뜻하며, 
  바이트를 배열하는 방법을 특히 바이트 순서(Byte order)라 한다.
  엔디언은 보통 큰 단위가 앞에 나오는 빅 엔디언(Big-endian)과 작은 단위가 앞에 나오는 리틀 엔디언(Little-endian)으로 나눌 수 있으며, 
  두 경우에 속하지 않거나 둘을 모두 지원하는 것을 미들 엔디언(Middle-endian)이라 부르기도 한다.
  빅 엔디언은 사람이 숫자를 쓰는 방법과 같이 큰 단위의 바이트가 앞에 오는 방법이고, 리틀 엔디언은 반대로 작은 단위의 바이트가 앞에 오는 방법이다.
  
  빅 엔디언은 소프트웨어의 디버그를 편하게 해 주는 경향이 있다. 사람이 숫자를 읽고 쓰는 방법과 같기 때문에 디버깅 과정에서 메모리의 값을 보기 편한데, 
  예를 들어 0x59654148은 빅 엔디언으로 59 65 41 48로 표현된다.
  
  리틀 엔디언은 메모리에 저장된 값의 하위 바이트들만 사용할 때 별도의 계산이 필요 없다는 장점이 있다. 
  예를 들어, 32비트 숫자인 0x2A는 리틀 엔디언으로 표현하면 2A 00 00 00이 되는데, 
  이 표현에서 앞의 두 바이트 또는 한 바이트만 떼어 내면 하위 16비트 또는 8비트를 바로 얻을 수 있다. 
  반면 32비트 빅 엔디언 환경에서는 하위 16비트나 8비트 값을 얻기 위해서는 변수 주소에 2바이트 또는 3바이트를 더해야 한다. 
  보통 변수의 첫 바이트를 그 변수의 주소로 삼기 때문에 이런 성질은 종종 프로그래밍을 편하게 하는 반면, 
  리틀 엔디언 환경의 프로그래머가 빅 엔디언 환경에서 종종 실수를 일으키는 한 이유이기도 하다.
  또한 가산기가 덧셈을 하는 과정은 LSB로부터 시작하여 자리 올림을 계산해야 하므로, 첫 번째 바이트가 LSB인 리틀 엔디언에서는 가산기 설계가 조금 더 단순해진다. 
  빅 엔디언에서는 가산기가 덧셈을 할때 마지막 바이트로부터 시작하여 첫 번째 바이트까지 역방향으로 진행해야 한다. 
  그러나 오늘날의 프로세서는 여러개의 바이트를 동시에 읽어들여 동시에 덧셈을 수행하는 구조를 갖고 있어 두 엔디언 사이에 사실상 차이가 없다.
  
  
  * 파이썬에서 빅엔디안, 리틀엔디안
        Little Endian
            struct.pack('<L',0x41424344)
            'DCBA'
        
        Big Endian
            struct.pack('>L',0x41424344)
            'ABCD'



'''

# 예6.
with open('somefile.bin', 'rb') as f:
    data = f.read(16)
    text = data.decode('UTF-8')

with open('somefile.bin', 'wb') as f:
    text = 'hello world'
    f.write(text.encode('UTF-8'))


'''

5.5 존재하지 않는 파일에 쓰기 : 파일이 파일 시스템에 존재하지 않는 경우 데이터를 파일에 쓸 때 open() 함수에 x 모드를 사용한다.



'''

# 예7.
with open('somefile', 'xt') as f:
    f.write('Hello\n')


'''

5장 6절 문자열에 입출력 작업하기 : 파일같은 객체에 동작하도록 작성한 코드에 텍스트나 바이너리 문자열을 지공하고 싶을 경우 io.StringIO()나 io.BytesIO() 클래스를 사용한다.



'''

# 예8.
s = io.StringIO()
s.write('Hello World\n')
# 12
print('This is a test', file=s)
# 15

'''

5장 7절 압축된 데이터 파일 읽고 쓰기 : gzip이나 bz2로 압축한 파일을 읽거나 써야 하는 경우 gzip, bz2 모듈을 사용한다.

'''


'''

5장 8절 : 고정 크기 레코드 순환 : 파일을 줄 단위로 순환하지 않고 크기를 지정해서 크기 단위 별로 순환하고 싶은 경우 iter() 함수와 functools.partial() 메소드를 사용한다.


- iter() 함수는 호출 가능 객체와 종료 값을 전달하면 이터레이터를 만들어 준다. 이렇게 생성한 이터레이터는 제공 받은 호출 가능 객체를 반복적으로 호출하며 종료 값을 반환하면
  순환을 멈춘다. 아래 예제에선 functools.partial로 고정 크기 바이트를 읽어 호출 가능 객체를 생성해서 파일을 읽고 마지막에 도달하면 b''를 반환한다.


'''

# 예9.
from functools import partial
RECORD_SIZE = 32
with open('somefile.data', 'rb') as f:
    records = iter(partial(f.read, RECORD_SIZE), b'')
    for r in records:
        ...


'''

5장 9절 바이너리 데이터를 수정 가능한 버퍼에 넣기 : 바이너리 데이터를 읽어 수정 가능 버퍼에 넣을 때 어떠한 복사 과정도 거치고 싶지 않은 경우 수정가능한 배열에 넣으려면
                                             readinto() 메소드를 사용한다.

- readinto() 메소드를 사용해서 미리 할당해 놓은 배열에 데이터를 채워 넣을 수 있는데 array 모듈이나 numpy와 같은 라이브러리로 생성한 배열도 사용할 수 있다.
  read() 메소드완 다르게 readinto() 메소드는 기존의 버퍼에 내용을 채워 넣는다. 따라서 불 필요한 메모리 할당을 피할 수 있다.

'''

# 예10.
import os.path

def read_into_buffer(filename):     # 데이터를 읽어 수정 가능한 배열에 넣는 함수
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return buf

with open('sample.bin', 'wb') as f:
    f.write(b'Hello World')


buf = read_into_buffer('sample.bin')
buf
# bytearray(b'Hello World')
buf[0:5] = b'Hallo'
buf
# bytearray(b'Hallo World')


# 예11.
buf
# bytearray(b'Hallo World')
m1 = memoryview(buf)
m2 = m1[-5:]
m2
# <memory at 0x100681390>
m2[:] = b'WORLD'
buf
# bytearray(b'Hallo WORLD')


'''

5장 10절 바이너리 파일 메모리 매핑 : 바이너리 파일을 수정 가능한 바이트 배열에 매핑하고 내용에 접근하거나 수정하고 싶은 경우 mmap 모듈을 사용해서 파일을 메모리매핑한다.

- 메모리 매핑 


'''

# 예12.
import os
import mmap

def memory_map(filename, access=mmap.ACCESS_WRITE):     # mmap 모듈을 사용해서 파일을 열고 메모리 매핑하는 함수
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)

m = memory_map('data')

'''

5장 11절 경로 다루기 : 기본 파일 이름, 디렉토리 이름, 절대 경로 등을 찾기 위해 경로가 필요한 경우 os.path 모듈의 함수를 사용한다.

.basename() : 경로의 마지막 부분
.dirname() : 디렉토리 이름
.join() : 각 부분을 합치는 것
.expanduser() : 홈 디렉토리 펼치기
.splitext() : 파일 확장자 나누기


'''

'''

5장 12절 파일 존재 여부 확인 : 파일이나 디렉토리가 존재하는지 확인해야 하는 경우 os.path모듈을 사용한다.

.exists() : 디렉토리 존재 여부 확인
.isfile() : 디렉토리 인지 확인
.islink() : 심볼릭 링크인지 확인
.realpath() : 연결된 파일 얻기
.getsize() : 메타데이터(파일크기, 수정날짜) 를 확인



'''

'''

5장 13절 디렉토리나 파일 시스템 내부의 파일 리스트를 구하고 싶은 경우 os.listdir() 함수로 디렉토리 내에서 파일 리스트를 얻는다.

- 데이터를 걸러 내야 한다면 os.path 라이브러리의 파일에 리스트 컴프리헨션을 사용한다.

'''

import os.path
import os
import glob


names = [name for name in os.listdir('somedir') if os.path.isfile(os.path.join('somedir', name))]   # 일반파일 모두 구하기
dirnames = [name for name in os.listdir('somedir') if os.path.isdir(os.path.join('somedir', name))]   # 디렉토리 모두 구하기

pyfiles = glob.glob('*.py')

name_sz_date = [(name, os.path.getsize(name), os.path.getmtime(name)) for name in pyfiles]

for name, size, mtime in name_sz_date:
    print(name, size, mtime)

