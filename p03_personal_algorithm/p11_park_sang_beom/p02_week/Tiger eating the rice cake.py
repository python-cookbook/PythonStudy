import os
import psutil
import time

###################################################################################################
## 1. 문제        : 떡 먹는 호랑이
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 28672 byte
## 4. 만든 사람    : 박상범
###################################################################################################

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

'''
피보나치 수열 식
f(n) = af(n-2) + bf(n-1) (단, n>=3)
f(3) = f(1) + f(2)
f(4) = f(1) + 2f(2)
f(5) = 2f(1) + 3f(2)
f(6) = 3f(1) + 5f(2)
f(7) = 5f(1) + 8f(2)
 :           :
 :           :
'''

# a 의 계수를 구하기 위한 함수 생성
def fi_a(num):
    res = [1,1]
    for i in range(2, num-2):
        res.append(res[i-1]+res[i-2])
    return res

# b 의 계수를 구하기 위한 함수 생성
def fi_b(num):
    res = [1,2]
    for i in range(2, num-2):
        res.append(res[i-1]+res[i-2])
    return res

last = int(input('할머니가 넘어온 날 입력 : '))
value = int(input('그날 호랑이에게 준 떡의 개수 입력 : '))

# 시작 시간 체크
stime = time.time()

a = fi_a(last)[-1]  # a의 계수
b = fi_b(last)[-1]  # b의 계수

p = []              # af(1)의 모든 수를 담을 변수
q = []              # bf(2)의 모든 수를 담을 변수
res_f1 = ''         # 첫째날 준 떡의 개수를 위한 변수
res_f2 = ''         # 둘째날 준 떡의 개수를 위한 변수

for i in range(1,value):
    if a*i <= value:
        p.append(a*i)
# print(p)
for i in range(1,value):
    if b*i <= value:
        q.append(b*i)
# print(q)
for f1 in range(len(p)):
    for f2 in range(len(q)):
        if p[f1]+q[f2] == value and f1 < f2:
            # print(p[f1] + q[f2], f1 + 1, f2 + 1)
            res_f1 = f1+1
            res_f2 = f2+1

print('첫째날 준 떡의 개수 : ', res_f1, '개')
print('둘째날 준 떡의 개수 : ', res_f2, '개')

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
