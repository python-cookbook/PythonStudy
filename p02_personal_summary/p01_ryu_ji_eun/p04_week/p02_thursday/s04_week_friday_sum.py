###############################################################################################################
## 6.5 turning a dictionary into xml (딕셔너리를 xml로 바꾸기)
# you want to take the data in a Python dictionary and turn it into xml
################################################################################################################
# although the xml.etree.ElementTree library is commonly used for parsing, it can also be used to create XML documents

from xml.etree.ElementTree import Element


def dict_to_xml(tag, d):
    '''
    turn a simple dict of key/value pairs into xml
    '''
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem


s = {'name': 'GOOG', 'shares': 100, 'price': 490.1}
e = dict_to_xml('stock', s)
e
# <Element 'stock' at 0x1004b64c8>


from xml.etree.ElementTree import tostring

tostring(e)


# b'<stock><price>490.1</price><shares>100</shares><name>GOOG</name></stock>'


# when creating xml, you might be inclined to just make strings instead
def dict_to_xml_str(tag, d):
    '''
    turn a simple dict of key/value pairs into xml
    '''
    parts = ['<{}>'.format(tag)]
    for key, val in d.items():
        parts.append('<{0}>{1}</{0}>'.format(key, val))
    parts.append('</{}>'.format(tag))
    return ''.join(parts)




###############################################################################################################
## 6.6 xml 파싱, 수정, 저장
# xml 문서를 읽고, 수정하고, 그 내용을 xml에 반영하고 싶다
################################################################################################################
# xml.etree.ElementTree 모듈로 해결. pred.xml라는 파일을 ElementTree로 이 문서를 읽고 수정해보자

## 여기는 XML
<?xml version="1.0"?>
<stop>
    <id>14791</id>
    <nm>Clark &amp; Balmoral</nm>
    <sri>
        <rt>22</rt>
        <d>North Bound</d>
        <dd>North Bound</dd>
        </sri>
        <cr>22</cr>
        <pre>
            <pt>5 MIN</pt>
            <fd>Howard</fd>
            <v>1378</v>
            <rn>22</rn>
        </pre>
        <pre>
            <pt>15 MIN</pt>
            <fd>Howard</fd>
            <v>1867</v>
            <rn>22</rn>
        </pre>
    </stop>

## 기본 XML은 여기까지


from xml.etree.ElementTree import parse, Element
doc = parse('pred.xml')
root = doc.getroot()
root
# <Element 'stop' at 0x100770cb0>

# 요소 몇 개 제거하기
root.remove(root.find('sri'))
root.remove(root.find('cr'))

# <nm> .. </nm> 뒤에 요소 몇 개 삽입하기
root.getchildren().index(root.find('nm'))
# 결과값 : 1

e = Element('spam')
e.text = 'This is a test'
root.insert(2, e)


# 파일에 쓰기
doc.write('newpred.xml', xml_declaration=True)


## 위의 코드를 수행한 XML 결과값
<?xml version='1.0' encoding='us-ascii'?>
<stop>
    <id>14791</id>
    <nm>Clark &amp; Balmoral</nm>
    <spam>This is a test</spam><pre>
        <pt>5 MIN</pt>
        <fd>Howard</fd>
        <v>1378</v>
        <rn>22</rn>
    </pre>
    <pre>
        <pt>15 MIN</pt>
        <fd>Howard</fd>
        <v>1867</v>
        <rn>22</rn>
    </pre>
</stop>



###############################################################################################################
## 6.7 네임스페이스로 xml 문서 파싱
# xml 문서를 파싱할 때 xml 네임 스페이스를 사용하고 싶다
################################################################################################################
<?xml version="1.0" encoding="utf-8"?>
<top>
    <author>David Beazley</author>
    <content>
        <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <title>Hello World</title>
            </head>
            <body>
                <h1>Hello World</h1>
            </body>
        </html>
    </content>
</top>


# 유틸리티 클래스로 네임스페이스를 감싸주면 문제를 단순화 할 수 있다
class XMLNamespaces:
    def __init__(self,**kwargs):
        self.namespaces = {}
        for name, uri in kwargs.items():
            self.register(name, uri)

    def register(self, name, uri):
        self.namespaces[name] = '{'+uri+'}'

    def __call__(self,path):
        return path.format_map(self.namespaces)


# 이 클래스 사용하는 방법
ns = XMLNamespaces(html='http://www.w3.org/1999/xhtml')
doc.find(ns('content/{html}html'))
# <Element '{http://www.w3.org/1999/xhtml}html' at 0x1007767e0>




###############################################################################################################
## 6.8 관계형 데이터 베이스 작업
# 관계형 데이터베이스에 선택, 삽입, 행삭제(select, insert, delete row)등의 작업을 하고 싶다
################################################################################################################
stocks = [
    ('GOOG',100,490.1),
    ('AAPL',50,545.75),
    ('FB',150,7.45),
    ('HPQ',75,33.2)
]

## sqlite3 모듈을 사용
# DB연결
import sqlite3
db = sqlite3.connect('database.db')

# data 작업을 하기 위해서는 cursor를 만들어야 한다
c = db.cursor()
c.execute('create table portfolio (symbol text, shares integer, price real)')
# <sqlite3.Cursor object at 0x10067a730>
db.commit()

# 데이터행에 시퀀스를 삽입하려면
c.executemany('insert into portfolio values (?,?,?)',stocks)
# <sqlite3.Cursor object at 0x10067a730>
db.commit()


# 쿼리를 수행하려면
for row in db.execute('select * from portfolio'):
    print(row)
# ('GOOG',100,490.1)
# ('AAPL',50,545.75)
# ('FB',150,7.45)
# ('HPQ',75,33.2)


# 사용자가 입력한 파라미터를 받는 쿼리를 수행하려면 ?를 사용해 파라미터를 이스케이핑 해야한다
min_price = 100
for row in db.execute('select * from portfolio where price >= ?',
                      (min_price,)):
    print(row)
# ('GOOG',100,490.1)
# ('AAPL',50,545.75)





###############################################################################################################
## 6.9 16진수 인코딩, 디코딩
# 문자열로 된 16진수를 바이트 문자열로 디코딩하거나, 바이트 문자열을 16진법으로 인코딩해야 한다
################################################################################################################
# 문자열을 16진수로 인코딩하거나 디코딩하려면 binascii 모듈을 사용한다

# 기본 바이트 문자열
s = b'hello'

# 16진법으로 인코딩
import binascii
h = binascii.b2a_hex(s)
print(h)
# 결과값 : b'68656c6c6f'


# 바이트로 인코딩
binascii.a2b_hex(h)
# 결과값 : b'hello'


# base64 모듈의 유사한 기능
import base64
h = base64.b16encode(s)
print(h)
# b'68656C6C6F'

base64.b16decode(h)
# b'hello'

## 두 함수의 차이는 대소문자 구분에 있다.
# bas64.b16decode()와 base64.b16encode() 함수는 대문자에만 동작하지만 binascii는 대소문자를 가리지 않는다.
# 인코딩 함수가 만들 출력물은 언제나 바이트 문자열이므로, 유니코드를 사용해야 한다면 디코딩 과정을 하나 더 추가해야 함
h = base64.b16encode(s)
print(h)
# b'68656C6C6F'

print(h.decode('ascii'))
# 68656C6C6F




###############################################################################################################
## 6.10 base64 인코딩, 디코딩
# base64를 사용한 바이너리 데이터를 인코딩, 디코딩 해야 한다
################################################################################################################
# 해당 모듈에 b64encode()와 b64decode() 함수를 사용하면 됨
## 바이트 데이터
s = b'hello'
import base64

# base64로 인코딩
a = base64.b64encode(s)
print(a)
# b'aGVsbG8='

# bse64를 인코딩
base64.b64decode(a)
# b'hello'

## base64 인코딩 데이터와 유니코드 텍스트를 함께 사용하려면 추가적인 디코딩 작업을 해야한다
a = base64.b64encode(s).decode('ascii')
print(a)
# 'aGVsbG8'




###############################################################################################################
## 6.11 바이너리 배열 구조체 읽고 쓰기
# 바이너리 배열 구조를 파이썬 튜플로 읽거나 쓰고 싶다
################################################################################################################
# 바이너리 데이터를 다루기 위해서 struct 모듈을 사용한다. struct를 사용해서 튜플을 인코딩하는 식으로 써보자
from struct import Struct
def write_records(records, format, f):
    record_struct = Struct(format)
    for r in records:
        f.write(record_struct.pack(*r))


# 예제
if __name__=='__main__':
    '''
    일련의 튜플을 구조체에 기록
    '''
    records = [(1, 2.3, 4.5),
               (6, 7.8, 9.0),
               (12, 13.4, 56.7)]

    with open('data.b','wb') as f:
        write_records(records, '<idd',f)


# 1. 파일을 조각조각 튜플 리스트로 읽어들이는 방법
from struct import Struct

def read_records(format, f):
    record_struct = Struct(format)
    chunks = iter(lambda: f.read(record_struct.size), b'')
    return (record_struct.unpack(chunk) for chunk in chunks)

# 예제
if __name__=='__main__':
    with open('data.b','rb') as f:
        for rec in read_records('<idd',f):
            # rec 처리 ...


# 2. 바이트 문자열을 한 번에 읽어들이고 추후 여러 조각으로 변환하는 방법
from struct import Struct

def unpack_records(format, data):
    record_struct = Struct(format)
    return (record_struct.unpack_from(data, offset)
            for offset in range(0,len(data), record_struct.size))


# 예제
if __name__=='__main__':
    with open('data.b','rb') as f:
        data = f.read()

    for rec in unpack_records('<idd',data):
        # rec 처리 ...

## 방대한 바이너리 데이터를 다루는 프로그램을 작성할 때는 numpy와 같은 라이브러리를 사용하는 것이 좋다.
# 예시로 바이너리 데이터를 읽어 튜플 리스트에 넣지 않고 구조적 배열에 넣을 수 있다
import numpy as np
f = open('data.b','rb')
records = np.fromfile(f, dtype='<i,<d,<d')
records
# array([1, 2.3, 4.5), (6, 7.8, 9.0), (12, 13.4, 56.7)], dtype =[('f0','<i4'),('f1','<f8'),('f2','<f8')])

records[0]
# (1, 2.3, 4.5)

records[1]
# (6, 7.8, 9.0)




###############################################################################################################
## 6.12 중첩, 가변 바이너리 구조체 읽기
# 중첩되거나 크기가 변하는 레코드 컬렉션으로 이루어진 바이너리 인코딩 데이터를 읽어야 한다.
# 이미지, 비디오, shapefile 등등
################################################################################################################
# 거의 모든 바이너리 데이터 구조를 인코딩, 디코딩할 때 struct 모듈을 사용할 수 있다
# 아래는 폴리곤의 꼭지점을 나타내는 파이썬 데이터이다
polys = [
    [(1.0, 2.5), (3.5, 4.0), (2.5, 1.5)],
    [(7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0)],
    [(3.4, 6.3), (1.2, 0.5), (4.6, 9.2)]
]


# 아래의 헤더로 시작하는 바이너리 파일에 데이터를 인코딩해서 넣자
# byte    type        explain
# ------ ----------- ------------------------------
# 0       int         파일 코드(0x1234, 리틀 엔디안)
# 4       double      최소 x (리틀 엔디안)
# 12      double      최소 y (리틀 엔디안)
# 20      double      최대 x (리틀 엔디안)
# 28      double      최대 y (리틀 엔디안)
# 36      int         폴리곤 수 (리틀 엔디안)


# 헤더 뒤에 오는 인코딩된 폴리곤 레코드
# 0          int        길이를 포함한 레코드 길이 (N 바이트)
# 4-N        Points     double로 표현한 (x,y) 페어


# 이 파일을 쓰기 위해 아래 코드를 쓴다
import struct
import itertools

def write_polys(filename, polys):
    # 충돌 박스 계산
    flattened = list(itertools.chain(*polys))
    min_x = min(x for x,y in flattened)
    max_x = max(x for x,y in flattened)
    min_y = min(y for x,y in flattened)
    max_y = max(y for x,y in flattened)

    with open(filename, 'wb') as f:
        f.write(struct.pack('<iddddi',
                            0x1234,
                            min_x, min_y,
                            max_x, max_y,
                            len(polys)))
        for poly in polys:
            size = len(poly) * struct.calcsize('<dd')
            f.write(struct.pack('<i', size+4))
            for pt in poly:
                f.write(struct.pack('<dd',*pt))

# 폴리곤 데이터를 가지고 호출
write_polys('polys.bin',polys)


## 결과 데이터를 읽어 들이기 위해, 쓰기 코드를 반대로 작성해보자
# struct.unpack() 함수 사용
import struct

def read_polys(filename):
    with open(filename, 'rb') as f:
        # 헤더 읽기
        header = f.read(40)
        file_code, min_x, min_y, max_x, max_y, num_polys = \
        struct.unpack('<iddddi',header)

        polys = []
        for n in range(num_polys):
            pbytes, = struct.unpack('<i', f.read(4))
            poly = []
            for m in range(pbytes // 16):
                pt = struct.unpack('<dd', f.read(16))
                poly.append(pt)
            polys.append(poly)
    return polys



## 첫째로 바이너리 데이터를 읽을 때, 파일에는 일반적으로 헤더와 여타의 자료 구조가 포함된다.
# struct 모듈이 이런 데이터를 언패킹해서 튜플로 만들 수 있지만, 이런 정보를 표현하는 다른 방식은 클래스를 사용한다
import struct
class StructField:
    '''
    간단한 구조 필드를 나타내는 디스크립터
    '''
    def __init__(self, format, offset):
        self.format = format
        self.offset = offset

    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            r = struct.unpack_from(self.format,
                                   instance._buffer, self.offset)
            return r[0] if len(r) == 1 else r

class Structure:
    def __init__(self, bytedata):
        self._buffer = memoryview(bytedata)


# 이 코드는 각 구조 필드를 나타내는 데 descriptor를 사용한다. 각 descriptor는 struct와 호환되는 포맷 코드와
# 메모리 버퍼를 가리키는 바이트 오프셋을 가지고 있다
# __get__() 메소드에서, struct.unpack_from() 함수로 버퍼의 값을 언팩하는데, 이때 추가적인 조각을 만들거나
# 복사를 발생하지 않는다.
#

# structure 클래스는 바이트 데이터를 받고 StructField 디스크립터가 사용한 메모리 버퍼에 저장하는 베이스 클래스
# 역할(...뭔 말임)을 한다. 이 클래스에서 memoryview()를 사용한 목적은 조금 더 뒤에서 배운다
class PolyHeader(Structure):
    file_code = StructField('<i', 0)
    min_x = StructField('<d', 4)
    min_y = StructField('<d', 12)
    max_x = StructField('<d', 20)
    max_y = StructField('<d', 28)
    num_polys = StructField('<i', 36)

# 이 클래스로 앞에 나왔던 폴리곤 데이터의 헤더를 읽는 예제를 보자
f = open('polys.bin','rb')
phead = PolyHeader(f.read(40))
phead.file_code == 0x1234
# True
phead.min_x
# 0.5
phead.min_y
# 0.5
phead.max_x
# 7.0
phead.max_y
# 9.2
phead.num_polys
# 3


## 메타클래스를 사용해서 Structure 클래스를 다시 구현해보자
class StructureMeta(type):
    '''
    StructField descriptor를 자동으로 만드는 메타 클래스
    '''
    def __init__(self, clsname, bases, clsdict):
        fields = getattr(self, '_fields_', [])
        byte_order = ''
        offset = 0
        for format, fieldname in fields:
            if format.startswith(('<','>','!','@')):
                byte_order = format[0]
                format = format[1:]
            format = byte_order + format
            setattr(self, fieldname, StructField(format, offset))
            offset += struct.calcsize(format)

class Structure(metaclass = StructureMeta):
    def __init__(self, bytedata):
        self._buffer = bytedata


    @classmethod
    def from_file(cls,f):
        return cls(f.read(cls.struct_size))


## 이제 새로운 Structure 클래스를 사용해서 구조체 정의를 다음과 같이 해보자
class PolyHeader(Structure):
    _fields_=[
        ('<i', 'file_code'),
        ('d','min_x'),
        ('d','min_y'),
        ('d','max_x'),
        ('d','max_y'),
        ('i','num_polys')
    ]

# from_file() 클래스 메소드가 추가되었는데, 이 메소드는 파일에서 데이터의 구조나 크기를 몰라도 쉽게 읽을 수 있게 해줌
f = open('polys.bin','rb')
phead = PolyHeader.from_file(f)
phead.file_code == 0x1234
# True
phead.min_x
# 0.5
phead.min_y
# 0.5
phead.max_x
# 7.0
phead.max_y
# 9.2
phead.num_polys
# 3


## 중첩된 바이너리 구조를 지원해야 한다고 할 때, 이 기능을 지원하는 새로운 descriptor와 함께 메타 클래스를 수정해보자
class NestedStruct:
    '''
    중첩 구조를 표현하는 디스크립터
    '''
    def __init__(self,name,struct_type,offset):
        self.name = name
        self.struct_type = struct_type
        self.offset = offset

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            data = instance._buffer[self.offset:
                                self.offset+self.struct_type.struct_size]
            result = self.struct_type(data)
            # 결과 구조를 인스턴스에 저장해서
            # 이 단계를 다시 계산하지 않도록 한다
            setattr(instance, self.name, result)
            return result


class StructureMeta(type):
    '''
    StructField 디스크립터를 자동으로 만드는 메타 클래스
    '''
    def __init__(self, clsname, bases, clsdict):
        fields = getattr(self, '_fields_',[])
        byte_order = ''
        offset = 0
        for format, fieldname in fields:
            if isinstance(format, StructureMeta):
                setattr(self, fieldname,
                        NestedStruct(fieldname, format, offset))
                offset += format.struct_size
            else:
                if format.startswith(('<','>','!','@')):
                    byte_order = format[0]
                    format = format[1:]
                format = byte_order + format
                setattr(self, fieldname, StructField(format, offset))
                offset += struct.calcsize(format)
            setattr(self, 'struct_size',offset)


## ..blah blah 어쨌든 새로운 구현법을 사용해서 코드를 작성하는 방법
class Point(Structure):
    _fields_=[
        ('<d','x'),
        ('d','y')
    ]

class PolyHeader(Structure):
    _fields_=[
        ('<i','file_code'),
        (Point,'min'),
        (Point,'max'),
        ('i','num_polys')
    ]


## 잘 동작함

# 크기가 변하는 섹션이 있는 폴리곤 파일을 처리하려면 바이너리 데이터 조각을 표현하는 클래스와 함께
# 다른 방식으로 내용을 해석하는 유틸리티 함수를 작성하면 된다
class SizedRecord:
    def __init__(self,bytedata):
        self._buffer = memoryview(bytedata)

    @classmethod
    def from_file(cls,f,size_fmt,includes_size=True):
        sz_nbytes = struct.calcsize(size_fmt)
        sz_bytes = f.read(sz_nbytes)
        sz, = struct.unpack(size_fmt, sz_bytes)
        buf = f.read(sz - includes_size * sz_nbytes)
        return cls(buf)

    def iter_as(self,code):
        if isinstance(code, str):
            s = struct.Struct(code)
            for off in range(0,len(self._buffer),s.size):
                yield s.unpack_from(self._buffer,off)

        elif isinstance(code, StructureMeta):
            size = code.struct_size
            for off in range(0,len(self._buffer),size):
                data = self._buffer[off:off+size]
                yield code(data)


## 클래스 메소드 SizedRecord.from_file()은 파일에서 크기가 고정된 데이터를 읽어 들이는 기능이다. 대부분 파일서 사용
# 입력으로 구조체 포맷 코드를 받는데 여기엔 바이트로 된 크기 인코딩이 담겨 있다.
# 추가적 인자인 includes_size는 바이트에 크기 헤더가 포함되어 있는지 아닌지를 가리킨다
f = open('polys.bin','rb')
phead = PolyHeader.from_file(f)
phead.num_polys
# 3
polydata = [SizedRecord.from_file(f,'<i')
            for n in range(phead.num_polys)]
polydata
# [<__main__.SizedRecord object at 0x1006a4d50>,
# <__main__.SizedRecord object at 0x1006a4f50>,
# <__main__.SizedRecord object at 0x10070da90>]


for n, poly in enumerate(polydata):
    print('Polygon',n)
    for p in poly.iter_as('<dd'):
        print(p)

# Polygon 0
# (1.0, 2.5)
# (3.5, 4.0)
# (2.5, 1.5)
# Polygon 1
# (7.0, 1.2)
# (5.1, 3.0)
# (0.5, 7.5)
# (0.8, 9.0)
# Polygon 2
# (3.4, 6.3)
# (1.2, 0.5)
# (4.6, 9.2)


for n, poly in enumerate(polydata):
    print('Polygon',n)
    for p in poly.iter_as(Point):
        print(p.x, p.y)

# Polygon 0
# 1.0 2.5
# 3.5 4.0
# 2.5 1.5
# Polygon 1
# 7.0 1.2
# 5.1 3.0
# 0.5 7.5
# 0.8 9.0
# Polygon 2
# 3.4 6.3
# 1.2 0.5
# 4.6 9.2



## 이제 모든 내용을 합쳐서 read_polys() 함수를 구현해보자
class Point(Structure):
    _fields_ = [
        ('<d','x'),
        ('d','y')
    ]

class PolyHeader(Structure):
    _fields_ = [
        ('<i','file_code'),
        (Point, 'min'),
        (Point, 'max'),
        ('i','num_polys')
    ]

def read_polys(filename):
    polys = []
    with open(filename, 'rb') as f:
        phead = PolyHeader.from_file(f)
        for n in range(phead.num_polys):
            rec = SizedRecord.from_file(f,'<i')
            poly = [(p.x, p.y)
                    for p in rec.iter_as(Point)]
            polys.append(poly)
    return polys



###############################################################################################################
## 6.13 데이터 요약과 통계 수행
# 커다란 dataset을 요약하거나 통계를 내고 싶다
################################################################################################################
# pandas 라이브러리를 알아봐야 한다
import pandas

# csv 파일을 읽고 마지막 라인은 건너뛴다
rats = pandas.read_csv('rats.csv',skip_footer=1)
rats
# <class 'pandas.core.frame.DataFrame'>
# Int64Index: 74055 entries, 0 to 74054
# Data columns:
# Creation Date                       74055 non-null values
# Status                              74055 non-null values
# Completion Date                     72154 non-null values
# Service Request Number              74055 non-null values
# Type of Service Request             74055 non-null values
# Number of Premises Baited           65804 non-null values
# Number of Premises with Garbage    65600 non-null values
# Number of Premises with Rats       65752 non-null values
# Current Activity                    66041 non-null values
# ...... ......... blah blah blah........
# dtypes: float64(11), object(9)

## 특정 필드에 대해 값의 범위를 조사한다
rats['Current Activity'].unique()
# 결과값 : array([nan, Dispatch Crew, REquest Sanitation Inspector], dtype=object)

## 데이터 필터링
crew_dispatched = rats[rats['Current Activity'] == 'Dispatch Crew']
print(len(crew_dispatched))
# 결과값 : 65676

## 시카고에서 쥐가 가장 많은 장소...를 내가 알아서 어따 쓰냐 ㅠ
crew_dispatched['ZIP Code'].value_counts()[:10]
# 60647   3837
# 60618   3530
# 60614   3284
# 60629   3251
# 60636   2801
# 60641   2238
# 60609   2206
#  .... ....


## 완료 날짜로 그룹 짓기
dates = crew_dispatched.groupby('Completion Date')
# <pandas.core.groupby.DataFrameGroupBy object at 0x10d0a2a10>
len(dates)
# 472


## 각 날짜에 대한 카운트 얻기
date_counts = dates.size()
date_counts[0:10]
# 암튼 섞인 날짜 뜸


## 카운트 정렬
date_counts.sort()
date_counts[-10:]
# 암튼 가장 쥐가 활발했던 순서대로(아래로 갈수록 증가하는...이름 까묵) 정렬된 날짜 뜸
# 암튼 그러함...



###############################################################################################################
## 7.1 매개변수 개수에 구애받지 않는 함수 작성
# 입력 매개변수 개수에 제한이 없는 함수를 작성하고 싶다
################################################################################################################
# 위치 매개변수의 개수에 제한이 없는 함수를 작성하려면 * 인자를 사용한다
def avg(first, *rest):
    return (first + sum(rest)) / (1 + len(rest))

# 샘플
avg(1,2)            # 1.5
avg(1,2,3,4)        # 2.5

## 이 예제에서 rest에 추가적 위치 매개변수가 튜플로 들어간다.
# 키워드 매개변수 수에 제한이 없는 함수를 작성하려면 **로 시작하는 인자를 사용한다
import html

def make_element(name, value, **attrs):
    keyvals = [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(
                name = name,
                attrs = attr_str,
                value = html.escape(value))
    return element

# 예제
# '<item size="large" quantity="6">Albatross</item>' 생성
make_element('item','Albatross',size='large',quantity=6)

# '<p>&lt;spam&gt;</p>' 생성
make_element('p','<spam>')


## attrs은 전달받은 키워드 매개변수(만약 있다면)를 저장하는 딕셔너리이다
# 위치 매개변수와 키워드 매개변수를 동시에 받는 함수를 작성하려면, *와 **를 함께 사용하면 된다
def anyargs(*args, **kwargs):
    print(args)             # 튜플
    print(kwargs)           # 딕셔너리

# 이 함수에서 모든 위치 매개변수는 튜플 args에, 모든 키워드 매개변수는 딕셔너리 kwargs에 들어간다

## *는 함수 정의의 마지막 위치 매개변수 자리에만 올 수 있다. **는 마지막 매개변수 자리에만 올 수 있다.
## 그리고 * 뒤에도 매개변수가 또 나올 수 있다는 것이 함수 정의의 미묘한 점이다
def a(x, *args, y):
    pass

def b(x, *args, **kwargs):
    pass





###############################################################################################################
## 7.2 키워드 매개변수만 받는 함수 작성
# 키워드로 지정한 특정 매개변수만 받는 함수가 필요하다
################################################################################################################
# 이 기능은 키워드 매개변수를 * 뒤에 넣거나 이름없이 * 만 사용하면 간단히 구현할 수 있다
def recv(maxsize, *, block):
    'Receives a message'
    pass

recv(1024, True)            # TypeError
recv(1024, block=True)      # Ok

# 이 기술로 숫자가 다른 위치 매개변수를 받는 함수에 키워드 매개변수를 명시할 때 사용할 수도 있다
def minimum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m

minimum(1, 5, 2, -5, 10)                # -5 반환
minimum(1, 5, 2, -5, 10, clip=0)        # 0 반환


## 키워드로만 넣을 수 있는 인자는 추가적 함수 인자를 명시할 때 코드의 가독성을 높이는 좋은 수단이 될 수 있다
msg = recv(1024, False)

# recv()가 어찌 동작하는지 잘 모른다면 False가 뭐냐?? 라고 하겠지. 그러니 아래처럼 표시해주면 이해가 훨 좋겠죠?
msg = recv(1024, block=False)



###############################################################################################################
## 7.3 함수 인자에 메타데이터 넣기
# 함수를 작성했다. 이때 인자에 정보를 추가해서 다른 사람이 함수를 어떻게 사용해야 하는지 알 수 있도록 하고 싶다
################################################################################################################
# 함수 인자 주석으로 프로그래머에게 이 함수를 어떻게 사용해야 할지 정보를 줄 수 있다
def add(x:int, y:int) -> int:
    return x + y

# 파이썬 인터프리터는 주석에 어떠한 의미도 부여하지 않는다. 단지 소스 코드를 읽는 사람이 이해하기 쉽도록 설명할 뿐이다
help(add)
# help on function add in module __main__:
# add(x: int, y: int) -> int


## 함수 주석은 함수의 __annotations__ 속성에 저장된다
add.__annotations__
# 결과값 : {'y':<class 'int'>, 'return':<class 'int'>, 'x':<class 'int'>}




###############################################################################################################
## 7.4 함수에서 여러 값을 반환
# 함수에서 값을 여러개 반환하고 싶다
################################################################################################################
# 튜플 써 ㅇㅇ
def myfun():
    return 1,2,3

a,b,c = myfun()
print(a)
# 결과값 : 1
print(b)
# 결과값 : 2
print(c)
# 결과값 : 3


## myfun()이 값을 여러개 반환하는 것처럼 보이지만, 사실은 튜플 하나를 반환한 것이다
# it looks awkward .. 실제로 튜플을 생성하는 것은 쉼표지 괄호가 아니당
a = (1,2)                           ## 괄호 사용
print(a)
# 결과값 : (1, 2)
b = 1, 2                            ## 괄호 미사용
print(b)
# 결과값 : (1, 2)


## 튜플을 반환하는 함수를 호출할 때, 결과값을 여러 개의 변수에 넣는 것이 일반적이다
# 그게 1.1에 나왔던 튜플 언패킹인데... 잊어버렸죠 ^^
x = myfun()
print(x)
# 결과값 : (1, 2, 3)               # 반환값을 변수 하나에 할당할 수도 있습니다




###############################################################################################################
## 7.5 기본 인자를 사용하는 함수 정의
# 함수나 메소드를 정의할 때 하나 혹은 그 이상 인자에 기본값을 넣어 선택적으로 사용할 수 있도록 하고 싶다
################################################################################################################
# 표면적으로 선택적 인자를 사용하는 함수를 정의하는 방법, 함수 정의부에 값을 할당하고 가장 뒤에 이를 위치시킨다
def spam(a, b=42):
    print(a,b)

spam(1)             # Ok. a=1, b=42
spam(1,2)           # Ok. a=1, b=2


## 기본값이 리스트, 세트, 딕셔너리 등 수정 가능한 컨테이너여야 한다면 None을 사용해 다음과 같이 코드를 작성한다
# 기본값으로 리스트 사용
def spam(a,b=None):
    if b is None:
        b = []
        # ...


## 기본값을 제공하는 대신 함수가 받은 값이 특정 값인지 아닌지 확인하려면 다음 코드를 사용한다
_no_value = object()

def spam(a,b=_no_value):
    if b is _no_value:
        print('No b value supplied')
        # ...


## 함수의 동작방법
spam(1)
# No b value supplied
spam(1,2)                   # b = 2                 여기값과 아래값의 차이점에 주목하세요
spam(1, None)              # b = None


## 기본 인자를 갖는 함수를 정의할 때
# 첫번째, 할당하는 기본 값은 함수를 정의할 때, 한 번만 정해지고 그 이후에는 변하지 않는다
x = 42
def spam(a, b=x):
    print(a,b)

spam(1)
# 1 42
x = 23                      # 효과없음 ㅎㅎ
spam(1)
# 1 42


# 두번째, 기본값으로 사용하는 값은 None, True, False, 숫자, 문자열같이 항상 변하지 않는 객체를 사용해야 한다
# 변수에 리스트같은거 넣어주면 안됨!!


###############################################################################################################
## 7.6 이름없는 함수와 인라인 함수 정의
# sort() 등에 사용할 짧은 콜백 함수를 만들어야 하는데, 한 줄짜리 함수를 만들면서 def 구문까지 사용하고 싶지는 않다
# 그 대신 in line(인라인)이라 불리는 짧은 함수를 만들고 싶다
################################################################################################################
# 표현식 계산 외에 아무 일도 하지 않는 간단한 함수는 lambda 람다람다람다람쥐

add = lambda x,y: x+y               # def add(x, y):                람다와 이 함수 둘 다 동일한 함수이다
add(2,3)                             #      return x + y
# 5


names = ['Luke Skywalker','Darth Vader',
         'Optimus Prime','Starscream']
sorted(names, key=lambda name: name.split()[-1].lower())

# ['Optimus Prime', 'Luke Skywalker', 'Starscream', 'Darth Vader'] 옵티머스 프라이이이임



###############################################################################################################
## 7.7 이름없는 함수에서 변수 고정
# lambda를 사용해서 이름없는 함수를 정의했는데, 정의할 때 특정 변수의 값을 고정하고 싶다
################################################################################################################
x = 10
a = lambda y: x + y
print(a(10))
# 결과값이 얘는 20

y = 20
b = lambda y: x + y
print(b(10))
# 결과값이 얘도 20이 나오는데요 쿡북님??!!?!?

x = 15
print(a(10))
# 얘는 25

x = 3
print(a(10))
# 13

## 이름없는 함수를 정의할 때 특정 값을 고정하고 싶으면 그 값을 기본 값으로 지정하면 된다.
x = 10
a = lambda y, x=x: x + y
x = 20
b = lambda y, x=x: x + y
print(a(10))
print(b(10))
# 엥 30나옴..


## 똑똑하게 람다 표현식을 쓰려면 아래처럼
funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
    print(f(0))

# 0
# 1
# 2
# 3
# 4

