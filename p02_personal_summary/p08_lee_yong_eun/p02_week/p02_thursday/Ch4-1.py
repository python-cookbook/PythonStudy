####################################################################################################
# 4.1] 수동으로 이터레이터 소비
#   * 순환 가능한 아이템에 접근할 때 for 순환문을 사용하고 싶지 않다.
#
# 1] 수동으로 이터레이터를 소비하기 위해서는, next() 함수를 사용하고
#       StopIteration 예외를 처리하기 위한 코드를 직접 작성한다.
#   * 일반적으로 StopIteration은 순환의 끝을 알리기 위해 사용한다.
#
# * 대개의 경우 순환에 for 문을 사용하지만, 보다 더 정교한 조절이 필요한 때도 있다.
#   기저에서 어떤 동작이 일어나는지 정확히 알아둘 필요가 있다.
####################################################################################################

## next()를 이용하여 파일에서 줄을 읽는 구문
with open('/etc/passwd') as f:
    try:
        while True:
            line = next(f)
            print(line, end='')
    except StopIteration:
        pass


## None과 같은 종료 값을 이용해서 순환을 끝낼 수도 있다.
with open('/etc/passwd') as f:
    while True:
        line = next(f)
        if line is None:
            break
        print(line, end='')


## 이터레이터의 순환 동작 이해하기
items = [1, 2, 3]
# 이터레이터 얻기
it = iter(items)    # items.__iter__() 실행
# 이터레이터 실행
print(next(it))    # it.__next__() 실행 : 1
print(next(it))    # 2
print(next(it))    # 3
print(next(it))    # StopIteration Exception