##########################################################################################################
# 5.12] 파일 존재 여부 확인
#   * 파일이나 디렉터리가 존재하는지 확인해야 한다.
#     : os.path 모듈 사용
#       (파일 테스팅 가능, 파일 접근 권한 주의)
##########################################################################################################
import os

# 파일이나 디렉터리가 존재하는지 여부 확인
print(os.path.exists('/etc/passwd'))    # False
print(os.path.exists('/tmp/spam'))

## 파일의 종류가 무엇인지 확인할 수 있다. 파일이 없는 경우에도 False 반환
# 일반 파일인지 확인
print(os.path.isfile('Ch5-19.py'))  # True

# 디렉터리인지 확인
print(os.path.isdir('Ch5-1.py'))    # False

# 심볼릭 링크인지 확인
print(os.path.islink('C:/Users/MK-K/Desktop/Discord.lnk')) # False. Why?

# 연결된 파일 얻기
print(os.path.realpath('C:/Users/MK-K/Desktop/Discord.lnk'))

## 메타데이터 얻기
print(os.path.getsize('C:/Users/MK-K/Desktop/Discord.lnk')) # 2228

# 파일 수정 날짜
print(os.path.getmtime('C:/Users/MK-K/Desktop/Discord.lnk'))    # 1492653215.5703669

import time
print(time.ctime(os.path.getmtime('C:/Users/MK-K/Desktop/Discord.lnk')))    # Thu Apr 20 10:53:35 2017