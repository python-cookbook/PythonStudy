"""
Cahp05 파일과 입출력

여러 조율의 파일을 다루는 방법을 다루는 챕터이다.
파일이름 또는 디렉터리 수정하는 방법도 다룬다.
"""

"""
    5.1 텍스트 데이터 읽고 쓰기
    
        텍스트 데이터 읽거나 써야하는 상황에서 
        ASCII,UTF-8,UTF-16 과 같이 서로 다른 인코딩을 사용해야 하는 경우
"""

print('5.1 텍스트 데이터 읽고 쓰기')

# 텍스트파일을 읽기 위해 open()함수에 rt모드를 사용 한다.


# with oepn('somefile.txt', 'rt') as f:     #파일 전체를 하나의 문자열로 읽어버린다.
#     data = f.read()


# with open('somefile.txt','rt') as f:      #파일의 줄을 순환한다.
#     for line in f:
#         #                                 #라인처리


print(24%16)
print(16%8)

# 텍스트 파일을 쓰는 모드 중 wt모드가 있다.
# wt모드는 기존 내용이 있으면 덮어쓰기 저장을 한다.


# with open('somefile.txt','wt') as f:      # 텍스트 데이터 쓰기
#     f.write(text1)
#     f.write(text2)


# with open('somefile.txt','wt') as f:      # 리다이렉트한 print 문
#     print(line1, file =f)
#     print(line2, file =f)



#파일의 끝에 내용을 추가하려면 at 모드로 open() 사용한다.
#기본적으로 파일을 읽고 쓸때 sys.getdefaultencoding()으로 확인 할 수 있는
#시스템을 기본 인코딩으로 사용한다. 대부분은 utf-8 사용함
#텍스트가 다른 인코딩 사용한다면, open에 추가옵션으로 encoding인자를 전달한다.



# with open('aa.txt', 'at', encoding='latin-1') as f:
#     ...



# 파이썬이 이해할 수 있는 인코딩의 종류는 수백가지 이며
# 주로 사용하게 될건 ascii, latin-1, utf-8, utf-16 일 것이다.
# UTF-8이 가장 안전하다.






####################주의 사항 #######################

# 1) with문에서 open한게 아니라면, 반드시 close()를 하라!

    # with 문은 파일을 사용할 콘텍스트를 생성한다.
    # 컨트롤이 with문의 블록을 벗어나면 파일이 자동으로 닫힌다.
    # 반드시 with 문을 사용하지 않아도 되지만, 그럴때는 반드시 파일을 닫아야 한다.

    # f = open('somefile.txt','rt')
    # data = f.read()
    # f.close()


# 2) Unix와 Windows의 서로 다른 줄바꿈 문자에 주의하라!
    # \n과   \r\n
    # 기본적으로 파이썬은 보편적 줄바꿈 모드로 동작한다.
    # 줄바꿈 변환 없이 읽기동작을 원한다면 open()안에 newline=''인자를 넣어라.

    # with open('aa.txt','rt', newline='') as f:
    #     ...


# 3)UNIX 컴퓨터와 WINDOWS형식으로 인코딩된 텍스트 파일을 읽어보겠다.

    #줄바꿈 변환 사용(기본)
    # f = open('hello.txt','rt')
    # f.read()



# 4) 마지막으로 텍스트 파일의 인코딩 에러 주의해야한다.

# f = open('samplex.txt', 'rt', encoding='ascii')
# f.read()
#UnicodeDecodeError: 'ascii' codec can't decode byte..


# 일반적인 에러 처리 방식의 예

# f = open('samlex.txt','rt', encoding='ascii', errors='replace')
# f.read()

# 알 수 없는 문자를 무시

# g = open('sample.txt', 'rt', encoding='ascii', errors='ignore')   << 에러 무시!!






"""
    5.2 파일에 출력
        
        print() 함수의 결과를 파일에 출력하고 싶다?!!?
        
        
        파일에 출력하기에서 이 이상의 내용은 없다. 
        하지만 파일을 텍스트모드로 열었는지 꼭 확인해야 한다.
        바이너리 모드로 파일을 열면 출력에 실패한다.
        
"""

print('5.2 파일에 출력')




"""
    5.3 구별자 or 종단 부호 바꾸기

    print()를 사용해 데이터를 출력할 때 구분자나 종단부호 ( line ending) 을 바꾸고 싶다.
     

"""

print('5.3 구별자 or 종단 부호 바꾸기')

#print() 에 sep과 end 키워드 인자를 사용한다.



print('ACME',50,91.5)
print('ACME',50,91.5,sep=',')
print('ACME',50,91.5,sep=',',end='!!\n')

#출력의 개행 문자(newline) 를 바꿀 때도 end 인자를 사용한다.

for i in range(5):
    print(i)

for i in range(5):
    print(i, end=' ')
    print('워우')


#print() 로 출력 시, 아이템을 구분하는 문자를 스페이스 공백문 이외로 바꾸는 가장 쉬운 방법은 구별자로 지정하는 것이다.
#어떤 프로그래머는 동일한 목적으로 str.join() 을 사용하기도 한다.

# print(','.join('ACME','50','91.5'))

#하지만 str.join() 은 문자열에만 동작한다는 문제점이 있다.
# 문자열이 아닌 데이터에 사용하려면 귀찮은 작업을 먼저 적용해야 할지도 모른다.
# 다음과 같이한다.

row = ('ACME',50, 91.5)
# print(','.join(row))


print(*row, sep=',')

"""
    5.4 바이너리 데이터 읽고 쓰기 
    
    이미지 또는 사운드 파일 등 바이너리 데이터를 읽고 써야 한다!
    
    
    >> open() 함수에 rb와 wb 모드를 사용해서 바이너리 데이터를 읽거나 쓴다.
    

"""

print('5.4 바이너리 데이터 읽고 쓰기')


# 파일 전체를 하나의 바이트 문자열로 읽기.

# with open('d:/data/winter.txt','rb') as f:
#     data = f.read()
#     # print(data)
#
# # 바이너리 데이터 파일에 쓰기
#
# with open('some.bin', 'wb') as f:
#     f.write(b'Hello World')

# 바이너리 읽을 때,반환된 모든 데이터가 텍스트 문자열 형식이 아니라, 바이트 문자열 형식이 된다는 점을 기억해야해요 ㅠㅠ
# 마찬가지로 뭐 데이터 쓸 때도 바이트로 표현할 수 있는 형식의 객체를 제공해야 합니다.
# ex ) 바이트 문자열 / bytearray 객체 등..



# 바이너리 데이터를 읽을 때, 바이너리 문자열과 텍스트 문자열 사이에 미묘한 문법 차이가 있다.
# 자세히 말하면 데이터에 인덱스나 순환으로 반환한 값은 바이트 문자열이 아닌, 정수 바이트 값이 된다.


# 텍스트 문자열
# t = 'Hello World'
# print(t[0])
# for c in t:
#     print(c)
#
#
# #바이트 문자열
# b=b'Hello World'
# print(b[0])
# for c in b:
#     print(c)


# # 바이너리 모드 파일로부터 텍스트를 읽거나 쓰려면 인코딩이나 디코딩 과정이 꼭 필요하다.
#
# with open('somefile.bin', 'rb') as f:
#     data = f.read(16)
#     text = data.decode('utf-8')
#
# with open('somefile.bin','wb') as f:
#     text = 'Hello World'
#     f.write(text.encode('utf-8'))

#바이너리 입출력 시 잘 알려지지 않은 기능으로, 배열이나 C 구조체와 같은 객체를
# 바이츠로 객체로 변환하지않고 바로 쓸 수 있다는 점이다.
#
# import array
# nums = array.array('i',[1,2,3,4])
# with open('data.bin','wb') as f:
#     f.write(nums)


#이 기능은 소위 "버퍼 인터페이스"로 구현되어 있는 객체에 모두 적용된다.
#이런 객체는 기반 메모리 버퍼를 바로 작업에 노출시켜 작업이 가능하다.
#바이너리 데이터를 쓰는 것도 이런 작업의 일종이다.

# 또한 파일의 readinto() 메소드를 사용하면 여러 객체의 바이너리 데이터를 직접 메모리에 읽어 들일 수 있다.

#
# import array
# a = array.array('i',[0,0,0,0,0,0,0,0,0])
# with open('data.bin', 'rb') as f:
#     f.readinto(a)
#
#     #16
#
#
#
#




"""
    5.5 존재하지 않는 파일에 쓰기 

    파일이 파일 시스템에 존재하지 않을 때, 데이터를 파일에 쓰고 싶다.
    
    이 문제는 open()에 x모드를 사용해서 해결할 수 있다. x모드와 다르게 x모드는 잘 알려져 있지 않다.

"""

print('5.5 존재하지 않는 파일에 쓰기')

# with open('somefile','wt') as f:
#     f.write('Hello\n')
#
#
# with open('somefile', 'wt') as f:
#     f.write('Hello\n')   #FileExistsError:  ... file exists..




# 이 레시피는 파일을 쓸 때, 발생할 수 있는 문제점 (실수로 파일을 덮어 쓰는 등) 을 아주
# 우아하게 피해 가는 법을 알려준다. 혹은 파일을 쓰기 전에 파일이 있는지 확인하는 방법도 있다.



"""
    
    5.6 문자열에 입출력 작업하기
    파일 같은 객체에 동작하도록 작성한 코드에 텍스트나 바이너리 문자열을 제공하고 싶다.
    io.StringI0() 와 io.BytesIO() 클래스로 문자열 데이터에 동작하는 파일 같은 객체를 생성한다.
"""

print('5.6 문자열에 입출력 작업하기')

#
# s = io.StringIO()
# s.write('Hello World\n') #12
# print('This is a test', file=s)  #15

#기록한 모든 데이터 얻기
# s.getvalue()



#일반 파일 기능을 흉내 내려 할때 stringIO와 bytesIO클래스가 가장 유용하다.
#file, pipe socket 등 실제 시스템 레벨 파일을 요구하는 코드에는 사용할 수 없다.


"""

    5.7 압축된 데이터 파일 읽고 쓰기
    gzip 나 bz2로 아북한 파일을 읽거나 써야한다.
    
"""

print('5.7 압축된 데이터 파일 읽고 쓰기')

#gzip모듈 / bz2 모듈 사용하면 해결 가능
#open 명령어의 대안책이 될 수 있음.


#gzip 압축

# import gzip,bz2
# with gzip.open('somefile','rt') as f:
#     text = f.read()
#
# #bz2 압축
# with bz2.open('somefile.bz2','rt') as f:
#     text = f.read()


#앞에서 살펴본 대로, 모든 입출력은 텍스트를 사용하고 유니코드 인코딩/디코딩 을 수행한다.
#바이너리 데이터를 원하면 rb 또는 wb 모드 사용하도록 하자.


#압축한 데이터를 읽거나 쓰기가 어려운건 아니다.
# 하지만 올바른 파일 모드를 선택하는 것은 상당히중요하다.
# 모드를 명시하지 않으면, 기본적으로 '바이너리 모드'
# 텍스트파일 받을것이라고 가정한 프로그램엔 문제가 발생!
# gzip.open()과 bz2.open은 인코딩/에러,뉴라인/ 과 같이 내장함수와 동일한 인자를 받는다.


# with gzip.open('somfile.gz','wt', compresslevel=5) as f:  #compresslevel --_> 압축률
#     f.write(text)


##### 기본 레벨은 9로, 가장 높은 압축률을 가리킨다.
# 레벨을내리면 속도는 빠르지만, 압축률은 떨어진다.

#두 라이브러리를 기존에 열려있는 바이너리 파일의 상위에 위치시키기


# import gzip
# f = open('some.gz', 'rb')
# with gzip.open(f, 'rt' ) as g:
#     text = g.read()
#
"""

    5.8 고정 크기 레코드 순환
    
    파일을 줄 단위로 순환하지 않고, 크기를 지정해서 그 단위별로 순환하고 싶다.

"""

print('5.8 고정 크기 레코드 순환')


#iter함수와 functools.partial() 사용

from functools import partial

RECORD_SIZE = 32

# with open('some.data', 'rb') as f:
#     rec = iter(partial(f.read, RECORD_SIZE), b'')
#     for r in rec:
#         ..


# 이 예제는 records 객체는 파일의 마지막에 도달할 때 까지 고정 크기 데이터를 생산하는 순환객체이다.
# 그러나, 파일의 크기가 지정한 크기의 정확한 배수가 아닌 경우 마지막 아이템의 크기가 예상보다 작을 수 있다.


#iter() 함수에 잘 알려지지 않는 기능으로,
#  1)호출 가능 객체와   2) 종료 값
# 을 전달하면 이터레이터를 만드는 것이 있다.
# 그 이터레이터는 제공 받은 호출 가능 객체를 반복적으로 호출하며 종료 값을 반환할 때 순환을 멈춘다.
# 이 해결책에서 partial 로 파일에서 고정크기바이트를 읽어 호출 가능 객체를 생성했다.
#


"""

    5.11 경로 다루기

    기본 파일 이름, 디렉터리 이름, 절대경로 등을 찾기 위해 경로를 다루어야 한다.


    경로를 다루기 위해선 os.path 함수를 사용한다. 
    몇몇 기능을 예제를 통해 살펴보자.
    
"""

print('5.11 경로 다루기')


import os
path = 'd:/data/eno.csv'
#경로의 마지막 부분 구하기
print(os.path.basename(path))     #eno.csv

# 디렉터리 이름 구하기
print(os.path.dirname(path))  #d:/data


#각 부분을 합치기

print(os.path.join('tmp','data', os.path.basename(path)))  #tmp\data\eno.csv


# 사용자의 홈 디렉터리 펼치기

path = '~/Data/data.csv'
print(os.path.expanduser(path))  #C:\Users\sru/Data/data.csv




# 파일 확장자 나누기
print(os.path.splitext(path))  #('~/Data/data', '.csv')




#파일 이름을 다루기 위해서 문자열에 관련된 코드를 직접 작성하지 말고,
# os.path 모듈을 사용 해야 한다.
# 이는 이식성과도 어느 정도 관련이 있다.
#os.path 모듈은 유닉스와 윈도우의 차이점을 알고, /이거랑 \이거랑 차이점을 자동으로 처리한다.
#최대한 기능있는건 써먹는게 낫다.





"""

    5.12 파일 존재 여부 확인

    파일이나 디렉토리가 존재하는지 확인해야 한다.

    
"""

print('5.12 파일 존재 여부 확인')


# 파일이나 디렉토리의 존재 여부를 확인하기 위해서 os.path 모듈을 사용한다.

import os

print(os.path.exists('/etc/passwd'))    #False
print(os.path.exists('/tmp/spam'))      #False  이거 갓코드인듯.. 있다..없다...없으면? 저장해라..써먹을 수 있겠다.


#추가적으로 파일의종류가 무엇인지 확인할 수 있다. 다음 코드에서 파일이 없는 경우 False를 반환한다.

# 일반 파일인지 확인
print(os.path.isfile('/etc/passwd'))

#디렉토리인지 확인
print(os.path.isdir('/etc/passwd'))

#심볼릭 링크인지 확인
print(os.path.islink('/etc/passwd'))

#연결된 파일 얻기
print(os.path.realpath('/usr/local/bin/python3'))  #D:\usr\local\bin\python3


#메타데이터 (파일 크기, 수정날짜) 등이 필요할 때도 os.path 모듈을 사용한다.

print(os.path.getsize('d:/data/emp.csv'))  # 749   749바이트겠지아마
print(os.path.getmtime('d:/data/emp.csv'))  #1492500899.0708685  #수정날짜

import time

print(time.ctime(os.path.getmtime('d:/data/emp.csv')))  #Tue Apr 18 16:34:59 2017  #시간변환 / 초변환 / 타임모듈


# os.path 를 사용하면 파일 테스팅은 그리 어렵지 않다. 유의해야 할 점은 아마도 파일 권한에 관련된 것 뿐이다.
# 특히 메타데이터에 접근할 때는 권한에 주의해야 한다.

# print(os.path.getsize('메타데이터'))   #PermissionError











"""

    5.13 디렉터리 리스팅 구하기

    디렉터리나 파일 시스템 내부의 파일 리스트를 구하고 싶다.


"""

print('5.13 디렉터리 리스팅 구하기')


#os.listdir() 함수로 디렉터리 내에서 파일 리스트를 구하고 싶다.

import os
names = os.listdir('somedir')

#이렇게 하면 디렉터리와 파일, 서브디렉터리, 심볼릭 링크 등 모든 것을

import os.path

#일반 파일 모두 구하기
# names = [name for name in os.listdir('somedir')
#          if os.path.isfile(os.path.join('somedir',name)) ]

#디렉터리 모두 구하기
# dirnames = [name for name in os.listdir('somedir')
#             if os.path.isdir(os.path.join('somedir',name))
#             ]
#
# #문자열의 startswith()와 endswith() 메소드를 사용하면 디렉터리의 내용을 걸러 내기 유용하다.
# pyfiles = [name for name in os.listdir('somedir')
#            if name.endswith('.py') ]



import glob
import os.path
import os


p = glob.glob('somdir/*.py')

from fnmatch import fnmatch
pn = [name for name in os.listdir('somedir') if fnmatch(name, '*.py')]

# 파일 크기와 수정 날짜 구하기

# name_sz_date = [(name, os.path.getsize(name), os.path.getmtime(name) for name in pyfiles)]

for name, size, mtime in name_sz_date:
    print(name,size,mtime)

#대안 : 파일 메타데이터 구하기

# file_metadata = [(name, os.stat(name)) for name in pyfiles]
# for name, meta in file_metadata:
#     print(name, meta.st_size, meta.st_mtime)

