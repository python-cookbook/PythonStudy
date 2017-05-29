number = input('숫자 입력# ')
num = number.split(' ')

list_=[]
for i in num:
    if int(i) == 1:
        print('number one')
    else:
        for j in range(1,int(i)):
            if int(i)%int(j) == 0:
                list_.append(int(i))
        if len(list_)==1:
            print('prime number')
            list_=[]
        else:
            print('composite number')
            list_=[]