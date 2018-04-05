import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model, load_model
from keras.layers import Input, Activation, Dropout, Flatten, Dense, Reshape, merge
from keras import optimizers
from keras.layers.normalization import BatchNormalization as BN
from keras.layers.core import Dropout
from keras.applications.vgg16 import VGG16
import numpy as np
import os
from PIL import Image
import glob
import pickle
import sys
import random
import json

# 学習も後々使うみたいなので、整備が必要 
input_tensor = Input(shape=(224, 224, 3))
vgg16_model = VGG16(include_top=False, weights='imagenet', input_tensor=input_tensor)
for layer in vgg16_model.layers[:12]:
  layer.trainable = False

x = vgg16_model.layers[-1].output
x = Flatten()(x)
x = BN()(x)
x = Dense(5000, activation='relu')(x)
x = Dropout(0.3)(x)
x = Dense(5000, activation='sigmoid')(x)
model = Model(inputs=vgg16_model.input, outputs=x)
model.compile(loss='binary_crossentropy', optimizer='adam')


def train():
    for i in range(500):
        print('now iter {} load pickled dataset...'.format(i))
        Xs = []
        ys = []
        names = [name for idx, name in enumerate(glob.glob('/mnt/sda/asano/illustration2vec/pkl/*'))]
        random.shuffle(names)
        
        for idx, name in enumerate(names):
            try:
                X, y = pickle.loads(open(name, 'rb').read())
            except EOFError as e:
                continue

            if idx%100 == 0:
                print('now scan iter ', idx)
            
            if idx >= 15000:
                break

            Xs.append(X)
            ys.append(y)

        Xs = np.array(Xs)
        ys = np.array(ys)
        model.fit(Xs, ys, epochs=1)
        print('now iter {}'.format(i))
        model.save_weights('models/{:09d}.h5'.format(i))


def pred():
    model.load_weights(sorted(glob.glob('/home/ubuntu/repos/tech-tools/illustration2vec/models0/*'))[-1])

    tag_idx = json.loads(open('/home/ubuntu/repos/tech-tools/illustration2vec/tag_index.json', 'r').read())
    index_tag = {index:tag for tag, index in tag_idx.items()}

    # 現在はgoogle VisionAPIの蒸留モデルで予測精度検証中
    # パスをStormRulerに変える
    for name in glob.glob('/home/ubuntu/s3_mnt/outputs/i2v_ad/resized_pkl/*.pkl'):
        x, Y = pickle.loads(open(name, 'rb').read())
        print(np.array([Y]))
        result = model.predict(np.array([Y]))
        result = result.tolist()[0]
        result = {i:w for i, w in enumerate(result)}
        
        tag_dic = {}
        pkl_name = '/home/ubuntu/s3_mnt/outputs/i2v_ad/predict/' + name.split('/').pop().replace('.pkl','_rlt.pkl')

        # 追記モードで開けるかな?
        with open(pkl_name, 'wb') as pkl:
            for i, w in sorted(result.items(), key=lambda x:x[1]*-1)[:30]:
                print("{name} tag ={tag} prob={prob}".format(name=name, tag=index_tag[i], prob=w))
                tag_dic[index_tag[i]] = w

            # 今pickleに書き込んでるけど、連携のことを考えるとjsonがいいかも
            l = [Y, tag_dic]
            pkl.write(pickle.dumps(l))
            #pkl.write(pickle.dumps(Y))
            #pkl.write(pickle.dumps(tag_dic))


if __name__ == '__main__':
    if  '--train' in sys.argv:
        train()
    if '--pred' in sys.argv:
        pred()

