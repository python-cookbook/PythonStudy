#16진수 인코딩, 디코딩
#문제
#문자열로 된 16진수를 바이트 문자열로 디코딩하거나 바이트 문자열을 16진법으로 인코딩해야 한다.
#해결
#문자열을 16진수로 인코딩하거나 디코딩할면 binascii
#최초바이트문자열
s=b'hello'
#16진법인코딩
import binascii
h=binascii.b2a_hex(s)
h
#바이트로 인코딩
binascii.a2b_hex(h)
# base64 모듈에도 유사한 기능이 있다.
import base64
h = base64.b16encode(s)
h
base64.b16decode(h)
#토론
#두 기술의 차이점은 대소문자 구분에 있음. base64는 대뭍자에만 동작하지만 binascii는 대소문자 구분하지 않음
#또한 인코딩 함수가 만들 출력물은 언제나 바이트 문자열. 반드시 유니코드를 사용해야 한담 디코딩 과정을 추가해야 한다.
h=base64.b16encode(s)
h
print(h.decode('ascii'))
#16진수 디코딩할 때  b16decode()와 a2b_hex() 함수는 바이트 혹은 유니코드 문자열을 받는다.
#이 문자열에는 반드시 ascii로 인코딩한 16진수가 포함되어 있어야 한다.
