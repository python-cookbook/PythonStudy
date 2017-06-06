# 이미 열려있는 파일의 인코딩을 수정하거나 추가하기
#문제
#이미 열려있는 파일을 닫지 않고 유니코드 인코딩을 추가하거나 변경하고 싶다.
#해결
#바이너리 모드로 이미 열려있는 파일 객체를 닫지 않고 유니코드 인코딩 디코딩을 추가하고 싶다면 그 객체를 io.TextIOWrapper()객체로 감싼다.
import urllib.request,io
u = urllib.request.urlopen('http://python.org')
f = io.TextIOWrapper(u,encoding='utf-8')
text = f.read()
text
#텍스트 모드로 열린 파일의 인코딩을 변경하려면 detach()메소드로 텍스트 인코딩 레이어를 제거하고 다른 것으로 치환한다. sys.stdout 인코딩을 바꾸는 방법을 보자.
import sys
sys.stdout.encoding
sys.stdout=io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
sys.stdout.encoding
#이 코드는 단순히 예를 위한 목적. 터미널 망가짐
#토론
#IO시스템은 여러 레이어로 만드러옂 ㅣㅇㅆ다. 다음 간단한 코드를 통해 레이어를 볼 수 있다.,
f=open('sample.txt','w')
f
f.buffer
f.buffer.raw
#이 예제에서 iotextwrapper는 유니코드를 인코딩 디코딩하는 텍스트 처리 레이어, iobufferwriter는 바이너리 데이터를 처리하는 버퍼 io레이어, iofileio는 운영체제에서
#하위 레벨 파일 디스크럽터를 표현하는 로우 파일이다. 텍스트 인코딩의 추가 수정에는 최상단 레이어인 iotrxtwrapper의 추가 수정이 포함된다.
#일반적으로 앞에 나타난 속성에 접근해 레이얼르 직접 수정하는 것은 안전하지 않다. 예를 들어 이 기술을 사용해 인코딩을 변경했을 때 무슨일이 벌어지는지 살펴보자.
f
f = io.TextIOWrapper(f.buffer,encoding='latin-1')
f
f.write('hello')
#f의 원본값이 파괴되고 프로세스의 기저 파일을 닫았기 때문에 제대로 동작하지 않는다.
#detach() 메소드느 ㄴ파일의 최상단 레이어를 끊고 그 다음 레이어를 반환한다. 그 다음에 상단 레이어를 더이상 사용할 수 없다.
f=open('sample.txt','w')
f
b=f.detach()
b
f.write('hello')
#하지만 연결을 끊은 후에는 반환된 결과에 새로운 상단 레이어를 추가할 수 있다.
f - io.TextIOWrapper(b,encoding='latin-1')
f
#인코딩을 변경하는 방법을 보였지만, 이 기술을 라인 처리, 에러 규칙등 파일 처리의 다른 측면에 활용할 수 있다.