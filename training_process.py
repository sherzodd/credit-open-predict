import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
import joblib

df= pd.read_csv('credit_train.csv')
df = df.drop('client_id', axis=1)
df["gender"] = (df["gender"] == "M").astype(int)
df = df.dropna()

le_education = LabelEncoder()
le_region = LabelEncoder()
le_marital_status = LabelEncoder()
le_job_position = LabelEncoder()

# Replace names with labelencoder
df["education"] = le_education.fit_transform(df["education"])
df["living_region"] = le_region.fit_transform(df["living_region"])
df["marital_status"] = le_marital_status.fit_transform(df["marital_status"])
df["job_position"] = le_job_position.fit_transform(df["job_position"])
df['credit_sum'] = df['credit_sum'].apply(lambda x: float(x.replace(',', '.')))
df['score_shk'] = df['score_shk'].apply(lambda x: float(x.replace(',', '.')))


# Store mapping 
education_mapping = dict(zip(le_education.classes_, le_education.transform(le_education.classes_)))
region_mapping = dict(zip(le_region.classes_, le_region.transform(le_region.classes_)))
marital_status__mapping = dict(zip(le_marital_status.classes_, le_marital_status.transform(le_marital_status.classes_)))
job_position_mapping = dict(zip(le_job_position.classes_, le_job_position.transform(le_job_position.classes_)))

#{'ACD': 0, 'GRD': 1, 'PGR': 2, 'SCH': 3, 'UGR': 4}
#{'74': 0, '98': 1, 'АДЫГЕЯ РЕСП': 2, 'АЛТАЙСКИЙ': 3, 'АЛТАЙСКИЙ КРАЙ': 4, ...}
#{'CIV': 0, 'DIV': 1, 'MAR': 2, 'UNM': 3, 'WID': 4}
#{'ATP': 0, 'BIS': 1, 'BIU': 2, 'DIR': 3, 'HSK': 4, ...}


train_size = int(0.8 * len(df))
train = df.iloc[:train_size, :]
test = df.iloc[train_size:, :]

#scaling inputs
def scale_dataframe(df, oversampler=False):
  X = df[df.columns[:-1]].values
  y = df[df.columns[-1]].values

  scaler = StandardScaler()
  X = scaler.fit_transform(X)
  if oversampler:
    ros = RandomOverSampler()
    X, y = ros.fit_resample(X, y)

  data = np.hstack((X, np.reshape(y, (-1, 1))))

  return data, X, y


train, X_train, y_train = scale_dataframe(train, oversampler=True)
test, X_test, y_test = scale_dataframe(test, oversampler=False)

#training the model
knn_model = KNeighborsClassifier(n_neighbors=1)
knn_model.fit(X_train, y_train)
joblib.dump(knn_model, 'card-pred.joblib')
