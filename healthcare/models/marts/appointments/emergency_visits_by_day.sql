-- Are there specific days of the week with higher emergency visits?
SELECT
  a.day_of_week,
  COUNT(*) AS emergency_visits
FROM {{ ref('stg_appointments') }} a
WHERE LOWER(appointment_type) = 'emergency'
GROUP BY a.day_of_week
