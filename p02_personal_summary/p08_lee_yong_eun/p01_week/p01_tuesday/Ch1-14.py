#######################################################################################
# 1.14) 기본 비교 기능 없이 객체 정렬
#     * 동일한 클래스 객체를 정렬해야 하는데, 이 클래스는 기본적인 비교 연산을 제공하지 않는다.
#
# operator.attrgetter() : 클래스의 특정 변수값 얻기
#
# * attrgetter가 lambda보다 빠른 경우가 종종 있고, 동시에 여러 필드를 추출하는 기능이 있다.
#     ex) by_name = sorted(users, key=attrgetter('last_name','first_name'))
#######################################################################################

class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return 'User({})'.format(self.user_id)


users = [User(23), User(3), User(99)]

#lambda 사용
res = sorted(users, key=lambda k: k.user_id)
print(res)

#attrgetter 사용
from operator import attrgetter

res = sorted(users, key=attrgetter('user_id'))
print(res)

#min/max에 활용
minuser = min(users, key=attrgetter('user_id'))
print(minuser) # User(3)