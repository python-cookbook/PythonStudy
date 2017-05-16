#1.10 순서 깨지 않고, 시퀀스 중복 없애기

#해시 가능한 타입
def dedupe(items):
    seen = set()
    for i in items:
        if i not in seen:
            yield i
            seen.add(i)
a = [1,5,2,1,9,1,5,10]
print(list(dedupe(a)))


#해시 불가능한 dict 타입

# example2.py
#
# Remove duplicate entries from a sequence while keeping order

def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item   # yield 는 글로벌한 함수이다. 비휘발성임.
            seen.add(val)

if __name__ == '__main__':
    a = [
        {'x': 2, 'y': 3},
        {'x': 1, 'y': 4},
        {'x': 2, 'y': 3},
        {'x': 2, 'y': 3},
        {'x': 10, 'y': 15}
        ]
    print(a)
    print('#############################################')
    print(list(dedupe(a, key=lambda a: (a['x'],a['y']))))





#1.11 슬라이스 이름 붙이기

"""
문제 :     프로그램 코드에 슬라이스(slice)를 지시하는 하드코딩이 너무많아 이해하기 어려울 때, 이를 정리하려면?
해결 :     내장 함수 slice() 는 모든 곳에 사용할 수 있는 조각을 생성한다.
"""


items=[0,1,2,3,4,5,6]
a = slice(2,4)
items[2:4]
items[a]
items[a]= [10,11]
items

del items[a]
items


a = slice(10,50,2)
print(a.start)
print(a.stop)
print(a.step)


a = slice(5,10,2)
s = 'HelloWorld'
print(a.indices(len(s)))

for i in range(*a.indices(len(s))):
    print(s[i])

# ▩1.12 시퀀스에 가장 많은 아이템 찾기

print('######################################################################')
"""
시퀀스에 가장 많이 나타난 아이템을 찾고 싶다면?

필요한 것은?         collections모듈 / Counter 함수
                    most_common()  메소드
"""

words = [
   'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
   'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
   'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
   'my', 'eyes', "you're", 'under'
]

from collections import Counter
word_counts = Counter(words)
print(word_counts)  #Counter({'eyes': 8, 'the': 5, 'look': 4, 'into': 3, 'my': 3, 'around': 2, 'not': 1, "don't": 1})
top_three = word_counts.most_common(3)
print(top_three)  # [('eyes', 8), ('the', 5), ('look', 4)]


morewords = ['why','are','you','not','looking','in','my','eyes']

for word in morewords:
    word_counts[word] += 1
print(word_counts['eyes']) # 9

word_counts.update(morewords)
print(word_counts.most_common(3)) #9     (위 코드 지워야 9 나옴. 같이하면 10됨..)

word_counts['not']
word_counts['eyes']


a = Counter(words)
b = Counter(morewords)
print(a)
print(b)

c= a+b
d = a-b
print(c)
print(d)


# ▩1.13 일반키로 딕셔너리 리스트 정렬

print('######################################################################')
"""
딕셔너리 리스트가 있고, 하나 혹은 그 이상의 딕셔너리 값으로 이를 정렬하고 싶다.

필요한 것     operator 모듈   / itemgetter 함수

정리 : itemgetter는 호출 가능 객체 요소를 튜플형태로 반환한다.
       sorted가 위와 같은 객체 요소를 키워드인자로 받을 때, 튜플의 순서에 따라 키를 잡고 정렬한다.
       같은 기능으로 itemgetter를 lambda가 대체할 수 있다. 
       그러나 속도,성능은 itemgetter > lambda 
       
"""

from operator import itemgetter


rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]


rows_by_fname = sorted(rows, key=itemgetter('fname')) # fname키값을 기준으로 정렬하라.
rows_by_uid = sorted(rows, key=itemgetter('uid'))  # uid키 값을 기준으로 정렬하라

print(rows_by_fname)
print(rows_by_uid)

# itemgetter함수는 키를 여러개 전달 할 수도 있다.

rows_by_lfname = sorted(rows, key = itemgetter('fname','uid'))
print(rows_by_lfname)



# 키워드 인자 key를 받는 내장함수 sorted에 rows를 전달해서 실습해보았다.
# 이 인자는 rows로부터 단일 아이템을 받는 호출 가능 객체를 입력으로 받고 정렬의 기본이 되는값을
# 반환한다. itemgetter() 가 그런 호출가능한 객체를 생성하는 것이다. 그래서 같이 쓰는것..!!
# 아하.. 그러니까 sorted X itemgetter구나
# operator.itemgetter()가 뽑을수 있는것들은 __getitem__메소드에 넣을 수 있는 것들이면 모든 가능하다
# 반환시킬때 튜플형태로 반환을 하는데, 그 튜플의 정렬 순서에 따라 키를 잡고 순서를 잡는다. 마치 lfname처럼
# 그러니까 때로는 lambda표현식도 가능함

# lambda표현식

rows_by_fname = sorted(rows, key=lambda r: r['fname'])
rows_by_lname = sorted(rows, key = lambda r: (r['lname'], r['fname'])  )

# ▩1.14 동일한 클래스 객체를 정렬해야하는데, 이 클래스는 기본적인 비교 연산을 제공하지 않는다면??

print('######################################################################')
"""

해결 :  내장함수 sorted는 key인자에 호출 가능 객체를 받아, sorted가 객체 비교에 사용할 수 있는 값을 반환한다.
        ex) 시퀀스 상태의 User인스턴스갖고, User_ID요소를 기반으로 정렬하고 싶다. 
        User인스턴스를 입력으로 받고, user_id를 반환하는 코드 작성하면 됨.
        
"""

class User:
    def __init__(self,user_id):
        self.user_id = user_id
    def __repr__(self):
        return 'User({})'.format(self.user_id)

users = [User(23), User(3), User(99)]  # 시퀀스(리스트) 형태의 인스턴스
print(users)

users_sort = sorted(users, key=lambda u: u.user_id)  # [User(3), User(23), User(99)]
print(users_sort)



#lambda를 쓸지 attrgetter를 쓸지 개인 선호지만, 후자가 더 빠르닥 함. operator.itemgetter() 랑 유사

from operator import attrgetter
class Student(object):
    def __init__(self, id, name, marks):
        self.id = id
        self.name = name
        self.marks = marks

    def __str__(self):
        return '%s 의 학생번호는 %s' % (self.name, self.marks)


students = [Student(0, '경찬', 30), Student(1, '원주', 95), Student(2, '용현', 80)]
order_student = sorted(students, key= attrgetter('id'), reverse = True)  #메모리 영역이 뜸.. 해결아직 못함.

best_student = max(students, key= attrgetter('marks'))
print(order_student)
print (best_student)

# ▩1.15 필드에 따라 레코드 묶기

print('######################################################################')
"""
문제 : 일련의 딕셔너리 or 인스턴스 있고 특정 필드 값에 기반한 Group의 data를 순환하고 싶다..?
해결 :  itertools.groupby() 함수는 이와 같은 데이터를 묶는데 유용하다. 다음과 같은 딕셔너리가 있다고 가정해보자.

"""

rows = [
    {'address': '5412 N CLARK', 'date': '07/01/2012'},
    {'address': '5148 N CLARK', 'date': '07/04/2012'},
    {'address': '5800 E 58TH', 'date': '07/02/2012'},
    {'address': '2122 N CLARK', 'date': '07/03/2012'},
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
    {'address': '1060 W ADDISON', 'date': '07/02/2012'},
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
    {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
]


# 날짜로 구분을 지을 데이터 조각을 순환해야 한다.
# 먼저 원하는 필드에 따라 정랠햐아 하며 ( data 필드),
# 그 후, groupby() 한다.

from operator import itemgetter
from itertools import groupby

#우선 원하는 필드로 정렬한다.

rows.sort(key = itemgetter('date'))

#그룹 내부에서 순환한다.

test = groupby(rows, key = itemgetter('date'))
print(test)  #메모리로 뜸. 대체 그럼 for문에서만 모습을 보이는건가?
for date, items in groupby(rows, key = itemgetter('date')):
    print(date)       #여기에다가 item넣으면 또 메모리로 뜸.
    for i in items:
        print ('   ', i)



# groupby함수는 시퀀스를 검색하고 동일한 값( or 키 함수에서 반한한 value)에 대한 일련의 "실행"을 찾는다?
# 개별 순환에 대해서 값, 그리고 같은 값을 가진 그룹의 모든 아이템을 만드는 이터레이터를 함께 반환한다.
# 그에 앞서 원하는 필드 ( 여기선 date) 에 따라 데이터를 정렬해야 하는 과정이 중요하다.^^
# groupby 함수는 연속된 아이템에만 동작하기 때문에  정렬 과정 생략하면 원하는대로 함수실행 불가

# 단순히 날짜에 따라 데이터를 묶어, 커다란 자료 구조에 넣어 놓고, 원할 때마다 접근하는 거라면,
# 차라리 defaultdict()를 사용하여, multidict구성하는게 나을수도 있음..


from collections import defaultdict
rows_by_date = defaultdict(list)
for row in rows:
    rows_by_date[row['date']].append(row)
print(rows_by_date)   # {'07/01/2012' : [ blah ..], '07/02/2012' : [ blah ..] , ..}

# 위처럼 defaultdict으로 multidict을 구성해 놓으면, 원하는 날짜의 데이터에 다음과 같이 쉽게 접근할 수 있다.
print('###########################################################################')
for r in rows_by_date['07/01/2012']:
    print(r)










# ▩1.16 시퀀스 필터링

print('######################################################################')
"""
문제 : 시퀀스 내부에 데이터가 있고 특정 조건에 따라 값을 추출하거나 줄이고 싶다.
해결 :  가장 간단한 해결책은 list comprehension 이다.

list comprehension 의 일반 표현식

[expression for item1 in iterable1 if condition1
                   for item2 in iterable2 if condition2
                   ...
                   for itemN in iterableN if conditionN]
                   
즉, 간단한 for문이나 if문은 컴프리헨션으로 끝내는게더 효율적이다.
 
 단점은 입력된 내용이 크면 매우 큰 결과가 생성될 수도 있다는 점이다.
 이 부분이 걱정이라면, 생성자 표현식을 사용해서 값을 걸러낼 수 있다.
 
"""


mylist = [1,4,-5,10,-7,2,3,-1]
print([n for n in mylist if n>0])
print([n*2 for n in mylist if n<0]) # 컴프리헨션 연습하기


#생성자 표현식  genexpr

pos = (n for n in mylist if n >0)
print(pos) #generator object <genexpr> at 0x035793C0>
for x in pos:
    print(x)

#만일 필터 조건이 까다로워지면 어떻게 해야할까?
#필터링 코드를 함수 안에 넣고 filter()하면 된다.
#filter의 일반식 filter(function, iteration)
values = ['1','2','-3','-','4','n/a','5']

def is_int(val): #정수값만 출력하는 함수
    try:          #문제가 없다면 ?
        x = int(val)   # x라는 변수에는 int(val)이다.
                       # 근데 얘는 왜 있는걸까
        return True  # True를 반환
    except ValueError:
        return False  #문제가 있으면 False


print(is_int(values[0]))   # '1'  >>   True 를 반환
print(is_int(values[3]))   # '-'  >>   False를 반환
isvals = filter(is_int,values)  # 메모리 형태
# filter는 이터레이터를 생성한다. 따라서 결과의 리스트를 만들고 싶다면 위에 나온대로
# list도 함께 사용해야 한다.

isvals_applied = list(isvals)
print(isvals_applied)


# 리스트 컴프리헨션과 생성자 표현식은 간단한 데이터를 걸러 내기 위한 가장 쉽고 직관적인 방법이다.
# 또한 동시에 데이터 변형 기능도 가지고 있다.
import math
mylist = [1,4,-5,10,-7,2,3,-1]
test2 = [math.sqrt(n) for n in mylist if n >0]
print(test2)


# 새로운 값으로 치환하는 방식 (ex : 양수만 걸르기 , 잘못된 값을 특정 범위에 들어가도록 하기 등..)
clip_neg = [n if n >0 else 0 for n in mylist]   #n>0은 True로 okay며, 그 외에는 모두 0으로 취급해버려라.
print(clip_neg)  #[1, 4, 0, 10, 0, 2, 3, 0]
clip_neg2 = [n if n < 0 else 0 for n in mylist]
print(clip_neg2)  # [0, 0, -5, 0, -7, 0, 0, -1]

# 또 다른 추천하는 필터링 도구   =  itertools.compress()
# 순환가능한 것과 Boolean셀렉터 시퀀스를 입력받는다.

addresses = [
    '5412 N CLARK',
    '5148 N CLARK',
    '5800 E 58TH',
    '2122 N CLARK',
    '5645 N RAVENSWOOD',
    '1060 W ADDISON',
    '4801 N BROADWAY',
    '1039 W GRANVILLE',
]

counts = [0,3,10,4,1,7,6,1]

# 카운트 값이 5 이상인 주소만 남기려 한다면 다음과 같이 하면 된다.

from itertools import compress
more5 = [n>5 for n in counts]
print(more5) # [False, False, True, False, False, True, True, False]
compress_test = []
for i in compress(addresses,more5):
    compress_test.append(i)
print(compress_test)
# compress_test = list(compress(addresses,more5))
print(compress_test)  #more5의 True값만 출력한다.
# 우선주어진 조건에 만족하는지 여부를 담은 Boolean 시퀀스를 만들어 두는 것이 포인트다.
# 그리고 compress함수로 True에 일치하는 값만 골라낸다.
# compress도 이터레이터를 반환한다. 따라서 실행 결과를 리스트에담고 싶음 list를 써야 한다.



# ▩1.17 딕셔너리의 부분 추출

print('######################################################################')
"""
문제 : 딕셔너리의 특정 부분으로부터 다른 딕셔너리를 만들고 싶다.
해결 : 딕셔너리 컴프리헨션을 사용하면 간단하게 해결된다.

"""


prices = {
   'ACME': 45.23,
   'AAPL': 612.78,
   'IBM': 205.55,
   'HPQ': 37.20,
   'FB': 10.75
}

# 가격이 200 이상인 것에 대한 딕셔너리
p200 = {k:v for k,v in prices.items() if v > 200}
print(p200)
# 기술 관련 주식으로 딕셔너리 구성

tech_names = {'AAPL','IBM','HPQ','MSFT'}
p2 = {k:v for k,v in prices.items() if k in tech_names}
print(p2)

#dict comprehension으로 할 수 있는 일은
#튜플 시퀀스 만든 후, dict에 전달 하는것으로도 대체할 수 있다.
#예제
#
# p1 = dict((key,value) for key, value in prices.items() if tech_names > 200 )
# #TypeError: '>' not supported between instances of 'list' and 'int'
# print(p1) 이거 안됨
# 아무튼 아래 대체방법보다 딕셔너리 컴프리헨션이 성능도 좋고 깔끔함

p2 = {key:prices[key] for key in prices.keys() & tech_names}
print(p2)      # 딕셔너리 컴프리헨션보다 1.6배 느리다.




