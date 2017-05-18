#######################################################################################
# 1.8) 딕셔너리 계산
#
# zip() : 1회용 이터레이터 생성
#######################################################################################

#주식
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}

# 일반적으로 사용하면 오직 키에 대해서만 작업이 이루어진다.
print(min(prices)) # AAPL
print(max(prices)) # IBM

# value에 대해 작업을 하고 싶다면 zip()을 이용해서 value와 key를 뒤집어준다.
min_price = min(zip(prices.values(),prices.keys()))
print(min_price) # (10.75, 'FB')

prices_sorted = sorted(zip(prices.values(),prices.keys()))
print(prices_sorted) # [(10.75, 'FB'), (37.2, 'HPQ'), (45.23, 'ACME'), (205.55, 'IBM'), (612.78, 'AAPL')]

#어떤 주식이 가장 쌀까?
min_price = min(prices, key=lambda k: prices[k])
print(min_price) # FB
print(prices[min_price]) # 10.75 => 이 값을 알기 위한 과정이 번거롭다!