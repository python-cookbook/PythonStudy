##########################################################################################################
# 4.8] 순환 객체 첫번째 부분 건너뛰기
#   * 순환 객체의 아이템을 순환하려고 하는데,처음 몇가지 아이템에는 관심이 없어 건너뛰고 싶다.
#
# 1] itertools.dropwhile()
#   : 특정 조건을 만족하는 부분을 건너뛴다.
# 2] itertools.islice()
#   : 뛰어넘어야 할 항목 수를 알고 있는 경우에 사용할 수 있다.
# 3] if 문을 이용
#   : 전체 파일에서 if 조건에 맞지 않는 부분을 전부 제거하게 된다. (전체 범위라는 점이 dropwhile과의 차이점)
##########################################################################################################
from itertools import dropwhile, islice


## f에서 처음 나오는 주석을 모두 무시하는 코드 : dropwhile
with open('/etc/passwd') as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line, end='')


## islice()를 사용
items = ['a', 'b', 'c', 1, 4, 10, 15]
for x in islice(items, 3, None):
    print(x, end=' ')   # 1 4 10 15


## f 전체에서 주석을 삭제
with open('/etc/passwd') as f:
    lines = (line for line in f if not line.startswith('#'))
    for line in lines:
        print(line, end='')

