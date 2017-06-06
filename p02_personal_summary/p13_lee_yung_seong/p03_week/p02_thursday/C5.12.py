#파일 존재 여부 확인
#문제
#파일이나 디렉터리가 존재하는지 확인 해야 한다.
#해결
#파일이나 디렉터리의 존재 여부를 확인하기 위해서 os.path 모듈을 사용한다.
import os
os.path.exists('/etc/passwd') #없음 있으면 True
#추가적으로 파일의 종류가 무엇인지 확인 가능 다음 코드에서 파일이 없음 False
#일반 파일인지 확인
os.path.isfile('/etc/passwd')

#디렉터리인지 확인
os.path.isdir()

#심볼릭 링크인지
os.path.islink()

#연결된 파일 얻기
os.path.realpath('/usr/local/bin/python3')

#메타 데이터(파일 크기, 수정 날짜) 등이 필요할 때도 os.path 모듈을 사용한다.
os.path.getsize('/etc/passwd') #파일 크기가 나옴
time=os.path.getmtime() #
import time
time.ctime(time)#시간이 제대로 나옴
#os.path를 사용하면 파일 테스팅은 어렵지 않지만 권한을 주의해야 한다. 특히 메타데이터
