from sqlalchemy.orm import sessionmaker
from models.models import db_connect, create_tables
from models.models import PatData, Chanxyz, Regxyz, EegRecord

from dataparse.reader import CSVReader

class EegPipeline(object):
    '''
    The eeg pipeline for storing the metadata and related
    data for eeg records in the database.
    '''
    def __init__(self, datafile=None):
        '''
        Init the db connection and sessionmaker

        Creates the tables
        '''
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)
        self.s = self.Session()

        if datafile is not None:
            self.csvreader = CSVReader(datafile)

        # column mapping of excel columns to patdata column names
        self.patcolmapping = {
            'patient id': 'patid',
            'gender': 'gender',
            'age at surgery': 'age',
            'engel score': 'engel_score',
            'outcome': 'outcome',
            'hand dominant': 'hand_dominant',
            'seizure type': 'seizure_type',
            'location of surgery': 'surgery_location',
            'localization from eeg': 'eeg_localization',
            'date of treatment': 'surgery_date',
            'onset electrodes': 'onset_chans',
            'time since first seizure': 'epilepsy_duration'
        }

    def loadcsv(self, datafile):
        # load in the data and add a record
        self.csvreader = CSVReader(datafile)
        data = self.csvreader.loadcsv()

        # add patient data
        self._add_patdata(data)

    def _add_record(self, db_record):
        self.s.add(db_record)

    def update_records(self, tablename, query):
        pass

    def _add_patdata(self, data):
        try:
            records = dict()

            # loop through columns of the data
            for col in data:
                # cast all the columns to lowercase and compare
                if col.lower() in self.patcolmapping.keys():
                    # get the colname 
                    colname = self.patcolmapping[col.lower()]
                    records[colname.lower()] = data[col]
            # create the database record from PatData schema       
            db_record = PatData(**records)
            # add to our session
            self._add_record(db_record)
        except:
            self.s.rollback()
        finally:
            self.s.close()

    def _add_eegrecord(self, data):
        try:
            records = dict()

            # loop through columns of the data
            for col in data:
                # cast all the columns to lowercase and compare
                if col in self.patcolmapping.keys():
                    # get the colname 
                    colname = self.patcolmapping[col]
                    records[colname] = data[col]
            # create the database record from PatData schema       
            db_record = EegRecord(**records)
            # add to our session
            self._add_record(db_record)
        except:
            self.s.rollback()
        finally:
            self.s.close()

    def add_chanxyz(self, data):
        try:
            records = dict()
            # loop through columns of the data
            # for col in data:
            #     # cast all the columns to lowercase and compare
            #     if col.lower() in self.chancolmapping.keys():
            #         # get the colname 
            #         colname = self.chancolmapping[col.lower()]
            #         records[colname.lower()] = data[col]
            # create the database record from PatData schema       
            db_record = Chanxyz(**records)
            # add to our session
            self._add_record(db_record)
        except:
            self.s.rollback()
        finally:
            self.s.close()

    def add_regxyz(self, data):
        try:
            records = dict()
            # loop through columns of the data
            # for col in data:
            #     # cast all the columns to lowercase and compare
            #     if col.lower() in self.regcolmapping.keys():
            #         # get the colname 
            #         colname = self.regcolmapping[col.lower()]
            #         records[colname.lower()] = data[col]
            # create the database record from PatData schema       
            db_record = Regxyz(**records)
            # add to our session
            self._add_record(db_record)

        except:
            self.s.rollback()

        finally:
            self.s.close()

if __name__ == '__main__':
    pipeline = EegPipeline()