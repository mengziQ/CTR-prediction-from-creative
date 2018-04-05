# https://www.kaggle.com/garethjns/microsoft-lightgbm-with-parameter-tuning-0-823
# 学習率とn_estimatorsをチューニングするスクリプト

import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
#from sklearn.grid_search import GridSearchCV
import pandas as pd

# trainRawと一緒
train = pd.read_csv('train.csv')
# testRawと一緒
test = pd.read_csv('test.csv')

# 学習データの行数
n_train = train.shape[0]
# 学習データ+ テストデータ
full = pd.concat([train, test], axis=0)

def prepLGB(data):
  # lDataとlabelsだけ作ることにする
  labels = data.iloc[:,0]
  #print('data.columns:', data.columns)
  # free_raw_data sets true for need to free raw data after construct
  # optimal split for categorical features
  l_data = lgb.Dataset(data, label=labels, free_raw_data=False, feature_name=list(data.columns), categorical_feature='auto')
  return l_data, labels

# stratifyはいらない？層化サンプリングをする必要あり？
train_data, valid_data = train_test_split(train, test_size=0.3)
# 学習データの7割
train_data_l, train_labels = prepLGB(train_data)
# 学習データの3割
valid_data_l, valid_labels = prepLGB(valid_data)
# テストデータ
test_data_l, test_labels = prepLGB(test)
# 学習データ
all_train_data, all_train_labels = prepLGB(train)

# cf. train.conf
# train.confになくてもチューニング用に入れた方がいいパラメータもあるかも？例えばsubsample_for_binとか？
params = {
  'boosting_type': 'gbdt',
  'max_depth': -1,
  'objective': 'regression',
  'nthread': 5, # -1だと自動決定。cpu数にしたら特徴量が多いせいかメモリエラーになった。。
  'metric': 'l2',
  'num_leaves': 31,
  'learning_rate': 0.05,
  'max_bin': 255,
  'subsample_for_bin': 200, # bin_construct_sample_cnt
  'subsample': 0.8, # bagging_fraction
  'subsample_freq': 5, # bagging_freq
  'colsample_bytree': 0.8, # feature_fraction 
  'reg_alpha': 5,
  'reg_lambda': 10,
  #'min_split_gain': 0.5,
  #'min_child_weight': 1, # min_sum_hessian_in_leaf デフォルトが1e-3だけど・・・ 
  #'min_child_samples': 5, # min_data_in_leaf
}

grid_params = {
  'learning_rate': [0.0125, 0.001],
  'n_estimators': [1000, 2000, 3000, 4000]
}

mdl = lgb.LGBMRegressor(
  boosting_type = params['boosting_type'],
  objective = params['objective'],
  n_jobs = params['nthread'],
  silent = 'True',
  max_depth = params['max_depth'],
  max_bin = params['max_bin'],
  subsample_for_bin = params['subsample_for_bin'],
  subsample = params['subsample'],
  subsample_freq = params['subsample_freq']
)

print('the default model params')
print(mdl.get_params().keys())
#print('all_train_data:', type(all_train_data))
#print('all_train_labels:', type(all_train_labels))
# 参考コードのn_jobsが-1になってるけど除外
print('GridSearchCV開始')
grid = GridSearchCV(mdl, grid_params, verbose=3, cv=4)
print('fit開始')
grid.fit(train, all_train_labels)

print('best params: ', grid.best_params_)
print('best score: ', grid.best_score_)

