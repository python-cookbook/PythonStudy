import os
#import psutil
import time

###################################################################################################
## 1. 문제        : 1516단어세기
## 2. 소요 시간   : 6.425757  #다시 확인 요망
## 3. 사용 메모리 : 모듈설치후 확인
## 4. 만든 사람   : 김명학
###################################################################################################
'''
# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]
'''
# 시작 시간 체크
stime = time.time()

while 1:
    in_word = input()
    if in_word == "end" or len(in_word) >= 200:
        break
    else:
        match_word = in_word.split(' ')
        match_word.sort()
        print(match_word)
        count = 1
        for i in match_word:
            if match_word.count(i) == count:
                print(i,':',match_word.count(i))
                count = 1
            else:
                count+= 1

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))
'''
# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
'''