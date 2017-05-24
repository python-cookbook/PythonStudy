num = int(input())
array = [ [ 0 for i in range(num) ] for j in range(num) ]
n = 1
x, y = 0, 0
v = 1, 0
array[y][x] = n
while 1:
    x, y = x+v[0] , y+v[1]
    if (x < 0) or (x >= num) or (y < 0) or (y >= num) or (array[y][x] != 0):
        x, y = x-v[0] , y-v[1]
        v = -v[1], v[0] #v값 로테이션 시켜주는 부분 .
        x, y = x+v[0] , y+v[1]
    n+=1
    array[y][x] = n
    if n == (num*num):
        break

for y in range(num):
    for x in range(num):
        print ("%4d"%array[y][x],end="")
    print('\n')

#완료