##########################################################################################################
# 4.10] 인덱스-값 페어 시퀀스 순환
#   * 시퀀스를 순환하려고 한다. 이때 어떤 요소를 처리하고 있는지 번호를 알고 싶다.
#
# 1] enumerate()
#   : 순환 시퀀스의 index를 함께 반환해준다.
#
#   * 카운터 변수를 스스로 다루는 것에 비해 enumerate()를 사용하는 것이 훨씬 보기 좋다.
##########################################################################################################
from collections import defaultdict

my_list = ['a', 'b', 'c']

# enumerate를 이용한 index 출력
for idx, val in enumerate(my_list):
    print(idx, val, end=' / ')  # 0 a / 1 b / 2 c /

# index 시작 번호 변경
for idx, val in enumerate(my_list, 1):
    print(idx, val, end=' / ')  # 1 a / 2 b / 3 c /

## 실전 예시 : 에러 메세지에 파일의 라인 번호를 저장하고 싶은 경우에 유용하다 !
def parse_data(filename):
    with open(filename, 'rt') as f:
        for lineno, line in enumerate(f, 1):
            fields = line.split()
            try:
                count = int(fields[1])
                #할 일...
            except ValueError as e:
                print('Line {}: Parse error: {}'.format(lineno, e))

## 라인별 단어 빈도 매핑
word_summery = defaultdict(list)

with open('myfile.txt', 'r') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    # 현재 라인의 단어 리스트를 생성
    words = [w.strip().lower() for w in line.split()]
    for word in words:
        word_summery[word].append(idx)

## 카운터 변수로서의 사용
for lineno, line in enumerate(f):
    # 작업
    pass

