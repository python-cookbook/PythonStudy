#######################################################################################
# 1.17) 딕셔너리의 부분 추출
#       * 딕셔너리의 특정 부분으로부터 다른 딕셔너리를 만들고 싶다.
#
# 1] Dictionary Comprehension
# 2] 튜플 시퀀스를 만들어 전달 (깔끔하지 못하고 느리다 !)
#######################################################################################

# Dictionary Comprehension
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}
#가격이 200 이상인 것에 대한 딕셔너리
p1 = {key:value for key, value in prices.items() if value > 200 }
print(p1) # {'AAPL': 612.78, 'IBM': 205.55}

# 기술 관련 주식으로 딕셔너리 구성
tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = {key:value for key, value in prices.items() if key in tech_names}

# 튜플 시퀀스를 만들어 전달하는 방법 (나쁜 방법)
p1 = dict((key, value) for key, value in prices.items() if value > 200)