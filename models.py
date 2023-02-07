from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from database import Base


class Predictions(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    gender = Column(String)
    age = Column(Integer)
    marital_status = Column(String)
    job_position = Column(String)
    credit_sum = Column(Float)
    credit_month = Column(Integer)
    tariff_id = Column(Float)
    score_shk = Column(Float)
    education = Column(String)
    living_region = Column(String)
    monthly_income = Column(Float)
    credit_count = Column(Float)
    overdue_credit_count = Column(Float)
    open_account_flg =  Column(Integer, default=True)
    

