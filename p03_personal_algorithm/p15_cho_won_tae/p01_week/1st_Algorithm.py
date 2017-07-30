###################################################################################################
## 1. 문제        : 비밀 편지 (중급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 102400
## 4. 만든 사람   : 조원태
###################################################################################################
import psutil
import time
import os
# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]
from operator import eq
def Substr(password,first,last): # 6자리씩 잘라주는 함수
    return password[first:last]

def InEqual(pw_list,input_list): # 하나 하나씩 비교하는 함수
    cnt=0
    for i in range(6):
        if pw_list[i] == input_list[i]:
            cnt+=1
    if cnt == 5:
        return True
    else:
        return False

pw_list=[(65,'000000'),(66,'001111'),(67,'010011'),(68,'011100'),
         (69,'100110'),(70,'101001'),(71,'110101'),(72,'111010')] # 암호 리스트
input_list=[] # 암호를 담을 리스트
answer='' # 암호 해독할 변수
correct=01
wrong=0
temp='' # 암호 해독과 비교할 변수

# 시작 시간 체크
stime = time.time()

input1=int(input('문자의 개수 입력 : '))
input2=input('암호 입력 : ')

for i in range(input1):
    input_list.append(Substr(input2,i * 6,(i + 1)*6)) # 6자리씩 쪼갠다
    temp=answer

    for j in range(8): # 두 코드가 완전히 같다면
        if eq(input_list[i],pw_list[j][1]):
            answer += chr(pw_list[j][0])
            correct+=1
            break

    for j in range(8): # 두 코드가 다를때 하나만 다른 경우를 찾고 싶을때
        if InEqual(pw_list[j][1],input_list[i]):
            answer += chr(pw_list[j][0])
            correct+=1
            break

    wrong+=1
    if temp==answer:
        break

if correct == wrong:
    print(answer)
else:
    print(correct+1)

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))


# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)