#역방향 순환

#문제 : 시퀀스 아이템을 역방향으로 순환하고 싶다.
#해결
#내장 함수 reversed()를 사용한다.
a = [1,2,3,4]
for x in reversed(a):
    print(x)

#역방향 순환은 객체가 __reversed_() 특별 메소드를 구현하고 있거나 크기를 알 수 있는 경우에만 가능하다.
#두 조건 중에서 아무것도 만족하지 못하면 객체를 먼저리스트로 변환 해야 한다.
#하지만 순환 가능 객체를 리스트로 변환할 때 많은 메모리가 필요하다.
#토론 __reversed__()메소드를 구현하면 사용자 정의 클래스에서 역방향 순환이 가능하다는 점이있다.
class Countdown:
    def __init__(self,start):
        self.start = start

    def __iter__(self):#순방향
        n = self.start
        while n > 0:
            yield n
            n -= 1
    def __reversed__(self):#역방향
        n=1
        while n <= self.start:
            yield n
            n+=1
#역방향 이터레이터를 정의하면 코드를 훨씬 효율적으로 만들어 주고 데이터를 리스트로 변환하고 순환하는 수고를 덜어준다.
