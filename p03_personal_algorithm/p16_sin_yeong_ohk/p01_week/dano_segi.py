###################################################################################################
## 1. 문제        : 단어 세기 (초급)
## 2. 소요 시간   : 12.955523초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 53248
## 4. 만든 사람   : 신영옥
###################################################################################################

import psutil,time,os
# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())

mem1 = proc1.memory_info()

before_start = mem1[0]

stime = time.time() # 시작시간 체크

while True:    #무한루프 돌리기
    str_ = input('입력# ')     #문장 입력받구
    str1= list(set(str_.split(' ')))    #입력받은 문장을 공백기준으로 잘라내기+set으로 중복제거
    str2 = str_.split(' ')    #입력받은 문장을 중복제거하지 않고 잘라내기
    str1.sort()    #중복제거된 리스트를 알파벳순서로 정렬
    if str_=='END':    #입력받은 문장이 END라면 loop 나가기
        break
    else:   #END 아니면
        for i in str1:    #중복제거된 리스트 loop돌리기
            sum = 0    #sum 변수를 숫자로 받기
            for j in str2:    #중복제거X 문장을 돌려서
                if i == j:    #같으면
                    sum+=1    #sum에서 1씩 더해서 개수 세기
            print(i,':',sum)    #출력


etime = time.time() # 종료시간 체크
print('consumption time : ', round(etime-stime, 6))


proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use :', after_start-before_start)