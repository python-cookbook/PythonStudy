##########################################################################################################
# 4.9] 가능한 모든 순열과 조합 순환
#   * 아이템 컬렉션에 대해 가능한 모든 순열과 조합을 순환하고 싶다.
#
#   * 순열 : 순서 관련 있음
#   * 조합 : 순서 관련 없음
#
# 1] itertools.permutations()
#   : 가능한 순열 순환
# 2] itertools. combinations()
#   : 가능한 조합 순환
# 3] itertools.combinations_with_replacement()
#   : 같은 아이템을 두번 이상 선택할 수 있는 조합
#
#   * 순환과 관련된 복잡한 문제에 직면한다면 우선 itertools부터 살펴보자.
#     일반적인 문제라면 아마 이 모듈에 이미 해결책이 제시되어 있을 것이다.
##########################################################################################################
items = ['a', 'b', 'c']
from itertools import permutations, combinations
from itertools import combinations_with_replacement


## 순열
# items로 가능한 최대 길이의 모든 순열 반환
for p in permutations(items):
    print(p, end=' ')   # ('a', 'b', 'c') ('a', 'c', 'b') ('b', 'a', 'c') ('b', 'c', 'a') ('c', 'a', 'b') ('c', 'b', 'a')

# 순열의 길이 지정
for p in permutations(items, 2):
    print(p, end=' ')   # ('a', 'b') ('a', 'c') ('b', 'a') ('b', 'c') ('c', 'a') ('c', 'b')

## 조합
# items로 가능한 지정 길이의 모든 조합 반환
for p in combinations(items, 3):
    print(p, end=' ')   # ('a', 'b', 'c')

for p in combinations(items, 2):
    print(p, end=' ')   # ('a', 'b') ('a', 'c') ('b', 'c')

print()
# 중복 선택 가능한 조합
for p in combinations_with_replacement(items, 3):
    print(p, end=' ')   # ('a', 'a', 'a') ('a', 'a', 'b') ('a', 'a', 'c') ('a', 'b', 'b') ('a', 'b', 'c') ...
