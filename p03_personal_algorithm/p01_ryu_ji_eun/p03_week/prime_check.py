import os
import time
import psutil

##################################################################################################
## 1. 문제        : 합성수,소수 판별 (초급)
## 2. 소요 시간   : 4.24307 초 (소수점 6자리 반올림)
## 3. 사용 메모리 :  40960 byte
## 4. 만든 사람   : 류지은
##################################################################################################

################ 시작 메모리 체크 #################
proc1 = psutil.Process(os.getpid())
mem1 = proc1.memory_info()
before_start = mem1[0]

################ 시작 시간 체크 #################
stime = time.time()



def Prime_check():
    raw_list = input("공백을 사이에 두고 숫자들을 입력하세요(1, 0은 제외): ").split(' ')          # 잘라주고
    int_list = list(map(lambda x:int(x), raw_list))                                       # 인트형으로 바꿔서 넣어준다

    basic=[2,3,5,7,11,13]                                             # 기본 소수 소팅용 프라임's
    prime_check=[]                                              # 프라임 체크용 리스트

    for i in int_list:                                          # 인트 리스트의 숫자를 돌리는데
        for b in basic:                                         # 기본 소수 소팅용 프라임's도 돌려서
            try:                                                # Value error가 무서워서 try 넣어주고
                if i in [1,2,3,5,7,11,13]:                      # 15이하 소수는 특별 취급해서 i가 여기에 있으면
                    prime_check.append(1)                        # 프라임 체크용 리스트에 1 (True)을 넣어주세요
                    continue

                else:
                    if i % b == 0:                              # 나눴는데 나머지가 0임
                        prime_check.append(0)                   # 얘 합성수네. 0 (False)
                        continue

                    else:
                        prime_check.append(1)                   # 그외엔 뭐..
                        continue

            except:                                             # try가 있으니 except가 따라와야..
                continue


    part_check = [prime_check[x:x + 6] for x in range(0, len(prime_check), 6)]    # 6개(위의 basic 리스트안에 숫자 개수) 씩 짜르구
    # print(part_check)

    for i in part_check:                                            # 잘라준 리스트들 안에서 각각 숫자를 돌려봅니다.
        # print(i)
        if i.count(0) >= 1:                                         # 0 (False)를 체크해서 1개라도 있으면
            print("Composite number")                             # 합성수구요

        else:                                                       # 죄다 1이면
            print("Prime number")                                  # 소수입니다

Prime_check()


################# 종료 시간 체크 #################
etime = time.time()
print('consumption time : ', round(etime-stime, 6))

################# 실행 후 맨 밑에서 코드 구동 후 메모리 체크 #################
proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start = mem[0]
print('memory use : ', after_start-before_start)
