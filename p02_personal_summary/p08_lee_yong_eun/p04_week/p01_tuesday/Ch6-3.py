##########################################################################################################
# 6.3] 단순한 XML 데이터 파싱
#   * 단순 XML 문서에서 데이터를 얻고 싶다.
#       : xml.etree.ElementTree 모듈 사용
#         좀 더 고급 애플리케이션을 개발 중이라면 lxml을 사용하는 것도 고려할만하다.
##########################################################################################################

from urllib.request import urlopen
from xml.etree.ElementTree import parse

# RSS 피드 다운로드하고 파싱
u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(u)

# 관심 있는 태그를 뽑아서 출력한다.
for item in doc.iterfind('channel/item'):
    title = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')

    print(title)
    print(date)
    print(link)
    print()
    # Enthought: Press
    # Release: SciPy
    # 2017
    # Conference
    # to
    # Showcase
    # Leading
    # Edge
    # Developments in Scientific
    # Computing
    # with Python
    #     Mon, 05
    #     Jun
    #     2017
    #     18: 18:12 + 0000
    # http: // blog.enthought.com / general / press - release - scipy - 2017 - conference - showcase - leading - edge - developments - scientific - computing - python /
    #
    # Nikola: Nikola
    # v7
    # .8
    # .7 is out!
    # Mon, 05
    # Jun
    # 2017
    # 15: 07:46 + 0000
    # https: // getnikola.com / blog / nikola - v787 - is -out.html
    #
    # ...