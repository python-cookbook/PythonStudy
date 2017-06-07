##########################################################################################################
# 5.14] 파일 이름 인코딩 우회
#   * 시스템의 기본 인코딩으로 디코딩 혹은 인코딩되지 않은 파일명에 입출력 작업을 수행해야 한다.
#
#   * 일반적인 환경에서 파일명 인코딩/디코딩은 걱정할 필요 없이 잘 돌아간다.
#     하지만 많은 운영체제에서 사용자는 실수로, 혹은 악의적으로 인코딩 규칙을 따르지 않는 파일명을 생성할 수 있다.
#     이런 파일명은 많은 파일을 다루는 파이썬 프로그램을 망가뜨릴 수 있으므로,
#     파일명과 디렉터리를 읽을 때 디코딩되지 않은 로우 바이트를 이름으로 사용하면
#     프로그래밍은 조금 귀찮겠지만 이러한 문제점을 피해갈 수 있다.
##########################################################################################################
import sys

# 파일명 기본 인코딩값
print(sys.getfilesystemencoding())  # utf-8

## 인코딩을 우회하기 위해서는 raw 바이트 문자열로 파일명을 명시해야 한다.
# 유니코드로 파일명을 쓴다.
with open('jalape\xf1o.txt', 'w') as f:
    f.write('Spicy!')

# 디렉터리 리스트 (디코딩됨)
import os
print(os.listdir('.'))  # ~, 'jalapeño.txt'

# 디렉터리 리스트 (디코딩되지 않음)
print(os.listdir(b'.')) # b'jalape\xc3\xb1o.txt'

# 로우 파일명으로 파일 열기
with open(b'jalape\xc3\xb1o.txt') as f:
    print(f.read()) # Spicy!


