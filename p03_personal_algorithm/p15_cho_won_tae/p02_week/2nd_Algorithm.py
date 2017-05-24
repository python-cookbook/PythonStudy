import os
import psutil
import time

###################################################################################################
## 1. 문제        : 떡 먹는 호랑이
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 24576 byte
## 4. 만든 사람    : 조원태
###################################################################################################

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

# 피보나치 일반항
def Fibo(su):
    result = [1, 1]
    for i in range(su-2):
        result.append(result[i] + result[i+1])
    return result[su-3:su-1]

# 첫번째 자리와 두번째 자리 구하는 함수
def First_Second(su,res_su):
    re_x=0
    re_y=0
    a = Fibo(su)[0]  # 3
    b = Fibo(su)[1]  # 5
    for x in range(res_su//a+1):
        for y in range(res_su//b+1):
            if (x * a) + (y * b) == res_su:
                if x<y:
                    re_x = x
                    re_y = y
    print(re_x)
    print(re_y)

# 시작 시간 체크
stime = time.time()

###############변수설정#################
Question = input("넘어온 날? 떡의 개수?")
Answer = Question.split() # ['6','41']
su = int(Answer[0])
res_su= int(Answer[1])

#########출력##########
First_Second(su,res_su)

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)

