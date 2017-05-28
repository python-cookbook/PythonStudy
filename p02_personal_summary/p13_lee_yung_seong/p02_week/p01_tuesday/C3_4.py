#문제 : 숫자를 2진수,8진수, 16진수로 출력해야 한다.
#해결 정수를 2진수, 8진수, 16진수 문자열로 변환하려면 bin(), oct(), hex()를 사용한다.
x = 1234
bin(x)
oct(x)
hex(x)
#앞에 0x 0b 0o가 붙는 것이 싫으면 format
format(x,'b')
format(x,'o')
format(x,'x')
#정수형은 부호가 있는 숫자이므로, 음수를 사용하면 결과물에도 부호가 붙는다.
x = -1234
format(x,'b')
format(x,'x')
#부호가 없는 값을 사용하려면 최대값을 더해서 비트 길이를 설정해야 함. 예를 들어 32비트 값으 ㄹ보여주려면 다음과 같이 한다.
x = -1234
format(2**32+x,'b')
format(2**32+x,'x')
#다른 진법의 숫자를 정수형으로 변환하려면 int() 함수에 적절한 진수를 전달한다.
int('4d2',16)
int('10011010010',2)
#토론 : 2진수, 8진수, 16진수 변환은 간단히 해결 가능.
#8진법을 사용할 때에는 다른 언어와 약간의 차이가 있으니 주의해야함.
import os
os.chmod('script.py',0o755)
#8진법 값 앞에는 다음과 같이 0o를 붙여주어야 함.