#여러 시퀀스 동시에 순환
#문제 : 여러 시퀀스를 동시에 순환하고 싶다.
#해결 : zip
xpts = [1,5,4,2,10,7]
ypts = [101,78,37,15,62,99]
for x,y in zip(xpts,ypts):
    print(x,y)

#zip(a,b)는 tuple(x,y)를 생성하는 이터레이터를 생성한다.
#순환의 길이는 둘중에 짧은 것 까지만 순환 됨.
a=[1,2,3]
b=['w','x','y','z']
for a,b in zip(a,b):
    print(a,b)

#마음에 안들면 zip_longest
from itertools import zip_longest
for i in zip_longest(a,b):
    print(i)

for i in zip_longest(a,b,fillvalue=0): #널값에 채울 값을 정해줌
    print(i)

#토론 : zip은 데이터를 묶어야 할 때 주로 사용한다. 예를 들어 열 헤더와 값을 리스트로 가지고 있다고 가정하자.
headers = ['name','share','price']
value = ['acme',100,490.1]
#zip을 이용하면 두 값을 묶어 딕셔너리로 만들 수 있다.
s = dict(zip(headers,value))
s
#출력하려면
for name,val in zip(headers,value):
    print(name,'=',val)
#일반적이지는 않지만 zip()에 시퀀스를 두 개 이상 입력할 수 있다. 이런 경우 결과적으로 튜플에는 입력한 시퀀스의 개수 만큼의 아이템이 포함된다.
a=[1,2,3,]
b=[10,11,12]
c=['x','y','z']
for i in zip(a,b,c):
    print(i)

#마지막으로 zip이 결과적으로 이터레이터를 생성한다는 점을 기억하자. 묶은 값이 저장된 리스트가 필요하다면 list()함수를 사용한다.
zip(a,b)
list(zip(a,b))