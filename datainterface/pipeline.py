from sqlalchemy.orm import sessionmaker
from .models.models import db_connect, create_tables, 
from .models.models import PatData, Chanxyz, Regxyz, Eegrecord

class EegPipeline(object):
	'''
	The eeg pipeline for storing the metadata and related
	data for eeg records in the database.

	'''
	def __init__(self):
		'''
		Init the db connection and sessionmaker

		Creates the tables
		'''
		engine = db_connect()
		create_tables(engine)
		self.Session = sessionmaker(bind=engine)

	def add_record(self, eegrecord):
		pass

	def 