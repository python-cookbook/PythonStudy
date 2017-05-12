import os
import psutil
import time

###################################################################################################
## 1. 문제        : 단어 집합(초급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 53248 byte
## 4. 만든 사람   : 원지은
###################################################################################################


#시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

# 시작 시간 체크
stime = time.time()


word = []  # 빈 단어장
cnt = 0  # 추가한 횟수값 담기
while cnt < 10:  # 단어는 최대 10개까지 계속 추가하기
    new = input('추가할 단어를 입력하세요~ ')  # 추가할 단어 입력

    if len(new) >= 50:  # 50자 이상은 입력안됨.
        new = input('추가할 단어를 입력하세요~ ')

    if new not in word:  # 기존 단어장에 추가할 단어가 없다면
        word.append(new)  # 단어장에 추가하기

    for word_divided in word:  # 출력은 세로로!
        print(word_divided)

    if new == 'END':  # END를 입력하면 끝
        break

    cnt += 1  # 추가한 횟수 증가

    # 종료 시간 체크
    etime = time.time()
    print('consumption time : ', round(etime - stime, 6))

    # 실행 후 맨 밑에서 코드 구동 후 메모리 체크
    proc = psutil.Process(os.getpid())
    mem = proc.memory_info()
    after_start = mem[0]
    print('memory use : ', after_start - before_start)