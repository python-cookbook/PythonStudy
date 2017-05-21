import os 
import time 
import psutil 
import math

 
################################################################################################### 
## 1. 문제        : 마방진 (초급) 
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림) 
## 3. 사용 메모리 :  20480 byte 
## 4. 만든 사람   : 원지은
################################################################################################### 

n=int(input("정사각형의 크기를 입력하세요~ (2 이상의 홀수만 가능!)"))

################# 시작 메모리 체크 ################# 
proc1 = psutil.Process(os.getpid()) 
mem1 = proc1.memory_info() 
before_start = mem1[0] 

 
################ 시작 시간 체크 ################# 
stime = time.time() 

numlist=[] #네모판에 입력할 숫자를 담음
for i in range(1,n*n+1):
    numlist.append(i) # numlist=[1,2,3,4,5,6,7,8,9]
    
matrix={} 
(row, column)=(1,math.trunc(n/2)+1)     #숫자가 입력될 행과 열에 1의 자리(첫행의 가운데)로 초기화해준다.
                                        #round를 안쓰고 trunc()+1을 한 이유는 round에 버그가 있기 때문
for num in range(len(numlist)):
    matrix[numlist[num]]=(row, column)      #key를 숫자로, value는 입력될 위치로 딕셔너리 구성
                                            #1의 자리는 첫행의 가운데로 지정되어 있으므로 if절 밖에서
                                            #입력한다.
                                            
    if numlist[num]%n !=0 or num==0 :       # 숫자가 input으로 입력한 n의 배수가 아니라면 
        (row,column)=(row-1,column-1)       # row, column 값에 -1을 해줘서 갱신한다. 
                                            #num이 0, 즉 첫번째 숫자인 1인 경우에도 다음 숫자를 위해 
                                            #갱신해야 하므로 or num==0을 해줌
                                            
        if  row <=0:                        #만약 갱신된 행의 값이 0이라면   
            row = n                         # 마지막행(n)으로 다시 갱신
        if column <=0:                      # 만약 갱신된 열의 값이 0이라면
            column =n                       # 마지막 열(n)로 다시 갱신
            
                                                   
    elif numlist[num]%n ==0 :               # 숫자가 n의 배수라면 
        (row,column)=(row+1,column)         # 바로 아랫줄로 이동, 즉 row값에 +1을 해줫 갱신한다
        
result=sorted(zip(matrix.values(),matrix.keys())) #각 숫자에 위치가 배정되면 key와 value를 뒤바꿔서
                                                  # 행렬 순으로 정렬한다.
#print(result) #[((1, 1), 6), ((1, 2), 1), ((1, 3), 8), ((2, 1), 7), ((2, 2), 5), ((2, 3), 3), ((3, 1), 2), ((3, 2), 9), ((3, 3), 4)]


#출력할 정사각형 판 만들기
a=[]
b=[]
for i in range(n*n): 
    a.append('{'+ str(i)+'}' ) #보드판에 출력될 숫자의 갯수만큼 append
#print(a) # ['{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}']

for j in range(n):
    b.append (a[j*n:(j+1)*n]) # append 된 자리들을 n개씩 자르기
#print(b)    #[['{0}', '{1}', '{2}'], ['{3}', '{4}', '{5}'], ['{6}', '{7}', '{8}']]

c=['  '.join(x) for x in b] # sublist를 없애면서 각 요소 사이에 공백추가
d='\n'.join(c) #리스트 사이에 '\n'을 추가하여 줄 넘김


# 보드판 출력
def printboard(result):
    cells=[]
    for loc,num in result:    # print(result) #[((1, 1), 6), ((1, 2), 1), ((1, 3), 8), ((2, 1), 7), ((2, 2), 5), ((2, 3), 3), ((3, 1), 2), ((3, 2), 9), ((3, 3), 4)]
        cells.append(num)     # 숫자만 append
    print((d).format(*cells)) # 보드판에 하나씩 입력 & 출력
    
printboard(result) 
       
################# 종료 시간 체크 ################# 
etime = time.time() 
print('consumption time : ', round(etime-stime, 6)) 
 
 
################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 ################# 
proc = psutil.Process(os.getpid()) 
mem = proc.memory_info() 
after_start = mem[0] 
print('memory use : ', after_start-before_start) 
