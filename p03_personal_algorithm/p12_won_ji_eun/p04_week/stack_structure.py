import os
import time
import psutil
import random

###################################################################################################
## 1. 문제        : 스택 (초급)
## 2. 소요 시간   : 0.009 초 (소수점 6자리 반올림)
## 3. 사용 메모리 :  8192 byte
## 4. 만든 사람   : 원지은
###################################################################################################


################# 시작 메모리 체크 #########################################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 ##################
stime = time.time()
#################################################



######### 명령어 리스트 만들기 #########

command_cnt=random.choice(range(1,101))         # 명령어 개수 정하기 (명령의 수는 1~100)
i_cnt=random.choice(range(command_cnt))         # i 명령어 개수
o_cnt=random.choice(range(command_cnt-i_cnt))   # o 명령어 개수
c_cnt=command_cnt-i_cnt-o_cnt                   # c 명령어 개수
#print(command_cnt)
#print(i_cnt)
#print(o_cnt)    
#print(c_cnt)

i=['i '+ str(i) for i in (random.sample(range(1,10001),i_cnt))]   # i 명령어 리스트 (숫자는 10000이하의 자연수)
o=['o' for i in range(o_cnt)]                                     # o 명령어 리스트
c=['c' for i in range(c_cnt)]                                     # c 명령어 리스트

command_append=[]  # i, o, c 명령어 합치기 준비  
for a in i, o, c:  # 일단 넣고   
    command_append.append(a)  
#print(command_append)   


######## 명령어 개수와 명령어 출력 #########
print(command_cnt)  # 명령어 개수 출력
command= [b for a in command_append for b in a]   # 넣은거 풀어서 출력하기   

for N in command:   # 수행할 명령어들 출력
    print(N)


###### 입력된 명령어 수행하기 ########
Stack=[]  # 명령어가 수행될 list 초기화

for i in command:                 # 만약 명령어가 i라면
    if i[0] == 'i': 
        Stack.append(i[2:])       # i의 숫자를 출력하기
        
    elif i[0] == 'o':             # 만약 명령어가 o라면
        try : 
            print(Stack.pop())    # 가장 나중에 입력된 숫자부터 반환하고 리스트에서 삭제하기
            
        except IndexError:        # 만약 더이상 append 된 숫자가 없다면
            print("empty")        # empty라고 출력하기
            
    elif i[0] == 'c':             # 만약 명령어가 c라면
        print(len(Stack))         # 남은 명령어들의 개수를 출력하기


################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
