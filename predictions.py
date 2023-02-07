from sklearn.neighbors import KNeighborsClassifier
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
import pandas as pd


test= pd.read_csv('credit_test.csv')
test["gender"] = (test["gender"] == "M").astype(int)
# test = test.dropna()
# test = test.drop('client_id', axis=1)

# le_education = LabelEncoder()
# le_region = LabelEncoder()
# le_marital_status = LabelEncoder()
# le_job_position = LabelEncoder()

# test["education"] = le_education.fit_transform(test["education"])
# test["living_region"] = le_region.fit_transform(test["living_region"])
# test["marital_status"] = le_marital_status.fit_transform(test["marital_status"])
# test["job_position"] = le_job_position.fit_transform(test["job_position"])
# test['credit_sum'] = test['credit_sum'].apply(lambda x: float(x.replace(',', '.')))
# test['score_shk'] = test['score_shk'].apply(lambda x: float(x.replace(',', '.')))
arr = [[0, 30, 1, 12, 16159.0, 10, 1.32, 0.421477, 3, 236, 10000.0, 0.0, 0.0]]
# my_array = np.array(arr)
df = pd.DataFrame(arr, columns = ['gender','age', 'marital_status', 'job_position', 'credit_sum', 'credit_month', 'tariff_id', 'score_shk', 'education', 'living_region', 'monthly_income', 'credit_count', 'overdue_credit_count'])


knn_model = joblib.load('card-pred.joblib')
predictions = knn_model.predict(df)

print(predictions)


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