from db import *
import psycopg2
import logging


def normalize_db():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        create_table_query = """
            create table if not exists Countries (
                country_id serial primary key,
                country_name varchar(100) unique not null
            );
            
            create table if not exists Cities (
                city_id serial primary key,
                city_name varchar(100) unique not null,
                country_id int not null,
                latitude decimal,
                longitude decimal,
                foreign key (country_id) references Countries(country_id)
            );
            
            create table if not exists TargetTypes (
                target_type_id serial primary key,
                target_type_name varchar(255) unique not null
            );
            
            
            create table if not exists Targets (
                target_id serial primary key,
                target_industry varchar(255) not null,
                city_id int not null,
                target_type_id int,
                target_priority int,
                foreign key (city_id) references Cities(city_id),
                foreign key (target_type_id) references TargetTypes (target_type_id)
            );
        """
        cur.execute(create_table_query)
        logging.info("Tables create successfully")

        normalize_query = """
            insert into Countries (country_name)
            select distinct target_country
            FROM mission
            where target_country is not NULL
            on conflict (country_name) do nothing;
            
            insert into Cities (city_name, country_id, latitude, longitude)
            select distinct
                m.target_city,
                c.country_id,
                m.target_latitude::decimal,
                m.target_longitude::decimal
            from mission m
            join Countries c on m.country = c.country_name
            where m.target_city is not null
            on conflict (city_name) do nothing;
            
            insert into TargetTypes (target_type_name)
            select distinct target_type
            from mission
            where target_type is not null
            on conflict (target_type_name) do nothing;
            
            insert into Targets (target_industry, target_priority, city_id, target_type_id)
            select distinct
                m.target_industry,
                m.target_priority::integer,
                ci.city_id,
                tt.target_type_id
            from mission m
            inner join Cities ci on m.target_city = ci.city_name
            inner join TargetTypes tt on m.target_type = tt.target_type_name
            where m.target_id is not NULL and m.target_industry is not null
            on conflict (target_id) do nothing;
        """
        cur.execute(normalize_query)
        logging.info("Tables normalize successfully")
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error is : {e}")
        return False
    finally:
        release_db_connection(conn)
