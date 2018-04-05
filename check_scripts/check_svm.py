# SVMファイルのラベル確認スクリプト 

with open('/home/ubuntu/repos/creative-predictor/ctr/ctr7.svm', 'r') as svm:
  sv = svm.readlines()
  for i, s in enumerate(sv):
    ctr = s.split(' ')[0]
    ctr = float(ctr) / 10
    if ctr < 0 or ctr > 1 or ctr == 0:
      print('{}番目のデータのCTR: {}'.format(i, ctr))
