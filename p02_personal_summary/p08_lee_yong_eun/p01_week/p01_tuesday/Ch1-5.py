#######################################################################################
# 1.5) 우선순위 큐(Priority Queue) 구현
#
# heapq : heappush(list, (priority, index, item))
# class : __repr__ : print 시에 작동
#######################################################################################

import heapq


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0 #삽입 순서 : priority가 같을 때 index가 낮은 쪽이 우선순위가 높다, unique key로서의 역할도 가능

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1] # -1 : 시퀀스의 제일 마지막 값


class Item:
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return 'Item({!r})'.format(self.name)


q = PriorityQueue()
q.push(Item('foo'), 1)
q.push(Item('bar'), 5)
q.push(Item('spam'), 4)
q.push(Item('grok'), 1)
print(q.pop()) #Item('bar')
print(q.pop()) #Item('spam')
print(q.pop()) #Item('foo')
print(q.pop()) #Item('grok')
#우선순위가 같은 foo와 grok은 삽입된 순서와 동일하게 반환된다

