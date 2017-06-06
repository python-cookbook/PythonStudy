#4.7 이터레이터 일부 얻기


def count(n):
    while True:
        yield n
        n += 1


c = count(0)
c[10:20]

import itertools

for x in itertools.islice(c, 10, 20):
    print(x)

#4.8 순환객체 첫번째 부분 건너뛰기
with open('d:\\data\\passwd.txt') as f:
    for line in f:
        print(line, end='')

from itertools import dropwhile

with open('d:\\data\\passwd.txt') as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line, end='')

from itertools import islice

items = ['a', 'b', 'c', 1, 4, 10, 15]
for x in islice(items, 3, None):
    print(x)

# 4.9 가능한 모든 순열과 조합순환
items = ['a', 'b', 'c']
from itertools import permutations

for p in permutations(items):  # items에 들어간 abc가 들어간 모든 조합을 만들기
    print(p)




items = ['a', 'b', 'c']
from itertools import permutations

for p in permutations(items, 2):  # 원하는 개수를 ,개수로 작성한다.
    print(p)

# combinations()는 순서는 고려하지 않아서 조합이 있어도 출력이 되지 않는다.

# 같은 아이템을 두 번이상 선택
from itertools import combinations

for c in itertools.combinations_with_replacement(items, 3):
    print(c)

# 4.10 인덱스-값 페어 시퀀스 순환
my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list):  # enumerate()함수를 쓰면 index번호도 같이 출력
    print(idx, val)

for idx, val in enumerate(my_list, 1):  # index값을 1부터 출력하려면 입력해주면 된다.
    print(idx, val)  # 넣는 숫자부터 시작한다.

data = [(1, 2), (3, 4), (5, 6), (7, 8)]
for n, (x, y) in enumerate(data):
    print(n, (x, y))

# 4.11 여러 시퀀스 동시 순환
xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99]
for x, y in zip(xpts, ypts):  # zip()함수를 스면 동시에 순환이 가능하다.
    print(x, y)

a = [1, 2, 3]
b = ['w', 'x', 'y', 'z']  # a의 1,2,3이 끝나면 순환이 끝난다.
for i in zip(a, b):
    print(i)

from itertools import zip_longest  # 순환이 끝나도 출력을 하려면

for i in zip_longest(a, b):
    print(i)

# None을 임의로 지정해주고 싶다면
a = [1, 2, 3]
b = ['w', 'x', 'y', 'z', 'a']
for i in zip_longest(a, b, fillvalue=10):  # fillvalue에 입력하는 임의의 수가 출력된다.
    print(i)

# zip()을 사용하면 딕셔너리도 만들 수 있다.
headers = ['name', 'shares', 'price']
values = ['ACME', 100, 490.1]
s = dict(zip(headers, values))
s

# 출력 하려면
for name, val in zip(headers, values):
    print(name, '=', val)

a = [1, 2, 3]
b = [10, 11, 12]
c = ['x', 'y', 'z']
for i in zip(a, b, c):  # zip()함수에는 2개이상도 입력이 가능하다.
    print(i)

# zip()함수는 리스트로도 만들 수 있다.
list(zip(a, b, c))

# 4.12 서로 다른 콘테이너 아이템 순환
from itertools import chain  # chain 함수를 이용하면 두 개의 리스트를 한번에 반환한다.

a = [1, 2, 3, 4]
b = ['x', 'y', 'z']
for x in chain(a, b):
    print(x)

# 4.13 데이터 처리 파이프 라인 생성

import os
import fnmatch
import gzip
import bz2
import re


def gen_find(filepat, top):
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


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


def gen_concatenate(iterators):
    for it in iterators:
        yield from it


def gen_grep(pattern, lines):
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line


if __name__ == '__main__':
    lognames = gen_find('access-log*', 'www')
    files = gen_opener(lognames)
    lines = gen_concatenate(files)
    pylines = gen_grep('(?i)python', lines)
    for line in pylines:
        print(line)
    lognames = gen_find('access-log*', 'www')
    files = gen_opener(lognames)
    lines = gen_concatenate(files)
    pylines = gen_grep('(?i)python', lines)
    bytecolumn = (line.rsplit(None, 1)[1] for line in pylines)
    bytes = (int(x) for x in bytecolumn if x != '-')
    print('Total', sum(bytes))


# 4.14 중첩시퀀스 풀기

# 중첩된 시퀀스를 합쳐 하나의 리스트로 만들고 싶다면
# yield from문이 있는 재귀 제너레이터를 만들어 해결 할 수 있다.
from collections import Iterable


def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x


items = [1, 2, [3, 4, [5, 6], 7], 8]
for x in flatten(items):
    print(x)

# isinstance(x, Iterable)sms 아이템이 순환 가능한 것인지 확인한다.
items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
for x in flatten(items):
    print(x)


# 4.15 정렬된 여러 시퀀스를 변환 후 순환

import heapq

a = [1, 4, 7, 10]
b = [2, 5, 6, 11]
for c in heapq.merge(a, b):  # 시퀀스를 병합후 순환한다.
    print(c)

# 4.16 무한 while 순환문을 이터레이터로 치환

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

f = open('d:\data\passwd.txt')
for chunk in iter(lambda: f.read(10), ''):
    n = sys.stdout.write(chunk)
