####################################################################################################
# 3.11] 임의의 요소 뽑기
#   * 시퀀스에서 임의의 아이템을 고르거나 난수를 생성하고 싶다.
#
#   * 이론
#     random 모듈은 Mersenne Twister 알고리즘을 이용해 난수를 생성한다.
#     이 알고리즘은 정해진 것이지만, random.seed() 함수로 시드 값을 바꿀 수 있다.
#
#     random()의 함수는 암호화 관련 프로그램에서 사용하지 말아야 한다. (더 안전하게 ssl 모듈 사용)
#
# 1] random.choice()
#   : 시퀀스에서 임의의 아이템 선택
# 2] random.sample()
#   : 임의의 아이템을 N개 뽑아서 사용하고 버릴 목적
# 3] random.shuffle()
#   : 시퀀스 아이템 셔플
# 4] random.randint()
#   : 임의의 정수 생성
# 5] random.random()
#   : 0과 1 사이의 균등 부동 소수점 값 생성
# 6] random.getrandbits()
#   : N비트로 표현된 정수 생성
####################################################################################################
import random

values = [1, 2, 3, 4, 5, 6]

## 시드 값 설정(선택)
random.seed()   # 시스템 시간이나 os.urandom() 시드
random.seed(12345)  # 주어진 정수형 시드
random.seed(b'bytedata')    # 바이트 데이터 시드

## 임의의 아이템 1개 선택
a = random.choice(values)
print(a)    # 3

## 임의의 아이템 N개 선택
b = random.sample(values, 2)
print(b)    # [2, 4]

## 시퀀스 셔플
random.shuffle(values)
print(values)   # [5, 2, 4, 6, 3, 1]

## 임의의 정수 생성
d = random.randint(0,10)
print(d)    # 3

## 균등 부동소수점 생성
e = random.random()
print(e)    # 0.8417019862225978

## 200비트로 표현된 정수 생성
f = random.getrandbits(200)
print(f)    # 954619124442937630457988544363542831775003646840892304038342