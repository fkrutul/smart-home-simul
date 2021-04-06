CREATE DATABASE "Team1DB"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

CREATE SCHEMA public
    AUTHORIZATION postgres;

COMMENT ON SCHEMA public
    IS 'standard public schema';

GRANT ALL ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO postgres;

CREATE TABLE public.appliance
(
    weekend_use numeric,
    weekday_use numeric,
    wattage integer NOT NULL,
    water_use numeric,
    run_time numeric,
    name text COLLATE pg_catalog."default" NOT NULL,
    app_id uuid NOT NULL,
    uses_per_week integer,
    electric_use numeric,
    CONSTRAINT "Appliances_pkey" PRIMARY KEY (app_id)
)

TABLESPACE pg_default;

ALTER TABLE public.appliance
    OWNER to postgres;
    
ALTER TABLE public.appliance
    ADD CONSTRAINT "Appliances_pkey" PRIMARY KEY (app_id);

CREATE TABLE public.door
(
    door_id uuid NOT NULL,
    last_open time with time zone,
    last_close time with time zone,
    "open?" boolean,
    CONSTRAINT door_pkey PRIMARY KEY (door_id)
)

TABLESPACE pg_default;

ALTER TABLE public.door
    OWNER to postgres;
    
ALTER TABLE public.hot_water_heater
    ADD CONSTRAINT "HotWaterHeater_pkey" PRIMARY KEY (date);

ALTER TABLE public.hot_water_heater
    ADD CONSTRAINT person_id FOREIGN KEY (person_id)
    REFERENCES public.person (person_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

CREATE TABLE public.people_temp
(
    -- Inherited from table public.person: person_id uuid NOT NULL,
    -- Inherited from table public.person: name text COLLATE pg_catalog."default" NOT NULL,
    temp numeric,
    date_time timestamp with time zone
)
    INHERITS (public.person)
TABLESPACE pg_default;

ALTER TABLE public.people_temp
    OWNER to postgres;
    
CREATE TABLE public.person
(
    person_id uuid NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT person_pkey PRIMARY KEY (person_id)
)

TABLESPACE pg_default;

ALTER TABLE public.person
    OWNER to postgres;
    
CREATE TABLE public.shower
(
    begin_time time with time zone NOT NULL,
    end_time time with time zone NOT NULL,
    date date NOT NULL,
    person_id uuid NOT NULL,
    hot_water numeric,
    cold_water numeric,
    CONSTRAINT shower_pkey PRIMARY KEY (begin_time)
)

TABLESPACE pg_default;

ALTER TABLE public.shower
    OWNER to postgres;
    
ALTER TABLE public.shower
    ADD CONSTRAINT shower_pkey PRIMARY KEY (begin_time);
    
CREATE TABLE public.utility_cost
(
    utility_namer text COLLATE pg_catalog."default" NOT NULL,
    cost numeric NOT NULL,
    CONSTRAINT utility_cost_pkey PRIMARY KEY (utility_namer)
)

TABLESPACE pg_default;

ALTER TABLE public.utility_cost
    OWNER to postgres;
    
ALTER TABLE public.utility_cost
    ADD CONSTRAINT utility_cost_pkey PRIMARY KEY (utility_namer);
    
CREATE TABLE public."window"
(
    window_id uuid NOT NULL,
    last_opened time with time zone,
    last_closed time with time zone,
    "open?" boolean,
    CONSTRAINT window_pkey PRIMARY KEY (window_id)
)

TABLESPACE pg_default;

ALTER TABLE public."window"
    OWNER to postgres;
    
ALTER TABLE public."window"
    ADD CONSTRAINT window_pkey PRIMARY KEY (window_id);

CREATE OR REPLACE FUNCTION public.get_data()
  RETURNS json
  LANGUAGE plpgsql
AS
$body$
BEGIN
RETURN array_to_json(ARRAY(SELECT * FROM public.power_usage));
END;
$body$
  VOLATILE
  COST 100;
  
COMMIT;

    
COMMIT;