#### 초급 - 스택 자료구조 알고리즘 #####

num = int(input('숫자를 입력'))
stack = []
j = 0


while j in range(num):
    s = input()
    j += 1
    if 'i' in s.split(' '):
        a = s.split(' ')
        stack.append(a[1])
    elif s == 'o':
        if stack != []:
            print(stack.pop())
        else:
            print('empty')
    elif s == 'c':
        print(len(stack))

##