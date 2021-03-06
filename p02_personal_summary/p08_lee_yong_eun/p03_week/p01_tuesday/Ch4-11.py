##########################################################################################################
# 4.11] 여러 시퀀스 동시에 순환
#   * 여러 시퀀스에 들어있는 아이템을 동시에 순환하고 싶다.
#
# 1] zip()
#   : zip(a, b)는 tuple(x, y)를 생성하는 이터레이터를 생성한다.(x는 a에서, y는 b에서 가져온다)
#     순환은 한쪽 시퀀스의 입력이 모두 소비되었을 때 끝난다. (즉 짧은 시퀀스의 길이만큼만 순환한다)
# 2] itertools.zip_longest()
#   : 두 시퀀스 중 긴 쪽으로 순환이 돌게 한다.
#     짧은 쪽의 소비가 끝나면 이후로 None을 반환
#
#   * zip()은 데이터를 묶어야 할 때 주로 사용한다. 예를 들어 열 헤더와 값을 리스트로 각각 가지고 있을 때
#     s = dict(zip(headers,values)) 와 같이 딕셔너리 형태로 묶을 수 있다.
##########################################################################################################
xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99]
for x, y in zip(xpts, ypts):
    print(x, y, end=' / ')  # 1 101 / 5 78 / 4 37 / 2 15 / 10 62 / 7 99 /

a = [1, 2, 3]
b = ['w', 'x', 'y', 'z']
for i in zip(a,b):
    print(i, end=' / ')  # (1, 'w') / (2, 'x') / (3, 'y') /

print()
from itertools import zip_longest
for i in zip_longest(a, b):
    print(i, end=' / ') # (1, 'w') / (2, 'x') / (3, 'y') / (None, 'z') /

