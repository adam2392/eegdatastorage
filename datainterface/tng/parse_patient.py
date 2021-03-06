#!/usr/bin/env python


import datetime
import json
import logging
import os
import re
import sys
import zipfile

import nibabel as nib
import numpy as np
import pandas as pd

from .elecs import Contacts
from . import nifti

def get_sec(time):
    if type(time) == float:
        # Already in seconds
        return time
    elif type(time) == datetime.time:
        return datetime.timedelta(hours=time.hour,
                                 minutes=time.minute,
                                 seconds=time.second,
                                 microseconds=time.microsecond).total_seconds()
    elif type(time) == str:
        h, m, s = time.split(':')
        return int(h)*3600 + int(m)*60 + float(s)
    else:
        raise ValueError("Unexpected time type: %s" % type(time))

def add_same_occurence_index(df, column):
    df['_%s_repeated' % column] = False
    df['_%s_index' % column] = 1

    for key in pd.unique(df[column]):
        if pd.isna(key):
            continue

        subdf = df[df[column] == key]
        if len(subdf) > 1:
            for i, (index, row) in enumerate(subdf.iterrows()):
                df.loc[index, '_%s_repeated' % column] = True
                df.loc[index, '_%s_index' % column] = i + 1

def expand_channels(ch_list):
    ch_list = [a.replace("’", "'") for a in ch_list]

    new_list = []
    for string in ch_list:
        if not string.strip():
            continue

        # A'1
        match = re.match("^([A-Za-z]+[']*)([0-9]+)$", string)
        if match:
            new_list.append(string)
            continue

        # A'1-10
        match = re.match("^([A-Za-z]+[']*)([0-9]+)-([0-9]+)$", string)
        if match:
            name, fst_idx, last_idx = match.groups()
            new_list.extend([name + str(i) for i in range(int(fst_idx), int(last_idx) + 1)])
            continue

        # A'1-A10
        match = re.match("^([A-Za-z]+[']*)([0-9]+)-([A-Za-z]+[']*)([0-9]+)$", string)
        if match:
            name1, fst_idx, name2, last_idx = match.groups()
            if name1 == name2:
                new_list.extend([name1 + str(i) for i in range(int(fst_idx), int(last_idx) + 1)])
                continue

        print("expand_channels: Cannot parse this: %s" % string)

    return new_list

def get_ez_from_regions(xlsx_file, region_names):
    """Return list of indices of EZ regions given in the patient spreadsheet"""

    LH_NAMES_IND = 9
    LH_EZ_IND = 10
    RH_NAMES_IND = 12
    RH_EZ_IND = 13

    df = pd.read_excel(xlsx_file, sheet_name="EZ hypothesis and EI", header=1)

    ez_names = []
    for names_ind, ez_ind in [(LH_NAMES_IND, LH_EZ_IND), (RH_NAMES_IND, RH_EZ_IND)]:
        names_col = df.iloc[:, names_ind]
        mask = names_col.notnull()
        names = names_col[mask]
        ez_mask = df.iloc[:, ez_ind][mask].astype(str) == 'YES'
        ez_names.extend(names[ez_mask])

    return [region_names.index(name) for name in ez_names]


def get_ez_from_contacts(xlsx_file, contacts_file, label_volume_file):
    """Return list of indices of EZ regions given by the EZ contacts in the patient spreadsheet"""

    CONTACTS_IND = 6
    EZ_IND = 7

    df = pd.read_excel(xlsx_file, sheet_name="EZ hypothesis and EI", header=1)

    ez_contacts = []
    contacts_col = df.iloc[:, CONTACTS_IND]
    mask = contacts_col.notnull()
    contacts_names = contacts_col[mask]
    ez_mask = df.iloc[:, EZ_IND][mask] == 'YES'
    ez_contacts.extend(contacts_names[ez_mask])

    contacts = Contacts(contacts_file)
    label_vol = nib.load(label_volume_file)

    ez_inds = []
    for contact in ez_contacts:
        coords = contacts.get_coords(contact)
        region_ind = nifti.point_to_brain_region(coords, label_vol, tol=3.0) - 1   # Minus one to account for the shift
        if region_ind != -1:
            ez_inds.append(region_ind)

    return ez_inds


def save_ez_hypothesis(xlsx_file, tvb_zipfile, contacts_file, label_volume_file, output_file):
    """Extract the EZ hypothesis from the xlsx file and save it to plain text file"""

    with zipfile.ZipFile(tvb_zipfile) as zf:
        with zf.open("centres.txt") as fl:
            region_names = list(np.genfromtxt(fl, usecols=(0,), dtype=str))

    nreg = len(region_names)

    ez_inds_from_regions = get_ez_from_regions(xlsx_file, region_names)
    ez_inds_from_contacts = get_ez_from_contacts(xlsx_file, contacts_file, label_volume_file)
    ez_inds = list(set(ez_inds_from_regions + ez_inds_from_contacts))

    ez_hyp = np.zeros(nreg, dtype=int)
    ez_hyp[ez_inds] = 1

    np.savetxt(output_file, ez_hyp, fmt='%i')



if __name__ == '__main__':
    loglevel = logging.INFO
    if os.environ.get('VERBOSE', False):
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel)
    cmd = sys.argv[1]
    eval(cmd)(*sys.argv[2:])
