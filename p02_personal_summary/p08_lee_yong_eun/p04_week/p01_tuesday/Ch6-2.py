##########################################################################################################
# 6.2] JSON 데이터 읽고 쓰기
#   * JSON(Javascript Object Notation)으로 인코딩된 데이터를 읽거나 쓰고 싶다.
#       : json 모듈 사용
#
# * dumps()
#   : 파이썬 데이터를 json으로 변환
# * loads()
#   : json 인코딩된 문자열을 파이썬 자료 구조로 되돌림
# * pprint.pprint()
#   : 키를 알파벳 순으로 나열하고, 딕셔너리를 좀 더 보기 좋게 출력한다.
##########################################################################################################
import json

data = {
    'name': 'ACME',
    'shares': 100,
    'price': 542.23
}

# 파이썬 데이터를 json으로 변환
json_str = json.dumps(data)
print(json_str) # {"name": "ACME", "shares": 100, "price": 542.23}

# 인코딩된 문자열을 파이썬 자료 구조로 돌리는 방법
data = json.loads(json_str) # {'name': 'ACME', 'shares': 100, 'price': 542.23}
print(data)

# JSON 데이터 쓰기
with open('data.json', 'w') as f:
    json.dump(data, f)

# 데이터 다시 읽기
with open('data.json', 'r') as f:
    data = json.load(f)
    print(data) # {'name': 'ACME', 'shares': 100, 'price': 542.23}

## 트위터의 검색 결과 출력하기
from urllib.request import urlopen
from pprint import pprint

u = urlopen('http://search.twitter.com/search.json?q=python&rpp=5')
resp = json.loads(u.read().decode('utf-8'))
pprint(resp)