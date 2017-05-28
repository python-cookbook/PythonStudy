##########################################################################################################
# 4.6] 추가 상태를 가진 제너레이터 함수 정의
#   * 제너레이터 함수를 정의하고 싶지만, 사용자에게 노출할 추가적인 상태를 넣고 싶다.
#
#   * 제너레이터 함수와 클래스 정의 중 그때그때 더 좋은 것을 취사선택해야만 한다.
##########################################################################################################

from collections import deque


class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)

    # 사용자에게 추가 상태를 노출하기 위한 제너레이터 함수
    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()


# 사용 예시
with open('somefile.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')