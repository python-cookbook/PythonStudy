###################################################################################################
## 1. 문제        : 배낭 채우기1 (중급)
## 2. 소요 시간   : 0.016 초 (소수점 6자리 반올림)
## 3. 사용 메모리 :  24576 byte
## 4. 만든 사람   : 조태흠
###################################################################################################

import os
import time
import psutil
################# 시작 메모리 체크 #################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

#################알고리즘 풀이#########################################################
number = int(input('숫자를 입력하세요 '))
stime = time.time()   # 시작시간 체크
num = number
cnt = 0
for i in range(num, 0, -1):
    s_number = i**2
    for j in range(num):
        if s_number <= num:
            num -= s_number
            cnt += 1
            print('{}^'.format(i))
        if num == 0:
            break
print(number, '은 최소 {}개항의 제곱수 합으로 표현할 수 있다.'.format(cnt))

################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)