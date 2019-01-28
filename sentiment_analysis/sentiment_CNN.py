import pandas as pd
from sklearn.utils import shuffle

list = []
size = 2900
df = []

emotions = ["happy", "sad", "disgust", "angry", "fear", "surprise"]

for i, es in enumerate(emotions):
  data = shuffle(pd.read_json("./data/processed/{}.json".format(es))).iloc[:int(size)]
  data['label'] = i
  df.append(data)

df = pd.concat(df)
df = shuffle(df)
X = df['text']
y = df['label']
df.shape  #不是数组

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

max_features = 2000
maxlen = 100

# 特征化：
# 1. text的特征化   Tokenizer()
# 2. label的特征化  to_categorical()
# label: 1 => [0,1,0,0,0,0]
y = to_categorical(y)

# 切割测试
X_train, X_test, y_train, y_test = train_test_split(X, y)

# 用keras的Tokenizer进行文本预处理，序列化，向量化等
# 简单讲解Tokenizer如何实现转换。当我们创建了一个Tokenizer对象后，使用该对象的fit_on_texts()函数，可以将输入的文本中的每个词编号，编号是根据词频的，词频越大，编号越小。可能这时会有疑问：Tokenizer是如何判断文本的一个词呢？其实它是以空格去识别每个词。因为英文的词与词之间是以空格分隔，所以我们可以直接将文本作为函数的参数，但是当我们处理中文文本时，我们需要使用分词工具将词与词分开，并且词间使用空格分开。具体实现如下：
def preprocess(data, tokenizer, maxlen = maxlen):
    return(pad_sequences(tokenizer.texts_to_sequences(data), maxlen = maxlen))
tokenizer = Tokenizer(num_words = max_features, char_level = True)
tokenizer.fit_on_texts(X_train)

X_train = preprocess(X_train, tokenizer, maxlen)
X_test = preprocess(X_test, tokenizer, maxlen)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train)
X_train.shape, X_val.shape, X_test.shape

print(X_train.shape)
print(X_val.shape)
print(X_test.shape)

from keras.layers import Input, Dense, Embedding, Flatten
from keras.layers import SpatialDropout1D
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.models import Sequential

# 使用Sequential模型来实现极为方便
model = Sequential()
model.add(Embedding(max_features, 150, input_length = maxlen))

# Dropout 层还是非常重要的，值得一提。 Dropout 是一种方法能正则化我们的模型，防止出现过拟合。
model.add(SpatialDropout1D(0.2))

# 卷积过滤器的数量、每个卷积内核中的行数、每个卷积内核中的列数。
model.add(Conv1D(32, kernel_size = 3, padding = 'same', activation = 'relu'))

# MaxPooling2D 是一种减少模型中参数的方法，方式是在之前的层上滑动一个 2x2 的池化过滤器，在 2x2 过滤器中取 4 个值的最大值
model.add(MaxPooling1D(pool_size = 2))

# 卷积层(Conv Layer)
model.add(Conv1D(64, kernel_size = 3, padding = 'same', activation = 'relu'))

# 池化层(Pooling Layer)
model.add(MaxPooling1D(pool_size = 2))

# 最后再输出之前我们需要将上述几个层的输出作为全连接层的输入。由于卷积层和池化层的输出是2D的，因此需要将其压平，此时需要用到Flatten
model.add(Flatten())

# 最后一层的输出大小为 6，对应了情感的 6 个类别。
# 全连接层(Dense Layer)
# 如果分类的类别过多地话则可以用softmax作为激活函数)
model.add(Dense(6, activation = 'softmax'))

# 现在只需编译模型，就可以训练它了。在我们编译模型时，会声明损失函数和优化器（SGD，Adam 等等）。
model.compile(loss = 'categorical_crossentropy', optimizer = 'rmsprop', metrics = ['accuracy'])

epochs = 15
batch_size = 500

model.fit(X_train, y_train, validation_data = (X_val, y_val), epochs = epochs, batch_size = batch_size)


from sklearn.metrics import classification_report

import numpy as np
y_preds =  model.predict(X_test)
y_preds =  np.argmax(y_preds, axis=1)
y_true = np.argmax(y_test, axis=1)

emolabels = []
for e in emotions:
  emolabels.append(e)

print(classification_report(y_true, y_preds, target_names = emolabels))


examples = [
    "まじきもい、あいつ",
    "今日は楽しい一日だったよ",
    "ペットが死んだ、実に悲しい",
    "ふざけるな、死ね",
    "ストーカー怖い",
    "すごい！ほんとに！？",
    "葉は植物の構成要素です。",
    "ホームレスと囚人を集めて革命を起こしたい"
]

targets = preprocess(examples, tokenizer, maxlen=maxlen)
print('\t'.join(emolabels))
for i, ds in enumerate(model.predict(targets)):
  print('\t'.join([str(round(100.0*d)) for d in ds]))
