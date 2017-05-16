p = (4,5)
x,y=p
x
y

data = ['ACME',50,91.1,(2012,12,21)]
names,shares,price,date = data
names
type(date)
name, shares, price, (year,mon,day)=data
year
mon
day

p=(4,5)
x,y,z=p
s='hello'
a,b,c,d,e=s
a+b+c+d+e
_,shares,price,_=data
shares
price

def drop_first_last(grades):
    first,*middle,last = grades
    return avg(middle)

record = ('Dave','744-555-1212','123-456-7777','123-222-4444','dave@example.com')
name, *phone_numbers,email = record
name
phone_numbers

records=[
    ('foo',1,2),
    ('bar','hello'),
    ('foo',3,4)
]
records
type(records)

def do_foo(x,y):
    print('foo',x,y)

def do_bar(s):
    print('bar',s)

for tag,*args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag=='bar':
        do_bar(*args)

line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
uname, *field, homedir, sh=line.split(':')
uname
field
homedir
sh

record = ('ACME',50,123.45,(12,18,2012))
name, *_, (*_,year)=record
name
year

items=[1,10,7,4,5,9]
head, *tail = items
head
tail
type(tail)

def sum(items):
    head,*tail=items
    return head+sum(tail) if tail else head

sum(items)

from collections import deque
def search(lines,pattern,history=5):
    previous_lines=deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        previous_lines.append(line)

from collections import deque
q=deque(maxlen=3)
q.append(1)
q.append(2)
q.append(3)
q
q.append(4)
q=deque()
q.appendleft(4)
q.pop()
q
q.popleft()

import heapq
nums = [1,8,9,2,23,7,-4,18,23,42,37,2]
print(heapq.nlargest(3,nums))
print(heapq.nsmallest(3,nums))

portfolio = [{'name' : 'IBM', 'shares' : 100, 'price': 91.1},
             {'name' : 'AAPL', 'shares' : 50, 'price' : 543.22}]

cheap =heapq.nsmallest(3,portfolio,key=lambda s : s['price'])
expensive = heapq.nlargest(3, portfolio,key=lambda s:s['price'])

cheap
expensive

import heapq
heap = list(nums)
heapq.heapify(heap)
heap
heapq.heappop(heap)

import heapq

class PriorityQueue:
    def __init__(self):
        self._queue=[]
        self._index=0

    def push (self, item, priority):
        heapq.heappush(self._queue,(-priority,self._index,item))
        self._index+=1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

class Item:
    def __init__(self,name):
        self.name = name
    def __repr__(self):
        return 'Item({!r})'.format(self.name)

q=PriorityQueue()
q.push(Item('foo'),1)
q.push(Item('bar'),5)
q.push(Item('spam'),4)
q.push(Item('grok'),1)
q.pop()

a=Item('foo')
b=Item('bar')
a<b
a=(1,Item('foo'))
b=(5,Item('bar'))
a<b
c=(1,Item('grok'))
a<c
a=(1,0,Item('foo'))
b=(5,1,Item('bar'))
c=(1,2,Item('grok'))
a<c

#1.6 딕셔너리의 키를 여러 값에 매핑하기.
# 문제 : 딕셔너리의 키를 하나 이상의 값에 매핑하고 싶다.(Multidict)
# 해결
d = { 'a' : [1,2,3],
      'b' : [4,5]
      }
e = { 'a' : [1,2,3],
      'b' : [4,5]
      }

# 아이템의 삽입 순서를 지켜야 한다면 리스트, 순서가 상관없고 중복을 제거하려면 세트.
from collections import defaultdict
d=defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)
print(d)
d=defaultdict(set)
d['a'].add(1)
d['b'].add(2)
d['b'].add(4)
print(d)

#다만 defaultdict를 사용할 때는 딕셔너리에 존재하지 않는 값이라도 한 번이라도 접근했던 키의 엔트리를 자동으로 생성.
#이런 동작성이 맘에 들지 않으면 setdefault()
d={}
d.setdefault('a',[]).append(1)
d.setdefault('a',[]).append(2)
d.setdefault('b',[]).append(4)
print(d)
#토론 이론적으로 여러값을 가지는 딕셔너리를 만드는 것이 복잡하지는 않지만, 첫번째 값에 대한 초기화를 스스로 하려면 꽤나 복잡하다.


#1.7 딕셔너리 순서 유지
#문제 : 딕셔너리를 만들고 순환이나 직렬화 할 때 순서를 조절하고 싶다.
#해결 : 딕셔너리 내부 아이템의 순서를 조절하려면 collection 모듈의 Ordereddict를 사용한다. 이 모듈을 사용하면 삽입 초기의 순서를 그대로 기억한다.
from collections import OrderedDict
d=OrderedDict()
d['foo']=1
d['bar']=2
d['spam']=3
d['grok']=4
for key in d:
    print(key,d[key])
#Ordereddict는 나중에 직렬화 하거나 다른 포맷으로 인코딩 할 다른 매핑을 만들 때 특히 유용하다. 예를들어
#json 인코딩에 나타나는 특정 필드의 순서를 조절하기 위해서 Ordereddict에 다음과 같이 데이터를 생성한다.
import json
json.dumps(d)
#토론 ordereddict는 내부적으로 더블 링크드 리스트로 삽입 순서와 관련 있는 키를 기억한다.따라서 새로운 아이템을 처음으로 삽입하면 리스트의 제일 끝에 위치.
#이 때문에 일반적인 딕셔너리에 비해 크기가 두배로 크다. 따라서 추가적인 메모리 소비가 실질적으로 유용한지 살펴보아야 함.

#1.8 딕셔너리 계산
#문제 : 딕셔너리 데이터에 ㅇ러 계산을 수행하고 싶다.(최대,최소, 정렬 등)
#해결 : 딕셔너리에 주식이름과 가격이 들어 있다고 가정해보자.
prices = {
    'ACME' : 45.23,
    'AAPL' : 612.78,
    'IBM' : 205.55,
    'HPQ' : 37.20,
    'FB' : 10.75
}
#딕셔너리 내용에 대해 유용한 계산을 하려면 딕셔너리의 키와 값을  zip()으로 뒤집어 주는 것이 좋음.
min_price = min(zip(prices.values(),prices.keys()))
min_price
max_price = max(zip(prices.values(),prices.keys()))
max_price
#데이터의 순서를 매기려면 zip, sorted  사용
prices_sorted = sorted(zip(prices.values(),prices.keys()),reverse=True)
prices_sorted
#계산을 할 때 zip은 한번만 소비할 수 있는 이터레이터를 생성. 예를 들어 다음과 같은 코드에서는 에러가 발생한다.
prices_and_names = zip(prices.values(),prices.keys())
print(min(prices_and_names))
print(max(prices_and_names))
#토론: 딕셔너리에서 일반적인 데이터 축소르 시도하면, 오직 키에 대해서만 작업이 이루어진다.
min(prices)
max(prices) # key값이 도출됨. value값으로 하려면
min(prices.values())
max(prices.values()) # value값이 도출됨. 그러면 해당 value값에 대한 key값을 도출하려면?
min(prices,key=lambda k :prices[k])
max(prices,key=lambda k :prices[k])
#최소값을 얻기 위해서 한 번 더 살펴보는 작업이 필요하다.
min_value = prices[min(prices,key=lambda k:prices[k])]
min_value
#zip()을 포함한 해결책은 딕셔너리의 시퀀스를 value, key 페어로 뒤집는 것으로 문제를 해결한다. 이런 튜플에 비교를 수행하면 값(value) 요소를 먼저 비교하고 뒤이어
#key를 비교한다. 이렇게 하면 명령어 하나만으로 정확히 우리가 원하는 데이터 축소화 정렬을 수행한다.
#여러 엔트리가 동일한 값을 가지만 비교 결과를 결정하기 위해서 키를 사용한다.
prices = {'AAA' : 45.23, 'ZZZ' : 45.23}
min(zip(prices.values(),prices.keys()))
max(zip(prices.values(),prices.keys()))

#1.9 두 딕셔너리의 유사점 찾기.
#문제 두 딕셔너리가 있고 여기서 유사점을 찾고 싶다.(동일한 키, 동일한 값 등).
#해결 다음 두 딕셔너리를 보자.
a = {
    'x':1,
    'y':2,
    'z':3
}
b={
    'w':10,
    'x':11,
    'y':2
}
# 동일한 키 찾기
a.keys() & b.keys()
# a에만 있고 b에는 없는 키 찾기
a.keys() - b.keys()
#키 값 동일한 것
a.items() & b.items()
# 이런 연산을 이용하여 딕셔너리의 내용을 수정하거나 걸러낼 수도 있다.예를 들어 선택한 키를 삭제한 새로운 딕셔너리를
# 만들고 싶을 때는 다음과 같은 딕셔너리 생성 코드를 사용한다.
#특정 키를 제거한 새로운 딕셔너리 만들기
c = {key:a[key] for key in a.keys() - {'z','w'}}
c
#딕셔너리는 키와 값의 매핑으로 이루어 진다. 딕셔너리의 keys()메소드는 키를 노출하는 키-뷰 객체를 반환한다. 키 뷰에는 잘 알려지지 않았지만
#합집합, 교집합, 여집합과 같은 집합 연산 기능이 있다. 따라서 딕셔너리 키에 집합 연산을 수행하려면 집합으로 변환할 필요 없이
#키-뷰 객체를 사용하면 된다.
#딕셔너리의 items() 메소드는 key,value 페어로 구성된 아이템-뷰 객체를 반환한다. 이 객체는 집합 연산과 유사한 것을 지원하므로 두 딕셔너리에 동일한
#키-값 페어를 찾을 때 사용할 수 있다.
#유사하기 하지만 vales() 메소드는 앞에 나온 집합 연산을 지원하지 않는다. 이는 키와는 다르게 값-뷰는 유일하다는 보장이 없기 때문이다. 이 사실만으로도 특정
# 집합 연산을 사용할 수 없다. 하지만 반드시 이런 비교를 수행해야 한다면 먼저 값을 집합으로 변환하면 된다.

#1.10 순서를 깨지 않고 시퀀스의 중복 없애기
#문제 : 시퀀스에서 중복된 값을 없애고 싶지만 아이템의 순서는 유지하고 싶다.
#해결 : 시퀀스의 값이 해시(hash) 가능하다면 이 문제는 세트와 제너레이터를 사용해서 쉽게 해결할 수 있다.
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)

a=[1,5,2,1,9,1,5,10]
list(dedupe(a))
#시퀀스의 아이템이 해시 가능한 경우에만 사용할 수 있다. 해시 불가능한 타입(예를 들면 dict)의 중복을 없애려면 레시피에 약간의 수정이 필요.
def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)

a = [{'x' :1, 'y':2}, {'x' : 1, 'y' : 3}, {'x' : 1,'y':2},{'x':2,'y':4}]
list(dedupe(a, key = lambda d : (d['x'],d['y'])))
list(dedupe(a, key = lambda d : d['x']))
#다음 해결책은 필드가 하나이거나 커다란 자료 구조에 기반한 값의 중복을 없앨 때도 잘 작동한다.
#토론 : 중복을 없애려면 대게 세트를 만드는 것이 가장 쉽다.
a=[1,5,2,1,9,1,5,10]
set(a)
#하지만 이 방식을 사용하면 기존 데이터의 순서가 훼손됨. 하지만 앞에 설명한 방법을 사용하면 이 문제를 피할수 있다.
#제너레이터 함수를 사용했기 때문에 단순히 리스트 프로세싱 말고도 아주 일반적인 목적으로 함수를 사용할 수 있다.
#예를 들어 파일을 읽을 때 중복된 라인을 무시하려면 단순히 다음과 같은 코드를 사용한다.
#with open(somefile,'r') as f:
#    for line in dedupe:
#        if ...:

#key 함수의 스펙은 파이썬 내장 함수인 sorted(), min(), max() 등의 기능을 흉내 내고 있다. 자세한 내용은 레시피 1.8과 1.13을 참고.
#1.11 슬라이스 이름 붙이기.
#문제. 프로그램 코드에 슬라이스를 지시하는 하드코딩이 너무 많아 이해하기 어려운 상황이다. 이를 정리하자.
#해결. 고정된 문자열로부터 특정 데이터를 추출하는 코드가 있다고 가정해보자.
record='.....100513.23 ...'
shares = slice(5,8)
price = slice(8,14)
cost=int(record[shares])*float(record[price])
cost
record[5:8]
record[8:14]
#토론: 일반적으로 하드코딩이 늘어날수록 이해하기 어렵고 지저분해진다.
#slice()는 슬라이스 받는 모든 곳에 사용할 수 있는 조각을 생성한다.
items=[0,1,2,3,4,5,6]
a=slice(2,4)
items[2:4]
items[a]
items[a]=[10,11]
items
del items[a]
items
#slice 인스턴스 s가 있다면 s.start , s.stop, s.step 속성을 통해 좀 더 많은 정보를 얻을 수 있다.
a=slice(10,50,2)
a.start
a.stop
a.step
#indices(size) 메소드를 사용하면 특정 크기의 시퀀스에 슬라이스를 매핑할 수 있다. 이렇게 하면 튜플을 반환하는데 모든값은 경계를 넘어서지 않도록
#제약이 걸려 있다.(인덱스에 접근할 때 indexError예외가 발생하지 않도록 하기 위함.
s='HelloWorld'
a.indices(len(s))
for i in range(*a.indices(len(s))):
    print(s[i])

#1.12 시퀀스에 가장 많은 아이템 찾기.
#문제 시퀀스에 가장 많은 아이템을 찾고 싶다.
#해결 collections.Counter, most_common()
words=['']
from collections import Counter
words_counts = Counter(words)
top_three = words_counts.most_common(3)
print(top_three)
#r이러면 단어, 단어의 갯수가 3위까지 출력됨.
#토론 counter 객체에는 해시 가능한 모든 아이템을 입력할 수 있다. 내부적으로 counter는 아이템이 나타난 횟수를 가리키는 딕셔너리이다.
words_counts['not'] # 1
#카운트를 수동으로 증가시키고 싶다면 단순하게 더하기를 사용한다.
morewords = ['why','are','you','looking','in','my','eyes']
for word in morewords:
    words_counts[word] +=1
#혹은 update() 메소드
#Counter 인스턴스에 잘 알려지지 않은 기능으로 여러가지 수식을 사용할 수 있다는 점이 있다.
a=Counter(words)
b=Counter(morewords)
c=a+b
#-> a와 b의 단어 갯수를 합친다. 혹은 뺄 수도 있음.
#1.13 일반 키로 딕셔너리 리스트 정렬
#문제 딕셔너리 리스트가 있고, 하나 호은 그 이상의 딕셔너리 값으로 이를 정렬하고 싶다.
#해결 이와 같은 구조는 operator 모듈의 itemgetter 함수를 사용하면 쉽게 정렬할 수 있다. 어느 웹사이트 회원 리스트를 데이터베이스로부터 불러와 다음과 같은 자료구조를 만들었다고 가정
rows=[{'fname':'Brian','lname':'Jones','uid':1003},
      {'fname':'David','lname':'Beazley','uid':1002}]
#모든 딕셔너리에 포함된 필드를 기준으로 데이터를 정렬해  출력하는 것은 어렵지 않다.
from operator import itemgetter
rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows,key=itemgetter('uid'))
print(rows_by_fname) # fname을 오름차순으로 정렬
print(rows_by_uid) # uid를 오름차순으로 정렬
#itemgetter()함수에는 키를 여러개 전달할 수도 있다. 예를 들어
rows_by_lfname = sorted(rows,key=itemgetter('lname','fname'))
print(rows_by_lfname)
#토론 이번 예제에서 키워드 인자 key를 받는 내장 함수 sorted()에 rows를 전달했다.
#이 인자는 rows로부터 단일 아이템을 받는 호출 가능 객체를 입력으로 받고 정렬의 기본이 되는 값을 반환한다.
#itemgetter()함수는 그런 호출 가능 객체를 생성한다,
#operator, itemgetter() 함수는 rows 레코드에서 원하는 값을 추출하는데 사용하는 인덱스를 인자로 받는다. 딕셔너리 키 이름이나 숫자 리스트 요소가 될 수도 있고, 객체의
#__getitem__() 메소드에 넣을 수 있는 모든 값이 가능하다. itemgetter()에 여러인덱스를 전달하면, 생성한 호출 가능 객체가 모든 요소를 가지고 있는 튜플을 반환하고
#sorted()가 튜플의 정렬 순서에 따라 결과의 모든 순서를 잡는다. 이 방식은 여러 필드를 동시에 정렬할 때 유용하다.
#itemgetter()의 기능을 때때로 lambda 표현식으로 대체할 수 있다.
rows_by_fname = sorted(rows, key=lambda r: r['fname'])
rows_by_fname
#이 코드도 잘 되지만 itemgetter()의 실행속도가 조금더 빠르다. min. max도 사용 가능
#1.14 기본 비교기능 없이 객체 정렬
#문제 동일한 클래스 객체를 정렬해야 하는데 이 클래스는 기본적인 비교 연산을 제공하지 않는다.
#해결 내장 함수 sorted()는 키 인자에 호출 가능 객체를 받아 sorted가 객체 비교에 사용할 수 있는 값을 반환한다. 예를 들어, 애플리케이션에 user 인스턴스를 시퀀스로 갖고 있고
#이를 user_id 요소를 기반으로 정렬하고 싶다. 이럴 때느 ㄴuser 인스턴스를 입력으로 받고 user_id를 반환하는 코드를 작성할 수 있다.
class User:
    def __init__(self,user_id):
        self.user_id=user_id
    def __repr__(self):
        return 'User({})'.format(self.user_id)

users=[User(23),User(3),User(99)]
users
sorted(users,key=lambda u: u.user_id)
#람다 대신 operator.attrgetter()를 사용해도 된다.
from operator import attrgetter
sorted(users, key=attrgetter('user_id'))
#토론 람다를 사용할지 attrgetter()를 사용할지 여부는 개인의 선호도에 따라 갈릴 수 도 있다. 하지만 attrgetter()의 속도가 빠른 경우가 종종 있고 동시에 여러 필드를 추출
#하는 기능이 추가 되어 있다. 이는 딗너리의 operator.itemgetter()를 사용하는 것과 유사한 점이 있다.
#예를 들어 ,User인스턴스에 first_name과 last_name 속성이 있다면 다음과 같이 정렬할 수 있다.
#또한 min,max도 사용 가능하다.


#1.15 필드에 따라 레코드 묶기
#문제. 일련의 딕셔너리나 인스턴스가 있고 특정 필드 값에 기반한 그룹의 데이터를 순환하고 싶다.
#해결 : itertools.groupby() 함수는 이와 같은 데이터를 묶는데 유용하다. 다음과 같은 딕셔너리 리스트가 있다고 가정해보자.
rows = [
    {'address' : '5412 N CLARK1', 'date' : '07/01/2012'},
{'address' : '5148 N CLARK2', 'date' : '07/01/2012'},
{'address' : '5800 N CLARK3', 'date' : '07/02/2012'},
{'address' : '2122 N CLARK4', 'date' : '07/02/2012'},
{'address' : '5645 N CLARK5', 'date' : '07/03/2012'},
{'address' : '1060 N CLARK6', 'date' : '07/03/2012'},
{'address' : '4801 N CLARK7', 'date' : '07/04/2012'},
{'address' : '1039 N CLARK8', 'date' : '07/04/2012'},
]
from operator import itemgetter
from itertools import groupby

rows.sort(key=itemgetter('date'))#우선 원하는 필드로 정렬
for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print(' ',i)

#토론 groupby() 함수는 시퀀스를 검색하고 동일한 값(혹은 키 함수에서 반환한 값)에 대한 일련의 실행을 찾는다.
# 개별 순환에 대해서 값, 그리고 같은 값을 가진 그룹의 모든 아이템을 만드는 이터레이터를 함께 반환한다.
# 그에 앞서 원하는 필드에 따라 데이터를 정렬해야 하는 과정이 중요하다. groupby() 함수는 연속된 아이템에만
# 동작하기 때문에 정렬 과정을 생략하면 원하는 대로 함수를 실행할 수 없다.
# 단순히 날짜에 따라 데이터를 묶어서 커다란 자료 구조에 넣어 놓고 원할 때마다 접근하려는 것이라면 defaultdict()를 사용해서 multidict를 구성하는게 나을수도 있다.
from collections import defaultdict
rows_by_date = defaultdict(list)
for row in rows:
    rows_by_date[row['date']].append(row)
for r in rows_by_date['07/01/2012']:
    print(r)
#이 과정은 정렬 과정을 생략해도 된다. 메모리 사용량에 크게 구애 받지 않는다면 이 방식을 사용하는 것이 정렬 후 그룹바이를 사용하는 방법보다 빠르다.

#1.16 시퀀스 필터링
#문제 시퀀스 내부에 데이터가 있고 특정 조건에 따라 값을 추출하거나 줄이고 싶다.
#해결 가장 간단한 해결책은 리스트 컴프리핸션이다.
mylist=[1,4,-5,'N/A',-7,2,3,-1]
[n for n in mylist if n>0]
[n for n in mylist if n<0]
# 입력된 내용이 크면 매우 큰 결과가 생성될 수도 있다. 이는 생성자 표현식을 사용해서 값을 걸러낼 수 있다.
pos=(n for n in mylist if n>0)
pos
for x in pos:
    print(x)
#필터링 도중 복잡한 내용이 들어가려면?
def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False
ivals = list(filter(is_int,mylist))
print(ivals)
#filter()는 이터레이터를 생성한다 따라서 결과의 리스트를 만들고 싶다면 위에 나온대로 list를 함께 사용해야.
#토론 : 리스트 컴프리핸션과 생성자 표현식은 간단한 데이터를 걸러 내기 위한 가장 쉽고 직관적인 방법. 데이터 변형도 가능
mylist=[1,4,-5,10,-7,2,3,-1]
import math
[math.sqrt(n) for n in mylist if n>0]
clip_neg = [n if n>0 else 0 for n in mylist]
clip_neg
#또 다른 주목할 만한 필터링 도구로 순환 가능한 Boolean 셀렉터 시퀀스를 입력으로 받는 itertools.compress()가 있다. 그렇게
#입력하면 셀렉터에서 조건이 참인 요소만 골라서 반환.이것은 어떤 시퀀스의 필터링 결과를 다른 시퀀스에 반영하려 할 때 유용하다. 다음과 같이
# 두개의 열이 있는 데이터를 가정하자.
addresses = [
    '5412 N CLARK',
'5413 N CLARK',
'5414 E CLARK1',
'5415 N CLARK2',
'5416 N CLARK3',
'5417 N CLARK4',
'5418 N CLARK5',
]

#1.17 딕셔너리의 부분 추출
#문제  딕셔너리의 특정 부분으로부터 다른 딕셔너리를 만들고 싶다.
#해결 딕셔너리 컴프리헨션을 사용하면 해결된다.
prices = {
    'ACME' : 45.23,
    'AAPL' : 612.78,
    'IBM' : 205.55,
    'HPQ' : 37.20,
    'FB' : 10.75
}
p1 = {key:value for key, value in prices.items() if value>200}
p1
tech_names={'AAPL','IBM'}
p2 = {key:value for key, value in prices.items() if key in tech_names}
p2
#토론 딕셔너리 컴프리ㅔㄴ션으로 할 수 있는 대부분의 일은 튜플 시퀀스를 만들고 dict() 함수에 전달하는 것으로도 할 수 있다.
#하지만 딕셔너리 컴프리헨션이 더 빠르고 깔끔하다.
p1 = dict((key,value) for key, value in prices.items() if value > 299)
p1

#1.18 시퀀스 요소에 이름 매핑
