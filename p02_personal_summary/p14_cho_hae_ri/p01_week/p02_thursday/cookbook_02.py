'''

### 1.18 시퀀스 요소에 이름 매핑
#collections.namedtuple() : tuple 타입의 서브클래스를 반환하는 팩토리 메소드. 인스턴스화 가능한 클래스를 반환한다.

from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com','2017-05-16')

print(sub) # Subscriber(addr='jonesy@example.com', joined='2017-05-16')

print(sub.addr) # jonesy@example.com

print(sub.joined) # 2017-05-16


# namedtuple의 인스턴스는 튜플과 겨환이 가능하고, 인덱싱이나 언패킹과 같은 튜플의 기능들을 지원한다.


#print(len(sub)) # 2

addr, joined = sub
print(addr) # jonesy@example.com
print(joined) # 2017-05-16

# 네임드튜플은 주로 요소의 위치를 기반으로 구현되어 있는 코드를 분리한다. db 테이블에 새로운 열이 추가되는 경우 문제가 발생할 수 있다.
# but!! 반환된 튜플을 네임드 튜플로 변환했다면 이런 문제를 방지할 수 있다.

# 일반적인 튜플을 사용하는 코드
def conpute_cost(records):
    total = 0.0
    for rec in records:
        total += rec[1] * rec[2]
    return total

# 네임드 튜플을 사용하는 코드

from collections import namedtuple
Stock = namedtuple('Stock', ['name', 'shares', 'price'])
def conpute_cost(records):
    total =0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares* s.price
    return total

# namedtuple은 딕셔너리 대신 사용할 수 있으며 저장공간 측면에서 더 효율적이다. 하지만 딕셔너리와 달리 수정할 수 없다는 점!

s = Stock('ACME', 100, 123.45)
print(s) # Stock(name='ACME', shares=100, price=123.45)

s.shares = 87 # AttributeError: can't set attribute


# 속성을 수정해야 할 경우 replace() 메소드를 사용해야 한다.

from collections import namedtuple
Stock = namedtuple('Stock', ['name', 'shares', 'price'])
def conpute_cost(records):
    total =0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares* s.price
    return total

s = Stock('ACME', 100, 123.45)

s = s._replace(shares=78)
print(s) # Stock(name='ACME', shares=78, price=123.45)


# _replace 메소드를 사용하면 옵션이나 빈 필드를 가진 네임드 튜플을 간단히 만들 수 있다.

from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price', 'date', 'time'])

# 프로토 타입 인스턴스 생성
stock_prototype = Stock('', 0, 0.0, None, None)
# 딕셔너리를 stock으로 변환하는 함수
def dict_to_stock(s):
    return stock_prototype._replace(**s)

# 이 코드를 사용하는 예는 다음과 같다.
a = {'name':'ACME', 'shares':78, 'price':123.45}
#print(dict_to_stock(a))  # Stock(name='ACME', shares=78, price=123.45, date=None, time=None)
b = {'name':'ACME', 'shares':100, 'price':123.45, 'date':12/13/2013}
#print(dict_to_stock(b)) #Stock(name='ACME', shares=100, price=123.45, date=0.00045855783560701593, time=None)


### 1.19. 데이터를 변환하면서 줄이기

# 문제 : 감소함수(sum(), min(), max()) 를 실행해야 하는데, 먼저 데이터를 변환하거나 필터링해야 한다

# 데이터를 줄이면서 변형하는 가장 우아한 방식은 생성자 표현식을 사용하는 것이다. 예를 들어 정사각형 넓이의 합을 계산하려면,

nums = [1,2,3,4,5]
s = sum(x*x for x in nums)

print(s) # 55
'''
## 대안으로 다음과 같은 코드도 가능하다

# 디렉토리에 또 다른 .py 파일이 있는지 살펴본다.
import os
files = os.listdir('dirname')
if any(name.endswith('.py') for name in files):
    print('There be python!')
else:
    print('Sorry, no python')

















