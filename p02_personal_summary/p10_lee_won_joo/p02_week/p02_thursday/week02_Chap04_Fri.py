"""
                                                ▶ 4.1 수동으로 이터레이터 소비◀ 
♣  문제 :  순환 가능한아이템에 접근할 때 for 순환문을 사용하고 싶지 않다면?
        
↘  해결 : 수동으로 이터레이터를 소비하려면 next() 함수를 사용하고 StopIteration예외를 처리하기 위한
           코드를 직접 작성한다. 



 """

print('###############################################################################')
print('########################################## 4.1 수동으로 이터레이터 소비#####################################')
print('###############################################################################')


#파일의 줄을 읽어오는 코드를 예로 들어보자

with open('d:/data/emp2.csv') as f:
    try:
        while True:
            line = next(f)
            print(line, end='')
    except StopIteration:
        print('다 소비했습니다.')
        pass


# 일반적으로 Stopiteration 은 순환의 끝을 알리는데 사용한다.
# 하지만 next() 를 수동으로 사용한다면 None과 같은 종료 값을 반환하는데 사용할 수도 있다.


with open('d:/data/emp2.csv') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
        print(line, end='')

# 대개의 경우, 순환 for문을 사용하지만 보다 더 정교한 조절이 필요할 때도 있다.
# 기저에서 어떤 동작이 일어나는지 정확히 알아둘 필요가 있다.
# 다음 상호작용을 하는 예제를 통해 순환하는 동안 기본적으로 어떤 일이 일어나는지 보자.

itmes = [1,2,3]
# 이터레이터 열기
it = iter(itmes)        # items.__iter__()실행
# 이터레이터 실행
print(next(it))               #it.__next__()실행      1
print(next(it))               #it.__next__()실행      2
print(next(it))               #it.__next__()실행      3
# print(next(it))               #Error StopIteration

#다음 장에서는 순환 기술과, 기본 이터레이터 프로토콜이 소비되는 방법을 자세히 알아본다









"""
                                                ▶ 4.2 델리게이팅 순환◀ 
♣  문제 :  리스트, 튜플 등 순환 가능한 객체를 담은 사용자 정의 컨테이너를 만들었다. 
            이 컨테이너 안에 사용 가능한 이터레이터를 만들고 싶다.

↘  해결 :  일반적으로 컨테이너 순환에 사용할 __iter__() 메소드만 정의해주면 된다. 
            


 """

print('###############################################################################')
print('########################################## 4.2 델리게이팅 순환#####################################')
print('###############################################################################')



class Node:
    def __init__(self,value):
        self.value = value
        self._children = []
    def __repr__(self):
        return 'Node({!r})'.format(self.value)
    def add_child(self,node):
        print('리스트에 추가합니다.')
        self._children.append(node)
    def __iter__(self):
        return iter(self._children)

if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(root)
    child1.add_child((child2))
    # for ch in root:
    #     print(ch)
    for ch in child1:
        print(ch)
#
# 파이썬의 이터레이터 프로토콜은 __iter__() 가 실제 순환을 수행하기 위한 __next__() 메소드를
# 구현하는 특별 이터레이터 객체를 반환하기를 요구한다.
# 만일 다른 컨테이너에 들어있는 내용물에 대한 순환이 해야할 작업의 전부라면이터레이터 동작 방식을 완전 이해할 필요는 없다/
# iter() 함수에 대한 사용은 코드를 깔끔하게 하는 지름길과 같다.
# iter(s)는 단순히 s.__iter__()를 호출해서 이터레이터를 반환하는데, 이는 len(s)가 s.__len__()을 호출하는 것과 같은 방식이다.
# 아주효율적이라는거..?











"""
                                                ▶ 4.3 제너레이터로 새로운 순환 패턴 생성◀ 
♣  문제 :  내장함수 ( range(),  reversed()  ) 와는 다른 동작을 하는 순환 패턴을 만들고 싶다.
            새로운 순환 패턴을 만들고 싶다면,, 제너레이터 함수를 사용해서 정의해야 한다.
            특정 범위의 부동 소수점 숫자를 만드는 제너레이터 코드르 보라.

↘  해결 :   



 """

print('###############################################################################')
print('########################################## 4.3제너레이터로 새로운 순환 패터 생성#####################################')
print('###############################################################################')

# 특정 범위의 부동 소수점 숫자 만드는 제너레이터 코드
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

#위와 같은 함수를 사용하려면, for 순환문이나 순환 객체를 소비하는 다른 함수 등을 사용한 순환을 해야 한다.

for n in frange(0,4,0.5):
    print(n)

print(list(frange(0, 1, 0.125)))    #[0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]

#내부의 yield 문의 존재로 인해 함수가 제너레이터가 되었다.
# 일반 함수와는 다르게 제너레이터는 순환에 응답하기 위해 실행 된다.
# 이런 함수가 어떻게 동작하는지 다음 예를 본다.


def countdown(n):
    print('Starting to count from', n)
    while n > 0:
        yield n
        n -= 1
    print('Done!')

c = countdown(3)
print(c)   #<generator object countdown at 0x02EB81E0>

print(next(c))
print(next(c))
print(next(c))

# 중요한 점은 제너레이터 함수가 순환에 의한 [다음] 연산에 응답하기 위해서만 된다는 점이다.
# 제너레이터 함수가 반환되면 순환을 종료한다.
# 하지만, 일반적으로 순환에 사용하는 for 문이 상세 내역을 책임지기 때문에
# 우리가 직접적으로 신경쓰지 않아도 된다.






"""
                                                ▶ 4.4 이터레이터 프로토콜 구현◀ 
♣  문제 :  순환을 지원하는 객체를 만드는데,이터레이터 프로토콜을 구현하는 쉬운 방법이 필요하다.

↘  해결 :  객체에 대한 순환을 가장 쉽게 구현하는 방법은 제너레이터 함수를 사용하는 것이다.
          레시피 4.2에선 트리 구조를 표현하기 위해 Node클래스를 사용했다.
          노드를 [깊이 - 우선] 패턴으로 순환하는 이터레이터를 구현하고 싶다면 다음과 같이 한다.

   토론 : 

 """

print('###############################################################################')
print('########################################## 4.4 이터레이터 프로토콜 구현#####################################')
print('###############################################################################')

#depth-first pattern iterator


class Node:
    def __init__(self,value):
        self.value = value
        self._children = []
    def __repr__(self):
        return 'Node({!r})'.format(self.value)
    def add_child(self,node):
        print('리스트에 추가합니다.')
        self._children.append(node)
    def __iter__(self):
        return iter(self._children)
    def depth_first(self):
        yield self  #처음에는 자신을 만들고
        for c in self:  #그 후 자식을 순환한다.
            yield from c.depth_first() #이때 그 자식은 depth_first() 메소드로 아이템을 만든다.



if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child1.add_child(Node(5))
    for ch in root.depth_first():
        print(ch)




# 토론 파이썬의 이터레이터 프로토콜은 __iter__()가
# __next()__() 메소드를 구현하고 종료를 알리기 위해 StopIteration 예외를 사용하는 특별 이터레이터 객체를반환하기를 요구한다.
# 하지만 이런 객체를 깔끔하게 구현하기가 쉽지 않다. 예를 들어 , 다음 코드는 관련 이터레이터 클래스를 사용한 depth_first() 메소드와
# 대안 구현법을 보여준다.

#'더 깔끔해진 코드'
class Node:
    def __init__(self,value):
        self._value = value
        self._children = []
    def __repr__(self):
        return 'Node({!r})'.format(self._value)
    def add_child(self,other_node):
        print('리스트에 추가합니다.')
        self._children.append(other_node)
    def __iter__(self):
        return iter(self._children)
    def depth_first(self):
        return DepthFirstIterator(self)
class DepthFirstIterator(object):
    '''
    Depth-first traversal
    '''
    def __init__(self,start_nod):
        self._node = start_nod
        self._children_iter = None
        self._child_iter = None
    def __iter__(self):
        return self
    def __next__(self):
        # 막 시작했다면 자신을 반환한다. 자식에 대해서 이터레이터를 생성한다.
        if self._children_iter is None:
            self._children_iter = iter(self._node)
            return self._node
        # 자식을 처리 중이라면 다음 아이템을 반환한다.
        elif self._child_iter:
            try:
                nextchild = next(self._child_iter)
                return nextchild
            except StopIteration:
                self._child_iter = None
                return next(self)
        # 다음 자식으로 진행하고 순환을 시작한다.
        else:
            self._child_iter = next(self._children_iter).depth_first()
            return next(self)


if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child1.add_child(Node(5))
    for ch in root.depth_first():
        print(ch)


"""
                                                ▶ 4.5 역방향 순환◀ 
♣  문제 :  시퀀스 아이템을 역방향으로 순환하고 싶다.

↘  해결 :  내장 함수 reversed() 를 사용한다.
          
          역방향 순환은 객체가 __reversed__() 특별 메소드를 구현하고 있거나 크기를 알 수 있는 경우에만 가능하다.
          두 조건 중에서 아무것도 만족하지 못하면 객체를 먼저 리스트로 변환해야 한다.

   토론 : 

 """

print('###############################################################################')
print('########################################## 4.5 역방향 순환#####################################')
print('###############################################################################')


r = [i for i in reversed(range(0,5))]
print(r)

f = open('d:/data/emp2.csv')
rever_text = [line for line in reversed(list(f))]
print(rever_text)


#하지만 순환 가능 객체를 리스트로 변환할 때 많은 메모리가 필요하다는 점은 주의해야 한다.

#__reversed__() 메소드를 구현하면 사용자 정의 클래스에서 역방향 순환이 가능하다는 점을 많은 프로그래머들이 모르고 있다.

class Countdown:
    def __init__(self,start):
        self.start = start
        # print(self.start) #5가 들어갔다.
    #순방향 순환
    def __iter__(self):
        n = self.start

        while n>0:
            yield n
            n -=1
    #역방향 순환
    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n +=1
            # print(n)

a = Countdown(5).__iter__()
for i in a:
    print(i)

# 역방향 이터레이터를 정의하면 코드를 훨씬 효율적으로 만들어 주고, 데이터를 리스트로 변환하고 순환하는 수고를 덜어준다.






"""
                                                ▶ 4.6 추가 상태를 가진 제너레이터 함수 정의◀ 
♣  문제 :  제너레이터 함수를 정의하고 싶지만, 사용자에게 노출할 추가적인 상태를 넣고 싶다.

↘  해결 :  사용자에게 추가 상태를 노출하는 제너레이터를 원할 때, __iter__() 메소드에 제너레이터 함수 코드를 넣어서 쉽게 클래스로
            구현할수 있다는 점을 기억하자.

   토론 : 

 """

print('###############################################################################')
print('########################################## 4.6 추가 상태를 가진 제너레이터 함수 정의#####################################')
print('###############################################################################')


from collections import deque

class linehistory:
    def __init__(self,lines,histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)
    def __iter__(self):
        for lineno, line in enumerate(self.lines,1):
            self.history.append((lineno, line))
            yield line
    def clear(self):
        self.history.clear()

# 이 클래스를 사용하려면 일반 제너레이터 함수처럼 대해야 한다.
# 하지만 인스턴스를 만들기 때문에 history 속성이나 clear() 메소드 같은 내부 속성에 접근할 수 있다.

with open('d:/data/emp2.csv') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')


#제너레이터를 사용하면 모든 작업을 함수만으로 하려는 유혹에 빠지기 쉽다. 만약 제너레이터 함수가 프로그램의 다른 부분과 일반적이지 않게
#상호작용해야 할 경우 코드가 꽤 복잡해질 수 있다.
# 이럴때는 앞에서 본 대로 클래스 정의만을 사용한다.
# 제너레이터를 __iter__() 메소드에 정의한다고 해도 알고리즘을 작성하는 방식에는 아무런 변화가 없다.
# 클래스의 일부라는 점으로 인해 사용자에게 속성과 메소드를 쉽게 제공할 수 있다.
#for 문 대신 다른 기술을 사용해서 순환한다면 iter() 호출할 때 추가적으로 작업을 해야 할 필요가 생기기도 한다.

f = open('d:/data/emp2.csv')
lines = linehistory(f)
# next(lines)  #TypeError: 'linehistory' object is not an iterator

# iter() 를 먼저 호출하고, 순환을 시작한다.
it = iter(lines)
print(next(it))
print(next(it))
print(next(it))
print(next(it))
print(next(it))
print(next(it))  #StopIteration



