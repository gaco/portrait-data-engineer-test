-- -- What is the distribution of patients across age groups?
SELECT
  age_group,
  COUNT(*) AS num_patients
FROM {{ ref('stg_patients') }}
GROUP BY age_group
