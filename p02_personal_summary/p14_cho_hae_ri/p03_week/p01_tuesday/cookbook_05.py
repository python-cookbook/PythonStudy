


################################################################################
#  4.7. 이터레이터의 일부 얻기
################################################################################
#
# 문제 - 이터레이터가 만드는 데이터의 일부를 얻고 싶지만, 일반적인 자르기 연산자가 동작하지 않는다
#
# 해결 - 이터레이터와 제너레이터의 일부를 얻는 데는 itertools.islice() 함수가 가장 이상적임


def count(n):
    while True:
        yield n
        n += 1

c = count(0)
c[10:20]
# TypeError: 'generator' object is not subscriptable

# 이제 islice()를 사용한다.
c = count(0)
import itertools
for x in itertools.islice(c, 10, 20):
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




# 토론 - 이터레이터와 제너레이터는 일밙거으로 일부를 잘라낼 수 없다. 데이터의 길이를 알 수 없기 때문이다(또한 인덱스를 구현하고 있지도 않다.)
# islice()의 실행 결과는 원하는 아이템의 조각을 생성하는 이터레이터지만, 이는 시작 인덱스까지 모든 아이템을 소비하고 버리는 식으로 수행한다
# 그리고 그 뒤의 아이템은 마지막 인덱스를 만날 때까지 islice() 객체가 생성한다
# 주어진 이터레이터 상에서 islice()가 데이터를 소비한다는 점이 중요하다. 이터레이터를 뒤로 감을 수는 없기 때문에 이 부분을 잘 고려해야 한다.




#########################################################################
# 4.8. 순환 객체 첫 번쨰 부분 건너뛰기
########################################################################


# 문제 - 순환 객체의 아이템을 순환하고 싶은데, 처음 몇 가지 아이템에는 관심이 없어 건너뛰고 싶다.

# 해결
# itertools 모듈에 이 용도로 사용할 수 있는 몇 가지 함수가 있다. 첫번째는 itertools.dropwhile() 함수이다.
# 이 함수를 사용하려면 함수와 순환 객체를 넣으면 된다. 반환된 이터레이터는 넘겨준 함수가 true를 반환하는 동안은 시퀀스의 첫 번째 아이템을 무시한다.

# 주석으로 시작하는 파일을 읽는다고 가정해보자.

with open('c:/data/...') as f:
    for line in f:
        print(line, end ='')


## 처음 나오는 주석을 모두 무시하려면 다음과 같이 한다.

from itertools import dropwhile
with open('c:/data/...') as f:
    for line in dropwhile(lambda line : line.startswith('#'), f):
        print(line, end ='')


# 이 예제는 테스트 함수에 따라 첫 번째 아이템을 생략하는 방법을 다루고 있다. 만약 어디까지 생략해야 할 지 정확한 숫자를 알고 있다면
# itertools.islice() 함수를 사용하면 된다.


from itertools import islice
items = ['a', 'b', 'c', 'd', 'e', 1, 4, 34, 23]
for x in islice(items, 3, None):
    print(x)

# d
# e
# 1
# 4
# 34
# 23

# 이 예제에서 islice()에 전달한 마지막 none 인자는  처음 세 아이템 뒤에 오는 모든 것을 원함을 명시한다. [:3] 이 아니라 [3:]


##### 토론 ######

# dropwhile() 과 islice() 함수는 다음과 같이 복잡한 코드를 작성하지 않도록 도와준다.

with open('c:/data/...') as f:
    # 처음 주석을 건너뛴다.
    while True:
        line = next(f, '')
        if not line.startswith('#'):
            break

    # 남아있는 라인을 처리한다.
    while line:
        #의미있는 라인으로 치환한다.
        print(line, end='')
        line = next(f, None)

# 순환 객체의 첫 부분을 건너뛰는 것은 간단히 전체를 걸러내는 것과는 조금 다르다.
# 예를 들어 이번 레시피의 첫 부분을 다음과 같이 수정할 수 있다.


with open('c:/data/...') as f:
    lines = (line for line in f if not line.startswith('#'))
    for line in lines:
        print(line, end='')

# 이렇게 하면 파일 전체에 겇쳐 주석으로 시작하는 모든 라인을 무시한다.
# 하지만 레시피에서 제시한 방법대로 하면 제공한 함수가 만족하는 동안의 아이템을 무시하고, 그 뒤에 나오는 아이템은 필터링 없이 모두 반환한다.
# 마지막으로, 이 레시피의 방식은 순환가능한 모든 것에 적용 가능하다는 점!!!
# 크기를 알 수 없는 제너레이터, 파일 등 모든 것이 포함된다!


#######################################################################
# 4.9. 가능한 모든 순열과 조합 순환
#######################################################################


# 문제 - 아이템 컬렉션에 대해 가능한 모든 순열과 조합을 순환하고 싶다면

# 해결
# itertools 모듈은 이와 관련있는 세 함수를 제공한다. 첫째는 itertools.permutations() 로 ,
# 아이템 컬렉션을 받아 가능한 모든 순열을 튜플 시퀀스로 생성한다.


items = ['a', 'b', 'c']
from itertools import permutations
for p in permutations(items):
    print(p)
# ('a', 'b', 'c')
# ('a', 'c', 'b')
# ('b', 'a', 'c')
# ('b', 'c', 'a')
# ('c', 'a', 'b')
# ('c', 'b', 'a')

# 만약 더 짧은 길이의 순열을 원한다면 선택적으로 길이 인자를 지정할 수 있다.

for p in permutations(items, 2):
    print(p)

# ('a', 'b')
# ('a', 'c')
# ('b', 'a')
# ('b', 'c')
# ('c', 'a')
# ('c', 'b')


# itertools.combinations() 는 입력받은 아이템의 가능한 조합을 생성한다.

from itertools import combinations
for c in combinations(items, 3):
    print(c)
    # ('a', 'b', 'c')

for c in combinations(items, 2):
    print(c)
    # ('a', 'b')
    # ('a', 'c')
    # ('b', 'c')

for c in combinations(items, 1):
    print(c)
    # ('a',)
    # ('b',)
    # ('c',)


# combinations() 의 경우 실제 요소의 순서는 고려하지 않는다. 따라서 ('a', 'b')는 ('b', 'a')와 동일하게 취급되어 ('b', 'a')는 생성되지 않는다.
# 조합을 생성할 때 선택한 아이템은 가능한 후보의 컬렉션에서 제거된다(예를 들어 a 는 이미 선택되었기 때문에 고려에서 제외된다.)

# itertolles.combinations_with_replacement() 함수는 이러한 점을 보완해 같은 아이템을 여러번 선택할 수 있게 한다.

for c in itertools.combinations_with_replacement(items, 3):
    print(c)
# ('a', 'a', 'a')
# ('a', 'a', 'b')
# ('a', 'a', 'c')
# ('a', 'b', 'b')
# ('a', 'b', 'c')
# ('a', 'c', 'c')
# ('b', 'b', 'b')
# ('b', 'b', 'c') ...........


####### 토론 ########

# 이번 레시피에서 itertools 모듈의 편리한 도구 중 몇 가지만을 다루었다.
# 사실 조합이나 순열을 순환하는 코드를 직접 작성할 수도 있겠지만 그렇게 하려면 꽤 많은 고민을 해야 한다...



############################################################################
# 4. 10. 인덱스 - 값 페어 시퀀스 순환
############################################################################


# 문제 - 시퀀스를 순환하려고 한다. 이 때 어떤 요소를 처리하고 있는 지 번호를 알고 싶다.

# 해결
# 이 문제는 내장 함수 enumerate()을 사용해 해결할 수 있다.

my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list,):
    print(idx, val)
# 0 a
# 1 b
# 2 c

# 출력시 번호를 1부터 시작하고 싶다면 start 인자를 전달한다.
my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list, 1):
    print(idx, val)
# 1 a
# 2 b
# 3 c

# 이번 예제는 에러 메시지에 파일의 라인 번호를 저장하고 싶은 경우에 유용하다,


def parse_data(filename):
    with open(filename, 'rt') as f:
        for lineno, line in enumerate(f, 1):
            fields = line.split()
            try:
                count = int(fields[1])
                ...
            except ValueError as e:
                print('Line {}: Parse error: {}'.format(lineno, e))

# enumerate() 은 특정 값의 출현을 위한 offset 추적에 활용하기 좋다
# 파일 내의 단어를 출현한 라인에 매핑하려면, enumerate() 으로 단어를 파일에서 발견한 라인 오프셋에 매핑한다.

# 파일 처리 후 word_summary 를 출력하면 이는 각 단어를 키로 갖는 딕셔너리 형태가 된다.
# 키에 대한 값은 그 단어가 나타난 라인의 리스트가 된다. 한 라인에 단어가 두 번 나오면 그 라인은 두 번 리스팅되어 텍스트에 대한 단순 지표를 알아볼 수 있도록 한다.



##### 토론 #####

# 카운터 변수를 스스로 다루는 것에 비해 enumerate() 을 사용하는 것이 훨씬 보기 좋다.
# 예를 들어 다음과 같은 코드로 카운터 변수를 만들 수 있다.


lineno =1
for line in f:
    # 라인처리
    ...
    lineno += 1

# 하지만 enumerate() 을 사용하는 것이 훨씬 세련된 방식이다.

for lineno, line in enumerate(f):
    # 라인처리
    ...


# enumerate() 가 반환하는 값은 연속된 튜플을 반환하는 이터레이터인 enumerate객체의 인스턴스이다.
# 이 튜플은 전달한 시퀀스에 next() 를 호출해 반환된 카운터와 값으로 이루어져 있다.
# 사소한 문제이긴 하지만 주의해야 할 점!!!!!
# 한 번 더 풀어줘야 하는 튜플의 시퀀스에 enumerate() 를 사용할 때는 실수를 범하기 쉽다.

data = [(1,2), (3,4), (5,6), (7,8)]

# 올바른 방법!
for n, (x, y) in enumerate(data):
    ...

# 에러!
for n, x, y in enumerate(date):
    ...




#####################################################################
# 4. 11.  여러 시퀀스 동시에 순환
####################################################################

# 문제 - 여러 시퀀스에 들어 있는 아이템을 동시에 순환하고 싶다.

# 해결 - 여러 시퀀스를 동시에 순환하려면 zip() 함수를 사용한다.

xpts = [1,5,4,2,10,7]
ypts = [101, 78, 37, 15, 62, 99]
for x, y in zip(xpts, ypts):
    print(x,y)

# 1 101
# 5 78
# 4 37
# 2 15
# 10 62
# 7 99

#zip(a, b) 는 tuple(x,y) 를 생성하는 이터레이터를 생성한다. (x는 a 에서, y는 b 에서 가져옴)
# 순환은 한 쪽 시퀀스의 모든 입력이 소비되었을 때 정지한다. 따라서 순환의 길이는 입력된 시퀀스 중 짧은 것과 같다.

a = [1,2,3]
b = ['w', 'x', 'y', 'z']
for i in zip(a,b):
    print(i)

    # (1, 'w')
    # (2, 'x')
    # (3, 'y')


# 이렇게 동작하는 방식이 마음에 들지 않는다면 itertools.zip_longest() 를 사용해야 한다.

from itertools import zip_longest
for i in zip_longest(a,b):
    print(i)

    # (1, 'w')
    # (2, 'x')
    # (3, 'y')
    # (None, 'z')



###### 토론 #######

# zip() 은 데이터를 묶어야 할 때 주로 사용한다. 예를 들어 열 헤더와 값을 리스트로 가지고 있다고 가정해보자.

headers = ['name', 'shares', 'price']
values = ['ACME', 100, 490.1]

# zip() 을 사용하면 두 값을 묶어 딕셔너리로 만들 수 있다.
s = dict(zip(headers, values))

# 혹은 출력을 하려고 한다면 다음과 같은 코드를 작성한다.
for name, val in zip(headers, values):
    print(name, '=', val)


# 일반적이지는 않지만 zip() 에 시퀀스를 두 개 이상 입력할 수 있다.
# 이런 경우 결과적으로 튜플에는 입력한 시퀀스의 개수 만큼의 아이템이 포함된다.

a = [1,2,3]
b = [11,12,13]
c = ['x', 'y', 'z']
for i in zip(a,b,c):
    print(i)

    # (1, 11, 'x')
    # (2, 12, 'y')
    # (3, 13, 'z')


# 마지막으로 zip() 이 결과적으로 이터레이터를 생성한다는 점을 기억하도록 하자. 묶은 값이 저장된 리스트가 필요하다면 list() 함수를 사용한다.

zip(a, b)
# <zip at 0x4cb0d48>
list(zip(a,b))
# [(1, 11), (2, 12), (3, 13)]



################################################################
#  4.12. 서로 다른 컨테이너 아이템 순환
#################################################################

# 문제 - 여러 객체에 동일한 작업을 수행해야 하지만, 객체가 서로 다른 컨테이너에 들어 있다.
# 하지만 중첩된 반복문을 사용해 코드의 가독성을 해치고 싶지 않다.

# 해결
#itertools.chain() 메소드로 이 문제를 간단하게 해결할 수 있다. 이 메소드는 순환 가능한 객체를 리스트로 받고 마스킹을 통해 한번에 순환할 수 있는 이터레이터를 반환한다
#예를 들어 다음 코드를 살펴보자.


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


# chain() 은 일반적으로 모든 아이템에 동일한 작업을 수행하고 싶지만 이 아이템이 서로 다른 세트에 포함되어 있을 때 사용한다.


# 여러 아이템 세트
active_items = set()
inactive_items = set()

# 모든 아이템 한 번에 순환
for item in chain(active_items, inactive_items):
    # 작업
    ...

# 앞에 나온 방식은 반복문을 두 번 사용하는 것보다 훨씬 보기 좋다.

for item in inactive_items:
    # 작업
    ...


# itertools.chain() 은 하나 혹은 그 이상의 순환 객체를 인자로 받는다. 그리고 입력받은 순환 객체 속 아이템을 차례대로
# 순환하는 이터레이터를 생성한다. 큰 차이는 아니지만, 우선적으로 시퀀스를 하나로 합친 다음 순환하는 것보다 chain() 을 사용하는 게 더 효율적

#비효율적
for x in a + b:
    ...

#효율적
for x in chain(a, b):
    ...


# 첫번째 방식에서 a+b 는 두 개를 합친 전혀 새로운 시퀀스를 만들고, a 와 b가 동일한 타입이여야 한다는 요구조건이 있으나
# chain() 은 이런 과정이 없다. 따라서 입력한 시퀀스 크기가 아주 크다면 chain()을 사용하는것이 메모리 측면에서 유리하고 타입이 다른 경우에도 쉽게 사용 가능함


#############################################################################
#  4. 13. 데이터 처리 파이프라인 생성
#############################################################################


# 문제
# 데이터 처리를 데이터 처리 파이프라인과 같은 방식으로 순차적으로 처리하고 싶다(unix 파이프라인과 비슷하게)
# 예를 들어, 처리해야 할 방대한 데이터가 있지만 메모리에 한꺼번에 들어가지 않는 경우에 적용할 수 있다.


# 해결
# 제너레이터 함수를 사용하는 것이 처리 파이프라인을 구현하기에 좋다. 예를 들어 방대한 양의 로그 파일이 들어있는 디렉터리에 작업을 해야 한다고 가정해 보자.


# foo/
#     access-log-012007.gz
#     access-log-022007.gz
#     access-log-032007.gz
#     ...
#     access-log-012008
# bar/
#     access-log-092007.bz2
#     ...
#     access-log-022008

# 그리고 각 파일에는 다음과 같은 데이터가 담겨 있다.

# 124.115.6.12 - - [10/Jul/2012:00:18:50 -0500] "GET /robots.txt ..." 200 71
# 210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /ply/ ..." 200 11875
# 210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /favicon.ico ..." 404 369
# 61.135.216.105 - - [10/Jul/2012:00:20:04 -0500] "GET /blog/atom.xml ..." 304 -
# ...


# 이 파일을 처리하기 위해 특정 작업처리를 수행하는 작은 제너레이터 함수의 컬렉션을 정의할 수 있다.

import os
import fnmatch
import gzip
import bz2
import re

    def gen_find(filepat, top):
    '''
    디렉터리 트리에서 와일드 카드 패턴에 매칭하는 모든 파일 이름을 찾는다.
    '''
        for path, dirlist, filelsit in os.walk(top):
            for name in fnmatch.filter(filelsit, filepat):
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
        이터레이터 시퀀스를 합쳐 하나의 시퀀스로!
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


### 위 코드의 정체는 뭐지...?

# 이제 이 함수들을 모아서 어렵지 않게 처리 파이프라인을 만들 수 있다.

# python 이라는 단어를 포함하는 로그를 찾으려면!

lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)

# 파이프 라인을 확장하고 싶다면, 제너레이터 표현식으로 데이터를 넣을 수 있다.
# 예를 들어 다음 버전은 전송한 바이트 수를 찾고 그 총합을 구한다.

lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
bytecolumn = (line.rsplit(None,1)[1] for line in pylines)
bytes = (int(x) for x in bytecolumn if x != '-')
print('Total', sum(bytes))




###############################################################################
#  4. 14. 중첩 시퀀스 풀기
###############################################################################


# 문제
# 중첩된 시퀀스를 합쳐 하나의 리스트로 만들고 싶다면?/

# 해결
# 이 문제는 yield from 문이 있는 재귀 제너레이터를 만들어 쉽게 해결할 수 있다.

from collections import Iterable

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x

items = [1,2,[3,4, [5, 6], 7], 8]

# 1 2 3 4 5 6 7 8 생성
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


# 앞의 코드에서 isinstance(x, Iterable) 은 아이템이 순환 가능한 것인지 확인한다.
# 순환이 가능하다면 yield from 으로 모든 값을 하나의 서브루틴으로 분출한다.
# 결과적으로 중첩되지 않은 시퀀스 하나가 만들어진다.


# 추가적으로 전달 가능한 인자 ignore_types 와 not isinstance(x, ignore_types) 로 문자열과 바이트가 순환 가능한 것으로 해석되지 않도록 했다.
# 이렇게 해야만 리스트에 담겨 있는 문자열을 전달했을 때 문자를 하나하나 펼치지 않고 문자열 단위로 전개한다.

items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
for x in flatten(items):
    print(x)

    # Dave
    # Paula
    # Thomas
    # Lewis



# 토론
# 서브루틴으로써 다른 제너레이터를 호출할 떄 yield from 을 사용하면 편리하다. 이 구문을 사용하지 않으면 추가적인 for 문이 있는 코드를 작성해야 한다.

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            for i in flatten(x):
                yield i
        else:
            yield x

# 큰 차이는 아니지만 yield from 문이 더 깔끔하고 나은 코드를 만들어 준다.



#################################################################
#  4.15. 정렬된 여러 시퀀스를 병합 후 순환
#################################################################


# 문제
# 정렬된 시퀀스가 있고, 이들을 하나로 합친 후 정렬된 시퀀스를 순환하고 싶다.

# 해결
# 간단하다. heapq.merge() 함수를 사용하면 된다.

import heapq
a = [1,4,7,10]
b = [2,5,6,11]
for c in heapq.merge(a,b):
    print(c)

# 1
# 2
# 4
# 5
# 6
# 7
# 10
# 11


# heapq.merge 는 아이템에 순환적으로 접근하며 제공한 시퀀스를 한꺼번에 읽지 않는다.
# 따라서 아주 긴 시퀀스도 별다른 무리 없이 사용할 수 있다.
# 예를 들어 정렬된 두 파이릉ㄹ 병합하려면 다음고 ㅏ같이 한다.

with open('sorted_file_1', 'rt') as file1, \
    open('sorted_file_2', 'rt') as file2, \
    open('merged_file', 'wt') as outf:

    for line in heapq.merge(file1, file2):
        outf.write(line)



######################################################################
#  4. 16. 무한 while 순환문을 이터레이터로 치환
######################################################################

# 문제
# 함수나 일반적이지 않은 조건 테스트로 인해 무한 while 순환문으로 데이터에 접근하는 코드를 만들었다.

# 해결
# 입출력과 관련있는 프로그램에 일반적으로 다음과 같은 코드를 사용한다.

CHUNKSIZE = 8192

def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data == b'':
            break
        #process_data(data)

# 앞의 코드는 iter() 를 사용해 다음과 같이 수정할 수 있다.

def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data == b'':
            break

        #process_data(data)

# 앞의 코드는 iter() 를 사용해 다음과 같이 수정할 수 있다.

def reader2(s):
    for chunk in iter(lambda: s.recv(CHUNKSIZE), b''):
        pass
        # process_data(data)


# 정말 이 코드가 동작하는지 믿음이 안 간다면 파일과 관련 있는 예제를 실행해보자.

import sys
f = open('/etc/passwd')
for chunk in iter(lambda: f.read(10), ''):
    n = sys.stdout.write(chunk)

'''
nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
root:*:0:0:System Administrator:/var/root:/bin/sh
daemon:*:1:1:System Services:/var/root:/usr/bin/false
_uucp:*:4:4:Unix to Unix Copy Protocol:/var/spool/uucp:/usr/sbin/uucico
'''

# 토론

# 내장 함수 iter() 의 기능은 거의 알려져 있지 않다.
# 이 함수에는 선택적으로 인자 없는 호출 가능 객체와 종료 값을 입력으로 받는다....
# 이런 방식을 사용하면 입출력과 관련 있는 반복 호출에 잘 동작한다.