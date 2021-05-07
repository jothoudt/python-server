CREATE TABLE "owners" (
"id" SERIAL PRIMARY KEY,
"owner" VARCHAR
);

CREATE TABLE "pets"(
"id" SERIAL PRIMARY KEY,
"owner_id" int REFERENCES owners,
"breed" VARCHAR,
"color" VARCHAR,
"checked_in" DATE
);

ALTER TABLE pets ALTER COLUMN checked_in TYPE TIMESTAMPTZ

CREATE OR REPLACE FUNCTION trigger_set_timestamp() 
RETURNS TRIGGER AS $$ 
BEGIN 
    NEW.updated_at = NOW(); 
    RETURN NEW; 
    END; 
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp 
BEFORE UPDATE ON expenses 
FOR EACH ROW 
EXECUTE PROCEDURE trigger_set_timestamp();

ALTER TABLE pets ADD are_checked_in BOOLEAN DEFAULT FALSE

ALTER TABLE pets ADD name VARCHAR;