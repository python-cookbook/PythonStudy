
#1.18 시퀀스 요소에 이름 매핑
#문제 : 리스트나 튜플의 위치로 요소에 접근하는 코드가 있다. 하지만 때론 이런 코드의 가독성이 떨어진다. 또한 위치에 의존하는
# 코드의 구조도 이름으로 접근 가능하도록 수정하고 싶다.
#해결 : collections.namedtuple()을 사용하면 일반적인 튜플 객체를 사용하는 것에 비해 그리 크지 않은 오버헤드로 이 기능을 구현한다.
#collections.namedtuple()은 실제로 표준 파이썬 튜플 타입의 서브클래스를 반환하는 팩토리 메소드 이다. 타입 이름과 포함해야할 필드를
#전달하면 인스턴스화 가능한 클래스를 반환한다. 여기에 필드의 값을 전달하는 식으로 사용 가능하다.
from collections import namedtuple
Subscriber = namedtuple('Subscriber',['addr','joined'])
sub = Subscriber('aaa@naver.com','2012-01-02')
sub
sub.addr
#namedtuple의 인스턴스는 일반적인 클래스 인스턴스와 비슷해 보이지만 튜플과 교환이 가능하고 인덱싱이나 언패킹과 같은 튜플의 일반적인 기능을 모두 지원한다.
len(sub)
addr,joined = sub
addr
joined
#네임드 튜플은 주로 요소의 위치를 기반으로 규현되어 있는 코드를 분리한다. 따라서 데이터베이스로부터 거대한 튜플리스트를 받고 요소의 위치로
#접근하는 코드가 있을 때, 예를 들어 테이브렝 새로운 열이 추가되었다거나 할 떄 문제가 생길 수 있다. 하지만 반환된 튜플을 네임드 튜플로 변환했다면
#이런 문제를 예방할 수 있다.
def compute_cost(records):
    total = 0.0
    for rec in records:
        total += rec[1]*rec[2]
    return total
#위치에 기반한 다음과 같은 요소 접근은 가독성을 떨어뜨리고 자료의 구조형에 크게 의존한다.
from collections import namedtuple
Stock = namedtuple('Stock',['name','shares','price'])
def compute_cost(records):
    total =0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total
#예제의 records 시퀀스에 이미 인스턴스가 포함되어 있기 때문에 stock 네임드 튜플로 명시적인 변환을 하지 않아도 된다.
#토론 : 네임드 튜플은 저장 공간을 더 필요로 하는 딕셔너리 대신 사용할 수 있다. 딕셔너리를 포함한 방대한 자료 구조를 구상하고 있다면
#네임드 튜플을 사용하는 것이 효율적. 하지만 네임드 튜플은 수정이 불가능.
s=Stock('ACME',100,123.45)
s
s.shares = 75
#속성을 수정해야 한다면 네임드튜플 인스턴스의 _replace() 메소드를 사용한다.
s = s._replace(shares=75)
#_replace를 사용하면 옵션이나 빈 필드를 가진 네임드 튜플을 간단히 만들 수 있다. 일단 기본 값을 가진 프로토타입 튜플을 만들고.
# _replace()로 치환돤 값을 가진 새로운 인스턴스를 만든다.
from collections import namedtuple
Stock = namedtuple('Stock',['name','shares','price','date','time'])
stock_prototype=Stock(' ',0,0.0,None,None)
def dict_to_stock(s):
    return stock_prototype._replace(**s)
a={'name':'ACME','shares':100,'price':123.45}
dict_to_stock(a)
#인스턴스 요소를 빈번히 수정해야 하면 네임드 튜플은 적절치 않음. __slots__사용을 생각하자
#1.19 데이터르 ㄹ변환하면서 줄이기
#문제. 감소함수(sum,min,max)를 실행해야 하는데 데이터를 변환하거나 필터링 해야함.
#해결. 데이터를 줄이면서 변형하는 가장 우아한 방식은 생성자 표현식을 사용하는 것.
nums=[1,2,3,4,5]
s=sum(x*x for x in nums)
s
s=('ACME',50,123.45)
print(','.join(str(x) for x in s))
#토론: 앞에서 살펴본 코드는 함수에 인자로 전달된 생성자 표현식의 문법적인 측면을 보여준다.
#다음 두 코드는 동일하다
s = sum((x*x for x in nums))
s = sum(x*x for x in nums)
#생성자 인자를 사용하면 임시 리스트를 만드는 것보다 더 효율적이고 코드가 간결한 경우가 많음.
#생성자를 사용하면 데이터를 순환 가능하게 변형하므로 메모리 측면에서 훨씬 유리하다.
#min, max 같은 함수는 key라는 여러 상황에 유용한 인자를 받기 때문에 생성자 방식을 사용해야 하는 이유를 한 가지 더 만들어줌
#원본
min_shares = min(s['shares'] for s in portfolio)
#대안
min_shares = min(portfolio, key=lambda s:s['shares'])
#1.20 여러 매핑을 단일 매핑으로 합치기
#문제 딗너리나 매핑이 여러 개 있고 자료 검색이나 데이터 확인을 위해 하나의 매핑으로 합치고 싶다
#해결
a={'x':1,'z':3}
b={'y':2,'z':4}
from collections import ChainMap
c =ChainMap(a,b)
print(c['x'])
print(c['z'])
#체인맵은 여러개를 매핑받아 하나처럼 보이게 만듬. 근데 보이는 것일뿐 실제로는 아님.
#딕셔너리 동작을 재 정의할뿐 대부분의 명령이 동작
list(c.keys())
#중복키가 있으면 첫번째 매핑값 사용
#매핑값을 변경하는 동작은 언제나 리스트의 첫번째 매핑에 영향을 준다.
c['z']=10
c['w']=40
del c['x']
a
del c['y']
#체인맵은 프로그래밍 언어의 변수와 같이 범위가 있는 값(전역변수 지역변수)에 사용하면 유용#
#이 동적을 쉽게 만들어 주는 메소드
values = ChainMap()
values['x']=1
values = values.new_child() #새로운 매핑 추가
values['x']=2
values
#마지막 매핑 삭제
values = values.parents
values
#chainmap의 대안으로 update()를 사용해 딗너리를 하나로 합칠 수도 있다.
a={'x':1, 'z':3}
b={'y':2,'z':4}
merged=dict(b)
merged.update(a)
merged['x']
merged['y']
merged['z']
#이렇게 해도 잘 독장하지만, 완전히 별개의 딕셔너리 객체를 새로 만들어야 한다.
#또한 원본 딕셔너리 내용이 변경된다 해도 합쳐놓은 딕셔너리에 반영되지 않는다.
a['x']=13
merged['x']
#chainmap은 원본 딕셔너리를 참조하기 때문에 이와 같은 문제가 발생하지 않는다.
a = {'x':1, 'z':3}
b = {'y':2, 'z':4}
merged = ChainMap(a,b)
a['x']=42
merged['x']

#Chapter 2. 문자열과 텍스트
#2.1 여러 구분자로 문자열 나누기
#문제. 문자열을 필드로 나누고 싶지만 구분자가 문자열에 일관적이지 않다.
#해결 문자열 객체 split() 메소드
line = 'asd asdf grgf; asd, sad'
import re
re.split(r'[;,\s]\s*',line)
#re.split은 함수 분리 구문마다 여러 패턴을 명시할 수 있다는 점이 유리하다.
#re.split을 사용할 때는 괄호안에 묶인 정규 표현식 패턴이 캡처 그룹이 된다는 점에 유의
#캡처 그룹을 사용하면, 매칭된 텍스트에도 결과가 포함된다.
fields = re.split(r'(;|,|\s)\s',line)
fields
#구분문자만 추출해야할 경우
values = fields[::2]
delimeters=fields[1::2]+['']
values
delimeters
#분리구문을 결과에 포함시키고 싶지 않지만 정규식 괄호를 사용해야 할 필요가 있다면 논캡처그룹을 사용해야 함.
re.split(r'(?:,|;|\s)\s*',line)
#2.2 문자열 처음이나 마지막에 텍스트 매칭
#문제. 문자열의 처음이나 마지막에 파일 확장자, URL 스킴등 특정 펙스트 페턴이 포함되었는지 검사하고 싶다
#해결. 문자열의 처음이나 마지막에 패턴이 포함되었는지 확인하는 간단한 방법으로 str.startswith(), str.endswith()
filename = 'spam.txt'
filename.endswith('.txt')
filename.startswith('file:')
#여러개의 선택지를 검사하고 싶으면 그 값을 튜플에 담아 전달
import os
filenames = os.listdir('.')
filenames
from urllib.request import urlopen
def read_data(name):
    if name.startswith(('http:','https:','ftp:')):
        return urlopen(name).read()
    else:
        with open(name) as f:
            return f.read()
#이것은 파이썬에서 튜플만을 입력으로 받는 것 중 하나. 따라서 입력 값을 리스트나 세트로 가지고 있다면 튜플을 사용해서 먼저 변환해 주어야 함.
choices = ['http:','ftp:']
url ='http://www.python.org'
url.startswith(tuple(choices))
#토론. startswith과 endswith은 접두어와 접미어를 검사할 떄 매우 편리하다. 슬라이스를 사용하면 비슷하지만 가독성 저하
#2.3 쉘 와일드카드 페턴으로 문자열 매칭
#문제 유닉스 쉘에 사용하는 것과 동일한 와일드카드 패턴을 텍스트 매칭에 사용하고 싶다.
#해결 fnmatch 모듈 두 함수 를 사용하면 됨
from fnmatch import fnmatch, fnmatchcase
fnmatch('foo.txt','*.txt')
fnmatch('foo.txt','?oo.txt')
fnmatch('Dat45.csv','Dat[0-9]*')
names = ['Dat1.csv','config.ini','foo.py']
[name for name in names if fnmatch(name,'Dat*.csv')]
#일반적으로 fnmatch는 시스템의 파일 시스템과 동일하게 대소문자 구분한다.(윈도우는 대소문자 구분 안함 맥은 대소문자 구분함)
#이것이 맘에 ㅏㅇㄴ들면 fnmatchcase를 사용하면 됨. 얘는 정확히 구분해줌
#이 함수는 데이터 프로세싱에도 사용할 수 있다.
addresses = ['5412 N CLARK ST','1060 W ADDISON ST','1039 W GRANVILLE AVE']
[addr for addr in addresses if fnmatchcase(addr,'* ST')]
#토론 fnmatch가 수행하는 매칭은 간단한 문자열 메소드 기능과 정규식의 중간쯤 위치.
#데이터 프로세싱할 때 간단한 와일드카드를 사용할 생각이라면 이 함수를 사용하는 것이 괜찮음.
#파일 이름 찾고싶으면 glob모듈 사용
#2.4 텍스트 패턴 매칭과 검색
#문제 특정 패턴에 대한 텍스트 매칭이나 검색 하고 싶음.
#해결 매칭하려는 텍스트가 간단하면 str.find(), str.endswith(), str.startswith() 사용
#더 복잡하면 정규식, re모듈 사용 re.match(pattern,text)
#동일한 정규식 패턴을 많이 수행하면 정규식을 미리 컴파일 해서 객체로 만들어 놓으면 좋음
import re
datapat = re.compile(r'\d+/\d+/\d+')
if datapat.match(text1):
    print('yes')
#match()는 항상 문자열 처음에서 찾기를 시도. 텍스트 전체에 걸쳐 패턴을 찾으려면 findall()
text = 'Today is 11/27/2012. Pycon starts 3/13/2013.'
datapat.findall(text)
#정규식 정의할 때 괄호를 사용해 캡처 그룹을 만드는 것이 일반적.
datapat = re.compile(r'(\d+)/(\d+)/(\d+)')
#켑처 그룹을 사용하면 매칭된 텍스트에 작업할 떄 각 그룹을 개별적으로 추출 가능.
m=datapat.match('11/27/2012')
m
m.group(0)
m.group(1)
m.groups()
month, day, year = m.groups()
#findall 메소드는 텍스트를 검색하고 모든 매칭을 찾아 리스트로 반환. 한번에 결과를 얻지 않고 텍스트를 순환하며 찾으려면 finditer()
#match()메소드는 문자열의 처음만 확인한다. 정확한 매칭을 위해서는 $를 사용하자
#간단한 텍스트 매칭/ 검색을 수행하려 한다면 컴파일 과정을 생략하고 re 모듈의 모듈 레벨 함수를 바로 사용해도 괜찮다.
#패턴을 미리 컴파일 한다면 더 효율적
#2.5 텍스트 검색과 치환
#문제 문자열에서 텍스트 패턴을 검색하고 치환하고 싶다.
#해결 간단한 패턴이면 str.replace()
text = 'yeah, but no, but yeah, but no, but yeah'
text.replace('yeah','yep') # text가 변환되는 것은 아님
text
#조금 더 복잡한 패턴을 사용하려면 re 모듈의 sub()함수/메소드를 사용한다.
text="Today is 11/27/2012. Pycon starts 3/13/2013"
import re
re.sub(r'(\d+)/(\d+)/(\d+)',r'\3-\1-\2',text)
#e동일한 패턴을 사용한 치환을 계속해야 한다면 성능 향상을 위해 컴파일링을 고려해 보는 것이 좋다.
import re
datapat = re.compile(r'(\d+)/(\d+)/(\d+)')
datapat.sub(r'\3-\1-\2',text)
#더 복잡한 치환은 콜백 함수를 명시할 수도
from calendar import month_abbr
def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2),mon_name,m.group(3))

datapat.sub(change_date,text)
#인자가 되는 치환 콜백은 match()나 find()에서 반환한 매치 객체를 사용한다. 매치에서 특정부분 추출은 group()메소드
#이 함수는 치환된 텍스트를 반환해야 한다. 치환된 텍스트 몇 번인지 알고싶다면 re.subn()
newtext, n = datapat.subn(r'\3-\1-\2',text)
newtext
n
#2.6 대소문자를 굽ㄹ하지 않는 검색과 치환
#텍스트를 검색하고 치환할 때 대소문자를 구별하지 않고 싶다.
#해결 텍스트 관련 작업을 할 때 대소문자를 구별하지 않기 위해서는 re 모듈을 사용해야 하고 re.IGNORECASE를 지정해야함
text = 'UPPER PYTHON, lower python, Mixed Python'
re.findall('python',text,flags=re.IGNORECASE)
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
re.sub('python',matchcase('snake'),text,flags=re.IGNORECASE)
#이렇게하면 원본의 대소문자 구분에 따른 sub를 출력 할 수 있다.
#토론 대개의 경우 ignorecase를 사용하는 것만으로 대소문자를 무시한 텍스트 작업에 무리가 없다. 유니코드가 포함되면 부족할수도..
#2.7 가장 짧은 매칭을 위한 정규식
#문제 정규식을 이용한 텍스트 매칭을 하고 싶지만 텍스트에서 가장 긴 부분을 찾아냄. 짧은 부분을 찾고싶다면??
#해결 이런 문제는 문장 구분자에 둘러 싸여 있는 텍스트 찾을 때 종종 발생
str_pat = re.compile(r'\"(.*)\"')
text1 = 'Computer says "no."'
str_pat.findall(text1)
text2 = 'Computer says "no." Phone says "yes."'
str_pat.findall(text2)
#앞의 정규식은 따옴표에 둘러싸인 텍스트를 찾는 것. 하지만 가장 긴 텍스트를 찾음
str_pat = re.compile(r'\"(.*?)\"')
str_pat.findall(text2) #올바른 결과
#2.8 여러줄에 걸친 정규식
#문제 여러줄에 걸친 정규식을 사용하고 싶다.
#해결 이문제는 점을 사용한 텍스트 매칭을 할 때 이 문자가 개행문에 매칭하지 않는다는 사실을 잊었을 때 일반적으로 발생
#예를들어 다음과 같이 텍스트에서 C스타일 주석을 찾아보자
comment = re.compile(r'/\*(.*?)\*/')
text = '/* this is a comment */'
comment = re.compile(r'/\*((?:.|\n)*?)\*/')
text2 = '/*this is a \n multiline */'
comment.findall(text2)
#토론 re.compile에 re.DOTALL 플래그 사용 가능
comment = re.compile(r'/\*(.*?)\*/',re.DOTALL)
comment.findall(text2)
#위 플래그는 간단한 패턴에는 잘 도작하지만 복잡하면 문제가 발생할수도있다.
#2.11 문자열에서 문자 잘라내기
#문제 유텍스트의 처음,끝 중간에서 원하지 않는 공백문 등을 잘라내고 싶다.
#해결 strip메소드를 사용하면 문자여르이 처음과 끝에서 문자를 잘라냀 ㅜ있음. lstrip, rstrip 모두 사용 가능
s='   hello world \n'
s.strip()
s.lstrip()
s.rstrip()
t='------hello====='
t.lstrip('-')
t.strip('-=')
#토론 데이터를 보기 좋게 만들기 위한 용도로 사용함. 하지만 중간 잘라내기는 불가능
#이 부분을 처리하려면 replace()나 정규식 사용해야함
s= 'hello          world \n'
s.replace(' ','')
import re
re.sub('\s+', ' ',s)
#파일을 순환하며 데이터를 읽어 들이는 것과 같이 다른 작업과 문자열을 잘라내느 작업을 동시에 하고 싶을 수 있다.
with open(filename) as f:
    lines = (line.strip() for line in f)
    for line in lines:
        ...
#여기서 2줄은 데이터 변환을 담당.
#이것은 데이터를 실질적인 임시 리스트로 만들지 않으므로 효율적. 단지 잘라내기 작업이 적용된 라인을 순환하는 이터레이터를 생성할 뿐
#조금 더 고급 기술로는 translate()이 있음.
#2.12 텍스트 정리
#문제 이상한 문자를 입력해놓음
#텍스트를 정리하는 작업은 대게 텍스트 파싱과 데이터 처리와 관련이 있다. 단순히 생각하면 기본적인 문자열 함수를 사용해서 텍스트를
#표준 케이슬 변환하면됨.
#문자열에서 공백문을 잘라내보자
remap = {
    ord('\t') : ' ',
ord('\f') : ' ',
ord('\r') : None
}
a = s.translate(remap)
#앞에 나온 ㅐㄷ로 /t와 /f와 같은 공백문은 띄어쓰기 하나로 치환한다. 복귀코드 /r은 삭제한다.
#이를 발전시켜 더 큰 변환 테이블 만드는 것 가능. 결합 문자를 모두 없애보자.
import unicodedata
import sys
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
b= unicodedata.normalize('NFD',a)
#마지막 예제에서 dict.fromkeys()를 사용해 딕셔너리가 모든 유니코드 결합 문자를 None으로 매핑하고 있다.
#원본 입력문은 normalize()이용하여 노멀화한 후 변환 함수를 사용하여 필요 없는 문자를 모두 삭제한다.
#또 다른 예로 유니코드 숫자 문자를 이와 관련있는 아스키 숫자에 매핑하도록 변환 테이블을 작성한다.
digitmap = { c:ord("0") + unicodedata.digit(chr(c))
             for c in range(sys.maxunicode)
             if unicodedata.category(chr(c))=='Nd'}
len(digitmap)
x.translate(digitmap)
#또 다른 텍스트 정리 기술로 I/O 인코딩, 디코딩 함수가 있음. 이 방식은 텍스트를 우선 정리해 놓고 인코드나 디코드를 실행해서 잘라내거나 변경
b=unicodedata.normalize('NFD',a)
b.encode('ascii','ignore').decode('ascii')
#앞의 노멀화 과정은 원본 텍스트를 개별적인 결합 문자로 나눈다. 그리고 뒤 이은 아스키 인코딩 디코딩으로 그 문자들을 한번에 폐기
#물론 이 방식은 아스키 표현식 만을 얻으려고 할때만.
#간단한 치환은 str.replace()가 빠름.
def clean_space(s):
    s=s.replace('\r', '')
    s = s.replace('\r', ' ')
    s = s.replace('\r', ' ')
    return s
#translate()는 ㅁ복잡한 문자 리매핑이나 삭제에 좋음.
#2.13 텍스트 정렬
#문제 : 텍스트를 특정 형식에 맞추어 정렬하고 싶다.
#기본 메소드 rjust,ljust,center
text='Hello world'
text.ljust(20)
text.ljust(20,'=')
#정렬에 format()가능
format(text,'>20')
format(text,'^20')
format(text,'=>20')
#앞의 포맷 코드는 format()메소드에 사용해 여러 값을 서식화 할 수도 있다.
'{:>10s} {:>10s}'.format('Hello','World')
#format은 숫자 값등 모든 값에 동작
#2.14 문자열 합치기
#작은 문자열 여러개를 합쳐 하나의 긴 문자열 만들고 싶다.
#합치고자 하는 문자열이 시퀀스나 순환 객체 안에 있다면 join()메소드를 사용하는 것이 가장 빠름
parts = ['Is','Chicago','Not','Chicago']
' '.join(parts)
','.join(parts)
''.join(parts)
#합치려는 문자열의 수가 적다면 +만으로 충분
a = 'Is chicago'
b = 'Not chicago'
c=a+b
c
a = 'hello' 'world'
a
#별거 아니지만 프로그램 성능에 큰 영향을 주는 분야이다.
data = ['ACME','50','91.1']
','.join(str(d) for d in data)
print(a,b,c,sep=':')
#2.15 문자열의 변수사용
#문자열에 변수를 사용하고 변수에 맞는 값을 채우고 싶다.
#파이썬 문자열에 변수 값을 치환하는 간단한 방법은 없다. 하지만 format을 사용하면 비슷하게 흉내낼수있음
s = '{name} has {n} messages.'
s.format(name="guido",n=37)
#치환할 값이 변수에 들어있다면 ?
name = 'gido'
n =37
s.format_map(vars())
#vars에는 인스턴스를 사용 할 수 도 있다
class Info:
    def __init__(self,name,n):
        self.name = name
        self.n = n
a=Info('Guido', 37)
s.format_map(vars(a))
# format, format_map을 사용할 때 빠진 값이 있으면 제대로 동작하지 않음.
s.format(name='guido')
#피하는 방법
class safesub(dict):
    def __missing__(self,key):
        return '{'+key+'}'
del n
s.format_map(safesub(vars()))
#코드에서 변수 치환을 빈번히 사용할 것 같다면 치환하는 작업을 유틸리티 함수에 모아놓고 프레임 핵으로 사용 가능
import sys
def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))
name = 'Guido'
n=37
print(sub('Hello {name}'))
'%(name) has %(n) messages.' % vars()
#템플릿 사용
import string
s = string.Template('$name has $n messages')
s.substitute(vars())
#2.16 텍스트 열의 개수 고정
#문제 긴 문자열의 서식을 바꿔 여르이 개수를 조절하고 싶다.
#해결 textwrap 모듈을 사용해서 텍스트를 재 서식화 한다. 다음과 같이 긴 문자열이 있다고 가정.
s = "Look into my eyes, look into my eyes, the eyes, the eyes, the eyes, not around the eyes, don't look arond the eyes, look into my eyes, you're under"
import textwrap
print(textwrap.fill(s,70))
#텍스트를 출려갛기 전 textwrap을 사용하면 깔끔하게 서식을 맞출 수 있다. 특히 터미널에 사용할 텍스트에 적합하다.