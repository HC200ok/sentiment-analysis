import pandas as pd
import json
import nlp

def preprocess(file_name):
  data = pd.read_json("./origin/{}.json".format(file_name))
  # remove useless properties
  del data['html']
  del data['timestamp']
  del data['url']
  del data['user']
  del data['retweets']
  del data['replies']
  del data['fullname']
  del data['id']
  del data['likes']

  data['text'] = data['text'].map(lambda x: nlp.preprocess(x))

  data = data.to_json(orient = 'records',force_ascii = False)

  data = json.loads(data)

  with open("./processed/{}.json".format(file_name), "w", encoding = "utf-8") as f:
    json.dump(data, f, ensure_ascii = False)

emotions = ["happy", "sad", "disgust", "angry", "fear", "surprise"]

for i, es in enumerate(emotions):
  preprocess(es)
