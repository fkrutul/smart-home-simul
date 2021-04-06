DROP SEQUENCE IF EXISTS personnel_id_seq;

CREATE SEQUENCE personnel_id_seq
       AS integer
       INCREMENT BY 1
       MINVALUE 1
       MAXVALUE 2147483647
       CACHE 1
       NO CYCLE
       OWNED BY personnel.id;

DROP TABLE IF EXISTS appliances CASCADE;

CREATE TABLE appliances
(
   id           text,
   location     text,
   wattage      integer,
   water_usage  integer,
   is_on        boolean
);

DROP TABLE IF EXISTS bath_01 CASCADE;

CREATE TABLE bath_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS bath_02 CASCADE;

CREATE TABLE bath_02
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS baths CASCADE;

CREATE TABLE baths
(
   id        text,
   location  text,
   is_on     boolean
);

DROP TABLE IF EXISTS clothesdryer_01 CASCADE;

CREATE TABLE clothesdryer_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

COMMIT;

DROP TABLE IF EXISTS daily_usage CASCADE;

CREATE TABLE daily_usage
(
   date_  text,
   power  numeric,
   water  numeric,
   cost   numeric
);

COMMIT;

DROP TABLE IF EXISTS dishwasher_01 CASCADE;

CREATE TABLE dishwasher_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS door CASCADE;

CREATE TABLE door
(
   door_id     uuid      NOT NULL,
   last_open   timetz,
   last_close  timetz,
   "open?"     boolean
);

ALTER TABLE door
   ADD CONSTRAINT door_pkey
   PRIMARY KEY (door_id);

DROP TABLE IF EXISTS door_01 CASCADE;

CREATE TABLE door_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS door_02 CASCADE;

CREATE TABLE door_02
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS door_03 CASCADE;

CREATE TABLE door_03
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS ext_doors CASCADE;

CREATE TABLE ext_doors
(
   id        text,
   location  text,
   is_open   boolean
);

DROP TABLE IF EXISTS fan_01 CASCADE;

CREATE TABLE fan_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS fan_01 CASCADE;

CREATE TABLE fan_02
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS garage_01 CASCADE;

CREATE TABLE garage_02
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS garage_01 CASCADE;

CREATE TABLE garage_02
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS health CASCADE;

CREATE TABLE health
(
   date_        text,
   faye_temps   numeric,
   ed_temps     numeric,
   spike_temps  numeric,
   jet_temps    numeric
);

DROP TABLE IF EXISTS hvac_01 CASCADE;

CREATE TABLE hvac_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_01 CASCADE;

CREATE TABLE light_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_02 CASCADE;

CREATE TABLE light_02
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_03 CASCADE;

CREATE TABLE light_03
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_04 CASCADE;

CREATE TABLE light_04
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_05 CASCADE;

CREATE TABLE light_05
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_06 CASCADE;

CREATE TABLE light_06
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_07 CASCADE;

CREATE TABLE light_07
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_08 CASCADE;

CREATE TABLE light_08
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_09 CASCADE;

CREATE TABLE light_09
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_10 CASCADE;

CREATE TABLE light_10
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_11 CASCADE;

CREATE TABLE light_11
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_12 CASCADE;

CREATE TABLE light_12
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_13 CASCADE;

CREATE TABLE light_13
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_14 CASCADE;

CREATE TABLE light_14
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS light_15 CASCADE;

CREATE TABLE light_15
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS lights CASCADE;

CREATE TABLE lights
(
   id        text,
   location  text,
   wattage   integer,
   is_on     boolean
);

DROP TABLE IF EXISTS microwave_01 CASCADE;

CREATE TABLE microwave_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS monthly_usage CASCADE;

CREATE TABLE monthly_usage
(
   month  integer,
   power  numeric,
   water  numeric,
   cost   numeric
);

DROP TABLE IF EXISTS other_doors CASCADE;

CREATE TABLE other_doors
(
   id        text,
   location  text,
   is_open   boolean
);

DROP TABLE IF EXISTS oven_01 CASCADE;

CREATE TABLE oven_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS person CASCADE;

CREATE TABLE person
(
   person_id  uuid   NOT NULL,
   name       text   NOT NULL
);

ALTER TABLE person
   ADD CONSTRAINT person_pkey
   PRIMARY KEY (person_id);

DROP TABLE IF EXISTS personnel CASCADE;

CREATE TABLE personnel
(
   id          serial    NOT NULL,
   first_name  text,
   last_name   text,
   position    text,
   phone       text,
   active      boolean
);

-- Column id is associated with sequence public.personnel_id_seq

DROP TABLE IF EXISTS ref_01 CASCADE;

CREATE TABLE ref_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS stove_01 CASCADE;

CREATE TABLE stove_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS tv_02 CASCADE;

CREATE TABLE tv_02
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS utility_cost CASCADE;

CREATE TABLE utility_cost
(
   utility_namer  text      NOT NULL,
   cost           numeric   NOT NULL
);

ALTER TABLE utility_cost
   ADD CONSTRAINT utility_cost_pkey
   PRIMARY KEY (utility_namer);

DROP TABLE IF EXISTS waterheater_01 CASCADE;

CREATE TABLE waterheater_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_01 CASCADE;

CREATE TABLE window_01
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_02 CASCADE;

CREATE TABLE window_02
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_02 CASCADE;

CREATE TABLE window_02
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_03 CASCADE;

CREATE TABLE window_03
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_04 CASCADE;

CREATE TABLE window_04
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_05 CASCADE;

CREATE TABLE window_05
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_06 CASCADE;

CREATE TABLE window_06
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_07 CASCADE;

CREATE TABLE window_07
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_08 CASCADE;

CREATE TABLE window_08
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_09 CASCADE;

CREATE TABLE window_09
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_10 CASCADE;

CREATE TABLE window_10
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_11 CASCADE;

CREATE TABLE window_11
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_12 CASCADE;

CREATE TABLE window_11
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS window_13 CASCADE;

CREATE TABLE window_11
(
   begin_time  timestamp,
   end_time    timestamp,
   duration    numeric,
   usage       numeric
);

DROP TABLE IF EXISTS windows CASCADE;

CREATE TABLE windows
(
   id        text,
   location  text,
   open      boolean
);

CREATE OR REPLACE FUNCTION public.get_data()
  RETURNS json
  LANGUAGE plpgsql
AS
$body$
BEGIN
RETURN array_to_json(array_agg(public.daily_usage)) FROM public.daily_usage;
END;
$body$
  VOLATILE
  COST 100;

COMMIT;

CREATE OR REPLACE FUNCTION public.reset()
  RETURNS integer
  LANGUAGE plpgsql
AS
$body$
BEGIN
DELETE FROM light_01;
DELETE FROM light_02;
DELETE FROM light_03;
DELETE FROM light_04;
DELETE FROM light_05;
DELETE FROM light_06;
DELETE FROM light_07;
DELETE FROM light_08;
DELETE FROM light_09;
DELETE FROM light_10;
DELETE FROM light_11;
DELETE FROM light_12;
DELETE FROM light_13;
DELETE FROM light_14;
DELETE FROM light_15;
DELETE FROM bath_01;
DELETE FROM bath_02;
DELETE FROM clotheswasher_01;
DELETE FROM clothesdryer_01;
DELETE FROM dishwasher_01;
DELETE FROM door_01;
DELETE FROM door_02;
DELETE FROM door_03;
DELETE FROM fan_01;
DELETE FROM fan_02;
DELETE FROM garage_01;
DELETE FROM garage_02;
DELETE FROM hvac_01;
DELETE FROM microwave_01;
DELETE FROM oven_01;
DELETE FROM ref_01;
DELETE FROM stove_01;
DELETE FROM tv_01;
DELETE FROM tv_02;
DELETE FROM waterheater_01;
DELETE FROM window_01;
DELETE FROM window_02;
DELETE FROM window_03;
DELETE FROM window_04;
DELETE FROM window_05;
DELETE FROM window_06;
DELETE FROM window_07;
DELETE FROM window_08;
DELETE FROM window_09;
DELETE FROM window_10;
DELETE FROM window_11;
DELETE FROM window_12;
DELETE FROM window_13;
DELETE FROM daily_usage;
RETURN 1;
END;
$body$
  VOLATILE
  COST 100;

COMMIT;