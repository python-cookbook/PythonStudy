#데이터 처리 파이프라인 생성
#문제
#데이터 처리를 데이터 처리 파이프라인과 같은 방식으로 순차적으로 처리하고 싶다.(Unix 파이프라인과 비슷하게) 예를 들어 처리해야 할 방대한 데이터가 있지만
#메모리에 한꺼번에 들어가지 않는 경우에 적용할 수 있다.
#해결
#제너레이터 함수를 사용하는 것이 처리 파이프라인을 구현하기에 좋다.
import os,fnmatch,gzip,bz2,re
def gen_find(filepat,top):
    #디렉터리 트리에서 와일드카드 패턴에 매칭하는 모든 파일 이름을 찾는다.
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist,filepat):
            yield os.path.join(path,name)

def gen_opener(filenames):
    #파일 이름 시퀀스를 하나씩 열어 파일 객체를 생성한다. 다음 순환으로 넘어가는 순간 파일을 닫는다.
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()

def gen_concatenate(iterators):
    #이터레이터 시퀀스를 합쳐 하나의 시퀀스로 만든다.
    for it in iterators:
        yield from it #제너레이터 it이 생성한 모든 값을 분출하도록 만드는 구문

def gen_grep(pattern, lines):
    #라인 시퀀스에서 정규식 패턴을 살펴본다.
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line
#이제 이 함수들을 모아서 어렵지 않게 처리 파이프 라인을 만들수 있다. 예를 들어 python이란 단어를 포함하고 있는 모든 로그라인을 찾으려면 다음과 같이한다.
lognames = gen_find('access-log*','www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?!)python', lines)
for line in pylines:
    print(line)

#파이프라인을 확장 하고 싶다면 제너레이터 표혀식으로 데이터를 넣을 수 있다. 예를 들어 다음 버전은 전송한 바이트 수를 찾고 그 총합을 구한다.
lognames = gen_find('access-log*','www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?!)python', lines)
bytecolumn = (line.rsplit(None,1)[1] for line in pylines)
bytes = (int(x) for x in bytecolumn if x != '-')
print('Total',sum(bytes))

#토론
#파이프라인으로 데이터를 처리하는 방식은 파싱, 실시간 데이터 읽기, 주기적 폴링 등 다른 문제에도 사용할 수 있다.
#코드를 이해할 때 yield문이 데이터 생성자처럼 동작하고 for문은 데이터 소비자처럼 동작한다는 점이 중요하다.
#제너레이터가 쌓이면, 각 yield가 순환을 하며 데이터의 아이템 하나를 파이프라인의 다음 단계로 넘긴다. 마지막 예제에서 sum()함수가 실질적으로 프로그램을
#운용하며 제너레이터 파이프라인에서 한 번에 하나씩 아이템을 꺼낸다.
