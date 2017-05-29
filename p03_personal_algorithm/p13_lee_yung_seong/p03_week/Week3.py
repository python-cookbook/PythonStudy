import psutil
import time
import os,operator
###################################################################################################
## 1. 문제        : 보석 도둑 (중급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 84000 byte
## 4. 만든 사람   : 이융성
###################################################################################################

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

jewel_wei_val = []
jewel_avgval = []
jewel_idx_maxval = []
total_value = 0 #가장 높은 가치를 가지고 있는 보석의 배열 위치



input_data=input('보석의 가지 수 / 배낭의 용량')
jewel_num, bag_vol= map(int,input_data.split(' '))


for i in range(int(jewel_num)):
    temp=input(str(i+1)+'번째 보석의 무게와 값어치')
    temp=temp.split(' ')
    temp.append(int(temp[1])/int(temp[0]))
    jewel_wei_val.append(temp)







# 시작 시간 체크
stime = time.time()

jewel_wei_val.sort(reverse=True,key=operator.itemgetter(2))

for i in range(len(jewel_wei_val)):
    total_value += ( int(bag_vol)//int(jewel_wei_val[i][0]) ) * int(jewel_wei_val[i][1])
    bag_vol -= (int(bag_vol)//int(jewel_wei_val[i][0])) * int(jewel_wei_val[i][0] )
    if bag_vol == 0:
        break
print('총 값어치 : ',total_value)

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)