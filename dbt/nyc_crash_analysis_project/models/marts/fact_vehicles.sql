with base as(
    select
        vehicle_type
    from {{ref('stg_crashes')}}
    where vehicle_type is not null and lower(vehicle_type)!= 'unknown'
)

select
    vehicle_type,
    count(*) as total_crashes
from base
group by vehicle_type
order by total_crashes desc