####################################################################################################
# 2.12] 텍스트 정리
#   * 결합 문자들을 정리하고 싶다.
#
# 1] translate()
#   : 복잡한 문자 리매핑이 편리하다.
# 2] replace() 반복
#   : replace를 반복하더라도 이쪽이 더 빠르다.
####################################################################################################

s = 'python\fis\tawesome\r\n'
print(s)    # pythonis	awesome

##translate()
remap = {
    ord('\t') : ' ',
    ord('\f') : ' ',
    ord('\r') : None    # 삭제됨
}
res = s.translate(remap)
print(res)  # python is awesome

## 모든 결합 문자 삭제
import unicodedata
import sys
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode)
                         if unicodedata.combining(chr(c))) # 모든 결합문자가 fromkeys에 의해 None에 매핑됨
s1 = 'Spicy Jalape\u00f1o'
t1 = unicodedata.normalize('NFD', s1)   # NFC로 하면 안 된다.
print(t1)   # Spicy Jalapeño
res = t1.translate(cmb_chrs)
print(res)  # Spicy Jalapeno