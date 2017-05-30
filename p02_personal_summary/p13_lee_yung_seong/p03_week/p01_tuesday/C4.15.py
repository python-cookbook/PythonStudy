#정렬된 여러 시퀀스를 병합 후 순환
#문제
#정렬된 시퀀스가 여럿 있고, 이들을 합친 후 정렬된 시퀀스를 순환하고 싶다.
#해결
#heap.merge()
import heapq
a = [1,4,7,10]
b = [2,5,6,11]
for c in heapq.merge(a,b):
    print(c)

#토론
#heapq.merge는 아이템에 순환적으로 접근하며 제공한 시퀀스를 한꺼번에 읽지 않는다. 따라서 아주 긴 시퀀스도 별다른 무리 없이 사용할 수 있다.
#예를 들어 정렬된 두 파일을 병합하려면 다음과 같이 한다.
import heapq

with open('sorted_file_1','rt') as file1, \
    open('sorted_file_1','rt') as file2, \
    open('merged_file','wt') as outf:

    for line in heapq.merge(file1,file2):
        outf.write(line)

#heapq.merge()에 넣는 시퀀스는 모두 정려로디어 있어야 한다. 이 함수에 전달한다고 우선적으로 정렬을 하지 않는다.
#또한 입력된 데이터가 정렬되어 있는지 확인하지도 않는다. 단지 앞에서부터 읽어 가면서 가장 작은 것부터 데이터를 출력할 뿐이다.
#선택한 시퀀스에서 아이템을 읽고 모든 입력을 소비할 때까지 반복적으로 처리한다.