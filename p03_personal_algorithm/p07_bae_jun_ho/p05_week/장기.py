from operator import itemgetter
import time
import os, psutil

proc1 = psutil.Process(os.getpid())         # 시작 전 메모리 사용량 체크
mem1 = proc1.memory_info()
before_start=mem1[0]

class Knight_vs_pawn:
    def __init__(self):
        self.row_col_n = []
        self.knight_pawn_loc = []
        self.ans_list = []

    def input_row_col(self):
        self.row_col_n = list(input('행과 열의 숫자를 입력 : ').split(' '))

    def input_knight_pawn(self):
        self.knight_pawn_loc = list(input('마의 위치와 졸의 위치를 입력 : ').split(' '))

    def timechk(self):  # 구동 시간 체크하기 위한 시작시간 체크
        self.sTime = time.time()
        return self.sTime

    def equation(self):
        knight_row = int(self.knight_pawn_loc[0])
        knight_col = int(self.knight_pawn_loc[1])
        pawn_row = int(self.knight_pawn_loc[2])
        pawn_col = int(self.knight_pawn_loc[3])

        for a in range(0, round((int(self.row_col_n[0])+int(self.row_col_n[1]))/2), 1):
            for b in range(0, round((int(self.row_col_n[0])+int(self.row_col_n[1]))/2), 1):
                for c in range(0, round((int(self.row_col_n[0])+int(self.row_col_n[1]))/2), 1):
                    for d in range(0, round((int(self.row_col_n[0])+int(self.row_col_n[1]))/2), 1):
                        for e in range(0, round((int(self.row_col_n[0])+int(self.row_col_n[1]))/2), 1):
                            for f in range(0, round((int(self.row_col_n[0])+int(self.row_col_n[1]))/2), 1):
                                for g in range(0, round((int(self.row_col_n[0])+int(self.row_col_n[1]))/2), 1):
                                    for h in range(0, round((int(self.row_col_n[0])+int(self.row_col_n[1]))/2), 1):
                                        if pawn_row == (knight_row - 2)*(a + b) + (knight_row + 2)*(c + d) + (knight_row - 1)*(e + f) + (knight_row + 1)*(g + h) \
                                           and pawn_col == (knight_col - 1)*(a + b) + (knight_col + 1)*(c + d) + (knight_col - 2)*(e + f) + (knight_col + 2)*(g + h):
                                            ans_sum = a + b + c + d + e + f + g + h
                                            self.ans_list.append(ans_sum)
        print(min(self.ans_list))


    def run(self):
        self.input_row_col()
        self.input_knight_pawn()
        self.timechk()
        self.equation()


if __name__ == '__main__':
    kp = Knight_vs_pawn()
    kp.run()
    eTime = time.time()
    proc = psutil.Process(os.getpid())
    mem = proc.memory_info()
    after_start=mem[0]
    print('⊙ 코드 실행에 걸린 시간 : %.02f' %(eTime-kp.sTime))
    print('⊙ 코드의 메모리 사용량 : ', int(after_start-before_start)/1024,'kb')