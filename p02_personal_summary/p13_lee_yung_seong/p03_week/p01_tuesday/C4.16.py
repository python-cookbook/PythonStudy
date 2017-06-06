#무한 while문을 이터레이터로 치환
#문제
#함수나 일반적이지 않은 조건 테스트로 인해 무한 while 순환문으로 데이터에 접근하는 코드를 만들었다.
#해결
#입출력과 관련 있는 프로그램에 일반적으로 다음과 같은 코드를 사용한다.
CHUNKSIZE = 8192
def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data ==b'':
            break
        process_data(data)

#앞의 코드는 iter()를 사용해 다음과 같이 수정할 수 있다.
def reader(s):
    for chunk in iter(lambda : s.recv(CHUNKSIZE),b''):
        process_data(chunk)
#정말 이 코드가 동작하는지 믿음이 가지 않는다면 파일과 관련 있는 예제를 실행해보자.
import sys
f = open('/etc/passwd')
for chunk in iter(lambda : f.read(10),''):
    n = sys.stdout.write(chunk)

#토론
#내장함수 iter의 기능은 거의 알려져 있지 않다. 이 함수에는 선택적으로 인자 없는 호출 가능 객체와 종료 값을 입력으로 받는다. 이렇게 사용하면 주어진 종료 값을 반환하기 전까지
#무한히 반복해서 호출 가능 객체를 호출한다.
#이런 방식을 사용하면 입출려고가 관련 있는 반복 호출에 잘 동작한다. 예를 들어 소켓이나 파일에서 특정 크기의 데이터를 읽으려 한다면, 반복적으로 read()나 recv()를 호출하고 파일 끝을 확인해야한다.
#이번 레시피를 따른다면 두가지 동작을 하나의 iter()호출로 합칠 수 있다. lambda를 사용하면 인자를 받지 않는 호출 객체를 만들 수 있고 원하는 크기의 인자를 recv나 read에 전달한다.

