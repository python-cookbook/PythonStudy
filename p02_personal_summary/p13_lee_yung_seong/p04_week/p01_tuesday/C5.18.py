#기존 파일 디스크립터를 파일 객체로 감싸기
#문제
#운영체제 상에 이미 열려있는 IO채널에 일치하는 정수형 파일 디스크립터를 가지고 있고(file, pipe, socket)등 이를 상위 레벨 파이썬파일 객체로 감싸고 싶다.
#해결
#파일 디스크립터는 운영체제가 할당한 정수형 핸들로 시스템 IO채널 등을 참조하기 위한 목적으로써 일반 파일과는 다르다. 파일 디스크립터가 있을 때 open()함수를 사용해
#파이썬 파일 객체로 감쌀 수 있다. 하지만 이때 파일 이름 대신 정수형 파일 디스크립터를 먼저 전달해야 한다.
#하위 레벨 파일 디스크립터 열기
import os
fd = os.open('somefile.txt',os.O_WRONLY | os.O_CREAT)
f= open(fd,'wt')
f.write('hello world\n')
f.close()
#상위 레벨 파일 객체가 닫혔거나 파괴 되었다면 그 하단 파일 디스크립터 역시 닫힌다.
#이런 동작을 원하지 않는다면 closefd=False인자를 open()에 전달해야한다.
#파일 객체를 생성하지만, 사용이 끝났을 때 fd를 닫지 않는다.
f=open(fd,'wt',closefd=False)
#토론 UNIX 시스템 상에서 이 기술을 사용하면 기존의 IO채널 (pipe,socket)을 감싸 파일과 같은 인터페이스로 사용할 수 있는 쉬운 길이 열린다.
#소켓과 관련 있는 다음 예를 보자.\
from socket import socket, AF_INET, SOCK_STREAM
