###################################################################################################
## 1. 문제        : 도미노2 (고급)
## 2. 소요 시간   : 0.00 초 (소수점 6자리 반올림)
## 3. 사용 메모리 : 8.0 kb
## 4. 만든 사람   : 배준호
## 5. 정답 : 775
###################################################################################################

import time
import os, psutil

proc1 = psutil.Process(os.getpid())         # 시작 전 메모리 사용량 체크
mem1 = proc1.memory_info()
before_start=mem1[0]

class Domino:
    def __init__(self):
        self.number_list = []  # 데이터를 받을 리스트
        self.count = 0
        self.number_a = ''
        self.number_b = ''
        self.number_list_a = []
        self.number_list_b = []
        self.number_answer_list = []
        self.n = 0
        self.question_input = []

    def input(self):
        self.n = int(input('도미노 개수 : '))   # 질문 갯수 입력
        while self.count < self.n:
            self.count = self.count+1
            self.question_input = list(input('숫자 2종류를 입력 : ').split(' '))       # 질문을 입력받아 리스트 형태로 저장
            self.number_list.append(self.question_input)

    def array_number_add(self):
        for i in range(0, self.n, 1):
            for k in range(0, self.n-1, 1):
                before = self.number_list[k]
                self.number_list[k] = self.number_list[k+1]
                self.number_list[k+1] = before
            for i in range(0, self.n, 1):
                self.number_a = self.number_a+str(self.number_list[i][0])

            for j in range(0, self.n, 1):
                self.number_b = self.number_b+str(self.number_list[j][1])
        self.number_list_a.append(self.number_a)
        self.number_list_b.append(self.number_b)

    def number_split_sum(self):
        for z in range(0, self.n, 1):
            self.number_answer_list.append(int(self.number_list_a[0][self.n*z:self.n*z+self.n])+int(self.number_list_b[0][self.n*z:self.n*z+self.n]))

    # def answer_print(self):
    #     print(max(self.number_answer_lista))

    def run(self):
        self.input()
        sTime = time.time()
        self.array_number_add()
        self.number_split_sum()
        # self.number_answer_print()
        eTime = time.time()
        proc = psutil.Process(os.getpid())
        mem = proc.memory_info()
        print(' ')
        print('⊙ 정답 : ', max(self.number_answer_list))
        print(' ')
        print('⊙ 코드 실행에 걸린 시간 : %.02f' % (eTime - sTime))
        print(' ')
        after_start = mem[0]
        print('⊙ 코드의 메모리 사용량 : ', int(after_start - before_start) / 1024, 'kb')

if __name__ == '__main__':
    domino = Domino()
    domino.run()