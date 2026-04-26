-- models/marts/dim_indicador.sql
-- Dimensão Indicador — Bootcamp CI&T — Do Prompt ao Agente

with source as (
    select distinct
        nm_indicador
    from {{ ref('stg_indicadores') }}
)

select
    row_number() over (order by nm_indicador) as id_indicador,
    nm_indicador,
    current_timestamp                          as dt_carga
from source
