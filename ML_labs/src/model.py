from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from utils import preprocess_data  # Импортируем функцию для обработки данных
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")


def train_and_evaluate_model(data, config):
    """
    Обучение модели с использованием GridSearch и оценка её метрик
    """

    print("Starting data preprocessing...")
    data = preprocess_data(data)
    print("Data preprocessing completed.")

    X = data.drop(columns=["Quantity"])
    y = data["Quantity"]

    print("Preparing model...")
    model = RandomForestClassifier()

    if "max_features" not in config:
        config["max_features"] = ['sqrt', 'log2']

    grid_search = GridSearchCV(model, config, cv=5)
    print("Starting grid search for hyperparameter tuning...")
    grid_search.fit(X, y)
    print("Grid search completed.")

    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    print(f"Best Params: {best_params}")
    print(f"Best Score: {best_score}")

    return best_model, best_params, best_score
