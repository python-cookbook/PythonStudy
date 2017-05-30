#중첩 시퀀스 풀기
#문제
#중첩된 시퀀스를 합쳐 하나의 리스트로 만들고 싶다.
#해결
#이 문제는 yield from 문이 있는 재귀 제너레이터를 만들어 쉽게 해결할 수 있다.
from collections import Iterable

def flatten(items, ignore_types=(str,bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x

items = [1,2,[3,4,[5,6],7],8]
for x in flatten(items):
    print(x)

#앞의 코드에서 isinstance(x, Iterable)은 순환 가능한 것인지 확인한다. 순환이 가능하다면 yield from 으로 모든 값을 하나의 서브루틴으로 분출한다.
#결과적으로 중첩되지 않은 시퀀스 하나가 만들어진다.
#추가적으로 전달 가능한 인자 ignore_types와 not isinstance(x, ignore_types)로 문자열과 바이트가 순환 가능한 것으로 해석되지 않도록 했다.
#이렇게 해야만 리스트에 담겨 있는 문자열을 전달했을 때 문자를 하나하나 펼치지 않고 문자열 단위로 전개한다.
items = ['Dave','Paula',['Thomas','Lewis']]
for x in flatten(items):
    print(x)

#토론
#서브 루틴으로써 다른 제너레이터를 호출할 때 yield from 을 사용하면 편리하다. 이 구문을 사용하지 않으면 추가적인 for문이 있는 코드를 작성해야 한다.
def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            for i in flatten(x):
                yield i
        else :
            yield x
#큰 차이는 아니지만 yield from이 더 깔끔하다.

