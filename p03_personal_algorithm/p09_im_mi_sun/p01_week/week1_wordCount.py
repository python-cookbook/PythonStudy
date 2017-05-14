import os
import time
import psutil

###################################################################################################
## 1. 문제        : 단어세기 (초급)
## 2. 소요 시간   : 7.599207 초 (입력시간 포함)
## 3. 사용 메모리 : 49152 byte
## 4. 만든 사람   : 임미선
###################################################################################################

# ################ 시작 메모리 체크 #################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 #################
stime = time.time()




def wordcount():
    sentence = ''
    wordlist = []
    while len(sentence) <= 200:
        sentence = input('문장을 입력하세요')
        if sentence != 'END':
            for i in sentence.split():
                wordlist.append(i)
            print(len(set(wordlist)))
        else :
            break

wordcount()



################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
