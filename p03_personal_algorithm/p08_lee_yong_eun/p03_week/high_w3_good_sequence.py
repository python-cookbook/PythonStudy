import psutil, time, os

###################################################################################################
## 1. 문제        : 좋은 수열 (고급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 24576 byte
## 4. 만든 사람   : 이용은
###################################################################################################

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

index = int(input('자릿수를 입력하세요(1~80) : '))

# 일의 자릿수를 끼고 좋은 수에 위배되는 조건이 없는지 확인
# ex) 12345 -> 4<->5, 23<->45 비교
def is_good_number(n):
    n = ''.join(reversed(str(n)))
    for i in range(1, int(len(n)/2)+1):
        if n[:i] == n[i:2*i]:
            return False
    return True


# 시작 시간 체크
stime = time.time()

# 1. N자리 숫자까지의 숫자가 최소였으면, N+1자리의 경우 그 뒤에 무언가를 붙인 숫자가 최소가 된다. (단, 조건에 맞을 시)
# 2. N자리까지의 숫자가 좋은 수였다면, N+1자리 숫자가 좋은 수인지는 마지막 숫자를 포함한 수열만 체크하면 된다.
res = 0
i = 0
j = 1
while i < index:
    while True:
        # 직전 자릿수의 결과에 1,2,3 어떤 것을 붙여도 좋은 수가 될 수 없을 때 : 전 단계로 돌아가서 직전 자릿수를 바꾼다.
        # ex) 1213121 + 1,2,3 중 어떤 것도 나쁜 수가 된다. 이 경우 121312 + j=2부터 시작해서 다시 체크.
        if j >= 4:
            j = int(str(res)[-1])+1
            res = int(str(res)[0:-1])
            i -= 2
            break

        # 직전 결과에 j를 붙였을 때 좋은 수가 되는지, 가장 작은 j부터 체크
        # 좋은 수가 성립하면 결과값을 갱신하고 다음 자릿수 탐색으로 넘어간다.
        elif is_good_number(res*10+j):
            res = res*10 + j
            j = 1
            break
        j += 1
    i += 1

print('res : {}'.format(res))

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)