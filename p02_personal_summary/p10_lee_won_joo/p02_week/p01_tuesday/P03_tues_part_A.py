"""
                                                ▶ 3.1 반올림 ◀ 
♣  문제 : 부동 소수점 값을 10진수로 반올림하고 싶다.
↘  해결 : 간단한 반올림은 내장 함수인 round(value, ndigits)함수를 사용하고 싶다.
         자세한 소수점 계산    ==> decimal모듈
 """
print('########################################## 3.1 반올림 #####################################')


a = round(1.23,1)
b = round(1.27,1)
c = round(-1.27,1)
d = round(1.25361,3)
print(a,b,c,d)

a = 1627731
print(round(a,-1))
print(round(a,-2))
print(round(a,-3))

print('반올림과 서식화 헷갈려하지 말기')

x = 1.23456
print(format(x, '0.2f'))
print(format(x,'0.3f'))
print('value is {:0.3f}'.format(x))
#value is 1.235

"""
                                                ▶ 3.2 정확한 10진수 계산 ◀ 
♣  문제 : 정확히10진수 계산해야하며, 부동소숫점 사용 시, 작은오류 피하기
↘  해결 : 10진수는 아주 작은계산 하더라도 오류가 발생한다.. 따라서 Decimal모듈사용추천
 """
print('########################################## 3.2 정확한 10진수 계산 #####################################')

print('정확도 문제를 수정하기 위해, 반올림하는건 지양해야 함')
a = 2.1
b= 4.2
c=a+b
print(c)
print(round(c,2))

# 엄청 작은 소숫자 반올림이 문제가 없다면 보통 넘어가지만, 금융권은 절대 그러면 안됨
# decimal모듈 추천

print('부동 소숫점 값에는 10진수를 아주 정확히 표현하지 못한다는 문제있음. ')

a = 4.2
b = 2.1
print(a+b)  # 6.300000000000001
print(a+b == 6.3)  #False


print('위 오류를 피하고 싶다면, decimal사용')

from decimal import Decimal, localcontext
a = Decimal('1.3')
print(type(a))
b = Decimal('1.7')
print(a+b)
print(a+b == Decimal('3.0'))

# decimal객체는 숫자를 문자열로 표현해서, 어색할 수 있으나, 정확히 수행한다.
# 반올림의 자릿수와 같은 계산적 측면을 조절할 수 있는게 장점

print(a/b)
with localcontext() as ctx:
    ctx.prec = 3  #소숫점 3자리
    print(a/b)
    ctx.prec = 50
    print(a/b)


"""
         float   decimal
실행속도         >

"""




"""
                                                ▶ 3.3 출력을 위한 숫자 서식화 ◀ 
♣  문제 : 출력을 위해, 자릿수, 정렬, 천 단위 구분 등 숫자를 서식화하고 싶다.
↘  해결 : 출력을 위해 숫자를 서식화하려면, 내장 함수인 FORMAT을 사용한다.


g = 'The value is {:0,.1f}'.format(x)
print(g)         #The value is 1,234.6


g = format(x, '0.1f')
h = format(-x, '0.2f')
print(g,h)        #   1234.6         -1234.57
 """
print('########################################## 3.3 출력을 위한 숫자 서식화 #####################################')


x = 1234.56789

a=format(x,'0.2f')      #소수점 둘째 자리 정확도
b=format(x,'>10.1f')   # 소숫점 한자리 정확도로 문자 10개 기준 오른쪽에서 정렬
c=format(x,'<10.1f')   # 왼쪽정렬
d=format(x,'^10.1f')   # 우측정렬
e=format(x,',')        # 천 단위 구분자 넣기
f = format(x,'0,.1f')  #

print(a)
print(b,c,d)
print(e)
print(f)


####### 지수 표현법

expo = format(x,'e')
d = format(x,'0.2E')

print(expo)
print(d)

#너비와 자릿수를 나타내는 일반적인 형식은 '[<>^]     ?        너비   [,]   ?   (.자릿수)   ?      '         이다.
#                                         '[정렬]  (선택)     (int)       (선택)  (int)    (선택)'
#위 너비오 자릿수를 나타내는 형식은 format문에서도 동일하게 적용된다.
g = 'The value is {:0,.1f}'.format(x)
print(g)



#출력을 위한 숫자 서식화는 대개 간단하다. 앞에 소개한 기술은 부동 소수점 값과 decimal모듈의 숫자에 모두 잘 동작한다.
#자릿수를 제한하면 round() 함수와 동일한 규칙으로 반올림된다.
print(x)
g = format(x, '0.1f')
h = format(-x, '0.2f')
print(g,h)        #   1234.6         -1234.57
## 위 결과를 보면, 첫째자리, 둘째자리 반올림하고 있는 모습..
##그러면 따로 round치거나 하지말고, format문으로 스탠다드 잡아놓고, 위처럼 자릿수 제한둬놓으면 알아서 반올림되고 좋겠네
## 물론 반올림이 되면 안되는 그런 세밀한 값이 요구되거나 그런다면, 하지 말아야겠다.


# 천 단위 구분자는 지역 표기법을 따르지 않는다. 이를 염두에둔다면 locale모듈의 함수를 사용해야 한다.
# 문자열의 translate() 메소드를 사용하면 구분자 문자를 변경할 수도 있다.

swap_separators = {ord('.'):',', ord(','):'.'}
c = format(x, ',').translate(swap_separators)
print(c)

###### 많은 파이썬 코드에서 숫자를 % 연산자로 서식화한다.
h = '%0.2f' % x
print(h)
g = '%10.1f' % x
i = '%-10.1f' % x
print(g, i)

# 위 방식도 나쁘지 않은데, 천 단위 구분자는 %연산자가 제공하지 않는다.


## 내 결론은 format형식으로 다음과 같이 정렬과 너비와, 천 단위 구분자와 반올림 기능을 넣자!
#######


"""
                                                ▶ 3.4 2진수, 8진수, 16진수 작업 ◀ 
♣  문제 : 출력을 위해, 자릿수, 정렬, 천 단위 구분 등 숫자를 서식화하고 싶다.
↘  해결 : 정수를 2 / 8 / 16 진수 문자열로 변환하려면 bin(), oct(), hex()를 사용한다.
            
 """
print('########################################## 3.4 2진수 8진수 , 16진수작업 #####################################')


x = 1234

#2진수
bin(x)
#8진수
oct(x)
#16진수
hex(x)
print(bin(x),oct(x),hex(x))   # 0b10011010010,       0o2322,        0x4d2

#앞에 0b,, 0o 이런 접두사 붙는거 싫으면 format활용하기
a = format(x, 'b')
b = format(x, 'o')
c = format(x, 'x')
print(a,b,c)         #10011010010 2322 4d2




#정수형은 부호가 있는 숫자이므로, 음수를 사용하면 결과물에도 부호가 붙는다.! 오호
print('정수형은 부호가 있는 숫자이므로, 음수를 사용하면 결과물에도 부호가 붙는다')
y_float = -123.4
# print(format(y_float, 'b'))        #부동형 소수는 2진수 b,o,x 코드가 안먹히나보다.
# print(format(y_float,'o'))
# print(format(y_float,'x'))
y_int = -123
print(format(y_int,'b'))              # -1111011


#부호가 없는 값을 사용하려면, 최대값을 더해서 비트 길이를 설정해줘야 한다.
#예를 들어, 32비트 값을 보여주려면 다음과 같이 한다.

print('32비트')
x = -1234
print(format(2**32+x, 'b'))
print(format(2**32+x, 'x'))
print(format(2**32+x, 'o'))


# 다른 진법의 숫자를 정수형으로 변환혀려면 int() 함수에 적절한 진수를 전달한다.
print(int('4d2',16))
print(int('10011010010',2))


# 대부분의 진수 표기법은 int문법으로 간단하게 바꿔주면 된다.
# 한가지 8진법을 사용할 때 주의해야 한다 아래와 같다.

import os
# os.chmod('script.py', 0755)      #ㅈ8진법을 쓸 때는, 0o를 붙여줘야 함
# os.chmod('script.py', 0o0755)





"""
                                                ▶ 3.5 바이트에서 큰 숫자를 패킹/언패킹 ◀ 
♣  문제 : 바이트 문자열을 언패킹해서 정수 값으로 만들어야 한다. 
           혹은 매우 큰 정수값을 바이트 문자열로 변환해야한다.
↘  해결 : 프로그램에서 128비트 정수 값을 담을 수 있는, 길이 16의 바이트 문자열을 다루어야 한다고 가정해보자.
            바이트를 정수형으로 변환하려면?
                1. int.from_bytes()를 사용하여 [바이트 순서]를 명시한다.
                2. 큰 정수 값을 문자열로 변환혀려면, int.to_bytes() 사용하여 [바이트 길이]와 [순서]를 명시한다.
 
 """
print('########################################## 3.5 바이트에서 큰 숫자를 패킹/언패킹 #####################################')


# int.from_bytes()
data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
print(len(data),format(data))      #바이트길이 16

g = int.from_bytes(data, 'little')      # 정수(int)를 -------> 바이트(from_bytes)로 변환하며, 순서 명시하라.
h = int.from_bytes(data, 'big')
print(g,h)

# int.to_bytes()

X =94522842520747284487117727783387188

q = X.to_bytes(16, 'big')
w = X.to_bytes(16, 'little')

print(q,w)


# 정수형 값과 바이트문자열 간의 변환은 일반적인 작업은 아니다. 네트워크나 암호화가 필요한 특정APP에서 사용한다.
# 예를 들어, IPv6 네트워크 주소는 128bit 정수형으로 표시한다. 이 값을 데이터 레코드에서 추출하는 코드를 작성한다면
# int.from_bytes() 메소드 사용해야겠지
# 아니면 6.11에 나올 struct모듈 사용도 좋다. 그러나 언패킹할 수 있는 정수형의 크기가 제한적이라는 점이 있긴 함
# 크기가 제한적이니, 언팩을 여러번 하고, 합치면 되긴 한다.

data2 = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
import struct
high, low = struct.unpack('>QQ',data2)
print((high<< 64) + low)
