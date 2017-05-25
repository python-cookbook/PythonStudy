####################################################################################################
# 4.2] 델리게이팅 순환
#   * 리스트, 튜플 등 순환 가능한 객체를 담은 사용자 정의 컨테이너를 만들었다.
#     이 컨테이너에 사용 가능한 이터레이터를 만들고 싶다.
#
# * __iter__()
#   : 실제 순환을 위한 __next__() 메소드를 구현하는 특별 이터레이터 객체를 반환하기를 요구한다.
####################################################################################################

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


# 예제
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)
    # Node(1), Node(2) 출력


