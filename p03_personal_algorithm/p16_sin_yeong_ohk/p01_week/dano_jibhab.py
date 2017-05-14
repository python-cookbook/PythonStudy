str_ = input('입력# ')    #입력받고
str1 = str_.split(' ')    #공백을 기준으로 자르기
if str1 != '':    #NONE이 아니면
    print(str_)    #처음 입력받은 문장 출력

if str1 != 'END':    #첫문장이 END가 아니면
    while True:    #무한루프
        str_ = input('입력# ')    #다음 문장 입력받아서
        str2 = str_.split(' ')    #또 자르기
        if str_ =='END':    #입력받은 문장이 END라면
            break    #loop 빠져나가기
        for i in str1:    #자른 첫문장을 루프돌리고
            for j in str2:    #그 다음문장을 루프돌려서
                if i == j:    #같은 요소는
                    str2.remove(j)    #다음문장 리스트에서 빼기
        for k in str2:    #제거하고 남은 다음문장 리스트를 또 돌려서
            str1.append(k)    #첫문장에 넣고
        print(' '.join(str1))    #출력