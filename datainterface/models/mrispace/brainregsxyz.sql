' 
Creates Brain Regions xyz table

For patients, we create a table, where for each patient id, 
we fill with relevant channel xyz data for this patient.
'

DROP TABLE IF EXISTS "regxyz";

CREATE TABLE "regxyz"(
    pat_id TEXT,
    reg_label TEXT,
    x NUMERIC,
    y NUMERIC,
    z NUMERIC, 
);
