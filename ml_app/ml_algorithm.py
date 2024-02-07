# ml_app/ml_algorithm.py
import joblib
import numpy as np
import pandas as pd
from django.http import JsonResponse
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score


def train_ml_algorithm_rf(data):
    pd_data = pd.DataFrame.from_records(list(data))
    pd_data['date'] = pd.to_datetime(pd_data['date'])
    pd_data['date'] = (pd_data['date'] - pd_data['date'].min()) / np.timedelta64(1, 'D')
    pd_data["pct_change"] = pd_data['close'].shift(1) / pd_data['close'] - 1
    pd_data['direction'] = pd_data['pct_change'].apply(lambda x: 1 if x > 0 else 0)
    pd_data['direction'] = pd_data['direction'].shift(1)
    pd_data.dropna(inplace=True)

    # Filter the data into train and test sets based on the 'tag'
    train_data = pd_data[pd_data['tag'] == 'TRAIN']
    test_data = pd_data[pd_data['tag'] == 'TEST']

    # Extract features and labels for training and testing sets
    features = ['date', 'open', 'low', 'high', 'volume', 'dividends', 'stock_splits']
    X_train = train_data[['open', 'low', 'high', 'volume', 'dividends', 'stock_splits']].values
    y_train = train_data['direction'].values

    X_test = test_data[['open', 'low', 'high', 'volume', 'dividends', 'stock_splits']].values
    y_test = test_data['direction'].values

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    print(f'Accuracy Test Set: {accuracy:.2f}')
    precision = precision_score(y_test, predictions, average='binary', pos_label=1)
    print(f'Precision Test Set: {precision:.2f}')
    recall = recall_score(y_test, predictions, average='binary', pos_label=1)
    print(f'Recall Test Set: {recall:.2f}')
    joblib.dump(model, 'random_forest_classifier.joblib')

    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall
    }

    return metrics
