## パラメーターのチューニング手順  
scikit-learnのGridSearchCVでgrid paramsを指定します。  
このとき、チューニングしたいパラメータを一気に指定してもいいのですが、特徴量やデータ量が多いとチューニングに時間がかかります。  
なので、パラメータを小分けにしてチューニングしていきます。  

パラメーターチューニングには効率が良いとされる順番があるようです。[このサイト](http://kamonohashiperry.com/archives/209)によると、以下の順番でチューニングするのが良いそうです。  

1. 学習率と木の数  
2. 木に関するパラメーター：　max_depth, min_child_weight, gamma, subsample, colsample_bytree
3. 正則化パラメータ: lambda, alphaなど  
4. 学習率を下げる  

## Scikit-learn GridSearchCVのfit関数実行ログを見る  
verbose=3にすると以下のログが出力される
```
Fitting 4 folds for each of 1728 candidates, totalling 6912 fits
[CV] subsample=0.7, reg_lambda=1, boosting_type=gbdt, n_estimators=1000, learning_rate=0.06, random_state=501, reg_alpha=1, num_leaves=31, objective=regression, colsample_bytree=0.7 
[CV]  subsample=0.7, reg_lambda=1, boosting_type=gbdt, n_estimators=1000, learning_rate=0.06, random_state=501, reg_alpha=1, num_leaves=31, objective=regression, colsample_bytree=0.7, score=0.9975824977932051, total=  16.1s
[Parallel(n_jobs=1)]: Done   1 out of   1 | elapsed:   24.0s remaining:    0.0s
[CV] subsample=0.7, reg_lambda=1, boosting_type=gbdt, n_estimators=1000, learning_rate=0.06, random_state=501, reg_alpha=1, num_leaves=31, objective=regression, colsample_bytree=0.7 
[CV]  subsample=0.7, reg_lambda=1, boosting_type=gbdt, n_estimators=1000, learning_rate=0.06, random_state=501, reg_alpha=1, num_leaves=31, objective=regression, colsample_bytree=0.7, score=0.9979117721237265, total=  16.5s
[Parallel(n_jobs=1)]: Done   2 out of   2 | elapsed:   48.5s remaining:    0.0s
[CV] subsample=0.7, reg_lambda=1, boosting_type=gbdt, n_estimators=1000, learning_rate=0.06, random_state=501, reg_alpha=1, num_leaves=31, objective=regression, colsample_bytree=0.7 
[CV]  subsample=0.7, reg_lambda=1, boosting_type=gbdt, n_estimators=1000, learning_rate=0.06, random_state=501, reg_alpha=1, num_leaves=31, objective=regression, colsample_bytree=0.7, score=0.9981020341201355, total=  16.5s
・・・
```
### 実行時間の見積  
totalling fitsの回数と、1回の交差検証のtotalの秒数を見ることで分かる。  
上記の例であれば、
```
6912　×　約16秒 = 110592秒 = 30.72時間  
```
### Fitting 4 folds for each of 1728 candidates, totalling 6912 fits  
- folds: GridSearchCVインスタンス作成時に指定するパラメータ:cvの値。交差検証時にデータを何分割するか。  
- candidates: grid_paramsの組合せ数  
- totalling: folds　× candidates  

### score  
公式ドキュメントには「Mean cross-validated score of the best_estimator」とある。  
estimatorはcandidatesと同義だと思われる。Mean cross-validated scoreはfoldした回数分のスコアの平均値。  

## 各パラメーターの値ってどれくらいがいいの？(調べ中)  
### learning_rate(学習率)  
一般的には0.1だが、ケースによっては0.05〜0.3でもうまくいく可能性あり  

### n_estimators(木の数)  
LightGBMのRegressionの例では1000になっていた。意味のある分類が1000パターンあるという解釈。  

### max_depth(木の深さ)  
1つの木の深さ。LightGBMのRegressionの例では設定していない。デフォルトは-1で、これは無限に深くして良いという設定。  

### colsample_bytreeとかfeature_fraction  
1回のイテレーションで特徴量を何割を使用するかを指定する。過学習を防ぐ効果がある。  
だいたい0.7〜0.9あたり？  

### subsampleとかbagging_fraction  
1回のイテレーションでデータの何割を使用するかを指定する。過学習を防ぐ効果がある。  
だいたい0.7〜0.9あたり？  

### reg_alphaとかalpha(L1正則化項)  
「重み付けベクトルの要素の総和がx以上？以下？だったらペナルティ」のxを規定する？  
不要な特徴量を削減したいときに使用するらしい。  
値をどの程度にしたらいいか調査中。  

### reg_lambdaとかlambda(L2正則化項)  
「重み付けベクトルの要素の二乗の総和がx以上？以下？だったらペナルティ」のxを規定する？  
過学習を抑えて汎化性能を高めたいときに使用する。  
値をどの程度にしたらいいか調査中。  
