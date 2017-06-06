

################################################################
# 5장. 파일과 입출력
################################################################


# 모든 프로그램은 입력과 출력을 필요로 한다. 이번 장은 여러 종류의 파일(텍스트, 바이너리, 파일 인코딩 등)을 다루는 일반적인 방법을 다룬다.
# 또한 파일 이름과 디렉토리를 수정하는 방법도 배운다.




########## 5.1. 텍스트 데이터 일고 쓰기 ##########

# 문제- 텍스트 데이터를 읽거나 써야 하는데 ASCII, UTF-8, UTF-16 과 같이 서로 다른 인코딩을 사용해야 한다.

# 해결 - 텍스트 파일을 읽기 위해 OPEN() 함수에 rt 모드를 사용한다.



# 파일전체를 하나의 문자열로 읽음
with open('sonefile.txt', 'rt') as f:
    data = f.read()

# 파일의 줄을 순환
with open('some file', 'rt') as f:
    for line in f:
        #라인처리
        ...


#마찬가지로 텍스트 파일을 쓰려면 wt 모드를 사용한다. 이 모드를 사용하면 모든 내용을 지우고 (혹시 있다면) 새로운 내용을 덮어쓴다.

#텍스트 데이터 쓰기
with open('somefile', 'wt') as f:
    f.write(text1)
    f.write(text2)


# 리다이렉트한 print 문
with open('somefile', 'wt') as f:
    print(line1, file=f)
    print(line2, file=f)
    ...

# 파일의 끝에 내용을 추가하려면 at 모드로 open()을 사용한다
# 기본적으로 파일을 읽고 쓸때 sys.getdefaulttencoding()으로 확인할 수 있는 시스템 기본 인코딩을 사용한다.
# 대부분의 컴퓨터는 이 기본 인코딩으로 utf-8을 사용한다.
# 만일 읽고쓸 텍스트가 다른 인코딩을 사용한다면 open()에 추가적인 encoding 인자를 전달한다.

# 파이썬이 이해할 수 있는 인코딩의 종류는 수백가지에 이른다. 하지만 일반적으로 사용하는 인코딩은
# latin-1, ASCII, UTF-8, UTF-16 이다.


# 토론

# 텍스트 파일을 읽고 쓴느 과정에서 주의해야 할 점

# 예제에서 사용한 with문이 파일을 사용할 콘텍스트를 만든다. 컨트롤이 with 블록을 떠나면 파일이 자동으로 닫힌다.
# with문을 꼭 사용하지 않아도 되지만, 그럴 때느 ㄴ반드시 파일을 닫아얗 ㅏㄴ다.


f = open('somefile.txt', 'rt')
data = f.read()
f.close()


# 그리고 Unix 와 Windows 에서 서로 다른 줄바꿈 문자에 주의해야 한다(\n 과 \r\n)
# 기본적으로 파이썬은 보편적 줄바꿈 모드로 동작한다. 일반적인 모든 줄바꿈을 알아보고, 읽을 때 모든 줄바꿈 문자를 \n으로 변환한다.
# 그리고 출력시에는 줄바꿈 문자 \n을 시스템 기본 문자로 변환한다.
# 이런 자동 변환을 원하지 않을 때는 newline ='' 인자를 open() 에 넣어준다.

# 줄바꿈 변환없이 읽기
with open('somefile.txt', 'rt'. newline ='') as f:
    ...

# 차이점을 보기 위해 Unix 컴퓨터에서 Windows 형식으로 인코딩된 텍스트 파일을 읽어보겠다.


# 줄바꿈 변환 사용(기본)
f = open('hello.txt', 'rt')
f.read()
# 'hello owrld!\n'

# 줄바꿈 변환 미사용
g = open('hello.txt', 'rt')
g.read()
# 'hello owrld!\r\n'


# 마지막으로, 텍스트 파일의 인코딩 에러를 조심해야 한다. 텍스트 파일을 읽거나 쓸 때, 인코딩이나 디코딩에러가 발생할 수 있다.


f = open('sample.txt', 'rt', encoding='ascii')
f.read()

# 에러 발생!!!  -> 잘못된 인코딩을 사용했을 때





########## 5.2. 파일에 출력 ##########


# 문제 - print() 함수의 결과를 파일에 출력하고 싶다

# 해결 - print() 에 file 키워드 인자를 사용한다.

with open('somefile.txt', 'rt') as f:
    print('hello world!', file=f)

# 토론
# 파일에 출력하기에서 이 이상의 내용은 없다. 하지만 파일을 텍스트 모드로 열었는지 꼭 확인해야...
# 바이너리 모드로 파일을 열면 출력에 실패한다



########## 5.3. 구별자나 종단 부호 바꾸기 ##########

# 문제 - print() 를 사용해 데이터를 출력할 때 구분자나 종단 부호(line ending)을 바꾸고 싶다.

# 해결 - print()에 sep와 end 키워드 인자를 사용한다.

print('ACME', 50, 91.5)
#ACME 50 91.5

print('ACME', 50, 91.5, sep=',')
#ACME,50,91.5

print('ACME', 50, 91.5, sep=',', end='!!\n')
#ACME,50,91.5!!


# 출력의 개행문자(NEWLINE)을 바꿀 때도 end 인자를 사용한다.

for i in range(5):
    print(i)
# 0
# 1
# 2
# 3
# 4

for i in range(5):
    print(i, end= ' ')
    # 0 1 2 3 4

# 토론

# print() 로 출력 시 아이템을 구분하는 문자를 스페이스 공백문 이외로 바꾸는 가장 쉬운 방법은 구별자를 지정하는 것이다.
# str.join() 을 사용해도 된다.

print(','.join('ACME', '50', '91.5'))
#ACME,50,91.5
# 위의 결과가 나와야하는데 에러남....

# str.join()은 문자열에만 동작한다는 문제가 있다.
# 문자열이 아닌 데이터에 적용하려면 복잡하고 귀찮은 작업을 거쳐야 한다.

row = ('ACME', 50, 91.5)
print(','.join(row))
# Traceback (most recent call last):
#     File "<stdin>", line 1, in <module>
# TypeError: sequence item 1: expected str instance, int found
print(','.join(str(x) for x in row))
# ACME,50,91.5


# 구분자를 사용하면 훨씬 간단하다.

print(*row, sep=',')
#ACME,50,91.5




########## 5.4. 바이너리 데이터 읽고 쓰기 ##########

# 문제 - 이미지나 사운드 파일 등 바이너리 데이터를 읽고 써야 한다.

# 해결 - open() 함수에 rb 와 wb모드를 사용해서 바이너리 데이터를 읽거나 쓴다.


# 파일 전체를 하나의 바이트 문자열로 읽기
with open('somefile.bin', 'rb') as f:
    data = f.read()

with open('somefile.bin', 'wb') as f:
    f.write(b'Hello World')

# 바이너리를 읽을 때, 반환된 모든 데이터가 텍스트 문자열 형식이 아니라 바이트 문자열 형식이 된다는 점을 기억하자.
# 마찬가지로 데이터를 쓸 때도 바이트로 표현할 수 있는 형식의 객체를 제공해야 한다.(바이트 문자열, bytearray 객체 등)

# 토론
# 바이너리 데이터를 읽을 때, 바이너리 문자열과 텍스트 문자열 사이에 미묘한 문법 차이가 있다.
# 자세히 말하면, 데이터에 인덱스나 순환으로 반환한 값은 바이트 문자열이 아닌 정수 바이트 값이 된다.


# 텍스트 문자열
t = 'Hello World'
t[0]
#'H'

for c in t:
    print(c)
# H
# e
# l
# l
# o
#
# W
# o
# r
# l
# d

# 바이트 문자열
b = b'Hello World'
b[0]
#72

for c in b:
    print(c)
# 72
# 101
# 108
# 108
# 111
# 32
# 87
# 111
# 114
# 108
# 100


# 바이너리 모드 파일로부터 텍스트를 읽거나 쓰려면 인코딩이나 디코딩 과정이 꼭 필요하다.

with open('somefile.bin', 'rb') as f:
    data = f.read(16)
    text = data.decode('utf-8')

with open('somefile.bin', 'wb') as f:
    text = 'Hello World'
    f.write(text.encode('utf-8'))


# 바이너리 입출력 시 잘 알려지지 않은 기능으로 배열이나 c 구조체와 같은 객체를 bytes 객체로 변환하지 않고 바로 쓸 수 있다는 점이 있다.

import array
nums = array.array('i', [1,2,3,4])
with open('data.bin', 'wb') as f:
    f.write(nums)


# 이 기능은 소위 버퍼 인터페이스 로 구현되어 있는 객체에 모두 적용된다.
# 이런 객체는 기반 메모리 버퍼를 바로 작업에 노출시켜 작업이 가능하다. 바이너리 데이터를 쓰는 것도 이런 작업의 일종이다.

# 또한 파일의 readinto() 메소드를 사용하면 여러 객체의 바이너리 데이터를 직접 메모리에 읽어 들일 수 있다.

import array
a = array.array('i', [0, 0, 0, 0, 0, 0, 0, 0])
with open('data.bin', 'rb') as f:
    f.readinto(a)
...
#16
a
#array('i', [1, 2, 3, 4, 0, 0, 0, 0])

# 이 기법을 쓸 때는 구현법이 플랫폼에 따라 다르기도 하고 단어의 크기와 바이트 순서 등에 의해 좌우되기 때문에 주의해야 함.




########## 5.5 존재하지 않는 파일에 쓰기 ##########

# 문제
# 파일이 파일 시스템에 존재하지 않을 때, 데이터를 파일에 쓰고 싶다.

# 해결
# 이 문제는 open()에 x 모드를 사용해서 해결할 수 있다. w 모드와 다르게 x 모드느 잘 알려져 있지 않다.

with open('somefile', 'wt') as f:
    f.write('Hello\n')

with open('somefile', 'xt') as f:
    f.write('Hello\n')

# Traceback (most recent call last):
# File "<stdin>", line 1, in <module>
# FileExistsError: [Errno 17] File exists: 'somefile'

# 파일이 바이너리 모드이면 xt 대신 xb를 사용한다.


# 토론
# 이 레시피는 파일을 쓸 때 발생할 수 있는 문제점(실수로 파일을 덮어쓰는 등)을 아주 유용하게 피해 가는 법을 알려준다.
# 혹은 파일을 쓰기 전에 파일이 있는지 확인하는 방법도 있다.

import os
if not os.path.exists('somefile'):
    with open('somefile', 'wt') as f:
        f.write('Hello\n')
else:
    print('File already exists!')

#확실히 x 모드를 사용하는 것이 더 깔끔하다. 그리고 x 모드는 파이썬 3의 확장 기능이므로 이전 버전에 없당





########## 5.6. 문자열에 입출력 작업하기 ##########

# 문제 - 파일같은 객체에 동작하도록 작성한 코드에 텍스트나 바이너리 문자열을 제공하고 싶다면??

# 해결
# io.StringIO() 와 io.BytesIO() 클래스로 문자열 데이터에 동작하는 파일 같은 객체를 생성한다.
import io  # io를 import 해주어야!!

s = io.StringIO()
s.write('Hello World\n')
# 12

print('This is a test', file=s)
# 15가 나와야 하는데 아무것도 안나옴.....ㅋㅋㅋㅋ

# 기록한 모든 데이터 얻기
s.getvalue()
##'Hello World\nThis is a test\n'

# 기존 문자열을 파일 인터페이스로 감싸기
s = io.StringIO('Hello\nWorld\n')
s.read(4)
#'Hell'
s.read()
#'o\nWorld\n'

# io.StringIO() 클래스는 텍스트에만 사용해야 함.
# 바이너리 데이터를 다룰 때는  io.BytesIO() 클래스를 사용한다.

s = io.BytesIO()
s.write(b'binary data')
s.getvalue()
#b'binary data'


# 토론
# 일반 파일 기능을 흉내내려 할 때 StringIO() 와 BytesIO 클래스가 유용함.
# 예를 들어 유닛 테스트를 할 때 StringIO로 테스트 데이터를 담고 있는 객체를 만들어 일반 파일에 동작하는 함수에 사용할 수 있다.
# io.StringIO와 io.BytesIO 인스턴스가 올바른 정수 파일 디스크립터를 가지고 있지 않다는 점을 기억하자.
# 따라서  file, pipe, socket 등 실제 시스템 레벨 파일을 요구하는 코드에는 사용할 수 없다.





########## 5.7. 압출된 데이터 파일 읽고 쓰기 ##########


# 문제 - gzip 이나 bz2 로 압축한 파일을 읽거나 써야 한다면???

# 해결
# gzip 과 bz2 모듈을 사용하면 간단히 해결 가능하다. 이 모듈은 open() 을 사용하는 구현법의 대안을 제공한다.
# 예를 들어 압축된 파일을 텍스트로 읽으려면 다음과 같이 한다.

# gzip 압축
import gzip
with gzip.open('somefile.gz', 'rt') as f:
    text = f.read()

# bz2 압축
import bz2
with bz2.open('somefile.bz2', 'rt') as f:
    text = f.read()


# 압축한 데이터를 쓰는 방법은 다음과 같다.

# gzip 압축
import gzip
with gzip.open('somefile.gz', 'wt') as f:
    f.write(text)

# bz2 압축
import bz2
with bz2.open('somefile.bz2', 'wt') as f:
    f.write(text)

# 앞에서 살펴본 대로, 모든 입출력은 텍스트를 사용하고 유니코드 인코딩/디코딩을 수행한다.
# 바이너리 데이터를 사용하고 싶다면 rb 또는 wb 모드를 사용하도록 하자.



# 토론
# 압축한 데이터를 읽거나 쓰기가 어렵지는 않다. 하지만 올바른 파일 모드를 선택하는 것이 상당히 중요하다
# 모드를 명시하지 않으면 기본적으로 바이너리 모드가 된다.
# 텍스트 파일을 받을 것이라 가정한 프로그램에서는 문제가 발생하겠지....
# gzip.open() 과 bz2.open()은 encoding, error, newline 과 같이 내장 함수 open() 과 동일한 인자를 받는다.

with gzip.open('somefile.gz', 'wt', compresslevel=5) as f:
    f.write(text)

# 기본 레벨은 9로, 가장 높은 압축률을 가리킨다. 레벨을 내리면 속도는 더 빠르지만 압축률은 떨어진다.

# 마지막으로, 잘 알려지지 않은 기능인 gzip.open() 과 bz2.open()을 기존에 열려 있는 바이너리 파일의 상위에 위치시키는 코드를 보자

import gzip
f = open('somefile.gz', 'rb')
with gzip.open(f, 'rt') as g:
    text = g.read()

# 위와 같이 하면, gzip 과 bz2 모듈이 파일 같은 객체(메모리파일, pipe, socket) 와 같이 작업할 수 있다.







########## 5.8. 고정 크기 레코드 순환 ##########

# 파일을 줄 단위로 순환하지 않고, 크기를 지정해서 그 단위별로 순환하고 싶다.

# 해결
# iter() 함수와 functools.partial() 을 사용한다.

from functools import partial

RECORD_SIZE = 32

with open('somefile.data', 'rb') as f:
    records = iter(partial(f.read, RECORD_SIZE), b'')
    for r in records:
        ...

# 이 예제의 records 객체는 파일의 마지막에 도달할 때까지 고정 크기 데이터를 생성하는 순환 객체이다.
# 하지만 파일의 크기가 지정한 크기의 정확한 배수가 아닐 경우 마지막 아이템의 크기가 예상보다 작을 수 있다.


# 토론
# iter() 함수의 잘 알려지지 않은 기능으로, 호출 가능 객체와 종료 값을 전달하면 이터레이터를 만드는 것이 있다.
# 제공받는 호출 가능 객체를 반복적으로 호출하며 종료 값을 반환할 때 순환을 멈춘다.
# 위 예제에서 파일을 바이너리 모드로 열었음에 주목하자. 고정 크기 레코드를 읽기 위해서 이것이 가장 일반적이다.
# 텍스트 파일의 경우는 줄 단위로 읽는 경우가 더 많다.






########## 5. 9. 바이너리 데이터를 수정 가능한 버퍼에 넣기 ##########

# 문제
# 바이너리 데이터를 읽어 수정가능 버퍼(mutable buffer)에 넣을 때 어떠한 복사 과정도 거치고 싶지 않다면???
# 그리고 그 데이터를 변형한 후 다시 파일에 써야 할지도 모른다

# 해결
# 데이터를 읽어 수정 가능한 배열에 넣으려면 readinto() 메소드를 사용한다.

import os.path

def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return buf

# 사용법은 다음과 같다.

# 샘플 파일 쓰기
with open('sample.bin', 'wb') as f:
    f.write(b'Hello World')

buf = read_into_buffer('sample.bin')
buf
#bytearray(b'Hello World')

buf[0:5] = b'Hallo'
buf
#bytearray(b'Hallo World')
with open('newsample.bin', 'wb') as f:
    f.write(buf)

#11


# 토론

# readinto() 객체를 사용해서 미리 할당해 놓은 배열에 데이터를 채워 놓을 수 있다.
# 이 때 array 모듈이나 numpy 와 같은 라이브러리를 사용해서 생성한 배열을 사용할 수도 있다.
# 새로운 객체를 할당하고 반환하는 일반적인 read() 메소드와 다르게 readinto() 메소드는 기존의 버퍼에 내용을 채워넣는다.
# 따라서 불필요한 메모리 할당을 피할 수 있다.
# 예를 들어 레코드 크기가 고정적인 바이너리 파일을 읽는다면 다음과 같은 코드를 작성할 수 있다.

record_size = 32 # Size of each record (adjust value)

buf = bytearray(record_size)
with open('somefile', 'rb') as f:
    while True:
        n = f.readinto(buf)
        if n < record_size:
            break
        # buf 내용을 사용
        ...

#f.readinto() 를 사용할 때 반환 코드를 반드시 확인하자!!!\
# 반환 코드는 실제로 읽은 바이트 수가 된다.
# 바이트 수가 제시한 버퍼의 크기보다 ㅈ가다면 데이터에 이상이 있거나 무언가 잘려 나갔음을 의미한다.




########## 5.10 바이너리 파일 메모리 매핑 ##########

# 문제 - 바이너리 파일ㅇ르 수정가능한 바이트 배열에 매핑하고, 내용에 접근하거나 수정하고 싶다.

# 해결
# mmap 모듈을 사용해서 파일을 매모리 매핑한다. 파일을 열고 메모리 매핑하는 예를 참고하자.

import os
import mmap

def memory_map(filename, access=mmap.ACCESS_WRITE):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)


# 이 함수를 사용하려면, 데이터로 채워진 파일이 있어야한다. 파일을 생성하고 원하는 크기로 확장하는 예는 다음과 같다.


size = 1000000
with open('data', 'wb') as f:
    f.seek(size-1)
    f.write(b'\x00')


# 이제 memory_map() 함수로 파일을 메모리 매핑해보자.

m = memory_map('data')
len(m)
#1000000
m[0:10]
#b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
m[0]
#0
# 슬라이스 재할당
m[0:11] = b'Hello World'
m.close()

# 수정 검증
with open('data', 'rb') as f:
    print(f.read(11))

#b'Hello World'


#map() 에 반환한 mmap 객체를 콘텍스트 매니저로 사용할 수 있다.
# 그렇게 하면 파일 사용이 끝나면 자동으로 닫는다.


with memory_map('data') as m:
    print(len(m)) #1000000
    print(m[0:10]) #b'Hello Worl'

m.closed
# True

# 기본적으로 memory_map() 함수는 파일을 읽기/쓰기 모드로 열고, 데이터 수정을 하면 모두 원본 파일에 복사된다.
# 이렇게 하지 않고 읽기 전용으로 파일을 열고 싶으면 mmap.ACCESS_READ를 access 인자에 전달한다.
m = memory_map(filename, mmap.ACCESS_READ)

# 데이터를 지역 레벨에서 수정하고, 원복에는 영향을 주고 싶지 않다면 mmap.ACCESS_COPY 를 사용한다.
m = memory_map(filename, mmap.ACCESS_COPY)


# 토론
# mmap 으로 파일을 메모리에 매핑하면 파일 내용에 매우 효율적으로 무작위로 접근할 수 있다.
# 예를 들어 파일을 열고 seek(), read(), write() 호출을 번갈아 하며 해야 할 일을 파일에 매핑해 놓고 자르기 연산으로 쉽게 해결할 수 있당
# 일반적으로 mmap 메모리에 노출된 메모리는 bytearray 객체처럼 보인다. 하지만, 메모리뷰를 사용해서 데이터를 다르게 해석할 수 있다.

m = memory_map('data')
# 부호 없는 정수형의 메모리뷰
v = memoryview(m).cast('I')
v[0] = 7
m[0:4]
#b'\x07\x00\x00\x00'
m[0:4] = b'\x07\x01\x00\x00'
v[0]
#263




########## 5. 11. 경로 다루기 ##########


# 문제
# 기본 파일 이름, 디렉토리 이름, 절대 경로 등을 찾기 위해 경로를 다루어야 한다.

# 해결
# 경로를 다루기 위해서 os.path 모듈의 함수를 사용한다.

import os
path = '/Users/beazley/Data/data.csv'

# 경로의 마지막 부분 구하기
os.path.basename(path)
#'data.csv'

# 디렉토리 이름 구하기
os.path.dirname(path)
#'/Users/beazley/Data'

# 각 부분을 합치기
os.path.join('tmp', 'data', os.path.basename(path))
#'tmp/data/data.csv'

# 사용자의 홈 디렉토리 펼치기
path = '~/Data/data.csv'
os.path.expanduser(path)
#'/Users/beazley/Data/data.csv'

# 파일 확장자 나누기
os.path.splitext(path)
#('~/Data/data', '.csv')


# 토론
# 파일 이름을 다루기 위해서 문자열에 관련된 코드를 직접 작성하지 ㅁ라고
# os.path 모듈을 사용해야 한다.




########## 5. 12. 파일 존재 여부 확인 ##########

# 문제 - 파일이나 디렉토리가 존재하는지 확인해야 한다.

# 해결 - os.path 모듈을 사용한다.

import os
os.path.exists('/etc/passwd')
# True

import os
os.path.exists('/temp/spam')
#False

#추가적으로 파일의 종류가 무엇인지 확인할 수도 있다. 파일이 없는 경우  false 를 반환한다.

# 일반 파일인지 확인
os.path.isfile('/etc/passwd')
# True

#디렉토리인지 확인
os.path.isdir('/etc/passwd')
#False

#심볼릭 링크인지 확인
os.path.islink('/usr/local/bin/python3')
# True

# 연결된 파일 얻기
os.path.realpath('/usr/local/bin/python3')
# /usr/local/bin/python3.3



# 메타 데이터(파일 크기, 수정 날짜) 등이 필요한 때도 os.path를 사용한다.

os.path.getsize('/etc/passwd')
#3669
os.path.getmtime('/etc/passwd')
#1272478234.0

import time
time.ctime(os.path.getmtime('/etc/passwd'))
#'Wed Apr 28 13:10:34 2010'


# 특히 메타데이터에 접근할 때는 권한에 주의하자
os.path.getsize('/Users/guido/Desktop/foo.txt')
# Traceback (most recent call last):
#     File "<stdin>", line 1, in <module>
#     File "/usr/local/lib/python3.3/genericpath.py", line 49, in getsize
#         return os.stat(filename).st_size
# PermissionError: [Errno 13] Permission denied: '/Users/guido/Desktop/foo.txt'





########## 5. 13. 디렉토리 리스팅 구하기 ##########

# 문제 - 디렉토리나 파일 시스템 내부의 파일 리스트를 구하고 싶다.
# 해결 - os.listdir 함수로 디렉토리 내에서 파일 리스트를 얻는다.

import os
names = os.listdir('somedir')

# 이렇게 하면 디렉토리와 파일, 서브디렉토리, 심볼릭 링크 등 모든 것을 구할 수 있다. 만약 데이터를 걸러 내야 한다면
# os.path 라이브러리의 파일에 리스트 컴프리헨션을 사용한다.
import os.path
# 일반 파일 모두 구하기
names = [name for name in os.listdir('somedir')
        if os.path.isfile(os.path.join('somedir', name))]

# 디렉토리 모두 구하기
dirnames = [name for name in os.listdir('somedir')
        if os.path.isdir(os.path.join('somedir', name))]

# 문자열의 startswith()과 endswith() 메소드를 사용하면 디렉터리의 내용을 걸러내기 유용하다.

pyfiles = [name for name in os.listdir('somedir')
            if name.endswith('.py')]

# 파일 이름 매칭을 하기 위해 glob 나 fnmatch 모듈을 사용한다.
import glob
pyfiles = glob.glob('somedir/*.py')

from fnmatch import fnmatch
pyfiles = [name for name in os.listdir('somedir')
            if fnmatch(name, '*.py')]

# 토론
# 디렉토리 리스트를 구하기는 쉽지만, 앞의 방법으로는 엔트리의 이름만 얻을 수 있다.
# 만약 파일 크기나 수정 날짜 등 메타데이터가 필요하다면 os.path 모듈의 추가적인 함수를 사용하거나 os.stat() 함수를 사용한다.

# 디렉토리 리스트 구하기
import os
import os.path
import glob

pyfiles = glob.glob('*.py')

# 파일 크기와 수정 날짜 구하기
name_sz_date = [(name, os.path.getsize(name), os.path.getmtime(name))
                for name in pyfiles]
for name, size, mtime in name_sz_date:
    print(name, size, mtime)

# 대안 : 파일 메타데이터 구하기
file_metadata = [(name, os.stat(name)) for name in pyfiles]
for name, meta in file_metadata:
    print(name, meta.st_size, meta.st_mtime)


