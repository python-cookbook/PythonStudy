####################################################################################################
# 2.16] 텍스트 열의 개수 고정
#   * 긴 문자열의 서식을 바꿔 열의 개수를 조절하고 싶다.
#
# 1] textwrap.fill
#   1-1] initial_indent : 첫 줄의 시작에 넣을 문자열
#   1-2] subsequent_indent : 둘째 줄 이후의 시작에 넣을 문자열
####################################################################################################
import textwrap

s = "Look into my eyes, look into my eyes, the eyes, the eyes, " \
    "the eyes, not around the eyes, don't look around the eyes," \
    "look into my eyes, you're under."

print(textwrap.fill(s,70))
###
# Look into my eyes, look into my eyes, the eyes, the eyes, the eyes,
# not around the eyes, don't look around the eyes,look into my eyes,
# you're under.
###

print(textwrap.fill(s,40))
###
# Look into my eyes, look into my eyes,
# the eyes, the eyes, the eyes, not around
# the eyes, don't look around the
# eyes,look into my eyes, you're under.
###

print(textwrap.fill(s, 40, initial_indent='         '))
###
#          Look into my eyes, look into my
# eyes, the eyes, the eyes, the eyes, not
# around the eyes, don't look around the
# eyes,look into my eyes, you're under.
###

print(textwrap.fill(s, 40, subsequent_indent='            '))
###
# Look into my eyes, look into my eyes,
#             the eyes, the eyes, the
#             eyes, not around the eyes,
#             don't look around the
#             eyes,look into my eyes,
#             you're under.
###