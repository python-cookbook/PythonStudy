##########################################################################################################
# 4.4] 이터레이터 프로토콜 구현
#   * 순환을 지원하는 객체를 만드는데, 이터레이터 프로토콜을 구현하는 쉬운 방법이 필요하다.
#
# 1] 제너레이터 사용
#   : yield
# 2] __next__를 클래스로 구현
#   : 복잡하고 별로 좋지도 않다.. 제너레이터 쓰자.
##########################################################################################################

## depth-first 이터레이터
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


#예제
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))
    for ch in root.depth_first():
        print(ch, end=' ')  # Node(0) Node(1) Node(3) Node(4) Node(2) Node(5)
