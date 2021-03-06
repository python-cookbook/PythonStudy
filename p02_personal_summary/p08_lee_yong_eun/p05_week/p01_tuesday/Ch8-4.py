##########################################################################################################
# 8.4] 인스턴스를 많이 생성할 때 메모리 절약
#   * 프로그램에서 많은(예: 수백만) 인스턴스를 생성하고 메모리를 많이 소비한다.
#       : __slots__ 속성을 추가하여 메모리 사용을 상당히 많이 절약할 수 있다.
#         아래의 예시처럼 slots을 정의하면 파이썬은 인스턴스에서 훨씬 더 압축된 내부 표현식을 사용한다.
#         인스턴스마다 딕셔너리를 구성하지 않고 튜플이나 리스트 같이 부피가 작은 고정 배열로 만들어진다.
#         단, 슬롯에 없는 새로운 속성은 인스턴스에 추가할 수 없다는 점에 유의해야 한다.
#
#   * 예시 : 아래 Date 인스턴스를 slots 없이 저장하면 64비트 파이썬에서 428바이트를 소비한다.
#           하지만 슬롯을 정의하면 메모리 사용이 156바이트로 떨어진다.
#
#   * 얼핏 생각하기에 슬롯을 사용하는 곳이 많을 것같지만 대개의 코드에서 슬롯 사용은 피하는 것이 좋다.
#     파이썬에는 일반 딕셔너리 기반 구현에 의존하는 부분이 많으며, 슬롯을 정의한 클래스는 다중상속 등의
#     특정 기능을 지원하지 않는다. 프로그램에서 자주 사용하는 자료구조에만 슬롯 사용을 고려하는 것이 좋다.
#     (예: 특정 클래스에서 수백만 개의 인스턴스를 생성하는 경우)
#
#   * 슬롯을 인스턴스에 새로운 속성을 추가하지 못하게 하는 캡슐화 도구로 오해하는 경우가 많다.
#     슬롯을 쓰면 이런 현상이 생기기는 하지만, 원래 이런 용도로 디자인한 것은 아니며, 항상 최적화 도구로만 사용해야 한다.
###########################################################################################################

class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

