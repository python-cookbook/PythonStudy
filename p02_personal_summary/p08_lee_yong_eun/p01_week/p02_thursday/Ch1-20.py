#######################################################################################
# 1.20] 여러 매핑을 단일 매핑으로 합치기
#       * 딕셔너리나 매핑이 여러 개 있고, 자료 검색이나 데이터 확인을 위해 하나의 매핑으로 합치고 싶다.
#
# 1] collections.ChainMap() 사용
#   : 여러 맵에서 한꺼번에 검색 가능
#     중복 키가 있을 시엔 언제나 첫 번째 매핑의 값을 참조한다.
#     => 프로그래밍 언어와 같이 전역변수/지역변수 등이 존재하는 경우 사용하면 유용하다.
# 2] update()를 사용해 딕셔너리 합치기
#   : 완전 새로운 딕셔너리를 만들어야 한다.
#     원본 딕셔너리의 값이 바뀌어도 합친 딕셔너리에는 적용되지 않는다.
#######################################################################################

# collections.ChainMap() 사용
from collections import ChainMap

a = {'x':1, 'z':3}
b = {'y':2, 'z':4}
c = ChainMap(a,b)
print(c['x'])   # 1 from a
print(c['y'])   # 2 from b
print(c['z'])   # 3 from a


# 전역/지역변수 형태로 사용해보기
values = ChainMap()
values['x'] = 1
values = values.new_child()
values['x'] = 2
values = values.new_child()
values['x'] = 3

print(values)   # ChainMap({'x': 3}, {'x': 2}, {'x': 1})
print(values['x'])  # 3

values = values.parents
print(values)   # ChainMap({'x': 2}, {'x': 1})
print(values['x'])  # 2
