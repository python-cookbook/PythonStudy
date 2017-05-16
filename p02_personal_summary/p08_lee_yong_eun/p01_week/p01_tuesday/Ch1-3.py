#######################################################################################
# 1.3)마지막 N개 아이템 유지
#
# deque : maxlen, append
# yield
#######################################################################################

from collections import deque

#검색하고 결과 히스토리(5개) 저장
def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        previous_lines.append(line)

# 파일 사용 예
if __name__ == '__main__':
    with open('somefile.txt') as f:
        for line, prevlines in search(f, 'python', 5):
            for pline in prevlines:
                print(pline, end='')
            print(line, end='')
            print('-'*20)
