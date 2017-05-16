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


'''