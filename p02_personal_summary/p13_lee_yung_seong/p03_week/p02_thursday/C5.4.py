#바이너리 데이터 읽고 쓰기
#문제
#이미지나 사운드 파일 등 바이너리 데이터를 읽고 써야 한다.
#해결
#open 함수에 rb와 wb모드를 사용해서 바이너리 데이터를 읽거나 쓴다.
#파일 전체를 하나의 바이트 문자열로 읽기
with open('somefile.bin','rb') as f:
    data = f.read()

#q바이너리 데이터 파일에 쓰기
with open('somefile.bin','wb') as f:
    f.write(b'hello world')

#바이너리를 읽을 때 반환된 모든 데이터가 텍스트 문자열 형식이 아니라 바이트 문자열 형식이 된다는 점을 기억하자.
#마찬가지로 데이터를 쓸 때도 바이트로 표현할 수 있는형식의 객체를 제공해야 한다.

#토론
#바이너리 데이터를 읽을 때, 바이너리 문자열과 텍스트 문자열 사이에 미묘한 문법 차이가 있다.
#자세히 말하자면, 데이터에 인덱스나 순환으로 반환한 값은 바이트 문자열이 아닌 정수 바이트값이 된다.
t = 'hello world'
t[0]
for c in t:
    print(c)

b =b'hello world'
b[0]
for c in b:
    print(c)
#바이너리 모드 파일로 부터 텍스트를 읽거나 쓰려면 인코딩이나 디코딩 과정이 꼭 필요하다.
with open('somefile.bin','rb') as f:
    data = f.read(16)
    text = data.decode('utf-8')

with open('somefile.bin','wb') as f:
    text = 'hello world'
    f.write(text.encode('utf-8'))

#바이너리 입 출력시 잘 알려지지 않은 기능으로 배열이나 C 구조체와 같은 객체를 bytes 객체로 변환하지 않고 바로 쓸 수 있다는 점이 있다.
import array
nums = array.array('i',[1,2,3,4])
with open('data.bin','wb') as f:
    f.write(nums)

#이 기능은 소위 버퍼 인터페이스로 구현되어 있는 객체에 모두 적용된다. 이런 객체는 기반 메모리 버퍼를 바로 작업에 노출시켜 작업이 가능하다. 바이너리 데이터를 쓰는 것도
#이런 작업의 일종이다.
#또한 파일의 readinto() 메소드를 사용하면 여러 객체의 바이너리 데이터를 직접 메모리에 읽어 들일 수 있다.
import array
a = array.array('i',[0,0,0,0,0,0,0,0])
with open('data.bin','rb') as f:
    f.readinto(a)
a
#하지만 이 기술을 사용할 때는 각별히 주의해야함.
#구현법이 플랫폼에 따라 다르기도 하고 단어의 크기와 바이트 순서 등에 의존학 ㅣ때문.