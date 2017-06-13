##########################################################################################################
# 7.7] 이름 없는 함수에서 변수 고정
#   * lambda를 사용해서 이름 없는 함수를 정의했는데, 정의할 때 특정 변수의 값을 고려하고 싶다.
##########################################################################################################

# 아래와 같이 lambda 생성 시 후에도 변수가 바뀌면 lambda 함수의 값이 함께 바뀐다.
x = 10
a = lambda y: x + y
x = 20
b = lambda y: x + y

print(a(10))    # 30
print(b(10))    # 30

# 값이 바뀌지 않게 생성된 순간의 값을 고정하는 방법
a = lambda y, x=x: x + y

# 람다 함수에 순환 변수를 잘못 사용한 경우
funcs = [lambda x: x+n for n in range(5)]
for f in funcs:
    print(f(0), end=' ')    # 4 4 4 4 4 : 바뀌지 않는다

# 제대로 사용한 경우
funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
    print(f(0), end=' ')    # 0 1 2 3 4