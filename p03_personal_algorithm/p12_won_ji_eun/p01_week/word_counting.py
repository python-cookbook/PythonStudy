import os
import psutil
import time

###################################################################################################
## 1. 문제        : 1516 : 단어 세기(초급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 16384 byte
## 4. 만든 사람   : 원지은
###################################################################################################


#시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

# 시작 시간 체크
stime = time.time()

script='안녕하세요! 안녕하세요! 안녕하세요! 좋은 아침이네요! 네 좋은 아침입니다.'
divided_script=script.split(' ') #script를 단어로 나누기
dic={}
cnt=0 # cnt 초기화
for num in range(len(divided_script)): # 0,1,2,3,4,5,6,7
    cnt =divided_script.count(divided_script[num]) # 각 요소들의 개수를 센다
    dic[divided_script[num]]='{0}'.format(cnt) # c 딕셔너리에 ‘단어 = 개수’로 ‘key = value’ 값을 담는다
for key in dic:
    print(key,':',dic[key]) # dic에서 key를 가져오고, dic[key]로 value 값을 출력

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)