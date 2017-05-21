import os
import psutil
import time

###################################################################################################
## 1. 문제        : 달팽이 사각형
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 262144
## 4. 만든 사람    : 장경원
###################################################################################################

import numpy as np
n= int(input('숫자를 입력하세요'))
a = np.zeros((n, n))                     # 입력하는 숫자만큼의 행렬을 만들어주는 함수 np.zeros()
#리스트로 출력
# a= [[0 for number in range(1, n+1)] for number in range(n)]   # n*n 리스트를 생성해준다.
# for i in range(n):                                           # 리스트별로 하나씩 출력
#     print(a[i])
# 행렬 말고 리스트로도 출력 할수 있따.
# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]
# 시작 시간 체크
stime = time.time()
cnt = 1                         # cnt는 입력하는 숫자이다. 루프문 통과할때마다 +1씩 된다.
re= 0                           #초기화 값을 설정해준다.
k = n                          # 루프문의 횟수를 정하기 위해 입력 받은 수를 넣어준다.
while cnt <= (n*n):
    hang = re
    yeol = re
    while yeol < k:
        a[hang][yeol] = cnt     # 첫쨋줄 n만큼 넣어줌
        yeol += 1               # 열만 한칸씩 전진해서 입력
        cnt+= 1                 # 입력숫자가 1씩 증가하도록
    yeol = re                # 열을 다시 초기화
    while hang + 1 < k:
        a[hang + 1][k-1] = cnt  # 마지막줄에 n다음숫자로 채워줌
        hang += 1               # 행만 증가하도록
        cnt+= 1                 # cnt는 계속 증가
    hang = re                # 행을 다시 초기화
    while yeol < k - 1:         # 채운열은 제외 해야 하므로 n에 -1을 해준다
        a[k-1][n-2-yeol] = cnt  # 맨 밑에 행을 맨 마지막 열을 빼고 역순으로 입력
        yeol += 1               # 열 위치가 줄어든다 n-2-yeol에 의해
        cnt+= 1                 # 입력 숫자는 계쏙 증가
    yeol = re                # 열 다시 초기화
    while hang < k - 2:
        a[n-2-hang][yeol] =cnt   # 그리고 맨 오른쪽 칸을 행 숫자가 줄어들면서 채워준다
        hang += 1               # n-2-hang에 의해 행이 줄어든다 열은 그대로
        cnt+= 1                 # 입력숫자는 계속 증가
    re += 1                   # 반복을 위해 1을 더해준다
    k -= 1                 # 반복을 위해 1을 빼준다.

print(a)

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))



# 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)

