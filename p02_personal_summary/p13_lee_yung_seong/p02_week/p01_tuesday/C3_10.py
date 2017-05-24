#행렬과 선형 대수 계산
#문제 :행렬 곱셈, 행렬식 찾기, 선형 방정식 풀기 등 행렬이나 선형 대수 계산을 해야한다.
#해결 : numpy matrix를 사용하자.
import numpy as np
m = np.matrix([[1,-2,3],[0,4,5],[7,8,-9]])
m
m.T#전치행렬
m.I#역행렬
v = np.matrix([[2],[3],[4]])
m*v

import numpy.linalg
numpy.linalg.det(m)#determinant 행렬식
numpy.linalg.eigvals(m) #eigenvalue 고유값
#mx = v에서 x 풀기
x = numpy.linalg.solve(m,v)
x
m*x
v