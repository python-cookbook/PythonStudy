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

def word_plus():
    word_script ='' # 입력 받은 문장을 담을 변수
    word =''        # 입력 받은 문장을 split하여 담을 변수
    distinct_word=[]  # 중복을 제거 하고 난 뒤에 담을 변수
    while word_script != 'end':
        word_script = str(input('단어를 입력하세요!'))
        if word_script != 'end':        # end가 입력되지 않으면 계속 input해라
            # 시작 시간 체크
            stime = time.time()
            if len(word_script) < 50:   #입력한 word_script의 길이가 50 이하일때만 실행
                word = word_script.split()
                if len(word) < 10:          # word_script의 문장을 split했을때 10단어 이하만 실행
                    for i in word:
                        if i not in distinct_word:   # 미리 만들어놓은 distinct_word에 없다면
                            distinct_word.append(i)  # distinci_word에 append 해라
                    print(' '.join(distinct_word))  # join함수를 이용해서 ' '을 기준으로 리스트를 출력
                    # 종료 시간 체크
                    etime = time.time()
                    print('consumption time : ', round(etime-stime, 6))
print(word_plus())


# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)