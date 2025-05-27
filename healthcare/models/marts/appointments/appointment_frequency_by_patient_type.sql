-- How does the appointment frequency vary by patient type?
SELECT
  p.patient_type,
  COUNT(a.appointment_id) AS total_appointments
FROM {{ ref('stg_patients') }} p
JOIN {{ ref('stg_appointments') }} a
   ON (p.patient_id = a.patient_id)
GROUP BY p.patient_type
