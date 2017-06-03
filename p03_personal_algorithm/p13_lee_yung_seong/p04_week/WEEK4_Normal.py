import psutil
import time
import os,operator
###################################################################################################
## 1. 문제        : 못생긴 수 (중급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 53248byte
## 4. 만든 사람   : 이융성
###################################################################################################

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]


def algo(num):
    a=[]
    for i in range(1,num+5):
        if i<=5:
            a.append(i)
        elif i>5:
            if i%2==0 or i%3==0 or i%5==0:
                a.append(i)
        else:
            continue
    return a[num-1]

# 시작 시간 체크
while True:
    num = int(input('Input the Number'))
    stime = time.time()# 시작 시간 체크
    print(algo(num))
# 종료 시간 체크
    etime = time.time()
    print('consumption time : ', round(etime-stime, 6))
    if num==0:
        break

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)