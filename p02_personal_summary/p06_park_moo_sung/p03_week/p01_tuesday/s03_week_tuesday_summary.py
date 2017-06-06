##################################################

# 4.7 이터레이터의 일부 얻기

# itertools.islice() --> 일반적인 자르기 연산자는 이터레이터에 활용 불가

def count(n):
    while True:
        yield n
        n+=1
import itertools

c = count(0)
for x in itertools.islice(c,10,20):
    print(x)

'''
10
11
12
13
14
15
16
17
18
19
'''

##################################################

# 4.8 순환객체 첫 번째 부분 건너뛰기

# itertools.dropwhile()
# --> 함수가 True 반환하는 동안은 시퀀스의 첫 번재 아이템 무시. 이후 전체 시퀀스 생성


from itertools import dropwhile
with open('/etc/passwd') as f:
    for line in dropwhile(lambda  line : line.startswith('#'), f):
        print(line, end='')

## '#'로 시작하는 부분은 무시하고 반환하라

from itertools import islice
items = ['a','b','c',1,4,10,15]
for x in islice(items, 3, None):  # None 부분은 items[3:] 를 의미함
    print(x)
'''
1
4
10
15
'''

# 파일 전체에 걸쳐 주석으로 시작하는 모든 라인 무시

with open('/etc/passwd') as f:
    lines = (line for line in f if not line.startswith('#'))
    for line in lines:
        print(line, end='')

############################################################

# 4.9 가능한 모든 순열과 조합 순환

# itertools.permutations() # 가능한 모든 순열을 튜플 시퀀스로 생성

items = ['a','b','c']
from itertools import permutations
for p in permutations(items):
    print(p)

for p in permutations(items, 2): # 순열의 요소 갯수를 정할 수도 있음
    print(p)

# itertools.combinations() # 입력 받은 아이템의 조합을 생성

from itertools import combinations
for c in combinations(items, 3):
    print(c)

# itertools.combinations_with_replacement() # 조합 출력 시 요소 중복 가능
'''from c in combinations_with_replacement(items, 3): ## 왜 안되지??
    print(c)'''

##########################################################

# 4.10 인덱스-값 페어 시퀀스 순환

# 시퀀스 순환시 번호를 알고 싶다면?

my_list = ['a','b','c']
for idx ,val in enumerate(my_list,1):
    print(idx, val)

from collections import defaultdict
word_summary = defaultdict(list)

with open('myfile.txt', 'r') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    words = [w.strip().lower() for w in line.split()]
    for word in words:
        word_summary[word].append(idx)

# 튜플에 enumerate() 쓸 때 주의사항

data = [(1,2), (3,4), (5,6), (7,8)]
for n, (x,y) in enumerate(data):  # 이렇게 (x,y) 로 나눠서 해줘야 함
    print(n, x, y)

for n, x, y in enumerate(data): # 이렇게 하면 에러남

######################################################

# 4.11 여러 시퀀스 동시에 순환

# zip()함수 사용하기

xpts = [1,5,4,2,10,7]         # 이 때 순환은 길이가 짧은 시퀀스의 입력이 모두 소비되었을 때 종료
ypts = [101,78,37,15,62,99]
for x,y in zip(xpts,ypts):
    print(x,y)

from itertools import zip_longest # 이러면 길이가 긴 시퀀스 입력 모두 소비되었을 때 종료
for i in zip_longest(xpts, ypts):
    print(i)

# zip() 함수의 다양한 활용법

s = dict(zip(headers, values)) # 이러면 두 리스트의 밸류들을 묶어 딕셔너리로 표현 가능

for name, val in zip(headers, values): # 이렇게 동시 출력도 가능
    print(name, '=', val)

a=[1,2,3]
b=[3,2,1]
zip(a,b) # 이터레이터임
list(zip(a,b))
## [(1,3), (2,2), (3,1)] 로 리스트화 됨 !!!!! 신기하네

#############################################################

# 4.12 서로 다른 컨테이너 아이템 순환

# itertools.chain()

from itertools import chain  # 유용할듯!!!
a = [1,2,3,4]
b = ['x','y','z']
for x in chain(a,b): # for x in a+b 는 새로운 시퀀스 만드는 거라서 메모리 측면에서 불리, 리스트 밸류 타입 다른 경우에도 까다로움
    print(x)

'''
1
2
3
4
x
y
z
'''

###############################################################

# 4.13 데이터 처리 파이프라인 생성

# 방대한 데이터가 메모리에 한번에 들어가지 않을때 --> 제너레이터 함수 만들기... 뭔지 모르겠네
# 메모리 효율성 높음 + 유지하기 쉬움

import os
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat, top): # 디렉터리 트리에서 와일드카드 패턴에 매칭하는 모든 파일 이름 찾기
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)

def gen_opener(filenames): # 파일이름 시퀀스를 하나씩 열어 파일 객체 생성. 다음 순환으로 넘어갈 때 파일 닫기
    for filename in filenames:
        if filename.endswith(' .gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith(' .bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()

def gen_concatenate(iterators): # 이터레이터 시퀀스를 합쳐 하나의 시퀀스로 만든다
    for it in iterators:
        yield from it

def gen_grep(pattern, lines): # 라인 시퀀스에서 정규식 패턴 살펴보기
    pat = re.compile(pattern)
    for line in lines :
        if pat.search(line):
            yield line


lognames = gen_find('access-log*','www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python',lines)
for line in pylines :
    print(line)

####################################################

# 4.14 중첩 시퀀스 풀기

# yield from

from collections import Iterable ###### 이건 뭐지? 완전 신기

def flatten(items, ignore_types = (str, bytes)): # isinstance(x, Iterable) 은 아이템이 순환가능한지 확인하는 함수
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x) # 다른 제너레이터 호출할 때 씀 --> for i in flatten(x): yield i 와 같음
        else:
            yield x
items = [1,2, [3,4, [5,6], 7], 8]

for x in flatten(items):
    print(x)

'''
1
2
3
4
5
6
7
8
'''

#######################################################

# 4.15 정렬된 여러 시퀀스를 병합 후 순환

# heapq.merge()

import heapq # 하나로 합치고 정렬한 후 출력할 때 씀
a= [1,4,7,10]
b= [2,5,6,11]
for c in heapq.merg(a,b):
    print(c)

'''
장점! heapq.merge 는 아이템에 순환적으로 접근하며 제공한 시퀀스를 한꺼번에 읽지 않음 
     (긴 시퀀스에도 무리 없이 사용 가능)
주의사항! 각 시퀀스는 미리 정렬되어 있어야 함. 
         heapq.merge 는 각 시퀀스를 앞에서부터 읽어가며 가장 작은 데이터부터 출력하는 것임. 따라서 미리 시퀀스 정렬하기 !!
'''

##########################################################

# 4.16 무한 while 순환문을 이터레이터로 치환

CHUNKSIZE = 8192

def reader(s): # 무한 while 순환문
    while True:
        data = s.recv(CHUNKSIZE)
        if data == b'':
            break
        process_data(data)

def reader(s): # 위에꺼를 이터레이터로 치환하기. 뭔지 모르겠네...
    for chunk in iter(lambda : s.recv(CHUNKSIZE), b''):
        process_data(data)
