###################################################################################################
## 1. 문제        : 제곱수 합의 최소 갯수 구ㅏㅎ기
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 0
## 4. 만든 사람    : 이원주
###################################################################################################
import os
import psutil
import time


# 시작 메모리 체크

import math

print(pow(18,2))
def num_chk():
    proc1 = psutil.Process(os.getpid())
    mem1 = proc1.memory_info()
    before_start = mem1[0]  # 시작전 메모리 측정
    start_time = time.time()
    '''
    시간,메모리체크
    '''

    sqrt_list =list()
    temp = 0
    num = int(input('숫자를 입력하세요'))  #8
    for i in range(num,0,-1):
        if math.pow(i,2) <= num:
            num = num - math.pow(i,2)
            sqrt_list.append(i)
        elif num == 0:
            break

    '''
    시간 , 메모리 체크
    '''
    after_start = mem1[0]
    end_time = time.time()
    print(end_time - start_time, '초')
    print(after_start)
    print('memory use : ', after_start - before_start)
    return len(sqrt_list)
print(num_chk())
