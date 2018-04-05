# 任意の要素が1であり、その他の要素が異なるベクトルを探索するスクリプト
import numpy as np
import re

with open('/home/ubuntu/repos/creative-predictor/ctr8.svm', 'r') as svm:
  obj = svm.readlines()
  tmp_list = []
  cnt = 0 

  # どうするか。高重要度のタグ上位30個のうちいずれか1つのみが1で、他は任意の値をとるベクトルを基準とする？
  for i, o in enumerate(obj):
    splited = o.split(' ')[1:1679]
    vector_list = [] 
    for sp in splited:
      vector_list.append(float(re.sub(r'[0-9]+:', '', sp)))
    
    std = np.array(vector_list)
    #print(len(std))
    if std[28] == 1:
      print('{}行目'.format(i + 1))
      #cnt += 1
      break
 
  print('基準ベクトル探索完了')

  cos_sim = 0.0
  cs_idx = 0

  for idx, o in enumerate(obj):
    if idx == i:
      continue
    else:
      splited = o.split(' ')[1:1679]
      vector_list = []
      for sp in splited:
        vector_list.append(float(re.sub(r'[0-9]+:', '', sp)))

      target = np.array(vector_list) 
      if target[28] != 1:
        print('{}行目'.format(idx + 1))
        new_cos_sim = np.dot(std, target) / (np.linalg.norm(std) * np.linalg.norm(target))
        if new_cos_sim > cos_sim:
          cos_sim = new_cos_sim
          cs_idx = idx

  print('最終結果')
  print('基準ベクトル: {}行目'.format(i))
  print('コサイン類似度最大のベクトル: {}行目'.format(cs_idx))
  print('コサイン類似度: {}'.format(cos_sim))
