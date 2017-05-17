###############################################################################################
# 2.4] 텍스트 패턴 매칭과 검색
#   * 특정 패턴에 대한 텍스트 매칭이나 검색을 하고 싶다.
#
# 1] 간단한 텍스트 : str.find(), str.endswith(), str.startswith() 등 기본적인 문자열 메소드로 가능
# 2] 복잡한 매칭 : 정규 표현식, re 모듈 사용
#   * match : 문자열의 첫 부분이 주어진 표현식과 같은지 확인하여 저장. (group()으로 확인 가능)
#   * findall : 문자열 내의 주어진 표현식과 동일한 모든 부분을 list로 저장.
#   * finditer : 문자열 내의 주어진 표현식과 동일한 모든 부분을 iterator 형태로 반환
#       ex) for m in datepat.finditer(text):
################################################################################################

text = 'yeah, but no, but year, but no, but yeah'

## 기본 문자열 메소드 사용
# 정확한 매칭
text == 'yeah'  # False

# 처음이나 끝에 매칭
text.startswith('yeah') # True
text.endswith('no') # False

# 처음 나타난 곳 검색
text.find('no')  # 10

## 정규 표현식 사용
import re

text1 = '11/27/2012'
text2 = 'Nov 27, 2012'

# \d+는 하나 이상의 숫자를 의미
if re.match(r'\d+/\d+/\d+', text1): # text1이 '숫자/숫자/숫자'의 형태로 되어있는가?
    print('yes')    #ok
else:
    print('no')

# 동일 패턴으로 매칭을 많이 수행할 거라면 정규 표현식을 미리 컴파일해서 패턴 객체로 만들어두는 것이 좋다.
datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text2):
    print('yes')
else:
    print('no') #ok

# match는 문자열 처음부터 찾기를 시도한다. 문자열 전체에 걸쳐 패턴을 찾으려면 findall()을 사용!
text3 = 'Today is 11/27/2012. PyCon starts 3/13/2013'
print(datepat.findall(text3))   # ['11/27/2012', '3/13/2013']

# 캡처 그룹(match) : 괄호를 사용
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
m = datepat.match('11/27/2012')
print(m.group(0), m.group(1), m.group(2), m.group(3))   # 11/27/2012 11 27 2012
print(m.groups())   # ('11', '27', '2012')
month, day, year = m.groups()

m = datepat.findall('Today is 11/27/2012. PyCon starts 3/13/2013')
print(m)    # [('11', '27', '2012'), ('3', '13', '2013')]