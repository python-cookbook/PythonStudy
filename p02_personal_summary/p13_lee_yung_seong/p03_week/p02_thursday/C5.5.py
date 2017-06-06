#존재하지 않는 파일에 쓰기
#문제
#파일이 파일 시스템에 존재하지 않을 때, 데이터를 파일에 쓰고 싶다.
#해결
#이 문제는 open()에 x모드를 사용해서 해결할 수 있다. w모드와 다르게 x 모드는 잘 알려져 있지 않다.
with open('somefile','wt') as f:
    f.write('hello')

with open('somefile','xt') as f:
    f.write('hello\n')
 #파일이 바이너리 모드이면 xt 대신 xb를 사용한다.

#토론
#이 레시피는 파일을 쓸 때 발생하는 문제점(실수로 파일을 덮어 쓰는 등)을 깔끔하게 피해가는 법을 알려준다.
#혹은 파일을 쓰기 전에 파일이 있는지 확인하는 방법도 있다.
import os
if not os.path.exists('somefile'):
    with open('somefile','wt') as f:
        f.write('hello\n')
else:
    print('file already exists')

#x 모드는 파이썬 3의 확장 기능.