#문제
#순환을 지원하는 객체를 만드는데, 이터레이터 프로토콜을 구현하는 쉬운 방법이 필요하다.
#해결
#객체에 대한 순환을 가장 쉽게 구현하는 방법은 제너레이터 함수를 사용하는 것.
#4.2에서 트리구조를 표현하기 위해 Node클래스를 사용했다. 노드를 깊이-우선 패턴으로 순환하는 이터레이터를 구현하고 싶다면 다음 코드를 참조한다.
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()

if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))
    for ch in root:
        print(ch)

#이 코드에서 depth_first() 메소드는 직관적으로 읽고 이해할 수 있다., 처음에는 자기 자신(yield)을 만들고 그 다음에는 자식을 순환한다.
#이때 그 자식은 depth_first메소드로 (yield from사용) 아이템을 만든다.
#토론
#파이선의 이터레이터 프로토콜은 __iter__()가 __next__() 메소드를 구현하고 종료를 알리기 위해 StopIteration 예외를 사용하는 특별 이터레이터 객체를 반환하기를 요구한다.
#하지만 이런 객체를 깔끔하게 구현하기가 쉽지 않다.예를 들어, 다음 코드는 관련 이터레이터 클래스를 사용한 depth_first() 메소드의 대안 구현법을 보여준다.
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        return DepthFirstIterator(self)

class DepthFirstIterator:
    def __init__(self,start_node):
        self._node=start_node
        self._children_iter = None
        self._children_iter = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._children_iter is None:
            self._children_iter = iter(self._node)
            return self._node

        elif self._child_iter:
            try:
                nextchild = next(self._childiter)
                return nextchild
            except StopIteration:
                self._child_iter=None
                return next(self)

        else :
            self._child_iter = next(self._children_iter).depth_first()
            return next(self)

#DepthFirstIteration 클래스는 제너레이터를 사용한 것과 동일하기 ㄷㅇ작한다. 하지만 순환하는 동안 생기는 복잡한 상황을 처리하기 위해 코드가 지저분하다.
#이터레이터를 제너레이터로 정의하고 그걸로 만족하자



