while True:    #무한루프 돌리기
    str_ = input('입력# ')     #문장 입력받구
    str1= list(set(str_.split(' ')))    #입력받은 문장을 공백기준으로 잘라내기+set으로 중복제거
    str2 = str_.split(' ')    #입력받은 문장을 중복제거하지 않고 잘라내기
    str1.sort()    #중복제거된 리스트를 알파벳순서로 정렬
    if str_=='END':    #입력받은 문장이 END라면 loop 나가기
        break
    else:   #END 아니면
        for i in str1:    #중복제거된 리스트 loop돌리기
            sum = 0    #sum 변수를 숫자로 받기
            for j in str2:    #중복제거X 문장을 돌려서
                if i == j:    #같으면
                    sum+=1    #sum에서 1씩 더해서 개수 세기
            print(i,':',sum)    #출력