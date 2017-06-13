import os
import psutil
import time

###################################################################################################
## 1. 문제        : 못생긴 수
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 24576 byte
## 4. 만든 사람    : 조원태
###################################################################################################

# 시작 메모리 체크 #################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

# 함수 설정 ############################################################
PrimeFactorization = [1] # 1을 포함하고 소인수분해를 담을 리스트
# 소인수분해 해주는 함수
def factorization(su_len,inputs):
    for i in range(2,su_len+1):
        if i % 2 == 0 or i % 3 == 0 or i % 5 == 0:
            if (i % 2 == 0 and i % 3 == 0) or (i % 2 == 0 and i % 5 == 0) or ( i % 3 ==0 and i % 5 == 0):
                PrimeFactorization.append(i)
        else: continue
    print(PrimeFactorization)
    return findcount(PrimeFactorization,inputs)

# 찾고자 하는 자릿수의 소인수분해 값을 구하는 함수
def findcount(primefactorization,inputs):
    result = [int(re) for re in primefactorization[inputs-1:inputs+1]]
    return result[0]

# 시작 시간 체크####################
stime = time.time()

# 메인 #########################################
su_len = int(input("N 의 수까지 ? "))
inputs = int(input("몇 번째 자리의 N의 값 ? "))
print(factorization(su_len,inputs))
print('\n')

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)

