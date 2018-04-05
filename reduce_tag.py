import pickle

with open('tag_freq.pkl', 'rb') as tf:
  obj = pickle.load(tf)
  del_list = []
  for o in obj:
    if o[1] in [1, 2]: 
      term = o[0].replace('(','').replace('\'','')
      if term not in del_list:
        del_list.append(term)

with open('del_tag.pkl', 'wb') as dt:
  pickle.dump(del_list, dt)
