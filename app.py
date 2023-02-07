from fastapi import FastAPI, Depends
import schemas
import models
import pandas as pd
import numpy as np
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
    #Converting input string to numbers
    education_dict = {'ACD': 0, 'GRD': 1, 'PGR': 2, 'SCH': 3, 'UGR': 4}
    living_region_dict = {'74': 0, '98': 1, 'АДЫГЕЯ РЕСП': 2, 'АЛТАЙСКИЙ': 3, 'АЛТАЙСКИЙ КРАЙ': 4, 'АМУРСКАЯ ОБЛ': 5, 'АМУРСКАЯ ОБЛАСТЬ': 6, 'АО НЕНЕЦКИЙ': 7, 'АО ХАНТЫ-МАНСИЙСКИЙ АВТОНОМНЫЙ ОКРУГ - Ю': 8, 'АО ЯМАЛО-НЕНЕЦКИЙ': 9, 'АОБЛ ЕВРЕЙСКАЯ': 10, 'АРХАНГЕЛЬСКАЯ': 11, 'АРХАНГЕЛЬСКАЯ ОБЛ': 12, 'АРХАНГЕЛЬСКАЯ ОБЛАСТЬ': 13, 'АСТРАХАНСКАЯ': 14, 'АСТРАХАНСКАЯ ОБЛ': 15, 'АСТРАХАНСКАЯ ОБЛАСТЬ': 16, 'БАШКОРТОСТАН': 17, 'БАШКОРТОСТАН РЕСП': 18, 'БЕЛГОРОДСКАЯ ОБЛ': 19, 'БЕЛГОРОДСКАЯ ОБЛАСТЬ': 20, 'БРЯНСКАЯ ОБЛ': 21, 'БРЯНСКАЯ ОБЛАСТЬ': 22, 'БРЯНСКИЙ': 23, 'БУРЯТИЯ': 24, 'БУРЯТИЯ РЕСП': 25, 'ВЛАДИМИРСКАЯ ОБЛ': 26, 'ВЛАДИМИРСКАЯ ОБЛАСТЬ': 27, 'ВОЛГОГРАДСКАЯ ОБЛ': 28, 'ВОЛГОГРАДСКАЯ ОБЛАСТЬ': 29, 'ВОЛОГОДСКАЯ': 30, 'ВОЛОГОДСКАЯ ОБЛ': 31, 'ВОЛОГОДСКАЯ ОБЛ.': 32, 'ВОЛОГОДСКАЯ ОБЛАСТЬ': 33, 'ВОРОНЕЖСКАЯ ОБЛ': 34, 'ВОРОНЕЖСКАЯ ОБЛАСТЬ': 35, 'Г МОСКВА': 36, 'Г. МОСКВА': 37, 'Г. САНКТ-ПЕТЕРБУРГ': 38, 'ГОРЬКОВСКАЯ ОБЛ': 39, 'ГУСЬ-ХРУСТАЛЬНЫЙ Р-Н': 40, 'ДАГЕСТАН РЕСП': 41, 'ЕВРЕЙСКАЯ АВТОНОМНАЯ': 42, 'ЕВРЕЙСКАЯ АОБЛ': 43, 'ЗАБАЙКАЛЬСКИЙ КРАЙ': 44, 'ИВАНОВСКАЯ ОБЛ': 45, 'ИВАНОВСКАЯ ОБЛАСТЬ': 46, 'ИНГУШЕТИЯ РЕСП': 47, 'ИРКУТСКАЯ ОБЛ': 48, 'ИРКУТСКАЯ ОБЛАСТЬ': 49, 'КАБАРДИНО-БАЛКАРСКАЯ': 50, 'КАБАРДИНО-БАЛКАРСКАЯ РЕСП': 51, 'КАЛИНИНГРАДСКАЯ ОБЛ': 52, 'КАЛИНИНГРАДСКАЯ ОБЛ.': 53, 'КАЛМЫКИЯ': 54, 'КАЛМЫКИЯ РЕСП': 55, 'КАЛУЖСКАЯ': 56, 'КАЛУЖСКАЯ ОБЛ': 57, 'КАЛУЖСКАЯ ОБЛАСТЬ': 58, 'КАМЧАТСКАЯ ОБЛАСТЬ': 59, 'КАМЧАТСКИЙ КРАЙ': 60, 'КАРАЧАЕВО-ЧЕРКЕССКАЯ': 61, 'КАРАЧАЕВО-ЧЕРКЕССКАЯ РЕСП': 62, 'КАРЕЛИЯ': 63, 'КЕМЕРОВСКАЯ': 64, 'КЕМЕРОВСКАЯ ОБЛ': 65, 'КЕМЕРОВСКАЯ ОБЛАСТЬ': 66, 'КИРОВСКАЯ ОБЛ': 67, 'КИРОВСКАЯ ОБЛАСТЬ': 68, 'КОМИ РЕСП': 69, 'КОСТРОМСКАЯ ОБЛ': 70, 'КОСТРОМСКАЯ ОБЛАСТЬ': 71, 'КРАЙ АЛТАЙСКИЙ': 72, 'КРАЙ ЗАБАЙКАЛЬСКИЙ': 73, 'КРАЙ КАМЧАТСКИЙ': 74, 'КРАЙ КРАСНОДАРСКИЙ': 75, 'КРАЙ КРАСНОЯРСКИЙ': 76, 'КРАЙ ПЕРМСКИЙ': 77, 'КРАЙ ПРИМОРСКИЙ': 78, 'КРАЙ СТАВРОПОЛЬСКИЙ': 79, 'КРАЙ ХАБАРОВСКИЙ': 80, 'КРАЙ. КРАСНОЯРСКИЙ': 81, 'КРАЙ. ПЕРМСКИЙ': 82, 'КРАЙ. СТАВРОПОЛЬСКИЙ': 83, 'КРАЙ.ПЕРМСКИЙ': 84, 'КРАСНОДАРСКИЙ': 85, 'КРАСНОДАРСКИЙ КРАЙ': 86, 'КРАСНОЯРСКИЙ КРАЙ': 87, 'КУРГАНСКАЯ ОБЛ': 88, 'КУРГАНСКАЯ ОБЛАСТЬ': 89, 'КУРСКАЯ ОБЛ': 90, 'КУРСКАЯ ОБЛАСТЬ': 91, 'ЛЕНИНГРАДСКАЯ': 92, 'ЛЕНИНГРАДСКАЯ ОБЛ': 93, 'ЛЕНИНГРАДСКАЯ ОБЛАСТЬ': 94, 'ЛИПЕЦКАЯ ОБЛ': 95, 'ЛИПЕЦКАЯ ОБЛАСТЬ': 96, 'МАГАДАНСКАЯ ОБЛАСТЬ': 97, 'МАРИЙ ЭЛ РЕСП': 98, 'МОРДОВИЯ РЕСП': 99, 'МОСКВА': 100, 'МОСКВА Г': 101, 'МОСКВОСКАЯ ОБЛ': 102, 'МОСКОВСКАЯ': 103, 'МОСКОВСКАЯ ОБЛ': 104, 'МОСКОВСКАЯ ОБЛАСТЬ': 105, 'МУРМАНСКАЯ ОБЛ': 106, 'МУРМАНСКАЯ ОБЛАСТЬ': 107, 'МЫТИЩИНСКИЙ Р-Н': 108, 'НЕНЕЦКИЙ АО': 109, 'НИЖЕГОРОДСКАЯ ОБЛ': 110, 'НИЖЕГОРОДСКАЯ ОБЛАСТЬ': 111, 'НОВГОРОДСКАЯ ОБЛ': 112, 'НОВГОРОДСКАЯ ОБЛАСТЬ': 113, 'НОВОСИБИРСКАЯ': 114, 'НОВОСИБИРСКАЯ ОБЛ': 115, 'НОВОСИБИРСКАЯ ОБЛАСТЬ': 116, 'ОБЛ АМУРСКАЯ': 117, 'ОБЛ АРХАНГЕЛЬСКАЯ': 118, 'ОБЛ АСТРАХАНСКАЯ': 119, 'ОБЛ БЕЛГОРОДСКАЯ': 120, 'ОБЛ БРЯНСКАЯ': 121, 'ОБЛ ВЛАДИМИРСКАЯ': 122, 'ОБЛ ВОЛГОГРАДСКАЯ': 123, 'ОБЛ ВОЛОГОДСКАЯ': 124, 'ОБЛ ВОРОНЕЖСКАЯ': 125, 'ОБЛ ИВАНОВСКАЯ': 126, 'ОБЛ ИРКУТСКАЯ': 127, 'ОБЛ КАЛИНИНГРАДСКАЯ': 128, 'ОБЛ КАЛУЖСКАЯ': 129, 'ОБЛ КЕМЕРОВСКАЯ': 130, 'ОБЛ КИРОВСКАЯ': 131, 'ОБЛ КОСТРОМСКАЯ': 132, 'ОБЛ КУРГАНСКАЯ': 133, 'ОБЛ КУРСКАЯ': 134, 'ОБЛ ЛЕНИНГРАДСКАЯ': 135, 'ОБЛ ЛИПЕЦКАЯ': 136, 'ОБЛ МАГАДАНСКАЯ': 137, 'ОБЛ МОСКОВСКАЯ': 138, 'ОБЛ МУРМАНСКАЯ': 139, 'ОБЛ НИЖЕГОРОДСКАЯ': 140, 'ОБЛ НОВГОРОДСКАЯ': 141, 'ОБЛ НОВОСИБИРСКАЯ': 142, 'ОБЛ ОМСКАЯ': 143, 'ОБЛ ОРЕНБУРГСКАЯ': 144, 'ОБЛ ОРЛОВСКАЯ': 145, 'ОБЛ ПЕНЗЕНСКАЯ': 146, 'ОБЛ ПСКОВСКАЯ': 147, 'ОБЛ РОСТОВСКАЯ': 148, 'ОБЛ РЯЗАНСКАЯ': 149, 'ОБЛ САМАРСКАЯ': 150, 'ОБЛ САРАТОВСКАЯ': 151, 'ОБЛ САХАЛИНСКАЯ': 152, 'ОБЛ СВЕРДЛОВСКАЯ': 153, 'ОБЛ СМОЛЕНСКАЯ': 154, 'ОБЛ ТАМБОВСКАЯ': 155, 'ОБЛ ТВЕРСКАЯ': 156, 'ОБЛ ТОМСКАЯ': 157, 'ОБЛ ТУЛЬСКАЯ': 158, 'ОБЛ ТЮМЕНСКАЯ': 159, 'ОБЛ УЛЬЯНОВСКАЯ': 160, 'ОБЛ ЧЕЛЯБИНСКАЯ': 161, 'ОБЛ ЯРОСЛАВСКАЯ': 162, 'ОБЛ. БЕЛГОРОДСКАЯ': 163, 'ОБЛ. КИРОВСКАЯ': 164, 'ОБЛ. ЛИПЕЦКАЯ': 165, 'ОБЛ. НОВОСИБИРСКАЯ': 166, 'ОБЛ. СВЕРДЛОВСКАЯ': 167, 'ОБЛ. ЧЕЛЯБИНСКАЯ': 168, 'ОБЛ.МОСКОВСКАЯ': 169, 'ОБЛ.НИЖЕГОРОДСКАЯ': 170, 'ОБЛ.РОСТОВСКАЯ': 171, 'ОМСКАЯ': 172, 'ОМСКАЯ ОБЛ': 173, 'ОМСКАЯ ОБЛАСТЬ': 174, 'ОРЁЛ': 175, 'ОРЕНБУРГСКАЯ ОБЛ': 176, 'ОРЕНБУРГСКАЯ ОБЛАСТЬ': 177, 'ОРЛОВСКАЯ ОБЛ': 178, 'ОРЛОВСКАЯ ОБЛАСТЬ': 179, 'ПЕНЗЕНСКАЯ ОБЛ': 180, 'ПЕНЗЕНСКАЯ ОБЛАСТЬ': 181, 'ПЕРМСКАЯ ОБЛ': 182, 'ПЕРМСКИЙ': 183, 'ПЕРМСКИЙ КРАЙ': 184, 'ПРИВОЛЖСКИЙ ФЕДЕРАЛЬНЫЙ ОКРУГ': 185, 'ПРИМОРСКИЙ КРАЙ': 186, 'ПСКОВСКАЯ ОБЛ': 187, 'ПСКОВСКАЯ ОБЛАСТЬ': 188, 'РЕСП АДЫГЕЯ': 189, 'РЕСП АЛТАЙ': 190, 'РЕСП БАШКОРТОСТАН': 191, 'РЕСП БУРЯТИЯ': 192, 'РЕСП ДАГЕСТАН': 193, 'РЕСП ИНГУШЕТИЯ': 194, 'РЕСП КАБАРДИНО-БАЛКАРСКАЯ': 195, 'РЕСП КАЛМЫКИЯ': 196, 'РЕСП КАРАЧАЕВО-ЧЕРКЕССКАЯ': 197, 'РЕСП КАРЕЛИЯ': 198, 'РЕСП КОМИ': 199, 'РЕСП МАРИЙ ЭЛ': 200, 'РЕСП МОРДОВИЯ': 201, 'РЕСП САХА /ЯКУТИЯ/': 202, 'РЕСП СЕВЕРНАЯ ОСЕТИЯ - АЛАНИЯ': 203, 'РЕСП ТАТАРСТАН': 204, 'РЕСП ТЫВА': 205, 'РЕСП УДМУРТСКАЯ': 206, 'РЕСП ХАКАСИЯ': 207, 'РЕСП ЧЕЧЕНСКАЯ': 208, 'РЕСП. БАШКОРТОСТАН': 209, 'РЕСП. КОМИ': 210, 'РЕСП. САХА (ЯКУТИЯ)': 211, 'РЕСП.БАШКОРТОСТАН': 212, 'РЕСПУБЛИКА АДЫГЕЯ': 213, 'РЕСПУБЛИКА АЛТАЙ': 214, 'РЕСПУБЛИКА БУРЯТИЯ': 215, 'РЕСПУБЛИКА ДАГЕСТАН': 216, 'РЕСПУБЛИКА КАЛМЫКИЯ': 217, 'РЕСПУБЛИКА КАРЕЛИЯ': 218, 'РЕСПУБЛИКА КОМИ': 219, 'РЕСПУБЛИКА МАРИЙ ЭЛ': 220, 'РЕСПУБЛИКА МОРДОВИЯ': 221, 'РЕСПУБЛИКА САХА': 222, 'РЕСПУБЛИКА ТАТАРСТАН': 223, 'РЕСПУБЛИКА ТЫВА': 224, 'РЕСПУБЛИКА ХАКАСИЯ': 225, 'РЕСПУБЛИКАТАТАРСТАН': 226, 'РОССИЯ': 227, 'РОСТОВСКАЯ': 228, 'РОСТОВСКАЯ ОБЛ': 229, 'РОСТОВСКАЯ ОБЛАСТЬ': 230, 'РЯЗАНСКАЯ ОБЛ': 231, 'РЯЗАНСКАЯ ОБЛАСТЬ': 232, 'САМАРСКАЯ': 233, 'САМАРСКАЯ ОБЛ': 234, 'САМАРСКАЯ ОБЛАСТЬ': 235, 'САНКТ-ПЕТЕРБУРГ': 236, 'САНКТ-ПЕТЕРБУРГ Г': 237, 'САРАТОВСКАЯ ОБЛ': 238, 'САРАТОВСКАЯ ОБЛАСТЬ': 239, 'САХА /ЯКУТИЯ/': 240, 'САХА /ЯКУТИЯ/ РЕСП': 241, 'САХАЛИНСКАЯ ОБЛ': 242, 'САХАЛИНСКАЯ ОБЛАСТЬ': 243, 'СВЕРДЛОВСКАЯ': 244, 'СВЕРДЛОВСКАЯ ОБЛ': 245, 'СВЕРДЛОВСКАЯ ОБЛАСТЬ': 246, 'СЕВ. ОСЕТИЯ - АЛАНИЯ': 247, 'СЕВЕРНАЯ ОСЕТИЯ - АЛАНИЯ РЕСП': 248, 'СМОЛЕНСКАЯ ОБЛ': 249, 'СМОЛЕНСКАЯ ОБЛАСТЬ': 250, 'СТАВРОПОЛЬСКИЙ': 251, 'СТАВРОПОЛЬСКИЙ КРАЙ': 252, 'ТАМБОВСКАЯ ОБЛ': 253, 'ТАМБОВСКАЯ ОБЛАСТЬ': 254, 'ТАТАРСТАН РЕСП': 255, 'ТВЕРСКАЯ ОБЛ': 256, 'ТВЕРСКАЯ ОБЛАСТЬ': 257, 'ТОМСКАЯ': 258, 'ТОМСКАЯ ОБЛ': 259, 'ТОМСКАЯ ОБЛАСТЬ': 260, 'ТУЛЬСКАЯ ОБЛ': 261, 'ТУЛЬСКАЯ ОБЛАСТЬ': 262, 'ТЫВА РЕСП': 263, 'ТЮМЕНСКАЯ': 264, 'ТЮМЕНСКАЯ ОБЛ': 265, 'ТЮМЕНСКАЯ ОБЛАСТЬ': 266, 'УДМУРТСКАЯ РЕСП': 267, 'УДМУРТСКАЯ РЕСПУБЛИКА': 268, 'УЛЬЯНОВСКАЯ ОБЛ': 269, 'УЛЬЯНОВСКАЯ ОБЛАСТЬ': 270, 'ХАБАРОВСКИЙ КРАЙ': 271, 'ХАКАСИЯ': 272, 'ХАКАСИЯ РЕСП': 273, 'ХАНТЫ-МАНСИЙСКИЙ АВТОНОМНЫЙ ОКРУГ - ЮГРА': 274, 'ХАНТЫ-МАНСИЙСКИЙ АО': 275, 'ЧЕЛЯБИНСКАЯ ОБЛ': 276, 'ЧЕЛЯБИНСКАЯ ОБЛАСТЬ': 277, 'ЧЕЧЕНСКАЯ РЕСП': 278, 'ЧЕЧЕНСКАЯ РЕСПУБЛИКА': 279, 'ЧИТИНСКАЯ ОБЛ': 280, 'ЧУВАШИЯ ЧУВАШСКАЯ РЕСПУБЛИКА -': 281, 'ЧУВАШСКАЯ - ЧУВАШИЯ РЕСП': 282, 'ЧУВАШСКАЯ РЕСП': 283, 'ЧУВАШСКАЯ РЕСПУБЛИКА': 284, 'ЧУВАШСКАЯ РЕСПУБЛИКА - ЧУВАШИЯ': 285, 'ЧУКОТСКИЙ АО': 286, 'ЯМАЛО-НЕНЕЦКИЙ АО': 287, 'ЯРОСЛАВСКАЯ ОБЛ': 288, 'ЯРОСЛАВСКАЯ ОБЛАСТЬ': 289}
    martial_status_dict = {'CIV': 0, 'DIV': 1, 'MAR': 2, 'UNM': 3, 'WID': 4}
    job_position_dict = {'ATP': 0, 'BIS': 1, 'BIU': 2, 'DIR': 3, 'HSK': 4, 'INP': 5, 'INV': 6, 'NOR': 7, 'PNA': 8, 'PNI': 9, 'PNS': 10, 'PNV': 11, 'SPC': 12, 'UMN': 13, 'WOI': 14, 'WRK': 15, 'WRP': 16}
    
    marital_status = convert_to_dict_value(request.marital_status, martial_status_dict)
    job_position = convert_to_dict_value(request.job_position, job_position_dict)
    education = convert_to_dict_value(request.education, education_dict)
    living_region = convert_to_dict_value(request.living_region, living_region_dict)
    #Input for model dataframe
    model_input = input_dataframe(gender=request.gender,
                                  age=request.age,
                                  marital_status=marital_status,
                                  job_position=job_position,
                                  credit_sum=request.credit_sum,
                                  credit_month=request.credit_month,
                                  tariff_id=request.tariff_id,
                                  score_shk=request.score_shk,
                                  education=education,
                                  living_region=living_region,
                                  monthly_income=request.monthly_income,
                                  credit_count=request.monthly_income,
                                  overdue_credit_count=request.overdue_credit_count)
    
    is_null = pd.isna(model_input)
    print(is_null.any().any())
    null_position = np.where(is_null)
    print(f'NaN value found in row {null_position[0]} and column {null_position[1]}')


    prediction = get_model_prediction(model_input)
    updated_db_model = update_model(db_model, prediction.tolist()[0])
    print("passed")
    db.add(updated_db_model)
    db.commit()
    db.refresh(updated_db_model)
    return {"prediction": prediction.tolist()[0]}
    


    
def update_model(model_instance, optional_field_value=None):
    model_instance.open_account_flg = optional_field_value
    return model_instance


# Convert the values to the corresponding dictionary values
def convert_to_dict_value(value, conversion_dict):
    if value in conversion_dict:
        return conversion_dict[value]
    else:
        return None

