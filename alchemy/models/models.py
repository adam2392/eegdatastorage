from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
import settings

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy import MetaData

DeclarativeBase = declarative_base()

'''
Defines our SQL models we will use to store
the hierarchy of data that we receive from hospitals.

We implement patdata as our highest level table, which
regxyz, chanxyz and eegrecords can be extracted that are each
tied to a specific patid. 

This still allows us to store multiple implantations of the same patient, by
just incrementing the patid.

We can store different recordings by incrementing the recordid.
'''

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    dbdir = '/Users/adam2392/Documents/eegdatastorage/datainterface/__db__/'
    if not os.path.exists(dbdir):
        os.makedirs(dbdir)
    DATABASE_PATH = 'sqlite:////Users/adam2392/Documents/eegdatastorage/datainterface/__db__/master.sqlite'
    # create a sqlite database that runs in memory
    # engine = create_engine('sqlite:///:memory:', echo=True)
    engine = create_engine(DATABASE_PATH, echo=True)
    # create_engine(URL(**settings.DATABASE))
    return engine

def create_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

class PatData(DeclarativeBase):
    '''
    Sqlalchemy patient data model

    '''
    __tablename__ = 'patdata'

    id = Column(Integer, primary_key=True)
    patid = Column('patid', String(10))
    gender = Column('gender', String(1))
    age = Column('age', Integer)
    engel_score = Column('engel_score', Integer)
    onset_chans = Column('onset_chans', String)
    # birth_date = Column('birth_date', DateTime)
    outcome = Column('outcome', String(1))
    hand_dominant = Column('hand_dominant', String(1))
    seizure_type = Column('seizure_type', String(20))
    surgery_location = Column('surgery_location', String(20))
    surgery_date = Column('surgery_date', DateTime)
    eeg_localization = Column('eeg_localization', String(20))
    epilepsy_duration = Column('epilepsy_duration', Float)

class Chanxyz(DeclarativeBase):
    # create mrispace data
    __tablename__ = 'chanxyz'

    id = Column(Integer, primary_key=True)
    patid = Column('pat_id', String, ForeignKey('patdata.patid'))#, primary_key=True)
    x = Column('x', Float),
    y = Column('y', Float),
    z = Column('z', Float),

class Regxyz(DeclarativeBase):
    __tablename__ = 'regxyz'
    
    id = Column(Integer, primary_key=True)
    patid = Column('patid', String, ForeignKey('patdata.patid'))#, primary_key=True)
    x = Column('x', Float)
    y = Column('y', Float)
    z = Column('z', Float)

class EegRecord(DeclarativeBase):
    # eegrecord table
    __tablename__ = 'eegrecord'

    id = Column(Integer, primary_key=True)
    patid = Column('pat_id', String, ForeignKey('patdata.patid'))#, primary_key=True)
    chanxyz = Column('chanxyz', None, ForeignKey('chanxyz.id'))
    regxyz = Column('regxyz', None, ForeignKey('regxyz.id'))
    record_id = Column('record_id', String(10))
    filepath = Column('filepath', String(50))
    equipment = Column('equipment', String(20))
    recording_type = Column('recording_type', String(10))
    num_channels = Column('num_channels', Integer)
    sampling_rate = Column('sampling_rate', Float)
    date_record = Column('date_record', DateTime)
    onset_datetime = Column('onset_datetime', DateTime)
    offset_datetime = Column('offset_datetime', DateTime)

