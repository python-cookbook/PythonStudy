         #5.14 파일 이름 인코딩 우회

with open('jalape\xf1o.txt', 'w') as f:
    f.write('Spicy!')
    
    
import os
os.listdir('.')

os.listdir(b'.')

with open(b'jalapen\xcc\x83o.txt') as f:
    print(f.read())
    

            #5.15 망기진 파일 이름 출력
            
def bad_filename(filename):
    return repr(filename)[1:-1]

try:
    print(filename)
except UnicodeEncodeError:
    print(bad_filename(filename))
    
    
    
    
            #5.16 이미 열려 있는 파일의 인코딩을 수정하거나 추가하기
            
import urllib.request
import io

u = urllib.request.urlopen('http://www.python.org')
f = io.TextIOWrapper(u, encoding='utf-8')
text = f.read()

import sys
sys.stdout.encoding

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
sys.stdout.encoding



            #5.17 텍스트 파일에 바이트 쓰기

import sys
sys.stdout.write(b'Hello\n')

sys.stdout.buffer.write(b'Hello\n')



            #5.18 기존 파일 디스크립터를 파일 객체로 감싸기
import os
fd = os.open('somefile.txt', os.O_WRONLY | os.O_CREAT)

f = open(fd, 'wt')
f.write('hello world\n')
f.close()

f=open(fd, 'wt', closefd=False)



            #5.19 임시 파일과 디렉터리 만들기

#이름없는 임시파일 생성
from tempfile import TemporaryFile

with TemporaryFile('w+t') as f:
    f.write('Hello World\n')
    f.wrtie('Testing\n')
    
    f.seek(0)
    data = f.read()
   
    
from tempfile import NamedTemporaryFile

with NamedTemporaryFile('w+t') as f:
    print('filename is:', f.name)
    
# 임시 디엑터리 생성    
from tempfile import TemporaryDirectory
with TemporaryDirectory() as dirname:
    print('dirname is:', dirname)
    
    
    
    
                        # Chapter 6 데이터 인코딩과 프로세싱
                        
            #6.1 CSV 데이터 읽고 쓰기
#stock.csv
Symbol,Price,Date,Time,Change,Volume
"AA",39.48,"6/11/2007","9:36am",-0.18,181800
"AIG",71.38,"6/11/2007","9:36am",-0.15,195500
"AXP",62.58,"6/11/2007","9:36am",-0.46,935000
"BA",98.31,"6/11/2007","9:36am",+0.12,104800
"C",53.08,"6/11/2007","9:36am",-0.25,360900
"CAT",78.29,"6/11/2007","9:36am",-0.23,225400

          
import csv
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        
from collections import namedtuple
with open('stock.csv') as f:
    f_csv=csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row',headings)
    for r in f_csv:
        row = Row(*r)
        
import csv
with open('stocks.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        
        
with open('stocks.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
    
    
with open('stocks.csv','w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)
    


            #6.2 JSON 데이터 읽고 쓰기
            
import json

data = {'name':'ACME', 'shares':100, 'price':542.23}
json_str = json.dumps(data)


data=json.loads(json_str)

with opne('data.json', 'w') as f:
    json.dump(data, f)
    
with open('data.json','r') as f:
    data = json.load(f)
    

            #6.3 단순한 XML 데이터 파싱
            
from urllib.request import urlopen
from xml.etree.ElementTree import parse

u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(u)

for item in doc.iterfind('channel/item'):
    title = item.findtext('title')
    data = item.findtext('pubDate')
    link = item.findtext('link')

    print(title)
    print(date)
    print(link)
    print()



            #6.4 매우 큰 XML 파일 증분 파싱하기

from xml.etree.ElementTree import iterparse

def parse_and_remove(filename, path):
    path_parts=path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    
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
            


from xml.etree.ElementTree import parse
from collectrions import Counter

potholes_by_zip = Counter()
doc=parse('potholes.xml')
for pothole in doc.iterfind('row/row'):
    potholes_by_zip[pothole.findtext('zip')] += 1
                    
for zipcode, num in potholes-by_zip.most_common():
    print(zipcode, num)
    
from collections import Counter
potholes-by_zip = Counter()

data = parse_and_remove('potholes.xml', 'row/row')
for pothole in data:
    potholes_by_zip[pothole.findtext('zip')] += 1

for zipcode, num in potholes_by_zip.most-common():
    print(zipcode, num)

    