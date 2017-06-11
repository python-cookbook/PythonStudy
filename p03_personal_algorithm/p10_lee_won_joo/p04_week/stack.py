###################################################################################################
## 1. 문제        : 소수와 합성수
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 0
## 4. 만든 사람    : 이원주
###################################################################################################
import os
import psutil
import time


# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]   #시작전 메모리 측정
print(before_start)
class Stack:
    def __init__(self):
        self.__index = 0  # 명령어 수
    def put_stack(self):
        start_time = time.time()
        result = list()
        self.__index = int(input('명령어 제한을 설정하세요.'))
        while self.__index > 0:
            try:
                num = input('입력하세요')
                if num[0] == 'i':
                    if len(num) == 1:
                        continue
                    print('스택을 쌓았습니다.')
                    result.append(num[2:])
                    self.__index -= 1
                elif num[0] =='o':
                    if len(result) > 0:
                        print(result[-1])
                        result.pop()
                        self.__index -= 1
                    elif len(result) == 0:
                        print('empty')
                        self.__index -= 1
                elif num[0] =='c':
                    print(len(result))
                    self.__index -= 1
            except:
                print('잘못된 명령어입니다.')
                continue
            print(self.__index,'번 남았습니다.')
        after_start = mem1[0]
        end_time = time.time()
        print(end_time - start_time, '초')
        print(after_start)
        print('memory use : ', after_start - before_start)
        return

stack = Stack
stack().put_stack()



"""
스택 구조

그림과 같이 스택을 설계하고 처리조건에 맞는 출력을 하시오!

선입 후출방식
맨 위가 top이다.

처리조건 : 
주어진 명령은 다음의 3가지 이다.
1) 'i + 숫자'   (숫자는 1 <= N <= 100)
2) 'o'는 스택에서 데이터를 빼고, 그 데이터를 출력한다.
   if 스택이 비어있으면 empty 를 출력한다.
3) 'c'는 스택에 쌓여있는 데이터의 수를 출력한다.
----------------------------------------------------
첫줄에 N이 주어진다. 
N은 주어지는 명령의 수마다 둘째 줄부터 N+1줄까지 N개의 명령이 주어지는데, 
한 줄에 하나씩 주어진다.


아래의 경우 7까지의 명령의 수가 주어진다.

------------------------------------
각 명령에 대한 출력 값을 한 줄에 하나씩 출력한다. 출력 내용이 하나도 없는 경우는 주어지지 않는다.

입력              출력
7                   2
i 7                  5
i 5                  7
c                   empty
o                   0
o
o
c

"""