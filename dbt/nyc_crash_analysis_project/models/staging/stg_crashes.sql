with raw as(
    select * from {{source('nyc_traffic_data','raw_crashes')}} 
)

select
    DATE(crash_date) as crash_date,
    COALESCE(upper(borough),'UNK') as borough,
    upper(on_street_name) as on_street_name,
    cast(number_of_persons_injured as int64) as num_injured,
    cast(number_of_persons_killed as int64) as num_killed,
    contributing_factor_vehicle_1 as cause,
    vehicle_type_code1 as vehicle_type
from raw
where crash_date is not null