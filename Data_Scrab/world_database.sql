DROP TABLE IF EXISTS "worlddata";
CREATE TABLE "worlddata" (
	"index" int NOT NULL PRIMARY KEY,
    "rep_country_code" int NOT NULL,
    "rep_countries" varchar,
    "par_country_code" int,
    "par_countries" varchar,
    "item" varchar,
    "element" varchar,
    "year" int,
    "unit" varchar,
    "value" float 
);