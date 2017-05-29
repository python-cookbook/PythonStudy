##########################################################################################################
# 4.14] 중첩 시퀀스 풀기
#   * 중첩된 시퀀스를 합쳐 하나의 리스트로 만들고 싶다.
#
# 1] yield from 문이 있는 재귀 제너레이터 생성
#   * isinstance : 아이템이 순환 가능한지 확인
##########################################################################################################
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
for x in flatten(items):
    print(x, end=' ')   # 1 2 3 4 5 6 7 8