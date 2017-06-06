#CSV데이터 읽고 쓰기
#문제
#csv파일로 인코딩된 데이터를 읽거나 쓰고 싶다.
#해결
#대부분의 csv데이터는 csv라이브러리를 사용한다. 예를 들어 stocks.csv 파일에 담겨 있는 주식 시장 정보가 있다고 가정해보자.
#다음 코드로 데이터를 읽어 튜플 시퀀스에 넣을 수 있다
import csv
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        #행처리
#앞에 나온 코드에서 row는 튜플이 된다. 따라서 특정 필드에 접근할면 row[0](Symbol), row[4](Change)와 같이 인덱스를 사용해야 한다.
#인덱스 사용이 때때로 헷갈리기 때문에 네임드 튜플을 고려하는 것도 좋다.
from collections import namedtuple
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row',headings)
    for r in f_csv:
        row = Row(*r)
        #행 처리

#이렇게 하면 row.Symbol이나 row.Change와 같이 열 헤더를 사용할 수 있다. 다만 열 헤더가 유효한 파이썬 식별자여야 한다. 그렇지 않으면 초기 헤딩에 메시지를 보내서 식별자가 아닌 문자를 밑줄아나
#유사한 것으로 변경해야 할지도 모른다.
#또 다른 대안으로 데이터를 딕셔너리 시퀀스로 읽을 수도 있다.
import csv
with open('stock.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        #행처리..

#이 버전의 경우 각 행의 요소에 접근하기 위해서 행 헤더를 사용한다. 예를 들어 row['Symbol']또는 row['Chamge']등과 같이 한다.
#csv데이터를 쓰려면 csv모듈을 사용해서 쓰기 객체를 생성한다.
headers=['symbol','price']
rows = [('AA',39.48)]
with open('stock.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerow(rows)
#데이터를 딕셔너리 시퀀스로 가지고 있다면 다음과 같이 한다.
headers = ['Symbol','Price']
rows = [{'Symbol' : 'AA', 'Price' : 39.48}]
with open('stocks.csv','w') as f:
    f_csv = csv.DictWriter(f,headers)
    f_csv.writeheader()
    f_csv.writerow(rows)
#토론
#csv 데이터를 수동으로 다루는 프로그램을 작성하기 보다는 csv 모듈을 사용하는 것이 훨씬 나은 선택이다. 예를 들어 다음과 같은 코드를 작성하고 싶을지 모른다.
with open('stock.csv') as f:
    for line in f:
        row = line.split(',')
        #행처리
#앞에 나온 코드를 사용하면 프로그래머가 일일이 처리해야 할 점이 많아진다는 문제점이 있다.
#탭으로 나누어진 데이터
with open('stock.csv') as f:
    f_tsv = csv.reader(f,delimeter='\t')
    for row in f_tsv:
        #행 처리

#csv 데이터를 읽고 네임드 튜플로 변환한다면 열 헤더를 검증할 때 주의해야 한다. 예를 들어 csv 파일에 다음과 같이 유효하지 않은 식별 문자가 들어 있을 수 있다.
#실제로 앞에 나온 데이터로 네임드튜플을 만들때 valueerror 예외가 발생한다. 이 예외를 피하기 위해서 우선 헤더를 처리해야한다.
#예를 들어 다음과 같이 정규 푷ㄴ식을 사용해서 유효하지 않은 문자를 치환한다.
import re
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headers = [ re.sub('[^a-zA-Z_]','_',h) for h in next(f_csv)]
    Row = namedtuple('Row',headers)
    for r in f_csv:
        row = Row(*r)

#또한 csv는 데이터를 해석할 하거나 문자열이 아닌 형식으로 변환하려 하지 않는다는 점이 중요하다. 그런 변환이 중요하다면 프로그래머가 스스로 해야한다.
#CSV 데이터에 대해서 추가적인 형식 변환을 하는 예제를 보자.
col_types = [str,float,str,str,float,int]
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        #행 아이템에 변환 적용
        row = tuple(convert(value) for convert, value in zip(col_types,row))

#딗너리에서 선택한 필드만 변환하는 예제는 다음과 같다.
print('Reading as dicts with type conversion')
field_types = [('Price', float), ('Change', float)]
with open('stocks.csv') as f:
    for row in csv.DictReader(f):
        row.update((key, conversion(row[key])) for key, conversion in field_types)
    print(row)
#이런 변환을 할 때는 주의해야함. 실제 프로그램을 작성할 때 csv 파일에 값이 빠지거나 데이터가 망가져 있는 등 타입 변환에서 문제가 될 만한 이슈가 많다. 따라서 데이터에 에러가 없다고
#보장 하지 않는 이상은 항상 이 부분을 고려해야 한다(적절한 예외 처리 코드를 넣는 것이 좋다.)
#마지막으로 csv 데이터를 읽어 데이터 분석이나 통계에 활용하려는 경우 판다스를 사용하자.
