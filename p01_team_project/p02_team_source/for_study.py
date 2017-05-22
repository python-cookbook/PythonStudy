'''


# 야구게임
1) https://youtu.be/45CxKN0O6UI


# @property

1) http://brownbears.tistory.com/160
2) https://www.programiz.com/python-programming/property


# attack()
1) 함수 작동 방식 

# Team.init_player()
1) 어떤 자료가 들어가나
dic = ({1: '정근우'}, {2: '이용규'}, {3: '송광민'}, {4: '최진행'}, {5: '하주석'}, {6: '장민석'}, {7: '로사리오'}, {8: '이양기'}, {9: '최재훈'})

for i in dic :
    print(list(i.items()))

[(1, '정근우')]
[(2, '이용규')]
[(3, '송광민')]
[(4, '최진행')]
[(5, '하주석')]
[(6, '장민석')]
[(7, '로사리오')]
[(8, '이양기')]
[(9, '최재훈')]

for i in dic :
    print(list(i.items())[0])
(1, '정근우')
(2, '이용규')
(3, '송광민')
(4, '최진행')
(5, '하주석')
(6, '장민석')
(7, '로사리오')
(8, '이양기')
(9, '최재훈')

for i in dic :
    num, name = list(i.items())[0]
    print(num, name)
1 정근우
2 이용규
3 송광민
4 최진행
5 하주석
6 장민석
7 로사리오
8 이양기
9 최재훈



# Game 클래스 변수 설정한 이유는?

# Game.advance_setting()
1) 함수 작동 방식 
2) 왜 range는 큰 수에서 작은 수로 loop 돌게 했나


'''