##########################################################################################################
# 5.4] 바이너리 데이터 읽고 쓰기
#   * 이미지나 사운드 파일 등 바이너리 데이터를 읽고 써야 한다.
#     : open() 함수에 rb와 wb 모드를 사용해서 바이너리 데이터를 읽거나 쓴다.
#
# 1) 바이너리 데이터를 읽을 때, 바이너리 문자열과 텍스트 문자열 사이에 미묘한 문법 차이가 있다.
#   자세히 말하면, 데이터에 인덱스나 순환으로 반환한 값은 바이트 문자열이 아닌 정수 바이트 값이 된다.
# 2) 바이너리 모드로부터 텍스트를 읽거나 쓰려면 인코딩이나 디코딩 과정이 꼭 필요하다.
##########################################################################################################

# 파일 전체를 하나의 바이트 문자열로 읽기
with open('s.bin', 'rb') as f:
    data = f.read()

# 바이너리 데이터 파일에 쓰기
with open('s.bin', 'wb') as f:
    f.write(b'Hello world')

# 바이너리 모드에서의 인코딩/디코딩
with open('s.bin', 'rb') as f:
    data = f.read(16)
    text = data.decode('utf-8')

with open('s.bin', 'wb') as f:
    text = 'Hello World'
    f.write(text.encode('utf-8'))
