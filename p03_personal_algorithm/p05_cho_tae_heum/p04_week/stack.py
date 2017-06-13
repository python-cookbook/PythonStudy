commend_cnt = int(input('명령어 개수'))
stack_list = []
for i in range(commend_cnt):
    commend = input('명령어를 입력하세요')
    commend_list = commend.split(' ')

    if commend_list[0] == 'i':
        stack_list.append(commend_list[1])

    elif commend_list[0] == 'c':
        print(len(stack_list))

    elif commend_list[0] == 'o':
        if len(stack_list) == 0:
            print('empty')
        try:
            print(stack_list.pop())
        except:
            pass