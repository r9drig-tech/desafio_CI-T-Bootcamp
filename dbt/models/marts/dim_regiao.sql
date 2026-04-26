-- models/marts/dim_regiao.sql
-- Dimensão Região — Bootcamp CI&T — Do Prompt ao Agente

with source as (
    select distinct nm_regiao
    from {{ ref('stg_indicadores') }}
),

enriquecido as (
    select
        row_number() over (order by nm_regiao) as id_regiao,
        nm_regiao,
        case nm_regiao
            when 'AC' then 'Norte'
            when 'AM' then 'Norte'
            when 'AP' then 'Norte'
            when 'PA' then 'Norte'
            when 'RO' then 'Norte'
            when 'RR' then 'Norte'
            when 'TO' then 'Norte'
            when 'AL' then 'Nordeste'
            when 'BA' then 'Nordeste'
            when 'CE' then 'Nordeste'
            when 'MA' then 'Nordeste'
            when 'PB' then 'Nordeste'
            when 'PE' then 'Nordeste'
            when 'PI' then 'Nordeste'
            when 'RN' then 'Nordeste'
            when 'SE' then 'Nordeste'
            when 'DF' then 'Centro-Oeste'
            when 'GO' then 'Centro-Oeste'
            when 'MS' then 'Centro-Oeste'
            when 'MT' then 'Centro-Oeste'
            when 'ES' then 'Sudeste'
            when 'MG' then 'Sudeste'
            when 'RJ' then 'Sudeste'
            when 'SP' then 'Sudeste'
            when 'PR' then 'Sul'
            when 'RS' then 'Sul'
            when 'SC' then 'Sul'
            else 'Não identificado'
        end as nm_macrorregiao,
        current_timestamp as dt_carga
    from source
)

select * from enriquecido
