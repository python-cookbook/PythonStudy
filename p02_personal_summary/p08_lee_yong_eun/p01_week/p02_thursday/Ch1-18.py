#######################################################################################
# 1.18] 시퀀스 요소에 이름 매핑
#       * 리스트나 튜플의 위치로 요소에 접근하는 코드가 있는데, 때로 가독성이 떨어진다.
#         또한 위치에 의존하는 코드의 구조도 이름으로 접근 가능하게 수정하고 싶다.
#
# 1] collections.namedtuple()
#       : 튜플과 각 요소에 이름을 붙여서 가독성을 높인다.
#         튜플과 교환이 가능하고, 인덱싱 및 언패킹과 같은 튜플의 일반적인 기능을 모두 지원한다.
#
# 2] namedtuple을 딕셔너리 대신 사용할 때의 장단점
#       장점 : 딕셔너리가 저장 공간을 더 필요로 하므로 효율적이다.
#       단점 : 네임드튜플은 수정할 수 없다. (_replace 메소드를 사용해 지정한 값을 치환하여 새로운 네임드튜플 생성)
#               => 인스턴스 요소를 빈번히 수정해야 하는 자료 구조를 만들 때는 namedtuple을 사용하지 않는 것이 좋다.
#                   대신 __slots__를 사용하여 클래스를 정의하는 것을 고려해보자. (8.4 참고)
#######################################################################################

from collections import namedtuple

#namedtuple
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com', '2012-10-19')
print(sub)  # Subscriber(addr='jonesy@example.com', joined='2012-10-19')
print(sub.addr) # jonesy@example.com
print(sub[1])   # 2012-10-19

# 언패킹
addr, joined = sub
print(addr, joined) # jonesy@example.com 2012-10-19

# 실제 사용 예시
Stock = namedtuple('Stock', ['name', 'shares', 'price'])
def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total
# 내부에서 Stock으로 받아서 쓰므로 일반적인 리스트나 튜플을 넣어서 사용해도 무방하다 !
input = [
    ('A', 3, 5.5),
    ('B', 2, 10)
]
print(compute_cost(input))  # 36.5

# _replace를 사용한 값 치환
s = Stock('ACME', 100, 123.45)
s = s._replace(shares=75)
print(s)    # Stock(name='ACME', shares=75, price=123.45)

# _replace를 이용하여 옵션이나 빈 필드를 가진 네임드 튜플 간단히 만들기
Stock2 = namedtuple('Stock2', ['name', 'shares', 'price', 'date', 'time'])
stock_prototype = Stock2('', 0, 0.0, None, None)
def dict_to_stock2(s):
    return stock_prototype._replace(**s)

a = {'name': 'ACME', 'shares': 100, 'price': 123.45}
print(dict_to_stock2(a))    # Stock2(name='ACME', shares=100, price=123.45, date=None, time=None)