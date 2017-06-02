                    #Chapter 5 파일과 입출력

# 5.1 텍스트 데이터 읽고 쓰기 
with open('somefile.txt', 'rt') as f:
    data = f.read()
    
with open('somefile.txt', 'rt') as f:
    for line in f:
        #
        ..
        
with open('somefile.txt', 'wt') as f:
    f.write(text1)
    f.write(text2)
    

#5.2 파일에 출력

with open('somefile.txt', 'rt') as f:
    print('Hello World', file=f)
    
    
#5.3 구별자나 종단 부호 바꾸기

print('ACME', 50, 91.5)
print('ACME', 50, 91.5, sep=',')
print('ACME', 50, 91.5, sep=',', end='!!\n')

for i in range(5):
    print(i)
    
for i in range(5):
    print(i, end=' ')
    

#5.4 바이너리 데이터 읽고 쓰기

with open('somefile.bin', 'rb') as f:
    data= f.read()
    

with open('somefile.bin', 'wb') as f:
    f.write(b'Hello World')
    

#5.5 존재하지 않는 파일에 쓰기

with open('somefile','wt') as f:
    f.write('Hello\n')
    
    
with open('somefile','xt') as f:
    f.write('Hello\n
    
        
# 5.6 문자열에 입출력 작업하기

s= io.StringIO()
s.write('Hello World\n')

print('This is a test', file=s)

s.getvalue()

s=io.StringIO('Hello\nWorld\n')
s.read(4)
s.read()

s= io.BytesIO()
s.wrtie(b'binary data')
s.getvalue()


#5.7 압축된 데이터 파일 읽고 쓰기

import gzip
with gzip.open('somefile.gz', 'rt') as f:
    text = f.read()
    
import bz2
with bz2.open('somefile.bz2', 'rt') as f:
    text = f.read()


import gzip
with gzip.open('somefile.gz', 'wt') as f:
    f.write(text)
    
import bz2
with bz2.open('somefile.bz2', 'wt') as f:
    f.write(text)
    

#5.8 고정 크기 레코드 순환

from functools import partial
RECORD_SIZE = 32
with open('somefile.data', 'rb') as f:
    records = iter(partial(f.read, RECORD_SIZE), b'')
    for r in records:
        ...
        
#5.9 바이너리 데이터를 수정 가능한 버퍼에 넣기

import os.path
def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return buf

#5.10 바이너리 파일 메모리 매핑
import os
import mmap

def memory_map(filename, access=mmap.ACCESS_WRITE):
    size=os.path.getsize(filename)
    fd = os. open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)

size = 1000000
with open('data', 'wb') as f:
    f.seek(size-1)
    f.write(b'\x00')

m= memory_map('data')
len(m)

m[0:10]
m[0]
m[0:11] = b'Hello World'
m.close()

with open('data', 'rb') as f:
    print(f.read(11))
    
b'Hello World'

with memory_map('data') as m:
    print(len(m))
    print(m[0:10])


m.closed


#5.11 경로 다루기

import os
path = '/Users/beazley/Data/data.csv'

os.path.basename(path)
'data.csv'

os.path.dirname(path)
'/Users/beazley/Data'

os.path.join('tmp', 'data', os.path.basename(path))
'tmp/data/data.csv'

path = '~/Data/data.csv'
os.path.expanduser(path)
'/Users/beazley/Data/data.csv'

os.path.splitext(path)


#5.12 파일 존재 여부 확인

import os
os.path.exists('/etc/passwd')
os.path.exists('/tmp/spam')

os.path.isfile('/etc/passwd') 
os.path.isdir('/etc/passwd')        
os.path.islink('/usr/local/bin/python3')
os.path.realpath('/usr/local/bin/python3')

os.path.getsize('/etc/passwd')
os.path.getmtime('/etc/passwd') 
import time
time.ctime(os.path.getmtime('/etc/passwd'))


#5.13 디렉터리 리스팅 구하기

import os
names = os.listdir('somedir')

import os.path

names = [name for name in os.listdir('somedir')
         if os.path.isfile(os.path.join('somedir', name))]

dirnames = [name for name in os.listdir('somedir')
            if os.path.isdir(os.path.join('somedir', name))]

pyfiles = [name for name in os.listdir('somedir')
           if name.endwith('.py'):
               
import glob
pyfiles = glob.glob('somedir/*.py')

from fnmatch import fnmatch
pyfiles = [name for name in os.listdir('somedir')
           if fnmatch(name, '*.py')]