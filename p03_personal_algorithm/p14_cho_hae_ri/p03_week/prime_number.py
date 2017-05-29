


a = input('숫자를 5개 입력하세요 : ')

b = a.split(' ')

for number in b:
    number = int(number)

    cnt = 0

    if number == 1:
        print('number one')

    for j in range(1, number+1):

        if number % j == 0:
            cnt += 1

    if cnt >= 3:
        print('composite number')

    elif cnt ==2:
        print('prime number')
