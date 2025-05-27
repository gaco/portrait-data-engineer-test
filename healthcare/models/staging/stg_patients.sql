{{ config(materialized='incremental', unique_key='patient_id',  tags=['patients', 'stg']) }}

WITH source AS (
    SELECT
        patient_id,
        name,
        age,
        gender,
        CAST(registration_date AS DATE) AS registration_date
    FROM {{ source('public', 'patients') }}
)
SELECT
   patient_id,
   name,
   age,
   gender,
   registration_date,
   CASE
       WHEN age IS NULL THEN 'Unknown'
       WHEN age <= 18 THEN '0-18'
       WHEN age <= 30 THEN '19-30'
       WHEN age <= 50 THEN '31-50'
       WHEN age <= 70 THEN '51-70'
       ELSE '71+'
   END AS age_group,
   CASE
       WHEN EXTRACT('MONTH' FROM AGE(CURRENT_DATE, registration_date)) < 6 THEN 'New'
       WHEN EXTRACT('MONTH' FROM AGE(CURRENT_DATE, registration_date)) < 24 THEN 'Regular'
       ELSE 'Long-term'
   END AS patient_type
FROM source

{% if is_incremental() %}
    WHERE registration_date > (
        SELECT MAX(registration_date) FROM {{ this }}
    )
{% endif %}