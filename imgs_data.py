import pickle
import csv
import gzip
import glob
import zipfile
import os
from PIL import Image
import sys
import numpy as np
import json

args = sys.argv

def id_perform():  
  for name in glob.glob('/home/ubuntu/repos/StormRuler/server/download/*.csv.gz'):
    print(name)
    id_perform_dic = {}
    
    with gzip.open(name, 'rt') as f:
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
            if id_perform_dic.get(splited_dt[0]) is None:
              values = []

              for d in splited_dt:
                values.append(d)

              id_perform_dic[splited_dt[0]] = values
              # ctrだけ%抜く処理追加
              id_perform_dic[splited_dt[0]][18] = float(splited_dt[21])/float(splited_dt[20])

            else:
              try: 
                impressions = int(id_perform_dic[splited_dt[0]][20]) + int(splited_dt[20])
                id_perform_dic[splited_dt[0]][20] =  impressions
                clicks = int(id_perform_dic[splited_dt[0]][21]) + int(splited_dt[21])
                id_perform_dic[splited_dt[0]][21] = clicks
              except ValueError as e:
                print(e)
                continue
              try:
                #ctr = impressions*1.0 / clicks*1.0
                ctr = clicks*1.0 / imporessions*1.0 * 100
              except ZeroDivisionError as e:
                ctr = 0.0
                continue

              cost = int(id_perform_dic[splited_dt[0]][22]) + int(splited_dt[22])
              conversions = float(id_perform_dic[splited_dt[0]][24]) + float(splited_dt[24])

              id_perform_dic[splited_dt[0]][18] = ctr
              id_perform_dic[splited_dt[0]][22] = cost
              id_perform_dic[splited_dt[0]][24] = conversions     


    for ad_id, values in id_perform_dic.items():
      with open('/home/ubuntu/repos/StormRuler/server/download/performance/{}_performance.json'.format(ad_id), 'w') as p:
        dic = {}
        dic[ad_id] = values
        p.write(json.dumps(dic))
        p.close()


def perform_img():
  if os.path.exists('/home/ubuntu/repos/StormRuler/server/download/unzip/img') is False:
    os.mkdir('/home/ubuntu/repos/StormRuler/server/download/unzip/img')

  for name in glob.glob('/home/ubuntu/repos/StormRuler/server/download/*.zip'):
    #print(name)
    # file is not zip fileになってしまうものがある。元のファイルをunzipしてもだめなのでファイル自体の問題ぽい 

    try:
      z = zipfile.ZipFile(name, 'r')
    except Exception as e:
      print(e)
      print(name)
      continue

    perform_img_dic = {}
    #print('perform_img_dic生成')

    if len(z.namelist()) == 1:
      #print('namelistが１個=画像なし')
      continue
    elif 'imageinfo.csv' in z.namelist():
      #print('画像あり')
      z.extractall('/home/ubuntu/repos/StormRuler/server/download/')
      img_info = open('/home/ubuntu/repos/StormRuler/server/download/imageinfo.csv', 'r')
      
      try:
        it = csv.reader(img_info)
        head = next(it)

      except StopIteration as ire:
        print('StopIteration!')
        continue
        
      for line in it: 
        ad_id = line[0] 
        img_url = line[6]
        mime_type = line[3]
        height = line[4]
        width = line[5]
        
        file_path = '/home/ubuntu/repos/StormRuler/server/download/performance/{}_performance.json'.format(ad_id)
          
        if os.path.exists(file_path) is True:
          #print('ファイルあったよ！')
          with open(file_path, 'r') as rp:
            #print(file_path)
            perform_img_dic = json.load(rp)
            #print(perform_img_dic)
            perform_img_dic[ad_id].append(mime_type)
            perform_img_dic[ad_id].append(height)
            perform_img_dic[ad_id].append(width)

            try:
              img = Image.open('/home/ubuntu/repos/StormRuler/server/download/img/{}'.format(img_url))
            except OSError as e:
              print(e)
              continue

            img_array = np.array(img)
  
          with open('/home/ubuntu/repos/StormRuler/server/download/pkls/{}_per_img.pkl'.format(ad_id), 'wb') as final_pkl:
            #print(perform_img_dic)
            #print(img_array)
            final_pkl.write(pickle.dumps((perform_img_dic, img_array)))


if args[1] == '-perform':
  id_perform()
elif args[1] == '-img':
  perform_img()



