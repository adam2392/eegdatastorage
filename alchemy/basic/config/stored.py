# -*- coding: utf-8 -*-
#
#
#

"""
Manages reading and writing settings in file

.. moduleauthor:: Adam Li <adam2392@gmail.com>

"""

import os

# File keys
KEY_ADMIN_NAME = 'ADMINISTRATOR_NAME'
KEY_ADMIN_PWD = 'ADMINISTRATOR_PASSWORD'
KEY_ADMIN_EMAIL = 'ADMINISTRATOR_EMAIL'

KEY_TVB_PATH = 'TVB_PATH'
KEY_STORAGE = 'TVB_STORAGE'
KEY_MAX_DISK_SPACE_USR = 'USR_DISK_SPACE'
# During the introspection phase, it is checked if either Matlab or
# octave are installed and available trough the system PATH variable
# If so, they will be used for some analyzers
KEY_MATLAB_EXECUTABLE = 'MATLAB_EXECUTABLE'
KEY_IP = 'SERVER_IP'
KEY_PORT = 'WEB_SERVER_PORT'
KEY_URL_WEB = 'URL_WEB'
KEY_SELECTED_DB = 'SELECTED_DB'
KEY_DB_URL = 'URL_VALUE'
KEY_URL_VERSION = 'URL_TVB_VERSION'
KEY_MAX_THREAD_NR = 'MAXIMUM_NR_OF_THREADS'
KEY_MAX_RANGE_NR = 'MAXIMUM_NR_OF_OPS_IN_RANGE'
KEY_MAX_NR_SURFACE_VERTEX = 'MAXIMUM_NR_OF_VERTICES_ON_SURFACE'
KEY_LAST_CHECKED_FILE_VERSION = 'LAST_CHECKED_FILE_VERSION'
KEY_LAST_CHECKED_CODE_VERSION = 'LAST_CHECKED_CODE_VERSION'
KEY_FILE_STORAGE_UPDATE_STATUS = 'FILE_STORAGE_UPDATE_STATUS'

class SettingsManager(object):
    def __init__(self, config_file_location):
        self.config_file_location = config_file_location
        self.stored_settings = self._read_config_file()

    def _read_config_file(self):
        """
        Get data from the configurations file in the form of a dictionary.
        Return empty dictionary if file not present.
        """
        if not os.path.exists(self.config_file_location):
            return {}

        config_dict = {}
        with open(self.config_file_location, 'r') as cfg_file:
            data = cfg_file.read()
            entries = [line for line in data.split('\n') if not line.startswith('#') and len(line.strip()) > 0]
            for one_entry in entries:
                name, value = one_entry.split('=', 1)
                config_dict[name] = value
        return config_dict

    def add_entries_to_config_file(self, input_data):
        """
        Add to the dictionary of settings already existent in the settings file.

        :param input_data: A dictionary of pairs that need to be added to the config file.
        """
        config_dict = self._read_config_file()
        if config_dict is None:
            config_dict = {}

        for entry in input_data:
            config_dict[entry] = input_data[entry]

        with open(self.config_file_location, 'w') as file_writer:
            for key in config_dict:
                file_writer.write(key + '=' + str(config_dict[key]) + '\n')

        self.stored_settings = self._read_config_file()

    def write_config_data(self, config_dict):
        """
        Overwrite anything already existent in the config file
        """
        with open(self.config_file_location, 'w') as file_writer:
            for key in config_dict:
                file_writer.write(key + '=' + str(config_dict[key]) + '\n')

        self.stored_settings = self._read_config_file()

    def get_attribute(self, key, default=None, dtype=str):
        """
        Get a cfg attribute that could also be found in the settings file.
        """
        try:
            if key in self.stored_settings:
                return dtype(self.stored_settings[key])
        except ValueError:
            ## Invalid convert operation.
            return default
        return default

    def is_first_run(self):
        return self.stored_settings is None or len(self.stored_settings) <= 2
