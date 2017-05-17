"""
▶ 1.18 시퀀스 요소에 이름 매핑 ◀ 
♣ 문제 : 리스트나 튜플의 위치로 요소에 접근하는 코드가 있다. 하지만 때론 이런 코드는 가독성이 떨어진다.
            가독성이 좋게 하고, 이름으로도 코드에 접근 가능하도록 수정하려면?
 ↘ 해결 : collections.namedtuple() 사용하면 일반적인 튜플 객체를 사용하는 것에 비해 좋은 성능으로 기능 구현한다
           실제로 표준 파이썬 tuple타입의 sub class를 반환하는 팩토리 메소드이다. 
        타입이름   /  포함해야할 필드  를 전달하면 
        인스턴스화 가능한 클래스를 반환한다. 이를 필드의 값에 전달하는 식으로 사용 가능함
            
"""
print('########################################## 1.18 시퀀스 요소에 이름 매핑 #####################################')
from collections import namedtuple
Subscriber = namedtuple('Subscriber',['addr','joined'])  #namedtuple ( '타입이름', ['Field1','Field2'..] )
sub = Subscriber('jonesy@example.com','2012-10-19')
print(sub)  # <class '__main__.Subscriber'>
print(sub.addr)
print(sub.joined)

# neamedtuple의 인스턴스는 일반적인 클래스 인스턴스와 비슷해 보이지만, 튜플과 교환이가능하고, 인덱싱이나
# 언패킹과 같은 튜플의 일반적인 기능을 모두 지원한다.
len(sub)
addr,joined = sub
addr
joined

# namedtuple은 주로 요소의 위치를 기반으로 구현되어 있는 코드를 분리한다.
# 따라서 DB로부터 거대한 튜플 리스트를 받고 요소의 위치로 접근하는 코드가 있을 때
# 뭐 예를들어 테이블에 새로운 열이 추가된다거나 할때..
# 하지만, 반환된 튜플을 네임드 튜플로 변환했다면 이런 문제 예방 가능

# def compute_cost(records):
#     total = 0.0
#     for rec in records:
#         total += rec[1] * rec[2]
#     return total

from collections import namedtuple
Stock = namedtuple('Stock',['name','shares','price'])

def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)              #records 시퀀스에 이미 인스턴스가 포함되어 있기 때문에 Stock 네임드  튜플로 명시적인 변환 하지않아도 됨.
        total += s.shares *s.price
        # total += rec[1] * rec[2]
    return total


# 네임드 튜플은 저장 공간을 더 필요로 하는 딕셔너리 대신 사용할 수 있다.
# 딕셔너리를 포함한 방대한 자료 구조를 구상한다면 네임드 튜플을 꼭 써라! 하지만 딕셔너리와는 다르게
# 네임드 튜플은 수정할 수 없다는 점을 기억해야 한다.

s = Stock('ACME',100,123.45)
print(s)
# s.shares = 75     #AttributeError: can't set attribute 왜냐면 튜플이잖아.

# 속성을 수정해야겠다면 네임드튜플 인스턴스의 _replace() 메소드 사용해야 한다. 이 메소드는 지정한 값을 '치환'하여 완전히 새로운 네임드튜플을 만든다.

s = s._replace(shares = 75)
print(s)  # shares = 75

# _replace() 메소드를 사용하면 옵션이나 빈 필드를 가진 네임드 튜플을 간단히 만들 수 있다.
# 일단 default값을 가진 프로토타입 튜플을 만들고, _replace()로 치환!

from collections import namedtuple
Stock = namedtuple('Stock',['name','shares','price','date','time'])
# 프로토타입 인스턴스 생성 ( 튜플)
prototype = Stock('',0,0.0,None,None)     #빈 필드를 가진 네임드 튜플 생성


# 딕셔너리를 Stock으로 변환하는 함수
def dict_to_stcok(s):
    return prototype._replace(**s)

# 위 함수 사용하기

a = {'name':'ACME','shares':100,'price':123.45}
print(dict_to_stcok(a)) # Stock(name='ACME', shares=100, price=123.45, date=None, time=None)

b = {'name':'ACME','shares':100,'price':123.45, 'date':'12/17/2012'}
print(dict_to_stcok(b)) #Stock(name='ACME', shares=100, price=123.45, date='12/17/2012', time=None)

"""
▶ 1.19 데이터를 변환하면서 줄이기 ◀ 
♣ 문제 : 감소 함수 ( sum(), min(), max() ) 를 실행해야 하는데,, 먼저 데이터를 변환하거나 필터링 해야 한다.
 ↘ 해결 : 데이터를 줄이면서 변형하는 가장 우아한 방식은 [생성자 표현식]을 사용하는 것이다.
           예를 들어, 정사각형 넓이의 합을 계산하려면 다음과 같이 한다.
"""
print('########################################## 1.19 데이터를 변환하면서 줄이기 #####################################')

# 정사각형 넓이의 합 계산하기

nums = [1,2,3,4,5]
s = [x*x for x in nums]
print(s)
d = sum(x*x for x in nums)
print(d)

# 또 다른 방법은?
# 디렉토리에 또 다른 .py 파일이 있는지 살펴본다.
import os
files = os.listdir('c:/python/source/PythonClass/Algorithm')
if any(name.endswith('.py') for name in files):
    print('There be python!')
else:
    print('Sorry, no python')

# 튜플을 CSV로 출력한다.

s = ('ACME',50,123.45)
print(','.join(str(x) for x in s))


# 자료 구조의 필드를 줄인다.
portfolio = [
   {'name':'GOOG', 'shares': 50},
   {'name':'YHOO', 'shares': 75},
   {'name':'AOL', 'shares': 20},
   {'name':'SCOX', 'shares': 65}
]

min_shares = min(s['shares'] for s in portfolio)
print(min_shares)

# 위 코드는 함수에 인자로 전달된 생성자 표현식의 문법적인 측면을 보여준다.
# 예를 들어 다음 두 코드는 동일함

s = sum((x*x for x in nums))
s = sum(x*x for x in nums)  #생성자 표현식 덕분
print(s)
# 생성자 표현식 사용하지 않았을 때
s = sum([x*x for x in nums]) # 리스트 컴프리헨션
print(s)






"""
▶ 1.20 여러 매핑을 단일 매핑으로 합치기 ◀ 
♣ 문제 : dict or 맵핑이 여러개 있고, 자료 검색이나 데이터 확인을 위해서 하나의 매핑으로 합치고 싶다.
 ↘ 해결 : 다음과 같이 두 딕셔너리가 있다고 가정해본다.
            두 딕셔너리에 모두 검색을 해야 할 상황이라고 하자
            (우선 a에서 data를 검색하고, 그 후 b에도 data가 있는지 검색)
            간단하게 collections모듈의 chainMap클래스 사용하면 됨.

from collections import ChainMap
c = ChainMap(a,b)
            
            
values = ChainMap()
#새로운 맵핑 추가하기
values = values.new_child()
#마지막 번째 맵핑 삭제하기
values = values.parents 
"""
print('########################################## 1.20 여러 매핑을 단일 매핑으로 합치기 #####################################')

a = {'x':1,'z':3}
b = {'y':2,'z':4}

from collections import ChainMap
c = ChainMap(a,b)   # a에 있는게 b에도 있나~ 보자~
print(c['x'])  # a의 1출력
print(c['y'])  # b의 2출력
print(c['z'])  # a의 3을 출력

# 왜 z는 4를출력하지 않고?? a에는 y없는데 왜 y나옴?

# z의 경우처럼 한가지 키('z')에 중복되는 value가 있으면 첫번째 매핑의 값을 사용한다. (a의 z의 밸류(3) )
# 즉 ChainMap은 매핑에 대한 리스트를 유지하며 스캔하도록 만든것이지, 뭐 두 딕셔너리를 합치거나
# 그런게 아님

# 더 웃긴건, 매핑의 값을 변경하는 동작은 언제나 리스트의 첫번째 매핑에 영향을 준다.
# 즉, 중복됬을때 참조하는 것도 첫번재 리스트 , 즉 a였지만, 만약에 내가 del한다. 라고하면 그것도 첫번째 리스트(a)임.
print(c)
c['z'] = 10
c['w'] = 40
print(a)     # a = {'x': 1, 'z': 10, 'w': 40}       매핑리스트인 c를 바꿧더니, 참조하고 있는 c가 바뀜 ㅋㅋ

del c['x']
print(a)


c['y'] = 50 # 안먹힘 왜?
print(c)
# del c['y']



#ChainMap은 프로그래밍 언어의 변수와 같이 범위가 있는 값(즉, 전역변수, 지역변수) 에서 사용하면 유용함
# 이 동작을 쉽게 해주는 메소드가 있다.

values = ChainMap()   #비어있는 ChainMap인스턴스 활성화
values['x'] = 1       #'x' : 1 선언

#새로운 맵핑 추가하기
values = values.new_child()
values['x'] = 2
#새로운 맵핑 추가하기
values = values.new_child()
values['x'] = 3
print(values)
print(values['x'])   # 3  즉, 첫번째 값을 참조함
#마지막 번째 맵핑 삭제하기
values = values.parents
print(values)
print(values['x'])   # 2  즉, 3을 지운 후 2가 첫번째 값이므로 참조함


#aa

aa