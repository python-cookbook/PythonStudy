#경로 다루기
#문제
#기본 파일 이름, 디렉터리 이름, 절대 경로 등을 찾기 위해 경로를 다루어야 한다.
##해결
#경로를 다루기 위해서 os.path 모듈의 함수를 사용한다. 몇몇 기능을 예제를 통해 살펴보자.
import os
path = '/users/beazley/Data/data.csv'
os.path.basename(path)#경로의 마지막 부분
#디렉터리 이름
os.path.dirname(path)
#합치기
os.path.join('tmp','data',os.path.basename(path))
#사용자의 홈 디렉토리 펼치기
path = '~/Data/data.csv'
os.path.expanduser(path)
#파일 확장자 나누기
os.path.splitext(path)
#토론
#파일 이름을 다루기 위해서 문자열에 관련된 코드를 직접 작성하지 말고 os.path 모듈을 사용해야 한다. 이는 이식성과도 어느 정도 관련이 있다.
#os path 모듈은 unix와 윈도우의 차이점을 알고 자동으로 처리한다.