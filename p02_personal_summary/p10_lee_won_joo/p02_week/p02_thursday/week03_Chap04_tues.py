
"""
                                                ▶ 4.7 이터레이터의 일부 얻기◀ 
♣  문제 :  이터레이터가 만드는 데이터의 일부를 얻고 싶지만, 일반적인 자르기 연산자가 동작하지 않는다면?ㅠㅠ

↘  해결 :  이터레이터와 제너레이터의 일부를 얻는데는 itertools.islict() 함수가 가장 이상적이다.


   토론 :  이터레이터와 제너레이터는 일반적으로 일부를 잘라낼 수 없다. 왜냐하면 데이터의길이를 알 수 없기 때문이다.
          islice()의 실행결과는 원하는 아이템의 조각을 생성하는 이터레이터지만, 이는 시작 인데스까지 모든 아이템을 소비한 후, 버리는 식으로
          수행하기 때문에 좀 비효율적인 느낌이 없지 않아있지..
          그 뒤 아이템은 마지막 인덱스를 만날 때까지 islice객체가 생성한다.

          주어진 이터레이터 상에서 lislice()가 데이터를 소비하는 점이 중요하다.. 뒤로 감을 수 있는게 아니니까, 잘 고려해야 한다. 
          뒤로 돌아가는 동작 자체가 중요하다고 하면, 데이터를 리스트로 변환한 다음에 하는게 좋다.

 """

print('###############################################################################')
print('########################################## 4.7 이터레이터의 일부 얻기#####################################')
print('###############################################################################')




def count(n):
    while True:
        yield n
        n +=1


c = count(0)
# print(c[10:20])  #TypeError: 'generator' object is not subscriptable


# ㅇ제 islice()를 사용한다.  아마 i slice 합성어인듯 is lice가 아니고 ..ㅋㅋ

import itertools

for x in itertools.islice(c, 10, 20):
    print(x)  # 10,11,12,13 .. 19

"""
                                                ▶ 4.8 순환 객체 첫번째 부분 건너뛰기◀ 
♣  문제 :  순환객체의 아이템을 순환하려고 하는데, 처음 몇가지 아이템에는 관심이 없어 건너뛰고 싶다면?

↘  해결 :  itertools모듈에 이 용도로 사용할 수 있는 몇가지 함수가 있다. 

         1. 첫번째는 itertools,dropwhile()함수이다.
            이 함수는 함수와 순환객체를 넣으면 된다. 반환된 이터레이터는 넘겨준 함수가 True를 반환하는 동안 
            시퀀스의 첫 번째 아이템을 무시한다.
            그 이후엔 전체 시퀀스를 생성한다.

   토론 :  
 """

print('###############################################################################')
print('########################################## 4.8 순환 객체 첫번째 부분 건너뛰기#####################################')
print('###############################################################################')

with open('d:/data/emp2.csv') as f:
    for line in f:
        print(line, end='')  # 첫줄 7839,KING,PRESIDENT,0,1981-11-17,5000,0,10
        # 마지막 줄 7934,MILLER,CLERK,7782,1982-01-11,1300,0,10

# 처음 나오는 줄을 무시하려면 다음과 같이 한다.
from itertools import dropwhile

with open('d:/data/emp2.csv') as f:
    # 첫 줄을 건너 뛴다.
    for line in dropwhile(lambda line: line.startswith('7'), f):
        print(line, end='')

# 이 예제는 테스트 함수에 따라 첫번쨰 아이템을 생략하는 방법을 다루고 있다.
# 만약 어디까지 생략해야 할지 정확한 숫자를 알고 있다면
#  itertools.islice() 를 사용하면 된다.

# 이 예제에서 islice() 에 전달한 마지막 None 인자는
# 처음 세 아이템 뒤에 오는 모든 것들을 원함을 명시한다.
# ([:3]이 아니라 [3:]을 원함을 의미한다.)


# dropwhile과 islice() 함수는 다음과 같이 복잡한 코드를 작성하지 않도록 도와준다.

# with open('etc/passwd') as f:
#     # 처음 주석 건너 뛰기
#     while True:
#         line = next(f, '')
#         if not line.startswith('#'):
#             break
#     #남아 있는 라인 처리
#     while line:
#         #의미 있는 라인 치환
#         print(line, end='')
#         line = next(f, None)

# 순환 객체의 첫 부분을 건너뛰는 것은 간단히 전체를 걸러 내는 것과는 조금다르다.
# 예를 들어 이번 레시피의 첫 부분을 다음과 같이 수정할 수있다.
#
# with open('tec/passwd') as f:
#     lines = (line for line in f if not line.startswith('#'))
#     for line in lines:
#         print(line, end='')

# 이렇게 하면 파일 전체에 걸쳐, 주석으로 시작하는 모든 라인 무시한다.
# 아무튼간에 강조하고자 하는 내용은, 순환 가능한 모든 것에 적용 가능하다는 점이다.






"""
                                                ▶ 4.9 가능한 모든 순열과 조합 순환◀ 
♣  문제 :  아이템 컬렉션에 대해 가능한 모든 순열과 조합을 순환하고 싶다.

↘  해결 :  itertools 모듈은 이와 관련 있는 세 함수를 제공한다.
          첫째는 itertools.permutations() 이다.
            아이템 컬렉션을 받아, 가능한 모든 순열을 튜플 시퀀스로 생성한다.

   토론 :  
 """

print('###############################################################################')
print('########################################## 4.9 가능한 모든 순열과 조합 순환#####################################')
print('###############################################################################')

items = ['a', 'b', 'c']
from itertools import permutations

for p in permutations(items):
    print(p)
    #
    # ('a', 'b', 'c')
    # ('a', 'c', 'b')
    # ('b', 'a', 'c')
    # ('b', 'c', 'a')
    # ('c', 'a', 'b')
    # ('c', 'b', 'a')

# 더 짧은 길이의 순열을 원한다면, 선택적으로 길이인자 지정 가능하다.

for p in permutations(items, 2):
    print(p)
    # ('a', 'b')
    # ('a', 'c')
    # ('b', 'a')
    # ('b', 'c')
    # ('c', 'a')
    # ('c', 'b')

# itertools.combinations()는 입력 받은 아이템의 가능한 '조합'을 생성한다.

print('itertools.combinations()는 입력 받은 아이템의 가능한 ''조합''을 생성한다.')
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

# 콤비네이션의 경우 실제 요소의 순서는 고려하지 않는다.
# 따라서 a,b,는 b,a와 동일하게 취급 된다.

# 조합을 생성할 때, 선택한 아이템은 가능한 후보의 컬렉션에서 제거된다. (ex) 'a'는 이미 선택되었으므로 제외
# itertools.combinations_with_replacement()함수는 이를 보완해 같은 아이템을 두번 이상 선택할 수 있게 된다.

import itertools

for c in itertools.combinations_with_replacement(items, 3):
    print(c)
    # ('a', 'a', 'a')
    # ('a', 'a', 'b')
    # ('a', 'a', 'c')
    # ('a', 'b', 'b')
    # ('a', 'b', 'c')
    # ('a', 'c', 'c')
    # ('b', 'b', 'b')
    # ('b', 'b', 'c')
    # ('b', 'c', 'c')
    # ('c', 'c', 'c')

"""
                                                ▶ 4.10 인덱스- 값 페어 시퀀스 순환◀ 
♣  문제 :  시퀀스를 순환하려고 한다. 이때 어떤 요소를 처리하고 있는지 번호를알고 싶다.

↘  해결 :  이 문제는 내장 함수 enumerate()를 사용하면 간단히 해결할 수 있다.



   토론 :  
 """

print('###############################################################################')
print('##########################################4.10 인덱스- 값 페어 시퀀스 순환#####################################')
print('###############################################################################')

my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list):
    print(idx, val)
    # 0    a
    # 1    b
    # 2    c

# 출력시 번호를 1번부터 하고 싶으면 start인자를 전달한다.

for idx, val in enumerate(my_list, 1):
    print(idx, val)
    # 1    a
    # 2    b
    # 3    c


# 이번 예제는 에러 메세지에 파일의 라인 번호를 저장하고 싶은 경우에 유용하다.

def parse_date(filename):
    with open(filename, 'rt') as f:
        for line_num, line in enumerate(f, 1):
            fields = line.split()
            try:
                count = int(fields[1])
            except ValueError as e:
                print('Line {}: Parse error : {}'.format(line_num, e))


# enumerate()는 예를 들어 특정 값의 출력을 위한 오프셋 추적에 활용하기 좋다.
# 따라서 파일 내의단어를 출현한 라인에 매핑하려면,
# enumerate() 로 단어를 파일에서 발견한 라인 오프셋에매핑한다.

from collections import defaultdict

word_sum = defaultdict(list)
with open('d:/data/emp2.csv') as f:
    lines = f.readlines()
    print(lines[0])  # 7839,KING,PRESIDENT,0,1981-11-17,5000,0,10
for idx, line in enumerate(lines):
    # 현재 라인에 단어 리스트를 생성
    words = [w.strip().lower() for w in line.split(',')]
    for word in words:
        word_sum[word].append(idx)
print(word_sum)

# 파일 처리 후 word_summary를 출력하면 각 라인이 키로 잡히고, 인덱싱이 밸류로 잡힌다.
# 라인에 들어있는 단어의 개수를 센다...워



# 카운터 변수를 스스로 다루는 것에 비해 enumerate() 를 사용하는 것이 훨씬 보기 좋다.
# 예를 들어 다음고 ㅏ같은 코드로 카운터 변수를 만들 수 있다.

# linesno = 1
# for line in f:
#     #라인 처리
#     #..
#     lineno += 1
# 위 같은 촌스러운 방식을 아래와 같이 할 수 있음.

# for lineno, line in enumerate(f):
#     #라인 처리
#     ..


# enumerate()가 반환하는 값은 연속된 튜플을 반환하는 이터레이터인 enumerate객체의 인스턴스이다.
# 이 튜플은 전달한 시퀀스에 next()를 호출해 반환된 카운터와 값으로 이루어져있다.
# 사소한 문제이긴 하지만,주의해야할 점은 한번 더 풀어줘야하는 튜플의 시퀀스에 enumerate()를 사용할때는 실수를 범하기 쉽다.

data = [(1, 2), (3, 4), (5, 6), (7, 8)]

# 올바른 방법
for n, (x, y) in enumerate(data):
    print(n)
    print(x, y)
    print((x, y))

# 실수하는 종류
# for n,x,y in enumerate(data):
#     ..








"""
                                                ▶ 4.11 여러 시퀀스 동시에 순환◀ 
♣  문제 :  여러 시퀀스에 들어 있는 아이템을 동시에 순환하고 싶다.

↘  해결 :  여러 시퀀스를 동시에 순환하려면 zip() 함수를 사용 한다.
         zip(a,b)는 튜플(x,y)를 생성하는 이터레이터를 생성할 수도 있다.
         이터레이터는 한쪽 원소가 모두 소비되면 정지된다.
         for i in zip(a,b):
            print(i)
            (x,y)
            (x,y)
            ...
         itertools.zip_longest()는 한쪽이 모두 소비되면, None : Y 이런식으로 튜플을 반환한다.

   토론 :  
 """

print('###############################################################################')
print('##########################################4.11 여러 시퀀스 동시에 순환 #####################################')
print('###############################################################################')

xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99]

for x, y in zip(xpts, ypts):
    print(x, y)
    # 1    101
    # 5    78
    # 4    37
    # 2    15
    # 10    62
    # 7    99

# zip(a,b)는 tuple(x,y)를 생성하는 이터레이터를 생성한다.       (x는 a에서, y는 b에서 가져옴)
# 순환은 한쪽 시퀀스의 모든 입력이 소비되었을 때 정지한다.
# 따라서 순환의 길이는 입력된 시퀀스 중 짧은 것과 같다.

a = [1, 2, 3]
b = ['w', 'x', 'y', 'z']

for i in zip(a, b):
    print(i)  # 튜플
    # (1, 'w')
    # (2, 'x')
    # (3, 'y')

# 이렇게 동작하는 방식이 싫다면, itertools.zip_longest()를 사용해야 한다.

from itertools import zip_longest

for i in zip_longest(a, b):
    print(i)
    # (1, 'w')
    # (2, 'x')
    # (3, 'y')
    # (None, 'z')

for i in zip_longest(a, b, fillvalue=0):  # null, None값을 0으로 치환
    print(i)
    # (1, 'w')
    # (2, 'x')
    # (3, 'y')
    # (0, 'z')

# zip() 은 데이터를 묶어야할 때 주로 사용한다. 예를 들어 열 헤더와 값을 리스트로 가지고 있다고 가정해보자.

headers = ['name', 'shares', 'price']
values = ['ACME', 100, 490.1]

# zip을 사용하면 두 값을 묶어 딕셔너리로 만들 수 있다.

s = dict(zip(headers, values))
print(s)

# 혹은 출력 하려고 한다면 다음과 같이 해도된다.

for name, val in zip(headers, values):
    print(name, '=', val)
    # name = ACME
    # shares = 100
    # price = 490.1

# 일반적이지는 않지만 zip() 에 시퀀스를 두 개 이상 입력할 수 있다.
# 이런 경우 결과적으로 튜플에는 입력한 시퀀스의 개수 만큼의 아이템이 포함된다.

a = [1, 2, 3, 4]
b = [10, 11, 12]
c = ['x', 'y', 'z']

for i in zip_longest(a, b, c, fillvalue=0):  # zip도 2개 이상 시퀀스 가능.
    print(i)
    # (1, 10, 'x')
    # (2, 11, 'y')
    # (3, 12, 'z')
    # (4, 0, 0)

zip(a, b)
print(list(zip(a, b)))
# [(1, 10), (2, 11), (3, 12)]




"""
                                                ▶ 4.12 서로 다른 컨테이너 아이템 순환◀ 
♣  문제 :  여러 객체에 동일한 작업을 수행해야 하지만, 객체가 서로 다른 컨테이너에 들어 있다. 
          하지만 중첩된 반복문을 사용해 코드의 가독성을 해치고 싶지 않다.

↘  해결 :  itertools.cahin() 메소드로 해결 할 수 있다.
          이 메소드는 순환 가능한 객체를 리스트로 받고, 마스킹을 통해 한번에 순환할 수 있는 이터레이터를 반환한다.
          예를 들어, 다음 코드를 살펴보자.
   토론 :  
 """

print('###############################################################################')
print('##########################################4.12 서로 다른 컨테이너 아이템 순환 #####################################')
print('###############################################################################')

from itertools import chain

a = [1, 2, 3, 4]
b = ['x', 'y', 'z']

for x in chain(a, b):
    print(x)

c = [x for x in chain(a, b)]
print(c)

# chain() 은 일반적으로 모든아이템에 동일한 작업을 수행하고
# 이 아이템이 서로 다른 세트에 포함되어 있을 때 사용한다.

# 여러 아이템 세트
actvie_items = set()
inactvie_itmes = set()

# 모든 아이템 한번에 순환
# for item in chain(actvie_items,inactvie_itmes):
# 작업
# ...

# 위 방법이 아래 방법(for 문 두번 )보다 훨씬 낫다!

# for item in active_items:
# 작업..

# for item in inactive_items:
# 작업..



# itertools.chain()은 하나 혹은 그 이상의 순환 객체를 인자로 받는다.
# 그리고 입력받은 순환 객체 속 아이템을 차례대로 순환하는 이터레이터를 생성한다.
# 큰 차이는 아니지만, 우선적으로 시퀀스를 하나로 합친 다음 순환하는 것보다 chain()을 사용하는 것이 효율적임.


# 비효율적인 방법
# for x in a+b:
#     ...

# 더 나은 방식
# for x in chain(a,b):
#    ...


# 첫번째 방식에서 a+b는 두 개를 합쳐 전혀 새로운 시퀀스를 만들고, a와 b가 동일한 타입이어야한다는 요구조건이 있다.
# 하지만 chain 은 이런 과정을 걸치지 않는다.
# 다라서 입력한 시퀀스의 크기가아주 크다면, chain()을 사용하는 것이 메모리측면에서 유리하고, 타입이 다른 경우에도 쉽게 사용 가능하다.

dic = {}
dic['A'] = 1
dic['B'] = 2
print(dic)
temp = ['가', '나']

for x in chain(dic, temp):
    print(x)

# dict이랑 list 를 같이순환. 일단 키값이랑 리스트요소 출력되긴 한다.
# 좀더 연구해봐야함.




"""
                                                ▶ 4.13 데이터 처리 파이프라인 생성◀ 
♣  문제 :  데이터 처리를 데이터 처리 파이프라인과 같은 방식으로 순차적으로 처리하고 싶다(Unix 파이프라인과 비슷하게)
          예를 들어, 처리해야 할 방대한 데이터가 있지만 메모리에 한꺼번에 들어가지 않는 경우에 적용할 수 있다.

↘  해결 :  제너레이터 함수를 사용하는 것이 처리 파이프라인을 구현하기에 좋다. 예를 들어 방대한 양의로그파일이 들어있는 dir에 작업을 해야 한다고 가정해보자.
   토론 :  
 """

print('###############################################################################')
print('##########################################4.13 데이터 처리 파이프라인 생성 #####################################')
print('###############################################################################')

import os
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat, top):
    '''
    디렉터리 트리에서 와일드 카드 패턴에 매칭하는 모든 파일 이름을 찾는다.
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
        if filename.endswith('.gz'): #gz확장자 해당하는것
            f = gzip.open(filename, 'rt') #열어라
        elif filename.endswith('.bz2'): #bz2확장자 해당하는것
            f = bz2.open(filename, 'rt') #열어라
        else:
            f = open(filename, 'rt')  #열어라~
        yield f  #제너레이터 생성
        f.close()  #닫아라~

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

if __name__ == '__main__':

    # Example 2
    lognames = gen_find('access-log*', 'www')
    files = gen_opener(lognames)
    lines = gen_concatenate(files)
    pylines = gen_grep('(?i)python', lines)
    bytecolumn = (line.rsplit(None,1)[1] for line in pylines)
    bytes = (int(x) for x in bytecolumn if x != '-')
    print('Total', sum(bytes))



#파이프 라인으로 데이터를 처리하는 방식은, 파싱, 실시간 데이터 읽기, 주기적 폴링 등 다른 문제에도 사용할 수 있다.
#코드를 이해할 때, yield문이 데이터 생성자처럼 동작하고 for문은 데이터 소비자처럼 동작한다는 점이 중요하다.
#제너레이터가 쌓이면 각 yield가 순환을 하며 데이터의 아이템 하나를 파이프라인의 다음 단계로 넘긴다.. 마지막 예제에서 sum() 함수가 실질적으로
#프로그램을 운용하며 제너레이터 파이프라인에서 한번에 하나씩 아이템을 꺼낸다.

#파이프라인 방식을 따르면 메모리 효율성도 높다.
#방대한 디렉터리와 파일에도 잘 동작한다.


#더 많은 예제는 데이비드 비즐리의 시스템 프로그래머를 위한 제너레이터 트릭 튜토리얼 참고










"""
                                                ▶ 4.14 중첩 시퀀스 풀기◀ 
♣  문제 :  중첩된 시퀀스를 합쳐 하나의 리스트로 만들고 싶다.

↘  해결 :  이 문제는 yield from 문이 있는 재귀 제너레이터를 만들어 쉽게 해결할 수 있다.
   토론 :    
   
   
 """

print('###############################################################################')
print('##########################################4.14 중첩 시퀀스 풀기 #####################################')
print('###############################################################################')


# 중첩된 시퀀스를 합쳐 하나의 리스트로 만들려면, yield from 문이 있는 재귀 제너레이터를 만들어 쉽게 해결할 수 있다.
from collections import Iterable
#
# def flatten(items, ignore_types=(str, bytes)):
#     for x in items:
#         if isinstance(x, Iterable) and not isinstance(x, ignore_types):  #isinstance는 아이템이 순환가능 한것인지 확인한다.
#             yield from flatten(x)      #순환이 가능하다면 yield from 으로 모든 값을 하나의 서브루틴으로 분출한다.
#         else:
#             yield x

items = [1, 2, [3, 4, [5, 6], 7], 8]


# Produces 1 2 3 4 5 6 7 8
# for x in flatten(items):
#     print(x)
#



"""
책에 나온 코드구동이 안됩니다..
"""


# 추가적으로 전달 가능한 인자 ingore_types와 not isinstance(x, ignore_types)로 문자열과 바이트가
# 순환 가능한 것으로 해석되지 않도록 했다. 이렇게해야만 리스트에 담겨 있는 문자열을 전달했을 때 문자를 하나하나 펼치지 않고
# 문자열 단위로 전개한다.
#
# items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
# for x in flatten(items):
#     print(x)
#






"""
                                                ▶ 4.15 정렬된 여러 시퀀스를 병합 후 순환◀ 
♣  문제 :  정렬된 시퀀스가 여러 있고, 이들을 하나로 합친 후 정렬된 시퀀스를 순환하고 싶다.

↘  해결 :  heapq.merge()함수를 사용하면 된다.
   토론 :  heapq.merge()는 아이템에 순환적으로 접근하며 제공한 시퀀스를 한꺼번에 읽지 않는다.
          따라서, 아주 긴 시퀀스도 별다른 무리 없이 사용할 수 있다. 
          
          위 함수는 모두 정렬되어 있어야 한다. 이 함수에 전달한다고 우선적으로 정렬해주거나 하지 않는다.
          또한 input 데이터가 정렬되어있는지 확인도 안한다.
          단지 앞에서부터 읽어가면서 출력할 뿐
          
 """

print('###############################################################################')
print('##########################################4.15 정렬된 여러 시퀀스를 병합 후 순환#####################################')
print('###############################################################################')


#heapq.merge하기
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


#정렬된 두 파일을 병합하려면 다음과 같이 한다.
#
# with open('파일1','rt') as file1, \
#     open('파일2','rt') as file2, \
#     open('합친파일','wt') as outf:
#
#     for line in heapq.merge(file1,file2):
#         outf.write(line)
#





"""
                                                ▶ 4.16 무한 while 순환문을 이터레이터로 치환◀ 
♣  문제 :  함수나 일반적이지 않은 조건 테스트로 인해 무한 while 순환문으로 데이터에 접근하는 코드를 만들었다.

↘  해결 :  입출력과 관련 있는 프로그램에 일반적으로 다음과 같은 코드를 사용한다.
   토론 :  내장 함수 iter() 의 기능은 거의 알려져 있지 않다. 이 함수에는 선택적으로 인자 없는
          호출 가능 객체와 종료 값을 입력으로 받는다. 이렇게 사용하면 주어진 종료 값을 반환하기 전까지 
          무한히 반복해서 호출 가능 객체를 호출한다.

 """

print('###############################################################################')
print('##########################################4.16 무한 while 순환문을 이터레이터로 치환#####################################')
print('###############################################################################')

CHUNKSIZE = 8192

# def reader(s):
#     while True:
#         data = s.recv(CHUNKSIZE)
#         if data ==b'':
#             break
#         process_data(data)

#위 코드는 iter()를 사용해 다음과 같이 이터레이터로 치환할 수 있다.

# def reader(s):
#     for chunk in iter(lambda: s.recv(CHUNKSIZE), b''):
#         process_data(data)



#정말 이 코드가 동작하는지 믿음이 가지 않는다면 파일과 관련 있는 예제를 실행해보자.




