import requests
import random
from bs4 import BeautifulSoup
from urllib import parse
from sentimentja import Analyzer
analyzer = Analyzer()

user_agents =  ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']

headers = {'User-Agent': random.choice(user_agents)}

def getSearchResIds(p):
  search_url = 'https://news.yahoo.co.jp/search?p={}&ei=UTF-8&fr=news_sw&vaop=a&to=0&st=n&c_n=c_int'.format(p)

  r = requests.get(search_url, headers = headers)

  content = r.text

  soup = BeautifulSoup(content, 'lxml')

  results = soup.find(id = 'NSm').find_all(class_ = 'cf')

  if len(results) == 0:
    return {}

  # result = results[9]

  a_list = []

  for result in results:

    a = result.find(class_ = 't').find('a')

    title = a.text
    href = a['href']

    parseResult = parse.urlparse(href)

    param_dict = parse.parse_qs(parseResult.query)

    a_list.append({ "title": title, "id": param_dict['a'][0] })

  return a_list

def getCommentsUrl(id):
  url = 'https://headlines.yahoo.co.jp/cm/main?d=' + id

  r = requests.get(url, headers = headers)

  content = r.text

  soup = BeautifulSoup(content, 'lxml')

  plugin = soup.find(class_ = 'news-comment-plugin')

  if plugin == None:
    return False

  origin = 'https%3A%2F%2Fheadlines.yahoo.co.jp'
  sort = plugin['data-sort']
  order = plugin['data-order']
  # 页数
  page = plugin['data-page']
  type = plugin['data-page-type']
  keys = plugin['data-keys']
  full_page_url = plugin['data-full-page-url']
  # 数量
  # comment_num = plugin['data-comment-num']
  comment_num = 50
  bkt = 'paid001'
  grp = plugin['data-grp']
  opttype = plugin['data-opttype']

  url = 'https://news.yahoo.co.jp/comment/plugin/v1/full/?origin={}&sort={}&order={}&page={}&type={}&keys={}&full_page_url={}&comment_num={}&bkt={}&grp=hdl&opttype={}'.format(origin, sort, order, page, type, keys, full_page_url, comment_num, bkt, grp,opttype)

  return url

def getComments(url):
  r = requests.get(url, headers = headers)

  content = r.text

  soup = BeautifulSoup(content, 'lxml')

  number = soup.find(class_ = 'num').find('dd').get_text()

  if number == '0':
    return { 'number': '0', 'items': [] }

  list = soup.find(id = 'comment-list-item')

  lis = list.find_all(class_ = 'commentListItem')


  items = []

  for item in lis:
    comment = item.find(class_ = 'comment').find('span').get_text()
    items.append(comment)
  return { 'number': number, 'items': items }

def comments(id):
  url = getCommentsUrl(id)
  res = {}
  if url == False:
    res["comment_num"] = 0
    res["comments"] = []
  else:
    comments = getComments(url)
    res["comment_num"] = comments['number']
    res["comments"] = analyzer.analyze(comments['items'])
  return res
