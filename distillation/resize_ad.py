from PIL import Image
import numpy as np
import glob
import pickle
import os


for name in glob.glob('/home/ubuntu/repos/StormRuler/server/download/pkls/*.pkl'):
  print(name)
  pkl_name = '/home/ubuntu/s3_mnt/outputs/i2v_ad/resized_pkl/' + name.split('/').pop().replace('_per_img', '')   
  
  if os.path.exists(pkl_name):
    continue

  try:
    x, Y = pickle.loads(open(name, 'rb').read())
  except Exception as e:
    print(e)
    continue

  pilImg = Image.fromarray(np.uint8(Y))
  img = pilImg.convert('RGB') 
  w, h = img.size

  if w > h:
    blank = Image.new('RGB', (w, w))
  elif h >= w:
    blank = Image.new('RGB', (h, h))

  blank.paste(img, (0, 0))
  
  target_size = (224, 224) # ここってinput_tensorは三次元だけど
  blank = blank.resize(target_size)

  img_array = np.asarray(blank)
  img_array = img_array / 255.0

  pkl_name = '/home/ubuntu/s3_mnt/outputs/i2v_ad/resized_pkl/' + name.split('/').pop().replace('_per_img', '')  
  Y = img_array
  print('x:', x)
  print('Y:', Y)

  with open(pkl_name, 'wb') as resized_pkl:
    resized_pkl.write(pickle.dumps((x, Y)))


