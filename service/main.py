import os
from typing import List

import mlfoundry
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI

FIT_COLUMNS = ['age', 'duration', 'campaign', 'pdays', 'previous', 'emp.var.rate',
               'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'day_of_week_mon',
               'day_of_week_thu', 'day_of_week_tue', 'day_of_week_wed',
               'job_blue-collar', 'job_entrepreneur', 'job_housemaid',
               'job_management', 'job_retired', 'job_self-employed', 'job_services',
               'job_student', 'job_technician', 'job_unemployed', 'job_unknown',
               'marital_married', 'marital_single', 'marital_unknown',
               'education_basic.6y', 'education_basic.9y', 'education_high.school',
               'education_illiterate', 'education_professional.course',
               'education_university.degree', 'education_unknown', 'default_unknown',
               'default_yes', 'housing_unknown', 'housing_yes', 'loan_unknown',
               'loan_yes', 'contact_telephone', 'month_aug', 'month_dec', 'month_jul',
               'month_jun', 'month_mar', 'month_may', 'month_nov', 'month_oct',
               'month_sep', 'poutcome_nonexistent', 'poutcome_success']

app = FastAPI(docs_url="/")

client = mlfoundry.get_client()
model = client.get_model(os.getenv('MODEL_VERSION_FQN')).load()


class Request(BaseModel):
    instances: List[dict]


@app.post("/predict")
def predict(request: Request):
    df = pd.DataFrame(request.dict()["instances"])
    df = df.reindex(columns=FIT_COLUMNS, fill_value=0)
    predictions = model.predict(df)

    for features, prediction in zip(request.dict()["instances"], predictions.tolist()):
        data_id = client.generate_hash_from_data(
            features=features
        )
        client.log_predictions(os.getenv('MODEL_VERSION_FQN'), predictions=[mlfoundry.Prediction(
            data_id=data_id, features=features, prediction_data={"value": prediction})])

    return {
        "predictions": predictions.tolist()
    }
