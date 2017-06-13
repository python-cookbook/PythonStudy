##객체의 콘텍스트 관리 프로토콜 지원
#문제
#객체가 콘텍스트 관리 프로토콜을 지원하게 만들고 싶다
#해결
#객체와 with 구문을 함께 사용할 수 있게 만들려면, __enter__()와 __exit__() 메소드를 구현해야 한다. 예를 들어 네트워크 연결을 제공하는 다음 클래스를 보자
from socket import socket, AF_INET, SOCK_STREAM
class LazyConnection:
    def __init__(self,address,family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = SOCK_STREAM
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family,self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self,exc_ty,exc_val,tb):
        self.sock.close()
        self.sock = None
#이 클래스의 주요 기능은 네트워크 연결을 표현하는 것이지만 처음엔 아무런 작업을 하지 않음.
#그 대신 연결은 with 구문에서 이루어짐.
from functools import partial
conn = LazyConnection(('www.python.org',80))
#연결종료
with conn as s:
    # conn.enter 실행 : 연결
    s.send(b'GET / index.html HTTP/1.0\r\n')
    s.send(b'HOST : www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8129),b''))
    # conn.__exit__() 실행 : 연결종료

#토론
#콘텍스트 매니저를 작성할 때 중요한 원리는 with 구문을 사용하여 정의된 블럭을 감싸는 코드를 작성한다는 것이다. 처음으로 with를 만나면 __enter__() 메소드가 호출된다.
#__enter__()의 반환 값(있다면)은 as로 나타낸 변수에 위치시킨다. 그 후에 with의 내부 명령어를 실행하고 마지막으로 exit 메소드로 소거 작업.
#이번 레시피에서 with문을 여러번 써서 중첩된 연결을 lazyconnection 클래스가 허용하는지 여부가 미묘한 측면.
#앞에 나온 대로 한 번에 하나의 소켓 연결만 허용되고 소켓을 사용 중에 중복된 with 문이 나타나면 예외가 발생한다.
from socket import socket, AF_INET, SOCK_STREAM
class LazyConnection:
    def __init__(self,address,family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.connection = []
    def __enter__(self):
        sock = socket(self.family,self.type)
        sock.connect(self.address)
        self.connections.append(sock)
        return sock
    def __exit__(self,exc_ty,exc_val,tb):
        self.connections.pop().close()

#사용예제
from functools import partial
conn = LazyConnection(('www.python.org',80))

#두번째 버전에서 lazyconnection 클래스는 연결을 위한 팩토리 역할을 한다. 내부적으로 스택을 위해 리스트르 ㄹ사용했다.
#엔터 메소드가 실행될때마다 새로운 연결을 만들고 스택에 추가한다. exit메소드는 단순히 스택에서 마지막 연결을 꺼내고 닫는다.