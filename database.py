from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://postgres:thrymr%40123@localhost:5432/QuizapplicationYT'

engine=create_engine(URL_DATABASE)

Sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()