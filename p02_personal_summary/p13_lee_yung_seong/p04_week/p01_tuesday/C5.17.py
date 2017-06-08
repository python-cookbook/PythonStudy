#텍스트 파일에 바이트 쓰기
#문제
#텍스트 모드로 연 파일에 로우 바이트를 쓰고 싶다.
#해결
#단순히 바이트 데이터를 buffer에 쓴다.
import sys
sys.stdout.write(b'hello\n')#에러
sys.stdout.buffer.write(b'hell\n')
#이와 유사하게 텍스트 파일의 버퍼 속성에서 바이너리 데이터를 읽을 수도 있다.
#토론
#IO시스템은 레이어로부터 만들어진다. 텍스트 파일은 버퍼 바이너리 모드 파일 상단에 Unicode 인코딩/디코딩 레이어를 추가해서 생성된다. 버퍼 속성은 바로 이 파일 아래 부분을 가리킨다.
#여기에 접근하면 텍스트 인코딩/디코딩 레이어를 우회할 수 있다.
#이 예제에는 sys.stdout이 특별하게 보일 수 있다. 기본적으로 sys.stdout은 언제나 텍스트 모드로 열려있다.
#하지만 바이너리 데이터를 표준 출력에 출력하는 스크립트를 작성한다면 이 기술을 사용해 텍스트 인코딩을 우회할 수 있다.