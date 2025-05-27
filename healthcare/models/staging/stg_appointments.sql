{{ config(materialized='incremental', unique_key='appointment_id', tags=['appointments', 'stg']) }}

WITH source AS (
    SELECT
        appointment_id,
        patient_id,
        CAST(appointment_date AS DATE) AS appointment_date,
        appointment_type,
        provider_id
    FROM {{ source('public', 'appointments') }}
)
    SELECT
        appointment_id,
        patient_id,
        appointment_date,
        appointment_type,
        provider_id,
        TRIM(TO_CHAR(appointment_date, 'Day')) AS day_of_week,
        COALESCE(appointment_date - LAG(appointment_date) OVER (partition BY patient_id ORDER BY appointment_date), 0) AS days_since_last_appointment
    FROM source

    {% if is_incremental() %}
        WHERE appointment_date > (
            SELECT MAX(appointment_date) FROM {{ this }}
        )
    {% endif %}