##########################################################################################################
# 6.4] 매우 큰 XML 파일 증분 파싱하기
#   * 매우 큰 XML 파일에서 최소의 메모리만 사용하여 데이터를 추출하고 싶다.
#     : 이터레이터/제너레이터 사용 !
##########################################################################################################

from xml.etree.ElementTree import iterparse

# 아주 큰 XML 파일을 증분적으로 처리하며, 메모리 사용은 최소로 하는 함수
def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    # 뿌리 요소 건너뛰기
    next(doc)

    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass
