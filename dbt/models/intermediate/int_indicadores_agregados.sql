-- models/intermediate/int_indicadores_agregados.sql
-- Intermediate: agrega indicadores por região e período
-- Bootcamp CI&T — Do Prompt ao Agente

with stg as (
    select * from {{ ref('stg_indicadores') }}
),

agregado as (
    select
        date_trunc('month', dt_referencia)  as dt_mes,
        extract(year  from dt_referencia)   as nr_ano,
        extract(month from dt_referencia)   as nr_mes,
        extract(quarter from dt_referencia) as nr_trimestre,
        nm_indicador,
        nm_regiao,

        -- Métricas agregadas
        avg(vl_indicador)                   as vl_medio,
        sum(vl_indicador)                   as vl_total,
        min(vl_indicador)                   as vl_minimo,
        max(vl_indicador)                   as vl_maximo,
        count(*)                            as qt_registros,

        -- Variação mês a mês
        avg(vl_indicador)
          - lag(avg(vl_indicador)) over (
              partition by nm_indicador, nm_regiao
              order by date_trunc('month', dt_referencia)
            )                               as vl_variacao_mom,

        current_timestamp                   as dt_carga
    from stg
    group by 1, 2, 3, 4, 5, 6
)

select * from agregado
