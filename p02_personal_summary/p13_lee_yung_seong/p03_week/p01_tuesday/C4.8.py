#순환 객체 첫 번째 부분 건너뛰기
#문제 : 순환 객체의 아이템을 순환하려고 하는데, 처음 몇 가지 아이템에는 관심이 없어 건너뛰고 싶다.
#해결 : itertools 모듈에 이 용도로 사용할 수 있는 몇가지 함수가 있음. 첫번째는 itertools.dropwhile() 함수이다.
#이 함수를 사용하려면 함수와 순환 객체를 넣음ㄴ 된다. 반환된 이터레이터는 넘겨준 함수가 True를 반환하느 동안은 시퀀스의 첫번째 아이템을 무시한다.
#그 후에는 전체 시퀀스를 생성한다.
#이를 알아보기 위해서 주석으로 시작하는 파일을 읽는다고 가정해보자.
#주석을 무시하려면?
from itertools import dropwhile
with open(...) as f:
    for line in dropwhile(lambda line : line startswith('#'), f):
        print(line, end=' ')

from itertools import islice
items = ['a','b','c',1,4,10,15]
for x in islice(items,2,None):
    print(x)
#토론 dropwhile, islice는 복잡한 코드를 작성하지 않도록 도와준다,