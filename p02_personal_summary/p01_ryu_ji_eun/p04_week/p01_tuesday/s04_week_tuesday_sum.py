###############################################################################################################
## 5.14 Bypassing filename encoding (파일 이름 인코딩 우회)
# u want to perform file i/o operations using raw filenames that have not been decoded or encoded
# according to the default filename encoding                 #...no I'm not -ㅁ-
###############################################################################################################
# by default, all filenames are encoded and decoded according to the text encoding returned by
# sys.getfilesystemencoding()         겟 파일 시스템 인코딩

sys.getfilesystemencoding()
# sys.getfilesystemencoding()
# 'utf-8'

## if u wanna bypass this encoding for some reason,specify a filename using a raw byte string instead
# write a file using a unicode filename
with open('jalape\xf1o.txt','w') as f:
    f.write('Spicy!')

# directory listing (decoded)
import os
os.listdir('.')
# 'jalapeño.txt'

# directory listing (raw)
os.listdir(b'.')


# open file with raw filename
with open(b'jalapen\xcc\x83o.txt') as f:
    print(f.read())
# spicy!


# many operating systems may allow a user throught accident or malice to create files with names that
# don't conform to the expected encoding rules. Such filenames may mysteriously break Python programs
# that work with a lot of files.

## READING DIRECTORIES AND WORKING WITH FILENAMES AS RAW UNDECODED BYTES HAS THE POTENTIAL TO AVOID SUCH
# PROBLEMS, ALBEIT AT THE COST OF PROGRAMMING CONVENIENCE.




###############################################################################################################
## 5.15 Printing Bad filenames
# your program received a directory listing, but when it tried to print the filenames, it crashed with a
# UnicodeEncodeError exception and a cryptic message about "surrogates not allowed"
################################################################################################################
# when printing filenames of unknown origin, use this convention to avoid errors

def bad_filename(filename):
    return repr(filename)[1:-1]

try:
    print(filename)
except UnicodeEncodeError:
    print(bad_filename(filename))


# this recipe is about a potentially rare but very annoying problem regarding programs that must manipulate
# the filesystem. By default, Python assumes that all filenames are encoded according to the setting reported by
# sys.getfilesystemencoding()

# when executing a command such as os.listdir(), bad filenames leave Python in a bind. On the one hand, it can't
# just discard bad names. on the other hand, it still can't turn the filename into a proper text string.
# so.. Python's solution to this problem is to take an undecodable byte value \xhh in a filename and map it into
# a so-called "surrogate encoding" represented by the Unicode character \ydchh.

import os
files = os.listdir('.')
files
# result : ['spam.py','b\udce4d.txt','foo.txt']


# if u have code that manipulates filenames or even passes them to functions such as open(), eveything works
# normally. It's only in situations where you want to output the filename that you run into trouble
# specifically, if you tried to print the preceding listing, your program will crash

for name in files:
    print(name)
# 유니코드 인코드 에러 뜸. 그러니 아래처럼 쓰세요

for name in files:
    try:
        print(name)
    except UnicodeEncodeError:
        print(bad_filename(name))

# spam.py
# b\udce4d.txt
# foo.txt


def bad_filename(filename):
    temp = filename.encode(sys.getfilesystemencoding(),
    return temp.decode('latin-1')

for name in files:
    try:
        print(name)
    except UnicodeEncodeError:
        print(bad_filename(name))
# spam.py
# bad.txt
# foo.txt





###############################################################################################################
## 5.16 Adding or Changing the encoding of an already open file
# you want to add or change the Unicode encoding of an already open file without closing it first
################################################################################################################
# If you want to add Unicode encoding/decoding to an alredy existing file object that's opened in binary mode
# wrap it with an io.TextIOWrapper() object
import urllib.request
import io
u = urllib.request.urlopen('http://www.python.org')
f = io.TextIOWrapper(u,encoding='utf-8')
text = f.read()

# if you want to change the encoding of an alreday open text-mode file, use its detach() method to remove the
# existing text encoding layer before replacing it with a new one.
# sys.stdout example

import sys
sys.stdout.encoding
# utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(),encoding='latin-1')
sys.stdout.encoding
# latin-1

## The i/o system is built as a series of layers. You can see the layers yourself by trying this simple
# example involging a text file
f = open('sample.txt','w')
f
# <_io.TextIOWrapper name='sample.txt' mode='w' encoding='cp949'>
f.buffer
# <_io.BufferedWriter name='sample.txt'>
f.buffer.raw
# <_io.FileIO name='sample.txt' mode='wb' closefd=True>



###############################################################################################################
## 5.17 writing bytes to a text file
# you want to write raw bytes to a file opened in text mode
################################################################################################################
# simply write the byte data to the files underlying buffer.
import sys
sys.stdout.write(b'Hello\n')
# typeError 납니다. must be str, not bytes

# similarly, binary data can be read from a text file by reading from its buffer attribute instead

# the i/o system is built from layers. Text files are constructed by adding a unicode encoding/decoding layer
# on top of a buffered binary-mode file. the buffer attribute simply points at this underlying file.



###############################################################################################################
## 5.18 wrapping an existing file descriptor as a file object
# you have an integer file descriptor corresponding to an already open i/o channel on the operating system,
# and you want to wrap a higher-level python file object around it
################################################################################################################
# a file descriptor is different than a normal open file in that it is simply an integer handle assigned by
# the operating system to refr to some kind of system i/o channel. if you happen to have such a file descriptor,
# you can wrap a Python file object around it using the open() function.

# open a low-level file descriptor
import os
fd = os.open('somefile.txt', os.O_WRONLY | os.O_CREAT)

# turn into a proper file
f = open(fd,'wt')
f.write('hello world\n')
f.close()

# on unix systems, this technique of wrapping a file descriptor can be a convenient means for putting a file-like
# interface on an existing i/o channel that was opened in a different way

from socket import socket, AF_INET, SOCK_STREAM
def echo_client(client_sock, addr):
    print('Got connection from', addr)

    client_in = open(client_sock.fileno(), 'rt',encoding='latin-1',closefd=False)
    client_out = open(client_sock.fileno(),'wt',encoding='latin-1',closefd=False)

    for line in client_in:
        client_out.write(line)
        client_out.flush()
    client_sock.close()


def echo_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    while True:
        client, addr = sock.accept()
        echo_client(client, addr)

# it's important to emphasize that the above example is only meant to illustrate a feature of the buit-in
# open() function and that it only works on Unix-based systems. if you are trying to put a file-like
# interface on a socket and need your code to be cross platform, use the makefile() method of sockets instead

# But- it portability is not a concern, you'll find that the above solution provides much better performance
# than using makefile()

import sys
# create a binary-mode file form stdout
bstdout = open(sys.stdout.fileno(), 'wb', closefd=False)
bstdout.write(b'Hello world\n')
bstdout.flush()




###############################################################################################################
## 5.19 Making temporary files and directories
# you need to create a temporary file or directory for use when your program executes
# afterward, you possibily want the file or directory to be destroyed
################################################################################################################
## The tempfile module has a variety of functions for performing this task. To make an unnamed temporary file,
# use tempfile.TemporaryFile

from tempfile import TemporaryFile
with TemporaryFile('w+t') as f:
    # read/write to the file
    f.write('hello world\n')
    f.write('Tesing\n')

    f.seek(0)
    data = f.read()

# or if you prefer, you can also use file like this
f = TemporaryFile('w+t')
f.close()


## discussion
# the TemoraryFile(), NamedTemporaryFile(), and TemporaryDirectory() functions are probably the most convenient
# way to work with temporary files and directories, because they automatically handle all of the steps of
# creation and subsequent cleanup. at a lower level, you can also use the mkstemp() and mkdtemp() to create
# temporary files and directories
import tempfile
tempfile.mkstemp()
tempfile.mkdtemp()
# C:\\Users\\soohyun\\AppData\\Local\\Temp\\tmpxi9l5fqk'


## however, these fuctions don't really take care of further management. for example, the mkstemp() function
# simply returns a raw OS file descriptor and leaves it up to you to turn it into a proper file. Similarity,
# it's up to you to clean up the files if you want



###############################################################################################################
## 5.20 Communicating with serial ports
# you want to read and write data over a serial port, typically to interact with some kind of hardware device
################################################################################################################
## Although you can probably do this directly using Python's built-in i/o primitives, your best bet for serial
# communication is to use the pySerial package.
import serial
ser = serial.Serial('/dev/tty.usbmodem641',
                    baudrate=9600,
                    bytesize=8,
                    parity='N',
                    stopbits=1)



###############################################################################################################
## 5.21 serializing python objects
# you need to serialize a Python object into a byte stream so that you can do things such as save it to a file,
# store it in a database, or transmit it over a network connection
################################################################################################################
# the most common approach for serializing data is to use the pickle module. to dump an object to a file
import pickle
data = ... # some python object
f = open('somefile','wb')
pickle.dump(data,f)

# to dump an object to a string, use pickle.dumps()
s = pickle.dumps(data)

# to re-create an object from a byte stream, use either the pickele.load() or pickle.loads() functions
## restore from a file
f = open('somefile','rb')
data = pickle.load(f)

# restore frokm a string
data = pickle.loads(s)


# for most programs, usage of the dump() and load() function is all you need to effectively use pickle.
# it simply works with most Python data types and instances of user-defined classes.
# if you're working with any kind of library that lets you do things such as save/restore Python objects in
# databases or transmit objects over the network, there's a pretty good chance that pickle is being used.

# pickle is a Python-specific self-describing data encoding. By self-describing, the serialized data contains
# information related to the start and end of each object as well as information about its type.
import pickle
f = open('somedata','wb')
pickle.dump([1,2,3,4],f)
pickle.dump('hello',f)
pickle.dump({'apple','pear','banana'},f)
f.close()
f = open('somedata','rb')
pickle.load(f)
# [1,2,3,4]
pickle.load(f)
# 'hello'
pickle.load(f)
# {'apple','pear','banana'}

import time
import threading

class Countdown:
    def __init__(self,n):
        self.n = n
        self.thr = threading.Thread(target=self.run)
        self.thr.daemon = True
        self.thr.start()

    def run(self):
        while self.n > 0:
            print('T-minus',self.n)
            self.n -= 1
            time.sleep(5)

    def __getstate__(self):
        return self.n

    def __setstate__(self,n):
        self.__init__(n)


## try the following experiment involging pickling
import countdown
c = countdown.Countdown(30)
T-minus 30

# after a few moments
f = open('cstate.p','wb')
import pickle
pickle.dump(c,f)
f.close()


# now quit python and try this after restart
f = open('cstate.p','rb')
pickle.load(f)




###############################################################################################################
## 6.1 reading and writing CSV data
# you want to read or write data encoded as a csv file
################################################################################################################
# for most kinds of csv data, use the csv library. for example, supopose you have some stock market data
# in a file named stocks.csv like ... awkward..

# here's how you would read the data as a sequence of tuples
import csv
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        # process row   ...


# since such indexing can often be confusing, this is one place where you might want to consider the use of
# named tuples
from collections import namedtuple
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row',headings)
    for r in f_csv:
        row = Row(*r)
        # process row


# this would allow you to use the column headers such as row.Symbol and row. Change instead of indices.
# it should be noted that this only works if the column headers are valid Python identifiers
# if not, you might have massage the initial headings

## 으아아아아아아아아아아아아아아아아~~~ 원서니까 당연하다곤 해도 뭐 이리 영어판이냐아아아아아아아아아아.

# another alternative is to read the data as a sequence of dictionaried instead.
import csv
with open('stocks.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        # process row..


# in this version, you would access the elements of each row using the row headers
# for example, row['Symbol'] or row['Change']
# to write csv data, you also use the csv module but create a writer object
headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('AA',39.48, '6/11/2007','9:36am',-0.18,181800),
        ('AIG',71.38,'6/11/2007','9:37am',-0.15,195500),
        ('AXP',62.58,'6/11/2007','9:36am',-0.46,935000)]

with open('stocks.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)


# if you have the data as a sequence of dictionaries
headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('Symbol':'AA','Price':39.48,'Date':'6/11/2007','Time':'9:36am','Change':-0.18,'Volume':181800),
        ('Symbol':'AIG','Price':71.38,'Date':'6/11/2007','Time':'9:37am','Change':-0.15,'Volume':195500),
        ('Symbol':'AXP','Price':62.58,'Date':'6/11/2007','Time':'9:36am','Change':-0.46,'Volume':935000)]

with open('stocks.csv','w') as f:
    f_csv = csv.DictWriter(f,headers)
    f_csv.writeheader()
    f_csv.writerows(rows)


import re
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headers = [re.sub('[^a-zA-Z_','_',h) for h in next(f_csv)]
    Row = namedtuple('Row',headers)
    for r in f_csv:
        row = Row(*r)
        # process row...



col_types = [str, float, str, str, float, int]
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for rokw in f_csv;
        # apply conversions to the row items
        row = tuple(convert(value) for convert, value in zip(col_types, row))
        # ...

# alternatively, here is an example of converting selected fields of dictionaries
print('Reading as dicts with type conversion')
field_types = [('Price',float),
               ('Change',float),
               ('Volumne',int)]

with open('stocks.csv') as f:
    for row in csv.DictReader(f):
        row.update((key, conversion(row[key]))
                   for key, conversion in field_types)
        print(row)




###############################################################################################################
## 6.2 reading and writing JSON data
# you want to read or write data encoded as a json file
################################################################################################################
# the json module provides an easy way to encode and decode data in JSON. the two main functions are
# json.dumps() and json.loads(), mirroring the interface used in other serialization libraries, such as pickle
import json
data = {
    'name':'ACME',
    'shares':100,
    'price':542.23
}
json_str = json.dumps(data)


# writing JSON data
with open('data.json','w') as f:
    json.dump(data,f)

# reading data back
with open('data.json','r') as f:
    data = json.load(f)



from urllib.request import urlopen
import json
u = urlopen('http://search.twitter.com/search.json?q=python&rpp=5')
resp = json.loads(u.read().decode('utf-8'))
from pprint import pprint
pprint(resp)
{'completed_in': 0.074,
 'max_id': 264043230692245504,
 'max_id_str': '264043230692245504',
 'next_page': '?page=2&max_id=264043230692245504&q=python&rpp=5',
 'page': 1,
 'query': 'python',
 'refresh_url': '?since_id=264043230692245504&q=python',
 'results': [{'created_at': 'Thu, 01 Nov 2012 16:36:26 +0000',
              'from_user': ...
             },
             {'created_at': 'Thu, 01 Nov 2012 16:36:14 +0000',
              'from_user': ...
             },
             {'created_at': 'Thu, 01 Nov 2012 16:36:13 +0000',
              'from_user': ...
             },
             {'created_at': 'Thu, 01 Nov 2012 16:36:07 +0000',
              'from_user': ...
             }
             {'created_at': 'Thu, 01 Nov 2012 16:36:04 +0000',
              'from_user': ...
             }],
 'results_per_page': 5,
 'since_id': 0,
 'since_id_str': '0'}


# here's how you could turn a json dictionary into a Python object
class JSINobject:
    def __init__(self,d):
        self.__dict__=d

data = json.loads(s, object_hook=JSONobject)
data.name
# 'ACME'
data.shares
# 50
data.price
# 490.1



###############################################################################################################
## 6.3 parsing simple xml data
# you would like to extract data from a simple xml document
################################################################################################################
# the xml.etree.ElementTree module can be used to extract data from simple xml documents.
# to illustrate, suppose you want to parse and make a summary of the RSS feed on Planet Python
from urllib.request import urlopen
from xml.etree.ElementTree import parse

# download the RSS feed and parse it
u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(u)

# extract and output tags of interest
for item in doc.iterfind('channel/item'):
    title = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')

    print(title)
    print(date)
    print(link)
    print()





###############################################################################################################
## 6.4 parsing huge xml files incrementally
# you need to extract data from a huge XML document using as little memory as possible
################################################################################################################
# any time you are faced with the problem of incremental data processing, you should think of iterators and
# generators
from xml.etree.ElementTree import iterparse

def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start','enc'))
    # skip the root element
    next(doc)

    tag_stack = []
    elem_stact = []
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


# suppose you want to write a script that ranks ZIP codes by the number of pothole reports
from xml.etree.ElementTree import parse
from collections import Counter

potholes_by_zip = Counter()

doc = parse('potholes.xml')
for pothole in doc.iterfind('row/row'):
    potholes_by_zip[pothole.findtext('zip')] += 1

for zipcode, num in potholes_by_zip.most_common():
    print(zipcode,num)





