import os
import time
import psutil

###################################################################################################
## 1. 문제        : 떡 먹는 호랑이 (중급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 :  20480 byte
## 4. 만든 사람   : 박무성
###################################################################################################

# 인풋 받기
input_list = input('몇 번째 항인지, 떡의 갯수는 얼만지 입력하세요 ').split(' ')

# ################ 시작 메모리 체크 #################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 #################
stime = time.time()


# 1항=1, 2항=1로 시작하는 피보나치수열 함수 만들기
def fibo(num):
    if num <= 2:
        return 1
    return fibo(num - 1) + fibo(num - 2)

# 몇번째 날인지(cnt), 마지막 날 몇개의 떡을 줬는지(num) 입력하면
# 첫째날, 둘째날 준 떡의 개수 출력해주는 함수
def dduck(cnt, num):
    #first_second_list = []
    last_number = num

    for first_number in range(1,num+1):
        remain_number = (last_number - (fibo(cnt - 2) * first_number))
        second_number = remain_number // fibo(cnt - 1)

        if first_number <= second_number and remain_number % fibo(cnt-1) == 0:
            return first_number,second_number
            #first_second_list.append([first_number, second_number])

if __name__ == '__main__':
    dduck_list = dduck(int(input_list[0]),int(input_list[1]))
    print('\n''첫 번째 날은 {0}개, 두번째날은 {1}개 먹었어요.'.format(dduck_list[0], dduck_list[1]))


################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)


