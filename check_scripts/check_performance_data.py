import pickle
import csv
import gzip
import glob
import zipfile

imp_zero = 0
click_zero = 0
ctr_zero = 0 # CTR列のctrが0のもの 
click_bigger_imp = 0
data_num = 0

for name in glob.glob('/home/ubuntu/repos/StormRuler/server/download/adwords_media_info/*.csv.gz'):
  print(name)
    
  with gzip.open(name, 'rt') as f:
    print(name)
    # f.read()のままだと一文字ごとになってしまう
    for idx, r in enumerate(f.read().split('\n')):
      if idx == 1:
        head = r
      elif idx > 1 :
        splited_dt = r.split(',')
        # 要素の中に,が含まれていて配列がずれることがあるため
        if 'Total' in splited_dt[0] or len(splited_dt) != 27:
          break
        else:
          if '%' in splited_dt[18]:
            splited_dt[18] = float(splited_dt[18].strip('%'))
          if splited_dt[18] == 0:
            ctr_zero += 1
          if float(splited_dt[20]) == 0:
            imp_zero += 1
          if float(splited_dt[21]) == 0:
            click_zero += 1
          if float(splited_dt[20]) < float(splited_dt[21]):
            click_bigger_imp += 1
          data_num += 1

with open('check_performance_data.txt', 'w') as p:
  p.write('ctr_zero: {}'.format(ctr_zero) + '\n')
  p.write('imp_zero: {}'.format(imp_zero) + '\n')
  p.write('click_zero: {}'.format(click_zero) + '\n')
  p.write('click_bigger_imp: {}'.format(click_bigger_imp) + '\n') 
  p.write('data_num: {}'.format(data_num) + '\n') 
