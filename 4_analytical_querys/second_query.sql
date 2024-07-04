with predata as (
select dp.id
, dp.department
, count(he.id) as hired
from hired_employees he
join departments dp on dp.id = he.department_id
where 1=1
and year(datetime) = 2021
group by 1,2
)
, average as (
select avg(hired) as average
from predata
)
select *
from predata 
where hired >= (select average from average)
order by hired desc
;