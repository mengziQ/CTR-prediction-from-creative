# API Gatewayからデータを取得し、同じAd-IDのクリック数・インプレッション数を足し合わせた状態で欠損データ数を調べる。
import pickle
import glob

imp_zero = 0
click_zero = 0
click_bigger_imp = 0
data_num = 0

for name in glob.glob('/home/ubuntu/repos/StormRuler/server/download/pkls/*'):
  with open(name, 'rb') as pkls:
    objs = pickle.load(pkls)
    kpi = list(objs[0].values())
    if float(kpi[0][20]) == 0:
      imp_zero += 1
    if float(kpi[0][21]) == 0:
      click_zero += 1
    if float(kpi[0][20]) < float(kpi[0][21]) :
      click_bigger_imp += 1
    data_num += 1

with open('check_pkls.txt', 'w') as c:
  c.write('data_num: {}'.format(data_num) + '\n')
  c.write('imp_zero: {}'.format(imp_zero) + '\n')
  c.write('click_zero: {}'.format(click_zero) + '\n')
  c.write('click_bigger_imp: {}'.format(click_bigger_imp) + '\n')

