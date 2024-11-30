import json
import mlflow
from model import train_and_evaluate_model
from utils import save_model_to_s3, load_data, preprocess_data


def log_experiment(experiment_name, model, metrics):
    """
    Логирование метрик и модели в MLFlow
    """
    print("Logging experiment metrics to MLFlow...")
    mlflow.start_run(experiment_id=mlflow.create_experiment(experiment_name))
    mlflow.log_params(metrics)
    mlflow.sklearn.log_model(model, "model")
    mlflow.end_run()
    print("Experiment logged to MLFlow.")


def main(config_file, dataset_path, experiment_name):
    """
    Главная функция для запуска экспериментов
    """
    print("Loading configuration from:", config_file)
    with open(config_file, "r") as f:
        config = json.load(f)
    print("Configuration loaded.")

    print("Loading dataset from:", dataset_path)
    data = load_data(dataset_path)
    print(f"Dataset loaded with shape: {data.shape}")

    print("Starting data preprocessing...")
    data = preprocess_data(data)
    print(f"Data preprocessing completed. Processed data shape: {data.shape}")

    # Проверка, что обработанные данные имеют нужную структуру
    if data.shape[1] == 0:
        print("Warning: Processed data has no features. Check preprocessing.")

    print("Training model...")
    model, best_params, best_score = train_and_evaluate_model(data, config)
    print(f"Model trained. Best params: {best_params}, Best score: {best_score}")

    # Логирование эксперимента в MLFlow
    metrics = {"best_params": best_params, "best_score": best_score}
    log_experiment(experiment_name, model, metrics)

    # Сохранение модели в S3
    print("Saving model to S3...")
    save_model_to_s3(model, experiment_name)
    print("Model saved to S3.")


if __name__ == "__main__":
    main("C:/Users/ikuli/PycharmProjects/Lab1_ML/ML_labs/config/config.json",
         "C:/Users/ikuli/PycharmProjects/Lab1_ML/ML_labs/src/online_sales_dataset.csv",
         "experiment1")
