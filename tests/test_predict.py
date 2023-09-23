import numpy as np
import joblib


def test_predict_wating_time():
    "predict wating time test code"
    data = [
        0, 36, 73, 1,
        7, 2, 44735, 6,
        2, 2, 24, 34,
        18, 0, 3, 25.8,
        0, 66.3
    ]
    data = np.array([data])
    loaded_model = joblib.load('models/model.pkl')
    predict = loaded_model.predict(
        data,
        num_iteration=loaded_model.best_iteration
        )
    assert len(predict) > 0
