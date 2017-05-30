            #4.7 이터레이터의 일부 얻기

#문제: 자르기 연산자가 동작을 안한다

    #예제 : itertools.islice() 함수

def count(n):
    while True:
        yield n
        n+=1
        
c = count(0)
c[10:20]
#(실행결과) TypeError: 'generator' object is not subscriptable

import itertools
for x in itertools.islice(c,10,20):
    print(x)
#(실행결과) 
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



            #4.8 순환 객체 첫번째 부분 건너뛰기
    
    #예제 itertools.dropwhile()
with open('/etc/passwd') as f:
    for line in f:
        print(line, end='')
        
#처음나오는 주석 무시
from itertools import dropwhile
with open('/etc/passwd') as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line, end='')
        
#생략할 위치까지 정확한 숫자를 알고 있다면
from itertools import islice
items=['a','b','c',1,4,10,15]
for x in islice(items, 3, None): # <- None 은 3번째 인자 이후 전부 
    print(x)
#(실행결과) 



            #4.9 가능한 모든 순열과 조합 순환
#문제 아이템 컬렉션에 대해 가능한 모든 순열과 조합을 순환하고 싶다.
            
    #예제 itertools.permutations()로 아이템 컬렉션을 받아 가능한 모든 순열을 튜플 시퀀스로 생성한다.
items=['a','b','c']
from itertools import permutations
for p in permutations(items):
    print(p)
#(실행결과) 
#('a', 'b', 'c')
#('a', 'c', 'b')
#('b', 'a', 'c')
#('b', 'c', 'a')
#('c', 'a', 'b')
#('c', 'b', 'a')

for p in permutations(items, 2):  #<- 더 짧은 순열 길이를 위해 길이 인자 지정
    print(p)
#(실행결과) 
#('a', 'b')
#('a', 'c')
#('b', 'a')
#('b', 'c')
#('c', 'a')
#('c', 'b')

    #예제 itertools.combinations()
from itertools import combinations
for c in combinations(items, 3):
    print(c)
#(실행결과) ('a', 'b', 'c')

from itertools import combinations
for c in combinations(items, 2):
    print(c)
#(실행결과) 
('a', 'b')
('a', 'c')
('b', 'c')

from itertools import combinations
for c in combinations(items, 1):
    print(c)
#(실행결과) 
('a',)
('b',)
('c',)



            #4.10 인덱스-값 페어 시퀀스 순환

#문제 시퀀스를 순환할때 어떤 요소를 처리하고 있는지 번호를 알고 싶다.

    #예제 enumerate()
my_list = ['a','b','c']
for idx, val in enumerate(my_list):
    print(idx, val)

#(실행결과) 
#0 a
#1 b
#2 c

my_list = ['a','b','c']
for idx, val in enumerate(my_list, 1):
    print(idx, val)
#(실행결과) 
#1 a
#2 b
#3 c



            #4.11 인덱스-값 페어 시퀀스 순환
#문제 여러 시퀀스를 동시에 순환 zip()
    #예제 zip() 사용
xpts=[1,5,4,2,10,7]
ypts=[101,78,37,15,62,99]
for x, y in zip(xpts, ypts):
    print(x,y)
#(실행결과) 
#1 101
#5 78
#4 37
#2 15
#10 62
#7 99

a=[1,2,3]
b=['w','x','y','z']
for i in zip(a,b):
    print(i)
#(실행결과) 
(1, 'w')
(2, 'x')
(3, 'y')


    #예제 itertools.zip_longest()를 사용
from itertools import zip_longest
for i in zip_longest(a,b):
    print(i)
#(실행결과) 
(1, 'w')
(2, 'x')
(3, 'y')
(None, 'z')

for i in zip_longest(a,b,fillvalue=0):
    print(i)
#(실행결과) 
(1, 'w')
(2, 'x')
(3, 'y')
(0, 'z')



            #4.12 서로 다른 컨테이너 아이템 순환
    #예제  
from itertools import chain
a=[1,2,3,4]
b=['x','y','z']
for x in chain(a,b):
    print(x)
#(실행결과) 
1
2
3
4
x
y
z



            #4.13 데이터 처리 파이프라인 생성
#문제 
    #예제 
import os
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat, top):
    '''
    Find all filenames in a directory tree that match a shell wildcard pattern
    '''
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path,name)

def gen_opener(filenames):
    '''
    Open a sequence of filenames one at a time producing a file object.
    The file is closed immediately when proceeding to the next iteration. 
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
    Chain a sequence of iterators together into a single sequence.
    '''
    for it in iterators:
        yield from it

def gen_grep(pattern, lines):
    '''
    Look for a regex pattern in a sequence of lines
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line



            #4.14 중첩 시퀀스 풀기
#문제 : 중첩된 시퀀스를 합쳐 하나의 리스트로 만들고 싶다

    #예제 yield from 문에 있는 재귀 제너레이터를 만들어 해결
    
from collections import Iterable
def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x

items = [1,2,[3,4,[5,6],7],8] 
for x in flatten(items):
    print(x)           
#(실행결과) 
1
2
3
4
5
6
7
8

items=['Dave','Paula',['Thomas','Lewis']]
for x in flatten(items):
    print(x)
#(실행결과) 
Dave
Paula
Thomas
Lewis



            #4.15 정렬된 여러 시퀀스를 병합 후 순환
#문제 정렬된 시퀀스가 여럿 있고, 이들을 하나로 합친 후 정렬된 시퀀스를 순환하고 싶다.
    #예제 heapq.merge() 사용
import heapq
a=[1,4,7,10]
b=[2,5,6,11]
for c in heapq.merge(a,b):
    print(c)
#(실행결과) 
1
2
4
5
6
7
10
11



            #4.16 무한 while 순환문을 이터레이터로 치환
#문제 함수나 일반적이지 않은 조건 테스트로 인해 무한 while 순환문으로 데이터에 접근

CHUNKSIXE = 8192

def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data == b'':
            break
        process_data(data)
    
#수정된 코드
def reader(s):
    for chunk in iter(lambda: s.recv(CHUNKSIZE), b''):
        process_data(data)
        



