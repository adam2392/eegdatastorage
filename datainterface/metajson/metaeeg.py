from .metabase import MetaData

from jsonschema import validate
# A sample schema, like what we'd get from json.load()
# >>> schema = {
# ...     "type" : "object",
# ...     "properties" : {
# ...         "price" : {"type" : "number"},
# ...         "name" : {"type" : "string"},
# ...     },
# ... }


class MetaDataEEG(MetaData):
    def __init__(self):
        super.__init__(self)

    def getschema(self):
        datascheme = {
            "type": "object",
            "properties": {
                    # patient string (e.g. jh105, ummc001, id001_ac)
                'patient': "string",
                # record id (e.g. sz1, inter2, aslp1)
                'recordid': 'string',
                'datestart': '',
                'dateend': '',
                'birthdate': '',
                'gender': 'string',
                'age': 'string',
                'device': 'string',
                'samplerate': 'float',
                'reference': 'string',
                'clinnotes': 'object',
            }
        }
        return datascheme

    def clinnotes(self):
        datascheme = {
            "type": "object",
            "properties": {
                    'eeg_onsettime': 'float',
                'eeg_offsettime': 'float',
                'clin_onsettime': 'float',
                'clin_offsettime': 'float',
                'notes': 'string',
                'author': 'string'
            }
        }
        return datascheme
