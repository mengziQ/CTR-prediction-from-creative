# Google vision APIの画像タグを一覧にするスクリプト

import glob
import json
import pickle

# また長い辞書作る・・・？
tags = {}
err_jsons = []

for name in glob.glob('/home/ubuntu/s3_mnt/outputs/i2v_ad/json/*'):
  with open(name,  'r') as js:
    obj = json.load(js)
    print(name)
    try:
      res = obj['responses'][0]
      tag_list = res['labelAnnotations']

    except Exception as e:
      print(e)
      err_jsons.append(name)
      continue

    for li in tag_list:
      if tags.get(li['description']) is None:
        tags[li['description']] = 1
      else:
        tags[li['description']] += 1

with open('tag_freq.pkl', 'wb') as tf:
  pickle.dump(sorted(tags.items(), key=lambda x: x[1]), tf)
