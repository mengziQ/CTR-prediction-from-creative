# ネット広告のクリエイティブからCTRを予測する  
ネット広告に掲載される画像(クリエイティブ)から、その広告のCTRを予測できないかというモチベーションで実施した分析です。  
クリエイティブをタグ要素に分解し、どのタグがCTRを上昇させているのか・もしくは下降させているのかを調べます。  

## 概要図  
![概要図](https://github.com/mengziQ/study_room/blob/master/gradient-boosting/lightgbm/pics/overview.PNG)
   
## 1. Google Adword　APIで入手したクリエイティブとCTR実績値を結合する  
クリエイティブデータとCTR値は社内専用のAPIでGoogle Adwords APIを操作して取得しているためスクリプトは割愛します。  

以下のレポートから取得しています。  
- クリエイティブデータ： MEDIA_SERVICE_WITH_IMAGE(リンク探し中)  
- CTR値： [AD_PERFORMANCE_REPORT](https://developers.google.com/adwords/api/docs/appendix/reports/ad-performance-report)

取得したCTR値(この時点では全てのパフォーマンスデータ)をjson形式に変換し、Ad IDが分かるようなファイル名に変更します。  
```
$ python3 imgs_data.py -perform
```

上で作成したjsonファイル(パフォーマンスデータ)とクリエイティブデータ(配列に変換)をAd IDで結合します。
```
$ python3 imgs_data.py -image
```


## 2. クリエイティブ→画像タグへの変換    
**使用したAPI**   Google Cloud Vision API  

まず、クリエイティブ画像(画像そのもの)をGoogle Cloud Vision APIに読み込ませるためにリサイズする  
```
$ python3 vision/vision.py --minimize
入力： クリエイティブ
出力： 縮小or拡大したクリエイティブ画像(一辺が最大224ピクセルとなるようにリサイズ)
```

リサイズしたクリエイティブのタグを検出する  
```
$ python3 vision/vision.py --scan
入力：　 リサイズしたクリエイティブ
出力：　 画像タグ(json)
```


## 3. tag_idxの作成  
クリエイティブへのタグ付けが終了したら、全タグを探索してidを振ります。スクリプトどっか消えました。  
この後、諸々作業して精度が悪かったので特徴量を減らしました。その際にタグの出現頻度を調べたので、これが参考になるかもしれません笑  
```
$ python3 tag_freq.py
```

出現頻度を元に特徴量を削減する
```
$ python3 reduce_tag.py
```

最終的なtag_idxはこちら → tag_idx2.pkl


## 4. 画像タグ・実績CTRを結合してSVMファイルを作成    
すごーく分かりづらいのですが、1でできたpickleファイル(パフォーマンスと画像配列)と2でできたjsonファイル(画像タグ)を画像名で照合しつつ、
3で作ったtag_idx2.pklを使ってLightGBMに読み込ませるためのSVMファイルを作成します。  

```
ラベルをCTRにしたいので、以下のように引数に指定してください

$ python3 kpi_tag.py ctr
```


## 5. LightGBMによる学習  
インストール方法は[ここ](https://github.com/mengziQ/study_room/blob/master/gradient-boosting/lightgbm/docs/installation.md)か公式githubを参照ください。  

```
$ cd ctr
$ lightgbm config=train.conf
```


## 6. 予測
```
$ cd ctr
$ lightgbm config=predict.conf
```

## 7. 精度が良くないのでパラメーターチューニングをした  
parameter_tuningフォルダを参照ください。

## 8. モデル検証結果  
結論としては、CTRの予測精度はほとんど出ませんでした。。。  

まずは、誤差率分布を調べました。(誤差率＝|実績値-予測値|/予測値 で計算)  
```
$ cd distribution
$ python3 calc_distirbution.py
```

![誤差率分布](https://github.com/mengziQ/study_room/blob/master/gradient-boosting/lightgbm/pics/err_distribution.PNG)
- 「CTR = クリック数/インプレッション数」なので、クリック数＝0の広告のCTRは0になるのですが、0.0000001(極小な値)を代入して学習させたところ、あまり学習がうまくいかなかった模様。。。  
- 誤差率が(0.9〜1に限らず)全体的に出てしまっているため、もちろんクリック数0のデータだけの問題ではない  

![散布図](https://github.com/mengziQ/study_room/blob/master/gradient-boosting/lightgbm/pics/scatter_plot.PNG)
データはCTR＝0〜0.1の範囲にほぼ集合。赤枠の中のデータが少ないため、ほぼCTR値を当てられていないことになります。  

## 9. 追加調査  
CTR値を直接予測することができなくても、タグがCTRを上げているか・下げているかだけでも当てられないか、調査をしました。  

手始めに、CTR値に影響力を持つタグがあるかないかで上記検証を行いたいと思ったため、特徴量重要度を出しました。(trend_analysis/feature_importance.ipynb参照)  
![特徴量重要度](https://github.com/mengziQ/study_room/blob/master/gradient-boosting/lightgbm/pics/feature_importances.png)

まずは、全データの中から、最も重要度の高いタグ「product」があるベクトル(＝**基準ベクトル**とします)と、逆に「product」がないベクトルで基準ベクトルに最も類似したベクトルをコサイン類似度で算出します。  
```
$ cd trend_analysis
$ python3 find_vectors.py
```
この時、そこそこCTRに影響がありそうなタグは排除しようと思いました。そこで色々試行錯誤した結果、重要度上位4つ目あたりまでの固定ならなんとかベクトルが見つかりそうだったので固定しました。  
![要素固定イメージ](https://github.com/mengziQ/study_room/blob/master/gradient-boosting/lightgbm/pics/find_vec.PNG)

こんな感じで、とりあえず上位2タグ「product」「advertizing」についてCTRを上げるのか下げるのか検証した結果が以下になります。  
![CTR影響](https://github.com/mengziQ/study_room/blob/master/gradient-boosting/lightgbm/pics/cos_sim.PNG)
上げるか下げるかくらいなら分かりそうですかね・・・？  
気が向いたら全タグについて同様の調査を行うスクリプトを作成します。。。  

