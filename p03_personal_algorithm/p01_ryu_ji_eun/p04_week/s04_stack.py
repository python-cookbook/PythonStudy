import os
import time
import psutil

##################################################
## 1. 문제        : 스택 (초급)
## 2. 소요 시간   : 17.76 초 (소수점 6자리 반올림)
## 3. 사용 메모리 :  24576 byte
## 4. 만든 사람   : 류지은
##################################################

################# 시작 메모리 체크 #################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 ###################
stime = time.time()
#################################################

def stacks():
    stacklist = []
    cnt = 0
    while cnt < 100:
        base = input("입력: ").split(' ')
        if base[0] == "i":
            if int(base[1]) < 10000 and int(base[1]) > 0:
                stacklist.append(int(base[1]))
                cnt += 1
            else:
                print("10000 이하 자연수를 입력해주세요")


        elif base[0] == "o":
            if len(stacklist) > 0:
                print(stacklist.pop())
                cnt += 1
            elif len(stacklist) == 0:
                print("Empty")
                cnt += 1


        elif base[0] == "c":
            list_lens=len(stacklist)
            print(list_lens)
            cnt += 1

        else:
            print("입력은 i로 시작, 값보기는 o, 개수는 c를 적어주세요.")
            continue


    if cnt == 100:
        print("입력 횟수가 100번이 되어 입력을 종료합니다.")
        return


stacks()


################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
