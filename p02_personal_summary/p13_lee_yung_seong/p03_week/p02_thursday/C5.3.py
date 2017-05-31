#구별자나 종단 부호 바꾸기
#문제
#print()를 사용해  데이터를 출력할 때 구분자나 종단 부호를 바꾸고 싶다.
#해결
#seq or end
print('ACME',50,91.5)
print('ACME',50,91.5,sep=',')
print('ACME',50,91.5,sep=',', end='!!\n')
#출력의 개행 문자를 바꿀 때도 end인자를 사용한다.
for i in range(5):
    print(i  ,end=' ')

#토론
#print()로 출력시 아이템을 구분하는 문자를 스페이스 공백문 이외로 바꾸는 가장 쉬운 방벙븐 구별자를 지정하는 것이다.,
#어떤 프로그래머는 동일한 목적으로 str.join()을 사용하기도 한다.
print(','.join('ACME','50','91.5'))#안됨

#하지만 str.join은 문자열만 작동함.
#문자열이 아닌 데이터는?
row = ('ACME',50,91.5)
print(','.join(str(x) for x in row))

#구별자가 훨씬 편함
print(*row, sep=',')
