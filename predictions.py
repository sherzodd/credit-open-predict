from sklearn.neighbors import KNeighborsClassifier
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
import pandas as pd



knn_model = joblib.load('card-pred.joblib')



def input_dataframe(
    gender,
    age,
    marital_status,
    job_position,
    credit_sum,
    credit_month,
    tariff_id,
    score_shk,
    education,
    living_region,
    monthly_income,
    credit_count,
    overdue_credit_count):
    
    array = [gender, age, marital_status, job_position, credit_sum, credit_month, tariff_id, score_shk, education, living_region, monthly_income, credit_count, overdue_credit_count]
    df = pd.DataFrame(array, columns = ['gender','age', 'marital_status', 'job_position', 'credit_sum', 'credit_month', 'tariff_id', 'score_shk', 'education', 'living_region', 'monthly_income', 'credit_count', 'overdue_credit_count'])
    
    return df


def get_model_prediction(dataframe):

    knn_model = joblib.load('card-pred.joblib')
    predictions = knn_model.predict(dataframe)
    
    return predictions