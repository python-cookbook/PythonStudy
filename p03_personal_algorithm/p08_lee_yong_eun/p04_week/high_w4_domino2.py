import psutil, time, os

###################################################################################################
## 1. 문제        : 도미노2 (고급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 24576 byte
## 4. 만든 사람   : 이용은
###################################################################################################

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

cnt = int(input("입력할 자릿수를 입력하세요 : "))
numlist = []
for i in range(cnt):
    n = [int(x) for x in input().split()]
    numlist.append(n)

# 시작 시간 체크
stime = time.time()

# 도미노의 두 수의 합이 큰 순서대로 정렬, 순서대로 합한 뒤 높은 자릿수에 배열
res = 0
for n in sorted(numlist, key=lambda x: sum(x), reverse=True):
    res *= 10
    res += sum(n)

print(res)

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)