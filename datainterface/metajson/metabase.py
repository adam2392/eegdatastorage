# https://www.npmjs.com/package/json-query
# https://pypi.python.org/pypi/jsonschema


class MetaData(object):
    '''
    This is a base class for metadata that is associated with our
    time series data that we get:

    - ECoG, SEEG, EEG

    Each of these need their corresponding metadata that stores important information
    in analyzing these datasets.

    '''

    def __init__(self):
        self.schema = self.getschema()

    def getschema(self):
        raise NotImplementedError(
            'All metadata classes need to implement getschema method.')
