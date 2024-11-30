import boto3
import pandas as pd
import joblib
from sklearn.preprocessing import OneHotEncoder


def load_data(dataset_path):
    """
    Загрузка данных из CSV файла.
    """
    try:
        print(f"Attempting to load data from {dataset_path}...")
        data = pd.read_csv(dataset_path)
        print("Data loaded successfully.")
        return data
    except FileNotFoundError:
        print(f"Ошибка: файл {dataset_path} не найден.")
        raise
    except pd.errors.EmptyDataError:
        print(f"Ошибка: файл {dataset_path} пуст.")
        raise
    except Exception as e:
        print(f"Ошибка при загрузке данных из {dataset_path}: {e}")
        raise


def save_model_to_s3(model, experiment_name, bucket_name="your-bucket-name"):
    """
    Сохранение модели в S3.
    """
    try:
        print("Preparing to save the model to S3...")
        s3 = boto3.client('s3')
        model_path = f"/tmp/{experiment_name}_model.pkl"

        # Сохраняем модель в файл
        joblib.dump(model, model_path)

        # Загружаем файл на S3
        s3.upload_file(model_path, bucket_name, f"models/{experiment_name}/model.pkl")
        print(f"Модель успешно загружена в S3 в путь models/{experiment_name}/model.pkl")
    except Exception as e:
        print(f"Ошибка при сохранении модели в S3: {e}")
        raise


def preprocess_data(data):
    """
    Преобразование данных: кодирование категориальных признаков и добавление числовых признаков.
    """
    # Проверим, были ли данные уже обработаны
    if not hasattr(data, 'processed'):  # Если нет атрибута processed, то обрабатываем
        print("Starting preprocessing...")
        encoder = OneHotEncoder(drop='first', sparse_output=True)
        categorical_cols = data.select_dtypes(include=['object']).columns
        print(f"Categorical columns before encoding: {categorical_cols}")

        if categorical_cols.any():
            encoded_data = encoder.fit_transform(data[categorical_cols])

            feature_names = encoder.get_feature_names_out(categorical_cols)
            processed_data = pd.DataFrame.sparse.from_spmatrix(encoded_data, columns=feature_names)

            numerical_cols = data.select_dtypes(exclude=['object']).columns
            if numerical_cols.any():
                processed_data[numerical_cols] = data[numerical_cols]

            print(f"Encoded data shape: {encoded_data.shape}")
            print(f"Processed data shape after encoding: {processed_data.shape}")

            data = processed_data  # Обновляем переменную data с преобразованными данными
            data.processed = True  # Устанавливаем флаг, что данные обработаны
        else:
            print("No categorical columns to encode.")

        print("Data preprocessing completed.")
    else:
        print("Data already processed.")

    return data
