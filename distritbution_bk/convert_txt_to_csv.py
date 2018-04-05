import csv

with open('../ctr/LightGBM_predict_result8.txt', 'r') as tr:
  obj = tr.readlines()
  with open('test8_rlt.csv', 'w') as c:
    writer = csv.writer(c)
    o_list = []
    for o in obj:
      o_list.append(float(o))
      o_list.append('\n')

    writer.writerow(o_list)

