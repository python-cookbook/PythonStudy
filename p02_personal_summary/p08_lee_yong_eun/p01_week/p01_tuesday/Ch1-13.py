#######################################################################################
# 1.13) 일반 키로 딕셔너리 리스트 정렬
#
# operator.itemgetter : 정렬을 할 때 기준으로 할 대상 지정
#     * lambda로 대체할 수 있는 경우도 있으나, itemgetter가 좀 더 빠르다.
#######################################################################################

rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]

from operator import itemgetter

# 각각 fname 순 정렬, uid 순 정렬
rows_by_frame = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))

# lname, fname 순 정렬
rows_by_lfname = sorted()

print(rows_by_frame)
print(rows_by_uid)
