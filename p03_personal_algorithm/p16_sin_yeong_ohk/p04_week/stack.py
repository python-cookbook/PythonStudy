list_ = []
while 1:
    number = input('입력# ')
    num = number.split(' ')
    for i in num:
        pass
    if number == 'c':
        print(len(list_))
    elif number == 'o':
        if len(list_) == 0:
            print('empty')
        else:
            print(list_[-1])
            list_.pop()
    elif number != 'c' and 'o':
        list_.append(i)
        print(i)