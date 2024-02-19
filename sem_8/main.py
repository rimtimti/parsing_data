# pip install scipy
# pip install scikit-learn
# pip install seaborn

# - Загрузите датасет googleplaystore.csv с помощью pandas.
# - Изучите датасет, чтобы выявить ошибки, пропущенные значения или дубликаты.
# - Примените методы очистки данных, такие как заполнение недостающих значений или удаление дубликатов.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats
from scipy.stats.mstats import winsorize
from sklearn.calibration import LabelEncoder
from sklearn.preprocessing import StandardScaler

sns.set(style="whitegrid")

file_path = "googleplaystore.csv"
df = pd.read_csv(file_path)
# print(df.head())
# print(df.describe())
# df.info()

# обработка отсутствующих значений
numeric_cols = df.select_dtypes(include=[np.number])
df[numeric_cols.columns] = numeric_cols.fillna(numeric_cols.mean())
categorical_cols = df.select_dtypes(include=["object"])  # выбор категориальных колонок
df[categorical_cols.columns] = categorical_cols.fillna(categorical_cols.mode().iloc[0])

# убираем дубликаты
df.drop_duplicates(inplace=True)

# визуализация
# plt.figure(figsize=(10, 6))
# sns.histplot(df["Rating"], kde=True, color="skyblue")
# plt.title("Рейтинг приложений")
# plt.show()

# plt.figure(figsize=(10, 6))
# sns.countplot(
#     y="Category", data=df, order=df["Category"].value_counts().index, palette="viridis"
# )
# plt.title("Рейтинг приложений")
# plt.show()

# plt.figure(figsize=(10, 6))
# sns.countplot(y="Type", data=df)
# plt.title("Рейтинг по типу")
# plt.show()


# обнаружение и обработка выбросов
z_scores = np.abs(
    stats.zscore(df.select_dtypes(include=np.number))
)  # z-оценки для числовых переменных
df = df[(z_scores < 3).all(axis=1)]  # удаление строк с выбросами

# стандартизация данных (числовых переменных)
df_standardized = df.copy()
df_standardized[numeric_cols.columns] = (
    df_standardized[numeric_cols.columns] - df_standardized[numeric_cols.columns].mean()
) / df_standardized[numeric_cols.columns].std()

# преобразование категорийной переменной в числовую
label_encoder = LabelEncoder()
df["Type_Encoded"] = label_encoder.fit_transform(df["Type"])

# one hot encoding
df = pd.get_dummies(
    df, columns=["Content Rating"], prefix="ContentRating", drop_first=True
)

# создание сводной таблицы
pivot_table = df.pivot_table(
    index="Category", columns="ContentRating_Teen", values="Rating", aggfunc="mean"
)
print(pivot_table)

output_file_path = "google_clear.csv"
df.to_csv(output_file_path, index=False)
