import os
import time
from copy import deepcopy
import psutil

###################################################################################################
## 1. 문제        : 소수와 합성수 (초급)
## 2. 소요 시간   : 0.000128 초 (소수점 6자리 반올림) (입력시간 포함
## 3. 사용 메모리 :  32768 byte
## 4. 만든 사람   : 임미선
###################################################################################################

# input 받기inputs = input('숫자를 입력하세요')
inputs = input('숫자를 입력하세요')
numbers =inputs.split(' ')          #공백 기준 숫자 분리
numlist = list(map(lambda x: int(x), numbers))  #str -> int

################ 시작 메모리 체크 #################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 #################
stime = time.time()

#recognizing numbers
for number in numlist:
    cnt = 0
    for i in range(1,number+1): #1부터 해당숫자까지 loop
        if number % i ==0:
            cnt += 1            #나눠질 때 마다 cnt +1
    if cnt == 1 :
        print(number, "number one")
        continue
    if cnt == 2 :
        print(number, "prime number")
        continue
    else:
        print(number, "composite number")


################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
