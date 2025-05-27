-- total_appointments must be bigger than 0
SELECT *
FROM {{ ref('appointment_frequency_by_patient_type') }}
WHERE total_appointments <= 0