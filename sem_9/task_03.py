import pandas as pd

# разделение данных на обучающую и тестовую выборку
from sklearn.model_selection import train_test_split

# преобразование текста в вектор
from sklearn.feature_extraction.text import TfidfVectorizer

# использование модели логистической регрессии
from sklearn.linear_model import LogisticRegression

# оценка производительности модели
from sklearn.metrics import accuracy_score, classification_report

# конвейер обработки данных
from sklearn.pipeline import Pipeline

data_path = "movie.csv"
data = pd.read_csv(data_path)
# print(data.head())

# разделение данных на обучающую и тестовую выборку
x_train, x_test, y_train, y_test = train_test_split(
    data["text"],  # тест рецензии - будет использоваться как входные данные
    data["label"],  # метка классов (+ или -)
    test_size=0.2,  # доля данных, которая попадет в тетст (20%)
    random_state=73,  # зерно генератора случайных чисел для воспроизводимости результаттов
)

# создание модели с использованием конвейера
# конвейер включает векторизатор и логистическую регрессию
pipeline = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(stop_words="english"),
        ),  # векторизация текста с исключением стоп-слов английского языка
        (
            "clf",
            LogisticRegression(max_iter=1000),
        ),  # модель логистической регрессии с увеличенным количеством итераций до 1000
    ]
)

# обучение модели на обучающем наборе данных
pipeline.fit(x_train, y_train)

# оценка модели
predictions = pipeline.predict(x_test)  # предсказание модели на тестовых данных
accuracy = accuracy_score(y_test, predictions)  # расчет точности модели
report = classification_report(y_test, predictions)

print(f"Точность модели: {accuracy}")
print("Отчет по классификации")
print(report)
