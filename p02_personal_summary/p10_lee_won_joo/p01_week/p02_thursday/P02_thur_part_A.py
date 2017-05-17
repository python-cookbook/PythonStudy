
"""
문자열 나누기/검색/빼기/렉싱/파싱
대부분 파이썬 내장 메소드 해결가능
복잡한 경우 정규표현식 / 문자열 파서 작성
유니코드 핸들링
"""
emps = list()
emps.append( { 'empno':7839,'ename':'KING','job':'PRESIDENT','mgr':0,'hiredate':'81.11.17','sal':5000,'comm':0,'deptno':10 }  )
emps.append( { 'empno':7698,'ename':'BLAKE','job':'MANAGER','mgr':7839,'hiredate':'81.05.01','sal':2850,'comm':0,'deptno':30} )
emps.append( { 'empno':7782,'ename':'CLARK','job':'MANAGER','mgr':7839, 'hiredate':'81.05.09','sal':2450 ,'comm':0, 'deptno':10}  )
emps.append( { 'empno':7566,'ename':'JOneS', 'job':'MANAGER','mgr':7839, 'hiredate':'81.04.01','sal':2975,'comm':0 , 'deptno':20}  )
emps.append( { 'empno':7654,'ename':'MArtIN', 'job':'SALESMAN', 'mgr':7698, 'hiredate':'81.08.10','sal':1250,'comm':1400,'deptno':30}  )
emps.append( { 'empno':7499,'ename':'AlleN', 'job':'SALESMAN',  'mgr':7698, 'hiredate':'81.02.11','sal':1600,'comm':300,'deptno':30}  )
emps.append( { 'empno':7844,'ename':'TURNER', 'job':'SALESMAN', 'mgr':7698, 'hiredate':'81.08.21', 'sal':1500,'comm':0,'deptno':30}  )
emps.append( { 'empno':7900,'ename':'James', 'job':'CLERK',   'mgr':7698, 'hiredate':'81.12.11','sal':950,'comm':0,'deptno':30}  )
emps.append( { 'empno':7521,'ename':'WARD', 'job':'SALESMAN',  'mgr':7698, 'hiredate':'81.02.23','sal':1250,'comm':500,'deptno':30}  )
emps.append( { 'empno':7902,'ename':'FORD',  'job':'ANALYST',  'mgr':7566, 'hiredate':'81.12.11', 'sal':3000,'comm':0,'deptno':20}  )
emps.append( { 'empno':7369,'ename':'SMITH', 'job':'CLERK', 'mgr':7902, 'hiredate':'80.12.09', 'sal':800,'comm':0, 'deptno':20}  )
emps.append( { 'empno':7788,'ename':'SCOTT',  'job':'ANALYST', 'mgr':7566, 'hiredate':'82.12.22', 'sal':3000,'comm':0,'deptno':20}  )
emps.append( { 'empno':7876,'ename':'ADAMS', 'job':'CLERK', 'mgr':7788, 'hiredate':'83.01.23',  'sal':1100,'comm':0,'deptno':20}  )
emps.append( { 'empno':7934,'ename':'MILLER', 'job':'CLERK', 'mgr':7782, 'hiredate':'82.01.12 ','sal':1300,'comm':0,'deptno':10}  )

"""
▶ 2.1 여러 구분자로 문자열 나누기 ◀ 
♣ 문제 : 문자열을 필드로 나누고 싶지만, 구분자(그리고 그주변의 공백)가 문자열에 직관적이지 않다.
 ↘ 해결 : 문자열 객체의 split() 메소드는 아주 간단한 상황에 사용하도록 설계되었고, 여러개의 구분자나 구분자 주변의 공백까지는 고려하지
            않는다. 좀더 유연해져야 한다면?
            re.split() 메소드를 사용!
        
        re.split()
        str.split()
"""
print('########################################## 2.1 여러 구분자로 문자열 나누기 #####################################')



import re
line = 'asdf@ fjdk afed, fjek,asdf,      foo'


# (a) Splitting on space, comma, and semicolon
parts = re.split(r'[@;,\s]\s*', line) #['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
print(parts)

# re.spilt() 는 분리 구문마다 여러 패턴을 명시할 수 있어서 유리함. 앞의 코드에서 본대로 쉼표,세미콜론,공백문자 등을 분리구문으로 사용한 것
# 이 패턴이 나올 때마다 매칭된 부분 모두가 구분자가 된다. 결과는 str.split() 과 마찬가지로 필드 리스트가 된다.

fields = re.split(r'(;|,|\s)\s*', line)
print(fields)

# 출력문을 재구성하기 위해 필요한 경우

values = fields[::2]
delimiters = fields[1::2] + ['']
print(values)
print(delimiters)

# 동일한 구분자로 라인을 구성한다.
a = ''.join(v+d for v,d in zip(values, delimiters))
print(a)

# 논캡쳐 그룹

d = re.split(r'(?:,|;|\s)\s*',line)
print(d)

"""
▶ 2.2 문자열 처음이나 마지막에 텍스트 매칭 ◀ 
♣ 문제 : 문자열의 처음이나 마지막에 파일 확장자, URL 스킴()등 특정 텍스트 패턴이 포함되었는지 검사하고 싶다.
 ↘ 해결 : 문자열의 처음이나 마지막에 패턴이 포함되었는지 확인하는 간단한 방법
           str.startswith()
           str.endswith()
 
 
 """
print('########################################## 2.2 문자열 처음이나 마지막에 텍스트 매칭 #####################################')

# 단일 개의 패턴 검사
fname = 'spam.txt'
a = fname.endswith('.txt')  # return True
print(a)

b = fname.startswith('file:') # return False
print(b)

url = 'http://www.python.org'
d = url.startswith('http:')
print(d)

# 여러 개의 패턴 검색
# 검사하고 싶은 값을 튜플에 담고 >> startswith()나 endswith()에 전달한다.
import os
fnames = os.listdir('.')
print(fnames)  # ['P02_thur_part_A.py', '__init__.py']
e = [name for name in fnames if name.endswith(('.c','.py'))]   # endswith ( ('a','b','c')  ) 이렇게 넣어야됨
print(e)

f = any(name.endswith('.py') for name in fnames)   #return True
print(f)


# 다른 예제

from urllib.request import urlopen

def read_data(name):
    if name.startswith(('http:','https:','ftp:')):
        return urlopen(name).read()
    else:
        with open(name) as f:
            return f.read()

choices = ['http:','ftp:']
url = 'http://www.python.org'
# d = url.startswith(choices)  #TypeError: startswith first arg must be str or a tuple of str, not list
# print(d)
d = url.startswith(tuple(choices))  #return True
print(d)


# 위처럼 두 메소드는 접두어와 접미어 검사할 때 매우 편리함.
# slice도 비슷한 동작 가능하나, 코드의 가독성이 떨어짐
# 정규표현식으로 해보기
import re
url = 'http://python.org'
g = re.match('http:|https:|ftp:', url)
print(g) # <_sre.SRE_Match object; span=(0, 5), match='http:'>  이게 뭔뜻이지

# 디렉토리에 특정 파일이 있는지 확인하는 방법!!
import os
if any(name.endswith(('.c','.h','.py','.txt')) for name in os.listdir("d:/data/")):
    print('있긴 해요')


"""
▶ 2.3 쉘 와일드카드 패턴으로 문자열 매칭 ◀ 
♣ 문제 : Unix 셀에 사용하는 것과 동일한 와일드카드 패턴을 텍스트매칭에 사용하고 싶다. (ex : *.py, Dat[0-9]*csv등).
 ↘ 해결 : fnmatch 모듈에 두 함수 fnmatch()와 fnmatchcase()가 있다. 이 함수를 사용하면 앞에 나온 문제를 해결할 수 있다.
            사용법은 간단하다.

        fnmatch가 수행하는 매칭은 간단한 문자열 메소드의 기능과 정규 표현식의 중간쯤 위치하고 있다.
        데이터 프로세싱을 할 때 간단한 와일드카드를 사용할 생각이라면 이 함수를 사용하는 것이 괜찮은 선택
        
        파일 이름을 찾는것을 만든다면 glob모듈을 사용해야 한다! recipe 5.13    
 """
print('########################################## 2.3 쉘 와일드카드 패턴으로 문자열 매칭 #####################################')

from fnmatch import fnmatch, fnmatchcase
a = fnmatch('foo.txt', '*.txt')
b = fnmatch('foo.txt', '?oo.txt')
print(a)
print(b)

c = fnmatch('Dat45.csv','Dat[0-9]*')
print(c)
names = ['Dat1.csv','Dat2.csv','config.ini','foo.py']
e = [name for name in names if fnmatch(name, 'Dat*.csv')]
print(e)

#일반적으로 fnmatch()는 windows 파일시스템과 동일한 대소문자 구문 규칙을 따른다.
#
f = fnmatch('foo.txt','*.TXT') # 윈도우는 return True, 맥은 return False
print(f)

# 위 같이 시스템에 따라 결과가 다른게 싫으면, fnmatchcase() 를 사용하면 된다.

g = fnmatchcase('foo.txt','*.TXT') # 이 메소드는 지정한 소문자 혹은 대문자에 정확히 일치하는 것만 찾아냄.
print(g)                           # txt인데 조건을 .TXT로 줬다고 그거 또 신경쓴다고 false돌려줌 ㅡㅡ



# fnmatch는 파일 이름이 아닌, 데이터 프로세싱에도 사용할 수 있다.
#데이터 프로세싱에 사용해보기

from fnmatch import fnmatchcase as match
#주소 리스트
addresses = [
    '5412 N CLARK ST',
    '1060 W ADDISON ST',
    '1039 W GRANVILLE AVE',
    '2122 N CLARK ST',
    '4802 N BROADWAY',
]

#리스트 컴프리헨션으로 풀어보기

h = [addr for addr in addresses if match(addr,'* ST')]
i = [addr for addr in addresses if match(addr,'54[0-9][0-9] *CLARK*')]
print(h)
print(i)

# 1039얘 뽑아보기

k = [addr for addr in addresses if match(addr, '*0[0-9]* *GRANVILLE*')]
print(k)

"""
▶ 2.4 텍스트 패턴 매칭과 검색 ◀ 
♣ 문제 : 특정 패턴에 대한 텍스트 매칭이나 검색을 하고 싶다.
 ↘ 해결 : 매칭하려는 텍스트가간단하다면 find() 나 endswith()나 startswith()같은 문자열메소드도 충분하죠
        그런데 더 복잡한 매칭 하려면 정규표현식과 re모듈 사용한다.
        
        import re
        re.match(표현식,txt)
        a = re.compile(표현식)  >> a.match(txt)
        findall()
        finditer()
 """
print('########################################## 2.4 텍스트 패턴 매칭과 검색 #####################################')


text1 = '11/27/2012'
text2 = 'Nov 27, 2012'
import re

#간단한 매칭 :   \d+  는 하나 이상의 숫자를 의미

if re.match(r'\d+/\d+/\d+', text1):  # match
    print('matching!!')
else:
    print('not matching!!')

if re.match(r'\d+/\d+/\d+',text2):   # not match
    print('matching!!')
else:
    print('not matching!!')


# 동일한 패턴으로 매칭을 많이 수행할 예정이라면?
# 정규 표현식을 미리 컴파일해서 패턴 객체로 만들어 놓자

datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')

if datepat.match(text2):
    print('yes')
else:
    print('no')


# match()는 항상 문자열 '처음' 에서 찾기를 시도한다. 텍스트 전체에 걸쳐 패턴을 찾으려면 findall()메소드 사용

text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
t = datepat.findall(text)
print(t)  # ['11/27/2012', '3/13/2013']

# 정규표현식을 정의할 때 , 괄호를 사용해 캡처 그룹을 만드는 것이 일반적임

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')

# 캡처 그룹을 사용하면 매칭된 텍스트에 작업할 때가 각 그룹을 개별적으로 추출할 수 있어서 편하다

m = datepat.match('11/27/2012')   #_sre.SRE_Match object

# 각 그룹에서 내용 추출

# print(m.group(0)) # 11/272012
# print(m.group(1)) # 11
# print(m.group(2)) # 27
# print(m.group(3)) # 2012
# m.group()
# month, day, year = m.group()       # 11/27/2012  << '11','27','2012' 나온다는데 조또 안나옴.
#
#
# for m in datepat.findall(text):
#     print(m.group())


# 정규표현식을 쓸 때 핵심이 되는 것은
# re.compile()을 사용해 패턴을 컴파일 하고 / 그것을 match, findall, finditer, 등에 사용한다는 점
# 패턴을 명시할 때는 로우 문자열을 그대로 쓰는 것이 일반적이다.


# 간단한 텍스트 매칭/검색을 수행하려면 컴파일 과정 생략 후, re모듈의 모듈 레벨 함수를 바로 사용해도 괜찮다.

q = re.findall(r'(\d+)/(\d+)/(\d+)', text)
print(q)

"""
▶ 2.5 텍스트 검색과 치환 ◀ 
♣ 문제 : 문자열에서 텍스트 패턴을 검색하고, [치환] 하고 싶다.
 ↘ 해결 : re모듈의 sub() 메소드를 사용한다. 
            예를 들어, "11/27/2012"형식의 날짜를 "2012-11-27"로 바꾸고 싶다면??
            
            re.sub() 활용
              # re.sub(pattern, replace, string, count=0, flag=0)
 """
print('########################################## 2.5 텍스트 검색과 치환 #####################################')

text = 'Today is 11/27/2012. Pycon starts 3/13/2013.'

import re,csv
a = re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)  # 숫자 앞 역슬래시가 붙어있는 \3과 같은 표현은 캡처 그룹을 참조
#   re.sub('매칭을 위한 패턴', '치환을 위한 패턴', 텍스트)
print(a)


# 더 복잡한 치환을 위해서 콜백 함수를 명시할 수도 있다.
# 인자가 되는 콜백은 match() or find() 에서 반환한 매치 객체를 사용한다.
# 특정 부분 추출하려면 .group() 메소드 사용..
# 치환된 텍스트 받기 전 몇번 치환이 발생했는지 보려면, re.subn사용한다.

from calendar import month_abbr
def change_date(m):
    mon_name = month_abbr[int(m.group(1))]  #m.group(1) = 11 즉 11월  = Nov로 치환될듯
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))  #m.group(2) = 27
g =datepat.sub(change_date, text)
print(g)

newtext, n = datepat.subn(r'\3-\1-\2',text)
print(newtext , 'count : ',n)








print('########################### EMP 활용 ########## EMP 활용 #####################')
#emp로 활용해보기
emppat = re.compile(r'\d+.\d+.\d+')
for i in emps:
    if emppat.match(i['hiredate']):  #okay가 나올것이다. 왜냐하면 패턴이 일치하기때문에.
        print('okay')
    else:
        print('no way')


#emp의 hiredate를 00/00/00 로 치환해보기
#emp 의 hiredate를 복잡한 패턴으로 바꿔보기
from calendar import month_abbr

def emp_month_change(emp):
    emp_month = month_abbr[int(emp.group(2))]   #int형으로 바꿔줘야함
    return '{} {} {}'.format(emp.group(3), emp_month, emp.group(1))

import re
emppat = re.compile(r'(\d+).(\d+).(\d+)')  #hiredate의 패턴을 미리 컴파일
for i in emps:
    emp_substit = emppat.sub(r'\1/\2/\3',i['hiredate'])   #다음과 같은 패턴으로 hiredate를 치환한다.
    complex_substit = emppat.sub(emp_month_change,emp_substit)          #치환된 데이터를 복잡한 패턴(emp_month_change)으로 재치환하여 complex_substit에 할당
    print(complex_substit)

"""
▶ 2.6 대소문자를 구별하지 않는 검색과 치환 ◀ 
♣ 문제 : 텍스트를 검색 / 치환 할때 대소문자를 구별없이 모두 수행하려면?
 ↘ 해결 : 텍스트 관련 작업 시, 대소문자 구별 않기 위해선, 
            re모듈을 사용해야 하며   /  re.IGNORECASE 플래그를 지정해야 한다. 
            

            
 """
print('########################################## 2.6 대소문자를 구별하지 않는 검색과 치환 #####################################')
import re

text = 'UPPER PYTHON, lower python, Mixed Python'

# a = re.findall(,text, flags=re.IGNORECASE)  #python 을 fuckyou로 치환하며, re.IGNORECASE를 플래그로 지정한다.

a = re.findall('python',text, flags=re.IGNORECASE)      #['PYTHON', 'python', 'Python']
print(a)

print(type(text))

b = re.sub('python','fuckyou',text,flags=re.IGNORECASE)
print(b)

def matchcase(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
    return replace

c=re.sub('python', matchcase('fuckyourself'),text,flags=re.IGNORECASE)
print(c) #UPPER FUCKYOURSELF, lower fuckyourself, Mixed Fuckyourself











"""
▶ 2.7 가장 짧은 매칭을 위한 정규 표현식 ◀ 
♣ 문제 : 이런 문제는 문장 구분자에 둘러싸여 있는 텍스트를 찾을 때 종종 발생한다. (ex: 인용문  "" )
 ↘ 해결 : complie할 패턴을 따옴표에 둘러싸인 텍스트를 찾도록 의도하라.
 
 """
print('########################################## 2.7 가장 짧은 매칭을 위한 정규 표현식 #####################################')


str_pat = re.compile(r'\"(.*)\"')  # 따옴표에 둘러싸인 문장을 찾고자 한다.
txt1 = 'Computer says "no."'
txt2 = 'Computer says. "no" Phone says "yes"'
a = str_pat.findall(txt1)
print(a)  # 'no'
b = str_pat.findall(txt2)
print(b) # ['no" Phone says "yes']

str_pat = re.compile(r'\"(.*?)\"')   # * 뒤에 ? 붙이면 됨
# ? = 바로 앞의 문자가 존재하거나 존재하지 않음 ( 문자가 0 혹은 1회 반복됨을 의미)

b = str_pat.findall((txt2))
print(b) # no, yes

# 점(.) 개행 문자를 제외한 문자 1자를 나타냄.
# .* 을 해서 개행 문자를 제외한 문자 1자가 무한대로 반복시켜서 패턴 찾게 하고 있음
# 여기서 ? 을 붙여서 적당히 끊는것?
# 이번 레시피는 점(.)을 사용한 정규표현식 작성 중 많이 발생하는 예 이다.
# 점이 처음과 중간에 있으면 매칭은 긴 것을 찾아내려고 하게 되서 오류발생
# 이때 *나 +에 ?를 붙여주면 매칭 알고리즘이 가장 짧은것을 찾으려고 노력할 것


"""
▶ 2.8 여러 줄에 걸친 정규 표현식 사용 ◀ 
♣ 문제 : 여러 줄에 걸친 정규 표현식 매칭을 사용하고 싶다면?
            위 문제는 주로 점(.)을 사용한 텍스트 매칭을 할때 이 문자가 개행문에 매칭하지 않는다는 사실을
            잊었을 때 주로 발생한다.
 ↘ 해결 : 

 """
print('########################################## 2.8 여러 줄에 걸친 정규 표현식 사용 #####################################')


comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'  # c스타일 주석
text2 = '''/* this is a
                        multiline comment */'''

t = comment.findall(text1)
y = comment.findall(text2)
print(t) #[' this is a comment ']
print(y) # []

# text2는 잡아내기 힘들다. 다음과 같은 패턴을 넣어야한다.
comment = re.compile((r'/\*((?:.|\n)*?)\*/'))

t = comment.findall(text1)  #[' this is a comment ']
y = comment.findall(text2)  #[' this is a\n                        multiline comment ']
print(t)
print(y)

# 이 패턴에서 (?:.|\n)은 논캡처 그룹을 명시한다. ( 이그룹은 매칭의 목적은 명시하지만, 개별적으로 캡처하거나 숫자를 붙이지는 않는다.)

# re.compile() 에서 re.DOTALL이라는 유용한 플래그를 사용할 수 있다.
# 이 플래그는 정규 표현식의 점(.)이 개행문을 포함한 모든 문자에 매칭한다.

comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)   #reDOTALL()플래그는 사용하면 간단한 패턴에 잘 동작한다. (복잡한 패턴or여러 정규표현식 합쳐 토큰화할땐 곤란)
# 웬만하면 플래그 없이 잘 동작할 수 있도록 표현식 짜는게 좋음.

