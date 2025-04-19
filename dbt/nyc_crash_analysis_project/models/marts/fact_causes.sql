with base as (
    select
        cause,
        count(*) as total_crashes
    from {{ref('stg_crashes')}}
    where cause is not null and lower(cause) != 'unspecified'
    group by cause
)

select
    cause,
    count(*) as total_crashes
from base
group by cause
order by total_crashes desc