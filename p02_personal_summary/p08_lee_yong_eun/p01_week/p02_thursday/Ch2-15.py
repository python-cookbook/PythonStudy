####################################################################################################
# 2.15] 문자열에 변수 사용
#   * 문자열에 변수를 사용하고 이 변수에 맞는 값을 채우고 싶다.
#
# 1] format() 사용
# 2] format_map() 사용
#  * vars() : 현재 변수 리스트를 반환
#   * __missing__ 메소드 : 
####################################################################################################

## format()
s = '{name} has {n} messages'
print(s.format(name='Guido',n=37))  # Guido has 37 messages

## format_map()
#vars() 이용
name = 'Bravo'
n = '70'
print(vars())
# {'__name__': '__main__', '__doc__': None, '__package__': None, ......
# 'name': 'Bravo', 'n': '70'}
print(s.format_map(vars())) # Bravo has 70 messages

# 인스턴스 이용
class Info:
    def __init__(self, name, n):
        self.name = name
        self.n = n

a = Info('Clerk','3')
print(s.format_map(vars(a)))    # Clerk has 3 messages