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
    sentence = ''   #입력한 문장 변수
    wordlist = []   #입력한 문장에서 공백 기준 쪼갠 단어를 담을 리스트 변수
    while len(sentence) <= 200:             #문장의 길이가 200이하일 경우에만 실행
        sentence = input('문장을 입력하세요')
        if sentence != 'END':
            for i in sentence.split():      #공백기준 쪼갠 단어를 순서대로 for문 실행
                wordlist.append(i)          # 리스트 변수에 단어를 담음
            print(len(set(wordlist)))       #단어의 개수 출력
        else :                              #END를 입력했을 경우 함수 종료
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
