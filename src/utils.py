import os
import sys

import numpy as np
import pandas as pd
import dill
from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as f:
            dill.dump(obj,f)

    except Exception as e:
        raise(CustomException(e,sys))


from sklearn.metrics import accuracy_score, classification_report

def evaluate(model, X, y_true):
    y_pred = model.predict(X)
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("Classification Report:\n", classification_report(y_true, y_pred))
