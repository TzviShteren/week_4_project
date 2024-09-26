-- query 1
create function get_all_attacks_by_year(year_f int) returns TABLE (country VARCHAR(100), air_force VARCHAR(100), mission_count bigint) AS $$
begin
    return QUERY select m.country, m.air_force, count(*) as mission_count
            from mission m
            where extract(year from m.mission_date) = year_f
            group by m.country, m.air_force;
end;
$$ language plpgsql;

with air_force_missions as(
    SELECT * FROM get_all_attacks_by_year(1941)
)
select country, air_force, mission_count
from air_force_missions
where (country, mission_count) in (select country, max(mission_count) from air_force_missions group by country);


-- query 2
EXPLAIN ANALYZE select target_country, bomb_damage_assessment
                from mission
                where airborne_aircraft:: INTEGER > 5
                  and bomb_damage_assessment is not null
                group by target_country, bomb_damage_assessment;
