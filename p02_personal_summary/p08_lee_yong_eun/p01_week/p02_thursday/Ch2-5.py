###############################################################################################
# 2.5] 텍스트 검색과 치환
#   * 문자열에서 텍스트 패턴을 검색하고 치환하고 싶다.
#
# 1] str.replace
#   : 간단한 패턴에 사용
#
# 2] re.sub()
#   : 더 복잡한 패턴에 사용
#
# 3] 작업 간소화 방법
#   3-1] 패턴 컴파일
#   3-2] 콜백 함수를 이용한 치환
#
# 4] re.subn()
#   : sub 함수의 기능을 수행하면서 치환이 일어난 횟수도 함께 받고 싶을 때 사용
###############################################################################################

## str.replace
text = 'yeah, but no, but yeah, but no, but yeah'
res = text.replace('yeah','yep')
print(res)  # yep, but no, but yep, but no, but yep

## re.sub()
import re

text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'

res = re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text) # 앞의 캡쳐 그룹 3개를 3,1,2 순으로 '3-1-2' 형태로 치환하겠다 !
print(res)  # Today is 2012-11-27. PyCon starts 2013-3-13.

## 패턴 컴파일을 통한 작업 간소화 및 성능 향상
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
res = datepat.sub(r'\3-\1-\2', text)
print(res)  # Today is 2012-11-27. PyCon starts 2013-3-13.

## 콜백 함수를 통한 치환
from calendar import month_abbr

def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))

res = datepat.sub(change_date,text)
print(res)  # Today is 27 Nov 2012. PyCon starts 13 Mar 2013.

## re.subn()
res, n = datepat.subn(r'\3-\1-\2',text)
print(res)  # Today is 2012-11-27. PyCon starts 2013-3-13.
print(n)    # 2