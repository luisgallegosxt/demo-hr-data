select dp.department
, jb.job
, sum(case when quarter(he.datetime) = 1 then 1 else 0 end) as q1
, sum(case when quarter(he.datetime) = 2 then 1 else 0 end) as q2
, sum(case when quarter(he.datetime) = 3 then 1 else 0 end) as q3
, sum(case when quarter(he.datetime) = 4 then 1 else 0 end) as q4
from hired_employees he
join departments dp on dp.id = he.department_id
join jobs jb on jb.id = he.job_id
where 1=1
and year(he.datetime) = '2021'
group by 1,2
order by 1,2
;