###############################################################################################
# 2.8] 여러 줄에 걸친 정규 표현식 사용
#   * 여러 줄에 걸친 정규 표현식 매칭을 사용하고 싶다.
#
# 1] 줄바뀜 명시
# 2] re.DOTALL 플래그 사용
#   : 간단한 패턴에는 잘 동작하지만, 아주 복잡한 패턴을 사용하거나 여러 정규 표현식을 합쳐 토큰화하는 등에서 문제가 발생할 수 있다.
#     따라서 다른 선택의 여지가 있다면 플래그는 사용하지 않는 것이 좋다.
###############################################################################################
import re

## 줄바뀜을 패턴에 명시해 주지 않으면 .*로는 찾을 수 없다.
comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = '''/* this is a
            multiline comment */'''

res = comment.findall(text1)
print(res)  # [' this is a comment ']
res = comment.findall(text2)
print(res)  # [] (결과 없음)

## 줄바뀜 명시
# (?:.|\n) : 논캡쳐 그룹(매칭의 목적은 명시하지만 개별적으로 캡쳐하거나 숫자를 붙이지는 않는다.)
comment = re.compile(r'/\*((?:.|\n)*?)\*/')
res = comment.findall(text1)
print(res)  # [' this is a comment ']
res = comment.findall(text2)
print(res)  # [' this is a\n            multiline comment ']

