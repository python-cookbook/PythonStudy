#JSON 데이터 읽고 쓰기
#문제
#JSON 으로 인코딩 된 데이터를 읽거나 쓰고 싶다.
#해결
#JSON으로 데이터를 인코딩, 디코딩하는 쉬운 방법은 json 모듈을 사용하는 것이다. 주요 함수는 json.dumps()와 json.loads()이고 pickle과 같은 직려로하 라이브러리에서 사용한것과 인터페이스는 동일하다;.
#파이선 데이터를 json으로 변환하는 코드
import json
data = {'name' : 'ACME',
        'shares' : 100,
        'price' : 542.23}
json_str = json.dumps(data)
json_str
#json으로 인코딩 된 문자열을 파이썬 자료 구조로 돌리는 방법
data = json.loads(json_str)
#문자열이 아닌 파일로 작업한다면 json.dump()와 json.load()를 사용해서 json 데이터를 인코딩/디코딩한다.
#json 데이터 쓰기
with open('data.json','w') as f:
    json.dump(data,f)

#데이터 다시 읽기
with open('data.json','r') as f:
    data = json.load(f)
#토론
#json인코딩은 none, bool, int, float, str과 같은 기본 타입과 함께 리스트,튜플,딕셔너리와 같은 컨테이너 타입을 지원한다,
#딕셔너리의 경우 키는 문자열로 가정한다(문자열이 아닌 키는 인코딩 과정에서 문자열로 변환된다.) JSON 스펙을 따르기 위해서 파이썬 리스트와 딕셔너리만 인코딩 해야 하낟.
#그리고 웹 어플리케이션의 경우에는 상위 레벨 객체는 딕셔너리로 하는 것이 표준이다.
#json 인코딩 포맷은 약간의 차이점을 제외하고 파이썬 문법과 거의 동일하다. 예를 들어 True는 true로 False는 false로 None은 null로 매핑된다. 어떤 식으로 인코딩 되는지
#다음 코드를 참고한다.
json.dumps(False)
d={'a':True,'b':'Hello','c':None}
json.dumps(d)
#json에서 디코딩한 데이터를 조사해야 한다면, 단순히 출력해서 구조를 알아내기는 쉽지 않다. 특히 데이터에 중첩이 심하게 된 구조체가 포함되어 있거나 필드가 많다면
#더 어렵다 이런 경우에는 pprint모듈의 pprint() 함수를 사용하자. 이 하무는 키를 알파벳 순으로 나열하고 딕셔너리를 보기 좋게 출력한다.
#트위터의 검색 결과를 예쁘게 출력
from urllib.request import urlopen
import json
u = urlopen('http://search.twitter.com/search.json?q=python&rpp=5')
resp = json.loads(u.read().decode('utf-8'))
from pprint import pprint
pprint(resp)
#일반적으로 json 디코딩은 제공 받은 데이터로 부터 딕셔너리나 리스트를 생성한다. 다른 종류의 객체를 만들고 싶다면 json.loads()에 object_pairs_hook나 object_hook를 넣는다.
#예를 들어 OrderedDict의 순서를 지키면서 json데이터를 디코딩하려면 다음과 같이 한다.
s='{"name":"ACME", "shares":50, "price":490.1}'
from collections import OrderedDict
data = json.loads(s, object_pairs_hook=OrderedDict)
data
#다음은 json 딕셔너리를 파이썬 객체로 바꾸는 예시이다.
class JSONObject:
    def __init__(self,d):
        self.__dict__=d

data = json.loads(s,object_pairs_hook=JSONObject)
#마지막 예제에서 json 데이터를 디코딩하여 생성한 딕셔너리를 __init__()에 인자로 전달했다. 여기부터는 객체의 딕셔너리 인스턴스인 것처럼 자유롭게 사용해도 괜찮다.
##json 인코딩 할 때 유용한 옵션이 몇가지 있다. 출력을 더 보기 좋게 하려면 json.dumps()에 indent인자를 사용한다.
print(json.dumps(data, indent=4))
#출력에서 키를 정렬하고 싶다면 sort_keys 인자
print(json.dumps(data, indent=4, sort_keys=True))
#인스턴스는 일반적으로 json으로 직렬화하지 않는다.
class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
point=Point(2,3)
p=point
json.dumps(p)

#인스턴스를 직렬화 하고 싶다면 인스턴스를 입력으로 받아 직렬화 가능한 딕셔너리를 반환하는 함수를 제공해야 한다.

def serialize_instance(obj):
    d = {'__classname__' : type(obj).__name__}
    d.update(vars(obj))
    return d
#인스턴스를 돌려받고 싶다면 다음과 같은 코드
classes = { 'Point' : Point}
def unserialize_object(d):
    clsname = d.pop('__classname__', None)
    if clsname:
        cls = classes[clsname]
        obj = cls.__new__(cls)
        for key,value in d.items():
            setattr(obj, key, value)
            return obj
        else:
            return d

#앞에 나온 함수는 다음과 같이 사용한다.
s=json.dumps(p, default=serialize_instance)
a=json.loads(s, object_hook=unserialize_object)
a.x\
#json 모듈에는 숫자, NaN과 같은 특별 값 등 하위 레벨 조절을 위한 많은 옵션이 있다. 자세한 내용은 공식 문서를 참고하도록 하자.