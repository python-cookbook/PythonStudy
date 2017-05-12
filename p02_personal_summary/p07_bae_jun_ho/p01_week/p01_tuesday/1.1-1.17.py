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
        # p = (4,5)
        # x,y,z = p
        
        Traceback (most recent call last):
        File "K:/Python/PythonStudy/p02_personal_summary/p07_bae_jun_ho/p01_week/p01_tuesday/1.1-1.17.py", line 87, in <module>
        x,y,z = p
        
ValueError: not enough values to unpack (expected 3, got 2)
- 같은 형의 나열형 객체끼리는 비교도 가능하다. 특히 리스트와 튜플은 길이와 같은 인덱스를 가지는 모든 요소들끼리 같다면 두 리스트/튜플은 같은 것으로 판별된다.
- 나열형 객체의 복사는 ‘얕은 복사’라는 것도 유의해야 한다. 즉, 중첩된 구조는 복사되지 않는다. (얕은 복사 : 리스트의 중첩 구조는 복사하지 않고 틀만 복사함 아래 예 참조)
    예)
        # >>> lst=[ [] ]*3
        # >>> lst
        # [[], [], []]
        # >>> lst[0].append(1)
        # >>> lst
        # [[1], [1], [1]]

- 서로 다른 리스트를 만들고 싶은 경우
    예)
        # lst = [ [] for _ in range(3)]
        # >>> lst
        # [[], [], []]
        # >>> lst[0].append(1)
        # >>> lst[1].append(2)
        # >>> lst[2].append(3)
        # >>> lst
        # [[1], [2], [3]]

- 만약 ‘깊은 복사’를 수행하려면 copy 모듈의 deepcopy 함수를 이용하면 된다. (깊은 복사 : 구조까지 전부 다 복사해옴. 아래 예 참조)
    예)
        # >>> x=[11,22]
        # >>> y=[x, 33]
        # >>> y
        # [[11, 22], 33]
        # >>> from copy import deepcopy
        # >>> z = deepcopy(y)
        # >>> z
        # [[11, 22], 33]
        # >>> x[0]=-44
        # >>> y
        # [[-44, 22], 33] # x가 변하면 y도 변한다.
        # >>> z
        # [[11, 22], 33] # x가 변해도 z는 변함이 없다.

* 언패킹
- 이터레이터(iterator)와 제너레이터(generator). 매우매우매우 중요!
    1. 이터레이터 : 반복가능한 객체 (초간단 이해 -> 객체에 .next가 가능하다면 이터레이터가 맞음)
        예) 이터레이터 =  iter(list) : list를 iter로 통하여 이터레이터를 만들었다, list는 반복가능하지만 이터레이터는 아니다.. 
                                     명시적으로 반복가능한객체로 만들어서 사용해줘야한다

        1-1. 이터레이블 : 반복 가능하다 (반복(loop)연산이 가능하여 해당 위치를 이동해가면서 값을 사용할수 있는 지를 말한다)
        예) a라는 dict를 생성하여 class를 확인하면 a는 dict일뿐 이터레이터가 아니다
            # a = {1:'a',2:'b'}
            # print(a.__class__)
            <class 'dict'>

'''

a = {1:'a',2:'b'}
print(a.__class__)

b = iter(a)
print(b.__class__)

