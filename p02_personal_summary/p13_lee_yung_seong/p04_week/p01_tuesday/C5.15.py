#망가진 파일 이름 출력
#문제
#프로그램에서 디렉터리 리스트를 받아 파일 이름을 출력하려고 할 때, UnicodeEncodeError 예외와 surrogates not allowed 메시지가 발생하면서 프로그램이 죽는다.
#해결
#출처를 알 수 없는 파일 이름을 출력할 때 다음 코드로 에러를 방지한다.
def bad_filename(filename):
    return repr(filename)[1:-1]

try:
    print(filename)
except UnicodeEncodeError:
    print(bad_filename(filename))
#토론
#자주 발생하지는 않지만 파일 시스템에 발생할 수 있는 아주 귀찮은 문제.
#기본적으로 파이썬은 모든 파일 이름이 sys.getfilesystemencode()이 반환하는 값으로 인코딩 되어 있다고 가정한다.
#하지만 특정 파일 시스템은 인코딩 규칙을 따르도록 강제하지 않아서 올바르지 않은 인코딩을 사용한 파일 이름이 생기기도 한다.
#이런 일이 비일비재하게 발생하지는 않지만 세상에는 우리가 예측하지 못하는 동작을 하는 사용자가 어디에 나있으니 조심해야 한다.
#os.listdir() 와 같은 명령을 실행할 때 망가진 파일 이름을 사용하면 파이썬에 문제가 생긴다. 한편으로 잘못된 이름이라고 단순히 무시해 버릴 수 없다.
#반면 이 이름을 올바른 텍스트 문자열로 변환할 수도 없다. 파이썬의 해결책은 디코딩할 수 없는 바이트 값 \xhh를 Unicode 문자 \udchh로 변환하는 소위
#대리 인코딩으로 매핑하는것이다.
#UTF-8이 아닌 Latin-1으로 인코딩한 bad.txt를 포함한 디렉터리 리스트가 어떻게 보이는지 예제를 보자.
import os
files = os.listdir('.')
files

#파일 이름을 다루거나 open()과 같은 함수에 전달하는 코드가 있다면 모두 정상적으로 동작한다. 이 파일 이름을 출력하려고 할 때만 문제가 발생한다.
#특히 선행 리스트를 출력하려고 하면 프로그램이 비 정상적으로 종료한다.
for name in files:
    print(name)
#프로그램이 죽는 이유는 \udce4가 잘못된 유니코드이기 때문이다. 대리 짝으로 알려진 문자 두개의 조합이다. 하지만 첫번째 반쪽이 없기 때문에 올바른 유니코드라 할 수 없다.
#따라서 올바른 출력을 하려면 망가진 파일 이름을 발견했을 때 교정작업을 해야 한다.
for name in files:
    try:
        print(name)
    except UnicodeEncodeError:
        print(bad_filename(name))
#bad_filename() 함수를 어떻게 처리할지는 모두 프로그래머에게 달려 있다. 혹은 그 값을 다음과 같이 재 인코딩할 수 있다.
def bad_filename(filename):
    temp = filename.encode(sys.getfilesystemencoding(), errors='surrogateescape')
    return temp.decode('latin-1')
for name in files:
    try:
        print(name)
    except UnicodeEncodeError:
        print(bad_filename(name))
#파일 이름과 파일 시스템에 신뢰할 수 있게 동작하는 프로그램을 작성하려면 고려해야할 문제이다. 그렇지 않으면 주말에 사무실에 불려 나와 알 수 없는 버그를 고치고 있을듯..

