###################################################################################################
## 1. 문제        : 숫자야구 (중급)
## 2. 소요 시간   : 0.02 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 16.0 kb
## 4. 만든 사람   : 배준호
## 5. 출력 결과
##
## ⊙ 정답으로 가능한 모든 경우의 수: [324, 328]
##
## ⊙ 정답의 개수: 2
##
## ⊙ 코드 실행에 걸린 시간: 0.02
##
## ⊙ 코드의 메모리 사용량: 16.0 kb
###################################################################################################


import time
import os, psutil

proc1 = psutil.Process(os.getpid())         # 시작 전 메모리 사용량 체크
mem1 = proc1.memory_info()
before_start=mem1[0]


question_list = []  # 데이터를 받을 리스트

count = 0
n = int(input('질문갯수 : '))   # 질문 갯수 입력
while count < n:
    count = count+1
    question_input = list(input('숫자3자리 스트라이크 볼넷을 입력 : ').split(' '))       # 질문을 입력받아 리스트 형태로 저장
    question_list.append(question_input)

answer_list=[]      # 모든 정답의 경우의 수를 담을 리스트

for k in range(122,988,1):      # 모든 정답의 경우의 수 : 0이 들어가는것, 중복 숫자가 들어가는 것을 제외한 123 부터 987 까지의 숫자
    if (int(str(k)[1]) != 0) & (int(str(k)[2]) != 0) & (str(k)[0] != str(k)[1]) & (str(k)[0] != str(k)[2]) & (str(k)[1] != str(k)[2]):
        answer_list.append(k)

case=[]      # 경우의 수를 담을 리스트


sTime = time.time()

for j in range(0,len(question_list),1):    # 입력한 질문 리스트를 루프문으로 각각의 질문 숫자를 판단
    if (int(question_list[j][1]) == 3) & (int(question_list[j][2]) == 0):     # 3스트 0볼은 무조건 정답 한 경우 이므로 해당 경우의 질문 값을 저장하고 루프문 바로 종료
        for k in answer_list:
            if (str(k)[0] == question_list[j][0][0]) & (str(k)[1] == question_list[j][0][1]) & (str(k)[2] == question_list[j][0][2]):
                case.append(k)


    elif (int(question_list[j][1]) == 0) & (int(question_list[j][2]) == 0):   # 0스트 0볼은 해당 숫자를 제외한 모든 경우가 정답
        for k in answer_list:
            if (str(k)[0] != question_list[j][0][0]) & (str(k)[0] != question_list[j][0][1]) & (str(k)[0] != question_list[j][0][2]) \
                    & (str(k)[1] != question_list[j][0][0]) & (str(k)[1] != question_list[j][0][1]) & (str(k)[1] != question_list[j][0][2]) \
                    & (str(k)[2] != question_list[j][0][0]) & (str(k)[2] != question_list[j][0][1]) & (str(k)[2] != question_list[j][0][2]) :
                case.append(k)

    elif (int(question_list[j][1]) == 2) & (int(question_list[j][2]) == 0):   # 2스트 0볼은 2개가 고정되고 한개는 필요없는 정보이므로 어떤 자리를 고정하고 어떤 자리를 버릴 지
        for k in answer_list:                                                 # 각각의 경우의 수를 계산해서 맞는 경우의 수를 ans리스트에 담는다
            if (str(k)[0] == question_list[j][0][0]) & (str(k)[1] == question_list[j][0][1]) & (str(k)[2] != question_list[j][0][2]): # S S X
                case.append(k)
            if (str(k)[0] == question_list[j][0][0]) & (str(k)[1] != question_list[j][0][1]) & (str(k)[2] == question_list[j][0][2]): # S X S
                case.append(k)
            if (str(k)[0] != question_list[j][0][0]) & (str(k)[1] == question_list[j][0][1]) & (str(k)[2] == question_list[j][0][2]): # X S S
                case.append(k)

    elif (int(question_list[j][1]) == 1) & (int(question_list[j][2]) == 0):   # 1스트 0볼
        for k in answer_list:
            if (str(k)[0] == question_list[j][0][0]) & (str(k)[1] != question_list[j][0][1]) & (str(k)[2] != question_list[j][0][2]) & (str(k)[2] != question_list[j][0][0])\
                    & (str(k)[2] != question_list[j][0][1]) & (str(k)[2] != question_list[j][0][2]) & (str(k)[1] != question_list[j][0][0]) \
                    & (str(k)[1] != question_list[j][0][1]) & (str(k)[1] != question_list[j][0][2]):                             # S X X
                case.append(k)
            if (str(k)[0] != question_list[j][0][0]) & (str(k)[1] == question_list[j][0][1]) & (str(k)[2] != question_list[j][0][2]) & (str(k)[2] != question_list[j][0][0]) \
                    & (str(k)[2] != question_list[j][0][1]) & (str(k)[2] != question_list[j][0][2]) & (str(k)[0] != question_list[j][0][0]) \
                    & (str(k)[0] != question_list[j][0][1]) & (str(k)[0] != question_list[j][0][2]):                            # X S X
                case.append(k)
            if (str(k)[0] != question_list[j][0][0]) & (str(k)[1] != question_list[j][0][1]) & (str(k)[2] == question_list[j][0][2]) & (str(k)[0] != question_list[j][0][0]) \
                    & (str(k)[0] != question_list[j][0][1]) & (str(k)[0] != question_list[j][0][2]) & (str(k)[1] != question_list[j][0][0]) \
                    & (str(k)[1] != question_list[j][0][1]) & (str(k)[1] != question_list[j][0][2]):                            # X X S
                case.append(k)



    elif (int(question_list[j][1]) == 1) & (int(question_list[j][2]) == 1):   # 1스트 1볼
        for k in answer_list:
            if (str(k)[0] == question_list[j][0][0]) & (str(k)[2] == question_list[j][0][1]) & (str(k)[1] != question_list[j][0][2]):           # S X B
                case.append(k)
            if (str(k)[0] == question_list[j][0][0]) & (str(k)[1] == question_list[j][0][2]) & (str(k)[2] != question_list[j][0][1]):           # S B X
                case.append(k)
            if (str(k)[1] == question_list[j][0][1]) & (str(k)[0] == question_list[j][0][2]) & (str(k)[2] != question_list[j][0][0]):           # B S X
                case.append(k)
            if (str(k)[1] == question_list[j][0][1]) & (str(k)[2] == question_list[j][0][0]) & (str(k)[0] != question_list[j][0][2]):           # X S B
                case.append(k)
            if (str(k)[2] == question_list[j][0][2]) & (str(k)[1] == question_list[j][0][0]) & (str(k)[0] != question_list[j][0][1]):           # X B S
                case.append(k)
            if (str(k)[2] == question_list[j][0][2]) & (str(k)[0] == question_list[j][0][1]) & (str(k)[1] != question_list[j][0][0]):           # B X S
                case.append(k)

    elif (int(question_list[j][1]) == 1) & (int(question_list[j][2]) == 2):   # 1스트 2볼
        for k in answer_list:
            if (str(k)[0] == question_list[j][0][0]) & (str(k)[1] == question_list[j][0][2]) & (str(k)[2] == question_list[j][0][1]):           # S B1 B2
                case.append(k)
            if (str(k)[1] == question_list[j][0][1]) & (str(k)[0] == question_list[j][0][2]) & (str(k)[2] == question_list[j][0][0]):           # B1 S B2
                case.append(k)
            if (str(k)[2] == question_list[j][0][2]) & (str(k)[1] == question_list[j][0][0]) & (str(k)[0] == question_list[j][0][1]):           # B1 B2 S
                case.append(k)

    elif (int(question_list[j][1]) == 0) & (int(question_list[j][2]) == 2):   # 0스트 2볼
        for k in answer_list:
            if (str(k)[0] == question_list[j][0][1]) & (str(k)[1] == question_list[j][0][0]) & (str(k)[2] != question_list[j][0][2]):           # B1 B2 X
                case.append(k)
            if (str(k)[0] == question_list[j][0][2]) & (str(k)[2] == question_list[j][0][0]) & (str(k)[1] != question_list[j][0][1]):           # B1 X B2
                case.append(k)
            if (str(k)[1] == question_list[j][0][2]) & (str(k)[2] == question_list[j][0][1]) & (str(k)[0] != question_list[j][0][0]):           # X B1 B2
                case.append(k)


    elif (int(question_list[j][1]) == 0) & (int(question_list[j][2]) == 1):  # 0스트 1볼
        for k in answer_list:
            # _ 4 _ str(k)[0] str(k)[0] str(k)[2] str(k)[2]
            if (question_list[j][0][0] == str(k)[1]) & (question_list[j][0][0] != str(k)[0]) & (question_list[j][0][2] != str(k)[0]) \
                    & (question_list[j][0][0] != str(k)[2]) & (question_list[j][0][2] != str(k)[2]):
                case.append(k)
            # _ _ 4 str(k)[0] str(k)[0] str(k)[1] str(k)[1]
            if (question_list[j][0][0] == str(k)[2]) & (question_list[j][0][0] != str(k)[0]) & (question_list[j][0][1] != str(k)[0]) \
                    & (question_list[j][0][0] != str(k)[1]) & (question_list[j][0][1] != str(k)[1]):
                case.append(k)
            # 8 _ _ str(k)[1] str(k)[1] str(k)[2] str(k)[2]
            if (question_list[j][0][1] == str(k)[0]) & (question_list[j][0][1] != str(k)[1]) & (question_list[j][0][2] != str(k)[1]) \
                    & (question_list[j][0][1] != str(k)[2]) & (question_list[j][0][2] != str(k)[2]):
                case.append(k)
            # _ _ 8 str(k)[0] str(k)[0] str(k)[1] str(k)[1]
            if (question_list[j][0][1] == str(k)[2]) & (question_list[j][0][0] != str(k)[0]) & (question_list[j][0][1] != str(k)[0]) \
                    & (question_list[j][0][0] != str(k)[1]) & (question_list[j][0][1] != str(k)[1]):
                case.append(k)
            # 9 _ _ str(k)[1] str(k)[1] str(k)[2] str(k)[2]
            if (question_list[j][0][2] == str(k)[0]) & (question_list[j][0][1] != str(k)[1]) & (question_list[j][0][2] != str(k)[1]) \
                    & (question_list[j][0][1] != str(k)[2]) & (question_list[j][0][2] != str(k)[2]):
                case.append(k)
            # _ 9 _ str(k)[0] str(k)[0] str(k)[2] str(k)[2]
            if (question_list[j][0][2] == str(k)[1]) & (question_list[j][0][0] != str(k)[0]) & (question_list[j][0][2] != str(k)[0]) \
                    & (question_list[j][0][0] != str(k)[2]) & (question_list[j][0][2] != str(k)[2]):
                case.append(k)

    elif (int(question_list[j][1]) == 0) & (int(question_list[j][2]) == 3):   # 0스트 3볼
        for k in answer_list:
            if (str(k)[0] == question_list[j][0][1]) & (str(k)[1] == question_list[j][0][2]) & (str(k)[2] != question_list[j][0][0]):
                case.append(k)
            if (str(k)[0] == question_list[j][0][2]) & (str(k)[1] != question_list[j][0][0]) & (str(k)[2] == question_list[j][0][1]):
                case.append(k)

# print(question_list)
# print(case)

final_answer = [i for i in set(case) if case.count(i) >= len(question_list)]
list.sort(final_answer, reverse=False)

eTime = time.time()

proc = psutil.Process(os.getpid())
mem = proc.memory_info()

print(' ')
print('⊙ 정답으로 가능한 모든 경우의 수 : ', final_answer)
print(' ')
print('⊙ 정답의 개수 : ', len(final_answer))
print(' ')
print('⊙ 코드 실행에 걸린 시간 : %.02f' %(eTime-sTime))
print(' ')
after_start=mem[0]
print('⊙ 코드의 메모리 사용량 : ', int(after_start-before_start)/1024,'kb')


# 4
# 123 1 1
# 356 1 0
# 327 2 0
# 489 0 1

# 질문갯수 : 4
# 숫자3자리 스트라이크 볼넷을 입력 : 123 0 0
# 숫자3자리 스트라이크 볼넷을 입력 : 234 0 0
# 숫자3자리 스트라이크 볼넷을 입력 : 567 3 0
# 숫자3자리 스트라이크 볼넷을 입력 : 891 0 0