##########################################################################################################
# 7.1] 매개변수 개수에 구애받지 않는 함수 작성
#   * 입력 매개변수 개수에 제한이 없는 함수를 작성하고 싶다.
#       : '*' 인자, '**' 인자 사용
#   '*' 인자 : 개수 제한 없이 위치 매개변수 받기
#   '**' 인자 : 개수 제한 없이 키워드 매개변수 받기
#
#
#   '*'는 함수 정의의 마지막 위치 매개변수에만 올 수 있다.
#   '**'는 마지막 매개변수 자리에만 올 수 있다.
#   '*' 뒤에도 매개변수가 또 나올 수 있다는 것이 함수 정의의 미묘한 점이다.
#       ex) def b(x, *args, y, **kwargs):
##########################################################################################################

# 위치 매개변수 : *
def avg(first, *rest):
    print((first + sum(rest)) / (1 + len(rest)))

avg(1, 2)       # 1.5
avg(1, 2, 3, 4) # 2.5

# 키워드 매개변수 : **
import html
def make_element(name, value, **attrs):
    keyvals = [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(
        name = name,
        attrs = attr_str,
        value = html.escape(value)
    )
    return element

# 예제
# '<item size="large" quantity="6">Albatross</item>' 생성
make_element('item', 'Albatross', size='large', quantity=6)

# '<p>&lt;spam&gt;</p>' 생성
make_element('p', '<spam>')

# 위치 매개변수와 키워드 매개변수 동시에 받기
def anyargs(*args, **kwargs):
    print(args) # 튜플
    print(kwargs)   # 딕셔너리