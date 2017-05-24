#3.1 반올림
#문제 부동 소수점 값을 10진수로 반올림 하고 싶다.
#해결 round
round(1.23,1)
round(1.23,2)

#값이 정화깋 두 선택지의 가운데 있으면 더 가까운 짝수가 된다. 예를 들어 1.5와 2.5는 모두 2가 된다.
#round()에 전달하는 자릿수는 음수가 될 수 있다. 이 경우 10의자리 100의자리 순으로 자릿수가 결정
a = 1627731
round(a, -1)

#토론 반올림과 서식화는 다름. 특정 자릿수까지 숫자를 표현하는 것이 목적이면 서식화를 위한 자릿수를 명시하기만 하면 됨.
x=1.23456
format(x,'0.2f')
format(x,'0.3f')
#또한 정확도 문제를 수정하려고 부동 소수점을 반올림 하는 방법도 지양해야함.
#부동 소수점 계산하는 대부분의 어플리케이션에서는 이러한 방법 불필요.