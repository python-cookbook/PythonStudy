import os
import psutil
import time

###################################################################################################
## 1. 문제        : 마방진
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 16384
## 4. 만든 사람    : 장경원
###################################################################################################


n=int(input("마방진을 위한 정방행렬의 행을 입력하시오:(홀수만)"))   #홀수 정방행렬만 가능

List= [[0 for number in range(1, n+1)] for number in range(n)]   # n*n 리스트를 생성해준다.
# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]
# 시작 시간 체크
stime = time.time()

#시작을 위한 위치 설정
hang=0
yeol=int(n/2)
#시작위치에 1을 넣고 시작
List[hang][yeol]=1

x=0                          #초기화 값
y=0

#마방진 생성 루프
num = List[hang][yeol]

while num < n*n :
    x= hang               # 진행중 hang 값을 넣어줌
    y= yeol               # 진행중 yeol 값을 넣어줌
    num += 1              # 숫자가 1씩 증가하도록
    hang-=1
    yeol-=1

    if hang < 0:             # 행이 0보다 크면 마방진 규칙에 따라
        hang=n-1            # 맨 밑의 행으로 보내준다.

    if yeol > n-1:           # 열이 n-1보다 크면 마방진 규칙에 따라
        yeol = 0             # 열을 맨 앞으로 보내준다.

    if yeol < 0:
        yeol = n-1

    if List[hang][yeol] == 0:       # 값이 0 이라면
        List[hang][yeol] = num        # 그 행에 i를 입력한다.

    else:                        # 값이 0이 아니라면 마방진 규칙에 따라
        hang=x+1                 # 처음 행값이 입력 된 것에서 +1을 해준다.
        yeol=y
        List[hang][yeol] = num
# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime - stime, 6))

for i in range(n):                                           # 리스트별로 하나씩 출력
    print(List[i])
# 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)