import psutil
import os
import time

###################################################################################################
## 1. 문제        : 오류고정 (고급)
## 2. 소요 시간   : 0.015633 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 69632 byte
## 4. 만든 사람   : 이용은
###################################################################################################

# 기본 파일 생성 코드
# with open('D:\data\\algorithm_input\highQ1_100.txt','w') as file:
#     file.write('100\n')
#     for i in range(100):
#         line = ''
#         for j in range(100):
#             line += str((i+j)%2) + ' '
#         file.write(line.rstrip() + '\n')
#

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

file = open('D:\data\\algorithm_input\highQ1_100.txt','r')
matrix_size = int(file.readline())
input = []
for i in range (matrix_size):
    input.append([int(x) for x in file.readline().split(' ')])

# 시작 시간 체크
stime = time.time()

rowparity = 0 #nonParity cnt
colparity = 0 #nonParity cnt
rowpoint = -1 #Change bit rowaddr
colpoint = -1 #Change bit coladdr
result = 0 #0 : OK, 1 : Change bit, 2 : Corrupt

# 패리티 위반 행과 열이 1개씩 나왔을 시 해당 위치를 Change bit point로 저장
# 행이나 열이 2개 이상 나올 시 result를 Corrupt로 하여 break
for i in range(matrix_size):
    temprow = 0 #체크할 row에서의 1의 갯수
    tempcol = 0 #체크할 col에서의 1의 갯수
    for j in range(matrix_size):
        if input[i][j] == 1:
            temprow += 1
        if input[j][i] == 1:
            tempcol += 1
    if temprow%2 == 1:
        if rowparity == 1:
            result = 2
            break
        else:
            rowparity += 1
            rowpoint = i
    if tempcol%2 == 1:
        if colparity == 1:
            result = 2
            break
        else:
            colparity += 1
            colpoint = i

#col/row중 한쪽에만 홀수줄이 존재할 경우 or col이나 row에 2개 이상의 홀수줄이 존재할 경우 : Corrupt
if result == 2 or colparity+rowparity == 1:
    print('Corrupt')
#col/row에 하나씩의 홀수줄이 존재할 경우 : Change bit
elif colparity == 1 and rowparity == 1:
    print('Change bit ({0},{1})'.format(rowpoint + 1, colpoint + 1))
#그 외(홀수줄이 하나도 없는 경우) : OK
else:
    print('OK')


# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)