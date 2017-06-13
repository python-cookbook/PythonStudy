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
res = []

while True: #명령수 1,100일때만 실행
    try:
        num = int(input('명령 개수를 입력하세요')) #num: 명령개수
        if 1 <= num <= 100:
            break
        else:
            raise ValueError
    except ValueError:
        print('다시 입력')

while num > 0:
    try:
        execute_statement = input('명령어를 입력하세요 ') #실행할 명령문
        if re.search('^i',execute_statement):
            if len(execute_statement.split()) != 2:
                raise ValueError
            val = int(execute_statement.split()[1]) #숫자변환 해줘야함
            res.append(val)
            num -= 1
        else:
            if execute_statement== 'o' or execute_statement == 'c':
                if execute_statement == 'o':
                    try :
                        print(res[-1])
                        res.pop()
                        num -= 1
                    except IndexError:
                        print('empty')
                        num -= 1
                else:
                    print(len(res))
                    num -= 1
    except ValueError:
        print('명령문을 잘못입력했습니다')




################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)

