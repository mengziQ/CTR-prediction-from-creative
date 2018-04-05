# 固定する要素を1つにして、全特徴量についてコサイン類似度を計算するパターン
import numpy as np
import re
import sys
import pickle

with open('/home/ubuntu/repos/creative-predictor/ctr8.svm', 'r') as svm:
  with open('cos_sim_result.txt', 'w') as rlt:
    obj = svm.readlines()
  
    # rは固定する要素
    for r in range(1679):
      std = []
      # もう一個for文で全体を囲う。特徴量ぶんだけループする。
      for i, o in enumerate(obj):
        print('{}行目!!'.format(i))
        splited = o.split(' ')[1:1679]
        vector_list = [] 
        for sp in splited:
          vector_list.append(float(re.sub(r'[0-9]+:', '', sp)))
   
        std = np.array(vector_list)
        #print(len(std))

        # ここの添え字を変更
        if std[r] == 1:
          print('基準ベクトル探索完了: {}行目'.format(i)) 
          break

      cos_sim = 0.0
      cs_idx = 0

      for idx, o in enumerate(obj):
        print('{}行目'.format(idx))
        tgt_flg = 0
        if idx == i:
          continue
        else:
          splited = o.split(' ')[1:1679]
          vector_list = []
          target = []
          for sp in splited:
            vector_list.append(float(re.sub(r'[0-9]+:', '', sp)))
        
          target = np.array(vector_list)
          # ここの添え字を変更
          if target[30] == 0:
            print('ターゲット{}行目'.format(idx))
            new_cos_sim = np.dot(std, target) / (np.linalg.norm(std) * np.linalg.norm(target))
            print('コサイン類似度:{}'.format(new_cos_sim))
            if new_cos_sim > cos_sim:
              cos_sim = new_cos_sim
              cs_idx = idx

      print('特徴量{} 最終結果'.format(r))
      rlt.write('特徴量{} 最終結果'.format(r))
      print('基準ベクトル: {}行目'.format (i))
      rlt.write('基準ベクトル: {}行目'.format (i))
      print('コサイン類似度最大のベクトル: {}行目'.format(cs_idx))
      rlt.write('コサイン類似度最大のベクトル: {}行目'.format(cs_idx))
      print('コサイン類似度: {}'.format(cos_sim))
      rlt.write('コサイン類似度: {}'.format(cos_sim))
      rlt.write('\n')

