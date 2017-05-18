#########1.1 시퀀스를 개별변수로 나누기
p =( 4,5 )
x , y = p   #거꾸로 하면 안됨
print(x)    #4
print(y)    #5
print( x, y)    # 4 5

data = [ 'ABC' , 50, 91.1, (2012,12,21)]
name , shares, price, (year, mon, day) = data
print(year)


c= (3,4)
d,e = c
f = d, e
print(c,f) # (3, 4) (3, 4)

s = 'Hello'
a,b,c,d,e= s
print(s)


shares = a
data = [ 'ABC' , 50, 91.1, (2012,12,21)]
_, shares, price,_ = data
print(shares)

#########1.2 임의 순환체의 요소 나누기
def drop_first_last(grades):
	first, *middle, last = grades
	return avg(middle)

record = ('dave', 'dave@email.com','777-777','746-555-1212','12')
name, email, *phone_numbers, num = record
print(name)
print(email)
print(phone_numbers) #['777-777', '746-555-1212']


*trailing_qrts, current_qtr = sales_record
trailing_avg = sum(trailing_qrts) / len(trailing_qtrs)
return avg_comparison(trailing_avg, current_qtr)

*trailing, current = [ 10,8,7,1,9,5,10,3]
print(trailing)
print(current)

records = [ ('foo',1,2), ('bar','hello'), ('foo',3,4)]
def do_foo(x,y):
	print('foo',x,y)

def do_bar(s):
	print('bar',s)

for tag , *args in records:
	if tag == 'foo':
		do_foo(*args)
	elif tag == 'bar':
		do_bar(*args)

line = 'nobody:*-2:-2:Unprivileged Users:/misoni/virtualEnvironment:/bin/python'
uname, *fields, homedir,sh = line.split(':')
print(uname) #nobody
print(fields) #['*-2', '-2', 'Unprivileged Users']
print(homedir)
print(sh)

record = ('AMIE',50, 123.45, (12,18,2012))
name, *_, (*_,year) =record
print(name)
print(year)

items = [1,10,7,4,5,9]
def sum(items):
	head, *tail = items  # head: 1 tail:[10,7,4,5,9]
	return head + sum(tail) if tail else head
print( sum(items) )


#########1.3 마지막 N개 아이템 유지
from collections import deque
def search(lines, pattern, history = 5 ):
	previous_lines = deque(maxlen=history)
	for line in line:
		yield line, previous_lines
	previous_lines.append(line)

#파일 사용 예
if __name__ == '__main__':
	with open('somefile.txt') as f:
		for line, prevlines in search(f, 'python', 5):
			for pline in prevlines:
				print(pline, end='')
			print(line,end='')
			print('-'*20)

q = deque(maxlen=3)
q.append(1)
q.append(2)
q.append(3)
print(q)  #deque([1, 2, 3], maxlen=3)

q.append(4)
print(q) #deque([2, 3, 4], maxlen=3)
q.append(5)
print(q) #deque([3, 4, 5], maxlen=3)

from collections import deque
q=deque()
q.append(1)
q.append(2)
q.append(3)
print(q) #>>>>deque([1, 2, 3])

q.appendleft(4)
print(q) # >>>deque([4, 1, 2, 3])
q.pop()
print(q) #>>>deque([4, 1, 2 ]) 맨 끝에꺼 삭제
q.popleft()
print(q) #>>>deque([1, 2]) 맨 오른쪽 삭제

#########1.4 N아이템의 최대 혹은 최소값 찾기
import heapq
nums = [ 1,8,2,23,7,-4,18,23,42,37,2]
print(heapq.nlargest(3,nums)) #>>>[42, 37, 23] 큰 순서대로 나옴
print(heapq.nsmallest(3,nums)) #>>>[-4, 1, 2] 작은 순서대로 나옴

portfolio = [
	{'name': 'IBM', 'shares':100, 'price':91.1},
	{'name':'AAPL','shares':5, 'price':543.22},
	{'name':'FB','shares':200,'price':21.09},
	{'name':'HPQ','shares':35,'price':31.75},
	{'name':'YHOO', 'shares':45, 'price':16.35},
	{'name':'ACME','shares':75, 'price':115.65}
]

cheap = heapq.nsmallest(3,portfolio, key= lambda s: s['price'])
print (cheap)#[{'name': 'YHOO', 'shares': 45, 'price': 16.35}, {'name': 'FB', 'shares': 200, 'price': 21.09}, {'name': 'HPQ', 'shares': 35, 'price': 31.75}]
expensive = heapq.nlargest(3,portfolio, key= lambda s: s['price'])
print(expensive) #[{'name': 'AAPL', 'shares': 5, 'price': 543.22}, {'name': 'ACME', 'shares': 75, 'price': 115.65}, {'name': 'IBM', 'shares': 100, 'price': 91.1}]

nums = [ 1,8,2,23,7,-4,18,23,42,37,2]
import heapq
heap = list(nums) #원래 리스트인데 왜 리스트로 바꿈?
heapq.heapify(heap)
print(heap) #>>>[-4, 2, 1, 23, 7, 2, 18, 23, 42, 37, 8]

print( heapq.heappop(heap)) #>>> -4  0번째요소 뽑아주고 그 요소를 삭제해주는 듯
print( heapq.heappop(heap)) ##>>> 1
print( heapa.heappop(heap) ) ##>>> 2

#########1.5 우선 순위 큐 구현
import heapq
class PriorityQueue:
	def __init__(self):
		self._queue =[]
		self._index = 0

	def push(self, item, priority):
		heapq.heappush(self._queue, (-priority, self._index, item))
		self._index += 1

	def pop(self):
		return heapq.heappop(self._queue)[-1]

class Item:
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return 'Item({!r})'.foramt(self.name)

q =PriorityQueue()
q.push(Item('foo'),1)
q.push(Item('bar'),5)
q.push(Item('spam'),4)
q.push(Item('grok'),1)
q.pop()
q.pop()
q.pop()


a= Item('foo')
b= Item('bar') #

a = (1,Item('foo'))
b = (5,Item('bar'))
a < b
c = (1, Item('grok'))
#a < c

a = (1,0,Item('foo'))
b = (5,1,Item('bar'))
c = (1,2,Item('grok'))
print( a < b) #>>> True
print( a < c) #>>> True

#########1.6 딕셔너리의 키를 여러 값에 매핑하기
d = { 'a' : [1,2,3],
	  'b' : [4,5]
}

e = { 'a' : {1,2,3},
	  'b' : {4,5}
}

from collections import defaultdict

d= defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)
print(d) # >>> defaultdict(<class 'list'>, {'a': [1, 2], 'b': [4]})

d = defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['b'].add(4)
print(d) # >>> defaultdict(<class 'set'>, {'a': {1, 2}, 'b': {4}})

d = {} #일반 딕셔너리
d.setdefault('a',[]).append(1)
d.setdefault('a',[]).append(2)
d.setdefault('b',{}).add(4)

print(d)

d = {}
for key, value in pairs:
	if key not in d:
		d[key] = []
	d[key].append(value)

d = defaultdict(list)
for key, value in pairs:
	d[key].append(value)

#########1.7 딕셔너리 순서 유지
from collections import OrderedDict
d = OrderedDict()
d['foo'] =1
d['bar']= 2
d['spam'] = 3
d['grok'] = 4
print(d) #OrderedDict([('foo', 1), ('bar', 2), ('spam', 3), ('grok', 4)])
print(type(d)) #<class 'collections.OrderedDict'>
for key in d:
	print(key, d[key])

# foo 1
# bar 2
# spam 3
# grok 4


d = {}
d['foo'] =1
d['bar']= 2
d['spam'] = 3
d['grok'] = 4
print(d) #{'foo': 1, 'bar': 2, 'spam': 3, 'grok': 4}

import json
print( json.dumps(d)) #{"foo": 1, "bar": 2, "spam": 3, "grok": 4}

#########1.8 딕셔너리 계산
prices = {
	'ACME' : 45.23,
	'AAPL' : 612.78,
	'IBM' : 205.55,
	'HPQ' : 37.20,
	'FB' : 10.75
}

min_price = min( zip(prices.values(), prices.keys())) #>>> (10.75, 'FB')
max_price = max( zip(prices.values(), prices.keys())) #>>> (10.75, 'FB')

#a = zip(prices.values(), prices.keys()) # >>> <zip object at 0x10521b708>

prices_sorted = sorted(zip(prices.values(), prices.keys()))
print(prices_sorted)
#>>> [(10.75, 'FB'), (37.2, 'HPQ'), (45.23, 'ACME'), (205.55, 'IBM'), (612.78, 'AAPL')]

prices_and_names = zip(prices.values(), prices.keys())
print(min(prices_and_names))
#print(max(prices_and_names))

print( min(prices) ) #AAPL
print( max(prices) ) #IBM

print( min(prices.values()) ) #10.75
print( max(prices.values()) ) #612.78

min(prices, key= lambda k: prices[k] ) #>>>FB
max(prices, key= lambda k: prices[k] ) #>>>AAPL
min_values = prices[ min(prices, key=lambda k:prices[k])] #>>>10.75

prices = {'AAA' : 45.23, 'ZZZ': 45.23}
min(zip(prices.values(), prices.keys()))
max(zip(prices.values(), prices.keys()))

print(min(zip(prices.values(), prices.keys()))) #>>> (45.23, 'AAA')
print(max(zip(prices.values(), prices.keys()))) #>>> (45.23, 'ZZZ') 읭? 이거는 한번만 소비안됨??

#########1.9 두 딕셔너리의 유사점 찾기
a = { 'x': 1,  'y' : 2 , 'z':3}
b = { 'w': 10, 'x': 11,  'y':2}

a.keys() & b.keys()  #>>>{'x', 'y'}
print( a.keys() - b.keys()) #{'z'}
print( a.items() & b.items()) #{('y', 2)}

c= {key:a[key] for key in a.keys() - {'z','w'}}
print(c) #>>> {'x': 1, 'y': 2}

#########1.10 순서를 깨지 않고 시퀀스의 중복 없애기

def dedupe(items):
	seen = set()
	for item in items:
		if item not in seen:
			yield item
			seen.add(item)

a = [ 1,5,2,1,9,1,5,10]
print( list(dedupe(a)) ) #리스트화는 왜해주는겨

def dedupe(items, key= None):
	seen =set()
	for item in items:
		val = item if key is None else key(item)
		if val not in seen:
			yield item
			seen.add(val)

a = [ {'x':1, 'y':2} ,  {'x':1, 'y':3} , {'x':1, 'y':2} , {'x':2, 'y':4}]
list(dedupe( a, key = lambda d: (d['x'],d['y'])))

list(dedupe( a, key= lambda d: d['x']))

a = [1,5,2,1,9,1,5,10]
print ( set(a) )

with open(somefile,'r') as f:
	for line in dedupe(f):
		...

#########1.11 슬라이드 이름 붙이기
##### '012345678901234567890123456789012345678901234567890123456789'
record = '.....................100       .......513.25    ..........'
SHARES = slice(20,32)
PRICE = slice(40,48)

cost = int(record[SHARES]) * float(record[price])

items = [0,1,2,3,4,5,6]
a= slice(2,4)	# print(a) >>> slice(2, 4, None)
items[2:4]		#print(items[2:4]) >> 	[2,3]
items[a]		#print(items[a]) >> [2,3]
items[a] = [10,11]
items			#print(items) >>> [0,1,10,11,4,5,6]
del items[a]
items			#[0,1,4,5,6]

a = slice(10,50,2)
a.start
a.stop
a.step

s = 'Helloworld'
a.indices(len(s))
#########1.12 시퀀스에 가장 많은 아이템 찾기
words = [ 'look', 'into','my', 'eyes' , 'look', 'into','my', 'eyes',
		 'the','eyes','the','eyes','the','eyes','not','around','the',
		 'eyes','dont', 'look','around','the','eyes','look','into',
		 'my','eyes',"your're",'under' ]

from collections import Counter
word_counts = Counter(words)
top_three =word_counts.most_common(3)
print(top_three) #>>>[('eyes', 8), ('the', 5), ('look', 4)]

word_counts['not'] #>>> 1
word_counts['eyes'] # >>> 8
print(word_counts)

morewords = ['why','are','you','not','looking','in','my', 'eyes']
for word in morewords:
	word_counts[word] += 1
	print(word_counts)
word_counts['eyes']

a = Counter(words)
#>>>Counter({'eyes': 8, 'the': 5, 'look': 4, 'into': 3, 'my': 3, 'around': 2, 'not': 1, 'dont': 1, "your're": 1, 'under': 1})
b= Counter(morewords)
#>>>Counter({'why': 1, 'are': 1, 'you': 1, 'not': 1, 'looking': 1, 'in': 1, 'my': 1, 'eyes': 1})
print(a)
print(b)
#카운트 합치기
c = a+b
#>>> Counter({'eyes': 9, 'the': 5, 'look': 4, 'my': 4, 'into': 3, 'not': 2, 'around': 2, 'dont': 1, "your're": 1, 'under': 1, 'why': 1, 'are': 1, 'you': 1, 'looking': 1, 'in': 1})


#########1.13 일반 키로 딕셔너리 리스트 정렬
rows = [
	{'fname':'Brian','lname':'Jones','uid':1003},
	{'fname':'David','lname':'Beazley','uid':1002},
	{'fname':'John','lname':'Cleese','uid':1001},
	{'fname':'Big','lname':'Jones','uid':1004}
]

from operator import itemgetter

rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid =sorted(rows, key=itemgetter('uid'))

print(rows_by_fname) #[{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, {'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}]
print(rows_by_uid) ##[{'fname': 'John', 'lname': 'Cleese', 'uid': 1001}, {'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}]


rows_by_lfname = sorted(rows, key=itemgetter('lname','fname'))
print(rows_by_lfname)

#
# [{'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
#  {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
#  {'fname': 'Big', 'lname': 'Jones', 'uid': 1004},
#  {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}]

rows_by_fname = sorted(rows, key= lambda r: r['fname'])
rows_by_lfname = sorted(rows, key= lambda r: ( r['lname'] , r['fname']))


#########1.14 기본 비교 기능 없이 객체 정렬
class User:
	def __init__(self, user_id):
		self.user_id = user_id
	def __repr__(self):
		return 'User({})'.format(self.user_id)

users = [User(23), User(3),User(99)]
users # >>> [User(23), User(3), User(99)]


sorted(users, key=lambda u : u.user_id) #이건 프린트 안해도 걍 나오네 [User(3), User(23), User(99)]

by_name = sorted(users, key=attrgetter('last_name','first_name'))

min(users, key= attrgetter('user_id')) #User(3)
max(users, key= attrgetter('user_id')) #User(99) 실행안대유ㅠㅠㅠ

#########1.15 필드에 따라 레코드 묶기
rows = [
	{'address': '5412 N CLARK' , 'date' : '07/01/2012'},
	{'address': '5148 N CLARK' , 'date' : '07/04/2012'},
	{'address': '5800 E 58TH' , 'date' : '07/02/2012'},
	{'address': '2122 N CLARK' , 'date' : '07/03/2012'},
	{'address': '5645 N RAVENSWOOD' , 'date' : '07/02/2012'},
	{'address': '1060 N ADDISON' , 'date' : '07/02/2012'},
	{'address': '4801 N BROADWAY' , 'date' : '07/01/2012'},
	{'address': '1039 W GRANVILLE' , 'date' : '07/04/2012'},
]

from operator import itemgetter
from itertools import groupby

#원하는 필드로 정렬
rows.sort(key=itemgetter('date'))

#그룹 내부에서 순환
for date, items in groupby(rows, key= itemgetter('date')):
	print(date)
	for i in items:
		print ('    ',i)


# 07/01/2012
#      {'address': '5412 N CLARK', 'date': '07/01/2012'}
#      {'address': '4801 N BROADWAY', 'date': '07/01/2012'}
# 07/02/2012
#      {'address': '5800 E 58TH', 'date': '07/02/2012'}
#      {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'}
#      {'address': '1060 N ADDISON', 'date': '07/02/2012'}
# 07/03/2012
#      {'address': '2122 N CLARK', 'date': '07/03/2012'}
# 07/04/2012
#      {'address': '5148 N CLARK', 'date': '07/04/2012'}
#      {'address': '1039 W GRANVILLE', 'date': '07/04/2012'}

from collections import defaultdict
rows_by_date = defaultdict(list)
for row in rows:
	rows_by_date[row['date']].append(row)
	print(rows_by_date)

#defaultdict(<class 'list'>, {'07/01/2012': [{'address': '5412 N CLARK', 'date': '07/01/2012'}, {'address': '4801 N BROADWAY', 'date': '07/01/2012'}], '07/02/2012': [{'address': '5800 E 58TH', 'date': '07/02/2012'}, {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'}, {'address': '1060 N ADDISON', 'date': '07/02/2012'}], '07/03/2012': [{'address': '2122 N CLARK', 'date': '07/03/2012'}], '07/04/2012': [{'address': '5148 N CLARK', 'date': '07/04/2012'}, {'address': '1039 W GRANVILLE', 'date': '07/04/2012'}]})

for r in rows_by_date['07/01/2012']:
	print(r)

#########1.16 시퀀스 필터링
mylist = [ 1,4,-5,10,-7,2,3,-1]
[n for n in mylist if n > 0]  #>>> [1, 4, 10, 2, 3]
[n for n in mylist if n <0] #>>>[-5,-7,-1]

pos = ( n for n in mylist if n > 0)
pos
for x in pos:
	print(x)

values = ['1','2','-3','-','4','N/A','5']
def is_int(val):
	try:
		x = int(val)
		return True
	except ValueError:
		return False

ivals = list(filter(is_int,values))
print(ivals) #['1', '2', '-3', '4', '5']

mylist = [1,4,5,10,-7,2,3,-1]
import math
[math.sqrt(n) for n in mylist if n>0]
#[1.0, 2.0, 2.23606797749979, 3.1622776601683795, 1.4142135623730951, 1.7320508075688772]

clip_neg = [ n if n > 0 else 0 for n in mylist]
clip_neg #>>>[1, 4, 5, 10, 0, 2, 3, 0]
clip_pos = [n if n < 0 else 0 for n in mylist]
clip_pos #>>>[0, 0, 0, 0, -7, 0, 0, -1]

addresses = [
	'5412 N CLARK',
	'5148 N CLARK',
	'5800 E 58TH',
	'2122 N CLARK',
	'5645 N RAVENSWOOD',
	'1060 W ADDISON',
	'4801 N BROADWAY',
	'1039 W GRANVILLE'
]
counts = [0,3,10,4,1,7,6,1]

from itertools import compress
more5 = [n > 5 for n in counts]
print( more5) #[False, False, True, False, False, True, True, False]
print( list(compress(addresses, more5)) ) #['5800 E 58TH', '1060 W ADDISON', '4801 N BROADWAY']

#########1.17 딕셔너리의 부분 추출
prices = {
	'ACME' : 45.23,
	'AAPL' : 612.78,
	'IBM' : 205.55,
	'HPQ' : 37.20,
	'FB' : 10.75
}

#가격이 200이상인 것에 대한 딕셔너리
p1 = {key: value for key, value in prices.items() if value > 200}
print(p1) #{'AAPL': 612.78, 'IBM': 205.55}
#기술 관련 주식으로 딕셔너리 구성
tech_names = {'AAPL','IBM','HPQ','MSFT'}
p2 = {key: value for key, value in prices.items() if key in tech_names}
print(p2) #{'AAPL': 612.78, 'IBM': 205.55, 'HPQ': 37.2}

p1 = dict((key,value) for key, value in prices.items() if value > 200 )
print(p1) #{'AAPL': 612.78, 'IBM': 205.55}

tech_names = {'AAPL','IBM','HPQ','MSFT'}
p2 = {key : prices[key] for key in prices.keys() & tech_names}