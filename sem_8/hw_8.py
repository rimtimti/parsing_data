# 1 .Скачайте датасет House Prices Kaggle со страницы конкурса (https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data)
#       и сохраните его в том же каталоге, что и ваш скрипт или блокнот Python.
# 2. Загрузите датасет в pandas DataFrame под названием df.
# 3. Выполните предварительную обработку данных, выполнив следующие шаги:
#   a. Определите и обработайте отсутствующие значения в датасете. Определите, в каких столбцах есть отсутствующие значения,
#       и решите, как их обработать (например, заполнить средним, медианой или модой, или отбросить столбцы/строки с существенными отсутствующими значениями).
#   b. Проверьте и обработайте любые дублирующиеся строки в датасете.
#   c. Проанализируйте типы данных в каждом столбце и при необходимости преобразуйте их (например, из объектных в числовые типы).
# 4. Проведите разведочный анализ данных (EDA), ответив на следующие вопросы:
#   a. Каково распределение целевой переменной 'SalePrice'? Есть ли какие-либо выбросы?
#   b. Исследуйте взаимосвязи между целевой переменной и другими характеристиками. Есть ли сильные корреляции?
#   c. Исследуйте распределение и взаимосвязи других важных характеристик, таких как 'OverallQual', 'GrLivArea', 'GarageCars' и т.д.
#   d. Визуализируйте данные, используя соответствующие графики (например, гистограммы, диаграммы рассеяния, квадратные диаграммы), чтобы получить представление о датасете.
# 5. Выполните проектирование признаков путем реализации следующих преобразований:
#   a. Работайте с категориальными переменными, применяя one-hot encoding или label encoding, в зависимости от характера переменной.
#   b. При необходимости создайте новые характеристики, такие как общая площадь или возраст объекта недвижимости, путем объединения существующих характеристик.
# 6. Сохраните очищенный и преобразованный набор данных в новый CSV-файл под названием 'cleaned_house_prices.csv'.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats
from scipy.stats.mstats import winsorize
from sklearn.calibration import LabelEncoder
from sklearn.preprocessing import StandardScaler

sns.set(style="whitegrid")

file_path = "train.csv"
df = pd.read_csv(file_path)
# print(df.head())
# print(df.describe())
# df.info()

# удаляем столбцы с малым заполнением
df = df.drop(["Alley", "MasVnrType", "PoolQC", "Fence", "MiscFeature"], axis=1)

# обработка отсутствующих значений
numeric_cols = df.select_dtypes(include=[np.number])
df[numeric_cols.columns] = numeric_cols.fillna(numeric_cols.mean())
categorical_cols = df.select_dtypes(include=["object"])  # выбор категориальных колонок
df[categorical_cols.columns] = categorical_cols.fillna(categorical_cols.mode().iloc[0])

# убираем дубликаты
df.drop_duplicates(inplace=True)

# визуализация
# plt.figure(figsize=(10, 6))
# sns.histplot(df["GrLivArea"], kde=True, color="skyblue")
# plt.title("Жилая площадь над уровнем земли (земля), квадратные футы")
# plt.show()

# plt.figure(figsize=(10, 6))
# sns.countplot(
#     y="GarageCars",
#     data=df,
#     order=df["GarageCars"].value_counts().index,
#     palette="viridis",
# )
# plt.title("Размер гаража по вместимости автомобиля")
# plt.show()

# plt.figure(figsize=(10, 6))
# sns.countplot(y="BldgType", data=df)
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
df["Condition_3"] = label_encoder.fit_transform(df["SaleCondition"])

# one hot encoding
df = pd.get_dummies(
    df, columns=["SaleCondition"], prefix="Condition_3", drop_first=True
)

# создание сводной таблицы
pivot_table = df.pivot_table(index="MSSubClass", values="SalePrice", aggfunc="mean")


output_file_path = "cleaned_house_prices.csv"
df.to_csv(output_file_path, index=False)
