import os
import psutil
import time
import operator

###################################################################################################
## 1. 문제        : 달핑애 수열
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 0
## 4. 만든 사람    : 이원주
###################################################################################################
# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]   #시작전 메모리 측정


how = int(input("몇번 배열 돌릴까요"))
array = [[0 for i in range(how)] for j in range(how)]      # N x N 0행렬 생성
N = 1
X,Y = 0, 0
V = 1,0      #행렬 회전시킬때 쓸 튜플값
start_time = time.time()
array[Y][X] = N   #array[0][0] = 1
array_list = list()
word_list = list()
while True:

    X,Y = X+V[0], Y+V[1]  # (0+1, 0+0), 즉 순환마다 1행 증가
    if X < 0 or X > how-1 or Y < 0 or Y > how-1 or array[Y][X] != 0:
        X,Y = X-V[0], Y-V[1]
        # print('X =',X,'Y=',Y)
        V = -V[1], V[0]
        # print(V)
        X,Y = X+V[0], Y+V[1]
        # print('빼고난 후','X =', X, 'Y=', Y)
    N += 1
    array[Y][X] = N

    if N == pow(how,2):
        after_start = mem1[0]
        break


for Y in range(how):
    temp = [] #초기화
    for X in range(how):
        d = array[Y][X]
        temp.append(d)
    word_list.append(temp)  #for문 끝날때 추가
end_time = time.time()
print(word_list)

print(end_time-start_time,'초')
print('memory use : ', after_start-before_start)

# word_list = [[Y for Y in range(how)] for X in range(how)]
# print(word_list)
# for Y in range(how):
#     temp = list()
#     for X in range(how):
#         temp.append(array[Y][X])
#         word_list.append(temp)
#     # print(temp)
# print(word_list)
# end_time = time.time()
#
# print(end_time-start_time,'초')
