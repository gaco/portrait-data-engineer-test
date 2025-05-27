-- What are the most common appointment types by age group?
SELECT
  p.age_group,
  a.appointment_type,
  COUNT(*) AS total
FROM {{ ref('stg_appointments') }} a
JOIN {{ ref('stg_patients') }} p
    ON (a.patient_id = p.patient_id)
GROUP BY p.age_group, a.appointment_type
