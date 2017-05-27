def discriminator(input_list):
    number_list = input_list.split(' ')
    print(number_list)
    for number in number_list:
        i = int(number)
        if i == 1:
            print('number one(1)')
        else:
            for j in range(2, i):
                if j == i - 1:
                    print('prime number(소수)')
                elif i % j == 0:
                    print('composite number(합성수)')
                    break


discriminator('7 24 23 19 1 3 4 5 6 7 1 1212154657')