#4.7 이터레이터의 일부 얻기
#이터레이터가 만드는 데이터의 일부를 얻고 싶지만, 일반적인 자르기 연산자가 동작하지 않는다.

#A.이터레이터와 제너레이터의 일부를 얻는데는 itertools.islice()함수가 가장 이상적이다.

def count(n):
    while True:
        yield n
        n += 1

c=count(0)
#c[10:20]

#Traceback (most recent call last):
#File "C:/python/PythonStudy/PythonStudy/p02_personal_summary/p02_kim_myeong_hak/p03_week/p01_tuesday/p03_sum.py", line 12, in <module>
#c[10:20]  TypeError: 'generator' object is not subscriptable

#이제 islice()를 사용한다.
import itertools
for x in itertools.islice(c,10,20):
    print(x)

#토론
#이터레이터와 제너레이터는 일반적으로 일부를 잘라낼 수 없다. 왜냐하면 데이터의 길이를 알 수 없기 때문이다.
#islice()의 실행결과는 원하는 아이템의 조각을 생성하는 이터레이터지만, 이는 시작 인덱스까지 모든 아이템을 소비하고 버리는 식으로 수행한다.
#그리고 그 뒤의 아이템은 마지막 인덱스를 만날때까지 islice 객체가 생성한다.
#주어진 이터레이터 상에서 islice()가 데이터를 소비한다는 점이 중요하다. 이터레이터를 뒤로 감을 수는 없기때문에 이 부분을 잘 고려해야한다. 뒤로 돌아가는 동작이 중요하다면 데이터를 먼저 리스트로 변환하는것이 좋다.


#4.8 순환 객체 첫 번째 부분 건너뛰기
#Q 순환 객체의 아이템을 순환하려고 하는데, 처음 몇가지 아이템에는 관심이 없어 건너뛰고 싶다


with open('/etc/passwd') as f:
    for line in f:
        print(line, end='')

##
# User Database
#
# Note that this file is consulted directly only when the system is running
# in single-user mode. At other times, this information is provided by
# Open Directory.


##
#nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
#root:*:0:0:System Administrator:/var/root:/bin/sh

#처음 나오는 주석을 무시하려면 다음과 같이 한다.

from itertools import dropwhile
with open('/etc/passwd') as f:
     for line in dropwhile(lambda line: line.startswith('#'), f):
         print(line, end='')


#nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
#root:*:0:0:System Administrator:/var/root:/bin/sh

#이 예제는 테스트 함수에 따라 첫 번째 아이템을 생략하는 방법을 다루고 있다. 만약 어디까지 생략해야 할지 정확한 숫자를 알고 있다면
#itertools .islice()를 사용하면 된다.

from itertools import islice
items = ['a', 'b', 'c', 1, 4, 10, 15]
for x in islice(items, 3, None):
    print(x)
#1,4,10,15
#이 예제에서 islice()에 전달한 마지막 None인자는 처음 세 아이템 뒤에 오는 모든 것을 원함을 명시한다
#[:3]이 아니라 [3:]을 원함을 의미한다.


#토론

#dropwhile()과 islice()함수는 다음과 같이 복잡한 코드를 작성하지 않도록 도와준다.
with open('/etc/passwd') as f:
    #처음 주석을 건너뛴다.
    while True:
        line = next(f, '')
        if not line.startswith('#'):
            break

    #남아 있는 라인을 처리한다
    while line:
        # 의미 있는 라인으로 치환한다.
        print(line, end='')
        line = next(f, None)

#순환 객체의 첫 부분을 건너뛰는 것은 간단히 전체를 걸러내는 것과는 조금 다르다.
#예를 들어 이번 레시피의 첫 부분을 다음과 같이 수정할 수 있다.

with open('/etc/passwd') as f:
    lines = (line for line in f if not line.startswith('#'))
    for line in lines:
        print(line, end='')


#이렇게 하면 파일 전체에 걸쳐 주석으로 시작하는 모든 라인을 무시한다. 하지만 레시피에서 제시한 방법대로
#하면 제공한 함수가 만족하는 동안의 아이템을 무시하고, 그 뒤에 나오는 아이템은 필터링 없이 모두 반환한다.


#4.9 가능한 모든 순열과 조합 순환
#Q 아이템 컬렉션에 대해 가능한 모든 순열과 조합을 순환하고 싶다.

#A itertools 모듈은 이와 관련있는 세 함수를 제공한다. 첫째는 itertools.permutations()로,
#아이템 컬렉션을 받아 가능한 모든 순열을 튜플 시퀀스로 생성한다.

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

#만약 더 짧은 길이의 순열을 원한다면 선택적으로 길이 인자를 지정할 수 있다.

for p in permutations(items, 2):
    print(p)

#('a', 'b')
#('a', 'c')
#('b', 'a')
#('b', 'c')
#('c', 'a')
#('c', 'b')


#itertools.combinations()는 입력 받은 아이템의 가능한 조합을 생성한다
from itertools import combinations
items = ['a', 'b', 'c']

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

#combinations()의 경우 실제 요소의 순서는 고려하지 않는다. 따라서 ('a','b')는
#('b','a')이는 생성되지 않는다)와 동일하게 취급된다.
#조합을 생성할 때, 선택한 아이템은 가능한 후보의 컬렉션에서 제거된다.
#예를 들어 'a' 는 이미 선택되었기 때문에 고려에서 제외된다.
#itertools.combinations_with_replacement() 함수는 이를 보완해 같은 아이템을 두번 이상 선택할 수 있게 한다.

for c in combinations_with_replacement(items, 3):
    print(c)

#4.10 인덱스 - 값 페어 시퀀스 순환
#시퀀스를 순환하려고 한다. 이때 어떤 요소를 처리하고 있는지 번호를 알고 싶다.

#A 이문제는 내장 함수 enumerate() 를 사용하면 간단히 해결할 수 있다.

my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list):
    print(idx, val)

#0 a
#1 b
#2 c


#출력시 번호를 1번부터 시작하고 싶으면 start 인자를 전달한다
my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list, 1):
     print(idx, val)
#1 a
#2 b
#3 c

#이번 예제는 에러 메시지에 파일의 라인 번호를 저장하고 싶은 경우에 유용하다.

def parse_data(filename):
    with open(filename, 'rt') as f:
        for lineno, line in enumerate(f, 1):
            fields = line.split()
            try:
                count = int(fields[1])
            except ValueError as e:
                print('Line {}: Parse error: {}'.format(lineno, e))


#enumerate()는 예를 들어 특정 값의 출현을 위한 오프셋(offset) 추적에 활용하기 좋다.
#따라서 파일 내의 단어를 출현한 라인에 매핑하려면, enumerate()로 단어를 파일에서 발견한 라인 오프셋에 매핑한다.


word_summary = defaultdict(list)

with open('myfile.txt', 'r') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    #현재 라인에 단어 리스트를 생성
    words = [w.strip().lower() for w in line.split()]
    for word in words:
        word_summary[word].append(idx)


#파일 처리후 word_summary를 출력하면 이는 각 단어를 키로 갖는 딕셔너리 형태가 된다.
#키에 대한 값은 그 단어가 나타난 라인의 리스트가 된다.
# 한라인에 단어가 두 번 나오면 그 라인은 두 번 리스팅 되어 텍스트에 대한 단순 지표를 알아볼 수 있도록 한다.



#토론
#카운터 변수를 스스로 다루는 것에 비해 enumerate()를 사용하는 것이 훨씬 보기 좋다.
#예를 들어 다음과 같은 코드로 카운터 변수를 만들 수 있다.
lineno = 1
for line in f:
    #라인처리
    #...
    lineno += 1

#하지만 enumerate()를 사용하는 것이 훨씬 더 세련된 방식이다.
for lineno, line in enumerate(f):
    #라인 처리
    ...


#enumerate()가 반환하는 값은 연속된 튜플을 반환하는 이터레이터인 enumerate() 객체의 인스턴스이다.
#이 튜플은 전달한 시퀀스에 next() 를 호출해 반환된 카운터와 값으로 이루어져있다.
#사소한 문제이긴 하지만 주의해야 할 점이 하나 있다. 한 번 더 풀어줘야 하는 튜플의 시퀀스에 enumerate()를 사용할 때는
#실수를 범하기 쉽다.

data = [ (1, 2), (3, 4), (5, 6), (7, 8) ]

#올바른 방법
for n, (x, y) in enumerate(data):

#에러!
for n, x, y in enumerate(data):


#4.11 여러 시퀀스 동시 순환
#여러 시퀀스에 들어 있는 아이템을 동시에 순환하고 싶다.

xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99]
for x, y in zip(xpts, ypts):
    print(x, y)


#zip(a,b)는 tuple (x,y)를 생성하는 이터레이터를 생성한다
#x는 a에서 y는 b에서 가져온다
#순환은 한쪽 시퀀스의 모든 입력이 소비되었을 때 정지한다
#따라서 순환의 길이는 입력된 시퀀스 중 짧은 것과 같다.

a = [1, 2, 3]
b = ['w', 'x', 'y', 'z']
for i in zip(a,b):
    print(i)

#(1, 'w')
#(2, 'x')
#(3, 'y')

#이렇게 동작하는 방식이 맘에 안들면
#itertools.zip_longest()를 사용해야 한다

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

#토론
#zip()은 데이터를 묶어야 할 때 주로 사용한다.
#예를들어 열 헤더와 값을 리스트로 가지고 있다고 가정해 보자.

headers = ['name', 'shares', 'price']
values = ['ACME', 100, 490.1]

#zip()을 사용하면 두 값을 묶어 딕셔너리로 만들 수 있다.

s = dict(zip(headers,values))

#혹은 출력하려고 한다면 다음과 같은 코드를 작성한다.
for name, val in zip(headers,values):
    print(name,'=',val)

#일반적이진 않지만 zip()에 시퀀스를 두개 이상 입력할 수 있다.
#이런 경우 결과적으로 튜플에는 입력한 시퀀스의 개수 만큼의 아이템이 포함된다.

a = [1, 2, 3]
b = [10, 11, 12]
c = ['x','y','z']
for i in zip(a, b, c):
    print(i)
(1, 10, 'x')
(2, 11, 'y')
(3, 12, 'z')

#마지막으로 zip()이 결과적으로 이터레이터를 생성한다는 점을 기억하도록 하자.
#묶은 값이 저장된 리스트가 필요하다면 list() 함수를 사용한다.

ip(a, b)
<zip object at 0x1007001b8>
list(zip(a, b))
[(1, 10), (2, 11), (3, 12)]


#4.12 서로 다른 컨테이너 아이템 순환
#Q 여러 객체에 동일한 작업을 수행해야 하지만, 객체가 서로 다른 컨테이너에 들어있다.
#하지만 중첩된 반복문을 사용해 코드의 가독성을 해치고 싶지 않다.

#A itertools.chain() 메소드로 이 문제를 간단히 해결할 수 있다.
# 이 메소드는 순환 가능한 객체를 리스트로 받고 마스킹을 통해 한번에 순환할 수 있는 이터레이터를 반환한다.

from itertools import chain
a = [1, 2, 3, 4]
b = ['x', 'y', 'z']
for x in chain(a, b):
    print(x)

#chain()은 일반적으로 모든 아이템에 동일한 작업을 수행하고 싶지만
#이 아이템이 서로 다른 세트에 포함되어 있을때 사용한다.

#여러 아이템 세트
active_items = set()
inactive_items = set()

#모든 아이템 한번에 순환
for item in chain(active_items, inactive_items):
    #작업

#앞에 나온 방식은 반복문을 두 번 사용하는 것보다 훨씬 보기 좋다.

for item in active_items:
#작업
for item in inactive_items:
#작업


#토론
#itertools.chain() 은 하나 혹은 그 이상의 순환 객체를 인자로 받는다.
#그리고 입력받은 순환 객체 속 아이템을 차례대로 순환하는 이터레이터를 생성한다. 큰차이는 아니지만,
#우선적으로시퀀스를 하나로 합친 다음 순환하는것보다 chain()을 사용하는것이 더 효율적이다
#비효율적
for x in a + b:

#효율적
for x in chain(a, b):


#4.13 데이터 처리 파이프라인 생성

#데이터 처리를  데이터 처리 파이프라인과 같은 방식으로 순차적으로 처리하고 싶다.
#예를 들어, 처리해야 할 방대한 데이터가 있지만 메모리에 한꺼번에 들어가지 않는 경우에 적용할 수 있다.



import os
import fnmatch
import gzip
import bz2
import re


def gen_find(filepat, top):
    '''
    디렉터리 트리에서 와일드카드 패턴에 매칭하는 모든 파일 이름을 찾는다.
    '''
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


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
    라인 시퀀스에서 정규식 패턴을 살펴본다
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line

#처리 파이프라인 만들기
#ex) python 이란 단어를 포함하고 있는 모든 로그 라인을 찾으려면 다음과 같다

lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)

#파이프라인을 확장하고 싶다면 , 제너레이터 표현식으로 데이터를 넣을 수 있다.
#예를 들어 다음 버전은 전송한 바이트 수를 찾고 그 총합을 구한다

lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
bytecolumn = (line.rsplit(None,1)[1] for line in pylines)
bytes = (int(x) for x in bytecolumn if x != '-')
print('Total', sum(bytes))



#4.14 중첩 시퀀스 풀기
#Q 중첩된 시퀀스를 합쳐 하나의 리스트로 만들고 싶다.

from collections import Iterable

# ignore_types : 문자열이나 바이트는 하나하나 펼치지 않게 제외해주었다.
def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        # 시퀀스일 경우 시퀀스 내부의 항목을 반환
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        # 시퀀스가 아니면 그 자신을 반환
        else:
            yield x

items = [1, 2, [3, 4, [5, 6], 7], 8]
# 1 2 3 4 5 6 7 8 생성
for x in flatten(items):
    print(x)

#앞의 코드에서 isinstance(x, Iterable)은 아이템이 순환 가능한 것인지 확인한다.
#순환이 가능하다면 yield from 으로 모든 값을 하나의 서브루틴으로 분출한다.
#ignore_types 와 not isinstance(x, ignore_types)로 문자열과 바이트가 순환 가능한 것으로 해석되지 않도록 했다.
# 이렇게 해야만 리스트에 담겨있는 문자열을 전달했을 때 문자를 하나하나 펼치지 않고 문자열 단위로 전개한다.

items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
for x in flatten(items):
    print(x)


#서브루틴으로 다른 제너레이터를 호출할 때 yield from을 사용하면 편리하다.
#이 구문을 사용하지 ㅏㄶ으면 추가적인 for 문이 있는 코드를 작성해야 한다.

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            for i in flatten(x):
                yield i
        else:
            yield x

#4.15 정렬된 여러 시퀀스를 병합 후 순환

#정렬된 시퀀스가 여럿 있고, 이들을 하나로 합친 후 정렬된 시퀀스를 순환하고 싶을땐?
#A

import heapq
a = [1, 4, 7, 10]
b = [2, 5, 6, 11]
for c in heapq.merge(a, b):
    print(c)


#heapq.merge는 아이템에 순환적으로 접근하며 제공한 시퀀스를 한꺼번에 읽지 않는다.
#따라서 아주 긴 시퀀스도 별 다른 무리 없이 사용할 수 있다.

with open('sorted_file_1', 'rt') as file1, \
    open('sorted_file_2', 'rt') as file2, \
    open('merged_file', 'wt') as outf:

    for line in heapq.merge(file1, file2):
        outf.write(line)


#4.16 무한 while 순환문을 이터레이터로 치환

#Q. 함수나 일반적이지 않은 조건 테스트로 인해 무한 while 순환문으로 데이터에 접근하는 코드
#


CHUNKSIZE = 8192

def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data == b'':
            break
        process_data(data)


#앞의 코드는 iter()를 사용해 다음과 같이 수정할 수 있다.

def reader2(s):
    for chunk in iter(lambda: s.recv(CHUNKSIZE), b''):
        pass


import sys
f = open('/etc/passwd')
for chunk in iter(lambda: f.read(10), ''):
    n = sys.stdout.write(chunk)

nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
root:*:0:0:System Administrator:/var/root:/bin/sh
daemon:*:1:1:System Services:/var/root:/usr/bin/false
_uucp:*:4:4:Unix to Unix Copy Protocol:/var/spool/uucp:/usr/sbin/uucico


#내장함수 iter()의 기능은 거의 알려져 있지 않다.
# 이함수에는 선택적으로 인자 없는 호출 가능 객체와 종료값을 입력으로 받는다. 이렇게 사용하면 주어진 종료 값을 반환하기 전까지
#무한히 반복해서 호출 가능 객체를 호출한다.
#이런 방식을 사용하면 입출력과 관련 있는 반복 호출에 잘 동작한다.
# 예를 들어 소켓이나 파일에서 특정 크기의 데이터를 읽으려 한다면
#반복적으로 read()난 recv()를 호출하고 파일 끝(end-of-file)을 확인해야 한다.
# 이번 레시피를 따른다면 두 가지 동작을 하나의 iter()호출로 합칠 수 있다. lambda를 사용하면 인자를 받지않는 호출 객체를 만들 수 있고
#원하는 크기의 인자를 recv()나 read()에 전달한다.