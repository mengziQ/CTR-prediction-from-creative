import numpy as np

with open('LightGBM_predict_result_d_over_1.txt', 'r') as rlt:
  ctrs = rlt.readlines()
  with open('/home/ubuntu/repos/creative-predictor/ctr/ctr_test4.svm', 'r') as data:
    lines = data.readlines()
    diff_n_0_09 = 0
    diff_n_0_08 = 0
    diff_n_0_07 = 0
    diff_n_0_06 = 0
    diff_n_0_05 = 0
    diff_n_0_04 = 0
    diff_n_0_03 = 0
    diff_n_0_02 = 0
    diff_n_0_01 = 0
    diff_n_0 = 0
    diff_0_01 = 0
    diff_0_02 = 0
    diff_0_03 = 0
    diff_0_04 = 0
    diff_0_05 = 0 
    diff_0_06 = 0
    diff_0_07 = 0
    diff_0_08 = 0
    diff_0_09 = 0
    diff_0_1 = 0

    for ctr, l in zip(ctrs, lines):
      l = l.split(' ')[0]
      ctr, l = map(lambda x: 1/(1 + np.exp(float(x))), [ctr, l])
      diff = l - ctr
      if -0.1 <= diff <= -0.09:
        diff_n_0_09 += 1
      elif -0.09 < diff <= -0.08:
        diff_n_0_08 += 1
      elif -0.08 < diff <= -0.07:
        diff_n_0_07 += 1
      elif -0.07 < diff <= -0.06:
        diff_n_0_06 += 1
      elif -0.06 < diff <= -0.05:
        diff_n_0_05 += 1
      elif -0.05 < diff <= -0.04:
        diff_n_0_04 += 1
      elif -0.04 < diff <= -0.03:
        diff_n_0_03 += 1
      elif -0.03 < diff <= -0.02:
        diff_n_0_02 += 1
      elif -0.02 < diff <= -0.01:
        diff_n_0_01 += 1
      elif -0.01 < diff <= 0:
        diff_n_0 += 1
      elif 0 < diff <= 0.01:
        diff_0_01 += 1
      elif 0.01 < diff <= 0.02:
        diff_0_02 += 1
      elif 0.02 < diff <= 0.03:
        diff_0_03 += 1
      elif 0.03 < diff <= 0.04:
        diff_0_04 += 1
      elif 0.04 < diff <= 0.05:
        diff_0_05 += 1
      elif 0.05 < diff <= 0.06:
        diff_0_06 += 1
      elif 0.06 < diff <= 0.07:
        diff_0_07 += 1
      elif 0.07 < diff <= 0.08:
        diff_0_08 += 1
      elif 0.08 < diff <= 0.09:
        diff_0_09 += 1
      elif diff <= 0.1:
        diff_0_1 += 1

    print('diff_n_0_09: {}'.format(diff_n_0_09)) 
    print('diff_n_0_08: {}'.format(diff_n_0_08)) 
    print('diff_n_0_07: {}'.format(diff_n_0_07)) 
    print('diff_n_0_06: {}'.format(diff_n_0_06)) 
    print('diff_n_0_05: {}'.format(diff_n_0_05)) 
    print('diff_n_0_04: {}'.format(diff_n_0_04))
    print('diff_n_0_03: {}'.format(diff_n_0_03))
    print('diff_n_0_02: {}'.format(diff_n_0_02)) 
    print('diff_n_0_01: {}'.format(diff_n_0_01)) 
    print('diff_n_0: {}'.format(diff_n_0))
    print('diff_0_01: {}'.format(diff_0_01))
    print('diff_0_02: {}'.format(diff_0_02))
    print('diff_0_03: {}'.format(diff_0_03))
    print('diff_0_04: {}'.format(diff_0_04))
    print('diff_0_05: {}'.format(diff_0_05))
    print('diff_0_06: {}'.format(diff_0_06))
    print('diff_0_07: {}'.format(diff_0_07))
    print('diff_0_08: {}'.format(diff_0_08))
    print('diff_0_09: {}'.format(diff_0_09))
    print('diff_0_1: {}'.format(diff_0_1))
