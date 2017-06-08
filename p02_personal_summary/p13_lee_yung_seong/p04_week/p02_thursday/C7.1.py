#매개변수 개수에 구애받지않는 함수 작성
#문제
#입력 매개변수 개수에 제한이 없는 함수를 작성하고 싶다.
#해결
#위치 매개변수의 개수에 제한이 없는 함수를 작성할면 * 인자
def avg(first, *rest):
    return (first + sum(rest)) / (1+len(rest))

#이 예제에서 rest에 추가적 위치 매개변수가 튜플로 들어가낟. 코드는 추후 작업에서 이를 하나의 시퀀스를 다룬다.
#키워드 매개변수 수에 제한이 없는 함수를 작성하려면 **로 시작하는 인자를 사용한다.
import html
def make_element(name,value,**attrs):
    keyvals = [ '%s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(name=name,attrs=attr_str,value=html.escape(value))
    return element

#attrs은 전달 받은 키워드 매개변수(있다면)를 저장하는 딕셔너리 이다.
#위치 매개변수와 키웓 ㅡ매개변수를 동시에 받는 함수를 작성하려면,* 와 **를 함께 사용하면 된다.
def anyargs(*args, **kwargs):
    print(args)
    print(kwargs)

#이 함수에서 모든 위치 매개변수는 튜플 args에, 모든 키워드 매개변수는 딕셔나리 kwargs에 들어간다.

#토론
#*는 함수 정의읭 마지막 위치 매개변수 자리에만 올 수 있다. **는 마지막 매개변수 자리에만 올 수 있다. 그리고 * 뒤에도 매개변수가 또 나올 수 있다는 것이 함수 정의의 미묘한 점이다.
def a(x,*args,y):
    pass
def b(x,*args,y,**kwargs):
    pass

#이런 매개변수는 키워드로만 넣을 수 있는 인자로 부름.