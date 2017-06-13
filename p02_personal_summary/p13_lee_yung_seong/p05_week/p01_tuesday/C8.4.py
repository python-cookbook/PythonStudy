#인스턴스를 많이 생성할 때 메모리 절약
#문제
#프로그램에서 많은 인스턴스를 생성하고 메모리를 많이 소비한다.
#해결
#간단한 자료구조 역할을 하는 클래스의 경우 slots 속성을 클래스 저읭에 추가하면 메모리 사용을 줄일수있다
class Date:
    __slots__ = ['year','month','day']
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day

#slots를 정의하면 파이썬은 훨씬 더 압축된 내부 표현식을 사용한다.
#인스턴스마다 딕셔너리를 구성하지 않고 튜플이나 리스트 같은 부피가 작은 고정 배열로 인스턴스가 만들어진다.
#토론
#슬롯을 사용해서 절약하는 메모리는 속성이ㅡ 숫자와 타입에 따라 다르다. 하지만 일반적으로 그 데이터를 튜플에 저장할 때의 메모리 사용과 비교할 만하다.
#하지만 슬롯 사용은 피하는게 좋다. 파이썬에 일반 딕셔너리 기반 구현에 의존하는 부분이 많다.
#그리고 슬롯을 정의하면 다중 상속과 같은 특정 기능을 지원하지 않음.
#자료구조에만 슬롯사용을 고려.
#슬롯은 최적화 용으로만 사용하자