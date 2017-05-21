import time
import os, psutil
''
question_list = []  # 데이터를 받을 리스트

count = 0
n = int(input('질문갯수 : '))   # 질문 갯수 입력
while count < n:
    count = count+1
    question_input = list(input('0부터 90까지 좌표점을 공백구분으로 입력 : ').split(' '))       # 질문을 입력받아 리스트 형태로 저장
    question_list.append(question_input)

sTime = time.time()
proc1 = psutil.Process(os.getpid())         # 시작 전 메모리 사용량 체크
mem1 = proc1.memory_info()
before_start=mem1[0]


def bubble(a):      # 버블 정렬로 x좌표가 내림차순 순으로 정렬
    for i in range(0,len(a)-1,1):
        for j in range(0,len(a)-1,1):
            if int(a[j][0]) >= int(a[j+1][0]):  # j번째가 j+1번째보다 크면 continue로 패스
                continue
            if int(a[j][0]) <= int(a[j+1][0]):  # j번째가 j+1번째보다 작으면 버블정렬로 큰것이 앞으로 가게 정렬
                temp = a[j]     # temp에 작은 수를 담아서
                a[j] = a[j+1]   # j와 j+1번째 수를 바꿔서 내림차순으로 정렬
                a[j+1] = temp

bubble(question_list)    # 위에서 생성한 버블정렬 내림차순 함수로 입력받은 질문리스트를 정렬

answer = 100*int(len(question_list))      # 사각형의 넓이를 담는 변수 시작은 사각형 개수 * 한 사각형의 넓이로 시작한다.

for i in range(0,len(question_list)-1,1):   # 질문이 n개라면 n-1 번째 까지에 대해 겹치는 부분만 빼주면 된다.
    if int(question_list[i][0]) - int(question_list[i+1][0]) >= 10:   # 두 사각형 시작지점 x좌표의 차이가 10 이상이면 두 사각형은 겹치지 않으므로 continue 한다.
        continue
    if int(question_list[i][0]) - int(question_list[i+1][0]) < 10:    # 두 사각형의 시작지점 x좌표의 차이가 10 미만이라면 두 사각형은 겹치게 된다. 이땐 생각이 필요하다.
         base = int(question_list[i+1][0])+10 - int(question_list[i][0])     # 이 경우 i+1번째 사각형의 시작지점 x좌표+10 한 좌표에서 i번째 사각형의 시작지점의 x좌표를 뺀 값이 겹치는 부분의 사각형의 밑변이 된다.
         height = int(question_list[i][1])+10 - int(question_list[i+1][1])      # 또한 i번째 사각형의 시작지점의 y좌표+10 한 좌표에서 i+1번째 사각형의 시작지점의 y좌표를 뺀 값이 겹치는 부분의 사각형의 높이가 된다.
         area = base * height    # 겹치는 부분의 사각형의 넓이
         answer = answer - area      # 전체 사각형 넓이의 합에서 조건이 부합할 때마다 겹치는 부분의 사각형 넓이를 제거

eTime = time.time()

proc = psutil.Process(os.getpid())
mem = proc.memory_info()
after_start=mem[0]

print('⊙ 구하고자 하는 넓이 : ', answer)
print('⊙ 코드 실행에 걸린 시간 : %.02f' %(eTime-sTime))
print('⊙ 코드의 메모리 사용량 : ', int(after_start-before_start)/1024,'kb')