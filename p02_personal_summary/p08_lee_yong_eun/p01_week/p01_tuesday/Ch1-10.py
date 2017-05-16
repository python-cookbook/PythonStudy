#######################################################################################
# 1.10) 순서를 깨지 않고 시퀀스의 중복 없애기
#     * 시퀀스에서 중복된 값은 없애고 싶지만, 아이템의 순서는 유지하고 싶다.
#######################################################################################


#시퀀스의 아이템이 해시 가능한 경우에 사용 가능
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)
    #return seen을 하면 정렬된 값이 반환된다.(순서 유지 x)

#해시 불가능한 타입(예: dict)의 중복을 없애기 위해서는 레시피에 약간의 수정이 필요하다.
def dedupe2(items, key=None):
    seen = set()
    for item in items:
        #val = item if key is None else key(item) : 위 dedupe 함수의 기능도 수행 가능
        val = key(item) # ex) (1,2)
        if val not in seen:
            yield item
            seen.add(val)

a = [1, 5, 2, 1, 9, 1, 5, 10]

res = set(a)
print(res) # {1, 2, 5, 9, 10} : 데이터의 순서가 훼손되었다.

res = list(dedupe(a))
print(res) # [1, 5, 2, 9, 10] : 데이터 순서 유지됨

a = [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}]

res = list(dedupe2(a,key=lambda d: (d['x'],d['y']))) # 'x','y'값에 대한 중복 검사
print(res) # [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]

res = list(dedupe2(a,key=lambda d: d['x'])) # 'x'값에 대한 중복 검사
print(res) # [{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]