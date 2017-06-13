#키워드 매개변수만 받는 함수 작성\
#문제
#키워드로 지정한 특정 매개변수만 받는 함수가 필요하다
#해결
#이 기능은 키워드 매개변수를 * 뒤에 넣거나 이름없이 *만 사용하면 간단히 구현할 수 있다.
def recv(maxsize,*,block):
    'receives a message'
    pass

recv(1024,True)
recv(1024,block=True)
#이 기술로 숫작 ㅏ다른 위치 매개변수를 받는 함수에 키워드 매개변수를 명시할 때 사용 할 수도 있다.,
def mininum(*values,clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m

mininum(1,5,2,-5,10)
#토론
#키워드로만 넣을 수 있는 인자는 추가적 함수 인자를 명시할 때 코드의 가독성을 높이는 좋은 수단이 될 수 있다.
msg = recv(1024,False)
#recv()가 어떻게 동작하는지 잘 모르는 사람이 있다면 False 인자가 무엇을 의미하는지도 모를 것이다. 따라서 호출하는 측에서 다음과 같은 식으로 표시해 준다면 이해하기 훨씬 쉽다.
msg = recv(1024,block=False)
#키워드로만 넣을 수 있는 인자는 **kawrgs와 관련된 것에 사용자가 도움을 요청하면 도움말 화면에 나타난다
