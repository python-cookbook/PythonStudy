####################################################################################################
# 2.9] 유니코드 텍스트 노멀화
#   * 유니코드 문자열 작업을 하고 있다. 이때 모든 문자열에 동일한 표현식을 갖도록 보장하고 싶다.
#     동일한 텍스트의 표현 방식이 여러 가지 존재할 수 있으며, 이들은 서로 다른 문자열로 인식되는 것이 문제이다.
#
#   * 일관적이고 안전한 유니코드 텍스트 작업을 위해 노멀화는 아주 중요하다.
#     특히 인코딩을 조절할 수 없는 상황에서 사용자에게 문자열 입력을 받을 때는 특히 조심해야 한다.
#
#   * 노멀화에 대한 자세한 정보 확인 : Unicode's page on the subject
#
# 1] unicodedata.normalize()
#   : 첫번째 인자에는 문자열을 어떻게 노멀화할 것인지 지정
#       * NFC : 문자를 정확히 구성하도록 지정(가능하다면 단일 코드 포인트 사용)
#       * NFD : 문자를 여러 개 합쳐서 사용하도록 지정
#
####################################################################################################

## 동일한 텍스트가 여러 형식으로 표현되는 사례
s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'
print(s1) # Spicy Jalapeño
print(s2) # Spicy Jalapeño
print(s1 == s2) # False

## unicodedata를 사용한 노멀라이즈
import unicodedata
t1 = unicodedata.normalize('NFC', s1)
t2 = unicodedata.normalize('NFC', s2)
print(t1 == t2) # True

# 텍스트에서 발음 구분 기호 모두 지우기
# combining : 해당 문자가 결합 문자인지 확인
t1 = unicodedata.normalize('NFD', s1)
res = ''.join(c for c in t1 if not unicodedata.combining(c))
print(res)  # Spicy Jalapeno