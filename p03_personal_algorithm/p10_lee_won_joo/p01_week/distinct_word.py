import os
import psutil
import time
import operator

###################################################################################################
## 1. 문제        : 단어 중복 제거
## 2. 소요 시간    : 0.0 초
## 3. 사용 메모리  : 16384
## 4. 만든 사람    : 이원주
###################################################################################################
# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

def str_add():
    word_list = []
    while True:  #무한 반복
        input_str = input('입력하세요.') # string 입력
        if input_str == 'end':
            print('Program off')
            break
        elif len(input_str) > 50 or input_str == '':   # 바이트 제한 50
            continue
        else:
            start_time = time.time()
            for i in input_str.split(' '):  # ['I' 'am' 'a' 'boy']
                if i in word_list:   #안에 이 값이 존재한다면 그냥 지나가.
                    continue
                else:               #그게아니라면 맨 뒤에다가 추가해
                    word_list.append(i)
            end_time = time.time()
            print(end_time-start_time,'초')
        print(word_list)
str_add()
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
