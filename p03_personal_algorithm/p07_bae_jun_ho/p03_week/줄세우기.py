###################################################################################################
## 1. 문제        : 줄 세우기 (중급)
## 2. 소요 시간   : 0.00 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 12.0 kb
## 4. 만든 사람   : 배준호
## 5. 출력 결과
# 4 2 3 5 1
###################################################################################################


import time
import os, psutil
''


proc1 = psutil.Process(os.getpid())         # 시작 전 메모리 사용량 체크
mem1 = proc1.memory_info()
before_start=mem1[0]


class Student:                  # 클래스 Student 생성
    def __init__(self):           # 초기화
        self.question_list = []   # question_list 를 빈 리스트로 선언
        self.n = 0                # n의 초기값으로 0 설정
        self.student_list = []    # 학생들을 정렬할 리스트인 student_list로 빈 리스트로 선언
        self.question_tuple = ()  # 필터링에 사용 할 맨 처음 입력된 순서는 변경되면 안되므로 변경불가하게 하기 위한 튜플 question_tuple을 빈 튜플로 선언
        self.filter_list = []     # 뽑은 표로 정렬 한 뒤 학생의 자리를 찾아가게 하기 위한 필터링 리스트를 filter_list로 빈 리스트로 선언
        self.answer_list = []     # 뽑은 표를 담아 정렬하는 answer_list 를 빈리스트로 선언

    def input(self):    # 학생 수, 뽑은 표를 input 받아 question_list에 저장
        self.n = int(input('학생 인원 수 : '))
        self.question_list = list(input('각각의 학생이 뽑은 숫자 : ').split(' '))

    def timechk(self):  # 구동 시간 체크하기 위한 시작시간 체크
        self.sTime = time.time()
        return self.sTime

    def change(self):                                         # 알고리즘 해결에 필요한 데이터셋들을 생성
        self.question_tuple = tuple(self.question_list)         # 위에서 입력받은 표에 대한 변경 전 초기 정보를 갖기 위해 question_list를 튜플화 해서 저장
        self.filter_list = list(self.question_tuple)            # 초기값의 위치를 찾아 갈 때 중복값을 필터링할 때 사용하기 위한 리스트.
        self.answer_list = self.question_list                   # 정답을 찾는데 사용 할 리스트

    def arrayS(self):                                         # 학생 위치를 정렬
        for i in range(0, len(self.answer_list), 1):           # 전체 answer_list에 대해 루프
            for j in range(0, len(self.answer_list), 1):       # 학생이 뽑을 수 있는 표는 학생이 표를 뽑는 순서 -1 만큼의 경우의 수로 존재.
                if int(self.answer_list[i]) == j:               # 해당 학생이 가진 숫자를 가지고 아래에서 순서를 바꿈
                    temp1 = self.answer_list[i]                 # 순서를 바꾸기전 학생의 위치를 temp1 에 담음
                    temp2 = self.answer_list[i - j:i]           # 순서가 바뀌게 되면 바뀌게 될 순서 뒤부터 원래 있던 위치까지의 학생 정보를 temp2에 담음
                    self.answer_list[i - j + 1:i + 1] = temp2   # 순서가 바뀔 예정이므로 바뀌는 부분을 temp2를 넣어서 한칸 뒤로 이동
                    self.answer_list[i - j] = temp1             # 뽑은 표에 해당하는 위치로 원래 학생(temp1)을 이동

    def filterS(self):                                        # 정렬한 학생 위치들에 맞는 학생을 찾아감
        for i in range(0, len(self.answer_list), 1):           # answer_list에 대해 루프
            for j in range(0, len(self.filter_list), 1):       # 필터링에 쓰는 filter_list에 대해 루프
                if self.answer_list[i] == self.filter_list[j]:  # 정렬된 학생이 필터리스트에 있으면
                    self.student_list.append(j + 1)             # 정답리스트에 append
                    self.filter_list[j] = 'a'                   # 필터에 사용한 값은 중복 필터링을 방지하기 위해 학생 위치리스트에 없는 값으로 변경

    def strun(self):                                           # Student 클래스를 구동
        self.input()
        self.timechk()
        self.change()
        self.arrayS()
        self.filterS()
        print(' '.join([str(num) for num in self.student_list])) # 문제에서 요구한 출력 포멧으로 출력


if __name__ == '__main__':  # 실행
    student = Student()
    student.strun()
    eTime = time.time()
    proc = psutil.Process(os.getpid())
    mem = proc.memory_info()
    after_start=mem[0]
    print('⊙ 코드 실행에 걸린 시간 : %.02f' %(eTime-student.sTime))
    print('⊙ 코드의 메모리 사용량 : ', int(after_start-before_start)/1024,'kb')