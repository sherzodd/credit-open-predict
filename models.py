from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from database import Base


class Predictions(Base):
    __tablename__ = "predictions"

    gender = Column(String, index=True)
    age = Column(Integer, index=True)
    marital_status = Column(String, unique=True, index=True)
    job_position = Column(String, index=True)
    credit_sum = Column(Float, index=True)
    credit_month = Column(Integer, index=True)
    tariff_id = Column(Float, index=True)
    score_shk = Column(Float, index=True)
    education = Column(String, index=True)
    living_region = Column(String, index=True)
    monthly_income = Column(Float, index=True)
    credit_count = Column(Float, index=True)
    overdue_credit_count = Column(Float, index=True)
    open_account_flg =  Column(Integer, default=True)
    

