import os
import time
import psutil

###################################################################################################
## 1. 문제        : 스택 (초급)
## 2. 소요 시간   : 14.451689 초 (입력시간 포함)
## 3. 사용 메모리 : 57344 byte
## 4. 만든 사람   : 임미선
###################################################################################################

# ################ 시작 메모리 체크 #################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 #################
stime = time.time()

import re
def stack():
    res = []
    num = input('명령 개수를 입력하세요')
    cnt = 0
    inputs = input('명령어를 입력하세요 ')
    while cnt != int(num):
        if re.search('^i',inputs):
            val = inputs.split()[1]
            res.append(val)
            cnt += 1
            if cnt == int(num):
                break
            inputs = input('명령어를 입력하세요 ')
        if inputs == 'o':
            try :
                res.pop()
                cnt += 1
                if cnt == int(num):
                    break
                inputs = input('명령어를 입력하세요 ')
            except IndexError:
                print('empty')
                cnt += 1
                if cnt == int(num):
                    break
                inputs = input('명령어를 입력하세요 ')
        if inputs == 'c':
            print( len(res))
            cnt += 1
            if cnt == int(num):
                break
            inputs = input('명령어를 입력하세요 ')

stack()


################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)

