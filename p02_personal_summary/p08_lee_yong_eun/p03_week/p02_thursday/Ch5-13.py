##########################################################################################################
# 5.13] 디렉터리 리스팅 구하기
#   * 디렉터리나 파일 시스템 내부의 파일 리스트를 구하고 싶다.
#     : os.listdir() : 디렉터리 내 파일 리스트 얻기
#       os.path나 문자열의 startswith/endswith 함수를 이용해 원하는 파일만 얻어낼 수 있다.
#       glob이나 fnmatch 모듈도 파일명 매칭에 유용하다.
#       만약 파일의 메타데이터들도 얻고 싶다면 os.path 모듈의 추가적인 함수나 os.stat() 함수를 사용한다.
##########################################################################################################
import os

# 디렉터리 내 파일 리스트 얻기
names = os.listdir('.')
print(names)    # ['Ch5-1.py', 'Ch5-11.py', 'Ch5-12.py', 'Ch5-13.py', 'Ch5-14.py', ... ]

import os.path
# 일반 파일 모두 구하기
names = [name for name in os.listdir('C:/Users/MK-K/Desktop/')
         if os.path.isfile(os.path.join('C:/Users/MK-K/Desktop/', name))]

# 디렉터리 모두 구하기
dirnames = [name for name in os.listdir('C:/Users/MK-K/Desktop/')
            if os.path.isdir(os.path.join('C:/Users/MK-K/Desktop/', name))]

print(names)    # ['.bash_profile', '3DP_Chip_v1511.exe', 'CDSpace8.lnk', 'desktop.ini', 'Discord.lnk', ... ]
print(dirnames) # [] (없음)

## startswith()와 endswith()를 이용한 디렉터리 내용 걸러내기
pyfiles = [name for name in os.listdir('.')
           if name.endswith('.py')]

## glob / fnmatch 모듈을 이용한 파일 매칭
import glob
pyfiles = glob.glob('somedir/*.py')

from fnmatch import fnmatch
pyfiles = [name for name in os.listdir('somedir')
           if fnmatch(name, '*.py')]

