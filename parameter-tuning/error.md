# エラーとその対処法  
## Memory Error  
特徴量が多すぎるとメモリエラーになる。  
nthreadで並列処理するスレッド数を決めることができ、公式ドキュメントではCPU数と同じにすることを推奨しているが、多分ほとんどエラーになるのでは？  
少なくとも私の環境とデータ量ではメモリエラーになった。  

**実行環境１（参考）**
```
- メモリ：　１６GB
- CPU: 4コア
- 特徴量数: 2000くらい
- 学習データ数： 178300
- テストデータ数: 44576

nthread=1でないとメモリエラーになった。
```
**実行環境2（参考）** 
``` 
- メモリ：　32GB
- CPU: 8コア
- 特徴量数: 2000くらい
- 学習データ数： 178300
- テストデータ数: 44576

nthread=5で実行できた。
```
## [LightGBM] [Warning] bagging_fraction is set=0.7, subsample=0.8 will be ignored. Current value: bagging_fraction=0.7.   
同じパラメータに対して、Scikit-learnAPIとLightGBMで別のパラメータ名を指定している可能性あり。  
例えば、bagging_fractionはaliasとしてcolsample_bytreeでも指定できる。どちらかに統一する必要がある。  
※Scikit-learnのパラメータはaliasがないので、こちらに統一する。  

LightGBMがチューニング中に出力する情報以外に、システム側で出力する警告文として以下の文章が出てくる。  
```
/usr/local/lib/python3.5/dist-packages/lightgbm/engine.py:99: UserWarning: Found `num_iteration` in params. Will use it instead of argument
  warnings.warn("Found `{}` in params. Will use it instead of argument".format(alias))  
```
上記だと、「num_iteration」がScikit-learn側にないパラメータなので警告が出ていると思われる。  
