##########################################################################################################
# 8.3] 객체의 콘텍스트 관리 프로토콜 지원
#   * 객체가 콘텍스트 관리 프로토콜(with 구문)을 지원하게 만들고 싶다.
#       : __enter__()와 __exit__() 메소드 구현
#
#   * 콘텍스트 매니저를 작성할 때 중요한 원리는, with 구문을 사용하여 정의된 블럭을 감싸는 코드를 작성한다는 것이다.
#     처음으로 with를 만나면 __enter__() 메소드가 호출되며, 만약 반환값이 있다면 as로 나타낸 변수에 위치시킨다.
#     그 뒤 with의 내부 명령어를 실행하고 마지막으로 __exit__() 메소드로 소거 작업을 한다.
#     이 흐름은 with 문 내부에서 어떤 일이 발생하든 동일하게 일어난다.
#     이는 예외가 발생할 때도 마찬가지로, 사실 __exit__() 메소드는 예외 정보를 고르거나 아무 일도 하지 않고
#     None을 반환하며 무시하는 방식을 선택할 수도 있다. 만약 exit가 True를 반환한다면 예외를 없애고
#     아무 일도 없었던 것처럼 with 블록 다음의 프로그램을 계속해서 실행할 것이다.
#
#   * LazyConnection 클래스는 연결을 위한 팩토리 역할을 한다.
#     enter가 실행될 때마다 새로운 연결을 만들고 스택에 추가한다.
#     exit 메소드는 단순히 스택에서 마지막 연결을 꺼내고 닫는다.
#     사소한 문제지만 이로 인해 중첩 with 구문으로 연결을 여러 개 생성할 수 있다.
#
##########################################################################################################
from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None

from functools import partial

conn = LazyConnection(('www.python.org', 80))
# 연결 종료
with conn as s:
    # with절 시작 시 conn.__enter__() 자동 실행 : 연결
    s.send(b'Get \index.html http/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # with절 종료 시 conn.__exit__() 자동 실행 : 연결 종료

