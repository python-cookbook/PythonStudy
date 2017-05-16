#######################################################################################
# 1.16) 시퀀스 필터링
#       * 시퀀스 내부에 데이터가 있고, 특정 조건에 따라 값을 추출하거나 줄이고 싶다.
#
# 1] List Comprehension 사용
#       : 특정 조건에 만족하는 값만 걸러내기
# 2] Filter() 사용
#       : 특정 조건을 담은 함수에서 True가 반환되는 값만 걸러내기 (반환값 : 이터레이터)
# 3] iterator.compress() 사용
#       : 어떤 시퀀스의 필터링 결과를 다른 시퀀스에 반영할 때 (반환값 : 이터레이터)
#
# 4] List Comprehension을 사용한 데이터 변형
#######################################################################################

# 1. List comprehension
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
res = [n for n in mylist if n > 0]
print(res)  # [1, 4, 10, 2, 3]
res = [n for n in mylist if n < 0]
print(res)  # [-5, -7, -1]
# 생성자 표현식 : 입력 내용이 클 시에 사용 가능
res = (n for n in mylist if n < 0)
print(res)  # <generator object <genexpr> at 0x00A2D030>
for x in res:
    print(x)    # -5 -7 -1

# 2. Filter()
values = ['1', '2', '-3', '-', '4', 'N/A', '5']
def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False
res = list(filter(is_int,values))
print(res)  # ['1', '2', '-3', '4', '5']

# 3. itertools.compress()
from itertools import compress
addresses = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
counts = [0, 3, 10, 4, 1, 7, 6, 1]
more5 = [x > 5 for x in counts] # 5보다 큰 경우 True, 그렇지 않으면 False
res = list(compress(addresses,more5))
print(res)  # ['C', 'F', 'G']

# List Comprehension을 사용한 데이터 변형
import math
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
res = [math.sqrt(x) for x in mylist if x > 0]
print(res)  # [1.0, 2.0, 3.1622776601683795, 1.4142135623730951, 1.7320508075688772]

# List Comprehension을 사용한 데이터 치환
res = [n if n > 0 else 0 for n in mylist]
print(res)  # [1, 4, 0, 10, 0, 2, 3, 0]
