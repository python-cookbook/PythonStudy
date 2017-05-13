###################################################################################################
## 1. 문제        : 메시지 (중급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 20480 byte
## 4. 만든 사람   : 이융성
###################################################################################################
import psutil
import time
import os
# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]


def decode(length,code):
    alphabet=[
     ['0','0','0','0','0','0','A']
    ,['0','0','1','1','1','1','B']
    ,['0','1','0','0','1','1','C']
    ,['0','1','1','1','0','0','D']
    ,['1','0','0','1','1','0','E']
    ,['1','0','1','0','0','1','F']
    ,['1','1','0','1','0','1','G']
    ,['1','1','1','0','1','0','H']]
    target='{0}'.format(code)
    arr=[]
    word=''
    matchcnt=0
    for i in range(len(target)):
        arr.append(target[i:i+1])

    for k in range(1,length+1):
        arr2=arr[6*(k-1):6*k]
        word2=word
        for i in range(8):
            for j in range(6):
                if alphabet[i][j]==arr2[j]:
                    matchcnt+=1
            if matchcnt>=5:
                matchcnt = 0
                word+=alphabet[i][6]
                break
            else:
                matchcnt=0
        if word2==word:
            return k
            break

    return word


# 시작 시간 체크
stime = time.time()

print(decode(5,'011111000000111111000000111111'))

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)