##########################################################################################################
# 5.7] 압축된 데이터 파일 읽고 쓰기
#   * gzip이나 bz2로 압축된 파일을 읽거나 써야 한다.
#    : gzip, bz2 모듈 사용
##########################################################################################################
import gzip
import bz2

## 읽기
with gzip.open('s.gz', 'rt') as f:
    text = f.read()

with bz2.open('s.bz2', 'rt') as f:
    text = f.read()

## 쓰기
# compresslevel : 압축률. 디폴트는 9로 가장 높다. 레벨을 내리면 속도는 더 빠르지만 압축률이 떨어진다.
with gzip.open('s.gz', 'wt', compresslevel=5) as f:
    f.write(text)

## gzip과 bz2 모듈이 파일 같은 객체와 함께 작업하도록 하는 방법
f = open('s.gz', 'rb')
with gzip.open(f, 'rt') as g:
    text = g.read()