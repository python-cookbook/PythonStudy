#=======================================================================================================================
# 4.7 이터레이터의 일부 얻기
# iterator가 만드는 데이터의 일부를 얻고 싶은데, 일반적인 자르기 연산자(slice ??)가 동작하지 않음
# 제너레이터에도 사용할 수 있다.
# ㄴ itertools.islice() 함수가 이상적
#=======================================================================================================================
def count(n):
    while True:
        yield n                    # 함수내에서 yield가 있으면 이 함수는 생성기라고 부른다. yield를 사용하면
        n += 1                     # 값을 반환하되 함수는 종료되지 않는다..

c = count(0)

import itertools
for x in itertools.islice(c,10,20):
    print(x)

## iterator, generator는 데이터의 길이를 알 수 없으므로, 잘라낼 수 없다. 인덱스도 없다.
# islice()는 원하는 아이템의 조각을 생성하는 iterator지만 한 번 쓰고 버림. sample같은 것?


#=======================================================================================================================
# 4.8 순환 객체 첫 번째 부분 건너뛰기
# 순환 객체 초반 몇 가지 아이템 건네뛰기
# ㄴ itertools.dropwhile() 함수와 순환 객체를 사용하면 된다.
# ㄴ 반환된 이터레이터는 넘겨준 함수가 True를 반환하는 동안은 sequence의 첫번째 아이템을 무시한다.
#=======================================================================================================================
with open('/etc/passwd') as f:
    for line in f:
        print(line, end='')

##
# User Database
#
# Note that this file is consulted directly only when the system is running in single-user mode
# At other times, this information is provided by Open directory
#
nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
root:*:0:0:System Administrator:/var/root:/bin/sh



## 여기서 처음 나오는 주석을 모두 무시하려면 아래와 같이 itertools.dropwhile()을 쓰면 된다.
from itertools import dropwhile
with open('/etc/passwd') as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line, end='')


## 슬라이싱할 것의 위치를 정확히 알고 있다면, itertools.islice()를 쓰면 된다.
from itertools import islice
items = ['a','b','c',1,4,10,15]
for x in islice(items, 3, None):
    print(x)

## for x in islice(items, 3, None): 3번째에서부터 마지막까지       [3:]과 같은 의미다
# 1
# 4
# 10
# 15


## 파일 전체에 걸쳐서 주석으로 시작하는 모든 라인을 무시하는 간단 코드
# 이건 순환 가능한 모든 것(generator, file etc..)에 적용시킬 수 있다.
with open('/etc/passwd') as f:
    lines = (line for line in f if not line.startswith('#'))
    for line in lines:
        print(line, end='')



#=======================================================================================================================
# 4.9 가능한 모든 순열과 조합 순환
# 아이템 컬렉션에 대해 가능한 모든 순열과 조합을 순환할래용
#=======================================================================================================================
## 첫번째. itertools.permutations()로 아이템 컬렉션을 받아 가능한 모든 순열(경우의 수)을 튜플 시퀀스로 생성한다.
# 순열이므로 순서를 고려해서 나가게 된다.

items = ['a','b','c']
from itertools import permutations
for p in permutations(items):
    print(p)

# ('a', 'b', 'c')
# ('a', 'c', 'b')
# ('b', 'a', 'c')
# ('b', 'c', 'a')
# ('c', 'a', 'b')
# ('c', 'b', 'a')

## 위에서처럼 죄다 순환하는게 아니라, 짧게 순환하는 걸 하려면 길이를 지정해줄 수 있다.
for p in permutations(items, 2):                                  # 2개만 순환
    print(p)

# ('a', 'b')
# ('a', 'c')
# ('b', 'a')
# ('b', 'c')
# ('c', 'a')
# ('c', 'b')


## 두번째. itertools.combinations() 입력받은 아이템의 가능한 조합을 생성한다.
# combinations()는 순서는 고려하지 않는다. 때문에 (a,b) = (b,a) 는 동일하다.
from itertools import combinations
items = ['a','b','c']
for c in combinations(items,3):
    print(c)
# ('a', 'b', 'c')

for c in combinations(items,2):
    print(c)
# ('a', 'b')
# ('a', 'c')
# ('b', 'c')

for c in combinations(items,1):
    print(c)
# ('a',)
# ('b',)
# ('c',)


## 조합을 생성할 때, 이미 선택되었던 아이템은 다시 나오지 않지만,
# itertools.combinations_with_replacement() 함수를 사용하면 같은 아이템을 두 번 이상 쓸 수 있다.
items = ['a','b','c']
for c in combinations_with_replacement(items,3):     # 이거 안되염..
    print(c)                                          # NameError: name 'combinations_with_replacement' is not defined


#=======================================================================================================================
# 4.10 인덱스-값 페어 시퀀스 순환
# 시퀀스를 순환시키려고 하는데, 어떤 요소를 처리하는지 번호를 알고 싶다
# ㄴ enumerate() 사용
#=======================================================================================================================
my_list = ['a','b','c']
for idx, val in enumerate(my_list):
    print(idx, val)

# 0 a
# 1 b
# 2 c

## 인덱싱을 할 때 1번부터 시작했으면 좋겠다-하면 넣어주면 됨.
my_list=['a','b','c']
for idx, val in enumerate(my_list,1):
    print(idx,val)

# 1 a
# 2 b
# 3 c


# 파일의 에러 메시지에 파일의 라인 번호를 저장하려면?

def parse_data(filename):
    with open(filename,'rt') as f:
        for lineno, line in enumerate(f,1):
            fields = line.split()
            try:
                count = int(fields[1])
                # ...
            except ValueError as e:
                print('Line {}: Parse error: {}'.format(lineno, e))


## enumerate()는 특정 값의 출현을 위한 오프셋 추적에 활용하기 좋다. 파일내의 단어를 출현한 라인에 매핑하려면
# enumerate()로 단어를 파일에서 발견한 라인 오프셋에 매핑한다.  # 이해못함
word_summary = defaultdict(list)
with open('myfile.txt','r') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    words = [w.strip().lower() for w in line.split()]
    for word in words:
        word_summary[word].append(idx)


#=======================================================================================================================
# 4.11 여러 시퀀스 동시에 순환
# ㄴ zip() 사용
#=======================================================================================================================
xpts = [1,5,4,2,10,7]
ypts = [101,78,37,15,62,99]
for x,y in zip(xpts, ypts):
    print(x,y)

# 1 101
# 5 78
# 4 37
# 2 15
# 10 62
# 7 99


## zip(a,b)는 tuple(x,y)를 생성하는 이터레이터를 생성한다. x=a, y=b
# 이런 순환은 한쪽 시퀀스의 모든 입력이 소비되었을 때 정지하기 때문에 시퀀스 중 짧은 것의 길이를 따라간다.

a = [1,2,3]
b = ['w','x','y','z']
for i in zip(a,b):
    print(i)

# (1, 'w')
# (2, 'x')
# (3, 'y')

# 다른 방식으로 itertools.zip_longest()를 쓸 수 있다.
from itertools import zip_longest
for i in zip_longest(a,b):
    print(i)

# (1, 'w')
# (2, 'x')
# (3, 'y')
# (None, 'z')                   # 한 쪽의 값이 없어도 이렇게 나온다

for i in zip_longest(a,b, fillvalue=0):
    print(i)

# (1, 'w')
# (2, 'x')
# (3, 'y')
# (0, 'z')                      # 한 쪽의 값이 없다면 0으로 출력된다



headers = ['name','shares','price']
values = ['ACME',100,490.1]
s = dict(zip(headers,values))           # zip을 사용해서 두 값을 묶어서 딕셔너리로 만들 수 있다

for name, val in zip(headers,values):
    print(name,'=',val)

# name = ACME
# shares = 100
# price = 490.1


#=======================================================================================================================
# 4.12 서로 다른 컨테이너 아이템 순환
# 여러 객체에 동일한 작업을 수행해야하지만, 객체가 서로 다른 컨테이너에 있다. 코드의 가독성도 유지하고 싶다.
# ㄴ itertools.chain() 메소드 사용
#=======================================================================================================================
from itertools import chain
a = [1,2,3,4]
b = ['x', 'y', 'z']
for x in chain(a,b):
    print(x)

# 1
# 2
# 3
# 4
# x
# y
# z

# chaine()은 일반적으로 모든 아이템에 동일한 작업을 수행하고 싶은데, 이 아이템들이 서로 다른 세트에 포함되어 있을때 쓴다

active_items=set()
inactive_items = set()
for item in chain(active_items,inactive_items):
    # ... da da da..

# 위에 구문을 안 쓰면 아래와같이 해야한다.
# for item in active_items:
#     ...
#
# for item in inactive_items:
#     ...



#=======================================================================================================================
# 4.13 데이터 처리 파이프라인 생성
# 처리해야 할 방대한 데이터가 있지만 메모리에 한꺼번에 들어가지 않는 경우
# ㄴ 제너레이터 함수를 사용하는 것이 처리 파이프라인 구현에 좋다
#=======================================================================================================================
import os
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat, top):
    '''
    디렉토리 트리에서 와일드카드 패턴과 매칭되는 모든 파일명을 찾는다.
    '''
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


def gen_opener(filenames):
    '''
    파일 이름 시퀀스를 하나씩 열어 파일 객체를 생성한다. 다음 순환으로 넘어가는 순간 파일을 닫는다.
    '''
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename,'rt')
        else:
            f = open(filename, 'rt')

        yield f
        f.close()


def gen_concatenate(iterators):
    '''
    이터레이터 시퀀스를 합쳐 하나의 시퀀스로 만든다
    '''
    for it in iterators:
        yield from it


def gen_grep(pattern, lines):
    '''
    라인 시퀀스에서 정규식 패턴을 살펴본다
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line


# 이제 이 함수들을 모아서 어렵지 않게 처리 파이프라인을 만들 수 있다.
## python이란 단어를 포함하고 있는 모든 로그 라인을 찾으려면?

lognames = gen_find('access-log*','www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python',lines)
for line in pylines:
    print(line)                                                 # 왜 결과값이 안나오지?

# 파이프라인 코드에서 yield 문이 데이터 생성자처럼 동작하고, for 문은 데이터 소비자처럼 동작한다.


#=======================================================================================================================
# 4.14 중첩 시퀀스 풀기
# 중첩 시퀀스를 합쳐서 하나의 리스트로
# ㄴ yield from 문이 있는 재귀 제너레이터(...)를 만들어서 쉽게(...) 해결
#=======================================================================================================================
from collections import Iterable
def flatten(items, ignore_types=(str,bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            # isinstance는 현재 내가 사용하는 데이터타입이 무엇인지 비교하여 true/false 를 리턴해 줍니다
            # 여기에서 isinstance는 x가 iterable - 순환 가능한 것인지 확인한다
            # 순환이 가능하면 yield from으로 모든 값을 하나의 서브루틴으로 보낸다
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



#=======================================================================================================================
# 4.15 정렬된 여러 시퀀스를 병합 후 순환
# 정렬된 시퀀스가 여럿있고, 이들을 하나로 합친 다음, 정렬된 시퀀스를 순환하고 싶다
# ㄴ heapq.merge()
#=======================================================================================================================
import heapq
a = [1,4,7,10]
b = [2,5,6,11]
for c in heapq.merge(a,b):
    print(c)

# 1                 # 순서대로 정렬되어져서 나온다
# 2
# 4
# 5
# 6
# 7
# 10
# 11

## heapq.merge()에 넣는 시퀀스는 정렬되어 있어야 한다. 정렬되어있는지 확인을 하지 않는데다, 앞에서부터 읽어가면서
# 가장 작은 것부터 데이터를 출력해줄 뿐이기 때문이다. 해당 시퀀스의 모든 입력을 소비할때까지


#=======================================================================================================================
# 4.16 무한 while 순환문을 이터레이터로 치환
# 함수나 일반적이지 않은 조건으로 인해 무한 while 순환문으로 데이터에 접근하는 코드를 만듬
#=======================================================================================================================
CHUNKSIZE = 8192

## 아래와 같은 이런거 쓰지말고
def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data == b'':
            break
        # print(process_data(data))                     # process_data란 애는 어디서 오는거냐

## iter()를 써서 이렇게 쓰세요
def reader(s):
    for chunk in iter(lambda: s.recv(CHUNKSIZE), b''):
        # print(process_data(data))


# 정말 이 코드가 동작하는가?-를 보려면?
import sys
f = open('/etc/passwd')
for chunk in iter(lambda: f.read(10), b''):
    n = sys.stdout.write(chunk)

# ..라는데 etc/passwd 라는게 없지

