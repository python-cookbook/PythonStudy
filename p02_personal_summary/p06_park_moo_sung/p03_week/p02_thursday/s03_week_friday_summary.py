###########################################################

# 5.1 텍스트 데이터 읽고 쓰기

# 서로 다른 인코딩 쓸 때


with open('file.txt', 'rt') as f: # 파일 전체를 하나의 문자열로 읽기
    data = f.read()

with open('file.txt', 'rt') as f: # 파일의 줄을 불러오기
    for line in f :
        print(line)

with open('file.txt', 'wt') as f: # 데이터 쓰기
    f.write(text1)
    f.write(text2)

with open('file.txt', 'wt') as f:  # 데이터 쓰기
    print(line1, file=f)
    print(line2, file=f)

# 텍스트 인코딩 종류

    # UTF-8 : 웹 애플리케이션
    # ascii : 7비트 문자?
    # latin-1 : 255 바이트 ? --> 절대 에러가 발생하지 않음

# with 문 안 쓸 때 주의사항 : close() 꼭 해야 함


############################################################

# 5.2 파일에 출력

# print 결과를 파일로 출력하고 싶다면?

with open('file.txt', 'rt') as f:
    print('hello world', file=f)

############################################################

# 5.3 구별자나 종단 부호 바꾸기

# print() 에 sep 과 end 키워드 인자 사용

print('ACME', 50, 91.5)
## ACME 50 91.5
print('ACME', 50, 91.5, sep=',')
## ACME,50,91.5
print('ACME', 50, 91.5, sep=',', end='!!\n')
## ACME,50,91.5!!

# 또다른 활용법

for i in range(5):
    print(i, end = '  ')
## 0 1 2 3 4

# join() : 문자열에만 작동함! 주의하기

##############################################################

# 5.4 바이너리 데이터 읽고 쓰기

# open() 함수 + rb, wb 모드 사용하기

with open('fiel.bin', 'rb') as f:
    data = f.read()

with open('fiel.bin', 'wb') as f:
    f.write(b'Hello World')

# 텍스트 문자열과 바이너리 문자열의 차이 : 인덱스, 순환으로 반환한 값은 바이트 문자열이 아닌 정수 바이트 값이 됨....??

# 바이너리 모드 -> 텍스트 읽고 쓰려면? 인코딩, 디코딩 필요

with open('file.bin', 'rb') as f:
    data = f.read(16)
    text = data.decode('utf-8')

with open('file.bin', 'wb') as f:
    text = 'hello world'
    f.write(text.encode('utf-8'))

#######################################################################

# 5.5 존재하지 않는 파일에 쓰기

# open() + x 모드

with open('file', 'xt') as f:
    f.write('hello\n')

# 파일 덮어쓰기 피하는 방법

import os
if not os.path.exists('file'):
    with open('file', 'wt') as f:
        f.write('hello\n')
else:
    print('File already exists!')

##################################################################

# 5.6 문자열에 입출력 작업하기

# 객체에 동작하도록 작성한 코드에 텍스트나 바이너리 문자열을 제공하려면? (무슨 말이지?)

import io
s = io.StringIO() # 텍스트에만 사용해야 함(바이너리 데이터 다룰때는 io.BytesIO() 클래스 사용)
s.write('hello world\n')
## 12
print('this is a test', file=s)
## 15
s.getvalue() # 기록한 모든 데이터 얻기
## 'hello world\nthis is a test\n'
s= io.StringIO('hello\nworld\n') # 기존 문자열을 파일 인터페이스로 감싸기
s.read(4)
## hell
s.read()
## o\nworld\n

##################################################################

# 5.7 압축된 데이터 파일 읽고 쓰기

# gzip, bz2 파일 읽으려면?

## gzip 압축 읽기
import  gzip
with gzip.open('file.gz', 'rt') as f:
    text = f.read()

## bz2 압축 읽기
import bz2
with bz2.open('file.bz2', 'rt') as f:
    text = f.read()

## gzip 압축 쓰기
import gzip
with gzip.open('file.gz','wt') as f:
    f.write(text)

## bz2 압축 쓰기
import bz2
with bz2.open('file.bz2','wt') as f:
    f.write(text)

###################################################

# 5.8 고정 크기 레코드 순환

# iter(), functiools.partial()

from functools import partial
RECORD_SIZE = 32
with open('file.data', 'rb') as f:
    records = iter(partial(f.read, RECORD_SIZE), b'')
    for r in records:

###################################################

# 5.9 바이너리 데이터를 수정 가능한 버퍼에 넣기

# readinto()

import os.path

def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return buf

with open('sample.bin', 'wb') as f:
    f.write(b'hello world')

buf = read_into_buffer('sample.bin')
print(buf)
## bytearray(b'hello world')

buf[0:5] = b'hello'
print(buf)
## bytearray(b'hallo world')
with open('newsample.bin' ,'wb') as f:
    f.write(buf)
print(11)

# 불필요한 메모리 할당 피하기(레코드 크기가 고정적인 바이너리 파일 읽을 때)

record_size = 32 # 레코드의 크기(값 조절)

buf = bytearray(record_size)
with open('somefile','rb') as f:
    while True:
        n=f.readinto(buf)
        if n < record_size:
            break # buf 내용을 사용

# 메모리뷰

m1 = memoryview(buf)
m2 = m1[-5:]
m2[:] = b'world'
print(buf)
## bytearray(b'hello world')

###########################################################

# 5.11 경로 다루기

# os.path

import os
path = '/Users/beazley/data/data.csv'

# 경로의 마지막 부분 구하기
os.path.basename(path)

# 디렉터리 이름 구하기
os.path.dirname(path)

# 각 부분 합치기
os.path.join('tmp','data',os.path.basename(path))

# 사용자의 홈 디렉터리 펼치기
path = '~/data/data.csv'
os.path.expanduser(path)

# 파일 확장자 나누기
os.path.splitext(path)

#####################################################

# 5.12 파일 존재 여부 확인

# os.path

import os
os.path.exists('/etc/passwd')
## True or False

# 파일 종류 확인

## 일반 파일인지
os.path.isfile('/etc/passwd')

## 디렉터리인지
os.path.isdir('/etc/paswd')

## 심볼릭 링크인지
os.path.islink('/usr/local/bin/python3')

## 연결된 파일 얻기
os.path.realpath('/usr/local/bin/python3')

# 메타데이터(파일크기, 수정날짜) 필요한 경우

os.path.getsize('/etc/passwd')

os.path.getmtime('/etc/passwd')

import time
time.ctime(os.path.getmtime('/etc/passwd'))

##################################################

# 5.13 디렉터리 리스팅 구하기

# 디렉터리 내 파일 리스트 얻기

import os
names = os.listdir('somedir')

# 일반 파일 모두 구하기
import os.path
names= [name for name in os.listdir('somedir') if os.path.isfile(os.path.join('somedir', name))]

# 디렉터리 모두 구하기
dirnames = [name for name in os.listdir('somedir') if os.path.isdir((os.path.join('somedir', name)))]

# startwith(), endswith()
pyfiles = [name for name in os.listdir('somedir') if name.endswith('.py')]

# fnmatch, glob
import glob
pyfiles = glob.glob('somedir/*.py')

from fnmatch import fnmatch
pyfiles = [name for name in os.listdir('somedir') if fnmatch(name, '*.py')]

# 디렉터리 리스트 구하기
import os
import os.path
import glob

pyfiles = glob.glob('*.py')

# 파일 크기와 수정 날짜 구하기

name_sz_date = [(name, os.path.getsize(name), os.path.getmtime(name)) for name in pyfiles]

for name, size, mtime in name_sz_date:
    print(name, size, mtime)

# 대안 : 파일 메타 데이터 구하기 
file_metadata = [(name, os.stat(name)) for name in pyfiles]
for name, meta in file_metadata:
    print(name, meta.st_size, meta.st_mtime)







