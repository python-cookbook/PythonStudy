import os
import time
import psutil

###################################################################################################
## 1. 문제        : 소수와 합성수 (초급)
## 2. 소요 시간   : 0.002 초 (소수점 6자리 반올림)
## 3. 사용 메모리 :  16384 byte
## 4. 만든 사람   : 원지은
###################################################################################################


nums=input("자연수 5개를 입력하세요~ ").split(' ')


################# 시작 메모리 체크 #########################################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 ##################
stime = time.time()
#################################################


from collections import defaultdict
divisor=defaultdict(list)                 # 약수를 담을 딕셔너리

for j in range(5):
    for i in range(1,int(nums[j])+1):
        if int(nums[j])%i==0:             #자연수마다 약수를 구해서
            divisor[nums[j]].append(i)    #딕셔너리에 넣는다

for value in divisor.values():      # 각 자연수의 약수가
    if len(value)==2:               # 소수인 경우
        print("prime number")
    elif len(value) >=3:            # 합성수인 경우
        print("composite number")    
    else:                           # 소수도 합성수도 아닌 경우
        print("number one")


################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
       