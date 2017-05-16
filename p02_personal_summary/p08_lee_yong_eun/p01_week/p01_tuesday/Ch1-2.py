#######################################################################################
# 1.2) 임의 순환체의 요소 나누기
# *args
#######################################################################################

def avg(list):
    return sum(list) / len(list)

# 첫 값과 마지막 값을 제외한 평균 반환하기
# *middle : first,last를 제외한 값
def drop_first_last(grades):
    first, *middle, last = grades
    return avg(middle)

# 전화번호만 빼내기
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record
print(phone_numbers) #['773-555-1212', '847-555-1212']

# 길이가 일정하지 않은 튜플에 사용하기
records = [
    ('foo',1,2),
    ('bar','hello'),
    ('foo',3,4)
]

def do_foo(a,b):
    print('foo',a,b)

def do_bar(a):
    print('bar',a)

for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)
    # foo 1 2
    # bar hello
    # foo 3 4

#문자열 프로세싱에 응용
line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
uname, *fields, homedir, sh = line.split(':')
print(homedir, sh) #/var/empty /usr/bin/false




