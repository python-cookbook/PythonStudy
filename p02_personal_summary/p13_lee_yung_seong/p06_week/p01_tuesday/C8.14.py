#커스텀 컨테이너 구현
#문제
#리스트나 딕셔너리와 같은 내장 컨테이너와 비슷하게 동작하는 커스텀 클래스를 구현하고 싶다. 하지만 이때 정확히 어떤 메소드를 구현해야 할지 확신이 없다.
#해결
#collections 라이브러리에 이 목적으로 사용하기 적절한 추상 베이스 클래스가 많이 정의되어 있다.
#클래스에서 순환을 지원해야 한다고 가정하자
import collections
class A(collections.Iterable):
    pass

#위처럼 상속받으면 필요한 모든 특별 메소드를 구현하도록 보장해줌
a=A()
#메소드 구현해야함
#이 에러를 고치려면 클래스가 필요로 하는 __iter__() 메소드를 구현한다.
#컬렉션스에 정의되어 있는 클래스에 또 주목할 만한 것으로 sequence, mutable sequence, mapping, mutablemapping, set, mutableset이 있음. 이 클래스 중 다수는 기능이 증가하는
#체계를 형성한다.
import collections
collections.Sequence() #에러

import collections
import bisect

class SortedItems(collections.Sequence):
    def __init__(self,initial=None):
        self._items=sorted(initial) if initial is None else []

    #필요한 시퀀스 메소드
    def __getitem__(self,index):
        return self._items[index]
    def __len__(self):
        return len(self._items)
    #올바른 장소에 아이템을 추가하기 위한 메소드
    def add(self,item):
        bisect.insort(self._items,item)
#클래스 사용 예제
items = SortedItems([5,1,3])
list(items)

#sorteditems의 인스턴스는 보통의 시퀀스와 동일한 동작을 하고 인덱스,순환, len(), in 연산자 자르기등 일반적인 연산 모두지원
#토론
#collections에 있는 추상 베이스 클래스를 상속 받으면 커스텀 컨테이너에 필요한 메소드를 모두 구현하도록 보장할 수 있다. 하지만 이 상속에는 타입 확이 ㄴ기능도 있다.
items = SortedItems()
import collections
isinstance(itmes,collections.Iterable)
#collections에 있는 추상 베이스 클래스는 일반적인 컨테이너 메소드의 기본 구현을 제공 하는 것도 많다. 예를들어 다음과 같이 collections.mutablesequence에서 상속 받는 클래스가 있다고 가정해보자.
class Items(collections.MutablsSequence):
    def __init__(self,initial=None):
        self._items = list(initial) if initial is None else []
    #필요한 시퀀스 메소드
    def __getitem__(self,index):
        print('Getting:', index)
        return self._items[index]
    def __setitem__(self,index,value):
        print('Setting:',index,value)
    def __delitem__(self,index):
        print('Deleting:',index)
        del self._items[index]
    def insert(self,index,value):
        print('Inserting:',index,value)
        self._items.insert(index,value)
    def __len__(self):
        print('len')
        return len(self._items)
#items의 인스턴스를 만들면, 리스트 메소드 중 중요한 것을 거의 다 지원한다는 것을 확인할 수 있다. #
#이런 메소드는 필요한 것만 사용하는 식으로 구현되어 있다.
a=Items([1,2,3])
len(a)
