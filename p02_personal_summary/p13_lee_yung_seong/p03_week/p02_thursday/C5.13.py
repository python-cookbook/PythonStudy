#디렉터리 리스팅 구하기
#문제 디렉터리나 파일 시스템 내부의 파일 리스트를 구하고 싶다.
#해결 os.listdir()함수로 디렉터리 내의 파일 리스트를 얻는다.
import os
names = os.listdir('somedir')#이렇게 하면 디렉터리와 파일 , 서브 디렉터리, 심볼릭 링크 등 모든 것을 구할 수 있다.
#만약 데이터를 걸러 내야 한다면 os.path 라이브러리의 파일에 리스트 컴프리헨션 을 사용한다.
import os.path
names = [name for name in os.listdir('somedir') if os.path.isfile(os.path.join('somedir',name))] #일반파일 모두 구하기
#디렉터리 모두 구하기
dirnames = [name for name in os.listdir('somedir') if os.path.isdir(os.path.join('somedir',name))]
#문자열의 startswith()와 endswith() 메소드를 사용하면 디렉터리의 내용을 걸러 내기 유용하다.
pyfiles = [name for name in os.listdir('somedir') if name.endswith('py')]
#파일 이름 매칭을 하기 위해 glob이나 fnmatch 모듈을 사용한다.
import glob
pyfiles = glob.glob('somefile/*.py')
from fnmatch import fnmatch
pyfiles = [name for name in os.listdir('somedir') if fnmatch(name, '*.py')]
#토론
#디렉터리 리스트를 구하기는 쉽지만, 앞에 나온 방법으로는 엔트리의 이름만 얻을 수 있다.
#만약 파일 크기나 수정 날짜 등 메타데이턱 ㅏ필요하다면 os.path 모듈의 추가적인 함수를 사용하거나 os.stat()함수를 사용한다.

#디렉터리 리스트 구하기
import os, os.path, glob
pyfiles = glob.glob('*.py')
#파일 크기와 수정 날짜 구하기
name_sz_date = [(name, os.path.getsize(name),, os.path.getmtime(name)) for name in pyfiles]
for name, size, mtime in name_sz_date:
    print(name,size,mtime)

#대안 : 파일 메타데이터 구하기
file_metadata=[(name, os.stat(name)) for name in pyfiles]
for name, meta in file_metadata:
    print(name,meta.st_size,meta.st_mtime)

#마지막으로 파일 이름을 다룰 때 인코딩과 관련된 문제가 발생할 수 있다. 일반적으로 os.listdir() 와 같은  함수가 반환하는 엔트리는 파일 시스템의 기본 인코딩으로 디코드 된다.
#허나 특정 상황에서는 파일 이름을 디코딩 하는 것이 불가능 할 수도 있다.