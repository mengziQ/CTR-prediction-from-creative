import csv

with open('../ctr/ctr8_train.svm', 'r') as tr:
  obj = tr.readline()
  with open('train8.csv', 'w') as c:
    writer = csv.writer(c)
    while obj:
      splited_obj = obj.strip().split(' ')
      o_list = []
      for i, so in enumerate(splited_obj):
        if i == 0:
          o_list.append(splited_obj[0])
        elif i < len(splited_obj):
          print(len(splited_obj))
          print(splited_obj[i])
          print(i)
          o_list.append(splited_obj[i].split(':')[1])
        else:
          break
      #o_list.append('\n')
      writer.writerow(o_list)
      obj = tr.readline()

