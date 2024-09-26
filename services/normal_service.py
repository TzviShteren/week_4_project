from db import *
import psycopg2
import logging
def normalize_db():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        create_mission_query = """
            CREATE TABLE mission
(
    mission_id                          INTEGER PRIMARY KEY,
    mission_date                        DATE,
    theater_of_operations               VARCHAR(100),
    country                             VARCHAR(100),
    air_force                           VARCHAR(100),
    unit_id                             VARCHAR(100),
    aircraft_series                     VARCHAR(100),
    callsign                            VARCHAR(100),
    mission_type                        INTEGER,    -- INTEGER
    takeoff_base                        VARCHAR(255),
    takeoff_location                    VARCHAR(255),
    takeoff_coordinates_id              INT REFERENCES coordinates (coordinates_id),
    target_id                           INT REFERENCES target (id),
    altitude_hundreds_of_feet           NUMERIC(7, 2),
    airborne_aircraft                   NUMERIC(4, 1),
    attacking_aircraft                  INTEGER,
    bombing_aircraft                    INTEGER,
    aircraft_returned                   INTEGER,
    aircraft_failed                     INTEGER,
    aircraft_damaged                    INTEGER,
    aircraft_lost                       INTEGER,
    high_explosives                     INTEGER,    -- INTEGER
    high_explosives_type                VARCHAR(255),
    high_explosives_weight_pounds       VARCHAR(25),
    high_explosives_weight_tons         NUMERIC(10, 2),
    incendiary_devices                  INTEGER,    -- INTEGER
    incendiary_devices_type             VARCHAR(255),
    incendiary_devices_weight_pounds    NUMERIC(10, 2),
    incendiary_devices_weight_tons      NUMERIC(10, 2),
    fragmentation_devices               INTEGER,
    fragmentation_devices_type          VARCHAR(255),
    fragmentation_devices_weight_pounds NUMERIC(10, 2),
    fragmentation_devices_weight_tons   NUMERIC(10, 2),
    total_weight_pounds                 NUMERIC(10, 2),
    total_weight_tons                   NUMERIC(10, 2),
    time_over_target                    VARCHAR(8), -- Combining military time with normal time has the option of normalizing by doing only one type
    bomb_damage_assessment              VARCHAR(255),
    source_id                           INTEGER     -- INTEGER
);
        """

        create_target_query = """
            create table target
(
    id             INTEGER PRIMARY KEY,
    target_id      INTEGER,
    country        VARCHAR(100),
    city           VARCHAR(100),
    type           VARCHAR(100),
    industry       VARCHAR(255),
    priority       INTEGER,
    coordinates_id INT REFERENCES coordinates (coordinates_id)
);
        """

        create_coordinates_query = """
        create table coordinates
(
    coordinates_id INTEGER PRIMARY KEY,
    latitude       VARCHAR(100),
    longitude      VARCHAR(100)
);
        """

        cur = conn.cursor()
        cur.executemany([create_mission_query, create_target_query, create_coordinates_query])
        conn.commit()

        cur.execute("SELECT * FROM mission_s")

        while True:
            customer_row = cur.fetchone()
            if customer_row is None:
                break

            mission_id = customer_row[1]
            mission_date = customer_row[3]
            theater_of_operations = customer_row[4]
            target_country = customer_row[17]
            target_city = customer_row[18]
            target_type = customer_row[19]
            target_industry = customer_row[20]
            target_priority = customer_row[21]
            target_latitude = customer_row[22]
            target_longitude = customer_row[23]
            takeoff_latitude = customer_row[11]
            takeoff_longitude = customer_row[12]

            insert_coordinates_query = """
                        INSERT INTO coordinates (latitude, longitude) VALUES (%s, %s) RETURNING coordinates_id;
                        """
            cur.execute(insert_coordinates_query, (takeoff_latitude, takeoff_longitude))
            takeoff_coordinates_id = cur.fetchone()[0]

            cur.execute(insert_coordinates_query, (target_latitude, target_longitude))
            target_coordinates_id = cur.fetchone()[0]

            insert_target_query = """
                        INSERT INTO target (target_id, country, city, type, industry, priority, coordinates_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
                        """
            cur.execute(insert_target_query, (
                mission_id, target_country, target_city, target_type, target_industry, target_priority,
                target_coordinates_id
            ))
            target_id = cur.fetchone()[0]

            insert_mission_query = """
                        INSERT INTO mission (
                            mission_id, mission_date, theater_of_operations, country, air_force, unit_id, aircraft_series, callsign, mission_type,
                            takeoff_base, takeoff_location, takeoff_coordinates_id, target_id, altitude_hundreds_of_feet, airborne_aircraft, 
                            attacking_aircraft, bombing_aircraft, aircraft_returned, aircraft_failed, aircraft_damaged, aircraft_lost,
                            high_explosives, high_explosives_type, high_explosives_weight_pounds, high_explosives_weight_tons,
                            incendiary_devices, incendiary_devices_type, incendiary_devices_weight_pounds, incendiary_devices_weight_tons,
                            fragmentation_devices, fragmentation_devices_type, fragmentation_devices_weight_pounds, fragmentation_devices_weight_tons,
                            total_weight_pounds, total_weight_tons, time_over_target, bomb_damage_assessment, source_id
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        """
            cur.execute(insert_mission_query, (
                mission_id, mission_date, theater_of_operations, customer_row[5], customer_row[6], customer_row[7],
                customer_row[8],
                customer_row[9], customer_row[10], customer_row[11], customer_row[12], takeoff_coordinates_id,
                target_id,
                customer_row[14], customer_row[15], customer_row[16], customer_row[17], customer_row[18],
                customer_row[19],
                customer_row[20], customer_row[21], customer_row[22], customer_row[23], customer_row[24],
                customer_row[25],
                customer_row[26], customer_row[27], customer_row[28], customer_row[29], customer_row[30],
                customer_row[31],
                customer_row[32], customer_row[33], customer_row[34], customer_row[35]
            ))

        conn.commit()
        logging.info("Tables normalize successfully")
        return True
    except psycopg2.Error as e:
        print(f"Error is : {e}")
        return False
    finally:
        release_db_connection(conn)

