from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
import settings

from sqlalchemy import Column, Integer, String, Float,
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy import MetaData


DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

class PatData(DeclarativeBase):
	'''
	Sqlalchemy patient data model

	'''
	__tablename__ = 'patdata'

	id = Column(Integer, primary_key=True),
	patid = Column('patid', String(10)),
	gender = Column('gender', String(1)),
	age = Column('age', Integer),
	engel_score = Column('engel_score', Integer),
	birth_date = Column('birth_date', DateTime),
	outcome = Column('outcome', String(1)),
	hand_dominant = Column('hand_dominant', String(1)),
	seizure_type = Column('seizure_type', String(20)),
	equipment = Column('equipment', String(20)),
	surgery_location = Column('surgery_location', String(20)),
	surgery_date = Column('surgery_date', DateTime)

