-- For each patient, we have a specific row that has some identifying unique metadata
CREATE TABLE "patdata"(
    pat_id TEXT,
    gender TEXT,
    age NUMERIC,
    birth_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    engel_score INTEGER,
    outcome BOOLEAN,
    hand_dominant TEXT,
    clin_center TEXT,
    seizure_type TEXT,
    equipment TEXT,
    surgery_location TEXT,
    surgery_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
);

