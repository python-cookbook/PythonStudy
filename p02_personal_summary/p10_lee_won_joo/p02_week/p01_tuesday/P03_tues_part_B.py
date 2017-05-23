"""
                                                ▶ 3.6 복소수 계산 ◀ 
♣  문제 : 최신 웹 인증을 사용하는 코드를 작서하던 도중, 복소수 평면을 사용할 수 밖에 없는 상황 처함
        혹은 복소수 사용하여 계산해야 한다.
↘  해결 : 복소수는 complex(reaml, imag)함수를 사용하거나 j를 붙인 부동 소수점 값으로 표현할 수 있다.
         1. 복소수 표현
            a. complex(정수,허수)
            b. 3-5j, 2_+1j
         2. 실수, 허수, 켤레복소수 표현
            a. 허수부분 a.imag
            b. 실수부분 a.real
            c. 켤레복소수 a.conjugate()
         3. 일반 사칙연산 가능
            5-1j + 3+1j
                ..
         4. 삼각함수 계산 가능 ( cmath  모듈)
            import cmath
            sin = cmath.sin(복소수)
            cos = cmath.cos(복소수)
            tan = cmath.tan(복소수)
            exp = cmath.exp(복소수)   #제곱

   토론 : 1. numpy와 같은 수학관련 모듈 대부분 복소수를 인식한다.
            1) 복소수 배열 생성가능
                a. [ 2.+3.j  4.+5.j  6.-7.j  8.+9.j]
            2) 배열 사칙연산 가능
                a. (2) + [ 2.+3.j  4.+5.j  6.-7.j  8.+9.j] 
                = [  4.+3.j   6.+5.j   8.-7.j  10.+9.j]
            3) numpy 삼각함수 가능
                a. np.sin(a)
         2. 일반 수학모듈은 복소수 값 만들지 않아 떄떄로 에러가 발생
            1) math.sqrt(-1)   #Error
            2) 위 문제 해결을 위해선 cmath 활용
                a. cmath.sqrt(-1)   #1j
 """
print('########################################## 3.6 복소수 계산#####################################')

# 복소수 표현    ===> complex(정수,±()j)
a = complex(2, 4)
b = 3 - 5j
print(a, b)

# 실수, 허수, 켤레 복소수를 구하는 방법은 어렵지 않다.

c = a.imag  # a.imag 는 2+4j의 허수부분인 4
g = a.conjugate()  # a의 켤레복소수  a= 2+4j 이라면, a.conjugate =2-4j
print(c)
print(g)

# 또한 일반적인 수학 계산도 잘 동작한다.

d = a + b  # 5-1j
c = a * b  # 26+2j
g = a / b
print(('나누기', g))
print(abs(b))  # 5.83...

# 사인, 코사인, 제곱 등을 계산하려면 cmath 모듈을 사용한다.

import cmath

com_sin = cmath.sin(a)
com_cos = cmath.cos(a)
com_exp = cmath.exp(a)
com_tan = cmath.tan(a)
print(com_sin, com_cos, com_exp, com_tan)

# 파이썬의 수학관련 모듈 대개는 복소수를 인식한다.
# ex) numpy의 경우 복소수 배열 계산 가능하다.

import numpy as np

a = np.array([2 + 3j, 4 + 5j, 6 - 7j, 8 + 9j])
print(a)
print(a + 2)
print(np.sin(a))

# 허나, 파이썬 일반수학모듈의 경우 복소수값 만들지 않는다.
# 때로는 이런 값 발생가능

# import math
# minus_sqrt = math.sqrt(-1) #math domain error
# print(minus_sqrt)




"""
                                                ▶ 3.7 무한대와 NaN 사용 ◀ 
♣  문제 : 부동 소수점 값의 무한대, 음의 무한대, NaN(not a number)을 검사해야 한다.
↘  해결 : 이와 같은 특별한 부동 소수점 값을 표현하는 파이썬 문법은 없지만,
         float()을 사용해서 만들수는 있다.

   토론 : 주의해야할 점
          1. 무한대 값은 일반적인 수학 계산법을 따른다.
            a. inf+45 = inf   /   10/inf  = 0.0
          2. 하지만 특정 연산자의 계산은 정의되어 있지 않고, NaN을 발생시킨다.
            a. inf/inf = nan   / inf+ (-inf) = nan
          3. NaN값은 모든 연산자에 대해 예외를 발생시키지 않는다.
            a. nan+23 = nan   / nan/2 = nan   / sqrt(nan) = nan
          4. Nan은 비교 결과가 일치하지 않는다. 오직 isnan으로 확인하는 것만이 기능함
            a. nan == nan   >> False    / nan is nan  >> False
            b. math.isnan()  >> True
          5. 

 """
print('########################################## 3.7 무한대와 NaN사용 #####################################')

a = float('inf')
b = float('-inf')
c = float('nan')
print(a, b, c)  # <class 'float'>

# 위 값 확인해보기
import math

print(math.isinf(a))  # True
print(math.isinf(c))  # False

# 앞에 나온특별한 부동 소수점 값에 대한 더 많은 정보를 원한다면 IEEE 754스펙을 확인해봐야 한다.
# 그 중 주의해야 할 것이 몇가지 있는데, 특히 비교와 연산자 부분에 관련이 있다.

# 무한대 값은 일반적인 수학 계산법을 따른다.

a = float('inf')
print(a + 45)  # inf
print(a * 10)  # inf
print(10 / a)  # 0

# 하지만 특정 연산자의 계산은 정의되어 있지 않고 NaN을 발생시킨다.

a = float('inf')
print(a / a)  # NaN

b = float('-inf')
print(a + b)  # NaN

# NaN값은 모든 연산자에 대해 예외를 발생시키지 않는다.

c = float('nan')
print(c + 23)  # nan
print(c / 2)  # nan
print(c * 2)  # nan
print(math.sqrt(c))  # nan

# NaN에서 주의해야 할 점은, 이 값은 절대로 비교 결과가 일치하지 않는다는 점이다.

c = float('nan')
d = float('nan')
print(c == d)  # false

# NaN 또는 무한대 값 발생 시, 예외를 발생시키고자 한다면 fpect1모듈 사용 가능하지만
# 기본적으로 파이썬 빌드 에는 활성화 되어 있지 않다.
# 추가적으로 더 연구해봐야 할듯





"""
                                                ▶ 3.8 분수 계산 ◀ 
♣  문제 : 분수계산하기
↘  해결 : 분수 관련 계산을 위해 fractions모듈을 사용한다.


   토론 : 
         limit_denominator : 
            def:   Finds and returns the closest Fraction to self that has denominator at most max_denominator. 
                    This method is useful for finding rational approximations to a given floating-point number
                    분모가 최대 max_denominator 인 자기에 가장 가까운 분수를 찾아서 반환합니다. 
                    이 방법은 주어진 부동 소수점 수에 대한 유리한 근사값을 찾는 데 유용합니다.


         Fraction 모듈의 기능
            1. 튜플형태(원소 2개)의 값을 분수로 변환해준다.
            2. 분자(numerator)/ 분모(denominator) 빼내기
            3. float타입의 값을 소수로 변환하는데 활용하기 ( float( Fraction(값)  ) )
            4. 
 """
print('########################################## 3.8 분수 계산하기 #####################################')

from fractions import Fraction

a = Fraction(5, 4)  # 5/4
b = Fraction(7, 16)  # 7/16
print(a + b)  # 27/16
print(a * b)  # 35/64
print(a / b)  # 20/7

c = a * b  # c= 35/64이겠다.
# 분자(numerator)/ 분모(denominator) 빼내기
print(c.numerator)  # 35
print(c.denominator)  # 64

# 소수로 변환하기

Fraction_to_float = float(c)  # c= 35/64
print(Fraction_to_float)  # c= 0.546875
# print(Fraction_to_float.numerator)  # 'float' object has no attribute 'numerator'


# 분모를 특정 값으로 제한하기   함수명은 분모제한?
print(c.limit_denominator(8))  # 4/7

# 소수를 분수로 변환

x = 3.75
y = Fraction(*x.as_integer_ratio())
y_2 = Fraction(x)
print(y)
print(y_2)  # 둘다 결과가 15/4인데 뭐가 다른걸까..?
# 뭔가 이상하다. 3.75/4.75/5.75 값은 제대로 최적의 분수값을 제공하는데
# 3.76만 넣어도, 값이 43255432443/354230448902480 이런식으로 나온다.


# 분해해보기
only_integer_ratio = x.as_integer_ratio()
print(only_integer_ratio)  # (15,4)
print(type(only_integer_ratio))  # 튜플타입으로 반환한다.
# Frac = Fraction(only_integer_ratio)  #Error
# print(Frac)  #argument should be a string or a Rational instance


# 즉, Fraction의 매개변수로 받는 x.as_integer_ratio()는 튜플형태로 변수로써 제공해주려 하지만
# Fraction 메소드 자체가 argument를 쉽게 받아주지 않는다.
# 따라서 앞에 가변매개변수 처리인 * 를 붙여줘야함
# 근데, Fraction 메소드가 그냥 float타입의 값은 굳이 가변매개변수 하지 않아도 에러나지 않음..ㅠㅠ

Frac = Fraction(*only_integer_ratio)
print(Frac)
print(type(Frac))  # <class 'fractions.Fraction'>

# 프로그래머들은 분수계산 많이 사용하지는 않으나, 유리한 상황이 생길수는 있다.
# 프로그램에서 치수 단위를 분수로 받아서 계산을 하는 것이 , 유저가 소수로 직접 변환하고 계산하는 것보다 더 편리할 수 있다.



"""
                                                ▶ 3.9 큰 배열 계산◀ 
♣  문제 : 배열이나 그리드와 같이 커다란 숫자 데이터셋에 계산을 해야 한다.
↘  해결 : 배열이 관련된 커다란 계산을 하려면 Numpy 라이브러리를 사용한다.
         표준 파이썬 보다 효율적임. 



   토론 : 


 """
print('########################################## 3.9 큰 배열 계산 #####################################')

x = [1, 2, 3, 4]
y = [5, 6, 7, 8]
print(x * 2)  # 난 처음에 [2,4,6,8]이 될줄 알았는데.. [1,2,3,4,1,2,3,4] 이다.
# print(y+2)    #따라서 + - / 는 다 안된다. 마치 string *2 가 파이썬에서 작동되듯


# numpy배열해보기
print('numpy')
import numpy as np

ax = np.array([1, 2, 3, 4])
ay = np.array([5, 6, 7, 8])

multiply = ax * 2  # [2 4 6 8]
plus = ax + 2  # [3 4 5 6]
each_plus = ax + ay  # [ 6  8 10 12]
minus = ax - 2  # [-4 -4 -4 -4]
each_minus = ax - ay  # [-1  0  1  2]
# print(multiply)
# print(plus)
# print(each_plus)
# print(each_minus)
# print(minus)

# 앞에 나온 대로 기본적인 수학 계산에 있어 많은 차이를 보인다.
# 특히 스칼라 연산  (ax * 2 or  ax + 10 등) 이 요소 기반으로 적용된다.
# 또한 배열과 배열 간 계산을 하면 연산자가 모든 요소에 적용되고 새로운 배열을 생성한다.

# 수학 연산이 모든 요소에 동시 적용된다는 점으로 인해 매우 빠르고 쉬운 배열 계산가능
# 따라서 다음과 같은 다항식 계산을 원하면 다음과 같이 한다.

print(ax)


def f(x):
    return 3 * x ** 2 - 2 * x + 7  # 3x^2 - 2x + 7


f(ax)  # [ 8 15 28 47]

# Numpy는 배열에 사용 가능한 "일반 함수(universal function)"을 제공한다.
# math 모듈이 제공하는 함수와 비슷하다.

print(np.sqrt(ax))
print(np.cos(ax))

# 계산 속도는 일반함수가 math모듈보다 훨~~씬 빠르다.
# math모듈은 순환하며 요소마다 계산하기 때문에 너무 느리다 ㅠㅠ
# numpy배열은 C 또는 fortran과 동일한 방식으로 할당한다.
# 다시 말해, 동일한 데이터 타을 메모리에 연속으로 나열한다.
# 따라서 파이선 리스트 보다 훨씬 더~~ 큰 배열을 만들 수 있다.
# 예를 들어, 소수를 담는 10,000 X 10,000 2차원 그리드를 만들고 싶다면 간단히 다음과 같이 하면 된다.

grid = np.zeros(shape=(10000, 10000), dtype=float)
print(grid)  # len  = 10000

# 마찬가지로 모든 연산은 모든 요소에 동시 적용된다.

grid += 10  # 모든 요소에 10을 더해라?
print(grid)

# 묘든 요소에 sin함수를 적용하라.
# print(np.sin(grid))   #-0.54402111, -0.544...  #메모리 에러떴다..뭐냐..얼마 안먹는다매..

# 넘파이가 다차원 배열의 인덱싱 기능을 확장하고 있다는 점을 주목해야 한다.

a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print(a)

# a의 첫번째 행을 선택해보자!
print('a의 첫번째 행을 선택해보자!')
b = a[1]
print(b)

# a의 첫번째 열을 선택해보자.
print('a의 첫번째 열을 선택해보자.')
b = a[:, 1]
print(b)

print('지역을 선택 [1:3](첫번째 행부터 3이하, 즉 2번째 행까지부터  후 변경[1:3]  (1번쨰 열부터 3이하의 열, 즉 2번째 열까지 선택')
print(a[1:3, 1:2])  # a[행,열]
a[1:3, 1:3] += 10

print(a)

# 행 벡터를 모든 행 연산에 적용

print(a + [100, 101, 102, 103])
print(a)

# 조건이 있는 할당

c = np.where(a > 10, a, 10)
print(c)

# numpy는 과학,공학 라이브러리 기초..







"""
                                                ▶ 3.10 행렬과 선행 대수 계산◀ 
♣  문제 : 행렬 곱셈, 행렬식 찾기, 선형 방정식 풀기 등 행렬이나 선형 대수 계산을 해야 한다.
↘  해결 : Numpy에 이런 용도로 사용할 수 있는 객체는 matrix 객체가 있다.
         행렬은 레시피에 나왔던 배열 객체와 비슷한 면이 있지만, 계산할 때는 선형대수 계산법을 따른다.




   토론 : 


 """
print('########################################## 3.10 행렬과 선행 대수 계산 #####################################')

import numpy as np

m = np.matrix([[1, -2, 3], [0, 4, 5], [7, 8, -9]])
m
# matrix([[ 1, -2,  3],
#         [ 0,  4,  5],
#         [ 7,  8, -9]])
# 전치 행렬(transpose)
m.T
# matrix([[ 1,  0,  7],
#         [-2,  4,  8],
#         [ 3,  5, -9]])
# 역행렬(inverse)
m.I
# matrix([[ 0.33043478, -0.02608696,  0.09565217],
#         [-0.15217391,  0.13043478,  0.02173913],
#         [ 0.12173913,  0.09565217, -0.0173913 ]])
# 벡터를 만들고 곱하기
v = np.matrix([[2], [3], [4]])
v
# matrix([[2],
#         [3],
#         [4]])
m * v
# matrix([[ 8],
#         [32],
#         [ 2]])
import numpy.linalg

# Determinant  #행렬식
print(numpy.linalg.det(m))
# -229.99999999999983

import numpy.linalg

# Determinant
numpy.linalg.det(m)
# -229.99999999999983
# Eigenvalues  (고유값)
numpy.linalg.eigvals(m)
# array([-13.11474312,   2.75956154,   6.35518158])
# mx = v에서 x 풀기
x = numpy.linalg.solve(m, v)
x
# matrix([[ 0.96521739],
#         [ 0.17391304],
#         [ 0.46086957]])
m * x
# matrix([[ 2.],
#         [ 3.],
#         [ 4.]])
#### m*x = v가 나왓다!!!
# 선형대수의 범위는 너무 방대하여 다 다룰 수 없으나, 아무튼 하려면 numpy를 제대로 해야함



















