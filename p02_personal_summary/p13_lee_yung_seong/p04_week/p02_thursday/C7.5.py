#기본 인자를 사용하는 함수 정의
#문제
#함수나 메소드를 정의할 때 하나 혹은 그 이상 인자에 기본 값을 넣어 선택적으로 사용할 수 있도록 하고 싶다.
#해결
#표면적으로 선택적 인자를 사용하는 함수를 정의하기는 쉽다. 함수 정의부에 값을 할당하고 가장 뒤에 이를 위치시키기만 하면 된다.
def spam(a, b=42):
    print(a,b)

spam(1)
spam(1,2)
#기본값이 리스트, 세트, 딕셔너리 등 수정 가능한 컨테이넝야 한다면 none을 사용해 다음과 같은 코드를 작성
def spam(a,b=None):
    if b is None:
        b=[]
#기본값을 제공하는 대신 함수가 받은 값이 특정 값인지 아닌지 확인하려면 다음 코드를 사용한다.
_no_value = object()
def spam(a,b=_no_value):
    if b is _no_value:
        print('No b...')

#함수는 다음과 같이 동작한다.
spam(1)
spam(1,2)
spam(1,None)
#앞에 나온 예제에서 아무런 값을 전달하지 않았을 때와 None값을 전달했을 때의 차이점에 주목하자
#토론
#기본인자를 가지는 함수를 정의하는 것은 간단, 눈에 보이는 것 외에 신경써야 할 부분이 있다.
#첫째로 할당하는 기본 값은 함수를 정의할 때 한번만 정해지고 그 이후에는 변하지 않는다.
x = 42
def spam(a,b=x):
    print(a,b)
spam(1)
x=23
spam(1)
#변수 x 의 값을 바꾸어도 그 이후에 기본 값이 변하지 않는다. 기본 값은 함수로 정의할 때 정해지기 때문이다.
#두번째로 기본 값으로 사용하는 값은 None, True, False, 숫자, 문자열 같이 항상 변하지 않는 객체를 사용해야 한다. 특히 다음과 같은 코드는 사용하지 않는다.
def spam(a,b=[]):
    return 'NO!!'
#이렇게 하면 기본 값이 함수를 벗어나서 수정되는 순간 많은 문제가 발생한다. 값이 변하면 기본 값이 변하게 되고 추후 함수 호출에 영향을 준다.
def spam(a,b=[]):
    print(b)
    return b

x=spam(1)
x.append(99)
x.append('yow')
x
spam(1)
#이런 부작용을 피하려면 앞의 예제에 나왔듯이 기본값으로 None을 할당하고 함수 내부에서 이를 확인하는 것이 좋다.
#None 을 확인할 때 is 연산자를 사용하는 것이 매우 중요하다. 어떤 사람은 다음과 같은 코드를 작성하는 실수를 범하기도 한다.
def spam(a, b=None):
    if not b:
        b = []
#여기서 문제는 None 이 False로 평가되지만, 그 외에 다른 객체(예: 길이가 0인 문자열, 리스트, 튜플, 딕셔너리 등)도 False로 평가된다는 점이다.
#따라서 특정 입력을 없다고 판단하게 된다.
spam(1)
x = []
spam(1,x)
spam(1,0)
spam(1,'')

#이번 레시피의 마지막 부분은 어쩌면 사소한 것인데, 함수가 추가적 매개변수 위치에 있는지 없는지 판단하는 것이다. 여기서 쉽지 않은 점은 사용자가 인자를 넣었는지 확인할 때 기본값으로
#None,0 또는 False를 사용할 수 없다는 것이다. 왜냐하면 사용자가 인자를 넣어쓴지 확인할 때 기본값으로 none,0,false를 사용할 수 없다느 ㄴ것이다.
#왜냐하면 사용자가 바로 이 값을 인자로 넣을 수도 있기 때문.
#이 문제를 해결하기 위해서는 앞의 예제에 나온것처럼 object의 유일한 인스턴스를 만들어야 한다. 그리고 함수에서 이 특별한 값과 들어온 인자를 비교해서
#인자가 있는지 없는지 알 수 있다. 이때 사용자가 _no_value 인스턴스를 입력 값으로 전달할 확률이 극히 적다. 따라서 값이 있는지 없는지 확인하는 데 이 인스턴스를 사용해도 안전하다.
