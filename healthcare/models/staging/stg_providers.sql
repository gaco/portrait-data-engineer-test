{{ config(materialized='incremental', unique_key='provider_id', tags=['providers', 'stg']) }}

WITH source AS (
    SELECT
        provider_id,
        name,
        specialty,
        md5(name || specialty) AS record_hash
    FROM {{ source('public', 'providers') }}
),
-- Used Chat GPT here:
{% if not is_incremental() %}
existing AS (
    SELECT NULL::int AS provider_id, NULL::text AS existing_hash WHERE false
),
{% else %}
existing AS (
    SELECT
        provider_id,
        md5(name || specialty) AS existing_hash
    FROM {{ this }}
),
{% endif %}
--
new_or_changed AS (
    SELECT s.*
    FROM source s
    LEFT JOIN existing e ON
     (s.provider_id = e.provider_id)
    WHERE e.existing_hash IS NULL OR e.existing_hash != s.record_hash
)

select
    provider_id,
    name,
    specialty
from new_or_changed