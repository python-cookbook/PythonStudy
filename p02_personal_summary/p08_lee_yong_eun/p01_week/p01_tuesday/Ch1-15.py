#######################################################################################
# 1.15) 필드에 따라 레코드 묶기
#     * 일련의 딕셔너리나 인스턴스가 있고 특정 필드 값에 기반한 그룹의 데이터를 순환하고 싶다.
#
# itertools.groupby() : 특정 값으로 묶기 (정렬 후 사용해야 한다)
#
# * defaultdict를 사용하여 multidict를 구성하는 것이 더 나을 수도 있다 !
#######################################################################################

rows = [
    {'address': '5412 ~', 'date': '07/01/2012'},
    {'address': '5148 ~', 'date': '07/04/2012'},
    {'address': '5800 ~', 'date': '07/02/2012'},
    {'address': '2122 ~', 'date': '07/03/2012'},
    {'address': '5645 ~', 'date': '07/02/2012'},
    {'address': '1060 ~', 'date': '07/02/2012'},
    {'address': '4801 ~', 'date': '07/01/2012'},
    {'address': '1039 ~', 'date': '07/04/2012'},
]

from operator import itemgetter
from itertools import groupby

#원하는 필드로 정렬
rows.sort(key=itemgetter('date'))

#그룹 내부 순환
for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print(' ', i)
''' 결과:
07/01/2012
  {'address': '5412 ~', 'date': '07/01/2012'}
  {'address': '4801 ~', 'date': '07/01/2012'}
07/02/2012
  {'address': '5800 ~', 'date': '07/02/2012'}
  {'address': '5645 ~', 'date': '07/02/2012'}
  {'address': '1060 ~', 'date': '07/02/2012'}
07/03/2012
  {'address': '2122 ~', 'date': '07/03/2012'}
07/04/2012
  {'address': '5148 ~', 'date': '07/04/2012'}
  {'address': '1039 ~', 'date': '07/04/2012'}
'''
