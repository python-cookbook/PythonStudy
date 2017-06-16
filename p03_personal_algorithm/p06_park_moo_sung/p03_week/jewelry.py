import os
import time
import psutil

###################################################################################################
## 1. 문제        : 배낭 채우기1 (중급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 :  24576 byte
## 4. 만든 사람   : 박무성
###################################################################################################

jewelrycnt,maxweight= input('보석 종류의 개수와 최대 무게 입력 ').split()

#############################################################################################
################# 시작 메모리 체크 #################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 #################
stime = time.time()
#############################################################################################

def jewelry(jewelrycnt):
    jewelrydic = {}
    for idx in range(jewelrycnt):
        weight, value=input('{}번째 보석의 무게와 가치를 입력 '.format(idx+1)).split()

        if weight not in jewelrydic:
            jewelrydic[int(weight)] = int(value)
        elif int(value) >= jewelrydic[int(weight)] :
            jewelrydic[int(weight)] = int(value)
    print(sorted(jewelrydic.items(), key=lambda kv : (kv[1]/kv[0], -kv[0]), reverse=True))
    return sorted(jewelrydic.items(), key=lambda kv : (kv[1]/kv[0], -kv[0]), reverse=True)

def greedy(maxweight):
    jewelrylist = jewelry(int(jewelrycnt))

    jewelryvalue = 0
    maxweight = int(maxweight)

    for eachjewelry in jewelrylist:
        jewelryvalue += (maxweight // eachjewelry[0])*eachjewelry[1]
        maxweight -= (maxweight // eachjewelry[0]) * eachjewelry[0]
    return jewelryvalue

if __name__ == '__main__':
    print(greedy(maxweight))

################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)

