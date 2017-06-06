#  5.14 파일 이름 인코딩 우회
#  ▣ 문제 : 시스템의 기본 인코딩으로 디코딩 혹은 인코딩되지 않은 파일 이름에 입출력 작업을 수행해야 한다.
#  ▣ 해결 : 기본적으로 모든 파일 이름은 sys.getfilesystemencoding() 이 반환하는 텍스트 인코딩 값으로 디코딩 혹은 인코딩 되어 있다.
#           하지만 이 인코딩을 우회하길 바란다면 raw 바이트 문자열로 파일 이름을 명시해야 한다.
import sys
print(sys.getfilesystemencoding())

#   - 유니코드로 파일 이름을 쓴다.
with open('PythonCookBook/files/jalape\xf1o.txt', 'w', encoding='utf-8') as f:
    f.write('Spicy!')

#   - 디렉터리 리스트 (디코딩됨)
import os
print(os.listdir('PythonCookBook/files/'))

#   - 디렉터리 리스트 (디코딩되지 않음)
print(os.listdir(b'PythonCookBook/files/'))

#   - raw 파일 이름으로 파일 열기
with open(b'PythonCookBook/files/.txt') as f:
    print(f.read())

#  ※ 마지막 두 작업에 나온 것처럼, open() 이나 os.listdir() 와 같은 파일 관련 함수에 바이트 문자열을 넣었을 때 파일 이름 처리는 거의 변하지 않는다.

#  ▣ 토론 : 파일 이름과 디렉터리를 읽을 때 디코딩되지 않은 raw 바이트를 이름으로 사용하면 이런 문제점을 피해 갈 수 있다.


#  5.15 망가진 파일 이름 출력
#  ▣ 문제 : 프로그램에서 디렉터리 리스트를 받아 파일 이름을 출력하려고 할 때, UnicodeEncodeError 예외와 "surrogates not allowed" 메시지가
#           발생하면서 프로그램이 죽어 버린다.
#  ▣ 해결 : 출처를 알 수 없는 파일 이름을 출력할 때, 다음 코드로 에러를 방지한다.
def bad_filename(filename):
    return repr(filename)[1:-1]

filenames = os.listdir('PythonCookBook/files/')
for filename in filenames:
    try:
        print(filename)
    except UnicodeEncodeError:
        print(bad_filename(filename))
#  ※ os.listdir() 와 같은 명령을 실행할 때, 망가진 파일 이름을 사용하면 파이썬에 문제가 생긴다.
#     해결책은 디코딩할 수 없는 바이트 값 \xhh 를 Unicode 문자 \udchh 로 표현하는 소위 "대리 인코딩"으로 매핑하는 것이다.

#  ▣ 토론 : UTF-8 이 아닌 Latin-1 으로 인코딩한 bad.txt 를 포함한 디렉터리 리스트가 어떻게 보이는지 예제를 보자.
filename = 'bad.txt'.encode('Latin-1')
with open(b'PythonCookBook/files/'+filename, 'wt', encoding='Latin-1') as f:
    f.write('test')

import os
files = os.listdir('PythonCookBook/files/')
print(files)
#   ※ Latin-1 로 인코딩한 bad.txt 를 출력하려할때 프로그램이 비정상적으로 종료된다.
#      따라서 아래와 같이 출력해야한다.
filenames = os.listdir('PythonCookBook/files/')
for filename in filenames:
    try:
        print(filename)
    except UnicodeEncodeError:
        print(bad_filename(filename))

#   - 아래와 같이 bad_filename() 함수안에서 잘못된 인코딩 된 값을 재인코딩할 수 있다.
def bad_filename(filename):
    temp = filename.encode(sys.getfilesystemencoding(), errors='surrogateescape')
    return temp.decode('latin-1')

for filename in filenames:
    try:
        print(filename)
    except UnicodeEncodeError:
        print(bad_filename(filename))


#  5.16 이미 열려 있는 파일의 인코딩을 수정하거나 추가하기
#  ▣ 문제 : 이미 열려 있는 파일을 닫지 않고 Unicode 인코딩을 추가하거나 변경하고 싶다.
#  ▣ 해결 : 바이너리 모드로 이미 열려 있는 파일 객체를 닫지 않고 Unicode 인코딩/디코딩을 추가하고 싶다면 그 객체를 io.TextIOWrapper()
#           객체로 감싼다.
import urllib.request
import io

u = urllib.request.urlopen('http://www.python.org')
f = io.TextIOWrapper(u, encoding='utf-8')  # 기존 byte 형태인 것을 utf-8 로 변경
text = f.read()
print(text)

#   - 텍스트 모드로 열린 파일의 인코딩을 변경하려면 detach() 메소드로 텍스트 인코딩 레이어를 제거하고 다른 것으로 치환한다.
import sys
print(sys.stdout.encoding)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
print(sys.stdout.encoding)
#   ※ 위 코드를 실행하면 터미널의 출력이 망가질 수도 있다.

#  ▣ 토론 : I/O 시스템은 여러 레이어로 만들어져 있다. 다음 간단한 코드를 통해 레이어를 볼 수 있다.
f = open('PythonCookBook/files/sample.txt', 'w', encoding='utf-8')
print(f)  # io.TextIOWrapper 는 Unicode 를 인코딩/디코딩하는 텍스트 처리 레이어
print(f.buffer)  # io.BufferedWriter 는 바이너리 데이터를 처리하는 버퍼 I/O 레이어
print(f.buffer.raw)  # io.FileIO 는 운영체제에서 하위 레벨 파일 디스크립터를 표현하는 raw file

#   - 일반적으로 앞에 나타난 속성에 접근해 레이어를 직접 수정하는 것은 안전하지 않다.
print(f)
f = io.TextIOWrapper(f.buffer, encoding='latin-1')
print(f)
f.write('Hello')  # ValueError: I/O operation on closed file.
#   ※ f의 원본 값이 파괴되고 프로세스의 기저 파일을 닫았기 때문에 제대로 동작하지 않는다.
#      detach() 메소드는 파일의 최상단 레이어를 끊고 그 다음 레이어를 반환한다.
#      그 다음에 상단 레이어를 더 이상 사용할 수 없다.
f = open('PythonCookBook/files/sample.txt', 'w', encoding='utf-8')
print(f)
b = f.detach()
print(b)
f.write('hello')  # ValueError: underlying buffer has been detached

#   - 하지만 연결을 끊은 후에는, 반환된 결과에 새로운 상단 레이어를 추가할 수 있다.
f = io.TextIOWrapper(b, encoding='latin-1')
print(f)

#   - 인코딩을 변경하는 방법을 보였지만, 이 기술을 라인 처리, 에러 규칙 등 파일 처리의 다른 측면에 활용할 수 있다.
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='ascii', errors='xmlcharrefreplace')
print('Jalape\u00f1o')


#  5.17 텍스트 파일에 바이트 쓰기
#  ▣ 문제 : 텍스트 모드로 연 파일에 로우 바이트를 쓰고 싶다.
#  ▣ 해결 : 단순히 바이트 데이터를 buffer 에 쓴다.
import sys
sys.stdout.write(b'Hello\n')
sys.stdout.buffer.write(b'Hello\n')
#  ※ 이와 유사하게, 텍스트 파일의 buffer 속성에서 바이너리 데이터를 읽을 수도 있다.

#  ▣ 토론 : I/O 시스템은 레이어로부터 만들어진다.
#           텍스트 파일은 버퍼 바이너리 모드 파일 상단에 Unicode 인코딩/디코딩 레이어를 추가해서 생성된다.
#           buffer 속성은 바로 이 파일 아래 부분을 가리킨다.
#           여기에 접근하면 텍스트 인코딩/디코딩 레이어를 우회할 수 있다.


#  5.18 기존 파일 디스크립터를 파일 객체로 감싸기
#  ▣ 문제 : 운영 체제 상에 이미 열려 있는 I/O 채널에 일치하는 정수형 파일 디스크립터를 가지고 있고(file, pipe, socket 등), 이를
#           상위 레벨 파이썬 파일 객체로 감싸고 싶다.
#  ▣ 해결 : 파일 디스크립터는 운영 체제가 할당한 정수형 핸들로 시스템 I/O 채널 등을 참조하기 위한 목적으로써 일반 파일과는 다르다.
#           파일 디스크립터가 있을 때 open() 함수를 사용해 파이썬 파일 객체로 감쌀 수 있다.
#           하지만 이때 파일 이름 대신 정수형 파일 디스크립터를 먼저 전달해야 한다.

# ★ 파일 디스크립터
#  - 파일을 관리하기 위해 운영체제가 필요로 하는 파일의 정보를 가지고 있는 것이다.
#    FCB(File Control Block)이라고 하며 FCB 에는 다음과 같은 정보들이 저장되어 있다.
#   1. 파일 이름
#   2. 보조기억장치에서의 파일 위치
#   3. 파일 구조 : 순차 파일, 색인 순차 파일, 색인 파일
#   4. 액세스 제어 정보
#   5. 파일 유형
#   6. 생성 날짜와 시간, 제거 날짜와 시간
#   7. 최종 수정 날짜 및 시간
#   8. 액세스한 횟수
#  - 결론은 파일 디스크립터란 운영체제가 만든 파일 또는 소켓의 지칭을 편히 하기 위해서 부여된 숫자이다.
#  - 기본적으로 파일 디스크립터는 정수형으로 차례로 넘버링 되고 0,1,2 는 이미 할당되어 있어서 3 부터 디스크립터를 부여한다.

#   - 하위 레벨 파일 디스크립터 열기
import os
fd = os.open('PythonCookBook/files/somefile.txt', os.O_WRONLY | os.O_CREAT)

#   - 올바른 파일로 바꾸기
f = open(fd, 'wt')
f.write('hello world\n')
f.close()

#   - 상위 레벨 파일 객체가 닫혔거나 파괴되었다면, 그 하단 파일 디스크립터 역시 닫힌다.
#     이런 동작을 원하지 않는다면 closefd=False 인자를 open() 에 전달해야 한다.
f = open(fd, 'wt', closefd=False)

#  ▣ 토론 : Unix 시스템 상에서 이 기술을 사용하면 기존의 I/O 채널(pipe, socket 등)을 감싸 파일과 같은 인터페이스로 사용할 수 있는
#           쉬운 길이 열린다.
from socket import socket, AF_INET, SOCK_STREAM

def echo_client(client_sock, addr):
    print('Got connection from', addr)

    # 읽기/쓰기를 위해 소켓에 대한 텍스트 모드 파일 래퍼(wrapper)를 만든다.
    client_in = open(client_sock.fileno(), 'rt', encoding='latin-1', closefd=False)
    client_out = open(client_sock.fileno(), 'wt', encoding='latin-1', closefd=False)

    # 파일 I/O를 사용해 클라이언트에 라인을 에코한다.
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
#  ※ 앞에 나온 예제는 내장 함수 open() 의 기능을 보이기 위한 목적으로 작성한 것이고 Unix 기반 시스템에서만 동작한다.
#     소켓에 대한 파일 같은 인터페이스가 필요하고 크로스 플랫폼 코드가 필요하다면 소켓의 makefile() 메소드를 사용해야 한다.
#     하지만 이식성을 신경쓰지 않는다면 makefile() 을 사용하는 것보다 앞에 나온 예제가 성능 면에서 훨씬 뛰어나다.

#   - stdout 에 바이너리 데이터를 넣기 위한 파일 객체를 만드는 방법
import sys
bstdout = open(sys.stdout.fileno(), 'wb', closefd=False)
bstdout.write(b'Hello World\n')
bstdout.flush()
#   ※ 기존 파일 디스크립터를 파일로 감싸는 것도 가능하지만, 모든 파일 모드를 지원하지 않을 수 있고 이런 파일 디스크립터에 예상치 못한 부작용이 생길 수 있다.
#      또한 동작성이 운영 체제에 따라 달라지기도 한다.
#      예를 들어 앞에 나온 모든 예제는 Unix 가 아닌 시스템에서 아마도 동작하지 않을 것이다.


#  5.19 임시 파일과 디렉터리 만들기
#  ▣ 문제 : 임시 파일이나 디렉터리를 만들어 프로그램에 사용해야 한다.
#           그 후에 파일이나 디렉터리는 아마도 파기할 생각이다.
#  ▣ 해결 : tempfile 모듈에 이런 목적의 함수가 많이 있다. 이름 없는 임시 파일을 만들기 위해서 tempfile.TemporaryFile 을 사용한다.
from tempfile import TemporaryFile

with TemporaryFile('w+t') as f:  # with 문 종료 시 임시 파일은 파기된다.
    # 파일에서 읽기/쓰기
    f.write('Hello World\n')
    f.write('Testing\n')

    # 처음으로 이동해 데이터를 읽는다.
    f.seek(0)
    data = f.read()

#   - 원한다면 다음과 같이 파일을 사용할 수도 있다.
f = TemporaryFile('w+t')
f.close()

with TemporaryFile('w+t', encoding='utf-8', errors='ignore') as f:  # TemporaryFile() 은 추가적으로 내장 함수 open() 과 동일한 인자를 받는다
    f.write('aaa')

#   - 대개 Unix 시스템에서 TemporaryFile() 로 생성한 파일에 이름이 없고 디렉터리 엔트리도 갖지 않는다.
#     이 제한을 없애고 싶으면 NamedTemporaryFile() 을 사용한다.
from tempfile import NamedTemporaryFile

with NamedTemporaryFile('w+t') as f:
    print('filename is : ', f.name)

#   - 자동으로 tempfile 이 삭제되는 걸 원하지 않는 경우 delete=False 키워드 인자를 사용한다.
with NamedTemporaryFile('w+t', delete=False) as f:
    print('filename is:', f.name)

#   - 임시 디렉토리를 만들기 위해서는 tempfile.TemporaryDirectory() 를 사용한다.
from tempfile import TemporaryDirectory
with TemporaryDirectory() as dirname:
    print('dirname is :', dirname)

#  ▣ 토론 : 임시 파일과 디렉터리를 만들 때 TemporaryFile(), NamedTemporaryFile(), TemporaryDirectory() 함수가 가장 쉬운 방법이다.
#            이 함수는 생성과 추후 파기까지 모두 자동으로 처리해 준다.
#            더 하위 레벨로 내려가면 mkstemp() 와 mkdtemp() 로 임시 파일과 디렉터리를 만들 수 있다.
import tempfile
print(tempfile.mkstemp())
print(tempfile.mkdtemp())
#  ※ mkstemp() 함수는 단순히 raw OS 파일 디스크립터를 반환할 뿐 이를 올바른 파일로 바꾸는 것은 프로그래머의 역할로 남겨 둔다.
#     이와 유사하게 파일을 제거하는 것도 독자에게 달려 있다.

#   - 일반적으로 임시 파일은 /var/tmp 와 같은 시스템의 기본 위치에 생성된다.
#     실제 위치를 찾으려면 tempfile.gettempdir() 함수를 사용한다.
print(tempfile.gettempdir())

#   - 모든 임시 파일 관련 함수는 디렉터리와 이름 규칙을 오버라이드 할 수 있도록 한다.
#     prefix, suffix, dir 키워드 인자를 사용하면 된다.
f = NamedTemporaryFile(prefix='mytemp', suffix='.txt', dir='C:\\Users\\kyh\\AppData\\Local\\Temp\\')
print(f.name)

#   - 마지막으로 tempfile() 은 가장 안전한 방식으로 파일을 생성한다는 점을 기억하자.
#     예를 들어 파일에 접근할 수 있는 권한은 현재 사용자에게만 주고, 파일 생성에서 레이스 컨디션이 발생하지 않도록 한다.


#  5.20 시리얼 포트와 통신
#  ▣ 문제 : 시리얼 포트를 통해 하드웨어 디바이스(로봇, 센서 등)와 통신하고 싶다.
#  ▣ 해결 : 파이썬의 내장 기능으로 직접 해결할 수도 있지만, 그보다는 pySerial 패키지를 사용하는 것이 더 좋다.
# import serial
# ser = serial.Serial('/dev/tty.usbmodem641',
#                     baudrate=9600,
#                     bytesize=8,
#                     parity='N',
#                     stopbits=1)
#  ※ 디바이스 이름은 종류나 운영 체제에 따라 달라진다. 예를 들어 Windows 에서 0, 1 등을 사용해서 "COM0", "COM1" 과 같은 포트를 연다.
#     열고 나서 read(), readline(), write() 호출로 데이터를 읽고 쓴다.
# ser.write(b'G1 X50 Y50\r\r')
# resp = ser.readline()

#  ▣ 토론 : 겉보기에는 시리얼 통신이 간단해 보이지만 때로 복잡해지는 경우가 있다.
#            pySerial 과 같은 패키지를 사용해야 하는 이유로 고급 기능(타임 아웃, 컨트롤 플로우, 버퍼 플러싱, 핸드셰이킹 등)을 지원한다는 점이 있다.
#            시리얼 포트와 관련된 모든 입출력은 바이너리임을 기억하자.
#            따라서 코드를 작성할 때 텍스트가 아닌 바이트를 사용하도록 해야 한다.
#            그리고 바이너리 코드 명령이나 패킷을 만들 때 struct 모듈을 사용하면 편리하다.


#  5.21 파이썬 객체를 직렬화 하기
#  ▣ 문제 : 파이썬 객체를 바이트 스트림에 직렬화시켜 파일이나 데이터베이스에 저장하거나 네트워크를 통해 전송하고 싶다.
#  ▣ 해결 : 데이터 직렬화를 위한 가장 일반적인 접근은 pickle 모듈을 사용하는 것이다.
import pickle

data = ['test', 'test1', 'test2', 'test3', 'test4']
f = open('PythonCookBook/files/somefile.bin', 'wb')
pickle.dump(data, f)

#   - 객체를 문자열에 덤프하려면 pickle.dumps() 를 사용한다.
s = pickle.dumps(data)
print(s)

#   - 바이트 스트림으로부터 객체를 다시 만들기 위해서 pickle.load() 나 pickle.loads() 함수를 사용한다.
f = open('PythonCookBook/files/somefile.bin', 'rb')
data = pickle.load(f)
print(data)

#   - 문자열에서 불러들이기
data = pickle.loads(s)
print(data)

#  ▣ 토론 : 대부분의 프로그램에서 pickle 을 효율적으로 사용하기 위해서는 dump() 와 load() 함수만 잘 사용하면 된다.
#            파이썬 객체를 데이터베이스에 저장하거나 불러오고, 네트워크를 통해 전송하는 라이브러리를 사용한다면 내부적으로
#            pickle 을 사용하고 있을 확률이 크다.

#   - 다중 객체와 작업
import pickle
f = open('PythonCookBook/files/somefile.bin', 'wb')
pickle.dump([1, 2, 3, 4], f)
pickle.dump('hello', f)
pickle.dump({'Apple', 'Pear', 'Banana'}, f)
f.close()
f = open('PythonCookBook/files/somefile.bin', 'rb')
print(pickle.load(f))
print(pickle.load(f))
print(pickle.load(f))

#   - 함수, 클래스, 인스턴스를 피클할 수 있지만 결과 데이터는 코드 객체와 관련 있는 이름 참조만 인코드한다.
import math
print(pickle.dumps(math.cos))

#  ※ pickle.load() 는 믿을 수 없는 데이터에 절대 사용하면 안 된다.
#     로딩의 부작용으로 pickle 이 자동으로 모듈을 불러오고 인스턴스를 만든다.
#     하지만 악의를 품은 사람이 이 동작을 잘못 사용하면 일종의 바이러스 코드를 만들어 파이썬이 자동으로 실행하도록 할 수 있다.
#     따라서 서로 인증을 거친 믿을 수 있는 시스템끼리 내부적으로만 pickle 을 사용하는 것이 좋다.

#  ※ 피클할 수 없는 객체
#   - 파일, 네트워크 연결, 스레드, 프로세스, 스택 프레임 등 외부 시스템 상태와 관련 있는 것들이 포함.

#   - 사용자 정의 클래스에 __getstate__() 와 __setstate__() 메소드를 제공하면 이런 제약을 피해 갈 수 있다.
#     정의를 했다면 pickle.dump() 는 __getstate__() 를 호출해 피클할 수 있는 객체를 얻는다.
#     마찬가지로 __setstate__() 는 언피클을 유발한다.

#   - 클래스 내부에 스레드를 정의하지만 피클/언피클 할 수 있는 예제를 보자.
from PythonCookBook import countdown
c = countdown.Countdown(30)

f = open('PythonCookBook/files/cstate.p', 'wb')
import pickle
pickle.dump(c, f)
f.close()

#   - 이제 파이썬을 종료하고 재시작한 후에 다음을 실행한다.
f = open('PythonCookBook/files/cstate.p', 'rb')
pickle.load(f)
#  ※ 쓰레드가 다시 살아나서 처음으로 피클했을 때 종료했던 곳부터 시작하는 것을 볼 수 있다.
#     pickle 은 array 모듈이나 numpy 와 같은 라이브러리가 만들어 낸 거대한 자료 구조에 사용하기에 효율적인 인코딩 방식이 아니다.
#     pickle 에는 아주 많은 옵션이 있고 주의해야 할 점도 많다.
#     일반적인 경우에 이런 것을 걱정할 필요는 없지만 직렬화를 위해 pickle 을 사용하는 큰 애플리케이션을 만든다면 공식 문서를 통해
#     이와 같은 내용을 잘 숙지하도록 하자.


# Chapter 6. 데이터 인코딩과 프로세싱
#  6.1 CSV 데이터 읽고 쓰기
#  ▣ 문제 : CSV 파일로 인코딩된 데이터를 읽거나 쓰고 싶다.
#  ▣ 해결 : 대부분의 CSV 데이터는 csv 라이브러리를 사용한다.
import csv
with open('PythonCookBook/files/emp.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    print(headers)
    for row in f_csv:
        print(row[0], row[1])

#   - 인덱스 사용이 때때로 헷갈리기 때문에 네임드 튜플을 고려한다.
#     이렇게 하면 row.empno, row.ename 과 같이 열 헤더를 사용할 수 있다.
from collections import namedtuple
with open('PythonCookBook/files/emp.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for r in f_csv:
        row = Row(*r)
        print(row.empno, row.ename)

#   - 또 다른 대안으로 데이터를 딕셔너리 시퀀스로 읽을 수도 있다.
import csv
with open('PythonCookBook/files/emp.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        print(row['empno'], row['ename'])

#   - CSV 데이터를 쓰려면, csv 모듈을 사용해서 쓰기 객체를 생성한다.
headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
        ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
        ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000)]
with open('PythonCookBook/files/stocks.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)

#   - 데이터를 딕셔너리 시퀀스로 가지고 있는 경우
headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [{'Symbol': 'AA', 'Price': 39.48, 'Date': '6/11/2007', 'Time': '9:36am', 'Change': -0.18, 'Volumn': 181800},
        {'Symbol': 'AIG', 'Price': 71.38, 'Date': '6/11/2007', 'Time': '9:36am', 'Change': -0.15, 'Volumn': 195500},
        {'Symbol': 'AXP', 'Price': 62.58, 'Date': '6/11/2007', 'Time': '9:36am', 'Change': -0.46, 'Volumn': 935000}]
with open('PythonCookBook/files/stocks.csv', 'w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)

#  ▣ 토론 : CSV 데이터를 수동으로 다루는 프로그램을 작성하기보다는 csv 모듈을 사용하는 것이 훨씬 나은 선택이다.
#   - 구분자가 tab 으로 나누어진 데이터를 읽는 경우
with open('PythonCookBook/files/stocks.csv') as f:
    f_tsv = csv.reader(f, delimiter='\t')
    for row in f_tsv:
        print(row)

#   - CSV 파일 헤더에 유효하지 않은 식별 문자가 들어있는 경우
import re
with open('PythonCookBook/files/stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = [re.sub('[^a-zA-Z_]', '_', h) for h in next(f_csv)]
    Row = namedtuple('Row', headers)
    for r in f_csv:
        row = Row(*r)

#   - CSV 데이터에 대해서 추가적인 형식 변환을 하는 경우
col_types = [str, float, str, str, float, int]
with open('PythonCookBook/files/stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        r = tuple(convert(value) for convert, value in zip(col_types, row))
        print(r)

#   - 딕셔너리에서 선택한 필드만 변환하는 경우
print('Reading as dicts with type conversion')
field_types = [('Price', float), ('Change', float), ('Volume', int)]
with open('PythonCookBook/files/stocks.csv') as f:
    for row in csv.DictReader(f):
        row.update((key, conversion(row[key])) for key, conversion in field_types)
        print(row)


#  6.2 JSON 데이터 읽고 쓰기
#  ▣ 문제 : JSON 으로 인코딩된 데이터를 읽거나 쓰고 싶다.
#  ▣ 해결 : JSON 으로 데이터를 인코딩, 디코딩하는 쉬운 방법은 json 모듈을 사용하는 것이다.
#            주요 함수는 json.dumps() 와 json.loads() 이고, pickle 과 같은 직렬화 라이브러리에서 사용한 것과 인터페이스는 동일하다.
import json

data = {'name': 'ACME', 'shares': 100, 'price': 542.23}
json_str = json.dumps(data)
data = json.loads(json_str)
print(data, type(data))

#   - 문자열이 아닌 파일로 작업한다면 json.dump() 와 json.load() 를 사용해서 JSON 데이터를 인코딩/디코딩한다.
with open('PythonCookBook/files/data.json', 'w') as f:
    json.dump(data, f)

with open('PythonCookBook/files/data.json', 'r') as f:
    data = json.load(f)
    print(data)

#  ▣ 토론 : JSON 인코딩은 None, bool, int, float, str 과 같은 기본 타입과 함께 리스트, 튜플, 딕셔너리와 같은 컨테이너 타입을 지원한다.
#            딕셔너리의 경우 키는 문자열로 가정한다.
#            JSON 인코딩 포맷은 약간의 차이점을 제외하고는 파이썬 문법과 거의 동일하다.
#            예를 들어 True 는 true 로 False 는 false 로 None 은 null 로 매핑된다.
print(json.dumps(False))
d = {'a': True, 'b': 'Hello', 'c': None}
print(json.dumps(d))

#   - 데이터에 중첩이 심하게 된 구조체가 포함된 경우 pprint 모듈의 pprint() 함수를 사용해 보자.
#     이 함수는 키를 알파벳 순으로 나열하고 딕셔너리를 좀 더 보기 좋게 출력한다.
from urllib.request import urlopen
import json
u = urlopen('http://search.twitter.com/search.json?q=python&rpp=5')
resp = json.loads(u.read().decode('utf-8'))
from pprint import pprint
pprint(resp)

#   - 일반적으로 JSON 디코딩은 제공 받은 데이터로부터 딕셔너리나 리스트를 생성한다.
#     다른 종류의 객체를 만들고 싶다면 json.loads() 에 object_pairs_hook 나 object_hook 를 넣는다.
s = '{"name": "ACME", "shares": 50, "price": 490.1}'
from collections import OrderedDict
data = json.loads(s, object_pairs_hook=OrderedDict)
print(data, data['name'])

#   - JSON 딕셔너리를 파이썬 객체로 바꾸는 예시
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

data = json.loads(s, object_hook=JSONObject)
print(data.name, data.shares, data.price)

#   - 출력을 더 보기 좋게 하기위해 json.dumps() 에 indent 인자를 사용한다.
print(json.dumps(data))
print(json.dumps(data, indent=4))  # indent : 들여쓰는 역할

#   - 출력에서 키를 정렬하는 경우
print(json.dumps(data, sort_keys=True))

#   - 인스턴스는 일반적으로 JSON 으로 직렬화하지 않는다.
#     직렬화하고 싶다면 인스턴스를 입력으로 받아 직렬화 가능한 딕셔너리를 반환하는 함수를 제공해야 한다.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def serialize_instance(obj):
    d = {'__classname__': type(obj).__name__}
    d.update(vars(obj))  # vars : 해당 객체에 대한 변수 정보 출력 -> dict
    return d

classes = {'Point': Point}

def unserialize_object(d):
    clsname = d.pop('__classname__', None)
    if clsname:
        cls = classes[clsname]
        obj = cls.__new__(cls)
        for key, value in d.items():
            setattr(obj, key, value)
        return obj
    else:
        return d

p = Point(2, 3)
s = json.dumps(p, default=serialize_instance)
print(s)
a = json.loads(s, object_hook=unserialize_object)
print(a, a.x, a.y)


#  6.3 단순한 XML 데이터 파싱
#  ▣ 문제 : 단순한 XML 문서에서 데이터를 얻고 싶다.
#  ▣ 해결 : 단순한 XML 문서에서 데이터를 얻기 위해 xml.etree.ElementTree 모듈을 사용하면 된다.
from urllib.request import urlopen
from xml.etree.ElementTree import parse

u = urlopen('http://planet.python.org/rss20.xml')  # RSS 피드를 다운로드하고 파싱한다.
doc = parse(u)

for item in doc.iterfind('channel/item'):
    title = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')

    print(title)
    print(date)
    print(link)
    print()

#  ▣ 토론 : 많은 애플리케이션에서 XML 로 인코딩된 데이터를 다룬다.
#            인터넷 상에서 데이터를 주고 받을 때 XML 을 사용하는 곳이 많기도 하지만, 애플리케이션 데이터를 저장할 때도
#            일반적으로 사용하는 형식이다.

#   - ElementTree 모듈이 나타내는 모든 요소는 파싱에 유용한 요소와 메소드를 약간 가지고 있다.
#     tag 요소에는 태그의 이름, text 요소에는 담겨 있는 텍스트가 포함되어 있고 필요한 경우 get() 메소드로 요소를 얻을 수 있다.
print(doc)
e = doc.find('channel/title')
print(e)
print(e.tag, e.text, type(e))
e1 = doc.find('channel')
print(e1.get('name'))  # get() :  태그 속성을 가져옴

#   - XML 파싱에 xml.etree.ElementTree 말고 다른 것을 사용할 수도 있다.
#     임포트 구문만 from lxml.etree import parse 로 바꾸면 된다.
#     lxml 은 XML 표준과 완벽히 동일한 혜택을 제공한다. 또한 매우 빠르고 검증, XSLT, XPath 와 같은 모든 기능을 제공한다.


#  6.4 매우 큰 XML 파일 증분 파싱하기
#  ▣ 문제 : 매우 큰 XML 파일에서 최소의 메모리만 사용하여 데이터를 추출하고 싶다.
#  ▣ 해결 : 증분 데이터 처리에 직면할 때면 언제나 이터레이터와 제너레이터를 떠올려야 한다.
#            여기 아주 큰 XML 파일을 증분적으로 처리하며 메모리 사용은 최소로 하는 함수를 보자.
from xml.etree.ElementTree import iterparse

def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
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
                elem_stack[-2].remove(elem)  # 앞에서 나온 요소를 부모로부터 제거하는 역할 (Tag 삭제)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass

#   - 파일 전체를 읽어 메모리에 넣고 수행하는 코드
from xml.etree.ElementTree import iterparse
from collections import Counter
potholes_by_zip = Counter()
doc = parse('PythonCookBook/files/potholes.xml')
for pothole in doc.iterfind('row/row'):
    potholes_by_zip[pothole.findtext('zip')] += 1

for zipcode, num in potholes_by_zip.most_common():
    print(zipcode, num)

#   - 파일의 특정 부분을 가지고 메모리에 넣고 수행하는 코드
from collections import Counter
potholes_by_zip = Counter()

data = parse_and_remove('PythonCookBook/files/potholes.xml', 'row/row')
for pothole in data:
    potholes_by_zip[pothole.findtext('zip')] += 1

for zipcode, num in potholes_by_zip.most_common():
    print(zipcode, num)

#  ▣ 토론 : iterparse() 메소드로, XML 문서를 증분 파싱
#             - iterparse() 가 생성한 이터레이터는 (event, elem) 으로 구성된 튜플을 만든다.
#             - start 이벤트는 요소가 처음 생성되었지만 다른 데이터를 만들지 않았을 때 생성된다.
#             - end 이벤트는 요소를 마쳤을 때 생성된다.
#             - start-ns 와 end-ns 이벤트는 XML 네임스페이스 선언을 처리하기 위해 사용한다.
#             - elem_stack[-2].remove(elem) 을 통해 부모 태그로부터 특정 태그(elem)를 제거한다.