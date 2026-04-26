-- models/marts/fato_indicadores.sql
-- Mart: tabela fato final para consumo em BI e ML
-- Star Schema — Bootcamp CI&T — Do Prompt ao Agente

with int_dados as (
    select * from {{ ref('int_indicadores_agregados') }}
),

dim_data as (
    select * from {{ ref('dim_data') }}
),

dim_indicador as (
    select * from {{ ref('dim_indicador') }}
),

dim_regiao as (
    select * from {{ ref('dim_regiao') }}
),

fato as (
    select
        -- Chaves
        dd.id_data,
        di.id_indicador,
        dr.id_regiao,

        -- Métricas
        i.vl_medio,
        i.vl_total,
        i.vl_minimo,
        i.vl_maximo,
        i.qt_registros,
        i.vl_variacao_mom,

        -- Campos de controle
        i.dt_carga
    from int_dados i
    left join dim_data      dd on dd.dt_data = i.dt_mes
    left join dim_indicador di on di.nm_indicador = i.nm_indicador
    left join dim_regiao    dr on dr.nm_regiao = i.nm_regiao
)

select * from fato
