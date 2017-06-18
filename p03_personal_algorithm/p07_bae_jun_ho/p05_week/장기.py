########################################################################################################
############
############   1. 방정식을 이용해서 해결 - 전수조사에 가까운 방법
############
########################################################################################################

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

########################################################################################################
############
############   2. 자료구조 알고리즘(BFS)을 이용한 방법
############
########################################################################################################

import queue
# Class for 1 horses in the chess board
class Horse:
    def __init__(self, pos, idx):
        self.pos = pos
        self.idx = idx

    # Return position of this horse
    def get_pos(self):
        return self.pos

    # Return idx of this horse
    def get_idx(self):
        return self.idx

    # Return another horse moved from this horse
    def move_and_create(self, dpos):
        return Horse(self.pos+dpos, self.idx + 1)


# Main
q = queue.Queue()
delta = (-2-1j, -1-2j, 1-2j, 2-1j, 2+1j, 1+2j, -1+2j, -2+1j)

# Input, initial setting
N, M = map(int, input().split(' '))
R, C, S, K = map(int, input().split(' '))
start, end = complex(R-1, C-1), complex(S-1, K-1)
q.put(Horse(start, 0))
visit = {}

finished = False
result = 0

# BFS
while not q.empty() and not finished:
    # Get the top of the queue
    out_horse = q.get()
    in_horse = None

    for i in range(8):
        # Find near position to get from out_horse horse
        in_horse = out_horse.move_and_create(delta[i])
        pos, x, y = in_horse.get_pos(), in_horse.get_pos().real, in_horse.get_pos().imag

        # Horse is out of the map
        if x < 0 or x >= N or y < 0 or y >= M or visit.get(pos) is not None:
            continue

        # When the horse get the end point
        if pos == end:
            result = in_horse.get_idx()
            finished = True
            break

        # Put this horse to the queue
        if not finished:
            q.put(in_horse)
            visit[pos] = 1

# Print result
print(result)