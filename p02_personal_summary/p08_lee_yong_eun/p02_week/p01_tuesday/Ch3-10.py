####################################################################################################
# 3.10] 행렬과 선형 대수 계산
#   * 행렬 곱셈, 행렬식 찾기, 선형 방정식 풀기 등 행렬이나 선형대수 계산을 해야 한다.
#
# 1] numpy.matrix()
#   : 모양은 3.9의 배열과 유사하지만, matrix의 계산은 선형대수의 계산법을 따른다.
# 2] numpy.linalg
#   : 더 많은 연산을 담고 있는 서브패키지.
####################################################################################################
import numpy as np

## 행렬 정의
m = np.matrix([[1, -2, 3], [0, 4, 5], [7, 8, -9]])
print(m)
# [[ 1 -2  3]
#  [ 0  4  5]
#  [ 7  8 -9]]

## 전치 행렬(transpose)
print(m.T)
# [[ 1  0  7]
#  [-2  4  8]
#  [ 3  5 -9]]

## 역행렬(inverse)
print(m.I)
# [[ 0.33043478 -0.02608696  0.09565217]
#  [-0.15217391  0.13043478  0.02173913]
#  [ 0.12173913  0.09565217 -0.0173913 ]]

## 벡터를 만들어 곱하기(행렬 곱셈)
v = np.matrix([[2], [3], [4]])
print(m*v)
# [[ 8]
#  [32]
#  [ 2]]

###numpy.linalg
import numpy.linalg

## Determinant
print(numpy.linalg.det(m))  # -230.0

## Eigenvalues
print(numpy.linalg.eigvals(m))  # [-13.11474312   2.75956154   6.35518158]

## mx = v에서 x 풀기
x = numpy.linalg.solve(m, v)
print(x)
# [[ 0.96521739]
#  [ 0.17391304]
#  [ 0.46086957]]

## 결과 확인
print(m*x)
# [[ 2.]
#  [ 3.]
#  [ 4.]]
print(v)
# [[2]
#  [3]
#  [4]]