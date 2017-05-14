import os
import time
import psutil

###################################################################################################
## 1. 문제        : 단어세기 (초급)
## 2. 소요 시간   : 7.797911 초 (입력시간 포함)
## 3. 사용 메모리 : 49152 byte
## 4. 만든 사람   : 임미선
###################################################################################################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]


# ################ 시작 메모리 체크 #################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 #################
stime = time.time()


def addword():
    sentence = ' '
    word = []
    while True:
        sentence = input('문장을 입력하세요')  #두번째 문장 입력
        if sentence == 'END':
            break
        wordlist = sentence.split()          #입력한 문장을 공백 기준 단어별 쪼개기              # 두번째 문장 단어별 쪼개기
        if len(sentence) <= 50 and len(wordlist) <= 10:
            for i in wordlist:             #단어 순서별로 i로 들어감
                if i not in word:       #입력한 문장의 단어가 word에 없으면               #중복되더라도 순서대로 한번씩만 들어감
                    word.append(i)      #word에 붙여짐 ( 처음 문장 입력시 word에는 처음 입력한 문장이 들어감)
            print(' '.join(word))

addword()



################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)


