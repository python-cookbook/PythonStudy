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

# answer_list=[]      # 모든 정답의 경우의 수를 담을 리스트

# for k in range(122,988,1):      # 모든 정답의 경우의 수 : 0이 들어가는것, 중복 숫자가 들어가는 것을 제외한 123 부터 987 까지의 숫자
#     if (int(str(k)[1]) != 0) & (int(str(k)[2]) != 0) & (str(k)[0] != str(k)[1]) & (str(k)[0] != str(k)[2]) & (str(k)[1] != str(k)[2]):
#         answer_list.append(k)

# case=[]      # 경우의 수를 담을 리스트


sTime = time.time()

from operator import itemgetter

class colorpaper:
    def __init__(self):
        self.question_list = question_list

    def sorting(self):
        self.sorted = sorted(question_dict, key=itemgetter('x'), reverse=False)

    def listtodict(self):
        dictkey=['x', 'y']
        question_dict = {}
        for i in range(0, len(question_list), 1):











