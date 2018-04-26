' 
Creates Meta Data Tables

For patients, we create a table, where for each patient, 
we fill with relevant data relating to this patient. 
We then have a record table that links to filepaths of 
each recording for this patient. 

Each recording has:
- filepath
- recording type (SEEG, ECoG, EEG)
- number of channels 
- sampling_rate

'

DROP TABLE IF EXISTS "eegrecord";

-- For each eeg recording for a patient, their specific data is stored
CREATE TABLE "eegrecord"(
	id INTEGER,
    pat_id TEXT,
    record_id TEXT,
    filepath TEXT,
    -- clinez_chans FOREIGN_KEY,
    recording_type TEXT,
    num_channels INTEGER,
    sampling_rate NUMERIC,
    onset_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    offset_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
);

-- For each channel, we need to store a row that references which patient, recording id this was hypothesized
CREATE TABLE "clinchans"(
	id INTEGER,
	pat_id TEXT,
	record_id TEXT,
	clinez_chan TEXT,
);