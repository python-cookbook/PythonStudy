list_ = []
num = int(input('숫자# '))

if (num >= 1) and (num <= 10000):
    for i in range(num, 0, -1):
        if pow(i, 2) <= num:
            num = num - pow(i, 2)
            list_.append(i)
            if (num != 0) and (num <= 3):
                for j in range(1,num):
                    if j == 1:
                        list_.append(j)

print(len(list_))