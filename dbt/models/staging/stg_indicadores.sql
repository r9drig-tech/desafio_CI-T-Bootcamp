-- models/staging/stg_indicadores.sql
-- Staging: padroniza dados brutos da fonte para uso interno
-- Bootcamp CI&T — Do Prompt ao Agente

with source as (
    select * from {{ source('raw', 'indicadores') }}
),

renamed as (
    select
        cast(data as date)         as dt_referencia,
        cast(valor as float)       as vl_indicador,
        upper(trim(indicador))     as nm_indicador,
        upper(trim(regiao))        as nm_regiao,
        current_timestamp          as dt_carga
    from source
    where valor is not null
      and data  is not null
)

select * from renamed
