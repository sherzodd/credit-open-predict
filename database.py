from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgres://bsvcbotezryjli:cac384c0af4cb890bb4816dceb94052b8a7089a526d71585b9df111f6892b3c8@ec2-99-81-68-240.eu-west-1.compute.amazonaws.com:5432/d78fkkk8qcavid"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()