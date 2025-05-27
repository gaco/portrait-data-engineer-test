-- What are the most prescribed medication categories by age group?
SELECT
  p.age_group,
  unnest(pr.medication_category) AS category,
  COUNT(*) AS total
FROM {{ ref('stg_prescriptions') }} pr
JOIN {{ ref('stg_patients') }} p
    on (pr.patient_id = p.patient_id)
GROUP BY p.age_group, category
