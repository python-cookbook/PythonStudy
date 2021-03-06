###############################################################################################
# 2.7] 가장 짧은 매칭을 위한 정규 표현식
#   * 정규 표현식을 사용한 텍스트 매칭을 하고 싶지만 텍스트에서 가장 긴 부분을 찾아낸다.
#     만약 가장 짧은 부분을 찾아내고 싶다면?
#
# 1] * 앞에 ?를 붙인다.
#   ex) (.*?)
###############################################################################################
import re

## 아무 옵션도 하지 않으면 패턴에 맞는 가장 긴 부분을 반환한다.(Greedy)
# 여기서의 반환 : Hi". I say "Bye
# 우리가 원하는 반환 : "Hi", "Bye"
str_pat = re.compile(r'\"(.*)\"')
text = 'He say "Hi". I say "Bye".'
res = str_pat.findall(text)
print(res)  # ['Hi". I say "Bye']

## 가장 짧은 부분을 찾아내도록 하는 코드
# 패턴을 (.*?)로 ?를 붙여준다 !
str_pat = re.compile(r'\"(.*?)\"')
res = str_pat.findall(text)
print(res)  # ['Hi', 'Bye']

