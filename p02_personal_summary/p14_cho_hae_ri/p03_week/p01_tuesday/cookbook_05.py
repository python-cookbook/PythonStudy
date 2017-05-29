


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



