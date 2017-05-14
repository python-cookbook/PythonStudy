#=======================================================================================================================
# 2.1 여러 구분자로 문자열 나누기
# 문자열을 필드로 나누고 싶지만 구분자(그리고 그 주변의 공백)가 문자열에 일관적이지 않다.
# ㄴsplit() 메소드는 아주 간단한 상황에 사용하도록 설계되었고, 여러개의 구분자나 주변 공백까지 고려하진 않는다.
#   때문에 re.split() 메소드가 필요하다
#=======================================================================================================================
line = 'asdf fjdk; afed, fjek,asdf,            foo'
import re
re.split(r'[;,\s]\s*', line)                                 # 쉼표, ;등 분리 구문마다 여러 패턴을 명시할 수 있다.

## re.split() 사용시에는 (괄호)안에 묶인 정규 표현식 패턴이 캡처 그룹이 된다는 점에 주의해야 한다
fields = re.split(r'(;|,|\s)\s*', line)
print(fields)

values = fields[::2]
delimiters = fields[1::2] + ['']
print(values)
print(delimiters)

# 동일한 구분자로 라인을 구성한다
print(''.join(v+d for v,d in zip(values, delimiters)))

print(re.split(r'(?:,|;|\s)\s*', line))


#=======================================================================================================================
# 2.2 문자열 처음이나 마지막에 텍스트 매칭
# 문자열의 처음이나 마지막에 파일 확장자, URL scheme 등 특정 텍스트 패턴이 포함되었는지 검사하고 싶다.
# ㄴstr.startswith()나 str.endswith()가 있다
#=======================================================================================================================
filename = 'spam.txt'
print(filename.endswith('.txt'))
print(filename.startswith('file:'))

# 여러 개의 선택지를 검사해야 한다면 검사하고 싶은 값을 튜플에 담아 startswith()나 endswith()에 전달한다
import os
filenames = os.listdir('.')
print(filenames)

print([name for name in filenames if name.endswith(('.c', '.h'))])

## 얘는 튜플만 입력받음
from urllib.request import urlopen

def read_data(name):
    if name.startswith(('http:','https:','ftp:')):
        return urlopen(name).read()
    else:
        with open(name) as f:
            return f.read()

## 정규 표현식을 사용해서 할 수 있다
import re
url = 'http://www.python.org'
re.match('http:|https:|ftp:', url)

#=======================================================================================================================
# 2.3 쉘 와일드카드 패턴으로 문자열 매칭
# Unix 쉘에 사용하는 것과 동일한 와일드카드 패턴을 텍스트 매칭에 사용하고 싶다
# ㄴfnmatch 모듈에 두 함수 fnmatch()와 fnmatchcase()를 쓰면 된다.
#=======================================================================================================================
from fnmatch import fnmatch, fnmatchcase
# print(fnmatch('foo.txt', '*.txt'))
# print(fnmatch('foo.txt', '?oo.txt'))
print(fnmatch('Dat45.csv','Dat[0-9]*'))

names = ['Dat1.csv','Dat2.csv','config.ini','foo.py']
print([name for name in names if fnmatch(name, 'Dat*.csv')])


#=======================================================================================================================
# 2.4 텍스트 패턴 매칭과 검색
# 특정 패턴에 대한 텍스트 매칭이나 검색을 하고 싶다
#=======================================================================================================================

# 매칭 텍스트가 간단하다면 str.find(), str.endswith(), str.startswith()와 같은 기본 문자열 메소드만으로 충분함
text = 'yeah, but no, but yeah, but no, but yeah'

# 정확한 매칭
print(text == 'yeah')

# 처음이나 끝에 매칭
print(text.startswith('yeah'))
print(text.endswith('no'))

# 처음 나타난 곳 검색
print(text.find('no'))


text1 = '11/27/2012'
text2 = 'Nov 27, 2012'

import re
# 간단한 매칭 : \d+는 하나 이상의 숫자를 의미
if re.match(f'\d+/\d+/\d+', text1):
    print('yes')
else:
    print('no')


# 동일한 패턴으로 매칭을 많이 수행할 예정이라면 정규 표현식을 미리 컴파일해서 패턴 객체로 만들어놓는 것이 좋다
datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')


# match()는 항상 문자열 처음에서 찾기를 시도한다. 텍스트 전체에 걸쳐 패턴을 찾으려면 findall() 메소드를 사용한다.
text = 'Today is 11/27/2012. PyCon starts 3/13/2013'
print(datepat.findall(text))

## 정규 표현식을 정의할 때, 괄호를 사용해 캡처 그룹을 만드는게 일반적이다
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
print(datepat)

# 캡처 그룹을 사용하면 매칭된 텍스트에 작업할 때 각 그룹을 개별적으로 추출할 수 있어 편리하다
m = datepat.match('11/27/2012')
print(m)

print(m.group(0))
print(m.group(1))
print(m.group(2))
print(m.group(3))
print(m.groups())


# 전체 매칭 찾기 (튜플로 나눈다)
datepat.findall(text)
for month, day, year in datepat.findall(text):
    print('{}-{}-{}'.format(year, month, day))

## findall() 메소드는 텍스트를 검색하고 모든 매칭을 찾아 리스트로 반환한다. 한 번에 결과를 얻지 않고 텍스트를 순환하며
# 찾으려면 finditer()를 사용한다
for m in datepat.finditer(text):
    print(m.groups())

# 간단한 텍스트 매칭/검색을 수행하려 한다면 컴파일 과정을 생략하고 re 모듈의 모듈 레벨 함수를 바로 사용해도 좋다
re.findall(r'(\d+)/(\d+)/(\d+)', text)


#=======================================================================================================================
# 2.5 텍스트 검색과 치환
# 문자열에서 텍스트 패턴을 검색하고 치환하고 싶다
# 간단한 패턴이라면 str.replace() 메소드를 사용한다
#=======================================================================================================================
text = 'yeah, but no, but yeah, but no, but yeah'
print(text.replace('yeah','yep'))

## 좀 더 복잡한 패턴을 사용하려면 re.sub()를 쓴다
text = 'Today is 11/27/2012. PyCon starts 3/13/2013'
import re
print(re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text))


import re
datepat = re.compile(r'(\d+)/(\d+)/(\d+)/(\d+)')
print(datepat.sub(r'\3-\1-\2', text))


## 더더 복잡한 치환을 하려면 콜백 함수를 명시한다
from calendar import month_abbr
def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))

print(datepat.sub(change_date, text))


# 인자가 되는 치환 콜백은 match()나 find()에서 반환한 매치 객체를 사용한다. 매치에서 특정 부붕늘 추출하려면 .group()
# 메소드를 사용한다. 이 함수는 치환된 텍스트를 반환하여야 한다.


#=======================================================================================================================
# 2.6 대소문자를 구별하지 않는 검색과 치환
# 텍스트를 검색하고 치환할 때 대소문자를 구별하지 않고 싶다
# re의 re.IGNORECASE 플래그를 지정해야 한다.
#=======================================================================================================================
text = 'UPPER PYTHON, lower python, Mixed Python'
# print(re.findall('python', text, flags=re.IGNORECASE))
print(re.findall('python', text, flags=re.IGNORECASE))
print(re.sub('python', 'snake', text, flags=re.IGNORECASE))

# 결과값을 보면 치환된 텍스트의 대소문자가 원본과 일치하지 않는다. 이를 수정하기 위한 함수
def matchcase(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text.isupper():
            return word.capitalize()
        else:
            return word
    return replace

print(re.sub('python', matchcase('snake'), text, flags = re.IGNORECASE))


#=======================================================================================================================
# 2.7 가장 짧은 매칭을 위한 정규 표현식
# 정규 표현식을 사용한 텍스트 매칭을 하고 싶지만 텍스트에서 가장 긴 부분을 찾아낸다. 만약 가장 짧은 부분을 찾고 싶다면?
# 이런 문제는 문장 구분자에 둘러싸여 있는 텍스트를 찾을 때 종종 발생한다.
#=======================================================================================================================
import re
str_pat = re.compile(r'\"(.*?)\"')
text1 = 'Computer says "no"'
print(str_pat.findall(text1))

text2 = 'Computer says "no" Phone says "yes"'
print(str_pat.findall(text2))


#=======================================================================================================================
# 2.8 여러 줄에 걸친 정규 표현식 사용
#=======================================================================================================================
comment = re.compile(r'/\*((?:.|\n)*?)\*/')
text1 = '/* this is a comment */'
text2 = '''/* this is a
                multiline comment */'''

print(comment.findall(text2))

## 이 패턴에서 (?:.|\n)은 noncapture group을 명시한다
comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)
print(comment.findall(text2))


#=======================================================================================================================
# 2.9 유니코드 텍스트 노멀화
# 유니코드 문자열 작업을 하고 있다. 이때 모든 문자열에 동일한 표현식을 갖도록 보장하고 싶다
#=======================================================================================================================
s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'
print(s1)
print(s2)
print(s1 == s2)

print(len(s1))
print(len(s2))


import unicodedata
t1 = unicodedata.normalize('NFC', s1)           # NFC는 문자를 정확히 구성하도록 지정한다 (가능하다면 단일 코드 사용)
t2 = unicodedata.normalize('NFC', s2)
print(t1 == t2)
print(ascii(t1))

t3 = unicodedata.normalize('NFD', s1)           # NFD는 문자를 여러개 합쳐서 사용하도록 지정한다
t4 = unicodedata.normalize('NFD', s2)
print(t3 == t4)
print(ascii(t3))


## 텍스트에서 발음 구별 부호 모두 제거하기
t1 = unicodedata.normalize('NFD', s1)
print(''.join(c for c in t1 if not unicodedata.combining(c)))

# combining() 함수는 문자가 결합 문자인지 확인한다. 이 모듈에는 문자 카테고리를 찾고 숫자를 확인하는 등 많은 함수가 있다.


#=======================================================================================================================
# 2.10 정규 표현식에 유니코드 사용
# 텍스트 프로세싱에 정규 표현식을 사용 중이다. 하지만 유니코드 처리가 걱정된다.
# 기본적인 유니코드 처리를 위한 대부분의 기능을 re 모듈이 제공한다.
#=======================================================================================================================
import re
num = re.compile('\d+')
print(num.match('123'))

print(num.match('\u0661\u0662\u0663'))

## 유니코드와 정규 표현식을 함께 사용하겠다면 서드파티의 regex 라이브러리를 설치하고 유니코드 대소문자 변환등을 기본으로
# 제공하는 많은 기능을 이용하는 것이 좋다.


#=======================================================================================================================
# 2.11 문자열에서 문자 잘라내기
# 텍스트의 처음, 끝, 중간에서 원하지 않는 공백문 등을 잘라내고 싶다
# strip() 메소드를 사용하면 문자열의 처음과 끝에서 문자를 잘라낼 수 있다.
#=======================================================================================================================
s = '    hello world \n'
print(s.strip())

t = '----------hello========='
print(t.lstrip('-'))
print(t.strip('-='))

# 다만 텍스트 중간에서 잘라내기를 할 수는 없다.

## 파일을 불러들이면서 문자열을 잘라내는 작업을 동시에 하고 싶을 수 있다. 생성자 표현식을 쓰면 된다.
with open(filename) as f:
    lines = (line.strip() for line in f)
    for line in lines:
        ...


#=======================================================================================================================
# 2.12 텍스트 정리
# 온통 발음기호인 문자를 정리하는 방법
#=======================================================================================================================
## 결합문자를 모두 없애보자
import unicodedata
import sys
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode)
                         if unicodedata.combining(chr(c)))

b = unicodedata.normalize('NFD', a)
print(b)


digitmap = {c: ord('0') + unicodedata.digit(chr(c))
            for c in range(sys.maxunicode)
            if unicodedata.category(chr(c)) == 'Nd'}
print(len(digitmap))


x = '\u0661\u0662\u0663'
print(x.translate(digitmap))


## 간단한 치환을 하려면 str.replace() 메소드를 사용하는 것이 가장 빠르다.
def clean_spaces(s):
    s = s.replace('\r', '')
    s = s.replace('\t', ' ')
    s = s.replace('\f'. ' ')
    return s

## translate() 메소드는 복잡한 문자 remapping이나 삭제에 사용하면 아주 빠르다



#=======================================================================================================================
# 2.13 텍스트 정렬
# 텍스트를 특정 형식에 맞추어 정렬하고 싶다
#=======================================================================================================================

## 기본적인 정렬 메소드로 ljust(), rjust(), center() 등이 있다
text = 'Hello world'
print(text.ljust(20))
print(text.rjust(20))
print(text.center(20))


print(format(text, '>20'))
print(format(text, '<20'))
print(format(text, '^20'))


#=======================================================================================================================
# 2.14 문자열 합치기
# 작은 문자열 여러개를 합쳐 하나의 긴 문자열을 만들고 싶다
# 합치고자 하는 문자열이 시퀀스나 순환 객체 안에 있다면 join() 메소드를 사용하는 것이 가장 빠르다
#=======================================================================================================================
parts = ['Is','Chicago','Not','Chicago?']
print(''.join(parts))
print(','.join(parts))
print(' '.join(parts))

## 구분 문자열을 지정하고 거기에 join() 메소드를 한 번만 사용하면 문자열을 모두 합친다
## 문자열을 변환한 다음, 생성자 표현식으로 합치는 방법이 있다
data = ['ACME', 50, 91.1]
print(','.join(str(d) for d in data))

# 문자열 합치기는 이렇게 하세욥
print(a,b,c, sep=':')

## 수많은 짧은 문자열을 합쳐 하나로 만드는 코드를 작성한다면 yield를 사용한 생성자 함수를 고려해보자
def sample():
    yield 'Is'
    yield 'Chicago'
    yield 'Not'
    yield 'Chicago?'

print(sample())


## 입출력을 조합한 하이브리드 방식 구현도 가능하다
def combine(source, maxsize):
    parts = []
    size = 0
    for part in source:
        parts.append(part)
        size += len(part)
        if size > maxsize:
            yield ''.join(parts)
            parts = []
            size = 0
    yield ''.join(parts)

for part in combine(sample(), 32768):
    f.write(part)


#=======================================================================================================================
# 2.15 문자열에 변수 사용
# 문자열에 변수를 사용하고 이 변수에 맞는 값을 채우고 싶다
# format() 메소드를 사용하면 비슷하게 흉내낼 수 있다
#=======================================================================================================================
s = '{name} has {n} messages'
print(s.format(name = 'Guido', n = 37))

## 치환할 값이 변수에 들어 있다면 format_map()과 vars()를 함께 사용하면 된다
name = 'Guido'
n = 37
print(s.format_map(vars()))


## vars()에는 인스턴스를 사용할 수도 있다
class Info:
    def __init__(self, name, n):
        self.name = name
        self.n = n

a = Info('Guido', 37)
print(s.format_map(vars(a)))

class safesub(dict):
    def __missing__(self,key):
        return '{'+key+'}'

del n
print(s.format_map(safesub(vars())))

## 코드에서 변수 치환을 번번히 사용할 것 같으면 치환하는 작업을 유틸리티 함수에 모아놓고 frame hack으로 쓸 수 있다
import sys
def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))      # f_locals는 호출 함수의 지역변수 복사본을 담아둔
                                                                    # 딕셔너리이다.
name = 'Guido'
n = 32
print(sub('Hello {name}'))

## 템플릿을 사용한 방법도 있다
import string
s = string.Template('$name has $n messages')
print(s.substitute(vars()))


#=======================================================================================================================
# 2.16 텍스트 열의 개수 고정
# 긴 문자열의 서식을 바꿔 열의 개수를 조절하고 싶다
# textwrap 모듈을 사용해서 텍스트를 재서식화(reformat)한다.
#=======================================================================================================================
s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
    the eyes, not around the eyes, don't look around the eyes,\
    look into my eyes, you're under"

import textwrap
# print(textwrap.fill(s, 70))
# print(textwrap.fill(s, 40))

# print(textwrap.fill(s, 40, initial_indent='          '))
print(textwrap.fill(s, 40, subsequent_indent='       '))


## 텍스트를 출력하기 전에 textwrap 모듈을 사용하면 깔끔하게 서식을 맞출 수 있다. 특히 터미널에 사용할 텍스트에 적합
# 터미널의 크기를 알려면 os.get_terminal_size()를 쓴다
import os
os.get_terminal_size().columns
