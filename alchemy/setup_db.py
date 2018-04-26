from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy import Table,  MetaData

from sqlalchemy.ext.declarative import declarative_base

'''
These classes and functions will mainly setup the database
that we will need to use that interfaces the various sources of data
that we have: 
	- MRI space data = channels xyz, brain regions xyz, 
	- EEG record data = the eeg record space data tied to each eeg
	recording given to us
	- Patient data = the specific data tied to each patient

One can also refer to the SQL files within each directory
for the schema layout.

Here, we mainly use SQLite for its ease of having a file construct
that works as a db.

'''
DATABASE_PATH = 'sqlite:////Users/adam2392/Documents/eegdatastorage/datainterface/master.db'
# create a sqlite database that runs in memory
# engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine(DATABASE_PATH, echo=True)
# engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')

# define our parent TABLE object
metadata = MetaData()

# for using the declarative api
# Base = declarative_base()

# patdata table
patdata = Table('patdata', metadata,
	Column('pat_id', String, primary_key=True),
	Column('gender', String(1)),
	Column('age', Integer),
	Column('engel_score', Integer),
	Column('birth_date', DateTime),
	Column('outcome', String(1)),
	Column('hand_dominant', String(1)),
	Column('seizure_type', String(20)),
	Column('equipment', String(20)),
	Column('surgery_location', String(20)),
	Column('surgery_date', DateTime)
)

# create mrispace data
chanxyz = Table('chanxyz', metadata,
	Column('pat_id', String, primary_key=True),
	Column('x', Float),
	Column('y', Float),
	Column('z', Float),
)

regxyz = Table('regxyz', metadata,
	Column('pat_id', String, primary_key=True),
	Column('x', Float),
	Column('y', Float),
	Column('z', Float),
)

# eegrecord table
eegrecord = Table('eegrecord', metadata,
	Column('pat_id', String, primary_key=True),
	Column('chanxyz', None, ForeignKey('chanxyz.pat_id')),
	Column('regxyz', None, ForeignKey('regxyz.pat_id')),
	Column('record_id', String(10)),
	Column('filepath', String(50)),
	Column('recording_type', String(10)),
	Column('num_channels', Integer),
	Column('sampling_rate', Float),
	Column('date_record', DateTime),
	Column('onset_datetime', DateTime),
	Column('offset_datetime', DateTime)
)

metadata.create_all(engine)

# conn = engine.connect()