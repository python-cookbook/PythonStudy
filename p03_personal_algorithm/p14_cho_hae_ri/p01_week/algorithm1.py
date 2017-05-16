###################################################################################################

## 1. 문제 : 단어 세기

## 2. 소요 시간 : 4.956705 초 (소수점 6자리 반올림)

## 3. 사용 메모리 : 36864

## 4. 만든 사람 : 조해리

###################################################################################################

import os
import psutil
import time

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())

mem1 = proc1.memory_info()

before_start = mem1[0]


stime = time.time() # 시작시간 체크

while True:
    words = input('문장을 입력하시오')

    if len(words) <= 200 and words != 'end':
        words = words.split(' ')

        word_list = list(set(words))
        word_list.sort(reverse=False)

        for i in range(len(word_list)):
            cnt = 0
            cnt += words.count(word_list[i])

            print(word_list[i], ':', cnt)

    elif words =='end':
        break

etime = time.time() # 종료시간 체크
print('consumption time : ', round(etime-stime, 6))


proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use :', after_start-before_start)

