''''''
'''

1장 1절 시퀀스를 개별 변수로 나누기

* 시퀀스 : 데이터들의 집합. 리스트, 튜플, 딕셔너리 등등. 시퀀스는 가변형 시퀀스, 불변형 시퀀스가 있다.
        
        가변형 시퀀스 - list, bytes, bytearray 등
        불변형 시퀀스 - str, tuple, range 등
        
* 시퀀스의 연산 (x는 임의의 객체, s는 시퀀스 객체, i j k l m n 은 정수)
- x in s                  :   s의 한 요소가 x와 같으면 True 
- x not in s              :   s의 한 요소가 x와 같으면 False
- s1 + s2                 :   두 시퀀스를 결합
- s*n 혹은 n*s             :   시퀀스를 n회 반복
- s[i]                    :   시퀀스s의 i번째 요소
- s[i:j]                  :   시퀀스s의 i번째 요소 부터 j-1번째 요소까지 추출
- s[i:j:k]                :   시퀀스s의 i번째 요소 부터 j-1번째 요소까지 k 단위로 추출
- len(s)                  :   시퀀스s내의 요소의 개수
- min(s)                  :   시퀀스s내에서 최소값
- max(s)                  :   시퀀스s내에서 최대값
- s.index(x[, i[, j]])    :   x와 같은 첫 번째 요소의 인덱스
- s.count(x)              :   x와 같은 요소의 개수

* 가변형 시퀀스의 조작
- s[i] = x          :   s의 i번째 요소를 x로 교체
- s[i:j] = t        :    i번째 요소부터 j-1번째 요소를 t(iterable)로 교체
- del s[i:j]        :    i번째 요소부터 j-1번째 요소를 삭제 ( s[i:j] = [] 와 동일)
- s[i:j:k] = t      :    i번째 요소부터 j-1번째 요소(k는 스텝)를 t(iterable)로 교체 (t 와 슬라이싱 된 요소들의 크기가 같아야 한다.)
- del s[i:j:k]      :    i번째 요소부터 j-1번째 요소(k는 스텝)를 삭제
- s.append(x)       :    s의 마지막 요소로 x를 삽입
- s.extend(t)       :    t의 내용물로 s를 확장 ( s[len(s):len(s)]=t 와 동일)
- s.insert(i, x)    :    i 번째에 x를 삽입
- s.pop()           :    마지막 삭제하고 그것을 반환한다.
- s.pop(i)          :    i 번째 요소를 삭제하고 그것을 반환한다.
- s.remove(x)       :    s의 요소 중 x와 같은 첫 번째 것을 제거 (s 안에 x가 없다면 ValueError 예외가 발생한다.)
- s.reverse()       :    요소들을 역순으로 배열한다. (요소의 순서를 역순으로 바꾼다. ( 역순으로 바뀐 객체가 반환되는 것이 아니다.) )
- s.clear()         :    모든 요소 삭제 (del s[:] 과 동일)



* 시퀀스에서의 주의 사항
- 모든 시퀀스는 개별 변수로 나눌 수 있지만 반드시 변수의 개수가 시퀀스에 일치해야만 한다. 그렇지 않을 경우 ValueError 가 발생한다.
    예)

'''

p = (4,5)
x,y,z = p
# Traceback (most recent call last):
# File "K:/Python/PythonStudy/p02_personal_summary/p07_bae_jun_ho/p01_week/p01_tuesday/1.1-1.17.py", line 87, in <module>

'''        
ValueError: not enough values to unpack (expected 3, got 2)
- 같은 형의 나열형 객체끼리는 비교도 가능하다. 특히 리스트와 튜플은 길이와 같은 인덱스를 가지는 모든 요소들끼리 같다면 두 리스트/튜플은 같은 것으로 판별된다.
- 나열형 객체의 복사는 ‘얕은 복사’라는 것도 유의해야 한다. 즉, 중첩된 구조는 복사되지 않는다. (얕은 복사 : 리스트의 중첩 구조는 복사하지 않고 틀만 복사함 아래 예 참조)
    예)
'''
lst=[ [] ]*3
lst
#[[], [], []]
lst[0].append(1)
lst
#[[1], [1], [1]]

'''
- 서로 다른 리스트를 만들고 싶은 경우
    예)
'''

lst = [ [] for _ in range(3)]
lst
#[[], [], []]
lst[0].append(1)
lst[1].append(2)
lst[2].append(3)
lst
#[[1], [2], [3]]


'''
- 만약 ‘깊은 복사’를 수행하려면 copy 모듈의 deepcopy 함수를 이용하면 된다. (깊은 복사 : 구조까지 전부 다 복사해옴. 아래 예 참조)
    예)
'''

x=[11,22]
y=[x, 33]
y
# [[11, 22], 33]

from copy import deepcopy
z = deepcopy(y)
z
#[[11, 22], 33]
x[0]=-44
y
#[[-44, 22], 33] # x가 변하면 y도 변한다.
z
#[[11, 22], 33] # x가 변해도 z는 변함이 없다.

'''
* 언패킹
- 패킹 : 하나의 변수에 여러 값을 넣는 것
  언패킹 : 패킹된 변수에서 여러개의 값을 꺼내 오는 것
   예)
'''

c = (3, 4)
d, e = c    # c의 값을 언패킹하여 d, e에 값을 넣었다
f = d, e    # 변수 d와 e를 f에 패킹


'''

- 이터레이터(iterator)와 제너레이터(generator). 매우매우매우 중요!
    1. 이터레이터 : 반복가능한 객체 (초간단 이해 -> 객체에 .next가 가능하다면 이터레이터가 맞음)
        예) 이터레이터 =  iter(list) : list를 iter로 통하여 이터레이터를 만들었다, list는 반복가능하지만 이터레이터는 아니다.. 
                                       명시적으로 반복가능한객체로 만들어서 사용해줘야한다

        1-1. 이터레이블 : 반복 가능하다 (반복(loop)연산이 가능하여 해당 위치를 이동해가면서 값을 사용할수 있는 지를 말한다)

        1-2. 이터레이션 : 반복가능한객체에서 해당값을 가져오는 행위

        1-3. 이터함수(iter 함수) : list나 dict를 이터레이터로 만들어주는 함수

    2. 제너레이터 : 이터레이터를 만들어주는것을 말한다 (= 반복가능한 객체를 만들어주는 행위)

        2-1. yield : function에서 return과 동일한 역할을 수행한다. 
            -> 해당 function을 yield를 사용하여 제너레이터를 만들어줌(아래 예제 참조)

'''


def generator(n):
    print("get_START")
    i = 0
    while i < n:
        yield i
        print("yield 이후 %d" % i)
        i += 1
    print("get_END")


for i in generator(4):
    print("for_START %d" % i)
    print(i)
    print("for_END %d" % i)


'''
위 코드 실행 결과

get_START # generator 최초생성시점 , # yield 구문 돌입, 여기서부터 while문의 시작

for_START 0 # generator에서 yield로 리턴된 값을 받아서 for문의 시작

0

for_END 0

yield 후 0 # yield후에 잔여코드실행(while문이 아직 이때 i는 0의 상태로 실행되고 있는것), 다돌고난뒤에 while문 한번반복하여 yield를 해준다 값은 1을 리턴

for_START 1 # for loop이 최초한번 돌고 두번째 돌입

1

for_END 1

yield 후 1

for_START 2

2

for_END 2

yield 후 2

for_START 3

3

for_END 3

yield 후 3

get_END #generator 종료

'''



'''

* 언패킹을 할 때 특정 값을 무시하는 법 : 해당 변수의 공간을 _ 로 입력
  예)
'''

data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
_, shares, price, _ = data

# shares
# 50
# price
# 91.1

''' 

1장 2절 임의 순환체의 요소 나누기
 - 순환체에 정해진 요소의 개수 보다 많은 요소를 언패킹 하게 되면 값이 너무 많습니다 라는 예외가 발생한다.
   이 문제를 해결하기 위해 별( * ) 표현식을 사용한다.
   
   * 이 별표 구문은 길이를 알 수 없는 순환체에 매우 효과적으로 사용 할 수 있다. ( 예 - 길이가 일정하지 않은 튜플 )
   
   예)
'''

def drop_first_last(grades):
    first, *middle, last = grades
    return avg(middle)

record = ('Dave', 'dave@example,com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = user_record

*trailing_qtrs, current_qtr = sales_record
trailing_avg = sum(trailing_qtrs)/len(trailing_qtrs)
return avg_comparison(trailing_avg, current_qtr)

*trailing, current = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
trailing    # *trailing과 current 순으로 요소가 담기므로 마지막 current의 자리인 마지막 1을 빼고 나머지가 전부 trailing에 담긴다
current     # current엔 딱 한자리인 1만 담긴다

records = [
    ('foo', 1, 2),
    ('bar', 'hello'),
    ('foo', 3, 4),
]

def do_foo(x, y):
    print('foo', x, y)

def do_bar(s):
    print('bar', s)

for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)