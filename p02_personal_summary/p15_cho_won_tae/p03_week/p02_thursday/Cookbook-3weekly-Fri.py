# 5.1 텍스트 데이터 읽고 쓰기
# 문제
# 텍스트 데이터를 읽거나 써야하는데 ASCII, UTF-8, UTF-16 과 같이 서로 다른 인코딩을 사용해야 한다
# 해결
# 텍스트 파일을 읽기 위해 open() 함수에 rt 모드를 사용한다
# 파일 전체를 하나의 문자열로 읽음
with open('somefile.txt','rt') as f:
    data = f.read()
# 파일의 줄을 순환
with open('somefile.txt','rt') as f:
    for line in f:
        # 라인처리
        ...
# 마찬가지로 텍스트 파일을 쓰려면 wt 모드를 사용한다. 이 모드를 사용하면 모든 내용을 지우고(혹시 있다면) 새로운 내용을 덮어쓴다
# 텍스트 데이터 쓰기
with open('somefile.txt','wt') as f:
    f.write(text1)
    f.write(text2)
# 리다이렉트한 print 문
with open('somefile.txt','wt') as f:
    print(line1,file=f)
    print(line2,file=f)
    ...
# 파일의 끝에 내용을 추가하려면 at 모드로 open()을 사용한다
# 기본적으로 파일을 읽고 쓸 때 sys.getdefaultencoding()으로 확인할 수 있는 시스템 기본 인코딩을 사용한다
# 대부분의 컴퓨터는 이 기본 인코딩으로 utf-8을 사용한다.
# 읽고 쓸 텍스트가 다른 인코딩을 사용한다면 open()에 추가적인 encoding 인자를 전달한다
with open('somefile.txt','rt',encoding='latin-1') as f:
    ...
# 파이썬이 이해할 수 있는 텍스트 인코딩의 종류는 수백가지에 이른다.
# 하지만 일반적으로 사용하는 인코딩은 ascii, latin-1, utf-8, utf-16 이다.
# 웹 애플리케이션을 만든다면 utf-8이 안전한 형식이다
# 토론
# 텍스트 파일을 읽고 쓰는 과정은 그다지 어렵지 않다.
# 하지만 몇 가지 주의해야 할 점이 있다
# 우선 예제에서 사용한 with 문이 파일을 사용할 콘텍스트를 만든다.
# 컨트롤이 with 블록을 떠나면 파일이 자동으로 닫힌다. with 문을 꼭 사용하지 않아도 되지만, 그럴때는 반드시 파일을 닫아야 한다

# 5.2 파일에 출력
# 문제
# print() 함수의 결과를 파일에 출력하고 싶다
# 해결
# print() 에 file 키워드 인자를 사용한다
with open('somefile.txt','rt') as f:
    print('Hello World!',file=f)
# 토론
# 파일에 출력하기에서 이 이상의 내용은 없다
# 하지만 파일을 텍스트 모드로 열었는지 꼭 확인해야 한다
# 바이너리 모드로 파일을 열면 출력에 실패한다

# 5.3 구별자나 종단 부호 바꾸기
# 문제
# print()를 사용해 데이터를 출력할 떄 구분자나 종단 부호를 바꾸고 싶다
# 해결
# print()에 sep 과 end 키워드 인자를 사용한다
print('ACME',50,91.5) # ACME 50 91.5 출력
print('ACME',50,91.5,sep=',') # ACME,50,91.5 출력
print('ACME',50,91.5,sep=',',end='!!\n') # ACME,50,91.5!! 출력
# 출력의 개행문자(NEWLINE)를 바꿀 때도 END 인자를 사용한다
for i in range(5):
    print(i) # 0 1 2 3 4 엔터로 출력
for i in range(5):
    print(i,end=' ') # 0 1 2 3 4 출력
# 토론
#print()로 출력시 아이템을 구분하는 문자를 스페이스 공백문 이외로 바꾸는 가장 쉬운 방법은 구별자를 지정하는 것이다
# 어떤 프로그래머는 동일한 목적으로 str.join()을 사용하기도 한다.
print(','.join('ACME','50','91.5'))
# 하지만 str.join() 은 문자열에만 동작한다는 문제점이 있다
# 문자열이 아닌 데이터에 사용하려면 귀찮은 작업을 먼저 적용해야 하므로 sep, end 를 이용해보자

# 5.4 바이너리 데이터 읽고 쓰기
# 문제
# 이미지나 사운드 파일 등 바이너리 데이터를 읽고 써야 한다
# 해결
# open() 함수에 rb와 wb 모드를 사용해서 바이너리 데이터를 읽거나 쓴다
# 파일 전체를 하나의 바이트 문자열로 읽기
# with open('somefile.bin','rb') as f:
#     data = f.read()
# # 바이너리 데이터 파일에 쓰기
# with open('somefile.bin','wb') as f:
#     f.write(b'Hello World')
# 바이너리를 읽을때 반환된 모든 데이터가 텍스트 문자열 형식이 아니라 바이트 문자열 형식이 된다는 점을 기억하자
# 마찬가지로 데이터를 쓸 때도 바이트로 표현할 수 있는 형식의 객체를 제공해야 한다(바이트 문자열, bytearray 객체 등)
# 토론
# 바이너리 데이터를 읽을 때, 바이너리 문자열과 텍스트 문자열 사이에 미묘한 문법 차이가 있다
# 자세히 말하자면, 데이터에 인덱스나 순환으로 반환한 값은 바이트 문자열이 아닌 정수 바이트 값이 된다
# 텍스트 문자열
t = 'Hello World'
print(t[0]) # H 출력
for c in t:
    print(c) # H e l l o W o r l d 출력
# 바이트 문자열
b = b'Hello World'
print(b[0]) # 72 출력
for c in b:
    print(c) # 72 101 108 108 111 ... 출력
# 바이너리 모드 파일로부터 텍스트를 읽거나 쓰려면 인코딩이나 디코딩 과정이 꼭 필요하다
with open('somefile.bin','rb') as f:
    data = f.read(16)
    text = data.decode('utf-8')
with open('somefile.bin','wb') as f:
    text = 'Hello World'
    f.write(text.encode('utf-8'))
# 바이너리 입출력 시 잘 알려지지 않은 기능으로 배열이나 C 구조체와 같은 객체를 bytes 객체로 변환하지 않고
# 바로 쓸수 있다는 점이 있다

import array
nums = array.array('i',[1,2,3,4])
with open('data.bin','wb') as f:
    f.write(nums)
# 이 기능은 소위 버퍼 인터페이스로 구현되어 있는 객체에 모두 적용된다
# 이런 객체는 기반 메모리 버퍼를 바로 작업에 노출시켜 작업이 가능하다
# 바이너리 데이터를 쓰는 것도 이런 작업의 일종이다
# 또한 파일의 readinto() 메소드를 사용하면 여러 객체의 바이너리 데이터를 직접 메모리에 읽어 들일 수 있다
import array
a = array.array('i',[0,0,0,0,0,0,0])
with open('data.bin','rb') as f:
    f.readinto(a)
# 하지만 이 기술을 사용할 때는 각별히 주의해야 한다.
# 구현법이 플랫폼에 따라 다르기도 하고 단어의 크기와 바이트 순서 등에 의존하기 때문이다.
# 바이너리 데이터 때 수정 가능한 버퍼에 읽어 들이는 다른 예는 레시피 5.9를 참고한다

# 5.5 존재하지 않는 파일에 쓰기
# 문제
# 파일이 파일 시스템에 존재하지 않을 때, 데이터를 파일에 쓰고 싶다
# 해결
# 이 문제는 open()에 x 모드를 사용해서 해결할 수 있다
# w 모드와 다르게 x 모드는 잘 알려져 있지 않다
with open('somefile','wt') as f:
    f.write('Hello\n')
with open('somefile','xt') as f:
    f.write('Hello\n')
# 파일이 바이너리 모드이면 xt 대신 xb를 사용한다
# 토론
# 이 레시피는 파일을 쓸 때 발생할 수 있는 문제점을 아주 우아하게 피해 가는 법을 알려준다
# 혹은 파일을 쓰기 전에 파일이 있는지 확인하는 방법도 있다
import os
if not os.path.exists('somefile'):
    with open('somefile','wt') as f:
        f.write('Hello\n')
else:
    print('File already exists!')
# 확실히 x 모드를 사용하는 것이 훨씬 깔끔하다
# 그리고 x 모드는 파이썬 3의 확장 기능임을 기억해야 한다
# 이전 버전의 파이썬이나 파이썬 구현에서 사용하는 C 라이브러리는 이 모드를 지원하지 않는다

# 5.6 문자열에 입출력 작업하기
# 문제
# 파일 같은 객체에 동작하도록 작성한 코드에 텍스트나 바이너리 문자열을 제공하고 싶다
# 해결
# io.StringIO()와 io.BytesIO() 클래스로 문자열 데이터에 동작하는 파일 같은 객체를 생성한다
s = io.StringIO()
s.write('Hello World\n') # 12 출력
print('This is a test',file=s) # 15 출력
# 기록한 모든 데이터 얻기
s.getvalue() # 'Hello World\nThis is a test\n' 출력
# 기존 문자열을 파일 인터페이스로 감싸기
s = io.StringIO('Hello\nWorld\n')
s.read(4) # 'Hell' 출력
s.read() # 'o\nWorld\n' 출력
# io.StringIO 클래스는 텍스트에만 사용해야 한다.
# 바이너리 데이터를 다룰 때는 io.BytesIO 클래스를 사용한다
s = io.BytesIO()
s.write(b'binary data')
s.getvalue() # b'binary data' 출력
# 토론
# 일반 파일 기능을 흉내 내려 할 때 StringIO 와 BytesIO 클래스가 가장 유용하다
# 예를 들어 유닛 테스트를 할때, StringIO로 테스트 데이터를 담고 있는 객체를 만들어 일반 파일에 동작하는 함수에 사용할 수 있다

# 5.7 압축된 데이터 파일 읽고 쓰기
# 문제
# gzip이나 bz2 로 압축한 파일을 읽거나 써야 한다
# 해결
# gzip과 bz2 모듈을 사용하면 간단히 해결 가능하다
# 이 모듈은 open()을 사용하는 구현법의 대안을 제공한다
# 예를 들어 압축된 파일을 텍스트로 읽으려면 다음과 같이 한다
# gzip 압축
import gzip
with gzip.open('somefile.gz','rt') as f:
    text = f.read()
# bz2 압축
import bz2
with bz2.open('somefile.bz2','rt') as f:
    text = f.read()
# 압축한 데이터를 쓰는 방법은 다음과 같다
# gzip 압축
import gzip
with gzip.open('somefile.gz','wt') as f:
    f.write(text)
# bz2 압축
import bz2
with bz2.open('somefile.bz2','wt') as f:
    f.write(text)
# 앞에서 살펴본 대로, 모든 입출력은 텍스트를 사용하고 유니코드 인코딩/디코딩을 수행한다
# 바이너리 데이터를 사용하고 싶다면 rb 또는 wb 모드를 사용하도록 하자
# 토론
# 압축한 데이터를 읽거나 쓰기가 어렵지는 않다
# 하지만, 올바른 파일 모드를 선택하는 것은 상당히 중요하다
# 모드를 명시하지 않으면 기본적으로 바이너리 모드가 된다
# 텍스트 파일을 받을 것이라고 가정한 프로그램에는 문제가 발생한다
# gzip.open() 과 bz2.open() 은 encoding, errors, newline과 같이 내장 함수 open() 과 동일한 인자를 받는다
# 압축한 데이터를 쓸 때는 compresslevel 인자로 압축 정도를 지정할 수 있다
with gzip.open('somefile.gz','wt',compresslevel=5) as f:
    f.write(text)
# 기본 레벨은 9로 가장 높은 압축률을 가리킨다.
# 레벨을 내리면 속도는 더 빠르지만 압축률은 떨어진다
# 마지막으로 잘 알려지지 않은 기능인 gzip.open() 과 bz2.open() 을 기존에 열려 있는 바이너리 파일의 상위에 위치시키는 것을보자
import gzip
f = open('somefile.gz','rb')
with gzip.open(f,'rt') as g:
    text = g.read()
# 이렇게 하면 gzip 과 gz2 모듈이 파일 같은 객체와 같이 작업한다

# 5.8 고정 크기 레코드 순환
# 문제
# 파일을 줄 단위로 순환하지 않고, 크기를 지정해서 그 단위별로 순환하고 싶다
# 해결
# iter() 함수와 functools.partial() 을 사용한다
from functools import partial
RECORD_SIZE = 32
with open('somefile.data','rb') as f:
    records = iter(partial(f.read,RECORD_SIZE),b'')
    for r in records:
        ...
# 이 예제의 records 객체는 파일의 마지막에 도달할 때까지 고정 크기 데이터를 생산하는 순환 객체이다
# 하지만 파일의 크기가 지정한 크기의 정확한 배수가 아닌 경우 마지막 아이템의 크기가 예상보다 작을 수도 있다
# 토론
# iter() 함수에 잘 알려지지 않은 기능으로, 호출 가능 객체와 종료 값을 전달하면 이터레이터를 만드는 것이 있다
# 그 이터레이터는 제공 받은 호출 가능 객체를 반복적으로 호출하며 종료 값을 반환할 때 순환을 멈춘다

# 5.11 경로 다루기
# 문제
# 기본 파일 이름, 디렉터리 이름, 절대 경로 등을 찾기 위해 경로를 다루어야 한다
# 해결
# 경로를 다루기 위해서 os.path 모듈의 함수를 사용한다. 몇몇 기능을 예제를 통해 살펴보자
import os
path = '\User\beazley\Data\data.csv'
# 경로의 마지막 부분 구하기
os.path.basename(path) #'data.csv' 출력
# 디렉토리 이름 구하기
os.path.dirname(path) # \Users\beazley\Data' 출력
# 각 부분을 합치기
os.path.join('tmp','data',os.path.basename(path))
# 'tmp/data/data.csv' 출력
# 파일 확장자 나누기
os.path.splitext(path) # '~/Data/data','.csv' 출력
# 토론
# 파일 이름을 다루기 위해서 문자열에 관련된 코드를 직접 작성하지 말고 os.path 모듈을 사용해야 한다
# 이는 이식성과도 어느 정도 관련이 있다
# os.path 모듈은 Unix 와 Window 의 차이점을 알고 자동으로 처리해준다

# 5.12 파일 존재 여부 확인
# 문제
# 파일이나 디렉토리가 존재하는지 확인해야 한다
# 해결
# 파일이나 디렉토리의 존재 여부를 확인하기 위해서 os.path 모듈을 사용한다
import os
print(os.path.exists('/etc/passwd')) # False 출력
print(os.path.exists('/tmp/spam')) # False 출력
# 추가적으로 파일의 종류가 무엇인지 확인할 수 있다
# 다음 코드에서 파일이 없는 경우 False 를 반환한다
# 일반 파일인지 확인
print(os.path.isfile('/etc/passwd')) # False 출력
# 디렉토리인지 확인
print(os.path.isdir('/etc/passwd')) # False 출력
# 메타데이터(파일 크기, 수정 날짜) 등이 필요할 때도 os.path 모듈을 사용한다
print(os.path.getsize('/etc/passwd')) # 3669
print(os.path.getmtime('/etc/passwd')) # 1272478234.0

# 5.13 디렉토리 리스팅 구하기
# 문제
# 디렉토리나 파일 시스템 내부의 파일 리스트를 구하고 싶다
# 해결
# os.listdir() 함수로 디렉토리 내에서 파일 리스트를 얻는다
import os
name = os.listdir('somedir')
# 이렇게 하면 디렉토리와 파일, 서브디렉토리, ㅣㅁ볼릭 링크 등 모든 것을 구할 수 있다
# 만약 데이터를 걸러 내야 한다면 os.path 라이브러리의 파일에 리스트 컴프리헨션을 사용한다
import os.path
# 일반 파일 모두 구하기
names=[name for name in os.listdir('somedir')
       if os.path.isfile(os.path.join('somedir',name))]
# 디렉토리 모두 구하기
dirnames = [name for name in os.listdir('somedir')
            if os.path.isdir(os.path.join('somedir',name))]
# 문자열의 startswith() 와 endswith() 메소드를 사용하면 디렉토리의 내용을 걸러내기 유용하다
pyfiles = [name for name in os.listdir('somedir')
    if name.endswith('.py')]
# 파일 이름 매칭을 하기 위해 glob이나 fnmatch 모듈을 사용한다
import glob
pyfiles = glob.glob('somedir/*.py')
# 토론
# 디렉토리 리스트를 구하기는 쉽지만, 앞에 나온 방법으로는 엔트리의 이름만 얻을 수 있다
# 만약 파일 크기나 수정 날짜 등 메타데이터가 필요하다면 os.path 모듈의 추가적인 함수를 사용하거나 os.stat() 함수를 사용한다
# 디렉토리 리스트 구하기
import os
import os.path
import glob
pyfiles = glob.glob('*.py')
# 파일 크기와 수정 날짜 구하기
name_sz_date = [(name,os.path.getsize(name),os.path.getmtime(name))
                for name in pyfiles]
for name,size,mtime in name_sz_date:
    print(name,size,mtime)
# 마지막으로 파일 이름을 다룰 때 인코딩과 관련된 문제가 발생할 수 있다
# 일반적으로 os.listdir()와 같은 함수가 반환하는 엔트리는 파일 시스템의 기본 인코딩으로 디코드된다
# 하지만, 특정상황에서는 파일 이름을 디코딩하는 것이 불가능하므로 나중에 더 자세히 다뤄보자!!!
