####################################################################################################
# 3.9] 큰 배열 계산
#   * 배열이나 그리드와 같이 커다라 숫자 데이터세트에 계산을 해야 한다.
#
# 1] Numpy 라이브러리
#   1-1] Numpy 기본 사용
#   1-2] 일반 함수(universal function)
#       : 일반 수식을 배열에도 그대로 사용할 수 있도록 기능 제공(math와 비슷하다.)
#         요소마다 math 모듈 함수로 계산하는 것보다 수백 배 빠르다! 가능하면 일반 함수를 쓰자!
#   1-3] 다차원 배열의 인덱싱 기능 확장
#       : 특정 영역에만 연산 적용
#         특정 조건을 만족하는 요소에만 가공
#         행 전체에 대한 연산 등
#
# * 이론
#   Numpy 배열은 C나 Fortran과 동일하게, 동일한 데이터 타입을 메모리에 연속으로 나열한다.
#   따라서 파이썬 리스트보다 훨씬 더 큰 배열을 만들 수 있다.
#   예를 들어 소수를 담는 10,000 x 10,000 2차원 그리드를 만들고 싶다면 간단히 다음과 같이 하면 된다.
#   grid = np.zeros(shape=(10000,10000), dtype=float)
#
#   참조 사이트 : http://www.numpy.org
####################################################################################################

x = [1, 2, 3, 4]
y = [5, 6, 7, 8]

## 표준 파이썬 리스트로 연산을 하기에는 더 복잡한 방법이 필요하다
print(x*2)  # [1, 2, 3, 4, 1, 2, 3, 4]
print(x+y)  # [1, 2, 3, 4, 5, 6, 7, 8]

## Numpy 배열
import numpy as np
# ax = np.array([1,2,3,4])
# ay = np.array([5,6,7,8])
# print(ax*2) # [2 4 6 8]
# print(ax+ay)    # [ 6  8 10 12]
# print(ax+10)    # [11 12 13 14]
# print(ax*ay)    # [ 5 12 21 32] : 같은 위치의 값끼리 곱셈
#
# ## 다항식 계산을 함수로 이용한 예시
# def f(x):
#     return 3*x**2 - 2*x + 7
#
# print(f(ax))    # [ 8 15 28 47]
#
# ## Numpy에서 제공되는 일반 함수
# print(np.sqrt(ax))  # [ 1.          1.41421356  1.73205081  2.        ]
# print(np.cos(ax))   # [ 0.54030231 -0.41614684 -0.9899925  -0.65364362]
#
# # 10000*10000 2차원 float grid 생성
# grid = np.zeros(shape=(10000,10000), dtype=float)
# print(grid)
# # [[ 0.  0.  0. ...,  0.  0.  0.]
# #  [ 0.  0.  0. ...,  0.  0.  0.]
# #  [ 0.  0.  0. ...,  0.  0.  0.]
# #  ...,
# #  [ 0.  0.  0. ...,  0.  0.  0.]
# #  [ 0.  0.  0. ...,  0.  0.  0.]
# #  [ 0.  0.  0. ...,  0.  0.  0.]]
#
# grid += 10
# print(grid)
# # [[ 10.  10.  10. ...,  10.  10.  10.]
# #  [ 10.  10.  10. ...,  10.  10.  10.]
# #  [ 10.  10.  10. ...,  10.  10.  10.]
# #  ...,
# #  [ 10.  10.  10. ...,  10.  10.  10.]
# #  [ 10.  10.  10. ...,  10.  10.  10.]
# #  [ 10.  10.  10. ...,  10.  10.  10.]]
#
## 배열로서의 인덱싱 기능 활용 예제
a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print(a)
# [[ 1  2  3  4]
#  [ 5  6  7  8]
#  [ 9 10 11 12]]

#첫번째 행 선택
print(a[0]) # [1 2 3 4]
#첫번째 열 선택
print(a[:,0])   # [1 5 9]

##특정 영역만 선택 후 변경
print(a[1:3, 1:3])
# [[ 6  7]
#  [10 11]]

a[1:3, 1:3] += 10
print(a)
# [[ 1  2  3  4]
#  [ 5 16 17  8]
#  [ 9 20 21 12]]

## 행 벡터를 모든 행 연산에 적용
print(a + [100, 101, 102, 103])
# [[101 103 105 107]
#  [105 117 119 111]
#  [109 121 123 115]]

## 특정 조건에 맞는 요소의 값만 바꾸어 보여주기(실제 값은 안 바뀐다)
print(np.where(a < 10, a, 10))
# [[ 1  2  3  4]
#  [ 5 10 10  8]
#  [ 9 10 10 10]]