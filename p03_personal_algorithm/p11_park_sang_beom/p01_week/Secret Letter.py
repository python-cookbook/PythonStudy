import os
import psutil
import time

###################################################################################################
## 1. 문제        : 비밀편지
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 28672 byte
## 4. 만든 사람    : 박상범
###################################################################################################

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

# 001111000000011100
letter = {
          '000000':'A',
          '001111':'B',
          '010011':'C',
          '011100':'D',
          '100110':'E',
          '101001':'F',
          '110101':'G',
          '111010':'H'
         }

# 비밀편지 딕셔너리 키 값 리스트화
letter_key = list(letter.keys())


letter_cnt = int(input())*6     # 문자의 개수
letter_num = input()            # 비밀편지 숫자

# 시작 시간 체크
stime = time.time()

temp =[]        # 6개씩 자른 비밀편지 숫자를 담을 리스트 변수
start = 0       # 비밀편지 숫자를 6개씩 자르기 위한 변수1
finish = 6      # 비밀편지 숫자를 6개씩 자르기 위한 변수2
cnt = 0         # 숫자 비교를 위한 카운팅 변수
count = 0       # 위치 확인을 위한 카운팅 변수
result = []     # 6개씩 자른 숫자를 문자로 바꿔서 담을 리스트 변수
ct = []         # 틀린 위치 리스트 변수

while finish <= letter_cnt:
    temp.append(letter_num[start:finish])
    start += 6
    finish += 6

for key in temp:
    for i in range(8):
        cnt = 0
        for j in range(6):
            if key[j] == letter_key[i][j]:
                cnt += 1
                if cnt == 5:
                    count += 1
                    result.append(letter[letter_key[i]])
                if len(temp) == count:
                    ct.append(0)
                elif cnt != 5:
                    ct.append(count)

print(''.join(result))
print(ct[-1])

# 종료 시간 체크
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

# 실행 후 맨 밑에서 코드 구동 후 메모리 체크
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
