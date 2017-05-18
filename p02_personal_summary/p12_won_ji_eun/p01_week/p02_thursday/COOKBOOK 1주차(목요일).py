            #1.18 시퀀스 요소에 이름 매핑
#문제: 리스트나 튜플의 위치로 요소에 접근하면 가독성이 떨어짐
#해결방법: collections.namedtuple() 사용

    #예제1        namedtuple() 사용                     
from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr','joined'])
sub = Subscriber('jonesy@exmaple.com','2012-10-19')
sub
#(실행결과) Subscriber(addr='jonesy@exmaple.com', joined='2012-10-19')
sub.addr   # sub를 인스턴스화 가능한 클래스처럼 사용
#(실행결과) 'jonesy@exmaple.com'
sub.joined
#(실행결과)  '2012-10-19'
len(sub)    #일반적인 튜플처럼 사용가능
#(실행결과) 2
addr, joined = sub
addr 
#(실행결과) 'jonesy@exmaple.com'
joined
#(실행결과) '2012-10-19'


     #예제2 
from collections import namedtuple
Stock = namedtuple('Stock',['name','shares','price'])
def compute_cost(records):
    total=0.0
    for rec in records:
        s= Stock(*rec)
        total +=s.shares*s.price
    return total


    #예제3
s=Stock('ACME',100,123.45)
s
#(실행결과) Stock(name='ACME', shares=100, price=123.45)
s.shares=75 # ←안됨. namedtuple은 수정할 수 없음. 수정하려면 namedtuple의 _replace() 메소드를 사용해야한다.
s=s._replace(shares=75)
s
#(실행결과) Stock(name='ACME', shares=75, price=123.45)

from collections import namedtuple
Stock = namedtuple('Stock',['name','shares','price'])
def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total +=s.shares*s.price
        
s=Stock('ACME',100,123.45)
s
#(실행결과) Stock(name='ACME', shares=100, price=123.45)

s.shares=75 #<- 안됨.

s= s._replace(shares=75)
s
#(실행결과) Stock(name='ACME', shares=75, price=123.45)

from collections import namedtuple
Stock = namedtuple('Stock',['name','shares','price', 'date', 'time'])
stock_prototype = Stock('',0,0.0, None, None)

def dict_to_stock(s):
    return stock_prototype._replace(**s) #**는 딕셔너리 가변 매개변수
    
a={'name': 'ACME', 'shares':100, 'price':123.45}
dict_to_stock(a)

#(실행결과) Stock(name='ACME', shares=100, price=123.45, date=None, time=None)

b={'name':'ACME', 'shares':100, 'price':123.45, 'date': '12/17/2012'}
dict_to_stock(b)
#(실행결과) Stock(name='ACME', shares=100, price=123.45, date='12/17/2012', time=None)



            #1.19 데이터를 변환하면서 줄이기
# 문제 : 감소함수를 실행할때는 데이터를 변환하거나 필터링해야한다.

    #예제1
numes=[1,2,3,4,5]
s = sum(x*x for x in nums) # 1+4+9+16+25
s
#(실행결과) 55

# 다른 방법
import os
files = os.listdir('dirname')
if any(name.endswith('.py') for name in files):
    print('There be python!')
else:
    print('Sorry, no python.')
    
    
s= ('ACME',50,123.45)
print(','.join(str(x) for x in s))
#(실행결과) ACME,50,123.45



             #1.20 여러 매핑을 단일 매핑으로 합치기

#문제 : 딕셔너리나 매핑이 여러개있고 자료검색이나 데이터 확인을 위해서 하나의 매핑으로 합치고 싶을 때

    # 예제1 
a={'x':1, 'z':3}
b={'y':2, 'z':4}

from collections import ChainMap
c=ChainMap(a,b)
print(c['x'])
#(실행결과)  1
print(c['y'])
#(실행결과) 2
print(c['z'])
#(실행결과) 3 #a의 z가 출력됨
 
     # 예제2
len(c)
#(실행결과) 3
list(c.keys()) 
#(실행결과) ['z', 'y', 'x']
list(c.values())
#(실행결과) [3, 2, 1]

c['z']=10
c['w']=40
del c['x']
a
#(실행결과) {'w': 40, 'z': 10}

del c['y']
#(실행결과) "Key not found in the first mapping: 'y'"

values=ChainMap()
values['x']=1 # 새로운 매핑 추가
vlaues=values.new_child()
values['x']=2 # 새로운 매핑 추가
vlaues=values.new_child()
values['x']=3 # 새로운 매핑 추가
values
#(실행결과) ChainMap({'x': 3},{'x': 2},{'x': 1})
values=values.parents # 마지막 매핑 삭제
values['x']
#(실행결과) 2

a={'x':1, 'z':3}
b={'x':2, 'z':4}
merged = dict(b)
merged.update(a)
merged['x']
#(실행결과) 1
merged['y']
#(실행결과) 2 
merged['z']
#(실행결과) 3

a['x']=13
merged['x']
#(실행결과) 1  #원본 파일이 수정되어도 딕셔너리에 반영안됨

a= {'x':1, 'z':3}
b={'x':2, 'z':4}
merged = ChainMap(a,b)
merged['x']
#(실행결과)  1
a['x'] = 42
merged['x']
#(실행결과) 42 #ChainMap은 원본 딕셔너리 참조





                #Chapter2 문자열과 텍스트
                
            #2.1 여러 구분자로 문자열 나누기
            
# 문제 : 문자열을 필드로 나누고 싶지만 구분자가 일관적이지 않음
# 해결방법 : split()과 re.split() 사용

    #예제
line = 'asdf fjdk; afed, fjek, adsp,     foo'
import re
re.split(r'[;,\s]\s*)', line)
#(실행결과) ['asdf','fjdk', 'afed', 'fjek', 'adsp', 'foo']


fields = re.split(r'(;|,|\s)\s*',line)
fields
#(실행결과) ['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjek', ',', 'adsp', ',', 'foo']

values = fields[::2] # 시작숫자, 갯수, 간격
delimiters = fields[1::2] +['']
values
#(실행결과) ['asdf', 'fjdk', 'afed', 'fjek', 'adsp', 'foo']

delimiters
#(실행결과) [' ', ';', ',', ',', ',', '']




            #2.2 문자열 처음이나 마지막에 텍스트 매칭
            
# 문제 : 문자열 처음이나 마지막에 파일 확장자 등이 포함되었는지 확인
# 해결 방법 : str.startswith(), str.endswith()메소드 사용

        #예제
filename='spam.txt'
filename.endswith('.txt')
            
#(실행결과) True
filename.startswith('file:')
 
#(실행결과) False

url = 'http://www.python.org'
url.startswith('http:')
#(실행결과) True

     #예제2 접두어와 접미사 검사

filename='spam.txt'
filename[-4:]=='.txt'
#(실행결과) True
url = 'http://www.python.org'
url[:5]=='http:' or url[:6] =='https:' or url[:4] =='ftp:'
#(실행결과) True

 
 
 
            #2.4 텍스트 패턴 매칭과 검색
            
# 문제 : 특정 패턴 검색            

    # 예제1 str.find(), str.endswith(), str.startswith()
    
text = 'yeah, but no, but yeah, but no, but yeah'
text =='yeah'
#(실행결과) False
text.startswith('yeah')
#(실행결과) True
text.endswith('no')
#(실행결과) False

text.find('no') # 처음 나타난 곳 검색 
#(실행결과) 10


     # 예제2 더 복잡한 경우 re 모듈 사용
     
text1 = '11/27/2012'
text2 = 'Nov 27, 2012'

import re
if re.match(r'\d+/\d+/\d+', text1): # \d+는 하나이상의 숫자를 의미
    print('yes')
else:
    print('no')
 
#(실행결과) yes

if re.match(r'\d+/\d+/\d+', text2):
    print('yes')
else:
    print('no')
    
#(실행결과) no

 
datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')
#(실행결과)yes
if datepat.match(text2):
    print('yes')
else:
    print('no')

#(실행결과) no

 
 
         #2.5 텍스트 검색과 치환
#문제 : 문자열에서 텍스트 패턴을 검색하고 치환

#해결방법: str.replace()

    #예제
text = 'yeah, but no, but yeah, but no, but yeah'
text.replace('yeah','yep')

#(실행결과)'yep, but no, but yep, but no, but yep'

     #예제2 더 복잡한 건 re 모듈의 sub()
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
import re
re.sub(r'(\d+)/(\d+)/(\d+)',r'\3-\1-\2', text)

#(실행결과) 'Today is 2012-11-27. PyCon starts 2013-3-13.'

     #예제3 더 더 복잡한 치환은 콜백 함수
from calendar import month_abbr
def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{}{}{}'.format(m.group(2), mon_name,m.group(3))

datepat.sub(change_date, text)




            #2.6 대소문자를 구별하지 않는 검색과 치환 
            
# 문제 대소문자 구별하고 싶지 않을 때

    #예제1 
text = 'UPPER PYTHON, lower python, Mixed Python'
re.findall('python', text, flags=re.IGNORECASE)

#(실행결과) ['PYTHON', 'python', 'Python']

re.sub('python', 'snake', text, flags=re.IGNORECASE)
#(실행결과) 'UPPER snake, lower snake, Mixed snake'

 
def matchcase(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text. islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
        return replace
    
re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE)
        
#(실행결과)'UPPER SNAKE, lower snake, Mixed Snake'



            #2.7 가장 짧은 매칭을 위한 정규 표현식
            
    #예제
str_pat = re.compile(r'\"(.*)\"')
text1='Computer says "no."'
str_pat.findall(text1)
#(실행결과) ['no.']
text2='Computer says "no." Phone says "yes."'
str_pat.findall(text2)
#(실행결과) ['no." Phone says "yes.']



            #2.8 여러줄에 걸친 정규표현식 사용
            
    #예제
comment = re.compile(r'/\*(.*?)\*/')
text1='/* this is a comment */'
text1='''/* this is a multiline comment */'''
comment.findall(text1)
#(실행결과) [' this is a multiline comment ']



            #2.11 문자열에서 문자 잘라내기
            
#문제 : 텍스트의 처음, 끝 중간에서 공백 없애기

    #예제
s='   hellow world \n'
s.strip()
#(실행결과)  'hellow world'
s.lstrip()
#(실행결과)'hellow world \n'
s.rstrip() 
#(실행결과)  '   hellow world'

s='  hello    world    \n'
s=s.strip()
s
#(실행결과)  'hello    world' # 가운데 공백은 없어지지 않는다 -> 정규표현식 사용

     #예제2
s.replace(' ','')

 #(실행결과)  'helloworld'
import re
re.sub('\s+','',s) 
#(실행결과) 'helloworld'



            #2.12 텍스트 정리
    # 예제 str.replace()나 re.sub(), normalize() 사용할수 있지만 고급스럽게 str.translate() 사용

s= 'python\fis\tawesome\r\n'
s
#(실행결과)  'python\x0cis\tawesome\r\n'

remap= {ord('\t'): ' ', 
        ord('\f'): ' ', 
        ord('\r'): None }
a= s.translate(remap)
a
#(실행결과) 'python is awesome\n' # \t와 \f같은 공백문은 띄어쓰기 하나로 치환한다

     #예제2 str.replace() 사용
def clean_spaces(s):
    s=s.replace('\r','')
    s=s.replace('\t',' ')
    s=s.replace('\f',' ')
    return s    



            #2.13 텍스트 정렬
# 문제 텍스트를 특정 형식에 맞춰 정렬

    #예제 ljust(), rjust(), center()
text = 'Hello World'
text.ljust(20)
#(실행결과) 'Hello World         '
text.rjust(20)
#(실행결과) '         Hello World'
text.center(20)
#(실행결과) '    Hello World     '

     #예제2 채워넣기
text.rjust(20,'=')
#(실행결과) '=========Hello World'
text.center(20,'*')
#(실행결과) '****Hello World*****'

format(text,'>20')
#(실행결과) '         Hello World'

 
 
         #2.14 문자열 합치기
         
    #예제1 
parts = ['Is', 'Chicago', 'Not', 'Chicago?']
' '.join(parts)
#(실행결과)  'Is Chicago Not Chicago?'

 
 
         #2.15. 문자열에 변수 사용
         
#예제 :
s = '{name} has {n} messages.'
s.format(name='Guido',n=37)

#(실행결과)  'Guido has 37 messages.'

 

        #2.16 텍스트 열의 개수 고정
        
# 문제 : 긴 문자열의 서식을 바꿔 열의 개수를 조절하고 싶다.

#해결방법: textwrap 모듈을 사용

s = "Look into my eyes, look into my eyes, the eyes, the eyes, \  the eyes, not around the eyes, don't look around the eyes, \  look into my eyes, you're under."  
  
import textwrap  

print(textwrap.fill(s, 70))  
print()  
  
print(textwrap.fill(s, 40))  
print()  
  
print(textwrap.fill(s, 40, initial_indent='    '))  
print()  
  
print(textwrap.fill(s, 40, subsequent_indent='    '))  
print()  


#(실행결과) 
'''Look into my eyes, look into my eyes, the eyes, the eyes, \  the eyes,
not around the eyes, don't look around the eyes, \  look into my eyes,
you're under.

Look into my eyes, look into my eyes,
the eyes, the eyes, \  the eyes, not
around the eyes, don't look around the
eyes, \  look into my eyes, you're
under.

    Look into my eyes, look into my
eyes, the eyes, the eyes, \  the eyes,
not around the eyes, don't look around
the eyes, \  look into my eyes, you're
under.

Look into my eyes, look into my eyes,
    the eyes, the eyes, \  the eyes, not
    around the eyes, don't look around
    the eyes, \  look into my eyes,
    you're under.

