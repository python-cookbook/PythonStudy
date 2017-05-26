#제너레이터로 새로운 순환 패턴 생성


#문제 : 내장함수(range)_, reversed()) 와는 다른 동작을 하는 순환 패턴을 만들고 싶다.
#해결 : 새로운순환 패턴을 만들고 싶다면 제너레이터 함수를 사용해서 정의 해야 된다.
def frange(start,stop,increment):
    x = start
    while x < stop:
        yield x
        x += increment

for n in frange(0,4,0.5):
    print(n)

list(frange(0,1,0.125))

#토론 : 내부의 yield문이ㅡ 존재로 인해 함수가 제너레이터가 되었다. 일반 함수와는 다르게 제너레이터는 순환에 응답하기 위해 실행된다. 이런 함수가 어떻게 동작하는지 다음 예를 통해 알아보자.
def countdown(n):
    print('Starting to count from',n)
    while n > 0:
        yield n
        n -= 1
    print('Done')

c = countdown(3)
c
next(c)
#중요한 점은 제너레이터 함수가 순환에 의한 "다음" 연산에 응답하기 위해서만 실행된다는 점이다.
#제너레이터 함수가 반환되면 순환을 종료한다. 하지만 일반적으로 순환에 사용하는 for문이 상세 내역을 책임지기 때문에 우리가 직접적으로 신경쓰지 않아도 됨.
