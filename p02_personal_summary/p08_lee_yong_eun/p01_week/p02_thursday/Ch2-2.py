#######################################################################################
# 2.2] 문자열 처음이나 마지막에 텍스트 매칭
#   * 문자열의 처음이나 마지막에 파일 확장자, URL 스킴(scheme) 등 특정 텍스트 패턴이 포함되었는지 검사하고 싶다.
#
# 1] str.startswith() / str.endswith()
#   1-2] 여러 문자열에 대해 검사할 때의 사용법 (검사할 리스트를 인풋 : (())의 형태가 된다!
# 2] 정규식 사용(re.match)
#   : 문자열의 시작부분부터 조건에 맞는지 확인
#######################################################################################
import os

# startswith() / endswith()
filename = 'spam.txt'
print(filename.endswith('txt')) # True
print(filename.startswith('file:')) # False

url = 'http://www.python.org'
print(url.startswith('http:'))  # True

# 파일 여러 개에 대한 검사
filenames = os.listdir('./../Chap 1')
print(filenames)    # ['Ch1-1.py', 'Ch1-10.py', 'Ch1-11.py', 'Ch1-12.py', 'Ch1-13.py', 'Ch1-14.py', 'Ch1-15.py', 'Ch1-16.py', 'Ch1-17.py', 'Ch1-18.py', 'Ch1-19.py', 'Ch1-2.py', 'Ch1-20.py', 'Ch1-3.py', 'Ch1-4.py', 'Ch1-5.py', 'Ch1-6.py', 'Ch1-7.py', 'Ch1-8.py', 'Ch1-9.py', 'classmethodsExample.py', 'DequeExample.py', 'HeapExample.py', 'somefile.txt']

# filenames 중 '.txt'로 끝나는 값 반환
res = [name for name in filenames if name.endswith('.txt')]
print(res)  # ['somefile.txt']

# filenames 안에 '.py'로 끝나는 문자열이 있다면 True 반환
res = any(name.endswith('.py') for name in filenames)
print(res)  # True


# url 주소 체크
from urllib.request import urlopen

# http:, https:, ftp: 중 하나로 시작하면 url로 open, 그렇지 않으면 파일명으로 open
def read_data(name):
    if name.startswith(('http:', 'https:', 'ftp:')):
        return urlopen(name).read()
    else:
        with open(name) as f:
            return f.read()

# 정규식을 사용한 url 주소 체크
import re

url = 'http://www.python.org'
res = re.match('http:|https:|ftp:', url)
print(res.group())  # http:

# 디렉토리에 특정 확장자의 파일이 있는지 확인
if any(name.endswith(('.c', '.py')) for name in filenames):
    print('OK')

