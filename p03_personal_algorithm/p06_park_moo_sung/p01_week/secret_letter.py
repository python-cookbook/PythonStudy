from copy import deepcopy

###################################################################################################
## 1. 문제        : 오류고정 (고급)
## 2. 소요 시간   : 0.0 초 (소수점 6자리 반올림)
## 3. 사용 메모리 :  2000 byte
## 4. 만든 사람   : 박무성
###################################################################################################

# 올바른 비밀번호 리스트 만들
a = ['0','0','0','0','0','0']
b = ['0','0','1','1','1','1']
c = ['0','1','0','0','1','1']
d = ['0','1','1','1','0','0']
e = ['1','0','0','1','1','0']
f = ['1','0','1','0','0','1']
g = ['1','1','0','1','0','1']
h = ['1','1','1','0','1','0']

# 올바른 비밀번호 리스트들을 letter_list에 넣기
letter_list = [a,b,c,d,e,f,g,h]

# password_dict 딕셔너리에 입력(예 : '000000' : 'A')
password_dict={''.join(a):'A',
               ''.join(b):'B',
               ''.join(c):'C',
               ''.join(d):'D',
               ''.join(e):'E',
               ''.join(f):'F',
               ''.join(g):'G',
               ''.join(h):'H'}

# 실수로 틀린 비밀번호 리스트들을 password_dict 딕셔너리에 넣기
for letter in letter_list:
    for idx in range(6):
        copy_letter = deepcopy(letter)
        copy_letter[idx] = '0' if letter[idx] == '1' else '1'
        password_dict[''.join(copy_letter)] = password_dict[''.join(letter)]

# input 받기
wordcnt = int(input('1.몇 글자인가요? '))
password = input('2.비밀편지를 입력하세요 ')
print_letter = ''

# 결과값 출력
for cnt in range(wordcnt):
    try:
        print_letter += password_dict[password[6*cnt:6*cnt+6]]
    except KeyError:
        print(cnt+1)
        print_letter =''
        break
print(print_letter)