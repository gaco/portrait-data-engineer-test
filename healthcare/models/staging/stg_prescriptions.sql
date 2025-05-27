{{ config(materialized='incremental', unique_key='prescription_id', tags=['prescriptions', 'stg']) }}

WITH source AS (
    SELECT
        prescription_id,
        patient_id,
        medication_name,
        CAST(prescription_date AS DATE) AS prescription_date
    FROM {{ source('public', 'prescriptions') }}
),
transformed AS (
    SELECT
        prescription_id,
        patient_id,
        medication_name,
        prescription_date,
        CASE
            WHEN LOWER(medication_name) = 'ibuprofen'       THEN ARRAY['inflammatory', 'pain', 'arthritis']
            WHEN LOWER(medication_name) = 'atorvastatin'    THEN ARRAY['heart', 'pain']
            WHEN LOWER(medication_name) = 'metformin'       THEN ARRAY['diabetes']
            WHEN LOWER(medication_name) = 'amoxicillin'     THEN ARRAY['infection']
            WHEN LOWER(medication_name) = 'lisinopril'      THEN ARRAY['hypertension', 'heart']
            WHEN LOWER(medication_name) = 'aspirin'         THEN ARRAY['pain', 'fever', 'inflammatory']
            ELSE ARRAY['other']
        END AS medication_category,
        ROW_NUMBER() over (PARTITION BY patient_id, medication_name ORDER BY prescription_date) AS rn
    FROM source
)

SELECT
    prescription_id,
    patient_id,
    medication_name,
    prescription_date,
    medication_category,
    CASE WHEN rn = 1 THEN 'First-time' ELSE 'Repeat' END AS prescription_frequency
FROM transformed

{% if is_incremental() %}
    WHERE prescription_date > (
        SELECT MAX(prescription_date) FROM {{ this }}
    )
{% endif %}