
"""
▶ 2.9 유니코드 텍스트 노멀화 ◀ 
♣ 문제 : 유니코드 문자열 작업을 하고 있다. 이때 모든 문자열에 동일한 표현식을 갖도록 보장하고 싶다면?
 ↘ 해결 : 유니코드에서 '몇몇' 문자는 '하나 이상의 유효한 시퀀스 코드 포인트' 로 표현할 수 있다.
        
            필요한 것   
                        import unicodedata
                        normalization 메소드    # 첫번째 인자에는 문자열을 어떻게 노멀화할것인지
                                                # ex) NFC = 문자를 정확히 구성하도록 지정
                                                      NFD = 문자를 여러 개 합쳐서 사용하도록 지정
                                                      NFKC = 분리..?
                                                      NFKD = 분리..?
                        
 """
print('########################################## 2.9 유니코드 텍스트 노멀화 #####################################')

s1 = 'Spicy Jalape\u00f1o'  # (U + 00F1)
s2 = 'Spicy Jalapen\u0303o' # (U + 0303)
print(s1)
print(s2)

print(s1 == s2) # False

print(len(s1))
print(len(s2))


# 여러 표현식을 갖는다는 것은 문자열을 비교하는 프로그램의 측면에서 문제가 된다.
# 문제를 해결하기 위해서는 unicodedata 모듈로 텍스트를 노멀라이제이션 해서
# '표준 표현식'으로 바꿔야 한다.

import unicodedata

# NFC 노멀라이제이션
t1 = unicodedata.normalize('NFC', s1)           #NFC = 문자를 정확히 구성하도록 지정
t2 = unicodedata.normalize('NFC', s2)
print(t1) #Spicy Jalapeño
print(t2) #Spicy Jalapeño
print(ascii(t1)) #'Spicy Jalape\xf1o'
print(ascii(t2)) #'Spicy Jalape\xf1o'
print(t1==t2) #return True

# NFD 노멀라이제이션
t3 = unicodedata.normalize('NFD',s1)            #NFD = 문자를 여러 개 합쳐서 사용하도록 지정
t4 = unicodedata.normalize('NFD',s2)
print(t3) #Spicy Jalapeño
print(t4) #Spicy Jalapeño
print(ascii(t3)) #'Spicy Jalapen\u0303o'
print(ascii(t4)) #'Spicy Jalapen\u0303o'
print(t3==t4) # Return True

s = '\ufb01'  #단일 문자
print(s)
s = unicodedata.normalize('NFD',s)
print(s) #ﬁ  <<얘랑 아래 분리한 애는 fi  하나는 붙여서 1바이트, 하나는 분리시켜서 2바이트 ㅋㅋ

#합쳐 놓은 문자가 어떻게 분리되는지 살펴본다.
t3 = unicodedata.normalize('NFKD',s)
t4 = unicodedata.normalize('NFKC',s)
print(t3)
print(t4)


# 일관적이고 안전한 유니코드 텍스트 작업을 위해서 노멀화는 아주 중요하다.
# 특히 '인코딩' 을 조절할 수 없는 상황에서 사용자에게 문자열 입력을 받는 경우엔 특히 조심해야 한다.
# 또한 텍스트 필터링 작업을 할 때도 노멀화는 중요하다.
# 예를 들어, 텍스트에서 발음 구별부호를 모두 제거하고 싶다면 다음과 같이 해야 한다.

s1 = 'Spicy Jalape\u00f1o'  # (U + 00F1)
s2 = 'Spicy Jalapen\u0303o' # (U + 0303)
t1 = unicodedata.normalize('NFD',s1)
d = ''.join(c for c in t1 if not unicodedata.combining(c))
# combining() 함수는 문자가 결합 문자인지 확인한다. 이 함수 안에는, 문자 카테고리찾기/숫자찾기 등 많은 함수가 들어있다.
# join 은 특정 구분자를 포함해 문자열으로 변환한다.
print(d)            # Spicy Jalapeno






"""
▶ 2.10 정규 표현식에 유니코드 사용 ◀ 
♣ 문제 : 텍스트 프로세싱에 정규 표현식을 사용 중이다. 하지만 유니코드 문자 처리가 걱정될때에는?
 ↘ 해결 : re 모듈을 통해 정규표현식을 적용한다. 
            예를 들어, \d는 유니코드 숫자에 이미 매칭한다.
            
    주의사항 : 유니코드의 대소문자 매칭에 주의!             #같은 유니코드에 upper()를 하면 글자가 바뀌어버림
    
    third-party regex 라이브러리 설치 추천 (유니코드 핸들링 유용)
 """
print('########################################## 2.10 정규 표현식에 유니코드 사용 #####################################')

import re
num = re.compile('\d+')

#   아스키(ASCII)숫자
a = num.match('123')
print(a) #<_sre.SRE_Match object; span=(0, 3), match='123'>

#   아라비아 숫자
b = num.match('\u0661\u0662\u0663')  #123...?
print(b) #<_sre.SRE_Match object; span=(0, 3), match='١٢٣'>


# 특정 유니코드 문자를 패턴에 포함하고자 한다면??
# >> 유니코드 문자에 escape 시퀀스를 사용한다.
# 예를 들어, 아라비아 코드 페이지의 모든 문자에 매칭하는 정규표현식은 다음과 같다.

arabic = re.compile('[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]+')    #모든 문자에 매칭하는 정규 표현식

# 검색 수행 전 '텍스트 노멀화'를 꼭 하는 것이 좋다.
# 주의사항으로, 대소문자 무시매칭에 대소문자 변환을 합친 코드가 좋다.
print('stra\u00dfe')   #straße
pat = re.compile('stra\u00dfe', re.IGNORECASE)
s = 'straße'
d = pat.match(s)
print(d)   # <_sre.SRE_Match object; span=(0, 6), match='straße'> ===>  일치

# 대문자로 변환 후 매치해보기 결과는?
print(s.upper())  #  STRASSE
print(s.lower())
e = pat.match(s.upper())
print(e)   # None ===>   불일치  !! 왜??
# 즉   stra\u00dfe <패턴은 straße < 얘를 일치시키는데,
# upper를 갈겨놓으면  STRASSE << 이렇게 변해서, 불일치!!


######### 유니코드와 정규표현식을 사용해야 한다면,
######### 서드파티(third-party) regex 라이브러리를 설치 후
######### 유니코드 대소문자 변환 등을 기본으로 제공하는 많은 기능 이용 추천






"""
▶ 2.11 문자열에서 문자 잘라내기 ◀ 
♣ 문제 : 텍스트의 처음, 끝, 중간에서 원하지 않는 공백문 등을 잘라내고 싶다.
 ↘ 해결 : strip() 메소드를 사용하면 문자열의 처음과 끝에서 문자를 잘라낼 수 있다. 
           lstrip() 과 rstrip()은 문자열의 왼쪽과 오른쪽의 문자를 잘라낸다.
           기본적으로 이 메소드는 공백문을 잘라내지만 원하는 문자를 지정할 수도 있다.
 """
print('########################################## 2.11 문자열에서 문자 잘라내기 #####################################')

# 공백문 잘라내기!

s = '        hello world \n'
a = s.strip()
b = s.lstrip()
c = s.rstrip()
print(a)
print(b)
print(c)
####### >> '         ' 도 잘라낼 수 있고, \n도 잘라낼 수 있다!

# 문자 잘라내기!

t = '----------hello==========='
a = t.lstrip('-')
b = t.rstrip('=')
c = t.strip('-=')
print(a)
print(b)
print(c)

#########    데이터를 보기 좋기 만들기 위한 용도로 여러 strip() 메소드를 일반적으로 사용함
#########    ex ) 문자열에서 공백문을 없애거나 인용 부호를 삭제하거나 하는 식이다.
#########    하지만 텍스트의 중간에서 잘라내기를 할 수는 없다.


s = '  hello          world     \n'
d = s.strip()      #hello          world
print(d)

#위 코드는 문자열 중간의 공백문이 사라지지 않았다. 이 부분을 처리하려면 replace() 나 정규표현식 치환을 해야 함.

d = s.replace(' ', '')
print(d)
import re
e = re.sub('\s+', ' ', s)
print(e)

# 때로는 파일을 순환하며 데이터를 읽어 들이는 것과 같이 다른 작업과 문자열을
# 잘라내는 작업을 동시에 하고 싶을 수가 있다.
# 이럴 때는 생성자 표현식 사용하는게 좋음

with open("d:/data/emp2.csv") as f:
    lines = (line.strip() for line in f)  # 데이터 변환 담당, 임시 리스트로 만들지 않고 바로 하니까 효율적
    for line in lines:                    # 단지 잘라내기 위한 작업이 적용된 라인을 순환하느 이터레이터 생성할 뿐
        print(line)

# 추가적인 기술은 translate() 메소드가 있다.



"""
▶ 2.12 텍스트 정리 ◀ 
♣ 문제 : 웹페이지에 어떤 사람이 유니코드 텍스트를 입력했다. 이를 정리하고 싶다.
 ↘ 해결 : 텍스트 정리 작업은 크게        1. 텍스트 파싱           2. 데이터 처리 와 관련 있음
           단순한건?      str.upper , str.lower 로 텍스트를 표준케이스로 변환
             또는         str.replace() , re.sub()를 사용한 치환은 특정 문자 시퀀스를 없애거나 바꾸는데 집중할 수 있음
            또는       unicodedata.normalize() 를 사용해서 텍스트 노멀화 시킬 수 있다.
            
            하지만 더 고급적인 게 있음.
            ex) 특정 범위의 문자 or 발음 구별 구호를 없애려고 할 때는 str.translate() 메소드를 사용해야 한다.
            
 """
print('########################################## 2.12 텍스트 정리 #####################################')



s = 'p\xfdt\u0125\xf6\xf1\x0cis\tawesome\r\n'
print(s)
print(s)

# 문자열에서 공백문을 잘라내보기
# 1. 먼저 작은 변환 테이블을 만들어야 한다.
remap = {
    ord('\t') : ' ',
    ord('\f') : ' ',
    ord('\r') : None      # 삭제됨
}

#############################################

a = s.translate(remap)
print('whitespace remapped:', a)


import unicodedata
import sys
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode)
                         if unicodedata.combining(chr(c)))

b = unicodedata.normalize('NFD', a)
c = b.translate(cmb_chrs)
print('accents removed:', c)


d = b.encode('ascii','ignore').decode('ascii')
print('accents removed via I/O:', d)














"""
▶ 2.13 텍스트 정렬 ◀ 
♣ 문제 : 텍스트를 특정 형식에 맞추어 정렬하고 싶다. 
 ↘ 해결 : 기본적인 정렬 메소드          ljust(), rjust(), center() 등이 있다.
            위 메소드는 채워넣기도 가능하다.   
                ex) STRING.center(20,'*')  = ****Hello World*****
            format함수로 텍스트정렬할 수 있다. 
                ex) format(STRING, '^20')                 # < 우측정렬  /  > 좌측정렬   / ^ 가운데정렬
            format역시 채워넣기 가능하다.
                ex) c = format(text, '=>20s')    =          '=========Hello World'
                
            결론 : 텍스트를 서식화 하는데 %나 연산자 사용보다 format이 강력
                   즉, format을 사용해서 더욱 더 일반적인 목적에 사용할 수 있도록 객체를 동작시키자.
 """
print('########################################## 2.13 텍스트 정렬 #####################################')



text = 'Hello World'
a = text.ljust(20)
print(a,'얼마나?')         #20바이트 먹은듯

#ljust(), rjust(), center()는 채워넣기 문자를 사용할 수 있다.

append_text = text.rjust(20,'=')  # 빈 공간을 =로 채워넣어라.
print(append_text)
center_append = text.center(20,'*')
print(center_append)


#정렬에   format() 함수를 사용할 수도 있다.
#인자로 <  , > , ^ 를 적절하게 사용해주면 된다.

a = format(text,'>20')     #우측정렬
b = format(text,'<20')     #좌측정렬
c = format(text,'^20')     #가운데정렬
print(a,b,c)


#공백 대신 특정 문자를 채워 넣고 싶다면 정렬 문자 앞에 그 문자를 지정한다.
c = format(text, '=>20s')
print(c)
d = format(text, '*^20s')     #*별로 채우며, 가운데 정렬(^) 하며, 20byte크기로.
f = format(text, '*^20')      #여기 s는 왜 붙이는 걸까?
print(type(d))
print(type(f))

# 앞의 포맷 코드는 format() 메소드에 사용해 여러 값을 서식화 할 수도 있다.
g = '{:>10s} {:>10s}'.format('Hello', 'World')
print(g)

# format()을 사용하면 문자열뿐만 아니라 숫자 값 등 모든 값에 동작한다.
x = 1.2345
c = 1.5262
d = format(x, '>10')
f = format(c, '<10')
print(d,f)

# 오래된 코드를 보면 % 연산자를 사용해 텍스트를 서식화 하기도 했다.
g = '%-20s ' % text
h = '%20s' % text
print(g,'g',h,'h')

# 요즘 작성하는 코드에서는 format()함수 or 메소드를 선호
# format은 강력하다.









"""
▶ 2.14 문자열 합치기 ◀ 
♣ 문제 : 작은 문자열 여러 개를 합쳐 하나의 긴 문자열을 만들고 싶다. 
 ↘ 해결 : 합치고자 하는 문자열이 시퀀스or 순환객체 안에 있다면 join() 메소드를 사용하는 것이 가장 빠르다.
            join()  :  문자열을 합치는 메소드
                        
 """
print('########################################## 2.14 문자열 합치기 #####################################')


parts = ['Is','Chicago','Not','Chicago?']
d = ' '.join(parts)
print(d)  #Is Chicago Not Chicago?
e = ','.join(parts)
print(e) #Is,Chicago,Not,Chicago?
g = ''.join(parts)
print(g) #IsChicagoNotChicago?


# join으로 문자열을 합치는데 사용한다.
# 그런데, 데이터 시퀀스 안에 얼마나 많은 객체의 갯수들이 있는지 모르는데
# 매번 호출하는 것은 불필요함.
# 따라서, 구분 문자열을 지정하고, 거기에 join() 메소드를 한번만 사용하면 문자열을 모두 합친다.

# 합치려고 하는 문자열의 수가 아주 적다면 +를 사용하는 것만으로도 충분하다.

a = 'Is Chicago'
b = 'Not Chicago?'
print(a+' '+b)  #Is Chicago Not Chicago?

# + 연산자는 조금 더 복잡한 문자열 서식 연산에 사용해도 잘 동작한다.

print('{} {}'.format(a,b))
print(a+' '+b)

# 소스 코드에서 문자열을 합치려고 할 떄는 단순히 옆에 붙여 놓기만 해도 된다.
a = 'Hello' 'World'
print(a)


# 문자열 합치기의 방법은 많지만, 프로그래머들의 선택에 의해 성능에 큰 영향을 주기도 하는 중요한 분야이다.
# 우선적으로 명심해야 할 부분은  !!
# + 연산자로 많은 문자열을 합치려고 하면
# 메모리 복사와 가비지 컬렉션(garbage collection) 으로 인해 매우 비효율적이라는 점이다.
# 다시 말해 다음과 같은 문자열 합치기 코드를 작성하지 말아야한다.

print('아래와 같은 코드는 작성하지말자')
s = ''
for p in parts:
    s += p
print(s)

# 위 방법은 join() 메소드보다 실행 속도가 약간 느린데,
# 이는 +=연산자가 새로운 문자열 객체를 만들어 내기 때문이다
# 이보다는 문자열을 한데 모아놓고 한번에 합치는 편이 더 효율적이다.




# 이와 관련 있는 기술로 데이터를 문자열로 변환한 다음,
# 1.13의 생성자 표현식으로 합치는 방법이 있다.

# 리스트 안에 문자열과 숫자형이 있을 때 생성자 표현식으로 합치기
data = ['ACME',50, 91.1]
# d = ','.join(d for d in data)  # TypeError: sequence item 1: expected str instance, int found
e = ','.join(str(d) for d in data)
j = ' '.join(str(data))
print(e)
print(j)


# 불필요한 문자열 합치기를 하고 있지 않은지도 주의해야 한다.
# 다음 예를 본다면?

print('a'+':'+'b'+':'+'c')          #제일 BAD
print(':'.join(['a','b','c']))      #별로
print(':'.join([str(a) for a in ['a','b','c']])) #썩 별로
print('a','b','c', sep=':')          #제일 추천


#입출력 동작과 문자열 합치기를 함께하는 방식은 고민해봐야 함.
#다음 두 코드 보기
#
# print('첫 버전  (문자열 합치기)')
# g = f.write(chunk1+chunk2)
#
#
#
# print('둘 버전 (개별 입출력 수행)')
# f.wirte(chunk1)
# f.write(chunk2)

# 두 문자열이 작다면, 첫번째 코드 사용하는 것이 성능측면에서 유리하다.
# 입출력 시스템 호출하는데 비용이 들기 때문이다.
# 문자열의 길이가 길다면, 두번째가 효율적일 수 있다.
# 아무튼 결국은 프로그래머의 선택임


def sample():
    yield 'IS'
    yield 'Chicago'
    yield 'Not'
    yield 'Chicago?'

print(sample())

#위 방식이 흥미로운 점은, 합칠 예정인 문자열은 있으나, 아직 조립 전의 상태라는 것
#다음과 같이 응용할 수 있다.

text = ' '.join(sample())
print(text)

# 혹은 문자열을 입출(I/O)으로 redirect할 수 있다.

# for part in sample():
    # f.write(part)       # f 는  f = open("d:/../?.txt")

# 입출력을 조합한 하이브리드 방식 구현도 가능하다.
print('입출력을 조합한 하이브리드 방식 구현도 가능하다.')
f = open("D:\\data\\winter7.txt")
print(f)
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

# for part in combine(sample(), 32768):
#     f.write(part)

for part in combine(sample(),15):
    print(part)

# 중요한 점은 생성자 함수가 미래의 구현 방식을 알지못한다는 사실
# 생성자 함수는 그저 문자열을 제공

# 어려움..ㅠㅠ












"""
▶ 2.15 문자열에 변수 사용 ◀ 
♣ 문제 : 문자열에 변수를 사용하고 이 변수에 맞는 값을 채우고 싶다면? 
 ↘ 해결 : 파이썬 문자열에 변수값을 치환하는 간단한 방법은 존재하지 않는다.
            하지만 format() 메소드를 사용하면 비슷하게 흉내낼 수 있다.
            
            주 키워드 : format()   / format_map()       / vars()
                        __missing__()
                        sys._getframe(depth)
                        f_locals
            
 """
print('########################################## 2.15 문자열에 변수 사용 #####################################')


# 파이썬 문자열에 변수 값을 치환하는 간단한 방법은 존재X
# format메소드로 비슷하게 흉내낼 수 있음

s = '{name} has {n} messages'
f = s.format(name = 'wonju', n= 37)
print(f)


# 혹은 치환할 값이 변수에 들어있다면
# format_map()       &    vars() 를 함께 사용하면 된다

name = 'Wonju'
n = 37
print(s.format_map(vars()))

# vars() 는 인스턴스를 사용할 수도 있다.
print('인스턴스 var사용')
class Info:
    def __init__(self, name, n):
        self.name = name
        self.n = n
a = Info('Wonju', 28)
print(s.format_map(vars(a)))      # vars() 에 Info의 인스턴스(a)를 사용한 모습


# format과 format_map을 사용할때는 빠진 값이 있으면 제대로 동작하지 않는다.
# 이 문제는 __missing__() 메소드가 있는 dic class를 정의해서 피할 수 있다.

class safesub(dict):
    def __missing__(self, key):
        return '{'+key+'}'
#이제 format_map()의 입력부를 이 클래스로 감싸서 사용한다.

del n       # n이 정의되지 않도록 막는다.
print(s.format_map(safesub(vars())))    # Wonju has {n} messages
# n이 입력되지 않았더라도, TypeError나지 않고, 변수할당되지 않은 raw한 상태로 남음.

#만일, 변수 치환을 자주 할 것 같다면, 치환작업 자체를 유틸리티 함수에 모아서
#소위 프레임 핵 (Frame hack)으로 사용할 수 있다.

import sys

def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))
# sys._getframe(n)    :  몇단계 전의 프레임을 얻어낼 때 사용합니다
#이제 이 함수를 다음과 같이 사용한다.

name = 'Wonju'
n = 37
print(sub('Hello {name}'))
print(sub('You have {n} messages.'))


# 파이썬 자체에서 변수 보간법이 존재 하지 않아서, 다양한 대안이 생겼음
# 이 레시피는 해결책이 아닌, 다음과 같이 문자열을 서식화하기도 한다.

# name = 'Guido'
# n = 58
# '%(name) has %(n) messages.' % vars()
# 위 작동 안됨


# 혹은 템플릿을 사용하기도 한다.

import string
s = string.Template('$name has $n messages.')
print(s.substitute(vars()))


#어찌되었든 그래도 format이나 format_map을 쓰는것을 추천한다.
#얘네는 정렬,공백,숫자서식 등 다양하게 활용이 가능하지만
#template는 안되기 때문
#게다가 이번 장에서 __missing__()메소드를 통해 없는 값을 처리할 수도 있으니 좋음
#예를 들어, 디버깅할 때 keyerror 예외발생이 아닌, 값이 없음을 알리는 문자열을 반환하게하면
#디버깅에 유용할듯

# sub()함수는 sys._getframe(1) 로 호출하여 스택 프레임을 반환한다.
# 여기서 지역변수를 얻기 위해 f_locals요소에 접근했다.
# 대개의 코드에선 스택 프레임에 접근하는 것을 권장하지 않지만, 문자열 치환기능과 같은 유틸리티 함수에선
# 유용할 수 있음.
# f_locals : 호출 함수의 지역변수 복사본을 담아둔 딕셔너리
# f_locals를 수정할 순 있으나, 효과가 있는 것은 아님.





"""
▶ 2.16 텍스트 열의 개수 고정 ◀ 
♣ 문제 : 긴 문자열의 서식을 바꿔 열의 개수를 조절하고 싶다. 
 ↘ 해결 : textwrap 모듈을 사용해서 텍스트를 재서식화(reformat)하고자 한다.
            
"""
print('########################################## 2.16. 텍스트 열의 개수 고정 #####################################')

s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."

import textwrap
print(s)
print('##################################70################################')
print(textwrap.fill(s,70))
print('##################################40#################################')
print(textwrap.fill(s,40))
print('##################################initial_indent='    '#################################')
print(textwrap.fill(s,40, initial_indent='            '))
print('##################################subsequent_indent='    '#################################')
print(textwrap.fill(s,40, subsequent_indent='       '))


# 텍스트를 출력하기 전에, textwrap 모듈을 사용하면 깔끔하게 서식을 맞출 수 있다
# 특히 터미널에 사용할 텍스트에 적합하다. 터미널의 크기를 얻으려면
# os.get_terminal_size() 를 사용한다.

# import os
# print(os.get_terminal_size().columns)

# fill메소드 사용하면, 탭을 처리하는 방법, 문장의 끝과 같은 추가적인 관리를 할 수 있다.
# textwrap.TextWrapper 클래스 문서 참조