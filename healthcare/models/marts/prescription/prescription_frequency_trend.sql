SELECT
  EXTRACT('year' FROM prescription_date) AS year,
  EXTRACT('month' FROM prescription_date) AS month,
  prescription_frequency,
  COUNT(*) AS total
FROM {{ ref('stg_prescriptions') }}
GROUP BY 1, 2, 3
