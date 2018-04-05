import http.server
import requests
import socketserver
import base64
import os
import json


# basehttprequesthandlerじゃなくてsimplehttprequesthandler
class Handler(http.server.SimpleHTTPRequestHandler):
  def _set_response(self):
    # このメソッドいるか謎。小林さんのclientのコードで足りるかも。
    # なんでsend_responseが使えるの？baseじゃないとダメなんじゃないの？
    self.send_response(200)

  def do_POST(self):
    data = self.rfile.read()
    # 画像のバイナリとmodeが入っているはず
    data = json.loads(data.decode())
    
    # この書き方あってる？
    if data['mode'] == "image":
      from PIL import Image
      from numpy as np

      # visionAPI？
      # リサイズ処理
      GOOGLE_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='
      # APIキーまだこのインスタンスには設定してないかも
      API_KEY = os.environ('GOOGLE')
      
      # 並列処理の必要はないと予想。一度に一枚アップされると想定。
      img_byte = data['img']
      try:
        # バイナリを画像に戻す？
        img = Image.fromarray(np.uint8(img_byte))
        img = img.convert('RGB')
        size = img.size
        ratio = max(size[0], size[1]) / 224
        resize = (size[0]/ratio, size[1]/ratio)
        try:
          img = img.resize(resize)
        except OSError as e:
          return
      except Exception as e:
        print('Some Deep Error as ', e)

      # スキャン処理
      img_b64 = base64.b64encode(img)
      api_url = GOOGLE_VISION_API_URL + API_KEY

      req_body = json.dumps({
          'requests': [{
              'image': {
                  'content': img_b64.decode()
              }
              'features': [{
                  'type': 'LABEL_DETECTION',
                  'maxResults': 100,
              }]
          }]
      })

    res = requests.post(api_url, data=req_body)
    # .json()をつける意味　json形式にならないのかな？
    return res.json()

    # LightGBM？
    

    # ここからはレスポンス準備
    self.send_response(200)

    try:
      print(data)
      target = data['data']
      # user_agentは写した。これで合ってるか要確認。
      user_agent = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}  
      # targetってurlなの？
      res = requests.post(target, json='')
      

  

