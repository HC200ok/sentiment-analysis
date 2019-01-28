import MeCab
import unicodedata
import stopwords
import re

# create stopwords list
stop_words = stopwords.create("stop_words.txt")

# MeCab Initialization
# tagger = MeCab.Tagger('-Ochasen')
tagger = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
tagger.parse('') # <= 空文字列をparseする

def clean_noise(text):
  replaced_text = re.sub(r'[【】]', ' ', text)       # 【】の除去
  replaced_text = re.sub(r'[『』]', ' ', text)       # 『』の除去
  replaced_text = re.sub(r'[「」]', ' ', text)       # 「」の除去
  replaced_text = re.sub(r'[（）()]', ' ', replaced_text)     # （）の除去
  replaced_text = re.sub(r'[［］\[\]]', ' ', replaced_text)   # ［］の除去
  replaced_text = re.sub(r'[@＠]\w+', '', replaced_text)  # メンションの除去
  replaced_text = re.sub(r'pic.twitter.com\/\w+', '', replaced_text)
  replaced_text = re.sub(r'http\S+', '', replaced_text)  # URLの除去
  replaced_text = re.sub(r'　', ' ', replaced_text)  # 全角空白の除去
  return replaced_text

# print(clean_noise('aa http://apple.com/yzgjzzawcl 除去'))
# 数字の置き換えを行う理由は、数値表現が多様で出現頻度が高い割には自然言語処理のタスクに役に立たないことが多いからです。
def normalize_number(text):
  # 連続した数字を0で置換
  return re.sub(r'\d+', '0', text)

# 自然言語処理の前処理
def preprocess(text):
  # 1.テキストのクリーニング
  # 1.1 HTMLタグの除去はtwitterscraperがもうやりました
  # 1.2 URLなどのノイズの除去：
  text = clean_noise(text)
  # 2.A -> a
  text = text.lower()
  # 3.正規化处理
  text = unicodedata.normalize('NFKC', text)
  text = normalize_number(text)

  # 4.単語の分割 形態素解析
  node = tagger.parseToNode(text)
  keys = []
  while node:
    # 5.ストップワードの除去
    if node.surface not in stop_words:
      keys.append(node.surface)
    node = node.next
  return ' '.join(keys).strip()

