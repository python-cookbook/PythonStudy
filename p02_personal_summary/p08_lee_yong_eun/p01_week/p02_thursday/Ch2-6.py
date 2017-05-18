###############################################################################################
# 2.6] 대소문자를 구별하지 않는 검색과 치환
#   * 텍스트를 검색하고 치환할 때 대소문자를 구별하고 싶지 않다.
#
# 1] re.IGNORECASE 플래그 지정
#   : 유니코드가 포함된 작업을 하기에는 부족할 수 있다. 이는 2.10 참조
###############################################################################################
import re

## re.IGNORECASE 사용
text ='UPPER PYTHON, lower python, Mixed Python'
res = re.findall('python', text, flags=re.IGNORECASE)
print(res)  # ['PYTHON', 'python', 'Python']

# snake로 치환, 대소문자가 유지되지 않는다.
res = re.sub('python', 'snake', text, flags=re.IGNORECASE)
print(res) # UPPER snake, lower snake, Mixed snake


## 대소문자가 유지되도록 콜백 함수 생성
# 함수를 반환하는 형태를 유지하면서도 변수(word)를 전달하기 위해 함수 내에 함수를 정의하였다 !
def matchcase(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
    return replace

res = re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE)
print(res)  # UPPER SNAKE, lower snake, Mixed Snake

