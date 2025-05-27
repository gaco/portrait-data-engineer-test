SELECT
  patient_id,
  COUNT(*) AS prescriptions_count
FROM {{ ref('stg_prescriptions') }}
GROUP BY 1