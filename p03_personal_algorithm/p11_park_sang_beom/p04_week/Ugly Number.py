import os
import psutil
import time

###################################################################################################
## 1. 문제        : 못 생긴 수
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 40960 byte
## 4. 만든 사람    : 박상범
###################################################################################################

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

# 시작 시간 체크
stime = time.time()

def ugly(n):
    result = [1]
    while True:
        last = result[-1]

        if len(result) == n:
            return result

        temp = []

        for r in result:
            for t in r*2, r*3, r*5:
                if t > last:
                    temp.append(t)

        result.append(min(temp))

def ugly_number():
    while True:
        question = int(input('n 번째 못생긴 수 입력 : ')) - 1
        if question != -1:
            print(ugly(question+1)[question])
        else:
            return

if __name__ == '__main__':
    ugly_number()

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)


