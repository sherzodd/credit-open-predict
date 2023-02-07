from fastapi import FastAPI, Depends
import schemas
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from predictions import input_dataframe
from predictions import get_model_prediction

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()
        
        
@app.get("/")
def info():
    return """It is a ML model made for predicting outcome of clients decision on opening credit account
            To get predictions, please, unput required client data in order: gender, age, marital_status, job_position,
            credit_sum, credit_month, tariff_id, score_shk, education, living_region, monthly_income, credit_count, 
            overdue_credit_count. """
            
        
    
            
@app.post("/predict")
def do_predictions(request: schemas.Predictions, db: Session = Depends(get_db)):
    db_model = models.Predictions(gender=request.gender,
                                  age=request.age,
                                  marital_status=request.marital_status,
                                  job_position=request.job_position,
                                  credit_sum=request.credit_sum,
                                  credit_month=request.credit_month,
                                  tariff_id=request.tariff_id,
                                  score_shk=request.score_shk,
                                  education=request.education,
                                  living_region=request.living_region,
                                  monthly_income=request.monthly_income,
                                  credit_count=request.monthly_income,
                                  overdue_credit_count=request.overdue_credit_count) #database model
    
    #Input for model dataframe
    model_input = input_dataframe(gender=request.gender,
                                  age=request.age,
                                  marital_status=request.marital_status,
                                  job_position=request.job_position,
                                  credit_sum=request.credit_sum,
                                  credit_month=request.credit_month,
                                  tariff_id=request.tariff_id,
                                  score_shk=request.score_shk,
                                  education=request.education,
                                  living_region=request.living_region,
                                  monthly_income=request.monthly_income,
                                  credit_count=request.monthly_income,
                                  overdue_credit_count=request.overdue_credit_count)
    
    prediction = get_model_prediction(model_input)
    updated_db_model = update_model(db_model, prediction)
    db.add(updated_db_model)
    db.commit()
    db.refresh(updated_db_model)
    return prediction
    


    
def update_model(model_instance, optional_field_value=None):
    model_instance.open_account_flg = optional_field_value
    return model_instance