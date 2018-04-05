import numpy as np
import sys

with open('/home/ubuntu/repos/creative-predictor/ctr/LightGBM_predict_result8.txt', 'r') as rlt:
  ctrs = rlt.readlines()
  with open('/home/ubuntu/repos/creative-predictor/ctr/ctr8_test.svm', 'r') as data:
    lines = data.readlines()
    diff_n_over = 0
    diff_n_0_5 = 0
    diff_n_0_4 = 0
    diff_n_0_3 = 0
    diff_n_0_2 = 0
    diff_n_0_1 = 0
    diff_0_1 = 0
    diff_0_2 = 0
    diff_0_3 = 0
    diff_0_4 = 0
    diff_0_5 = 0
    diff_0_6 = 0
    diff_0_7 = 0
    diff_0_8 = 0
    diff_0_9 = 0
    diff_over = 0
    cnt = 0

    for ctr, l in zip(ctrs, lines):
      l = l.split(' ')[0]
      #ctr, l = map(lambda x: 1/(1 + np.exp(float(x))), [ctr, l])
      ctr, l = map(lambda x: float(x)/10, [ctr, l])
      #print('ctr: {}'.format(ctr))
      #print('l: {}'.format(l))
      #diff = l - ctr
      # 誤差率の場合以下を使用
      diff = abs(l - ctr) / ctr
      if diff < -0.5:
        # ctrの予測値がマイナスになってしまったデータはここに入る
        diff_n_over += 1
      elif -0.5 <= diff < -0.4:
        diff_n_0_5 += 1
      elif -0.4 <= diff < -0.3:
        diff_n_0_4 += 1
      elif -0.3 <= diff < -0.2:
        diff_n_0_3 += 1
      elif -0.2 < diff < -0.1 :
        diff_n_0_2 += 1 
      elif -0.1 <= diff <= 0:
        diff_n_0_1 += 1
      elif diff <= 0.1:
        diff_0_1 += 1
        print('diff_0_1: {}'.format(cnt))
      elif diff <= 0.2:
        diff_0_2 += 1
        print('diff_0_2: {}'.format(cnt))
      elif diff <= 0.3:
        diff_0_3 += 1
        print('diff_0_3: {}'.format(cnt))
      elif diff <= 0.4:
        diff_0_4 += 1
        print('diff_0_4: {}'.format(cnt))
      elif diff <= 0.5:
        diff_0_5 += 1
        print('diff_0_5: {}'.format(cnt))
      elif diff <= 0.6:
        diff_0_6 += 1
        print('diff_0_6: {}'.format(cnt))
      elif diff <= 0.7:
        diff_0_7 += 1
        print('diff_0_7: {}'.format(cnt))
      elif diff <= 0.8:
        diff_0_8 += 1
        print('diff_0_8: {}'.format(cnt))
      elif diff <= 0.9:
        diff_0_9 += 1
        print('diff_0_9: {}'.format(cnt))
      else:
        diff_over += 1
        
      cnt += 1

    print('diff_n_over: {}'.format(diff_n_over)) 
    print('diff_n_0_5: {}'.format(diff_n_0_5)) 
    print('diff_n_0_4: {}'.format(diff_n_0_4)) 
    print('diff_n_0_3: {}'.format(diff_n_0_3)) 
    print('diff_n_0_2: {}'.format(diff_n_0_2)) 
    print('diff_n_0_1: {}'.format(diff_n_0_1))
    print('diff_0.1: {}'.format(diff_0_1))
    print('diff_0.2: {}'.format(diff_0_2)) 
    print('diff_0.3: {}'.format(diff_0_3)) 
    print('diff_0.4: {}'.format(diff_0_4))
    print('diff_0.5: {}'.format(diff_0_5))
    print('diff_0.6: {}'.format(diff_0_6))
    print('diff_0.7: {}'.format(diff_0_7))
    print('diff_0.8: {}'.format(diff_0_8))
    print('diff_0.9: {}'.format(diff_0_9))
    print('diff_over: {}'.format(diff_over))
