import psutil
import time
import os,operator
###################################################################################################
## 1. 문제        : 말과 졸 (중급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 36864 byte
## 4. 만든 사람   : 이융성
###################################################################################################

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

while 1:
    try:
        board = [int(x) for x in input('장기판!').split()]
        hor_row,hor_col,sol_row,sol_col = [int(x) for x in input('말과 쫄').split()]
        if board[0] <= 0 or board[1] <= 0 or hor_row <= 0 or hor_col <= 0 or sol_row <= 0 or sol_col <= 1 or \
                        board[0] < hor_row or board[0] < sol_row or board[1] < hor_col or board[1] < sol_col:
            raise ValueError
        break
    except ValueError:
        print('다시입력하세용')
        continue


# 시작 시간 체크
stime = time.time()

route=[[0,3,2,3,2],
       [3,2,1,2,3],
       [2,1,4,3,2],
       [3,2,3,2,3],
       [2,3,2,3,4]]

row_dist = abs(sol_row-hor_row)
col_dist = abs(sol_col-hor_col)

if row_dist > 4:
    for i in range(row_dist-4):
        route.append([route[len(route) - 2][1] + 1, route[len(route) - 2][0] + 1, route[len(route) - 2][1] + 1, route[len(route) - 2][0] + 1, route[len(route) - 2][1] + 1])

if col_dist > 3:
    for j in range(col_dist-4):
        route[0].append(route[1][len(route[1])-2]+1)
        route[1].append(route[0][len(route[1])-2]+1)
        for k in range(len(route)):
            if k<=1:
                continue
            else:
                compare_tmp=[]
                compare_tmp.append(route[k-2][len(route[k-2])-2])
                compare_tmp.append(route[k-1][len(route[k-1])-3])
                route[k].append(min(compare_tmp)+1)

print(route[row_dist][col_dist])


# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)




