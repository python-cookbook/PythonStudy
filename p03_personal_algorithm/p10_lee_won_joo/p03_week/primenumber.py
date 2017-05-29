
###################################################################################################
## 1. 문제        : 소수와 합성수
## 2. 소요 시간    : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리  : 0
## 4. 만든 사람    : 이원주
###################################################################################################


# 문제를 위해서 일단 지정된 리스트를 넣어보자.
import random
import math
import os
import psutil
import time

# 시작 메모리 체크
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]   #시작전 메모리 측정

def cal():
    start_time = time.time()
    num_list = [int(i) for i in input('숫자 입력하세요').split(' ')]
    print(num_list)
    for num in num_list:
        if num == 1:
            print('Number one')
            continue
        cnt_divid = [num%i for i in range(1,num+1)].count(0)
        # print('cnt_divid',cnt_divid)
        if cnt_divid ==2:
            print('소수')
        else:
            print('합성수')
    after_start = mem1[0]
    end_time = time.time()
    print(end_time - start_time, '초')
    print('memory use : ', after_start - before_start)

cal()







"""
소수란 1보다 큰 자연수 중 1과 자기 자신 두개 만을 약수로 갖는 수를 말한다.
합성수란 1보다 큰 자연수 중 소수가 아닌 수를 말하며 3개 이상의 약수를 갖는다.
1은 소수도 합성도 아니다.
5개의 자연수를 입력받아, 소수인지 합성수인지를 판단하는 프로그램을 작성하시오.
10억 이하의 자연수 5개가 공백으로 구분되어 주어진다.
입력된 순서대로 한 줄에 한 개씩 소수이면 프라임넘버, 합성수이면 컴포짓넘버 , 소수도 합성수도 아니면 넘버 원 이라고 출력한다.


입력 예   : 3 10 1 55 127

출력 예 :
              프라임
              컴포짓
              넘버원
              컴포짓
              프라임
"""
