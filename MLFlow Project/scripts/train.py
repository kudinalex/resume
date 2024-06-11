import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import time

print("Starting script...")

# Установите путь к директории с логами и моделью
tracking_uri = os.path.abspath(os.path.join(os.getcwd(), '../mlruns'))
mlflow.set_tracking_uri(f'file:///{tracking_uri.replace("\\", "/")}')
print(f"MLFlow tracking URI set to: {tracking_uri}")

# Проверка текущей рабочей директории
print(f"Current working directory: {os.getcwd()}")

# Формируем путь к файлу данных относительно текущей рабочей директории
data_path = os.path.abspath(os.path.join(os.getcwd(), '../data/data.csv'))
print(f"Data path: {data_path}")

# Загрузка данных
data = pd.read_csv(data_path)
print("Data loaded successfully.")

# Признаки и целевая переменная
features = ['Age', 'Gender', 'BMI', 'Smoking', 'GeneticRisk', 'PhysicalActivity', 'AlcoholIntake', 'CancerHistory']
target = 'Diagnosis'

X = data[features]
y = data[target]

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data split into train and test sets.")

# Установка имени эксперимента
experiment_name = "Cancer_Diagnosis_Experiment"
mlflow.set_experiment(experiment_name)

# Начало эксперимента
with mlflow.start_run():
    # Параметры модели
    n_estimators = 100
    max_depth = 5

    # Логирование параметров
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    print("Parameters logged.")

    # Обучение модели
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(X_train, y_train)
    print("Model trained.")

    # Предсказания
    y_pred = model.predict(X_test)
    print("Predictions made.")

    # Метрика
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy calculated: {accuracy}")

    # Логирование метрики
    mlflow.log_metric("accuracy", accuracy)
    print("Accuracy logged.")

    # Логирование модели
    mlflow.sklearn.log_model(model, "model")
    print("Model logged.")

    print(f"Model logged with Accuracy: {accuracy}")

if __name__ == "__main__":
    # Запуск скрипта
    print("Training script is running...")
    time.sleep(10)  # Задержка на 10 секунд перед закрытием окна
