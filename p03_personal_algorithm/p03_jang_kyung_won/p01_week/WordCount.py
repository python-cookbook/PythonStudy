import os
import psutil
import time

###################################################################################################
## 1. 문제        : 단어 세기
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 4096
## 4. 만든 사람    : 장경원
###################################################################################################
# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

def word_cnt():
    word_script = ''     # 입력받은 단어를 담을 변수
    while word_script != 'end':        # end를 입력하지 않으면 계속 진행
        word_list=[]                   # 입력된 단어 중 중복을 제거하고 남은 단어를 담을 변수
        word_script = str(input('단어를 입력하세요!'))
        if word_script != 'end':        # end가 입력되면 진행하지말고 종료
            # 시작 시간 체크
            stime = time.time()
            if len(word_script) < 200:  # 단어 길이가 200 이하로 입력이 되면 실행
                word = word_script.split()      # 입력받은 word_script를 split함수로 구분
                word_list = list(set(word))     # list(set())함수로 담겨진 단어들 중 중복 제거
                word_list.sort()               # sort()함수로 정렬
                for i in word_list:
                    word_cnt = 0
                    word_cnt += word.count(i) # 중복 제거한 word_list에서 word에 몇개가 들어가있는지 count
                    print(i,':',word_cnt)
                # 종료 시간 체크
                etime = time.time()
                print('consumption time : ', round(etime-stime, 6))
print(word_cnt())

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)