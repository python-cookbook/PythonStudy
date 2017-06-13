##########################################################################################################
# 6.8] 관계형 데이터베이스 작업
#   * 관계형 데이터베이스에 선택, 삽입, 행 삭제 등의 작업을 하고 싶다.
#
#   * 파이썬에 데이터 행을 나타내는 표준은 튜플 시퀀스이다.
#     주어진 형식을 통해 파이썬의 표준 DB API(예 : sqlite3)를 사용하면 관계형 데이터베이스 작업은 간단하다.
#     단, 데이터베이스 자료를 파이썬 타입에 매핑할 때 주의해야 한다.
#     정확한 매핑은 데이터베이스 백엔드에 따라 달라지기 때문에 관련 문서를 잘 읽어봐야 한다.
##########################################################################################################
import sqlite3
# connect() : DB 연결. 일반적으로 DB명, 호스트명, 사용자명, 암호 등 필요한 정보를 넣는다.
db = sqlite3.connect('database.db')

# SQL 쿼리 실행을 위한 커서 생성
c = db.cursor()
# 테이블 생성
#c.execute('create table portfolio (symbol text, shares integer, price real)')
db.commit()

# 데이터에 행 시퀀스 삽입
stocks = [
    ('GoG', 100, 490.1),
    ('AAPL', 50, 545.75)
]
c.executemany('insert into portfolio values (?,?,?)', stocks)
db.commit()

# 쿼리 수행
for row in db.execute('select * from portfolio'):
    print(row, end=' ') # ('GoG', 100, 490.1) ('AAPL', 50, 545.75)

# 사용자 파라미터 받아서 이용 : '?'
min_price = 500
for row in db.execute('select * from portfolio where price >= ?', (min_price,)):
    print(row)

