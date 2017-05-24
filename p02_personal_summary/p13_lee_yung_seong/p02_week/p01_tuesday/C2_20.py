#문제 바이트 문자열에 텍스트 연산 수행
#해결 바이트 문자열도 텍스트 문자열과 마찬가지로 대부분의 연산을 내장
data = b'Hello World'
data[0:5]
data.startswith(b'Hello')
data.split()
data.replace(b'Hello',b'Hello Cruel')
data = bytearray(b'Hello World')
data[0:5]
data.startswith(b'Hello')
data.split()
bytearray(b'Hello Cruel World')
#바이트 문장 패턴 매칭에 정규 표현식을 적용할 수 있다. 하지만 패턴 자체도 바이트로 나타내야 한다.
data = b'FOO:BAR,SPAM'
import re
re.split('[:,]',data)
#토론 : 대개의 ㄱㅇ우 텍스트 문장ㄹ에 있는 연산 기능은 바이트 문장ㄹ에도 내장 되어 있다. 하지만 주의해야할 차이점이 있다. 첫째로 바이트 문자열에 인덱스를 사용하면 개별 문자가 아니라 정수를 가르킴.
a = 'Hello world'
a[0]
b = b"hello world"
b[0]
#이 차이로 인해 캐릭터 기반의 데이터를 바이트 기준으로 접근하는 프로그램에 영향줌.
#둘째로 바이트 문자열은 보기 좋은 표현식을 지원하지 않으며 텍스트 문자열로 변환하지 않으면 깔끔하게 출력 못함.
s=b'Hello World'
print(s)
print(s.decode('ascii'))
#바이트 문자열은 formatting을 제공하지 않음
b'%10s %10d %10.2f' % (b'ACME',100,490.1)
b'{} {} {}'.format(b'ACME', 100, 490.1)
#바이트 문자열에 서식화를 적용하고 싶으면 일반 텍스트 문자열과 인코딩을 사용해야함.
'{:10s} {:10d} {:10.2f}'.format('ACME',100,490.1).encode('ascii')
#바이트 문장ㄹ을 사용하면 특정 연산의 문법에 영향을 주기도 한다. 특히 파일 시스템에 영향이 많음.
#예를들어 파일이름을 텍스트문자열이 아니라 바이트문자열로 제공하면 대게 파일 이름 인코딩,디코딩을 사용못함.
with open('jalape\xf10.txt','w') as f:
    f.write('spicy')

import os
os.listdir('.')
#디렉터리 이름에 바이트 문자열을 사용하면 겨로가 파일 이름이 디코딩 되지 않은 바이트로 반환된다. 디렉터리 리스트의 파일 이름은 raw UTF-8 인코딩을 포함한다.
#텍스트보다 바이트로 데이터를 다루는 것이 빠른것은 사실. 하지만 코드가 지저분해지고 이해하기 어려움.
#바이트 문자열을 파이썬의 다른부분과 사용했을 때 문제가 발생할 소지가 많고. 올바른 동작을 위해 인코딩/디코딩을 일일이 수작업해야함.
#그래서 텍스트 작업이 필요하면 텍스트 문자열을 쓰자.