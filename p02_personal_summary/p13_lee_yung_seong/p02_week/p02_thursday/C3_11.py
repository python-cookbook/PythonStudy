#3.11 임의의 요소 뽑기
#문제 : 시퀀스에서 임의의 아이템이나 난수를 생성하고 싶다.
#해결 : random 모듈에는 이 용도에 사용할 수 있는 많은 함수가 있다. 예를 들어 시퀀스에서 임의의 아이템을 선택하려면 random.choice()를 사용한다.
import random
values = [1,2,3,4,5,6]
random.choice(values)
#임의의 아이템 N개를 뽑아서 사용하고 버릴 목적이라면 random.sample()을 사용한다.
random.sample(values,2)
values
#단순히 시퀀스의 아이템을 무작위로 섞으려면 random.shuffle
random.shuffle(values)
values
#임의의 정수
random.randint(0,10)
#0~1사이 소수점 랜덤
random.random()
#N비트로 표현된 정수를 만들기 위해서는 random.getrandbits()
random.getrandbits(200)
#토론 랜덤 모듈은 Mersenne Twister 알고리믖ㅁ을 사용해 난수를 발생시킴. 이 알고리즘은 정해진 것이지만 random.seed() 함수로 시드값을 변경가능
random.seed()            #시스템 시간이나 os.urandom()시드
random.seed(12345)       #주어진 정수형 시드
random.seed(b'bytedata') #바이트 데이터 시드

#이 기능 외에 유니폼, 가우시안, 확률 분포 관련 함수도 포함되어 있다.
random.uniform()#균등분포숫자 계산
random.gauss()#정규분포 숫자 계산
#암호화 기능은 ssl모듈을 사용하자.