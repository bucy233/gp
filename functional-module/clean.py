import os

import numpy as np
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor

# 文件路径
input_file = r"F:\八打雁\origin\八打雁202307.xlsx"
output_dir = r"F:\八打雁\aft"

os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "八打雁202307_cleaned.xlsx")


def is_outlier_zscore(series, threshold=4):
    """判断是否为异常值，使用Z-Score方法"""
    mean = series.mean()
    std = series.std()
    z_scores = (series - mean) / std
    return abs(z_scores) > threshold

def is_outlier_iqr(series, multiplier=2):
    """判断是否为异常值，使用IQR方法"""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    return (series < lower_bound) | (series > upper_bound)


def is_outlier_lof(df, n_neighbors=30, contamination=0.02):
    """判断是否为异常值，使用局部异常因子（LOF）方法"""
    lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
    df_numeric = df.select_dtypes(include=[np.number]).dropna()  # 使用数值型字段
    if df_numeric.shape[0] < n_neighbors:  # 如果样本数小于邻居数，跳过
        return pd.Series([False] * df.shape[0])
    outlier_flags = lof.fit_predict(df_numeric)  # -1 表示异常点
    return pd.Series(outlier_flags == -1, index=df_numeric.index)


# 读取数据
try:
    df = pd.read_excel(input_file)
    total_rows = len(df)
    print(f"总行数: {total_rows}")
except Exception as e:
    print(f"读取文件失败: {e}")
    exit()

# 检查空值所在的行
null_rows = df[df.isnull().any(axis=1)]
null_count = len(null_rows)
print(f"空值行数: {null_count}")
print(f"空值行所占比例: {null_count / total_rows:.2%}")

# 删除空值所在的行
df_cleaned = df.dropna()

# 处理异常值并展示三种方法的结果

# Z-Score方法
outlier_rows_zscore = pd.DataFrame()
for column in df_cleaned.select_dtypes(include=[np.number]).columns:
    outliers = df_cleaned[is_outlier_zscore(df_cleaned[column])]
    outlier_rows_zscore = pd.concat([outlier_rows_zscore, outliers])
outlier_rows_zscore = outlier_rows_zscore.drop_duplicates()
outlier_count_zscore = len(outlier_rows_zscore)
print(f"使用Z-Score方法处理 - 异常值行数: {outlier_count_zscore}")
print(f"使用Z-Score方法处理 - 异常值行所占比例: {outlier_count_zscore / total_rows:.2%}")

df_zscore_cleaned = df_cleaned.drop(outlier_rows_zscore.index)

# IQR方法
outlier_rows_iqr = pd.DataFrame()
for column in df_cleaned.select_dtypes(include=[np.number]).columns:
    outliers = df_cleaned[is_outlier_iqr(df_cleaned[column])]
    outlier_rows_iqr = pd.concat([outlier_rows_iqr, outliers])
outlier_rows_iqr = outlier_rows_iqr.drop_duplicates()
outlier_count_iqr = len(outlier_rows_iqr)
print(f"使用IQR方法处理 - 异常值行数: {outlier_count_iqr}")
print(f"使用IQR方法处理 - 异常值行所占比例: {outlier_count_iqr / total_rows:.2%}")

df_iqr_cleaned = df_cleaned.drop(outlier_rows_iqr.index)

# LOF方法
outlier_rows_lof = df_cleaned[is_outlier_lof(df_cleaned)]
outlier_count_lof = len(outlier_rows_lof)
print(f"使用LOF方法处理 - 异常值行数: {outlier_count_lof}")
print(f"使用LOF方法处理 - 异常值行所占比例: {outlier_count_lof / total_rows:.2%}")

df_lof_cleaned = df_cleaned.drop(outlier_rows_lof.index)

# 保存处理后的数据
try:
    # 将三种方法处理后的数据保存为不同文件
    df_zscore_cleaned.to_excel(os.path.join(output_dir, "八打雁202307_zscore_cleaned.xlsx"), index=False)
    df_iqr_cleaned.to_excel(os.path.join(output_dir, "八打雁202307_iqr_cleaned.xlsx"), index=False)
    df_lof_cleaned.to_excel(os.path.join(output_dir, "八打雁202307_lof_cleaned.xlsx"), index=False)
    print(f"处理后的文件已保存到: {output_dir}")
except Exception as e:
    print(f"保存文件失败: {e}")
