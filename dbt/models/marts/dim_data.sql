-- models/marts/dim_data.sql
-- Dimensão Data — Bootcamp CI&T — Do Prompt ao Agente

with datas as (
    select
        generate_series(
            '2020-01-01'::date,
            '2030-12-31'::date,
            interval '1 month'
        )::date as dt_data
),

dim as (
    select
        row_number() over (order by dt_data) as id_data,
        dt_data,
        extract(year    from dt_data)::int   as nr_ano,
        extract(month   from dt_data)::int   as nr_mes,
        extract(quarter from dt_data)::int   as nr_trimestre,
        to_char(dt_data, 'Month')            as nm_mes,
        to_char(dt_data, 'YYYY-MM')          as cd_ano_mes
    from datas
)

select * from dim
