''''''
'''

1장 18절 시퀀스 요소에 이름 매핑 : 리스트나 튜플은 위치로 요ㅗ소에 접근 가능한데 위치에 의존하는 이런 코드를 이름으로 접근 가능하게 할 경우
                               collections.namedtuple()을 사용하면 된다.
                               
- collections.namedtuple()은 tuple 타입의 서브클래스를 반환하는 팩토리 메소드이다. 타입 이름과 포함해야할 필드를 전달하면 인스턴스화 가능한 클래스를 반환한다.
- namedtuple의 인스턴스는 일반적인 클래스 인스턴스와 비슷해 보이지만 튜플과 교환이 가능하고 인덱싱이나 언패킹과 같은 튜플의 기능을 모두 지원한다.
- namedtuple은 요소의 위치를 기반으로 구현된 코드를 분리해서 사용한다.
- 위치에 기반한 요소 접근 방법은 가독성을 떨어트리고 자료의 구조형에 크게 의존한다.
- 네임드 튜플은 저장공간을 더 필요로 하는 딕셔너리 대신 사용할 수 있지만 수정이 불가능하다.

- 수정이 필요한 경우 _replace() 메소드를 사용해야 한다. _replace()메소드는 지정한 값을 치환하여 완전히 새로운 데임드 튜플을 만든다.(예제 참조)
    _replace()를 사용하려면 일단 기본 값을 가진 튜플을 만든 다음 _replace()로 치환된 값을 가진 새로운 인스턴스를 만들어야 한다.



- 클래스, 인스턴스, 오브젝트 참조 필수 https://wikidocs.net/28

* 클래스와 오브젝트, 인스턴스

계산기에 3이라는 숫자를 입력하고 + 기호를 입력한 후 4를 입력하면 결과값으로 7을 보여준다. 
다시 한 번 + 기호를 입력한 후 3을 입력하면 기존 결과값 7에 3을 더해 10을 보여준다. 
즉, 계산기는 이전에 계산된 결과값을 항상 메모리 어딘가에 저장하고 있어야 한다.
한 프로그램에서 2개의 계산기가 필요한 상황이 발생하면 어떻게 해야 할까? 
각각의 계산기는 각각의 결과값을 유지해야 하기 때문에 위와 같이 adder 함수 하나만으로는결과값을 따로 유지할 수 없다.
이런 상황을 해결하려면 다음과 같이 함수를 각각 따로 만들어야 한다.

class Calculator:
    def __init__(self):
        self.result = 0

    def adder(self, num):
        self.result += num
        return self.result

cal1 = Calculator()
cal2 = Calculator()

print(cal1.adder(3))
print(cal1.adder(4))
print(cal2.adder(3))
print(cal2.adder(7))

Calculator 클래스로 만들어진 cal1, cal2라는 별개의 계산기(파이썬에서는 이것을 객체라고 한다)가 각각의 역할을 수행한다. 
그리고 계산기(cal1, cal2)의 결과값 역시 다른 계산기의 결과값과 상관없이 독립적인 결과값을 유지한다. 
클래스를 이용하면 계산기의 개수가 늘어나더라도 객체를 생성하기만 하면 되기 때문에 함수를 사용하는 경우와 달리 매우 간단해진다.
클래스의 이점은 단순히 이것만이 아니다. 하지만 이것 하나만으로도 "도대체 왜 클래스가 필요한 것일까?"라는 근본적인 물음에 대한 해답이 되었을 것이다.

클래스란 똑같은 무엇인가를 계속해서 만들어낼 수 있는 설계 도면 같은 것이고(뽑기 틀), 객체란 클래스에 의해서 만들어진 피조물(별 또는 하트가 찍힌 뽑기)을 뜻한다.

[오브젝트와 인스턴스의 차이]

클래스에 의해서 만들어진 객체를 인스턴스라고도 한다. 그렇다면 객체와 인스턴스의 차이는 무엇일까? 
이렇게 생각해 보자. kim = Programmer() 이렇게 만들어진 kim은 객체이다. 그리고 kim이라는 객체는 Programmer의 인스턴스이다. 
즉, 인스턴스라는 말은 특정 객체(kim)가 어떤 클래스(Programmer)의 객체인지를 관계 위주로 설명할 때 사용된다. 
즉, "kim은 인스턴스" 보다는 "kim은 객체"라는 표현이 어울리며, "kim은 Programmer의 객체" 보다는 "kim은 Programmer의 인스턴스"라는 표현이 훨씬 잘 어울린다.


'''

# 예1.
from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com', '2012-10-19')
sub
# Subscriber(addr='jonesy@example.com', joined='2012-10-19')
sub.addr
# 'jonesy@example.com'
sub.joined
# '2012-10-19'
addr, joined = sub
addr
# 'jonesy@example.com'
joined
# '2012-10-19'

# 예2.
def compute_cost(records):
    total = 0.0
    for rec in records:
        total += rec[1] * rec[2]
    return total

# 예3.
from collections import namedtuple
Stock = namedtuple('Stock', ['name', 'shares', 'price'])

def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.prices
    return total

# 예4.
s = Stock('ACME', 100, 123.45)
s = s._replace(shares = 75)
s
# Stock(name='ACME', shares75, price=123.45)

# 예5.
from collections import namedtuple
Stock = namedtuple('Stock', ['name', 'shares', 'price', 'date', 'time'])
  # 프로토타입 인스턴스
stock_prototype = Stock('', 0, 0.0, None, None)
  # 딕셔너리를 Stock으로 변환하는 함수
def dict_to_stock(s):
    return stock_prototype._replace(**s)
  # 사용 예
a = {'name' : 'ACME', 'shares' : 100, 'prices' : 123.45}
dict_to_stock(a)
# Stock(name='ACME', shares=100, price=123.45, date=None, time=None)

'''

1장 19절 데이터를 변환하면서 줄이기 : 감소함수를 실행해야 하는데 데이터를 변환하거나 필터링해야하는 경우 생성자 표현식을 사용하면 된다.

* 파이썬의 자료형

1) 집합(set)
    집합 자료형의 특징
     1. 중복을 허용하지 않는다.
     2. 순서가 없다(Unrordered)

2) 다중집합(multi-set)
    다중 집합은 집합과 비슷하지만, 집합 내 모든 원소가 다를 필요가 없다. 즉 어떤 원소가 하나 이상일 수 있다.
    하지만 순서가 없다는 것은 집합과 공통점이다.

3) 시퀀스(sequence) : 순서가 있는 문자
    파이썬에서 문자열, 리스트, 튜플 같은 자료형을 시퀀스(sequence) 자료형이라고 부른다. 
    여기에 포함된 각 객체는 순서를 가지고 인덱스를 사용하여 참조할 수 있다.
    a = "I love Python"이라고 하면 a의 객체 타입은 str형이다.
    a내 원소들은 순서를 가지고, 인덱스를 이용해 참조가 가능하다.
    파이썬을 인터프리터(interpreted)형 언어라고 한다.(프로그램을 한 줄 한 줄씩 읽어 하나하나 해석해가는 방식을 뜻한다.)
    
    for 원소 in 시퀀스: 명령어는 파이썬에서 한 번에 한 원소씩 시퀀스의 모든 원소에 명령을 실행하는 방법이다.  
    그러면 파일도 시퀀스일까? 아래 코드를 살펴보자. 

     file = open("observations")
     for line in file:

    파이썬은 '파일(file)'을 줄(line)의 시퀀스라고 인식한다. 파일의 각 줄은 문자의 시퀀스(sequence)이다. 따라서 파일은 시퀀스의 시퀀스라고 말할 수 있다.


4) 순서쌍(ordered pair) 
    무엇이 우선이고 다음인지를 알 수 있도록 두 개의 원소가 '순서대로' 정렬된 것이 순서쌍(ordered pair)이다. 
    이때, 두 개의 원소가 서로 다른 것을 의미한다.
    (이름, 이메일)이라는 두 개의 원소가 '순서대로' 정렬되어 있다면 이러한 순서쌍이 여러 개 모여서 순서쌍의 집합(set)을 만들고 있다.
    
    순서쌍의 집합을 일컬어 수학 용어로 관계(relation)라고 한다.

    * 이러한 관계중에는 매핑(mapping)이라는 것이 있다.

    매핑(mapping)은 첫 번째 원소가 모두 다른 순서쌍의 집합을 의미한다.
        예)
            x -> 1          x <-> 1
            y -> 2          y <-> 1
            z -> 4          z <-> 2
            a -> 3          a <-> 4
            b -> 5          b <-> 3

            < 매핑 >         < 관계 > 
            mapping         relation


'''

# 예6.
portfolio = [
    {'name': 'GOOG', 'shares': 50},
    {'name' : 'YHOO', 'shares' : 75},
    {'name' : 'AOL', 'shares' : 20},
    {'name' : 'SCOX', 'shares' : 65}
]

# 20을 출력
min_shares = min(s['shares'] for s in portfolio)
# {'name': 'AOL', 'shares': 20}을 출력
min_shares = min(portfolio, key=lambda s: s['shares'])


'''

1장 20절 여러 매핑을 단일 매핑으로 합치기 : 딕셔너리나 매핑이 여러 개 있고 자료 검색이나 확인을 위해 하나의 매핑으로 합치는 경우 collections 모듈의 Chainmap을 사용한다.

- ChainMap 클래스는 매핑을 여러개 받아서 한개로 '보이도록' 해준다. 보이도록 해주는 것이기 때문에 실제 한개로 합쳐주는 것은 아니다.
  매핑에 따른 리스트를 유지하면서 리스트를 스캔하도록 일반적인 딕셔너리 동작을 재정의 한다.

- update()를 사용해서 딕셔너리를 하나로 합칠 수도 있다.
  (update()의 경우 별개의 새 딕셔너리 객체를 만들거나 기존 딕셔너리의 내용을 변경해야만 하는데 원본 딕셔너리의 내용이 변경된다 해도 합쳐놓은 딕셔너리에 반영되지 않는다.
   ChainMap()은 원본 딕셔너리를 참조만 하기 때문에 위 문제가 발생하지 않는다.) 
  
'''

# 예7.
a = {'x':1, 'z':3}
b = {'y':2, 'z':4}

from collections import ChainMap
c = ChainMap(a,b)
print(c['x'])
# 1     <- a의 1
print(c['y'])
# 2     <- b의 2
print(c['z'])
# 3     <- a의 3

len(c)
# 3
list(c.keys())
# ['x', 'y', 'z']
list(c.values())
# [1, 2, 3]  <- 중복 키가 있으면 첫 번째로 매핑된 값을 사용한다. 마찬가지로 매핑 값을 변경하면 첫 번째 매핑된 리스트의 값에 영향을 준다.


# 예8.
values = ChainMap()
values['x'] = 1
values = values.new_child()  # 새로운 매핑 추가
values['x'] = 2
values = values.new_child()  # 새로운 매핑 추가
values['x'] = 3
values
# ChainMap({'x' : 3}, {'x' : 2}, {'x' : 1})

values['x']
# 3

values = values.parents     # 마지막 매핑 제거
values['x']
# 2
values = values.parents     # 마지막 매핑 제거
values['x']
# 1
values
# ChainMap({'x' : 1})


'''

2장 1절 여러 구분자로 문자열 나누기 : 문자열을 필드로 나누고 싶지만 구분자가 일정하지 않는 경우 split() 대신 re.split()을 사용한다.
- re.split()은 분리 구문마다 여러 패턴을 명시할 수 있다.

* https://wikidocs.net/13 : 문자열 자료형

* 정규식

1. 정규 표현식의 기초, 메타 문자

- 정규 표현식에서 사용하는 메타 문자(meta characters)에는 다음과 같은 것들이 있다.
  (※ 메타 문자란 원래 그 문자가 가진 뜻이 아닌 특별한 용도로 사용되는 문자를 말한다.)

- 정규식에 사용하는 메타 문자 : . ^ $ * + ? { } [ ] \ | ( )

    1) 문자 클래스 [ ]

    우리가 가장 먼저 살펴 볼 메타 문자는 바로 문자 클래스(character class)인 [ ]이다. 문자 클래스로 만들어진 정규식은 "[와 ] 사이의 문자들과 매치"라는 의미를 갖는다.
    (※ 문자 클래스를 만드는 메타 문자인 [와 ] 사이에는 어떤 문자도 들어갈 수 있다.)
    즉, 정규 표현식이 [abc]라면 이 표현식의 의미는 "a, b, c 중 한 개의 문자와 매치"를 뜻한다. 
    이해를 돕기 위해 문자열 "a", "before", "dude"가 정규식 [abc]와 어떻게 매치되는지 살펴보자.

    "a"는 정규식과 일치하는 문자인 "a"가 있으므로 매치
    "before"는 정규식과 일치하는 문자인 "b"가 있으므로 매치
    "dude"는 정규식과 일치하는 문자인 a, b, c 중 어느 하나도 포함하고 있지 않으므로 매치되지 않음

    [ ] 안의 두 문자 사이에 하이픈(-)을 사용하게 되면 두 문자 사이의 범위(From - To)를 의미한다. 
    예를 들어 [a-c]라는 정규 표현식은 [abc]와 동일하고 [0-5]는 [012345]와 동일하다.

    2) 문자 클래스 -

    [a-zA-Z] : 알파벳 모두
    [0-9] : 숫자

    3) 문자 클래스 ^
    
    문자 클래스([ ]) 내에는 어떤 문자나 메타 문자도 사용할수 있지만 주의해야 할 메타 문자가 1가지 있다. 
    그것은 바로 ^인데, 문자 클래스 내에 ^ 메타 문자가 사용될 경우에는 반대(not)라는 의미를 갖는다. 
    예를 들어 [^0-9]라는 정규 표현식은 숫자가 아닌 문자만 매치된다.

    * 자주 쓰이는 문자 클래스
    
    [0-9] 또는 [a-zA-Z] 등은 무척 자주 사용하는 정규 표현식이다. 이렇게 자주 사용하는 정규식들은 별도의 표기법으로 표현할 수 있다. 다음을 기억해 두자.

    \d - 숫자와 매치, [0-9]와 동일한 표현식이다.
    \D - 숫자가 아닌 것과 매치, [^0-9]와 동일한 표현식이다.
    \s - whitespace 문자와 매치, [ \t\n\r\f\v]와 동일한 표현식이다. 맨 앞의 빈 칸은 공백문자(space)를 의미한다.
    \S - whitespace 문자가 아닌 것과 매치, [^ \t\n\r\f\v]와 동일한 표현식이다.
    \w - 문자+숫자(alphanumeric)와 매치, [a-zA-Z0-9]와 동일한 표현식이다.
    \W - 문자+숫자(alphanumeric)가 아닌 문자와 매치, [^a-zA-Z0-9]와 동일한 표현식이다.
    (대문자로 사용된 것은 소문자의 반대임을 추측할 수 있을 것이다.)

    4) Dot(.)

    정규 표현식의 Dot(.) 메타 문자는 줄바꿈 문자인 \n를 제외한 모든 문자와 매치됨을 의미한다.

    (※ 정규식 작성 시 옵션으로 re.DOTALL이라는 옵션을 주면 \n 문자와도 매치가 된다.)

    5) 반복 *
    
    *의 의미는 *바로 앞에 있는 문자 a가 0부터 무한대로 반복될 수 있다는 의미이다. 

    예) ca*t
    ca*t	ct	Yes	"a"가 0번 반복되어 매치
    ca*t	cat	Yes	"a"가 0번 이상 반복되어 매치 (1번 반복)
    ca*t	caaat	Yes	"a"가 0번 이상 반복되어 매치 (3번 반복)
    
    6) 반복 +

    +는 최소 1번 이상 반복될 때 사용한다. 즉, *가 반복 횟수 0부터라면 +는 반복 횟수 1부터인 것이다. 

    예) ca+t
    ca+t	ct	No	"a"가 0번 반복되어 매치되지 않음
    ca+t	cat	Yes	"a"가 1번 이상 반복되어 매치 (1번 반복)
    ca+t	caaat	Yes	"a"가 1번 이상 반복되어 매치 (3번 반복)
    
    7) 반복 ({m,n}, ?)

    { } 메타 문자를 이용하면 반복 횟수를 고정시킬 수 있다. {m, n} 정규식을 사용하면 반복 횟수가 m부터 n까지인 것을 매치할 수 있다. 
    또한 m 또는 n을 생략할 수도 있다. 만약 {3,} 처럼 사용하면 반복 횟수가 3 이상인 경우이고 {,3} 처럼 사용하면 반복 횟수가 3 이하인 것을 의미한다. 
    생략된 m은 0과 동일하며, 생략된 n은 무한대(2억개 미만)의 의미를 갖는다.
    ※ {1,}은 +와 동일하며 {0,}은 *와 동일하다.

    예1) ca{2}t -> "c + a(반드시 2번 반복) + t"를 의미
    ca{2}t	cat	No	"a"가 1번만 반복되어 매치되지 않음
    ca{2}t	caat	Yes	"a"가 2번 반복되어 매치
    
    예2) ca{2,5}t -> "c + a(2~5회 반복) + t"를 의미
    ca{2,5}t	cat	No	"a"가 1번만 반복되어 매치되지 않음
    ca{2,5}t	caat	Yes	"a"가 2번 반복되어 매치
    ca{2,5}t	caaaaat	Yes	"a"가 5번 반복되어 매치

    예3) ab?c -> "a + b(있어도 되고 없어도 된다) + c"
    ab?c	abc	Yes	"b"가 1번 사용되어 매치
    ab?c	ac	Yes	"b"가 0번 사용되어 매치

2. 파이썬에서 정규 표현식을 지원하는 re 모듈

파이썬은 정규 표현식을 지원하기 위해 re(regular expression의 약어) 모듈을 제공한다. 
re 모듈은 파이썬이 설치될 때 자동으로 설치되는 기본 라이브러리로, 사용 방법은 다음과 같다.

import re
p = re.compile('ab*')

re.compile 을 이용하여 정규표현식(위 예에서는 ab*)을 컴파일하고 컴파일된 패턴객체(re.compile의 결과로 리턴되는 객체 p)를 이용하여 그 이후의 작업을 수행할 것이다.

※ 정규식 컴파일 시 특정 옵션을 주는 것도 가능한데, 이에 대해서는 뒤에서 자세히 살펴본다.
※ 패턴이란 정규식을 컴파일한 결과이다.

    1) 정규식을 이용한 문자열 검색

    컴파일 된 패턴 객체는 다음과 같은 4가지 메소드를 제공한다.
    match()	    문자열의 처음부터 정규식과 매치되는지 조사한다.
    search()	문자열 전체를 검색하여 정규식과 매치되는지 조사한다.
    findall()	정규식과 매치되는 모든 문자열(substring)을 리스트로 리턴한다
    finditer()	정규식과 매치되는 모든 문자열(substring)을 iterator 객체로 리턴한다

    (match, search는 정규식과 매치될 때에는 match 객체를 리턴하고 매치되지 않을 경우에는 None을 리턴한다.)
    
        (1) match
        match 메서드는 문자열의 처음부터 정규식과 매치되는지 조사한다.
        match의 결과로 match 객체 또는 None이 리턴되기 때문에 파이썬 정규식 프로그램은 보통 다음과 같은 흐름으로 작성한다.

        p = re.compile(정규표현식)
        m = p.match( 'string goes here' )
        if m:
            print('Match found: ', m.group())
        else:
            print('No match')
        
        즉, match의 결과값이 있을 때만 그 다음 작업을 수행하겠다는 의도이다.
        
            - match 객체의 메서드
            
            group()	매치된 문자열을 리턴한다.
            start()	매치된 문자열의 시작 위치를 리턴한다.
            end()	매치된 문자열의 끝 위치를 리턴한다.
            span()	매치된 문자열의 (시작, 끝) 에 해당되는 튜플을 리턴한다.
            
            * 모듈 단위로 수행하기

            이전엔 re.compile을 이용하여 컴파일된 패턴 객체로 그 이후 작업을 수행했다. re 모듈은 이 것을 좀 축약한 형태의 방법을 제공한다.

            p = re.compile('[a-z]+')
            m = p.match("python")

            위 코드가 축약된 형태는 다음과 같다.

            m = re.match('[a-z]+', "python")
            
            위 예처럼 사용하면 컴파일과 match 메서드를 한 번에 수행할 수 있다. 
            보통 한 번 만든 패턴 객체를 여러번 사용해야 할 때는 이 방법보다 re.compile을 사용하는 것이 유리하다.
            
            
        
        (2) search
        컴파일된 패턴 객체 p를 가지고 이번에는 search 메서드를 수행해 보자.
        "python"이라는 문자열에 search 메서드를 수행하면 match 메서드를 수행했을 때와 동일하게 매치된다.
        
        m = p.search("3 python")
        print(m)
        <_sre.SRE_Match object at 0x01F3FA30>
        
        "3 python"이라는 문자열의 첫 번째 문자는 "3"이지만 search는 문자열의 처음부터 검색하는 것이 아니라 문자열 전체를 검색하기 때문에
        "3 " 이후의 "python"이라는 문자열과 매치된다.
        이렇듯 match 메서드와 search 메서드는 문자열의 처음부터 검색할지의 여부에 따라 다르게 사용해야 한다.

        (3) findall
        
        result = p.findall("life is too short")
        print(result)
        ['life', 'is', 'too', 'short']
        
        "life is too short"라는 문자열의 "life", "is", "too", "short"라는 단어들이 각각 [a-z]+ 정규식과 매치되어 리스트로 리턴된다.

        (4) finditer

        result = p.finditer("life is too short")
        print(result)
        <callable_iterator object at 0x01F5E390>
        for r in result: print(r)
        ...
        <_sre.SRE_Match object at 0x01F3F9F8>
        <_sre.SRE_Match object at 0x01F3FAD8>
        <_sre.SRE_Match object at 0x01F3FAA0>
        <_sre.SRE_Match object at 0x01F3F9F8>
        
        finditer는 findall과 동일하지만 그 결과로 반복 가능한 객체(iterator object)를 리턴한다. 
        반복 가능한 객체가 포함하는 각각의 요소는 match 객체이다.
        
        
    2) 컴파일 옵션
    - 정규식을 컴파일할 때 다음과 같은 옵션을 사용할 수 있다.

        DOTALL(S) - . 이 줄바꿈 문자를 포함하여 모든 문자와 매치할 수 있도록 한다.
        IGNORECASE(I) - 대소문자에 관계없이 매치할 수 있도록 한다.
        MULTILINE(M) - 여러줄과 매치할 수 있도록 한다. (^, $ 메타문자의 사용과 관계가 있는 옵션이다)
        VERBOSE(X) - verbose 모드를 사용할 수 있도록 한다. (정규식을 보기 편하게 만들수 있고 주석등을 사용할 수 있게된다.)
    
        옵션을 사용할 때는 re.DOTALL처럼 전체 옵션명을 써도 되고 re.S처럼 약어를 써도 된다.

        (1) DOTALL, S

        메타 문자는 줄바꿈 문자(\n)를 제외한 모든 문자와 매치되는 규칙이 있다. 
        만약 \n 문자도 포함하여 매치하고 싶다면 re.DOTALL 또는 re.S 옵션을 사용해 정규식을 컴파일하면 된다.

        다음의 예를 보자.

        import re
        p = re.compile('a.b')
        m = p.match('a\nb')
        print(m)
        # None
        
        정규식이 a.b인 경우 문자열 a\nb는 매치되지 않음을 알 수 있다. 
        왜냐하면 \n은 . 메타 문자와 매치되지 않기 때문이다. 
        \n 문자와도 매치되게 하려면 다음과 같이 re.DOTALL 옵션을 사용해야 한다.

        p = re.compile('a.b', re.DOTALL)
        m = p.match('a\nb')
        print(m)
        # <_sre.SRE_Match object at 0x01FCF3D8>
        
        보통 re.DOTALL은 여러줄로 이루어진 문자열에서 \n에 상관없이 검색하고자 할 경우에 많이 사용한다.

        (2) IGNORECASE, I

        re.IGNORECASE 또는 re.I 는 대소문자 구분없이 매치를 수행하고자 할 경우에 사용하는 옵션이다.

        다음의 예제를 보자.

        p = re.compile('[a-z]', re.I)
        p.match('python')
        # <_sre.SRE_Match object at 0x01FCFA30>
        p.match('Python')
        # <_sre.SRE_Match object at 0x01FCFA68>
        p.match('PYTHON')
        # <_sre.SRE_Match object at 0x01FCF9F8>
        
        [a-z] 정규식은 소문자만을 의미하지만 re.I 옵션에 의해서 대·소문자 구분 없이 매치된다.

        (3) MULTILINE, M

        re.MULTILINE 또는 re.M 옵션은 조금 후에 설명할 메타 문자인 ^, $와 연관된 옵션이다. 
        이 메타 문자에 대해 간단히 설명하자면 ^는 문자열의 처음을 의미하고, $은 문자열의 마지막을 의미한다. 
        예를 들어 정규식이 ^python인 경우 문자열의 처음은 항상 python으로 시작해야 매치되고, 
        만약 정규식이 python$이라면 문자열의 마지막은 항상 python으로 끝나야 매치가 된다는 의미이다.

        다음 예를 보도록 하자.

        import re
        p = re.compile("^python\s\w+")
        data = """python one
                  life is too short
                  python two
                  you need python
                  python three"""

        print(p.findall(data))

        정규식 ^python\s\w+ 은 "python"이라는 문자열로 시작하고 그 후에 whitespace, 그 후에 단어가 와야한다는 의미이다. 
        검색할 문자열 data는 여러줄로 이루어져 있다.

        이 스크립트를 실행하면 다음과 같은 결과가 리턴된다.

        # ['python one']
        
        ^ 메타 문자에 의해 python이라는 문자열이 사용된 첫 번째 라인만 매치가 된 것이다.
        하지만 ^ 메타 문자를 문자열 전체의 처음이 아니라 각 라인의 처음으로 인식시키고 싶은 경우도 있을 것이다. 
        이럴 때 사용할 수 있는 옵션이 바로 re.MULTILINE 또는 re.M이다. 위 코드를 다음과 같이 수정해 보자.

        import re
        p = re.compile("^python\s\w+", re.MULTILINE)
        
        data = """python one
                  life is too short
                  python two
                  you need python
                  python three"""

        print(p.findall(data))
        
        re.MULTILINE 옵션으로 인해 ^ 메타 문자가 문자열 전체가 아닌 각 라인의 처음이라는 의미를 갖게 되었다. 이 스크립트를 실행하면 다음과 같은 결과가 출력된다.

        # ['python one', 'python two', 'python three']
        
        즉, re.MULTILINE 옵션은 ^, $메타 문자를 문자열의 각 라인마다 적용해 주는 것이다.

        (4) VERBOSE, X

        정규식을 주석 또는 라인 단위로 구분하기 위해 re.VERBOSE 또는 re.X 옵션을 이용한다.

        다음의 예를 보자.

        charref = re.compile(r'&[#](0[0-7]+|[0-9]+|x[0-9a-fA-F]+);')
        
        위 정규식이 쉽게 이해되는가? 이제 다음의 예를 보자.

        charref = re.compile(r"""&[#]   # Start of a numeric entity reference
                                    (0[0-7]+         # Octal form  
                                            | [0-9]+          # Decimal form 
                                            | x[0-9a-fA-F]+   # Hexadecimal form
                                    );                   # Trailing semicolon
                                      """, re.VERBOSE)
        
        첫 번째와 두 번째 예를 비교해 보면 컴파일된 패턴 객체인 charref는 모두 동일한 역할을 한다. 
        하지만 정규식이 복잡할 경우 두 번째처럼 주석을 적고 여러 줄로 표현하는 것이 훨씬 가독성이 좋다는 것을 알 수 있다.
        re.VERBOSE 옵션을 사용하면 문자열에 사용된 whitespace는 컴파일 시 제거된다
        (단 [ ] 내에 사용된 whitespace는 제외). 그리고 줄 단위로 #기호를 이용하여 주석문을 작성할 수 있다.

        (5) 백슬래시 문제
        정규표현식을 파이썬에서 사용하려 할 때 혼란을 주게 되는 요소가 한가지 있는데 그것은 바로 백슬래시(\)이다.
        예를들어 LaTex파일 내에 있는 "\section" 이라는 문자열을 찾기 위한 정규식을 만든다고 가정해 보자.
        다음과 같은 정규식을 생각해 보자.

        \section
        
        이 정규식은 \s 문자가 whitespace로 해석되어 의도한 대로 매치가 이루어지지 않는다.
        위 표현은 다음과 동일한 의미가 된다.

        [ \t\n\r\f\v]ection
        
        따라서 위 정규표현식은 다음과 같이 변경되어야 할 것이다.

        \\section
        
        즉, 위 정규식에서 사용한 \ 문자가 문자열 그 자체임을 알려주기 위해 백슬래시 2개를 사용하여 이스케이프 처리를 해야 하는 것이다.
        따라서 위 정규식을 컴파일하려면 다음과 같이 작성해야 한다.

        p = re.compile('\\section')
        
        위 처럼 정규식을 만들어서 컴파일 하면 실제 파이썬 정규식 엔진에는 파이썬 문자열 리터럴 규칙에 의하여 \\이 \ 로 변경되어 \section 이 전달되는 것이다.

        ※ 이 문제는 위와같은 정규식을 파이썬에서 사용할 때만 적용되는 문제이다. (파이썬의 리터럴 규칙) 유닉스의 grep, vi등에서는 이러한 문제가 없다.
          결국 정규식 엔진에 \\ 문자를 전달하려면 파이썬은 \\\\ 처럼 백슬래시를 4개나 사용해야 한다.

        ※ 정규식 엔진은 정규식을 해석하고 수행하는 모듈이다.

        p = re.compile('\\\\section')

        만약 위와 같이 \를 이용한 표현이 반복되서 사용되는 정규식이라면 너무 복잡하여 이해하기 쉽지 않을 것이다. 
        이러한 문제로 파이썬 정규식에는 Raw string이라는 것이 생겨나게 되었다. 
        즉 컴파일 해야 하는 정규식이 Raw String임을 알려줄 수 있도록 파이썬 문법이 만들어진 것이다. 그 방법은 다음과 같다.

        p = re.compile(r'\\section')
        
        위와 같이 정규식 문자열 앞에 r문자를 선행하면 이 정규식은 Raw String 규칙에 의하여 백슬래시 2개 대신 1개만 써도 두개를 쓴것과 동일한 의미를 갖게된다.

        ※ 만약 백슬래시를 사용하지 않는 정규식이라면 r의 유무에 상관없이 동일한 정규식이 될 것이다.

3. 메타문자

여기서 다룰 메타 문자들은 앞에서 살펴보았던 메타 문자들과 성격이 조금 다르다. 
이전에 살펴본 메타 문자들은 모두 매치되는 문자열들을 소모시킨다. 
소모된다는 말의 의미가 조금 헷갈릴 수 있을 것이다. 
문자열이 일단 소모되어 버리면 그 부분은 검색 대상에서 제외되지만 소모되지 않는 경우에는 다음에 또 다시 검색 대상이 된다고 생각하면 쉬울 것이다.

+, *, [], {} 등의 메타문자는 매치가 진행될 때 현재 매치되고 있는 문자열의 위치가 변경된다. (보통 소모된다고 표현한다.) 
하지만 이와 달리 문자열을 소모시키지 않는 메타 문자들도 있다. 이번에는 이런 문자열 소모가 없는(zero-width assertions) 메타 문자들에 대해서 살펴보기로 하자.

    1) |

    | 메타문자는 "or"의 의미와 동일하다. A|B 라는 정규식이 있다면 이것은 A 또는 B라는 의미가 된다.

    p = re.compile('Crow|Servo')
    m = p.match('CrowHello')
    print(m)
    # <_sre.SRE_Match object; span=(0, 4), match='Crow'>

    2) ^

    ^ 메타문자는 문자열의 맨 처음과 일치함을 의미한다. 
    이전에 알아보았던 컴파일 옵션 re.MULTILINE 을 사용할 경우에는 여러줄의 문자열에서는 각 라인의 처음과 일치하게 된다.

    다음의 예를 보자.  

    print(re.search('^Life', 'Life is too short'))
    # <_sre.SRE_Match object at 0x01FCF3D8>
    print(re.search('^Life', 'My Life'))
    # None
    
    ^Life 정규식은 "Life"라는 문자열이 처음에 온 경우에는 매치하지만 처음 위치가 아닌 경우에는 매치되지 않음을 알 수 있다.

    3) $
    $ 메타문자는 ^ 메타문자의 반대의 경우이다. $는 문자열의 끝과 매치함을 의미한다.

    다음의 예를 보자.

    print(re.search('short$', 'Life is too short'))
    # <_sre.SRE_Match object at 0x01F6F3D8>
    print(re.search('short$', 'Life is too short, you need python'))
    # None
    
    short$ 정규식은 검색할 문자열의 "short"로 끝난 경우에는 매치되지만 그 이외의 경우에는 매치되지 않음을 알 수 있다.

    ※ ^ 또는 $ 문자를 메타문자가 아닌 문자 그 자체로 매치하고 싶은 경우에는 [^], [$] 처럼 사용하거나 \^, \$ 로 사용하면 된다.

    4) \A

    \A는 문자열의 처음과 매치됨을 의미한다. ^와 동일한 의미이지만 re.MULTILINE 옵션을 사용할 경우에는 다르게 해석된다. 
    re.MULTILINE 옵션을 사용할 경우 ^은 라인별 문자열의 처음과 매치되지만 \A는 라인과 상관없이 전체 문자열의 처음하고만 매치된다.

    5) \Z

    \Z는 문자열의 끝과 매치됨을 의미한다. 이것 역시 \A와 동일하게 re.MULTILINE 옵션을 사용할 경우 $ 메타문자와는 달리 전체 문자열의 끝과 매치된다.

    6) \b

    \b는 단어 구분자(Word boundary)이다. 보통 단어는 whitespace에 의해 구분이 된다. 다음의 예를 보자.

    p = re.compile(r'\bclass\b')
    print(p.search('no class at all'))  
    # <_sre.SRE_Match object at 0x01F6F3D8>

    \bclass\b 정규식은 "class"라는 단어와 매치됨을 의미한다. 따라서 no class at all의 class라는 단어와 매치됨을 확인할 수 있다.

    print(p.search('the declassified algorithm'))
    # None

    위 예의 the declassified algorithm라는 문자열 안에 class라는 문자열이 포함되어 있긴 하지만 whitespace로 구분된 단어가 아니므로 매치되지 않는다.

    print(p.search('one subclass is'))
    # None
    
    subclass라는 문자열 역시 class앞에 sub라는 문자열이 더해져 있으므로 매치되지 않음을 알 수 있다.

    \b 메타문자를 이용할 경우 주의해야 할 점이 한가지 있다. 
    \b는 파이썬 리터럴 규칙에 의하면 백스페이스(Back Space)를 의미하므로 백스페이스가 아닌 Word Boundary임을 알려주기 위해 
    r'\bclass\b' 처럼 raw string임을 알려주는 기호 r을 반드시 붙여주어야 한다.

    7) \B

    \B 메타문자는 \b 메타문자의 반대의 경우이다. 즉, whitespace로 구분된 단어가 아닌 경우에만 매치된다.
    p = re.compile(r'\Bclass\B')
    print(p.search('no class at all'))  
    # None
    print(p.search('the declassified algorithm'))
    # <_sre.SRE_Match object at 0x01F6FA30>
    print(p.search('one subclass is'))
    # None
    
    class라는 문자열 좌우에 whitespace가 있는 경우에는 매치가 안되는 것을 확인할 수 있다.

4. 그룹핑

ABC라는 문자열이 계속해서 반복되는지 조사하는 정규식을 작성하고 싶다고 하면 지금까지 공부한 내용으로는 위 정규식을 작성할 수 없다. 
이럴 때 필요한 것이 바로 그룹핑(Grouping) 이다.

위의 경우는 다음처럼 그룹핑을 이용하여 작성할 수 있다.

(ABC)+

그룹을 만들어 주는 메타문자는 바로 ( 과 ) 이다.

p = re.compile('(ABC)+')
m = p.search('ABCABCABC OK?')
print(m)
# <_sre.SRE_Match object at 0x01F7B320>
print(m.group())
# ABCABCABC

다음의 예를 보자.

p = re.compile(r"\w+\s+\d+[-]\d+[-]\d+")
m = p.search("park 010-1234-1234")

\w+\s+\d+[-]\d+[-]\d+은 이름 + " " + 전화번호 형태의 문자열을 찾는 정규표현식이다. 

보통 반복되는 문자열을 찾을 때 그룹을 이용하는데, 그룹을 이용하는 보다 큰 이유는 위에서 볼 수 있듯이 매치된 문자열 중에서 특정 부분의 문자열만 뽑아내기 위해서인 경우가 더 많다.

위 예에서 만약 "이름" 부분만을 뽑아내려 한다면 다음과 같이 할 수 있다.

p = re.compile(r"(\w+)\s+\d+[-]\d+[-]\d+")
m = p.search("park 010-1234-1234")
print(m.group(1))
# park
이름에 해당되는 \w+ 부분을 그룹((\w+))으로 만들면 match object의 group(index) 메서드를 이용하여 그룹핑된 부분의 문자열만 뽑아낼 수 있다. 
group 메쏘드의 index는 다음과 같은 의미를 갖는다.

group(0)	매치된 전체 문자열
group(1)	첫 번째 그룹에 해당되는 문자열
group(2)	두 번째 그룹에 해당되는 문자열
group(n)	n 번째 그룹에 해당되는 문자열

다음의 예제를 계속해서 보자.

p = re.compile(r"(\w+)\s+(\d+[-]\d+[-]\d+)")
m = p.search("park 010-1234-1234")
print(m.group(2))
# 010-1234-1234

이번에는 전화번호 부분을 추가로 그룹((\d+[-]\d+[-]\d+))으로 만들었다. 이렇게 하면 group(2)처럼 사용하여 전화번호만을 뽑아낼 수 있다.

p = re.compile(r"(\w+)\s+((\d+)[-]\d+[-]\d+)")
m = p.search("park 010-1234-1234")
print(m.group(3))
# 010

위 예에서 보듯이 (\w+)\s+((\d+)[-]\d+[-]\d+) 처럼 그룹을 중첩되게 사용하는 것도 가능하다. 
그룹이 중첩되어 사용되는 경우는 바깥쪽부터 시작하여 안쪽으로 들어갈수로 인덱스가 증가한다.

    1) 그룹핑된 문자열 재참조하기

    그룹의 또 하나 좋은 점은 한번 그룹핑된 문자열을 재참조(Backreferences)할 수 있다는 점이다. 다음의 예를 보자.

    p = re.compile(r'(\b\w+)\s+\1')
    p.search('Paris in the the spring').group()
    # 'the the'
    
    정규식 (\b\w+)\s+\1은 (그룹1) + " " + "그룹1과 동일한 단어" 와 매치됨을 의미한다. 
    이렇게 정규식을 만들게 되면 2개의 동일한 단어가 연속적으로 사용되어야만 매치되게 된다. 
    이것을 가능하게 해 주는 것이 바로 재 참조 메타문자인 \1이다. \1은 정규식의 그룹중 첫번째 그룹을 지칭한다.

    ※ 두번째 그룹을 참조하려면 \2를 사용하면 된다.

    2) 그룹핑된 문자열에 이름 붙이기
    
    정규식 내에 그룹이 무척 많아진다고 가정해 보자. 
    예를 들어 정규식 내에 그룹이 10개 이상만 되어도 매우 혼란스러울 것이다. 
    거기에 더해 정규식이 수정되면서 그룹이 추가, 삭제되면 그 그룹을 인덱스로 참조했던 프로그램들도 모두 변경해 주어야 하는 위험도 갖게 된다. 
    만약 그룹을 인덱스가 아닌 이름(Named Groups)으로 참조할 수 있다면 어떨까? 그렇다면 이런 문제들에서 해방되지 않을까?

    이러한 이유로 정규식은 그룹을 만들 때 그룹명을 지정할 수 있게 했다. 그 방법은 다음과 같다.

    (?P<name>\w+)\s+((\d+)[-]\d+[-]\d+)

    위 정규식은 이전에 보았던 이름과 전화번호를 추출하는 정규식이다. 기존과 달라진 부분은 다음과 같다.

    (\w+) --> (?P<name>\w+)

    대단히 복잡해 진것처럼 보이지만 (\w+) 라는 그룹에 "name"이라는 이름을 붙인 것에 불과하다. 
    여기서 사용한 (?...) 표현식은 정규표현식의 확장구문이다. (여기서 ...은 다양하게 변한다는 anything의 의미이다.) 
    이 확장구문을 이용하기 시작하면 가독성이 무척 떨어지긴 하지만 반면에 강력함을 갖게 된다.

    그룹에 이름을 지어주기 위해서는 다음과 같은 확장구문을 사용해야 한다.

    (?P<그룹명>...)
    
    그룹에 이름을 지정하고 참조하는 다음의 예를 보자.

    p = re.compile(r"(?P<name>\w+)\s+((\d+)[-]\d+[-]\d+)")
    m = p.search("park 010-1234-1234")
    print(m.group("name"))
    # park

    위 예에서 볼 수 있듯이 name이라는 그룹명으로 참조할 수 있다.
    그룹명을 이용하면 정규식 내에서 재참조하는 것도 가능하다.

    p = re.compile(r'(?P<word>\b\w+)\s+(?P=word)')
    p.search('Paris in the the spring').group()
    # 'the the'
    위 예에서 보듯이 재 참조시에는 (?P=그룹명) 이라는 확장구문을 이용해야 한다.

5. 전방 탐색

정규식에 막 입문한 사람들이 가장 어려워하는 것이 바로 전방 탐색(Lookahead Assertions) 확장 구문이다. 
정규식 안에 이 확장 구문이 사용되면 순식간에 암호문처럼 알아보기 어렵게 바뀌기 때문이다. 
하지만 이 전방 탐색이 꼭 필요한 경우가 있으며 매우 유용한 경우도 많으니 꼭 알아 두도록 하자.

다음의 예제를 보자.

p = re.compile(".+:")
m = p.search("http://google.com")
print(m.group())
# http:

정규식 .+: 과 일치하는 문자열로 "http:"가 리턴되었다. 하지만 "http:" 라는 검색 결과에서 ":"을 제외하고 출력하려면 어떻게 해야 할까? 
위 예는 그나마 간단하지만 훨씬 복잡한 정규식이어서 그룹핑은 추가로 할 수 없다는 조건까지 더해진다면 어떻게 해야 할까?

이럴 때 사용할 수 있는 것이 바로 전방 탐색이다. 전방 탐색에는 긍정(Positive)과 부정(Negative)의 2종류가 있고 다음과 같이 표현된다.

긍정형 전방 탐색((?=...)) - ... 에 해당되는 정규식과 매치되어야 하며 조건이 통과되어도 문자열이 소모되지 않는다.
부정형 전방 탐색((?!...)) - ...에 해당되는 정규식과 매치되지 않아야 하며 조건이 통과되어도 문자열이 소모되지 않는다.
긍정형 전방 탐색

긍정형 전방 탐색을 이용하면 http:의 결과를 http로 바꿀 수 있다. 다음의 예를 보자.

p = re.compile(".+(?=:)")
m = p.search("http://google.com")
print(m.group())
# http

정규식 중 :에 해당하는 부분이 긍정형 전방탐색 기법이 적용되어 (?=:) 으로 변경되었다. 
이렇게 되면 기존 정규식과 검색에서는 동일한 효과를 발휘한다.
하지만 :에 해당되는 문자열이 정규식 엔진에 의해 소모되지 않아(검색에는 포함되지만 검색 결과에는 제외됨) 검색 결과에서는 :이 제거된 후 리턴되는 효과가 있다.

자, 이번에는 다음의 정규식을 보자.

.*[.].*$

이 정규식은 파일명 + '.' + 확장자 를 나타내는 정규식이다. 이 정규식은 foo.bar, autoexec.bat, sendmail.cf등과 매치할 것이다.

자, 이제 이 정규식에 확장자가 "bat인 파일은 제외해야 한다"는 조건을 추가해 보자. 가장 먼저 생각할 수 있는 정규식은 다음과 같을 것이다.

.*[.][^b].*$

이 정규식은 확장자가 b라는 문자로 시작하면 안된다는 의미이다. 하지만 이 정규식은 foo.bar라는 파일마저 걸러내 버린다. 다시 정규식을 다음과 같이 수정 해 보자.

.*[.]([^b]..|.[^a].|..[^t])$

이 정규식은 | 메타 문자를 사용하여 확장자의 첫 번째 문자가 b가 아니거나 두 번째 문자가 a가 아니거나 세 번째 문자가 t가 아닌 경우를 의미한다. 
이 정규식에 의하여 foo.bar는 제외되지 않고 autoexec.bat은 제외되어 만족스러운 결과를 리턴한다. 하지만 이 정규식은 아쉽게도 sendmail.cf처럼 확장자의 문자 개수가 2개인 케이스를 포함하지 못 하는 오동작을 하기시작한다.

자, 이제 다음과 같이 바꾸어야 한다.

.*[.]([^b].?.?|.[^a]?.?|..?[^t]?)$
확장자의 문자 개수가 2개여도 통과되는 정규식이 만들어졌다. 하지만 정규식은 점점 더 복잡해지고 이해하기 어려워진다.

자, 그런데 여기서 bat 파일말고 exe 파일도 제외하라는 조건이 추가로 생긴다면 어떻게 될까? 이 모든 조건을 만족하는 정규식을 구현하려면 패턴은 더욱더 복잡해져야만 할 것이다.

6. 부정형 전방 탐색

이러한 상황의 구원투수는 바로 "부정형 전방탐색"이다. 위 케이스는 부정형 전방탐색을 사용하면 다음과 같이 간단하게 처리된다.

.*[.](?!bat$).*$

확장자가 bat가 아닌 경우에만 통과된다는 의미이다. 
bat라는 문자열이 있는지 조사하는 과정에서 문자열이 소모되지 않으므로 bat가 아니라고 판단되면 그 이후 정규식 매칭이 진행된다.

exe 역시 제외하라는 조건이 추가되더라도 다음과 같이 간단히 표현할 수 있다.

.*[.](?!bat$|exe$).*$

7. 문자열 바꾸기

sub 메서드를 이용하면 정규식과 매치되는 부분을 다른 문자로 쉽게 바꿀 수 있다.

다음의 예를 보자.

p = re.compile('(blue|white|red)')
p.sub('colour', 'blue socks and red shoes')
# 'colour socks and colour shoes'

sub 메서드의 첫 번째 입력 인수는 "바꿀 문자열(replacement)"이 되고, 두 번째 입력 인수는 "대상 문자열"이 된다. 
위 예에서 볼 수 있듯이 blue 또는 white 또는 red라는 문자열이 colour라는 문자열로 바뀌는 것을 확인할 수 있다.
그런데 딱 한 번만 바꾸고 싶은 경우도 있다. 이렇게 바꾸기 횟수를 제어하려면 다음과 같이 세 번째 입력 인수로 count 값을 넘기면 된다.

p.sub('colour', 'blue socks and red shoes', count=1)
# 'colour socks and red shoes'

처음 일치하는 blue만 colour라는 문자열로 한 번만 바꾸기가 실행됨을 알 수 있다.

[sub 메서드와 유사한 subn 메서드]

subn 역시 sub와 동일한 기능을 하지만 리턴되는 결과를 튜플로 리턴한다는 차이가 있다. 
리턴된 튜플의 첫 번째 요소는 변경된 문자열이고, 두 번째 요소는 바꾸기가 발생한 횟수이다.

p = re.compile('(blue|white|red)')
p.subn( 'colour', 'blue socks and red shoes')
# ('colour socks and colour shoes', 2)

    - sub 메서드 사용 시 참조 구문 사용하기

    sub 메서드를 사용할 때 참조 구문을 사용할 수 있다. 다음의 예를 보자.

    p = re.compile(r"(?P<name>\w+)\s+(?P<phone>(\d+)[-]\d+[-]\d+)")
    print(p.sub("\g<phone> \g<name>", "park 010-1234-1234"))
    # 010-1234-1234 park
    
    위 예는 이름 + 전화번호의 문자열을 전화번호 + 이름으로 바꾸는 예이다. sub의 바꿀 문자열 부분에 \g<그룹명>을 이용하면 정규식의 그룹명을 참조할 수 있게된다.

    다음과 같이 그룹명 대신 참조번호를 이용해도 마찬가지 결과가 리턴된다.

    p = re.compile(r"(?P<name>\w+)\s+(?P<phone>(\d+)[-]\d+[-]\d+)")
    print(p.sub("\g<2> \g<1>", "park 010-1234-1234"))
    # 010-1234-1234 park

    - sub 메서드의 입력 인수로 함수 넣기

    sub 메서드의 첫 번째 입력 인수로 함수를 넣을 수도 있다. 다음의 예를 보자.

    def hexrepl(match):
         "Return the hex string for a decimal number"
         value = int(match.group())
         return hex(value)

    p = re.compile(r'\d+')
    p.sub(hexrepl, 'Call 65490 for printing, 49152 for user code.')
    # 'Call 0xffd2 for printing, 0xc000 for user code.'

    hexrepl 함수는 match 객체(위에서 숫자에 매치되는)를 입력으로 받아 16진수로 변환하여 리턴하는 함수이다. 
    sub의 첫 번째 입력 인수로 함수를 사용할 경우 해당 함수의 첫 번째 입력 인수에는 정규식과 매치된 match 객체가 입력된다. 
    그리고 매치되는 문자열은 함수의 리턴값으로 바뀌게 된다.

8. Greedy vs Non-Greedy
정규식에서 Greedy(탐욕스러운)란 어떤 의미일까? 다음의 예제를 보자.

s = '<html><head><title>Title</title>'
len(s)
# 32
print(re.match('<.*>', s).span())
# (0, 32)
print(re.match('<.*>', s).group())
# <html><head><title>Title</title>

<.*> 정규식의 매치결과로 <html> 문자열이 리턴되기를 기대했을 것이다. 
하지만 * 메타문자는 매우 탐욕스러워서 매치할 수 있는 최대한의 문자열인 <html><head><title>Title</title> 문자열을 모두 소모시켜 버렸다. 
어떻게 하면 이 탐욕스러움을 제한하고 <html> 이라는 문자열까지만 소모되도록 막을 수 있을까?

다음과 같이 non-greedy 문자인 ?을 사용하면 *의 탐욕을 제한할 수 있다.

print(re.match('<.*?>', s).group())
# <html>

non-greedy 문자인 ?은 *?, +?, ??, {m,n}?과 같이 사용할 수 있다. 가능한 한 가장 최소한의 반복을 수행하도록 도와주는 역할을 한다.



'''

# 예9.
line = 'asdf fjdk; afed, fjel, asdf,     foo'
import re
re.split(r'[;,\s]\s*', line)  # 세미콜론, 쉼표, 공백(\s), 공백여러개(\s*)를 구분자로 써서 글자를 구분
#['asdf', 'fjdk', 'fjek', 'asdf', 'foo']

# 예10.

# match 메소드 사용
m = p.match("python")
m.group()
# 'python'
m.start()
# 0
m.end()
# 6
m.span()
# (0, 6)

# search 메소드 사용
m = p.search("3 python")
m.group()
# 'python'
m.start()
# 2
m.end()
# 8
m.span()
# (2, 8)