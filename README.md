# eegdatastorage
A repository for eeg data and its metadata storage.

# Installation

    pip install -r requirements.txt

# Models
This module is for storing all the SQL models we have that sqlalchemy will store and integrate with. We define different models for different types of data, with the common factor being a single patient. However, these datasets can have varying depth with respect to the patient. For example, one patient can have many eegrecord tables, while only one patdata table. 

1. Elecspace
For storing metadata related to each eegrecord we have, such as the recording datetime, onsettimes if available, etc.

2. MRIspace
For storing data related to the MRI space, such as channels xyz, regions xyz coordinates that would be used.

Stores the inverse gain matrix file as well.

3. Patspace
For the patient specific data, which would be clinically tied data, such as seizure type, age, engel score, etc.

4. To Be Added:
to the MRIspace add the data that is extrapolated from the dMRI, such as tract lengths, number of tracts, triangles, areas, normal vectors for the cortical surface.

This should give a connectivity matrix between the different regions of the brian, but since this connectivity matrix can change depending on what parcellation we use, then we don't necessarily store this.

# DataParse
This module is meant to parse the data necessary and format it before feeding into our SQL tables.


