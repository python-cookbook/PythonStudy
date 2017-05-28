#인덱스 값 페어 시퀀스 순환
#시퀀스를 순환하려고 한다. 이때 어떤 요소를 처리하고 있는지 번호를 알고 싶다.
#해결 enumrate
my_list = ['a','b','c']
for idx, val in enumerate(my_list):
    print(idx,val)

for idx, val in enumerate(my_list,1):#출발을 1부터 하고 싶으면 이렇게
    print(idx,val)


#이번 예제는 에러 메시지에 파일의 라인 번호를 저장하고 싶은 경우에 유용하다.
def parse_data(filename):
    with open(filename,'rt') as f:
        for lineno, line in enumerate(f,1):
            fields = line.split()
            try:
                cont = int(fields[1])
            except ValueError as e:
                print(lineno,e)

#enumerate는 예를 들어 특정 값의 출현을 위한 오프셋 추적에 활용하기 좋다. 따라서 파일 내의 단어를 출현한 라인에 매핑하려면, enumerate()로 단어를 파일에서 발견한 라인 오프셋에 매핑한다.
from collections import defaultdict
word_summary = defaultdict(list)
word_summary
with open('myfile.txt','r') as f:
    lines = f.readlines()
for idx, line in enumerate(lines):
    words = [w.strip,format() for w in line.splt()]
    for word in words:
        word_summary[word].append(idx)

#파일 처리 후 word_summary를 출력하면 이는 각 단어를 키로 갖는 딕셔너리 형태가 된다. 키에 대한 값은 그 단어가 나타난 라인의 리스트가 된다.
#한 라인에 단어가 두번 나오면 그 라인은 두번 리스팅 되어 텍스트에 대한 단순 지표를 알아볼수있도록 한다.
#토론
#카운터 변수를 스스로 다루는 것에 비해 enumerate가 보기 좋다.
#enumerate가 반환하는 값은 연속된 튜플을 반환하는 이터레이터인 enumerate 객체의 인스턴스이다.
#한번 더 풀어 줘야 하는 튜플의 시퀀스에 enumerate()를 사용할 때는 실수를 범하기 쉽다.
data = [ (1,2),(3,4)]
for n,(x,y) in enumerate(data):#이런식으로 리스트 안의 데이터 형태에 맞게 작성해주어야 한다. 괄호 풀면 작동하지 않음.
    print(n,(x,y))