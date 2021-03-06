#객체순환(이터레이션)은 파이썬의 강력한 기능 중 하나이다. 순환을 단순히 시퀀스 내부 아이템에 접근하는 방법으로 생각할 수도 있다.
#하지만 순환을 통해 할 수 있는 일은, 순환 객체 만들기, itertools 모듈의 순환 패턴 적용하기, 제너레이터 함수 만들기 등 여러가지가 있다.


#수동으로 이터레이터 소비
#순환가능한 아이템에 접근할 때 for문을 사용하고 싶지 않다.
#해결 수동으로 이터레이터를 소비하려면 next()함수를 사용하고 StopIteration 예외를 처리하기 위한 코드를 직접 작성한다.
#일반적으로 StopIteration은 순환의 끝을 알리는데 사용한다. 하지만 next()를 수동으로 사용한다면 None과 같은 종료 값을 반환하는데 사용할 수 있다,
#대개의 경우 순환에 for문을 사용하지만 보다 더 정교한 조절이 필요한 때도 있다. 기저에서 어떤 동작이 일어나는지 정확히 알아둘 필요가 있다.
#다음 상호작용을 하는 예제를 통해 순환하는 동안 기본적을 어떤 일이 일어나는지 알아보자.
items = [1,2,3]
#이터레이터 얻기
it = iter(items)
next(it)
