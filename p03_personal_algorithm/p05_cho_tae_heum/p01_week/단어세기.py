while True:
    word1 = input('문장입력 ').upper()
    if word1 == 'END':
        break
    else:
        word2 = word1.split(' ')
        word3 = list(set(word2))
        for i in word3:
            print(i + ' : '+ str(word2.count(i)))
