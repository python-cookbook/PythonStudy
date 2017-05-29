#가능한 모든 순열과 조합 순환

#문제 아이템 컬렉션에 대해 가능한 모든 순열과 조합을 순환하고 싶다.
#해결 itertools 모듈은 이와 관련 있는 세 함수를 제공한다. 첫째는 itertools.permutations()로 아이템 컬렉션을 받아 가능한 모든 순열을 튜플 시퀀스로 생성한다.
items = ['a','b','c']
from itertools import permutations
for p in permutations(items):
    print(p)

#만약 더 짧은 길이의 순열을 원한다면 선택적으로 길이 인자를 지정할 수 있다.
for p in permutations(items,2):
    print(p)


#itertools.combinations() 는 아이템의 가능한 조합 생성
from itertools import combinations

for c in combinations_with_replacement(items,3):
    print(c)
