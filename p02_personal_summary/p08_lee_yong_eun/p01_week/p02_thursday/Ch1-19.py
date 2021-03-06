#######################################################################################
# 1.19] 데이터를 변환하면서 줄이기
#       * 감소 함수(sum,min,max 등)을 실행해야 하는데, 먼저 데이터를 변환하거나 필터링해야 한다.
#
# 1] 생성자 표현식 사용
#   : 반복적 괄호를 하지 않아도 된다.
#       임시 리스트가 생성되지 않으므로 메모리 측면에서 훨씬 유리하며, 더욱 우아하다
#######################################################################################

nums = [1, 2, 3, 4, 5]
# 생성자 표현식 사용 안 하는 경우
s = sum([x*x for x in nums])

# 생성자 표현식 사용
s = sum(x*x for x in nums)
print(s)    # 55

# 딕셔너리 등에 사용할 수 있는 응용법
# min_shares = min(s['shares'] for s in portfolio)