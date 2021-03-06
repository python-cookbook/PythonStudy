===============================================================================
#4.7 이터레이터의 일부 얻기
#이터레이터가 만다는 테이터의 일부를 얻고 싶지만, 일반적인자르 기 연산자가 동작하지 않는다.
#"itertools.islice() 함수"

EX1>
def count(n):
    while True:
        yield n
        n += 1

c = count(0)
c[10:20]
#Traceback (most recent call last):

#  File "<ipython-input-1-ee45de20e236>", line 8, in <module>
#    c[10:20]

#TypeError: 'generator' object is not subscriptable

#"이제 islice()를 사용한다.."
import itertools
for x in itertools.islice(c, 10, 20):
    print(x)   
#10
#11
#12
#13
#14
#15
#16
#17
#18
#19



#이터레이터와 제너레이터는 일반적으로 일부를 잘라낼 수 있다.
#데이터의 길이를 알 수 없기 때문이다.(또한 인덱스를 구현하고 있지도 않다.)
#islice()의 실행 결과는 원하는 아이템의 조각을 생성하는 이터레이터지만,
#이는 시작 인덱스까지 모든 아이템을 소비하고 버리는 식으로 수행한다.
#그리고 그 뒤의 아이템은 마지막 인덱스를 만날 때까지 islice()객체가 생성한다.
#주어진 이터레이터 상에서 islice()가 데이터를 소비한다는 점이 중요한다.
#이터레이터를 뒤로 감을 수는 없기 때문에 이 부분을 잘 고려해야 한다.
#뒤로 돌아가는 동작이 중요하다면 데이터를 먼저 리스트로 변환하는 것이 좋다.
===============================================================================





===============================================================================
#4.8 순환 객체 첫 번째 부분 건너뛰기
#순환 객체의 아이템을 순호나하려고 하는데, 처음 몇 가지 아이템에는 관심이 없어 건너뛰고 싶다.
#"itertools 모듈"의 "iterools.dropwhile() 함수"
# 함수와 순환 객체를 넣기
#반호나된 이터레이터는 넘겨준 함수가 True를 반환하는 동안은 시퀀스의 첫 번째 아이템을 무시한다.
#그 후에는 전체 시퀀스를 생성한다.

EX1>
#주석으로 시작하는 파일 읽기
with open('/etc/passwd') as f:
    for line in f:
        print(line, end='')

##
#User Database
#
#Note that this file is consulted directly only when the system is running
#in single-user mode. At other times, this information is provided by
#Open Directory.
...
##
nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
root:*:0:0:System Administrator:/var/root:/bin/sh
...
#?????????

#처음 나오는 주석 모두 무시
from itertools import dropwhile
with open('/etc/passwd') as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line, end='')
...
nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
root:*:0:0:System Administrator:/var/root:/bin/sh
...


#이 예제는 테스트 함수에 따라 첫 번쩨 아이템을 생략하는 방법을 다루고 있다,
#만약 생략해야 할지 정확한 숫자를 알고 있다면 "itertools.islice()를 사용하면 된다.
from itertools import islice
items = ['a', 'b', 'c', 1, 4, 10, 15]
for x in islice(items, 3, None):
    print(x)
#1
#4
#10
#15

#이 예제에서 islice()에 전달한 마지막 None 인자는 처음 세 아이템 뒤에 오는 모든 것을 원함을 명시한다.
#[:3]이 아니라 [3:]을 원함을 의미한다.
===============================================================================





===============================================================================
#4.9 가능한 모든 순열과 조합 순환
#아이템 컬렉션에 대해 가능한 모든 순열과 조합을 순환하고 싶다.
#"itertools 모듈의 세가지 함수
#1_itertools.permutations()
#아이템 컬렉션을 받아 가능한 모든 순열을 튜플 시퀀스로 생성

EX1>
items = ['a', 'b', 'c']
from itertools import permutations
for p in permutations(items):
    print(p)    
#('a', 'b', 'c')
#('a', 'c', 'b')
#('b', 'a', 'c')
#('b', 'c', 'a')
#('c', 'a', 'b')
#('c', 'b', 'a')

EX1_1>
#만약 더 짧은 길이의 순열을 원한다면 선택적으로 길이 인자 지정 가능
for p in permutations(items, 2):
    print(p)
#('a', 'b')
#('a', 'c')
#('b', 'a')
#('b', 'c')
#('c', 'a')
3('c', 'b')



EX2>
#2_itertools.combinations()
#입력 받은 아이템의 가능한 조합 생성
from itertools import combinations
for c in combinations(items, 3):
    print(c)
#('a', 'b', 'c')

for c in combinations(items, 2):
    print(c)
#('a', 'b')
#('a', 'c')
#('b', 'c')

for c in combinations(items, 1):
    print(c)
#('a',)
#('b',)
#('c',)


EX3>
#combinations()의 경우 실제 요소의 순서는 고려하지 않는다.
#따라서 ('a','b')는 ('b','a')(이는 생성되지 않는다)와 동일하게 취급된다.
#조합을 생성할 때, 선택한 아이템은 가능한 후보의 컬렉션에서 제거도니다.
#예를 들어 'a'는 이미 선택되었기 때문에 고려에서 제외된다.)
#intertools.combinations_with_replacement() 함수는 이를 보완해 같은 아이템을
#두번 이상 선택할 수 있게 한다.
for c in combinations_with_replacement(items, 3):
    print(c)
#Traceback (most recent call last):

#  File "<ipython-input-11-44a34314f21b>", line 1, in <module>
#    for c in combinations_with_replacement(items, 3):

#NameError: name 'combinations_with_replacement' is not defined]??????
=============================================================================== 
    
    
    
    
    
===============================================================================   
#4.10 인덱스-값 페어 시퀀스 순환
#시퀀스를 순호나하려고 한다, 이때 어떤 요소를 처리하고 있는지 번호를 알고 싶다.
EX1>
#내장 함수 enumerate()
my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list):
    print(idx, val)
#0 a
#1 b
#2 c


#출력 시 번호를 1번부터 시작하고 싶으면 start인자 전달
my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list, 1):
    print(idx, val)
#1 a
#2 b
#3 c


EX2>
#에러 메시지에 파일의 라인 번호를 저장하고 싶은 경우
def parse_data(filename):
    with open(filename, 'rt') as f:
        for lineno, line in enumerate(f, 1):
            fields = line.split()
            try:
                count = int(fields[1])
                ...
            except ValueError as e:
                print('Line {}: Parse error: {}'.format(lineno, e))
                
#enumerate()는 특정 값의 출현을 위한 오프셋(offset) 추적에 활용하기 좋다.
#따라서 파일 내의 단어를 출현한 라인에 매핑하려면, enumerate() 단어를 파일에서 발견한 라인 오프셋에 매핑
word_summary = defaultdict(list)
with open('myfile.txt', 'r') as f:
    lines = f.readlines()
    for idx, line in enumerate(lines):
        # 현재 라인에 단어 리스트를 생성
        words = [w.strip().lower() for w in line.split()]
        for word in words:
            word_summary[word].append(idx)
#파일 처리 후 word_summary를 출력하면 각 단어를 키로 갖는 딕셔너리 형태가 된다.
#키에 대한 값은 그 단어가 나타난 라인의 리스트가 된다.
#한 라인에 단어가 두 번 나오면 그 라인은 두번 리스팅 되어
#텍스트에 대한 단순 지표를 알아볼 수 있도록 한다.
===============================================================================





===============================================================================
#4_11 여러 시퀀스 동시에 순환
#여러 시퀀스에 들어 있는 아이템을 동시에 순환하고 싶다,
#"zip()함수"
EX1>
xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99]
for x, y in zip(xpts, ypts):
    print(x,y)
#1 101
#5 78
#4 37
#2 15
#10 62
#7 99


EX2>
#zip(a,b)는 tuple(x,y)를 생성하는 이터레이터를 생성한다.(x는 a에서, y는 b에서 가져옴)
#순환은 한쪽 시퀀스의 모든 입력이 소비되었을 때 정지한다.
#따라서 순환의 길이는 입력된 시퀀스 중 짧은 것과 같다.
a = [1, 2, 3]
b = ['w', 'x', 'y', 'z']
for i in zip(a,b):
    print(i)
#(1, 'w')
#(2, 'x')
#(3, 'y')



EX3>
#"itertools.zip_longest()"
from itertools import zip_longest
for i in zip_longest(a,b):
    print(i)
#(1, 'w')
#(2, 'x')
#(3, 'y')
#(None, 'z')

for i in zip_longest(a, b, fillvalue=0):
    print(i)
#(1, 'w')
#(2, 'x')
#(3, 'y')
#(0, 'z')
===============================================================================




===============================================================================
#4.13 서로 다른 컨테이너 아이템 순환
#여러 객체에 동일한 작업을 숳애해야 하지만, 객체가 서로 다른 컨테이너에 들어 있다.
#하지만 중첩된 반복문을 사용해 코드의 가독성을 해치고 싶지 않다.
#itertools.chain() 메소드"
#이 메소드는 순환 가능한 객체를 리스트로 받고 마스킹을 통해 한번에 순환할 수 있는 이터레이터 반환
EX1>
from itertools import chain
a = [1, 2, 3, 4]
b = ['x', 'y', 'z']
for x in chain(a, b):
    print(x)

#1
#2
#3#4
#x
#y
#z



EX2>
#chain()은 일반적으로 모든 아이템에 동일한 작업을 수행하고 싶지만 이 아이템이
#서로 다른 세트에 포함되어 있을 때 사용한다.
#여러 아이템 세트
active_items = set()
inactive_items = set()

#모든 아이템 한번에 순환
for item in chain(active_items, inactive_items):
    #작업
    ...
    
#반복문 두 번 사용하는 것보다 좋음
===============================================================================





===============================================================================
#4.13 데이터 처리 파이프라인 생성
#데ㅐ이터 처리를 데이터 처리 파이프라인과 같은 방식으로 순차적으로 처리하고 싶다.(Unix 파이프라인같이)
#예를 들어, 처리해야 할 방대한 데이터가 있지만 메모리에 한꺼번에 들어가지 않는 경우에 적용 가능

EX1>
#제너레이터 함수를 사용하는 것이 처리 파이프라인을 구현하기 좋다.
#예를 들어 방대한 양의 로그 파일이 들어 있는 디렉토리에 작업을 해야 한다고 가정.
foo/
    access-log-012007.gz
    access-log-022007.gz
    access-log-032007.gz
    ...
    access-log-012008
bar/
    access-log-092007.gz
    ...
    access-log-022008

#각 파일에는 다음과 같은 데이터가 담겨있다..
124.115.6.12 - - [10/Jul/2012:00:18:50 -0500] "GET /robots.txt ..." 200 71
210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /ply/ ..." 200 11875
210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /favicon.ico ..." 404 369
                   61.135.216.105 - - [10/Jul/2012:00:20:04 -0500] "GET /blog/atom.xml ..." 304 -
...

#이 파일을 처리하기 위해 특정 작업 처리를 수행하는 작은 제너레이터 함수의 컬렉션 정의 가능
import os
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat,top):
    '''
    디렉토리 트리에서 와일드카드 패턴에 매칭하는 모든 파일 이름을 찾는다.
    '''
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path,name)
def gen_opener(filenames):
    '''
    파일 이름 시퀀스를 하나씩 열어 파일 객체를 생성한다.
    다음 순환으로 넘어가는 순간 파일을 닫는다.
    '''
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
    '''
    이터레이터 시퀀스를 합쳐 하나의 시퀀스로 만든다.
    '''
    for it in iterators:
        yield from it
        
def gen_grep(pattern, lines):
    '''
    라인 시퀀스에서 정규식 패턴을 살펴본다.
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line

#이 함수들을 모아서 처리 파이프라인
#예를 들어 python이란 단어를 포함하고 잇는 모든 로그 라인을 찾으려면 다음가 같이 한다.
lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)
    
###????????


#파이프라인 확장하고 싶다면, 제너레이터 표현식으로 데이터 넣을 수 있다.
#예를 들어 다음 버전은 전송한 바이트 수를 찾고 그 총합 구하기
EX2>
lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
bytecolumn = (line.rsplit(None,1)[1] for line in pylines)
bytes = (int(x) for x in bytecolumn if x != '-')
print('Total', sum(bytes))
===============================================================================





===============================================================================
#4.14 중첩 시퀀스 풀기
#중첩된 시퀀스를 합쳐 하나의 리스트로 만들고 싶다.
#yield from 문이 있는 재귀 제너레이터
EX1>
from collections import Iterable
def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x
items = [1, 2, [3, 4, [5, 6], 7], 8]

# 1 2 3 4 5 6 7 8 생성
for x in flatten(items):
    print(x)
#1
#2
#3
#4
#5
#6
#7
#8

#아ㅠ의 코드에서 isinstance(x, Iterable)은 아이템이 순환 가능한 것인지 확인한다.
#순환이 가능하다면 yield from 으로 모든 값을 하나의 서브루턴으로 분출한다.
#결과적으로 중첩되지 않은 시퀀스 하나가 만들어진다.
#ㅣ추가적으로 전달 가능한 인자 ignore_types와 not isinstance(x, ignore_types)로
#문자열과 바이트가 순환 가능한 것으로 해석되지 ㅇ낳도록
#리스트에 담겨 있는 문자열을 전달했을 때 문자를 하나하나 펼치지 않고 문자열 단위로 전개
items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
for x in flatten(items):
    print(x)
#Dave
#Paula
#Thomas
#Lewis
===============================================================================





===============================================================================
#4.15 정렬된 여러 시퀀스를 병합 후 순환
#정렬된 시퀀스가 여럿 있고, 이들을 하나로 합친 후 정렬된 시퀀스를 순환하고 싶다.
#"heapq.merge() 함수"
EX1>
import heapq
a = [1,4,7,10]
b = [2,5,6,11]
for c in heapq.merge(a,b):
    print(c)
#1
#2
#4
#5
#6
#7
#10
#11
===============================================================================





===============================================================================
#4.16 무한 while 순환문을 이터레이터로 치환
#함수나 일반적이지 않은 조건 테스트로 인해 무한 while 순환문으로 데이터에 접근하는 코드

EX1>
#입출력과 관련 있는 프로그램 코드
CHUNKSIZE = 8192

def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data == b'':
            break
        process_data(data)

EX1_1>
#iter()를 사용한 수정
def reader(s):
    for chunk in iter(lambda: s.recv(CHUNKSIZE), b''):
        process_data(data)
        
#예제>
import sys
f = open('/etc/passwd')
for chunk in iter(lambda: f.read(10), ''):
    n = sys.stdout.write(chunk)
===============================================================================
