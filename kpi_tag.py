# visionAPIでタグ付けしたjsonとkpiを紐づけるスクリプト
# インプレッション0を除外、クリック数0を入れたバージョン
import glob
import json
import pickle
import os
import sys
import numpy as np

#with open('/home/ubuntu/s3_mnt/outputs/i2v_ad/kpi_tag/{}.svm'.format(sys.argv[1]), 'w') as kpi_tag:
with open('/home/ubuntu/repos/creative-predictor/{}8.svm'.format(sys.argv[1]), 'w') as kpi_tag: 
  for i, name in enumerate(glob.glob('/home/ubuntu/repos/StormRuler/server/download/pkls/*')):
  #for name in glob.glob('/home/ubuntu/repos/StormRuler/server/download/pkls/*')[:2]:
    with open(name, 'rb') as pkl:
      print('{}: {}'.format(i, name))
      #print(name)
      try:
        obj = pickle.load(pkl)
      except Exception as e:
        print(e)
    
      kpi = list(obj[0].values())
      #print(kpi)
      img_name = kpi[0][11]
      #print(img_name)
      # CTRは全てclickとimpressionで計算する  
      #print('imp:{} click:{}'.format(kpi[0][20], kpi[0][21]))
      ctr = kpi[0][18]
      ad_id = kpi[0][0]
      imp = kpi[0][20]
      click = kpi[0][21]
      cost = kpi[0][22]
      cv = kpi[0][23]
      # インプレッションが0の値を除外
      if imp == 0:
        continue
      #print(ctr, imp, click, cost, cv)

#with open('/home/ubuntu/repos/creative-predictor/kpi_tag/{}_kpi_tag.pkl'.format(ad_id), 'wb') as output:

    tags = []
    json_path = '/home/ubuntu/s3_mnt/outputs/i2v_ad/json/{}.json'.format(img_name)
    if os.path.exists(json_path) is True:
      with open(json_path, 'r') as tag_json:
        tag = json.load(tag_json)
        try:
          res = tag['responses'][0]
          tag_list = res['labelAnnotations']
        except Exception as e:
          print(e)
          continue
    
      rlt = []
      with open('/home/ubuntu/repos/creative-predictor/tag_idx2.pkl', 'rb') as t_i:
        term_id = pickle.load(t_i)
        #term_id = sorted(term_id, key = lambda x:x[1])
        for term, i in sorted(term_id.items(), key = lambda x:x[1]):
          exist_flg = 0
          for li in tag_list:
            try:
              if term == li['description']:
                exist_flg = 1
            except Exception as e:
              print(e)

          if exist_flg == 1:
            rlt.append('{}:1 '.format(i))
          else:
            rlt.append('{}:0 '.format(i))

        if sys.argv[1] == 'ctr':
          try:
            print(ctr)
            #ctr = abs(np.log(1/float(ctr) - 1)) 
            ctr = float(click) / float(imp) * 10
            if click == 0:
              ctr = 0.0000001
            print(ctr)
          except ZeroDivisionError as e:
            print(e)
          kpi_tag.write(str(ctr) + ' ')
        elif sys.argv[1] == 'imp':
          kpi_tag.write(str(imp) + ' ')
        elif sys.argv[1] == 'click':
          kpi_tag.write(str(click) + ' ')
        elif sys.argv[1] == 'cost':
          kpi_tag.write(str(cost) + ' ')
        elif sys.argv[1] == 'cv':
          kpi_tag.write(str(cv) + ' ')
        else:
          print('オプションを入れてください: ctr, imp, click, cost, cv')

        for r in rlt:
          kpi_tag.write(r)

      kpi_tag.write('\n')

    else:
      continue

