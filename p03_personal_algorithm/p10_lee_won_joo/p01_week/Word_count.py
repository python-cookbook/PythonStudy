import os
import psutil
import time
import operator

###################################################################################################
## 1. 문제        : 단어 세기
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 28862
## 4. 만든 사람    : 이원주
###################################################################################################
# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]


list = 'I AM DOG DOG DOG DOG A AM I I AM OLYMPIAD JUNGOL JUNGOL OLYMPIAD '  #나중에는 input식으로
def count_word():
    while True:
        d = dict()
        list = input('문장을 입력하세요.')
        if list == 'end':            # input값으로 end를 작성한다면?

            print('Off the ProGram') # 프로그램 종료 실행하라.
            break
        elif list == '':
            continue
        elif len(list) > 200:       #200자 넘으면 다시묻게
            continue
        else:                        # 그렇지 않다면
            start_time = time.time()
            for i in list.split(' '): # 입력된 문장들의 단어를 쪼개어라.
                if i not in d:  # 첫번째 단어가 dict안에 없다면?
                    d[i] = 1    # 단어 와 1을 key- value로 셋팅하라.
                else: d[i] += 1   # 같은 단어가 한번 더 나오면 +1하라.
            # sorted_d = sorted(d.items(), key=operator.itemgetter(0))  # dict의 key를 기준으로 오퍼레이터를 이용해서, sorting한다.
            sort = sorted(zip(d.values(),d.keys()))
            end_time=time.time()

        print(sort)         #sorting된 결과를 리턴하라.
        print(end_time - start_time, '초')

count_word()
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
