from fastapi import FastAPI, Depends
import schemas
import models
from database import engine, SessionLocal
from sqlalchemy import Session
from predictions import input_dataframe, get_model_prediction

app = FastAPI()

# models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()
        
        
@app.get("/")
def info():
    return {"name": "First Data"}
    # return """It is a ML model made for predicting outcome of clients decision on opening credit account
    #         To get predictions, please, unput required client data in order: gender, age, marital_status, job_position,
    #         credit_sum, credit_month, tariff_id, score_shk, education, living_region, monthly_income, credit_count, 
    #         overdue_credit_count. """
            
        
    
            
# @app.post("/predict")
# def do_predictions(request: schemas.Predictions, db: Session = Depends(get_db)):
#     db_model = models.Predictions(request) #database model
#     model_input = input_dataframe(request)
#     prediction = get_model_prediction(model_input)
#     updated_db_model = update_model(db_model, prediction)
    


    
# def update_model(model_instance, optional_field_value=None):
#     model_instance.open_account_flg = optional_field_value
#     return model_instance