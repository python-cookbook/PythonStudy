#######################################################################################
# 1.4) N 아이템의 최대 혹은 최소값 찾기
#
# heapq : nlargest, nsmallest
# lambda s: s['price']
#######################################################################################

import heapq

###예제 1)
nums = [1,8,2,23,7,-4,18,23,42,37,2]

#가장 큰 값 순서대로 3개 출력
print(heapq.nlargest(3,nums)) #[42, 37, 23]

#가장 작은 값 순서대로 3개 출력
print(heapq.nsmallest(3,nums)) #[-4, 1, 2]


###예제 2)
portfolio = [
    {'name': 'A', 'shares': 100, 'price': 91.1},
    {'name': 'B', 'shares': 50, 'price': 543.22},
    {'name': 'C', 'shares': 200, 'price': 21.09},
    {'name': 'D', 'shares': 35, 'price': 31.75},
    {'name': 'E', 'shares': 45, 'price': 16.35},
    {'name': 'F', 'shares': 75, 'price': 115.65}
]
#가격이 가장 높은 3개 값 반환
expensive = heapq.nlargest(3,portfolio,key=lambda s: s['price'])
print(expensive) #[{'name': 'B', 'shares': 50, 'price': 543.22}, {'name': 'F', 'shares': 75, 'price': 115.65}, {'name': 'A', 'shares': 100, 'price': 91.1}]

