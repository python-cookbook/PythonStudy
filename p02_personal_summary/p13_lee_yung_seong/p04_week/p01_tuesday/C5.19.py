#임시 파일과 디렉터리 만들기
#문제
#임시 파일이나 디렉터리를 만들어 프로그램에 사용해야한다. 그 후에 파일이나 디렉터리는 아마도 파기할 생각이다.
#해결
#tempfile 모듈에 이런 목적의 함수가 많이 있다. 이름 없느 ㄴ임시 파일을 만들기 위해서 tempfile.TemporaryFile을 사용한다.
from tempfile import TemporaryFile
with TemporaryFile('w+t') as f:
    #파일에서 읽기,쓰기
    f.write('Hello world\n')
    f.write('Testing\n')
    #처음으로 이동해 데이터를 읽는다
    f.seek(0)
    data = f.read()

#혹은 원한다면 다음과 같이 파일을 사용할 수도 있다.
f = TemporaryFile('w+t')
#임시 파일 사용
f.close()

#TemporaryFile()에 전달하는 첫번째 인자는 파일모드이고, 텍스트 모드에는 대게 w+t를 바이너리 몯에는 w+b를 사용한다. 이 모드는 읽기와 쓰기를 동시에 지원하기 때문에,
#모드 변경을 위해 파일을 닫으면 실제로 파기하므로 유용하다. TemporaryFile()은 추가적으로 내장 함수 open()과 동일한 인자를 받는다.
#with TemporaryFile('w+t',encoding='utf-8', errors='ignore') as f:

#대게 유닉스 시스템에서 temporaryfile()로 생성한 파일에 이름이 없고 디렉터리 엔트리도 갖지 않는다. 이 제한을 없애고 싶으면 NamedTemporaryFile()을 사용함 된다.
from tempfile import NamedTemporaryFile

with NamedTemporaryFile('w+t') as f:
    print('filename is .. ',f.name)
    #파일이 자동적으로 파기된다.
#f.name 속성에 임시 파일의 파일 이름이 담겨 있다. 다른 코드에 이 파일을 전달해야할 필요가 생겼을 때 이 속성을 유용하게 사용할 수 있다. TemporaryFile()과 마찬가지로 생성된 파일의 사용이 끝났을 때 자동으로 삭제된다.
#이런 동작을 원하지 않는다면 delete=False 키워드 인자를 사용한다.
#with NamedTemporaryFile('w+t', delete=False) as f:
    #print('dirname is : ', dirname)
#토론
#임시 파일과 디렉터리를 만들 때 temporaryfile(), namedtemporaryfile(), temporardirectory() 함수가 가장 쉬운 방법이다. 이 함수는 생성과 추후 파기까지 모두 자동으로 처리해 준다. 더 하위 레벨로
#내려가면 mkstemp와 mkdtemp로 임시 파일과 디렉터리를 만들수 있다.
import tempfile
tempfile.mkstemp()
tempfile.mkdtemp()
#하지만 이 함수느 그 이상 관리를 책임지지 않음. mkstemp함수는 단순히 raw OS파일 디스크립터를 반환할 뿐 이를 올바른 파일로 바꾸는 것은 프로그래머의 역할로 남겨둔다.
#이와 유사하게 파일을 제거하는 것도 독자에게 달려있다.
#일반적으로 임시 파일은 /var/tmp와 같은 시스템의 기본 위치에 생성된다. 실제 위치를 찾으려면 tempfile.gettempdir()함수를 사용한다.
#모든 임시 파일 관련 함수는 디렉터리와 이름 규칙을 오버라이드 할 수 있도록 한다. prefix, suffix, dir 키워드 인자를 사용하면 된다.
tempfile.gettempdir()
#마지막으로 tempfile()은 가장 ㄹ안전한 방식으로 파일을 생성한다.,



