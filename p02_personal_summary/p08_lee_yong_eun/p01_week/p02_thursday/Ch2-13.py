####################################################################################################
# 2.13] 텍스트 정렬
#   * 텍스트를 특정 형식에 맞추어 정렬하고 싶다.
#
# 1] ljust(), rjust(), center()
#   : 좌정렬, 우정렬, 가운데
# 2] format()
#   : 인자로 <. >, ^ 사용
####################################################################################################

text = 'Hello World'

## ljust, rjust, center를 사용한 정렬
print(text.ljust(20))   # 'Hello World         '
print(text)             # 'Hello World'
print(text.rjust(20))   # '         Hello World'
print(text.center(20))  # '    Hello World     '

## 채워넣기 문자 사용
print(text.ljust(20,'-'))   # 'Hello World---------'

## format()을 사용한 정렬
print(format(text,'>20'))   # '         Hello World'
print(format(text,'<20'))   # 'Hello World         '
print(format(text,'^20'))   # '    Hello World     '

## format에 채워넣기 문자 사용
print(format(text,'=>20'))  # '=========Hello World'
print(format(text,'=^20'))  # '====Hello World====='

## format을 사용해 여러 값을 서식화
print('{:>10s} {:>10s}'.format('Hello', 'World'))   # '     Hello      World'

## format을 사용한 형변환
x = 1.2345
print(format(x, '>10'))     # '    1.2345'
print(format(x, '>10.2f'))  # '      1.23'