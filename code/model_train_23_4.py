#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/18  10:20
# @Author  : chensw、wangwei
# @File    : model_train.py
# @Describe: 标明文件实现的功能
# @Modify  : 修改的地方

import pandas as pd
import os
import xgboost as xgb
import operator
from sklearn.externals import joblib


#  将特征重要性排序出来和打印并保存
def create_feature_map(features):
    outfile = open(r'../data/output/featureMap/firstXGB.fmap', 'w')
    i = 0
    for feat in features:
        outfile.write('{0}\t{1}\tq\n'.format(i, feat))
        i = i + 1
    outfile.close()


def feature_importance(bst_xgb):
    importance = bst_xgb.get_fscore(fmap=r'../data/output/featureMap/firstXGB.fmap')
    importance = sorted(importance.items(), key=operator.itemgetter(1), reverse=True)

    df = pd.DataFrame(importance, columns=['feature', 'fscore'])
    df['fscore'] = df['fscore'] / df['fscore'].sum()
    return df


if __name__ == '__main__':
    print('Start building training and test sets!!!')
    # (1)模型5的训练
    dataSet1 = pd.read_csv('../data/features/features_2_4/trainSet.csv')
    dataSet = pd.read_csv('../data/features/features_3_4/trainSet.csv')
    dataSet = pd.concat([dataSet1, dataSet])
    del dataSet1
    x_test = pd.read_csv('../data/features/features_test/testSet.csv')

    dataSet['ucs_b1_count_in_5_1_diff'] = dataSet['ucs_b1_count_in_5'] - dataSet['ucs_b1_count_in_1']
    dataSet['ucs_b1_count_in_7_3_diff'] = dataSet['ucs_b1_count_in_7'] - dataSet['ucs_b1_count_in_3']
    dataSet['ucs_b2_count_in_5_1_diff'] = dataSet['ucs_b2_count_in_5'] - dataSet['ucs_b2_count_in_1']
    dataSet['c_b_count_in_7_3_diff'] = dataSet['c_b_count_in_7'] - dataSet['c_b_count_in_3']
    dataSet['us_b4_count_in_5_1_diff'] = dataSet['us_b4_count_in_5'] - dataSet['us_b4_count_in_1']
    dataSet['us_b3_count_in_5_1_diff'] = dataSet['us_b3_count_in_5'] - dataSet['us_b3_count_in_1']
    dataSet['us_b4_count_in_7_3_diff'] = dataSet['us_b4_count_in_7'] - dataSet['us_b4_count_in_3']
    dataSet['us_b3_count_in_7_3_diff'] = dataSet['us_b3_count_in_7'] - dataSet['us_b3_count_in_3']
                                                  
    x_test['ucs_b1_count_in_5_1_diff'] = x_test['ucs_b1_count_in_5'] - x_test['ucs_b1_count_in_1']
    x_test['ucs_b1_count_in_7_3_diff'] = x_test['ucs_b1_count_in_7'] - x_test['ucs_b1_count_in_3']
    x_test['ucs_b2_count_in_5_1_diff'] = x_test['ucs_b2_count_in_5'] - x_test['ucs_b2_count_in_1']
    x_test['c_b_count_in_7_3_diff'] = x_test['c_b_count_in_7'] - x_test['c_b_count_in_3']
    x_test['us_b4_count_in_5_1_diff'] = x_test['us_b4_count_in_5'] - x_test['us_b4_count_in_1']
    x_test['us_b3_count_in_5_1_diff'] = x_test['us_b3_count_in_5'] - x_test['us_b3_count_in_1']
    x_test['us_b4_count_in_7_3_diff'] = x_test['us_b4_count_in_7'] - x_test['us_b4_count_in_3']
    x_test['us_b3_count_in_7_3_diff'] = x_test['us_b3_count_in_7'] - x_test['us_b3_count_in_3']

    dataSet.drop(['city_level_6.0','cs_major_cate', 'province_18.0', 'province_24.0', 'unknown', 'reg_time_4', 'ucs_b4_count_in_5', 'ucs_b3_count_in_7', 'us_b3_count_in_1'], axis=1, inplace=True)
    x_test.drop(['city_level_6.0','cs_major_cate', 'province_18.0', 'province_24.0', 'unknown', 'reg_time_4', 'ucs_b4_count_in_5', 'ucs_b3_count_in_7', 'us_b3_count_in_1'], axis=1, inplace=True)
    dataSet.drop(['us_b4_count_in_7','us_b3_count_in_5','us_b4_count_in_1','province_25.0','province_12.0','province_9.0','ucs_b3_count_in_3','ucs_b4_count_in_7','ucs_b3_count_in_5','or_shop_score', 'province_3.0','province_17.0','ucs_b4_count_in_3','province_2.0', 'province_13.0', 'shop_reg_tm_5','c_b_count_in_3', 'c_b_count_in_5', 'c_b_count_in_7', 'city_level_2.0', 'province_4.0', 'ucs_b2_count_in_1'], axis=1, inplace=True)
    x_test.drop(['us_b4_count_in_7','us_b3_count_in_5','us_b4_count_in_1','province_25.0','province_12.0','province_9.0','ucs_b3_count_in_3','ucs_b4_count_in_7','ucs_b3_count_in_5','or_shop_score', 'province_3.0','province_17.0','ucs_b4_count_in_3','province_2.0', 'province_13.0', 'shop_reg_tm_5','c_b_count_in_3', 'c_b_count_in_5', 'c_b_count_in_7', 'city_level_2.0', 'province_4.0', 'ucs_b2_count_in_1'], axis=1, inplace=True)

    # 提取训练特征集
    x_train = dataSet.loc[:, dataSet.columns != 'label']
    y_train = dataSet.loc[:, dataSet.columns == 'label']

    del x_train['user_id'], x_train['cate'], x_train['shop_id']
    del x_test['user_id'], x_test['cate'], x_test['shop_id']

    dtrain = xgb.DMatrix(x_train, label=y_train)

    # 快速训练和测试：xgboost训练
    param = {'n_estimators': 500,
             'max_depth': 6,
             'min_child_weight': 3,
             'gamma': 0.3,
             'subsample': 0.9,
             'colsample_bytree': 0.8,
             'eta': 0.125,
             'silent': 1,
             'objective': 'binary:logistic',
             'eval_metric': 'auc'
             }
    plst = param.items()
    evallist = [(dtrain, 'train')]
    bst = xgb.train(plst, dtrain, 500, evallist, early_stopping_rounds=10)

    # 保存模型
    joblib.dump(bst, '../data/output/model/model_23_4.pkl')
    del dataSet, dtrain

    # 创建特征图
    create_feature_map(list(x_train.columns[:]))
    # 根据特征图，计算特征重要性，并排序和展示
    feature_importances = feature_importance(bst)
    feature_importances.sort_values("fscore", inplace=True, ascending=False)
    feature_importances.to_csv('../data/output/feature_importance/feature_importance_23_4.csv', index=False, encoding='utf-8')
    # print(feature_importances.head(20))
    del x_train

    # 使用模型对测试集进行预测
    x_test_DMatrix = xgb.DMatrix(x_test)
    y_pred = bst.predict(x_test_DMatrix)
    predict = pd.DataFrame({'prob': y_pred})
    test_set = pd.read_csv('../data/features/features_test/test_index.csv')
    predict = pd.concat([test_set, predict], axis=1)
    predict.to_csv('../data/output/predict/prediction_23_4.csv', index=False, encoding='utf-8')
    
    print('The fifth model_train is OK!!!')








