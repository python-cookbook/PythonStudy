#순환 기술과 기본 이터레이터 프로토콜이 소비되는 방법을 자세히 알아보자.

#델리게이팅 순환
#문제 : 리스트, 튜플 등 순환 가능한 객체를 담은 사용자 정의 컨테이너를 만들었다. 이 컨테이너에 사용 가능한 이터레이터를 만들고 싶다.
#해결 일반적으로 컨테이너 순환에 사용할 __iter__() 메소드만 정의해 주면 된다.
class Node:
    def __init__(self,value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self,node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)

#이 코드에서 __iter__()메소드는 순환 욫ㅇ을 _children 속성으로 전달한다.

#토론
#파이썬의 이터레이터 프로토콜은 __iter__()가 실제 순환을 수행하ㅣ 위한 __next__()메소드를 구현하는 특별 이터레이터 객체르 ㄹ반환하기를 요구한다.
#만약 다른 컨테이너에 들어있는 내용물에 대한 순환이 해야 할 작업의 전부라면, 이터레이터 동작 방식을 완전히 이해할 피요는 없다. 이때는 요청받은 순환을 전달하기만 하면 된다,
#iter()함수에 대한 사용은 코드를 깔끄맣게 하는 지름길과 같다.

