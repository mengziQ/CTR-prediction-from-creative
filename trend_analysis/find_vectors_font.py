# 任意の要素が1であり、その他の要素が異なるベクトルを探索するスクリプト
import numpy as np
import re
import sys

def find_vector():
  with open('/home/ubuntu/repos/creative-predictor/ctr8.svm', 'r') as svm:
    obj = svm.readlines()
    tmp_list = []
    cnt = 0 

    # 上位2個で実験
    top30_list = [30, 33]
    std = []
    for i, o in enumerate(obj):
      print('{}行目'.format(i))
      splited = o.split(' ')[1:1679]
      vector_list = [] 
      for sp in splited:
        vector_list.append(float(re.sub(r'[0-9]+:', '', sp)))
   
      std = np.array(vector_list)
      #print(len(std))

      # ここのtの数値を変更
      for t, top in enumerate(top30_list):
        if t == 0 and std[top] == 0:
          break
        elif t != 0 and std[top] == 1:
          break
        elif t == len(top30_list) - 1:
          print('基準ベクトル探索完了: {}行目'.format(i))
          sys.exit()
  

def calc_cos_sim():
  with open('/home/ubuntu/repos/creative-predictor/ctr8.svm', 'r') as svm:
    obj = svm.readlines()
    cos_sim = 0.0
    cs_idx = 0
    i = int(sys.argv[2])

    for idx, o in enumerate(obj):
      splited = o.split(' ')[1:1679]
      vector_list = []
      target = []
      for sp in splited:
        vector_list.append(float(re.sub(r'[0-9]+:', '', sp)))

      if idx == i:
        std = np.array(vector_list)
        continue
      else:
        target = np.array(vector_list) 
      
      if target[30] != 1:
        print('{}行目'.format(idx))
        new_cos_sim = np.dot(std, target) / (np.linalg.norm(std) * np.linalg.norm(target))
        if new_cos_sim > cos_sim:
          cos_sim = new_cos_sim
          cs_idx = idx

    print('最終結果')
    print('基準ベクトル: {}行目'.format (i))
    print('コサイン類似度最大のベクトル: {}行目'.format(cs_idx))
    print('コサイン類似度: {}'.format(cos_sim))

if sys.argv[1] == '--vec':
  find_vector()
elif len(sys.argv) == 3 and sys.argv[1] == '--cs':
  calc_cos_sim()
else:
  print('please enter args')

