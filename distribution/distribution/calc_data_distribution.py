import numpy as np

with open('/home/ubuntu/repos/creative-predictor/ctr/ctr8_test.svm', 'r') as data:
  da = data.readlines()
  diff_0_1 = 0
  diff_0_2 = 0
  diff_0_3 = 0
  diff_0_4 = 0
  diff_0_5 = 0
  diff_0_6 = 0
  diff_0_7 = 0
  diff_0_8 = 0
  diff_0_9 = 0
  diff_1 = 0

  for d in da:
    d = d.split(' ')[0]
    d = float(d) / 10
    if d <= 0.1:
      diff_0_1 += 1
    elif d <= 0.2:
      diff_0_2 += 1
    elif d <= 0.3:
      diff_0_3 += 1
    elif d <= 0.4:
      diff_0_4 += 1
    elif d <= 0.5:
      diff_0_5 += 1
    elif d <= 0.6:
      diff_0_6 += 1
    elif d <= 0.7:
      diff_0_7 += 1
    elif d <= 0.8:
      diff_0_8 += 1
    elif d <= 0.9:
      diff_0_9 += 1
    elif d <= 1:
      diff_1 += 1

  print('diff_0.1: {}'.format(diff_0_1))
  print('diff_0.2: {}'.format(diff_0_2)) 
  print('diff_0.3: {}'.format(diff_0_3)) 
  print('diff_0.4: {}'.format(diff_0_4))
  print('diff_0.5: {}'.format(diff_0_5))
  print('diff_0.6: {}'.format(diff_0_6))
  print('diff_0.7: {}'.format(diff_0_7))
  print('diff_0.8: {}'.format(diff_0_8))
  print('diff_0.9: {}'.format(diff_0_9))
  print('diff_1: {}'.format(diff_1))
