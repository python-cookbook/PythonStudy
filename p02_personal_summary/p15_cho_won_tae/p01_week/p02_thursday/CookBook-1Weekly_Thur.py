# # 1.7 딕셔너리의 부분 추출
# # 문제
# # 딕셔너리의 특정 부분으로부터 다른 딕셔너리를 만들고 싶다
# # 해결
# # dictionary comprehension을 사용하면 간단하게 해결된다
# price = {'ACME':45,'AAPL':612,'IBM':205,'HPQ':37,'FB':10}
# # 가격이 200 이상인 것에 대한 딕셔너리
# p1 = {key:value for key,value in price.items() if value > 200}
# print(p1) # {'AAPL': 612, 'IBM': 205} 출력
# # 기술 관련 주식으로 딕셔너리 구성
# tech_name = { 'AAPL','IBM','HPQ','MSFT'}
# p2 = { key:value for key,value in price.items() if key in tech_name}
# print(p2) # {'AAPL': 612, 'IBM': 205, 'HPQ': 37} 출력
# # 토론
# # 딕셔너리 컴프리헨션으로 할 수 있는 대부분의 일은 튜플 시퀀스를 만들고 dict() 함수에 전달하는 것!!
# # 예제1)
# p1 = dict((key,value) for key,value in price.items() if value > 200)
# print(p1) # {'AAPL': 612, 'IBM': 205} 출력
# # 하지만 딕셔너리 컴프리헨션을 사용하는 것이 더 깔끔하고 실행 속도 측면에서
# # 조금 더 유리하다
# # 동일한 방법의 예제2)
# p2 = {key:price[key] for key in price.keys() & tech_name}
#           # └─> price[key]는 values 들을 가리킨다
# print(p2) # {'HPQ': 37, 'IBM': 205, 'AAPL': 612} 출력
# # 하지만 이 방법은 전의 p2의 방식에 비해 1.6배 실행 속도가 느리다

# # 1.18 시퀀스 요소에 이름 매핑
# # 문제
# # 리스트나 튜플의 위치로 요소에 저근하는 코드가 있다
# # 하지만 때론 이런 코드의 가독성이 떨어진다
# # 또한 위치에 의존하는 코드의 구조도 이름으로 접근 가능하도록 수정하고 싶다
# # 해결
# # collections.namedtuple()을 사용하면 일반적인 튜플 객체를 사용하는 것에 비해 그리 크지 않는 오버헤드로 구현 가능!!
# #collections.namedtuple()은 실제로 표준 파이썬 tuple 타입의 서브클래스를 반환하는 팩토리 메소드
# from collections import namedtuple
# Subscriber = namedtuple('Subscriber',['addr','joined'])
# sub = Subscriber('jonesy@example.com','2012-10-19')
# print(sub) # Subscriber(addr='jonesy@example.com', joined='2012-10-19') 출력
# print(sub.addr) # jonesy@example.com 출력
# print(sub.joined) # 2012-10-19 출력
# # namedtuple의 인스턴스는 일반적인 클래스 인스턴스와 비슷해 보이지만 튜플과 교환이 가능하다
# # 또한 인덱싱이나 언패킹과 같은 튜플의 일반적인 기능을 모두 지원한다

# # 1.19 데이터를 변환하면서 줄이기
# # 문제
# # 감소 함수(sum(),min(),max())를 실행해야 하는데 먼저 데이터를 변환하거나 필터링해야한다
# # 해결
# # 데이터를 줄이면서 변형하는 가장 우아한 방식은 생성자 표현식을 사용하는 것이다.
# # 예를 들어 정사각형 넓이의 합을 계산하려면 다음과 같이 한다
# num = [1,2,3,4,5]
# s = sum(x * x for x in num)
# print(s) # 1*1, 2*2, 3*3, 4*4, 5*5 의 합을 출력
# # 토론
# # 앞에서 살펴본 코드는 함수에 인자로 전달된 생성자 표현식의 문법적인 측면을 보여준다
# # 예를 들어 다음 두 코드는 동일하다
# s = sum((x*x for x in num))
# s = sum(x*x for x in num)
# # 물론 이 코드도 동작하지만 추가적인 리스트를 생성해야 한다는 번거로움이 있다.
# # 문제는 num 크기가 방대해지만 한번 쓰고 버릴 임시 리슽의 크기도 커진다는 문제가 생긴다
# # 예제1)
# min_shares = min(s['shares'] for s in protfolio)
# min_shares = min(portfolio, key=lambda x:x['shares'])
#
# # CHAPTER 2
# # 문자열과 텍스트
# # 이번 장은 문자열 나누기, 검색, 빼기, 렉싱, 파싱과 같은 텍스트 처리와 관련있는 일반적인 문제에 초점을 맞춘다
# # 2.1 여러 구분자로 문자열 나누기
# # 문제
# # 문자열을 필드로 나누고 싶지만 구분자가 문자열에 일관적이지 않다
# # 해결
# # 문자열 객체의 split() 메소드는 아주 간단한 상황에 사용하도록 설계되었고 여러개의 구분자나 구분자 주변의 공백까지 고려하지는 않는다
# # 좀더 유연하게 쓸려면 re.split() 메소드를 써보자!!
# # 예제1)
# line = 'asdf fghjk; asdf, fgjk,asdf,    foo'
# import re
# a=re.split(r'[;,\s]',line)
# # ['asdf', 'fghjk', '', 'asdf', '', 'fgjk', 'asdf', '', '', '', '', 'foo'] 출력
# # 빈칸이였던 공간이 전부다 리스트 안의 변수가 되었으므로 이를 바르게 할려면
# a=re.split(r'[;,\s]\s*',line) # ['asdf', 'fghjk', 'asdf', 'fgjk', 'asdf', 'foo'] 출력
# print(a)
#
# # 2.2 문자열 처음이나 마지막에 텍스트 매칭
# # 문제
# # 문자열의 처음이나 마지막에 파일 확자,URL 스킴(scheme) 등 특정 텍스트 패턴이 포함되었는지 검사하고 싶을때!!
# # 해결
# # 문자열의 처음이나 마지막에 패턴이 포함되었는지 확인하는
# # 간단한 방법으로 str.startswith()나 str.endswith() 메소드가 있다.
# # 예제1)
# filename = 'spam.txt'
# a = filename.endswith('.txt')
# b = filename.endswith('file:')
# print(a,b) # True, False 출력
# url = 'http://www.python.org'
# c = url.startswith('http:')
# print(c) # True 출력
# # 여러 개의 선택지를 검사해야 한다면 검사하고 싶은 값을 튜플에 담아 startswith() 이나 endswith()에 전달한다
# # 예제1)
# import os
# filenames = os.listdir('.') # 본인의 파이썬 폴더에 있는 파일을 불러준다
# print(filenames) # ['.git', '.idea', '1st_Algorithm.py', 'buffon.py', 'Class_Ex1.py', 'cross_entropy.py', ... 출력
# a = [name for name in filenames if name.endswith(('.py','.h'))]
# print(a)
# # 예제2)
# from urllib.request import urlopen
# def read_data(name):
#     if name.startswith(('http:','https:','ftp:')):
#         return urlopen(name).read()
#     else:
#         with open(name) as f:
#             return f.read()
# # 이런 것처럼 이러한 방법을 쓸려면 startswith 값에 튜플로 넣어줘야한다
# # 예제3)
# choices = ['http:','ftp:'] # 리스트기때문에 에러남!! ('http:','ftp:') 로 튜플화 할것!!!!
# url = 'http://www.python.org'
# A = url.startswith(tuple(choices))
# print(A)
# # 토론
# # startswith()와 endswith() 메소드는 접두어와 접미어를 검사할 때 매우 편리하다
# # 슬라이스를 사용하면 비슷한 동작을 할 수 있지만 코드의 가독성이 많이 떨어진다
# filename = 'spam.txt'
# print(filename[-4:] == '.txt') # True 출력
# url = 'http://www.python.org'
# print(url[:5] == 'http:' or url[:6]=='https:' or url[:4] == 'ftp:') # True 출력
# # 정규식 re로도 가능하다!!!
# import re
# url = 'http://www.python.org'
# a = re.match('http:|https:|ftp:',url)
# print(a) # <_sre.SRE_Match object; span=(0, 5), match='http:'> 출력
# # startswith() 와 endswith() 메소드는 일반적인 데이터 감소와 같은 다음 동작에 함께 사용하기에도 좋다.
# # 예를 들어, 다음 코드는 디렉토리에서 특정 파일이 있는지 확인하는 것이다
# if any(name.endswith(('.c','.py')) for name in listdir(dirname)):
#     ...
#
# # 2.3 쉘 와일드카드 패턴으로 문자열 매칭
# # 문제
# # Unix 셸에 사용하는 것과 동일한 와일드카드 패턴을 텍스트 매칭에 사용하고 싶다
# # ex) *.py, Dat[0-9]*.csv 등
# # 해결
# # fnmatch 모듈에 두 함수 fnmatch() 와 fnmatchcase() 가 있다. 사용법은 아래와 같다
# from fnmatch import fnmatch, fnmatchcase
# a = fnmatch('foo.txt','*.txt')
# print(a) # True 출력
# b = fnmatch('foo.txt','?oo.txt')
# print(b) # True 출력
# name = ['Dat1.csv','Dat2.csv','config.ini','foo.py']
# c = [name for name in name if fnmatch(name,'Dat*.csv')]
# print(c) # ['Dat1.csv', 'Dat2.csv'] 출력
#
# # 2.4 텍스트 패턴 매칭과 검색
# # 문제
# # 특정 패턴에 대한 텍스트 매칭이나 검색을 하고 싶다
# # 해결
# # 매칭하려는 텍스트가 간단하다면 str.find(),str.endswith(),str.startswith()와 같은 기본적인 문자열 메소드만으로 충분!!!
# text = 'yeah, but no, but yeah, but no, but yeah'
# # 정확한 매칭
# a = text == 'yeah'
# print(a) # False 출력 # 왜냐하면 text는 yeah, but no,... 이기 때문!!!!!!!!!!!!!!!!!!!!!
#
# # 처음이나 끝에 매칭
# a = text.startswith('yeah')
# print(a) # True 출력
# b = text.endswith('no')
# print(b) # False 출력
# c = text.find('no')
# print(c) # 10 출력
# # 동일한 패턴으로 매칭을 많이 수행할 예정이라면 정규 표현식을 미리 컴파일해서 패턴 객체로 만들어 놓는 것이 좋다
# import re
# text1 = '11/27/2012'
# text2 = 'Nov 27, 2012'
# datepat = re.compile(r'\d+/\d+/\d+')
# if datepat.match(text1): # compile 해놓은 datepat으로 객체를 만드는 과정
#     print('yes')
# else:
#     print('no')
#
# if datepat.match(text2):
#     print('yes')
# else:
#     print('no')
#
# # match()는 항상 문자열 처음에서 찾기를 시도한다. 텍스트 전체에 걸쳐 패턴을 찾으려면 findall() 메소드를 사용한다
# # findall() 과 match() 의 차이점을 확인하고 findall() 함수를 잘쓰자!!!!!!!!!!!!!!!!!!!!!!!!!
# text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
# a = datepat.findall(text)
# print(a) # ['11/27/2012', '3/13/2013'] 출력
# # 정규 표현식을 정의할 때 괄호를 사용해 캡처 그룹을 만드는 것이 일반적!!!!!!!!!!!!!
# # 예제1)
# datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
# # 이렇게 캡처 그룹을 사용하면 매칭된 텍스트에 작업할 때 각 그룹을 개별적으로 추출할 수 있어서 편리하다!!
# m = datepat.match('11/27/2012')
# a = m.group(0)
# b = m.group(1)
# c = m.group(2)
# d = m.groups()
# print(a) # 0번째는 모두 출력!! 11/27/2012
# print(b) # 11 출력
# print(c) # 27 출력
# print(d) # ('11','27','2012') 출력
# # 전체 매칭 찾기
# month, day, year = m.groups()
# A =datepat.findall(text) # [('11', '27', '2012'), ('3', '13', '2013')] 출력
# print(A)
# for month,day,year in A:
#     print('{}-{}-{}'.format(year,month,day)) # 2012-11-27 / 2013-3-13 출력
# # 토론
# # 정규 표현식의 내용을 다 다룰순 없지만 기본적인 방법이니 이것만이라도 기억해보자!!
# # 간추리자면 re.compile()을 사용해 패턴을 저장하고,
# # 그것을 match(), findall(), finditer() 등에 사용하면 된다
# # 정확한 매칭을 할려면 $ 기호를 쓰자!!
#
# # 2.5 텍스트 검색과 치환
# # 문제
# # 문자열에서 텍스트 패턴을 검색하고 치환하고 싶다.
# # 해결
# # 간단한 패턴이라면 str.replace() 메소드를 사용하면 된다
# text = 'yeah, but no, but yeah, but no, but yeah'
# a = text.replace('yeah','yep')
# print(a) # yep, but no, but yep, but no, but yep 출력
# # 조금 더 복잡한 패턴을 사용하려면 re 모듈의 sub() 함수/메소드를 사용한다
# # 예를 들어 11/27/2012 를 2012-11-27 로 바꿔보자
# text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
# import re
# a = re.sub(r'(\d+)/(\d+)/(\d+)',r'\3-\1-\2',text) # 3/13/2013의 순서 1 / 2 / 3 이므로 3-1-2 순으로 표기한거임
# print(a) # Today is 2012-11-27. PyCon starts 2013-3-13. 출력
# # sub()에 전달한 첫번째 인자는 매칭을 위한 패턴이고 두번째 인자는 치환을 위한 패턴이다.
# # 숫자앞에 백슬래시가 붙어있는 표현은 패턴의 캡처그룹을 참조하자(나중에)
# # 만약 치환된 텍스트를 받기 전에 치환이 몇번발생했는지 알고싶다면 re.subn()을 사용하면된다
# # re.subn() re.subn() re.subn() re.subn() re.subn() -> 치환 몇번했는지 알랴줌
# newtext,n = datepat.subn(r'\3=\1-\2',text)
# # 치환 2번 했다고 출력해줌
# # 토론
# # 앞서 살펴본 sub() 메소드에 정규 표현식 검색과 치환 이외에 어려운 것은 없다.
# # 가장 이해하기 어려운 것이 정규표현식 패턴을 만드는 것이니까 열심히 하쟈
#
# # 2.6 대소문자를 구별하지 않는 검색과 치환
# # 문제
# # 텍스트를 검색하고 치환할 때 대소문자를 구별하지 않고 싶다
# # 해결
# # 텍스트 관련 작업을 할 때 대소문자를 구별하지 않기 위해서는 re 모듈을 사용하고
# # re.IGNORECASE 플래그를 지정해야한다??
# # 예제1)
# import re
# text = 'UPPER PYTHON, lower python, Mixed Python'
# a = re.findall('python',text,flags=re.IGNORECASE)
# print(a) # ['PYTHON', 'python', 'Python'] 출력
# b = re.sub('python','snake',text,flags=re.IGNORECASE)
# print(b) # UPPER snake, lower snake, Mixed snake 출력
# # 바꾸니까 snake 통일????
# # 원본과 똑같이 대소문자를 구분할려면?
# def matchcase(word):
#     def replace(m):
#         text = m.group()
#         if text.isupper():
#             return word.upper()
#         elif text.islower():
#             return word.lower()
#         elif text[0].isupper(): # 첫번쨰 자리가 대문자라면:
#             return word.capitalize() # 맨 앞에 대문자 출력하는 함수
#         else:
#             return word
#     return replace
# a = re.sub('python',matchcase('snake'),text,flags=re.IGNORECASE)
# print(a) # UPPER SNAKE, lower snake, Mixed Snake 출력
# # 토론
# # 대개 re.IGNORECASE 를 사용하는 것만으로 대소문자를 무시한 텍스트 작업에 무리가 없다.
# # 하지만 유니코드가 포함된 작업을 하기에는 부족할 수 있으므로 주의하자!!!
#
# # 2.7 가장 잛은 매칭을 위한 정규 표현식
# # 문제
# # 정규 표현식을 사용한 텍스트 매칭을 하고 싶지만 텍스트에서 가장 긴 부분을 찾아낸다.
# # 만약 가장 잛은 부분을 찾아내고 싶다면 어떻게 해야 할까??
# # 해결
# # 이런 문제는 문장 구분자에 둘러싸여 있는 텍스트를 찾을 때 종종 발견한다
# import re
# str_pat = re.compile(r'\"(.*)\"')
# text1 = 'Computer says "no."'
# a = str_pat.findall(text1)
# print(a) # ['no.'] 출력
# text2 = 'Computer says "no." Phone says "yes."'
# b = str_pat.findall(text2)
# print(b) # ['no." Phone says "yes.'] 출력
# # \" ~ \" 에 둘러쌓인 *은 기본적으로 탐욕(greedy)의 방식을 써서 가장 긴 문자를 출력할려고한다
# # 그러므로 *뒤에 ?를 붙이면 비탐욕의 방식으로 출력해준다
# str_pat1 = re.compile(r'\"(.*?)\"')
# b1 = str_pat1.findall(text2)
# print(b1) # ['no.', 'yes.'] 출력
# # 결국 *나 +에 ?를 붙여주면 정규 표현식의 매칭 알고리즘에게 가장 짧은 것을 찾도록 해준다
#
# # 2.8 여러 줄에 걸친 정규 표현식 사용
# # 문제
# # 여러줄에 걸친 정규 표현식 매칭을 사용하고 싶다
# # 해결
# # 이 문제는 점(.)을 사용한 텍스트 매칭을 할 때 이 문자가 개행문에 매칭하지 않는다는 사실을 잊었을때 발생!!
# # 예를 들어 다음과 같이 텍스트에서 C 스타일 주석을 찾아볼 때
# import re
# comment = re.compile(r'/\*(.*?)\*/')
# text1 = '/* this is a comment */'
# text2 = '''/* this is a multiline comment */'''
# a = comment.findall(text1)
# b = comment.findall(text2)
# print(a) # [' this is a comment '] 출력
# print(b) # [] 출력
# # text2에 C 스타일 주석이 포함되어 있지만 이를 찾아내지 못한다. 이 문제를 해결하려면 다음과 같이 패턴을 넣어야 한다
# comment = re.compile(r'/\*((?:.|\n)*?)\*/')
# a = comment.findall(text2)
# print(a) # [' this is a multiline comment '] 출력
# # 이 패턴에서 (?:.|\n)은 논캡처 그룹을 명시해주는것
# # 즉, 매칭의 목적은 명시하지만 개별적으로 캡처하거나 숫자를 붙이지는 않는다??
#
# # 2.11 문자열에서 문자 잘라내기
# # 문제
# # 텍스트의 처음, 끝, 중각에서 원하지 않는 공백문 등을 잘라내고 싶다.
# # 해결
# # strip() 메소드를 사용하면 문자열의 처음과 끝에서 문자를 잘라낼 수 있다.
# # lstrip() 과 rstip()은 문자열의 왼쪽과 오른쪽의 문자를 잘라낸다.
# # 기본적으로 이 메소드는 공백문을 잘라내지만 원하는 문자를 지정할 수도 있다
# # 공백문 잘라내기
# s = '     hello world \n'
# a = s.strip()
# print(a) # hello world 출력
# b = s.lstrip()
# print(b)
# c = s.rstrip()
# print(c) #      hello world 출력
#
# # 문자 잘라내기
# t = '-----hello====='
# b = t.lstrip('-')
# c =b.rstrip('=')
# print(c) # hello 출력
# # strip()은 일반적으로 잘 사용하지만 중간에서 잘라내기를 할 수는 없다
# # 중간 잘라내기를 하고싶다면 re.sub를 이용해 \s를 쓰면된다
# import re
# a = re.sub('\s+','',s)
# print(a) # helloworld 출력
# # 때로는 파일을 순환하며 데이터를 읽어 들이는 것과 같이 다른 작업과 문자열을 잘라내는 작업을 동시에 하고싶다면??
# # 이럴떄는 생성자 표현식을 사용하는 것이 좋음!!
# # 예제1)
# with open(filename) as f:
#     lines = (line.strip() for line in f)
#     for line in lines:
#         ...
#
# # 2.12 텍스트 정리
# # 문제
# # 당신의 웹 페이지에 어떤 사람이 장난스럽게 ajodf이라는 텍스트를 입력했다. 이를 정리하고 싶을 때는??
# # 해결
# # 텍스트를 정리하는 작업이 대개 텍스트 파싱과 데이터 처리와 관련이 있다.
# # 단순히 생각하면 기본적인 문자열 함수(upper()와 lower()를 사용해서 텍스트를 표준케이스로 변환하면 된다
# # 또는 normalize()를 사용해서 텍스트를 노멀화할 수도 있다
# remap ={ord('\t'):' ',ord('\f') :' ',ord('\r'):None}
# s = 'python\fis\tawesome\r\n'
# a = s.translate(remap)
# print(a) # python is awesome 출력
# # 앞에 나온 대로 \t와 \f는 띄어쓰기로 치환하고 \r은 삭제한다
# # 토론
# # 텍스트 정리를 하다보면 실행 성능문제에 직면하기도 한다. 당연하게도 간단한 작업일수록 실행 속도도 빠르다.
# # 간단한 치환을 하려면 replace() 메소드를 사용하는 것이 가장 빠르다
# def clean_spaces(s):
#     s = s.replace('\r','')
#     s = s.replace('\t',' ')
#     s = s.replace('\f',' ')
#     return s
# print(clean_spaces(a)) # python is awesome 출력

# # 2.13 텍스트 정렬
# # 문제
# # 텍스트를 특정 형식에 맞추어 정렬하고 싶다
# # 해결
# # 기본적인 정렬 메소드로 ljust(),rjust(),center() 등이 있다
# text = 'Hello World'
# a = text.ljust(20)
# print(a)
# b = text.rjust(20)
# print(b) #          Hello World 출력
# c = text.center(20)
# print(c) #     Hello World     출력
# # 앞에 나온 빈칸은 채워 넣기로 문자를 사용할수 있다
# a = text.rjust(20,'=')
# print(a) # =========Hello World  출력
# # 정렬에는 format()함수를 사용할 수도있다
# a = format(text,'>20')
# print(a) #          Hello World 출력
# # 즉 > 은 rjust < 은 ljust ^ 은 center를 의미
# # 포맷 코드는 format() 메소드에 사용해 여러 값을 서식화할 수도있다
# a = '{:>10} {:>10}'.format('Hello','World')
# print(a) #      Hello      World  출력
# # format()을 사용하면 문자열뿐만 아니라 숫자에도 작동한다
# x = 1.2345
# a = format(x,'>10')
# b = format(x,'^10.2f')
# print(a) #     1.2345 출력
# print(b) #    1.23   출력

# # 2.14 문자열 합치기
# # 문제
# # 작은 문자열 여러개를 합쳐 하나의 긴 문자열을 만들고 싶을때
# # 해결
# # 합치고자 하는 문자열이 시퀀스나 순환 객체 안에 있다면 join() 메소드를 사용하면 된다
# parts=['Is','Chicago','Not','Chicago?']
# a = ' '.join(parts)
# print(a) # Is Chicago Not Chicago?
# b = ','.join(parts)
# print(b) # Is,Chicago,Not,Chicago?
# c = ''.join(parts)
# print(c) # IsChicagoNotChicago?
# # 합치려고 하는 문자열의 수가 아주 적다면 + 를 사용하는 것으로 만족하자 !
# a = 'Is Chicago'
# b = 'Not Chicago?'
# print(a+' '+b) # Is Chicago Not Chicago?
# # 소스 코드에서 문자열을 합치려고 할때는 단순히 옆에 붙여놓기만 해도 된다
# a = 'Hello''World'
# print(a) # HelloWorld
# # 토론
# # 문자열 합치기가 그리 고급 주제가 아니라고 생각하지만 큰 영향을 준다
# # 명심할 것은 + 연산자로 많은 문자열을 합치려고 하면 비효율적이니 join()을 쓰자!!
# # 생성자 표현식으로 합치는 방법 또한 있다
# data = ['ACME',50,91.1]
# a = '.'.join(str(d) for d in data)
# print(a) # ACME.50.91.1
# # 함수로 코드를 작성한다면 이런 예도 있다
# def sample():
#     yield 'Is'
#     yield 'Chicago'
#     yield 'Not'
#     yield 'Chicago?'
# text = ''.join(sample())
# print(text) # IsChicagoNotChicago?
# # 입출력을 조합한 하이브리드 방식 구현도 가능하다
# def combin(source,maxsize):
#     parts=[]
#     size=0
#     for part in source:
#         parts.append(part)
#         size += len(part)
#         if size > maxsize:
#             yield ''.join(parts)
#             parts=[]
#             size=0
#     yield ''.join(parts)
# for part in combine(sample(),32768):
#     f.write(part)
# # 중요한 점은 생성자 함수가 미래의 구현 방식을 알지못하고 문자열을 제공할 뿐이다.

# # 2.15 문자열 변수 사용
# # 문제
# # 문자열에 변수를 사용하고 이 변수에 맞는 값을 채우고 싶다
# # 해결
# # 파이썬 문자열에 변수 값을 치환하는 간단한 방법은 존재하지 않는다.
# # 하지만 format() 메소드를 사용하면 비슷하게 흉내 낼수있다
# s = '{name} has {n} messages.'
# a = s.format(name='Thomas',n=37)
# print(a) # Thomas has 37 messages.name = 'Guido'
# # 혹은 치환할 값이 변수에 들어 있다면 format_map()과 vars()를 함꼐 사용하면 된다
# name = 'Guido'
# n = 37
# a = s.format_map(vars()) # 뭐야 이 신세계는......
# print(a) # Guido has 37 messages.
# # vars()에는 인스턴스를 사용할 수도 있다
# class Info:
#     def __init__(self,name,n):
#         self.name=name
#         self.n=n
#
# a = Info('Guido',37)
# print(s.format_map(vars(a))) # Guido has 37 messages. 출력
# # 머야 이 신세계는 ㅡㅡ...
# # format_map(vars())를 기억하쟈 format_map(vars()) format_map(vars())
# # 하지만 값이 빠져있다면 제대로 동작하지 않으니 절대로 빼먹지않고 꼼꼼히 확인하자!!
# # 그래도 빠져나갈 구멍이 있단다
# class safesub(dict):
#     def __missing__(self, key):
#         return '{' + key + '}'
# del n
# print(s.format_map(safesub(vars())) # Guido has {n} messages. 출력
# # 뭐야 이거....개 신기해.....미쳐따ㅓㄹ맨ㅇ러ㅐ먄어래냐ㅓㄹㅇ
# # 토론
# 파이썬 자체에서 변수 보간법이 존재하지 않아서 다양한 대안이 있기에 책을 많이 훑어보자!!

# 2.16 텍스트 열의 개수 고정
# 문제
# 긴 문자열의 서식을 바꿔 열의 개수를 조절하고 싶다
# 해결
# textwrap 모듈을 사용해서 텍스트를 재서식화한다
s = "Look into my eyes, look into my eyes, the eyes, the eyes,"\
    "the eyes, not around the eyes, don't look around the eyes,"\
    "look into my eyes, you're under."
import textwrap
print(textwrap.fill(s,70))
print(textwrap.fill(s,20)) # (s,숫자)의 숫자가 width를 의미!!
print(textwrap.fill(s,40,initial_indent='          '))
#            Look into my eyes, look into
# my eyes, the eyes, the eyes,the eyes,
# not around the eyes, don't look around
# the eyes,look into my eyes, you're
# under. 출력
# 즉, initial_indent는 첫 줄에 '       ' 을 주겠다

print(textwrap.fill(s,40,subsequent_indent='              '))
# Look into my eyes, look into my eyes,
#               the eyes, the eyes,the
#               eyes, not around the eyes,
#               don't look around the
#               eyes,look into my eyes,
#               you're under. 출력
# 즉, subsequent_indent는 첫줄을 제외한 sub 줄에 '            ' 을 주겠다
# 토론
# 텍스트를 출력하기 전에 textwrap 모듈을 사용하면 깔끔하게 서식을 맞출 수 있다.
# 특히 터미널에 사용할 텍스트에 적합하다.


