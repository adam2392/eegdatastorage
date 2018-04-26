' 
Creates Channel xyz table

For patients, we create a table, where for each patient id, 
we fill with relevant channel xyz data for this patient.
'

DROP TABLE IF EXISTS "chanxyz";

CREATE TABLE "chanxyz"(
    pat_id TEXT,
    chan_label TEXT,
    x NUMERIC,
    y NUMERIC,
    z NUMERIC, 
);
