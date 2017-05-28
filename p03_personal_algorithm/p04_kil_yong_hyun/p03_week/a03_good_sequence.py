import psutil, time, os

###################################################################################################
## 1. 문제        : 좋은 수열 (고급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 28672 byte
## 4. 만든 사람   : 길용현
###################################################################################################

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

def check_sequence(number, index):
    if index >= 1:
        if number[index-1] == number[index]:
            return False
    if index >= 3:
        if number[index-3:index-1] == number[index-1:index+1]:
            return False
    if index >= 5:
        if number[index-5:index-2] == number[index-2:index+1]:
            return False
    return True

number = []

while True:
    digit = int(input('자리수를 입력하세요 : '))
    if 1 <= digit <= 80:
        break
    else:
        print('1~80 이하의 자리수만 가능합니다.')

# 시작 시간 체크
stime = time.time()

for index in range(digit):
    for i in range(1, 4):
        number.append(i)
        if check_sequence(number, index):
            break
        else:
            del number[index]

print(''.join([str(num) for num in number]))

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)