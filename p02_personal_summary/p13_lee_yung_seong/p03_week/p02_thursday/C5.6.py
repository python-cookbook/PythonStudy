#문자열에 입출력 작업하기
#문제
#파일 같은 객체에 동작하도록 작성한 코드에 텍스트나 바이너리 문자열을 제공하고 싶다.
#해결
#io.StringIO()와 io.BytesIO() 클래스로 문자열 데이터에 동작하는 파일 같은 객체를 생성하낟.
import io
s = io.StringIO()
s.write('hello world\n')
print('this is a test',file=s)
s.getvalue()

#기존 문자열을 파일 인터페이스로 감싸기
s = io.StringIO('hello\nworld\n')
s.read(4)
s.read()
#io.string  클래스는 텍스트에만. 바이너리는 io.BytesIO
#토론
#일반 파일 기능을 흉내 내려 할 때 StringIO와 BytesIO 클래스가 가장 유용하다. 예를 들어 유닛 테스트를 할 때 StringIO로 테스트 데이터를 담고 있느 ㄴ객체를 만들어
#일반 파일에 동작하는 함수에 사용할 수 있다.
#StringIO bytesIO 인스턴스가 올바른 정수 파일 디스크립터를 가지고 있지 않음.
#따라서 file,pipe,socket등 실제 시스템 레벨 파일을 요구하는 코드에는 사용할 수 없다.