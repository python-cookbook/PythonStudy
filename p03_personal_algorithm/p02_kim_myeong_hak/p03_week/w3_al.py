input_number_list = input()
input_number = input_number_list.split(' ')

for number in input_number:
    number = int(number)
    cnt = 0
    if number == 1:
        print('number one')

    for i in range(1,number):
        if number%i == 0:
            cnt += 1
            if cnt >= 3:
                print('composite number')
                break
            elif cnt == 2:
                print('prime number')
