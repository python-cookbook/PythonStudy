##########################################################################################################
# 4.13] 데이터 처리 파이프라인 생성
#   * 데이터 처리를 파이프라인과 같이 순차적으로 처리하고 싶다.
#     예를 들어 처리해야 할 방대한 데이터가 있지만 메모리가 한번에 들어가지 않을 경우에 적용할 수 있다.
#
#   * 파이프라인으로 데이터를 처리하는 방식은 파싱, 실시간 데이터 읽기, 주기적 폴링 등 다른 문제에도 사용할 수 있다.
#   * 장점 :
#       1) 각 제너레이터 함수를 작게 모듈화할 수 있다.
#          대개 모듈화된 제너레이터 함수는 아주 일반적이기 때문에 여러 곳에서 재사용할 수 있다. 코드 가독성도 높다.
#       2) 메모리 효율성이 높다.
##########################################################################################################
import os
import fnmatch
import gzip
import bz2
import re

## 대량의 로그 파일이 들어있는 디렉터리에서 작업을 하기 위한 파이프라인

#디렉터리 트리에서 와일드카드 패턴에 매칭하는 모든 파일 이름을 찾는다.
def gen_find(filepat, top):
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)

# 파일 이름 시퀀스를 하나씩 열어 파일 객체를 생성한다.
# 다음 순환으로 넘어가는 순간 파일을 닫는다.
def gen_opener(filenames):
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()

# 이터레이터 시퀀스를 합쳐 하나의 시퀀스로 만든다.
def gen_concatenate(iterators):
    for it in iterators:
        yield from it

# 라인 시퀀스에서 정규식 패턴을 살펴본다.
def gen_grep(pattern, lines):
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line

## python이라는 단어를 포함한 모든 로그 라인을 찾는 파이프라인
lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)

## 파이프라인 확장 : 전송한 바이트 수를 찾고 그 총합을 구한다.
lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
bytecolumn = (line.rsplit(None,1)[1] for line in pylines)
bytes = (int(x) for x in bytecolumn if x != '-')
print('Total', sum(bytes))