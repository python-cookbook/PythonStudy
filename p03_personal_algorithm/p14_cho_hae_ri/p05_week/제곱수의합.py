


# 초급 알고리즘 - 해리

def square(num):
    for i in range(num+1, 0, -1):
        if pow(i, 2) <= num:
            a.append(i)
            re = num-pow(i,2)
            return square(re)
    print(len(a), '개 입니다.')

a=[]
square(464)