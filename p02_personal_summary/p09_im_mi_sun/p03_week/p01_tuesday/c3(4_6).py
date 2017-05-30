#####4.6 추가 상태를 가진 제너레이터 함수 정의
from collections import deque
class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines =lines
        self.history = deque(maxlen =histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines,1):
            self.history.append((lineno,line))
            yield line
    def clear(self):
        self.history.clear()

# 클래스를 사용하려면 일반 제너레이터 함수처럼 대애햐 함 인스턴스를 만들기 때문에 history속성이나 clear()메소드 같은 내부 속성에 접근할 수 있음

with open('somefile.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno,hline), end ='')


f = open('somefile.txt')
lines =linehistory(f)
next(lines) #제너레이터라서 실행이 안됨

#iter()를 먼저 호출하고 순환 시작
it = iter(lines)
next(it) #'hello word\n
next(it) # this is a test\n'



#####4.7 이터레이터의 일부 얻기
def count(n):
    while True:
        yield n
        n += 1
c = count(0)
#c[10:20]
# Traceback (most recent call last):
#   File "<input>", line 6, in <module>
# TypeError: 'generator' object is not subscriptable


import itertools
for x in itertools.islice(c,10,20):
    print(x)

# 10
# 11
# 12
# 13
# 14
# 15
# 16
# 17
# 18
# 19

with open('/etc/passwd') as f:
    for line in f:
    print(line, end='')

#User database
#Note that this file is consulted directly only when the system is running
#in single-user mode. At other times, this information is provided by
#Open Directory
#..
#nobody : *:-2:-2:Unpriviledged User:/var/empty:/usr/bin/false
#root:*:0:0:System Administrator :/var/root:/bin/sh

#처음 나오는 주석을 무시하려면 아래와 같이 함
from itertools import dropwhile
with open('etc/passwd') as f:
    for line in dropwhile(lambda line: line.startswith('#'),f):
        print(line,end='')
#nobody : *:-2:-2:Unpriviledged User:/var/empty:/usr/bin/false
#root:*:0:0:System Administrator :/var/root:/bin/sh

#어디까지 생략해야할 지 정확한 숫자를 알고 있다면 itertools.islice()  tkdyd
from itertools import islice
items = ['a','b','c',1,4,10,15]
for x in islice(items, 3, None):
    print(x)

#islice()에 전달한 마지막 None인자는 처음 세 아이템 뒤에 오는 모든 것을 원한 :3 이 아니라 3:
#처음 주석을 건너뜀
with open('/etc/passwd') as f:
    while True:
        line = next(f, '')
        if not line.startswith('#'):
            break
#남아 있는 라인 처리
while line:
    #의미 있는 라인으로 치환
    print(line, end='')
    line = next(f, None)


#순환 객체 첫부분을 건너뛰는 것은 간단히 전체를 걸러내는 것과는 조금 다름.
with open('etc/passwd') as f:
    lines = (line for line in f if not line.startswith('#'))
    for line in lines:
        print(line, end='')

#파일 전체에 걸쳐 주석으로 시작하는 모든 라인 무시
# 제공한 함수가 만족하는 동안의 아이템은 무시하고 그 뒤에 나오는 아이템은 필터링 없이 모두 반환
# 순환 가능한 모든 것에 적용 가능하다. 처음에 크기를 알 수 없는 제너레이터 파일 등 모든 것이 포함됨

#####4.9 가능한 모든 순열과 조합 순환
items =['a','b','c']
from itertools import permutations
for p in permutations(items):
    print(p)

# ('a', 'b', 'c')
# ('a', 'c', 'b')
# ('b', 'a', 'c')
# ('b', 'c', 'a')
# ('c', 'a', 'b')
# ('c', 'b', 'a')
#
#짧은 길이의 순열을 원할 경우 선택적으로 길이 인자 지정 가능
for p in permutations(items,2):
    print(p)
# ('a', 'b')
# ('a', 'c')
# ('b', 'a')
# ('b', 'c')
# ('c', 'a')
# ('c', 'b')
for p in permutations(items,1):
    print(p)
# ('a',)
# ('b',)
# ('c',)
#itertools.combinations()는 입력 받은 아이템의 가능한 조합 생성
from itertools import combinations
for c in combinations(items,3): #애는 숫자 안써주면 오류남
    print(c)
# ('a', 'b', 'c')
for c in combinations(items,1):
    print(c)
# ('a',)
# ('b',)
# ('c',)
from itertools import combinations_with_replacement
for c in combinations_with_replacement(items,3): #중복 조합
    print(c)

#####4.10 인덱스값 페어 시퀀스 순환
my_list =['a','b','c']
for idx, val in enumerate(my_list):
    print(idx,val)
# 0 a
# 1 b
# 2 c

my_list =['a','b','c']
for idx, val in enumerate(my_list,1):
    print(idx,val)
# 1 a
# 2 b
# 3 c

#에러메세지에 파일의 라인 번호를 저장하고 싶은 경우 유용
def parse_data(filename):
    with open(filename, 'rt') as f:
        for lineno, line in enumerate(f,1):
            fields = line.split()
            try:
                count=int(fields[1])
            except ValueError as e:
                print('Line {}: Parse error: {}'.format(lineno,e))
from collections import defaultdict
word_summary= defaultdict(list)
with open('myfile.txt','r') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    words = [w.strip().lower() for w in line.split() ]
    for word in words:
        word_summary[word].append(idx)
# 파일 처리 후 word_summary를 출력하면 각 단어를 키로 갖는 딕셔너리 형태가 됨
#키에 대한 값은 그 단어가 나타난 라이늬 리스트가 됨
# 한 라인에 두번 나오면 그 라인은 두번 리스팅 되어 단순 지표를 알아볼 수 있도록 함

data = [(1,2),(3,4),(5,6),(7,8)]
#올바른 방법
# for n, (x,y) in enumerate(data):
# for n,x,y in enumerate(data):

#####4.11 여러 시퀀스 동시에 순환
xpts = [1,5,4,2,10,7]
ypts = [101,78,37,15,62,99]
for x,y in zip(xpts,ypts):
    print(x,y)

# 1 101
# 5 78
# 4 37
# 2 15
# 10 62
# 7 99
a = [1,2,3]
b = ['x','y','z','w','a']
from itertools import zip_longest
for i in zip_longest(a,b):
    print(i)
# (1, 'x')
# (2, 'y')
# (3, 'z')
# (None, 'w') #길이 안맞는 애들은 다 none

for i in zip_longest(a,b,fillvalue=0):
    print(i) #길이 안맞는 애들은 다 0
# (1, 'x')
# (2, 'y')
# (3, 'z')
# (0, 'w')
# (0, 'a')

headers = ['name','shares','price']
values = ['ACME',100,409.1]

s = dict(zip(headers,values))
print(s) #{'name': 'ACME', 'shares': 100, 'price': 409.1}

for name, val in zip(headers,values):
    print(name, '=',val)

# name = ACME
# shares = 100
# price = 409.1

a = [1,2,3]
b = [10,11,12]
c = ['x','y','z']
for i in zip(a,b,c):
    print(i)
# (1, 10, 'x')
# (2, 11, 'y')
# (3, 12, 'z')

zip(a,b)
list(zip(a,b))

######## 4.12 서로 다른 컨테이너 아이템 순환
from itertools import chain
a = [1,2,3,4]
b = ['x','y','z']
for x in chain(a,b):
    print(x)
# 1
# 2
# 3
# 4
# x
# y
# z
#여러아이템 세트
active_items = set()
inactive_items = set()

#모든 아이템 한번에 순환
for item in chain(active_items, inactive_items):
    #작업

#이거는 별루임
for item in active_items:
    #작업
for item in inactive_items:
    #작업

######## 4.13 데이터 처리 파이프 라인 생성
import os
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat, top):
    #디렉토리 트리에서 와일드 카드 패턴에 매칭하는 모든 파일 이름을 찾음
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path,name)

def gen_opener(filenames):
    #파일 이름 시퀀스를 하나씩 열어 파일 객체 생성
    # 다음 순환으로 넘어가는 순간 파일을 담음
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
    # 이터레이터 시퀀스를 합쳐 하나의 시퀀스로 만듦
    for it in iterators:
        yield from it

def gen_grep(pattern, lines):
    #라인 시퀀스에서 정규식 패턴을 살펴봄
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line

lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?!)python', lines)
for line in pylines:
    print(line)

#파이프 라인을 확장하고 싶으면 제너레이터 표현식으로 표현식을 넣을 수 있음
#전송한 바이트 수를 찾고 총합을 구함
lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?!)python', lines)
bytecolumn = (line.rsplit(None,1)[1] for line in pylines)
bytes = (int(x) for x in bytecolumn if x != '-')
print('Total', sum(bytes))

#####4.14 중첩 시퀀스 풀기
from collections import Iterable
def flatten(items, ignore_types=(str,bytes)):
    for x in items:
        if isinstance(x,Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x
items = [1,2,[3,4,[5,6],7],8]
for x in flatten(items):
    print(x)

# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8

items = ['Dave','Paula',['Thomas','Lewis']]
for x in flatten(items):
    print(x)

def flatten(items, ignore_types=(str,bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            for i in flatten(x):
                yield i
        else:
            yield x
#####4.15 정렬된 여러 시퀀스 반환
import heapq
a = [1,4,7,10]
b = [2,5,8,6,11]
for c in heapq.merge(a,b): #번갈아 가면서 출력되넹
    print(c)
# 1
# 2
# 4
# 5
# 7
# 8
# 6
# 10
# 11

import heapq
with open('sorted_file_1', 'rt') as file1, \
    open('sorted_file_2','rt') as file2, \
    open('merged_file','wt') as outf:

    for line in heapq.merge(file1,file2):
        outf.write(line)

#####4.16 무한 while순환문을 이터레이터로 순환
CHUNKSIZE = 8192
def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data == b'':
            break
        process_data(data)

def reader(s):
    for chunk in iter(lambda: s.recv(CHUNKSIZE), b''):
        process_data(data)

import sys
f = open('/etc/passwd')
for chunk in iter(lambda : f.read(10),''):
    n = sys.stdout.write(chunk)

