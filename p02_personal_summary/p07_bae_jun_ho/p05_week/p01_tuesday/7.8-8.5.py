''''''
'''

7장 8절 인자를 N개 받는 함수를 더 적은 인자로 사용 : 파이썬 코드에 콜백함수나 핸들러로 사용할 호출체가 있지만 함수의 인자가 너무 많고 예외가 발생할 경우 functiools.partial()을 사용해 인자 개수를 줄인다.
                                              partial() 함수를 사용하면 함수의 인자에 고정 값을 할당 할 수 있고 호출할 때 넣어야 하는 인자수를 줄일 수 있다.



'''

# 예1.
def spam(a, b, c, d):
    print(a, b, c, d)

from functools import partial
s1 = partial(spam, 1)  # a를 1로 고정
s1(2, 3, 4)
# 1 2 3 4

# 예2.
points = [ (1,2), (3,4), (5,6), (7,8) ]
import math
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2-x1,y2-y1)

pt = (4,3)

points.sort(key=partial(distance, pt))
points
# [ (3,4), (1,2), (5,6), (7,8) ]   # 특정 점(4,3) 으로 부터의 거리에 따라서 정렬. sort() 메소드는 key 인자를 받아서 정렬하는데 인자가 하나인 함수에만 동작하므로 인자가 2개인 distance()에는
                                   # 적합하지 않다. 이를 partial()로 해결한다.

# 예3.
def output_result(result, log=None):
    if log is not None:
        log.debug('Got: %r', result)

def add(x, y):
    return x+y

if __name__ == '__main__':
    import logging
    from multiprocessing import Pool
    from functools import partial

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')
    p=Pool()
    p.apply_async(add, (3,4), callback=partial(output_result, log=log))  # apply_async()로 콜백함수를 지원할 때 partial()을 사용하고 multiprocessing은 하나의 값으로 콜백함수를 호출
    p.close()
    p.join()


'''

7장 9절

- 퍼스트 클래스 함수
퍼스트클래스 함수란 프로그래밍 언어가 함수 (function) 를 first-class citizen으로 취급하는 것을 뜻한다. 
함수 자체를 인자 (argument)로 다른 함수에 전달하거나 다른 함수의 결과값으로 리턴 할 수도 있고, 함수를 변수에 할당하거나 데이터 구조안에 저장할 수 있는 함수다.

"first_class_function.py"라는 이름의 파일을 하나 만들든 후, 다음의 코드를 입력하면

# -*- coding: utf-8 -*-

def square(x):
    return x * x

print square(5)

f = square

print square
print f

파일을 저장한 후, 파일이 저장된 디렉터리에서 터미널이나, 커맨드창을 열고 다음의 명령어로 파이썬 파일을 실행해보면

$ python first_class_function.py
25
<function square at 0x1018dfe60>
<function square at 0x1018dfe60>

위의 코드를 보면 아주 간단한 함수 "square"를 정의하고 호출한다. 
그 다음에 square 함수를 "f"라는 변수에 할당한 후에 square와 f의 값을 출력해보면 메모리 주소값인 0x1018dfe60에 저장된 square 함수 오브젝트가 할당되어 있는 것을 볼 수 있다.


다음과 같이 코드를 수정 하고 저장한 다음 실행하면

# -*- coding: utf-8 -*-

def square(x):
    return x * x

f = square

print f(5)
$ python first_class_function.py
25

f(5) 구문으로 square 함수를 호출한 것을 볼 수 있다. 
프로그래밍 언어가 퍼스트클래스 함수를 지원하면, 금방 해본 것처럼 변수에 함수를 할당할 수 있을뿐만 아니라, 인자로써 다른 함수에 전달하거나, 함수의 리턴값으로도 사용할 수가 있다. 

다음과 같이 코드를 수정 하고 저장한 다음 실행하면

# -*- coding: utf-8 -*-
def square(x):
    return x * x

def my_map(func, arg_list):
    result = []
    for i in arg_list:
        result.append(func(i)) # square 함수 호출, func == square
    return result

num_list = [1, 2, 3, 4, 5]

squares = my_map(square, num_list)

print squares
$ python first_class_function.py
[1, 4, 9, 16, 25]

my_map 함수에 square 함수를 인자로 전달한 후 for 루프안에서 square 함수를 호출한 것을 볼 수 있다. 


다음과 같이 코드를 수정 하고 저장한 다음 실행하면

# -*- coding: utf-8 -*-
def square(x):
    return x * x

num_list = [1, 2, 3, 4, 5]

def simple_square(arg_list):
    result = []
    for i in arg_list:
        result.append(i * i)
    return result

simple_squares = simple_square(num_list)

print simple_squares
$ python first_class_function.py
[1, 4, 9, 16, 25]

간단히 함수 하나만을 실행하고 싶을때는 simple_square와 같은 일반 함수를 사용하여 같은 결과를 낼 수도 있다. 
하지만, 퍼스트클래스 함수를 사용하면 이미 정의된 여러 함수를 간단히 재활용할 수 있다는 장점이 있다. 

다음과 같이 코드를 수정 하고 저장한 다음 실행하면


# -*- coding: utf-8 -*-
def square(x):
    return x * x

def cube(x):
    return x * x * x

def quad(x):
    return x * x * x * x

def my_map(func, arg_list):
    result = []
    for i in arg_list:
        result.append(func(i)) # square 함수 호출, func == square
    return result

num_list = [1, 2, 3, 4, 5]

squares = my_map(square, num_list)
cubes = my_map(cube, num_list)
quads = my_map(quad, num_list)

print squares
print cubes
print quads
$ python first_class_function.py
[1, 4, 9, 16, 25]
[1, 8, 27, 64, 125]
[1, 16, 81, 256, 625]

이미 정의되어 있는 함수 square, cube, quad와 같은 여러개의 함수나 모듈이 있다고 가정했을때 my_map과 같은 wrapper 함수를 하나만 정의하여 기존의 함수나 모듈을 수정할 필요없이 편리하게 쓸 수 있다.

다음과 같이 코드를 수정 하고 저장한 다음 실행하면

first_class_function.py
# -*- coding: utf-8 -*-
def logger(msg):
    
    def log_message(): #1
        print 'Log: ', msg
    
    return log_message

log_hi = logger('Hi')
print log_hi # log_message 오브젝트가 출력됩니다.
log_hi() # "Log: Hi"가 출력됩니다.
$ python first_class_function.py
<function log_message at 0x1029ca140>
Log:  Hi

위의 #1에서 정의된 log_message라는 함수를 logger 함수의 리턴값으로 리턴하여 log_hi라는 변수에 할당한 후 호출한 것을 볼 수 있다.
msg와 같은 함수의 지역변수값은 함수가 호출된 이후에 메모리상에서 사라지므로 다시 참조할 수가 없는데, msg 변수에 할당됐던 'Hi'값이 logger 함수가 종료된 이후에도 참조 됐다. 
이런 log_message와 같은 함수를 "클로저 (closure)"라고 부르며 클로저는 다른 함수의 지역변수를 그 함수가 종료된 이후에도 기억을 할 수가 있다. 

log_message가 정말 기억을 하고 있는지 msg 변수를 지역변수로 가지고 있는 logger 함수를 글로벌 네임스페이스에서 완전히 지운 후, log_message를 호출하여 보면

다음과 같이 코드를 수정 하고 저장한 다음 실행하면

# -*- coding: utf-8 -*-
def logger(msg):
    
    def log_message(): #1
        print 'Log: ', msg
    
    return log_message

log_hi = logger('Hi')
print log_hi # log_message 오브젝트가 출력
log_hi() # "Log: Hi"가 출력됩니다.

del logger # 글로벌 네임스페이스에서 logger 오브젝트를 지움

# logger 오브젝트가 지워진 것을 확인
try:
    print logger
except NameError:
    print 'NameError: logger는 존재하지 않습니다.'

log_hi() # logger가 지워진 뒤에도 Log: Hi"가 출력
$ python first_class_function.py
<function log_message at 0x1007ca1b8>
Log:  Hi
logger는 존재하지 않습니다.
Log:  Hi

logger가 지워진 뒤에도 log_hi()를 실행하여 log_message가 호출된 것을 볼 수 있다.

logger 함수를 완전히 삭제한 이후에도 log_message 함수는 'Hi'를 기억하고 있는 것을 확인했다. 

다음과 같이 코드를 수정 하고 저장한 다음 실행하면

# -*- coding: utf-8 -*-
# 단순한 일반 함수
def simple_html_tag(tag, msg):
    print '<{0}>{1}<{0}>'.format(tag, msg)
    
simple_html_tag('h1', '심플 헤딩 타이틀')

print '-'*30

# 함수를 리턴하는 함수
def html_tag(tag):
    
    def wrap_text(msg):
        print '<{0}>{1}<{0}>'.format(tag, msg)
        
    return wrap_text

print_h1 = html_tag('h1') #1
print print_h1 #2
print_h1('첫 번째 헤딩 타이틀') #3
print_h1('두 번째 헤딩 타이틀') #4

print_p = html_tag('p')
print_p('이것은 패러그래프 입니다.')
$ python first_class_function.py
<h1>심플 헤딩 타이틀<h1>
------------------------------
<function wrap_text at 0x1007dff50>
<h1>첫 번째 헤딩 타이틀<h1>
<h1>두 번째 헤딩 타이틀<h1>
<p>이것은 패러그래프 입니다.<p>

#1에서 html_tag 함수를 print_h1 변수에 할당한 후, #2에서 변수의 값을 출력하니 wrap_text 함수 오브제트가 할당되어 있는 것을 볼 수 있다. 
그리고 #3과 #4에서 간단히 문자열을 전달하여 wrap_text 함수를 호출한 것을 볼 수 있다. 

html_tag와 같은 higher-order 함수등을 이해해야 클로저 (closure), 데코레이터 (decorator) 또는 제너레이터 (generator) 등에 대해서 쉽게 이해할 수가 있다. 



- 클로져

프로그래밍 언어에서의 클로저란 퍼스트클래스 함수를 지원하는 언어의 네임 바인딩 기술이다. 
클로저는 어떤 함수를 함수 자신이 가지고 있는 환경과 함께 저장한 레코드이다.
또한 함수가 가진 프리변수(free variable)를 클로저가 만들어지는 당시의 값과 레퍼런스에 맵핑하여 주는 역할을 한다. 
클로저는 일반 함수와는 다르게, 자신의 영역 밖에서 호출된 함수의 변수값과 레퍼런스를 복사하고 저장한 뒤, 이 캡처한 값들에 액세스할 수 있게 도와준다.

프리변수(free variable)란 파이썬에서 프리변수는 코드블럭안에서 사용은 되었지만, 그 코드블럭안에서 정의되지 않은 변수를 뜻한다.

원하는 디렉터리에 closure.py라는 이름의 파일을 만들고 다음의 코드를 저장.

# -*- coding: utf-8 -*-

def outer_func(): #1
    message = 'Hi' #3

    def inner_func(): #4
        print message #6 

    return inner_func() #5

outer_func() #2

$ python closure.py
Hi

프로그램을 실행하니 "Hi"라는 문자가 출력되었다. 간단한 구문이지만 클로저를 설명하기 위해 "Hi"가 출력되기까지의 프로세스를 하나씩 확인해 보면

 #1에서 정의된 함수 outer_func를 #2에서 호출을 합니다. 물론 outer_func는 어떤 인수도 받지 않는다.
 #3에서 outer_func가 실행된 후, 가장 먼저 하는 것은 messge 라는 변수에 'Hi'라는 문자열을 할당한다.
 #4에서 inner_func를 정의하고 #5번에서 inner_func를 호출하며 동시에 리턴한다.
 #6에서 message 변수를 참조하여 출력한다. 여기서 message는 inner_func 안에서 정의되지는 않았지만, inner_func 안에서 사용되기 때문에 프리변수라고 부른다.
 "Hi"가 출력되기까지의 일련의 프로세스는 위와 같다.

#5의 코드를 살짝 수정하고 실행하면

# -*- coding: utf-8 -*-

def outer_func(): #1
    message = 'Hi' #3

    def inner_func(): #4
        print message #6 

    return inner_func #5 <-- ()를 지움

outer_func() #2
$ python closure.py

아무것도 출력이 안되는 것을 볼 수 있다. #5에서 outer_func이 리턴할 때 inner_func 함수를 실행하지 않고, 함수 오브젝트를 리턴하였기 때문이다.

그럼 이번에는 outer_func이 리턴하는 inner_func 오브젝트를 변수에 할당하여 보면

#2의 코드를 수정하고 실행하여 보면

# -*- coding: utf-8 -*-

def outer_func(): #1
    message = 'Hi' #3

    def inner_func(): #4
        print message #6 

    return inner_func #5

my_func = outer_func() #2 <-- 리턴값인 inner_func를 변수에 할당
$ python closure.py

물론 이번에도 출력되는 값은 없다.

이번에는 my_func 변수에 정말 inner_func 함수가 할당되어 있는지 확인한다. #7행을 추가하고 실행하여 본다.

# -*- coding: utf-8 -*-

def outer_func(): #1
    message = 'Hi' #3

    def inner_func(): #4
        print message #6

    return inner_func #5

my_func = outer_func() #2

print my_func #7 <-- 추가
$ python closure.py
<function inner_func at 0x1020dfed8>

inner_func 함수가 할당되어 있다.

# -*- coding: utf-8 -*-

def outer_func(): #1
    message = 'Hi' #3

    def inner_func(): #4
        print message #6

    return inner_func #5

my_func = outer_func() #2

my_func() #7
my_func() #8
my_func() #9
$ python closure.py
Hi
Hi
Hi

my_func()를 3번 실행하여 "Hi"를 3번 출력했다. 

outer_func는 분명히 #2에서 호출된 후, 종료되었다. 

그런데 #7, #8, #9에서 호출된 my_func(*여기서 my_func는 inner_func와 같다) 함수가 outer_func 함수의 로컬변수인 message를 참조했다.

# -*- coding: utf-8 -*-

def outer_func():  #1
    message = 'Hi'  #3

    def inner_func():  #4
        print message  #6

    return inner_func  #5

my_func = outer_func()  #2

print my_func  #7
print
print dir(my_func)  #8
print
print type(my_func.__closure__) #9
print
print my_func.__closure__  #10
print
print my_func.__closure__[0]  #11
print
print dir(my_func.__closure__[0])  #12
print
print my_func.__closure__[0].cell_contents  #13
$ python closure.py
<function inner_func at 0x1019dfed8>

['__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__doc__', '__format__', '__get__', '__getattribute__', '__globals__', '__hash__', '__init__', '__module__', '__name__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'func_closure', 'func_code', 'func_defaults', 'func_dict', 'func_doc', 'func_globals', 'func_name']

<type 'tuple'>

(<cell at 0x1019e14b0: str object at 0x1019ea788>,)

<cell at 0x1019e14b0: str object at 0x1019ea788>

['__class__', '__cmp__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'cell_contents']

Hi

출력된 결과를 하나씩 확인하면

#7 결과: my_func 변수에 inner_func 함수 오브젝트가 할당되어 있다.

#8 결과: 클로저가 도데체 어디에 데이터를 숨기는지 dir() 명령어를 이용해 my_func의 네임스페이스를 확인하면 __closure__ 라는 속성이 숨어 있다.

#9 결과: __closure__는 튜플이다.

#10 결과: 튜플안에 뭐가 들어 있는지 확인하면 아이템이 하나 들어있다.

#11 결과: 튜플안에 첫 번째 아이템은 "cell"이라는 문자열 오브젝트.

#12 결과: cell 오브젝트는 "cell_contents"라는 속성이 존재.

#13 결과: cell_contents에는 'Hi'가 들어 있다. 


클로저의 주요기능은 따라서 (함수를) 정의할 떄의 환경을 기억한다는 것이다. 인자값을 기억하고 추후 호출에 사용할 수 있다.





'''

# 예4.
def logger(msg):
    def log_message():  # 1
        print('Log: ', msg)

    return log_message


log_hi = logger('Hi')
print(log_hi)
# <function logger.<locals>.log_message at 0x0000000004A24620>      #log_message 오브젝트가 출력됩니다.
log_hi()  # "Log: Hi"가 출력됩니다.

# 예5.
from urllib.request import urlopen
class UrlTemplate:
    def __init__(self, template):
        self.template = template
    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

# 위 클래스를 간단한 함수로 바꿀 수 있다.
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# 사용법
yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM, AAPL, FB', fields='sl1clv'):
    print(line.decode('utf-8'))

'''

7장 10절 콜백함수에 추가적 상태 넣기 : 콜백 함수를 사용하는 코드를 작성중인 경우 콜백 함수에 추가 상태를 넣고 내부 호출에 사용할 때 아래 레시피를 사용한다.

- 콜백함수 : 콜백은 함수를 직접 호출하지 않고 다른 함수가 대신 호출하게 하는 것.
            콜백함수는 콜백 실행으로 이끄는 초기 요청 코드와 콜백 함수가 끊어지기 때문에 결과적으로 요청한 곳과 처리한 곳을 찾지 못한다. 
            콜백을 여러 단계에 거쳐서 사용하는 경우 콜백 함수가 여러 단계에 걸쳐 실행을 계속하도록 만들기 위해 관련 상태를 저장하고 불러올지 정해 두어야 한다.
            이 방식엔 두가지 방법이 있는데 인스턴스에 바운드 메소드를 사용해서 상태를 저장하거나 클로저에 저장해두는 방법이 있다.
            클로져를 사용하는 경우 수정 가능한 변수를 조심해서 사용해야 하는데 아래 예제에서 nonlocal 선언은 해당 변수가 콜백 내부에서 수정됨을 의미하고 이 것이 없으면 에러가 발생한다.
            이를 방지하기 위한 방법이 코루틴을 사용하는 것이다. 코루틴은 하나의 함수로만 이루어져 있는데다 nonlocal 선언을 하지 않아도 되기 때문에 자유롭게 변수를 수정할 수 있지만 잠재적으로 
            파이썬 기능으로 받아들여지지 않는 경우가 있고 사용전에 next()를 호출해야만 하는 점이 있다.


- 바운드메소드, 언바운드메소드

기본적으로 클래스의 메소드는 클래스객체의 이름공간에 선언된다. 
이러한 이유로 인하여 인스턴스객체가 클래스의 메소드를 호출하면, 네임스페이스에 대한 정보를 호출하는 메소드에게 넘겨줘야 한다. 
메소드 호출시 암묵적으로 첫 인자로 인스턴스 객체를 넘기는 호출방식을 바운드메서드(Bound Method)호출이라 한다. 
이 때에는 메소드 정의시 첫 인자가 인스턴스 객체임을 선언하나, 호출시에는 자동으로 반영되기에 명시적으로 입력하지 않는다. 
반면에 메소드 호출시 명시적으로 첫 인자로 인스턴스 객체를 넘기는 호출방식을 언바운드메서드(Unbound Method) 호출이라 한다. 
이 때에는 클래스 객체를 통하여 메소드를 호출하며, 첫 인자로 인스턴스 객체를 입력하여야 한다.

p1.print() #바운드메서드호출
person.print(p1) #언바운드메서드호출

- 코루틴

코루틴은 제너레이터를 확장하는 방법으로 구현한다. 제너레이터 코루틴을 시작하는 데 드는 비용은 함수 호출이다.
코루틴은 제너레이터를 소비하는 코드에서 send 함수를 사용하여 역으로 제너레이터 함수의 각 yield 표현식에 값을 보낼 수 있게 하는 방법으로 동작한다. 
제너레이터 함수는 send 함수로 보낸 값을 대응하는 yield 표현식의 결과로 받는다.

def my_coroutine():
    while True:
        received = yield
        print('Received: ', received)
it = my_coroutine()
next(it) # 코루틴을 준비함
it.send('First')
it.send('Second')

# 결과
# ('Received: ', 'First')
# ('Received: ', 'Second')

제너레이터가 첫 번째 yield 표현식으로 전진해서 첫 번째 send의 값을 받을 수 있게 하려면 먼저 next를 호출해야 한다. 
yield와 send의 조합은 제너레이터가 외부 입력에 반응하여 다음 번에 다른 값을 얻게 하는 표준 방법이다. 
예를 들어 지금까지 보낸 값 중에서 최솟값을 넘겨주는 제너레이터 코루틴을 구현한다고 가정하면 여기서 넘길 값이 없는 yield로 외부에서 보낸 초기 최솟값을 받아서 코루틴을 준비한다. 
이후 제너레이터는 반복적으로 다음 값을 받으면서 새 최솟값을 넘겨준다.

def minimize():
    current = yield
    while True:
        value = yield current
        current = min(value, current)
 
# 제너레이터를 소비하는 코드는 한 번에 한 단계씩 실행하여 각 입력을 받은 이후의 최솟값을 출력
it = minimize()
next(it) # 제너레이터를 준비함
print(it.send(10))
print(it.send(4))
print(it.send(22))
print(it.send(-1))


# 결과
# 10
# 4
# 4
# -1

제너레이터 함수는 send를 새로 호출할 때마다 전진하면서 계속 실행하는 것처럼 보입니다. 스레드와 마찬가지로 코루틴은 주변 환경에서 받은 입력을 소비하여 결과를 만들어낼 수 있는 독립적인 함수다. 
둘의 차이는 코루틴이 제너레이터 함수의 각 yield 표현식에서 멈췄다가 외부에서 send를 호출할 때마다 다시 시작한다는 점입니다. 이게 바로 코루틴이 동작하는 메커니즘이다. 
이 동작 덕분에 제너레이터를 소비하는 코드에서 코루틴의 각 yield 표현식 이후에 원하는 처리를 할 수 있다. 
제너레이터를 소비하는 코드는 제너레이터의 출력값으로 다른 함수를 호출하고 자료 구조를 수정할 수 있다. 
가장 중요한 건 다른 제너레이터 함수들을 yield 표현식 이전까지 전진시킬 수 있다는 점이다. 
많은 별개의 제너레이터를 똑같은 방식으로 실행하면, 이 제너레이터들이 파이썬 스레드의 병행 동작을 흉내 내며 동시에 실행하는 것처럼 보인다.

요약

코루틴은 함수 수만 개를 마치 동시에 실행하는 것처럼 실행하는 효과적인 방법을 제공
제너레이터 안에서 yield 표현식의 값은 외부 코드에서 제너레이터의 send 메서드에 전달한 값
코루틴은 프로그램의 핵심 로직을 주변 환경과 상호 작용하는 코드로부터 분리할 수 있는 강력한 도구




'''

# 예6.
def apply_async(func, args, *, callback):
    result = func(*args)
    callback(result)

def print_result(result):
    print('Got: ', result)
def add(x, y):
    return x+y

apply_async(add, (2, 3), callback=print_result)
# Got: 5

# 예7.
class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))

# 클래스를 인스턴스화 하고 바운스 메소드 handler를 콜백으로 사용
r = ResultHandler()
apply_async(add, (2, 3), callback=r.handler)
# [1] Got: 5
apply_async(add, ('hello', 'world'), callback=r.handler)
# [2] Got: helloworld

# 클로져를 사용
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler

handler = make_handler()
apply_async(add, (2, 3), callback=handler)
# [1] Got: 5
apply_async(add, ('hello', 'world'), callback=handler)
# [2] Got: helloworld

# 코루틴 사용 : 코루틴은 콜백함수로 send() 메소드를 사용해야만 한다.
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))

handler = make_handler()
next(handler)   # advance to the yield
apply_async(add, (2, 3), callback=handler.send)
# [1] Got: 5
apply_async(add, ('hello', 'world'), callback=handler.send)
# [2] Got: helloworld

'''

7장 11절 인라인 콜백 함수 : 콜백 함수를 사용하는데 크기가 작은 함수를 너무 많이 만들게 되면 안되므로 코드가 정상적인 절차적 단계를 거치도록 하고 싶은 경우 제너레이터와 코루틴을 함수 내부에 넣는다.



'''

# 예8.
def apply_async(func, args, *, callback):
    # 결과 계산
    result = func(*args)
    # 결과 값으로 콜백함수 호출
    callback(result)

# 예9.
from queue import Queue
from functools import wraps

class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args

def inlined_async(func):                # 데코레이터 함수
    @wraps(func)                        #
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a=f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break
    return wrapper

def add(x, y):
    return x+y

@inlined_async
def test():
    r = yield Async(add, (2, 3))                      # 데코레이터가 yield 구문을 통해 제너레이터 함수를 하나씩 돈다. 이를 위해 결과 큐를 만들고 최소로 None을 입력한다.
    print(r)
    r = yield Async(add, ('hello', 'world'))
    print(r)
    for n in range(10):                               # 그 다음 루프문을 통해 결과를 큐에서 꺼낸 다음 제너레이터로 보내고 다음 생성으로 넘어간 다음 Async 인스턴스를 받는다.
        r = yield Async(add, (n, n))
        print(r)
    print('Goodbye')

test()

# 5
# helloworld
# 0
# 2
# 4
# 6
# 8
# 10
# 12
# 14
# 16
# 18
# Goodbye   # 특별 데코레이터와 yield를 제외하면 어떤 콜백함수도 나오지 않는다. yield는 제너레이터가 함수 값을 분출하고 연기하도록 한다.
            # 이어서 __next()__ 나 send() 메소드를 사용하면 다시 실행된다.


'''

7장 12절 클로저 내부에서 정의한 변수에 접근 : 클로저를 확장해서 내부 변수에 접근하고 수정하고 싶은 경우 일반적으로 클로져 내부변수는 외부와 단절되어있지만 접근함수를 만들고 클로저에 함수속성을 붙이면
                                        접근이 가능해진다. nonlocal 선언으로 내부 변수를 수정하는 함수를 작성한 다음 접근 메소드를 클로져 함수에 붙여 마치 함수가 인스턴스 메소드인 것 처럼 
                                        동작하게 만들면 된다. 클로져를 마치 클래스의 인스턴스 인 것 처럼 동작하게 만드는 것이다. 내부함수를 인스턴스 딕셔너리에 복사하고 반환하면 된다.



'''


# 예9.
def sample():
    n = 0
    # 클로져 함수
    def func():
        print('n= ', n)

    # n에 대한 접근 메소드
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    func.get_n = get_n
    func.set_n = set_n
    return func

f = sample()
f()
# n= 0
f.set_n(10)
f()
# n= 10
f.get_n()
# 10

# 예10.
import sys
class ClosureInstance:
    def __init__(self, locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals

        # 인스턴스 딕셔너리를 호출체로 갱신
        self.__dict__.update((key, value) for key, value in locals.items() if callable(value))

    # 특별 메소드 리다이렉트(redirect)
    def __len__(self):
        return self.__dict__['__len__']()

def Stack():
    items = []

    def push(item):
        items.append(item)

    def pop():
        return items.pop()

    def __len__():
        return len(items)

    return ClosureInstance()


'''

8장 1절 인스턴스의 문자열 표현식 변형 : 인스턴스를 출력하거나 볼 떄 생성되는 결과물을 좀 더 보기 좋게 바꾸고 싶은 경우 인스턴스의 문자열 표현식을 바꾸려면 __str__()과 __repr__() 메소드를 정의한다.

- __repr__() : 인스턴스의 코드 표현식을 반환하고 일반적으로 인스턴스를 재생성 할 때 입력한다. 내장 repr() 함수는 인터프리터에서 값을 조사할 때와 마찬가지로 텍스트를 반환한다.
- __str__() 메소드는 인스턴스를 문자열로 변환하고 str()과 print() 함수가 출력하는 결과를 가진다.


'''

# 예11.
