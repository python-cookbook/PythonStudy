import os
import time
import psutil

##################################################
## 1. 문제        : 못생긴 수 (중급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 :  40960 byte
## 4. 만든 사람   : 박무성
##################################################

################# 시작 메모리 체크 #################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 ###################
stime = time.time()
#################################################

def Nanugi(num):
    while num//2 == num/2:
        num /= 2
    while num//3 == num/3:
        num /= 3
    while num//5 == num/5 :
        num /= 5
    return num

def Uglynum():
    while True:
        cnt = int(input("숫자 입력(0 입력 시 exit) "))
        if cnt == 0:
            return
        uglylist = []
        num = 1
        while len(uglylist) <= cnt:
            if Nanugi(num) == 1 :
                uglylist.append(num)
            num+=1
        print(uglylist[cnt-1])

if __name__ == '__main__':
    Uglynum()

################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
