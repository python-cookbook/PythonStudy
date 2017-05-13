import psutil
import time
import os
###################################################################################################
## 1. 문제        : 피보나치 수열 (중급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 20480 byte
## 4. 만든 사람   : 이융성
###################################################################################################

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]



def pibo(n, num):
    gap = 1000
    pib_seq = [1, 1]
    for i in range(n - 3):
        pib_seq.append(pib_seq[i] + pib_seq[i + 1])
    a = pib_seq[len(pib_seq) - 2]
    b = pib_seq[len(pib_seq) - 1]
    x_max = (num - b) // a + 1
    y_max = (num - a) // b + 1
    for x in range(x_max):
        for y in range(y_max):
            if a * x + b * y == num:
                if x < y:
                    if gap > y - x:
                        gap = y - x
                        x_a = x
                        y_a = y
    return x_a, y_a


# 시작 시간 체크
stime = time.time()
print(pibo(7,218))

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)