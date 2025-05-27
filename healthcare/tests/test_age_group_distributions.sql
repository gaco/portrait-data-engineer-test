--  All age_groups in appointment_distribution_by_age_group must exist in patient_distribution_by_age_group
SELECT a.*
FROM {{ ref('appointment_distribution_by_age_group') }} a
LEFT JOIN {{ ref('patient_distribution_by_age_group') }} p
  ON (a.age_group = p.age_group)
WHERE p.age_group IS NULL