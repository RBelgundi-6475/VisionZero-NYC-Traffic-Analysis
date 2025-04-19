with base as(
    select * from {{ref('stg_crashes')}}
)

select
    crash_date,
    borough,
    count(*) as total_crashes,
    sum(num_injured) as total_injuries,
    sum(num_killed) as total_deaths
from base
group by crash_date, borough