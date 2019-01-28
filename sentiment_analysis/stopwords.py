import os
import urllib.request

def download_stopwords(path):
  url = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
  if os.path.exists(path):
    print('SlothLib File already exists.')
  else:
      print('Downloading...')
      urllib.request.urlretrieve(url, path)

def create(path):
  download_stopwords(path)
  stop_words = []
  for w in open(path, "r"):
      w = w.replace('\n','')
      if len(w) > 0:
        stop_words.append(w)
  return stop_words
