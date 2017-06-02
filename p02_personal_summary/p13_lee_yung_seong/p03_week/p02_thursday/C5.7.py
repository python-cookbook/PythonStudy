#압축된 데이터 파일 읽고 쓰기.
#문제
#gzip이나 bz2로 압축한 파일을 읽거나 써야함.
#해결
#모듈을 사용.
import gzip,bz2
with gzip.open('somefile.gz','rt') as f: #혹은 bz2.open()
    text = f.read()

#압축한 데이터를 쓰는 방법은 위와 동일하되 'rt'를 'wt'로 변경하고 f.write(text)로만 변경하면 됨

#모든 입출력은 텍스트를 사용하고 유니코드 인코딩 디코딩을 사용. 바이너리는 wb,rb 모드를 사용하자
#압축한 데이터를 읽거나 쓰는 건 어렵지 않지만 올바른 파일 모드를 선택하는 것은 중요.
#모드를 명시하지 않으면 기본적으로 바이너리 모드. 텍스트 파일을 받을것이라고 가정한 프로그램에는 문제가 생김
#gzip.open()가 bz2.open()은 encoding,errors,newline과 같이 내장 함수 open()과 동일한 인자를 받는다.
#압축한 데이터를 쓸 때는 compresslevel인자로 압축 정도를 지정가능
with gzip.open('somefile.gz','wt',compresslevel=5) as f:
    f.write(text)
#기본 레벨은 9로 가장 높은 압축률. 레벨을 내릴수록 속도는 빠르지만 압축률은 낮아짐.
#마지막으로 잘 알려지지 않은 기능인 gzip.open()과 bz2.open()을 기존에 열려 있는 바이너리 파일의 상위에 위치시키는 것을 보자
import gzip
f = open('file.gz','rb')
with gzip.open(f,'rt') as g:
    text = g.read()

#이렇게 하면 gzip과 bz2 모듈이 파일 같은 객체와 같이 작업 가능

