import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import mlfoundry

df = pd.read_csv("bank-additional-full.csv")
df_final = pd.get_dummies(df, columns=["day_of_week", "job",
                                       "marital", "education",
                                       "default", "housing",
                                       "loan", "contact", "month",
                                       "poutcome"], drop_first=True)

X = df_final.drop("y", axis=1)
y = df_final["y"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

rfc = RandomForestClassifier(n_estimators=1000)
rfc.fit(X_train, y_train)

client = mlfoundry.get_client()
run = client.create_run(project_name="term-deposit-rfc")

features = []
for k, v in df.dtypes.to_dict().items():
    if k == 'y':
        continue
    if v == 'object':
        feature_type = 'string'
    if v == 'int64':
        feature_type = 'int'
    if v == 'float64':
        feature_type = 'float'
    features.append({'name': k, 'type': feature_type})

run.log_params({'n_estimator': 1000})
run.log_artifact()

run.log_model(name="term-deposit-rfc", model=rfc, framework="sklearn", model_schema={
    "features": features,
    "prediction": "categorical"
}, custom_metrics=[{"name": "log_loss", "type": "metric", "value_type": "float"}])
