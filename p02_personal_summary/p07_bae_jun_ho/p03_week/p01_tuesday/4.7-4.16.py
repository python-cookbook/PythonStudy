''''''
'''

4장 7절 이터레이터의 일부 얻기 : 이터레이터가 만드는 데이터의 일부를 얻고 싶지만 일반적인 슬라이싱이 되지 않는 경유 itertools.islice() 함수를 사용한다.

이터레이터랑 제너레이터는 데이터의 길이를 알 수 없고 인덱스를 구현하고 있지 않기 때문에 슬라이싱이 불가능하다. 
islice()의 실행  결과는 아이템 조각을 생성해내는 이터레이터지만 시작 인덱스까지 모든 아이템을 소비하고 버린다. 
따라서 뒤로 돌아가는 동작이 중요하면 데이터를 리스트로 변환해야만 한다.  


'''

def count(n):
    while True:
        yield n
        n += 1

c = count(0)

import itertools
for x in itertools.islice(c, 10, 20):
    print(x)


'''

4장 8절 순환 객체 첫 번째 부분 건너뛰기기 : 순환 객체의 아이템을 순환하려고 하는데 스킵하고 검색할 경우 itertools.dropwhile() 함수를 쓴다.



'''

with open('/etc/passwd') as f:
    for line in f:
        print(line, end='')

#

from itertools import islice
items = ['a', 'b', 'c', 1, 4, 10, 15]
for x in islice(items, 3, None):


'''

4장 9절 가능한 모든 순열과 조합 순환 : 아이템 컬렉션에 대해 가능한 모든 순열과 조합을 순환 하고 싶은 경우 itertools.permutations()를 사용한다.


'''

items = ['a', 'b', 'c']
from itertools import permutations
for p in permutations(items):
    print(p)

'''

4장 10절 인덱스 - 값 페어 시퀀스 순환 : 시퀀스를 순환할 때 어떤 요소를 처리하는지 번호를 알고 싶은 경우 내장함수 enumerate()를 사용한다.



'''

my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list):
    print(idx, val)

'''

4장 11절 여러 시퀀스 동시에 순환 : 여러 시퀀스에 있는 아이템을 동시에 순환하고 싶은 경우 zip() 함수를 사용한다.


'''

xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99]
for x, y in zip(xpts, ypts):
    print(x, y)

#

a = [1, 2, 3]
b = ['w', 'x', 'y', 'z']

for i in zip(a,b):
    print(i)

'''

4장 12절 서로 다른 컨테이너 아이템 순환 : 여러 객체에 동일한 작업을 수행해야하지만 객체가 서로 다른 컨테이너에 들어있는 경우 itertools.chain() 메소드를 사용한다.



'''

from itertools import chain
a = [1, 2, 3, 4]
b = ['x', 'y', 'z']
for x in chain(a, b):
    print(x)

'''

4장 13절 데이터 처리 파이프라인 생성 : 데이터 처리를 데이터 처리 파이프라인과 같은 방식으로 순차적으로 처리하고 싶은 경우 제너레이터 함수를 사용하는것이 매우 좋다.

'''

'''

4장 14절 중첩 시퀀스 풀기 : 중첩된 시퀀스를 합쳐서 하나의 리스트로 만들고 싶은 경우 yield from 문으로 재귀 제너레이터를 만들어서 사용한다.


'''

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

'''

4장 15절 정렬된 여러 시퀀스를 병합 후 순환 : 정렬된 시퀀스가 여럿 있고 이들을 합친 후 정렬된 시퀀스로 순환하고 싶은 경우 heapq.merge()를 사용한다.



'''

import heapq
a = [1, 4, 7, 10]
b = [2, 5, 6, 11]
for c in heapq.merge(a,b):
    print(c)


#

import heapq
with open('sorted_file_1', 'rt') as file1, open('sorted_file_2', 'rt') as file2, open('mergeed_file', 'wt') as outf:
    for line in heapq.merge(file1, file2):
        outf.write(line)

'''

4장 16절 무한 while 순환문을 이터레이터로 치환 : 함수나 일반적이지 않은 조건 테스트로 인해 무한 while 순환문으로 데이터에 접근하는 코드를 만들었을 때 입출력과 관련있는
                                           프로그램에 다음 코드를 사용한다. iter() 함수를 사용한다. iter()함수는 선택적으로 인자 없는 호출 가능 객체와 종료값을
                                           입력으로 받는다. 이렇게 사용하면 주어진 종료 값을 반환하기 전까지 무한 반복해서 호출 가능 객체를 호출한다.
                                           
'''

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
f = open('etx/passwd')
for chink in iter(lambda: f.read(10), ''):
    n = sys.stdout.write(chunk)