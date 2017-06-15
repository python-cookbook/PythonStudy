import os
import time
import psutil
import random

###################################################################################################
## 1. 문제        : 제곱수의 합 (초급)
## 2. 소요 시간   : 0.001 초 (소수점 6자리 반올림)
## 3. 사용 메모리 :  24576 byte
## 4. 만든 사람   : 원지은
###################################################################################################

try:
    target_num=int(input("자연수를 입력하세요"))

    while target_num not in range(1,100001): # 1~100000 범위 밖의 숫자를 입력하면
        target_num=int(input("자연수를 입력하세요"))

except:
    target_num=int(input("1~100000사이의 자연수를 입력하세요")) #숫자를 입력하지 않았다면
    

################# 시작 메모리 체크 #########################################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 ##################
stime = time.time()
#################################################


small_pow=[] #제곱수를 담을 list
for i in range(target_num, 0, -1): # 최소의 제곱수의 개수를 찾아야 되기 때문에 역순으로 비교  
    if pow(i,2) <= target_num: # 만약 제곱한 수가 target_num보다 작다면

        target_num -= pow(i,2)  # target_num 에서 그 제곱한 수를 빼기
        
        small_pow.append(i) # 제곱수 append
        #print(i) # 제곱수 출력

        if target_num ==0 : # 제곱수를 빼고 남은 target_num이 0이면
            break           # 멈춰라

        if pow(i,2) <= target_num: # 그 제곱수가 아직 target_num보다 작다면
                        
            target_num -= pow(i,2) # 한번 더 빼고
    
            small_pow.append(i) # 한번더  append  ex) 8 = 2^2 + 2^2
            #print(i)
 
            if target_num ==0 : # 제곱수를 빼고 남은 target_num이 0이면
                break           # 멈춰라
           
print(len(small_pow)) # target num을 만드는 제곱수의 개수

     
################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
       