#이름없는 함수와 인라인 함수 정의
#믄제
#sort등에 사용할 짧은 콜백 함수를 만들어야 하는데, 한 줄 짜리 함수를 만들면서 def 구문까지 사용하고 싶지는 않다.
#해결
#lambda
add = lambda x,y:x+y
add(2,3)
add('hello','world')
#일반적으로 lambda는 정렬이나 데이터 줄이기 등 다른 작업에 사용할 때 많이 쓴다.
names = ['David Beazly','Brian Jones','Raymond Hettinger']
sorted(names,key=lambda name:name.split()[-1].lower())
#토론
#람다를 사용해서 간단한 함수를 정의할 수 있지만 제약이 많다. 우선 표현식을 하나만 사용해야 하고 그 결과가 반환값이 된다. 따라서 명령문을 여러개 쓴다거나 조건문, 순환문, 에러 처리를 넣을 수 없다.
