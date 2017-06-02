##########################################################################################################
# 5.11] 경로 다루기
#   * 기본 파일명, 디렉터리명, 절대경로 등을 찾기 위해 경로를 다루어야 한다.
#       : os.path 모듈 사용
#
#   * 파일명을 다루기 위해서 문자열 관련 코드를 직접 작성하지 말고 os.path 모듈을 사용해야 한다.
#     이는 이식성과도 어느 정도 관련이 있다.(ex : unix와 windows (/,\)의 차이점 자동 처리)
#
##########################################################################################################
import os
path = '/Users/beazley/Data/data.csv'

# 경로의 마지막 부분 구하기
print(os.path.basename(path))   # data.csv

# 디렉터리명 구하기
print(os.path.dirname(path))    # /Users/beazley/Data

# 각 부분 합치기
print(os.path.join('tmp', 'data', os.path.basename(path)))  # tmp\data\data.csv

# 사용자의 홈 디렉터리 펼치기
path = '~/Data/data.csv'
print(os.path.expanduser(path)) # C:\Users\MK-K/Data/data.csv

# 파일 확장자 나누기
print(os.path.splitext(path))   # ('~/Data/data', '.csv')