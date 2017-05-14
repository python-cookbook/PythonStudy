import os
import time
from copy import deepcopy
import psutil
from collections import Counter

##################################################################################################
## 1. 문제        : 단어세기 (초급)
## 2. 소요 시간   : 13.163716 초 (소수점 6자리 반올림)
## 3. 사용 메모리 :  57344 byte
## 4. 만든 사람   : 류지은
##################################################################################################

################ 시작 메모리 체크 #################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 #################
stime = time.time()


while 1:
    text = input('문장 입력 ')
    if len(text) >= 200:
        print('문자열이 너무 깁니다')
        break

    tlist=text.split(' ')
    if 'END' in tlist:
        break
    word_counts=Counter(tlist)
    wlist=(word_counts)

    for word,cnt in sorted(wlist.items(), key=lambda x:x[0].upper()):
        print(str(word)+str(':')+str(cnt))


################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
