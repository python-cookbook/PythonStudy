##########################################################################################################
# 7.2] 키워드 매개변수만 받는 함수 작성
#   * 키워드로 지정한 특정 매개변수만 받는 함수가 필요하다.
#       : 이 기능은 키워드 매개변수를 * 뒤에 넣거나 이름 없이 *만 사용하면 간단히 구현할 수 있다.
#           keyword-only 인자는 추가적 함수 인자를 명시할 때 코드의 가독성을 높이는 좋은 수단이 될 수 있다.\
#
#    * help() : 인자 정보 및 함수에 기재된 주석을 확인할 수 있다.
#       ex) help(recv)
#       : recv(maxsize, *, block)
#           Receives a message
##########################################################################################################

def recv(maxsize, *, block):
    'Receives a message'
    pass

# recv(1024, True)    # TypeError
recv(1024, block=True)  # Ok

# 응용 : 숫자가 다른 위치 매개변수를 받는 함수에 키워드 매개변수를 명시할 때 사용할 수도 있다.
def minimum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    print(m)

minimum(1, 5, 2, -5, 10)            # -5
minimum(1, 5, 2, -5, 10, clip=0)    # 0

help(recv)

