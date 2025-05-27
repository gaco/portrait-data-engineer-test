-- How does prescription frequency correlate with appointment frequency?

WITH prescriptions_appointments AS (
    SELECT
        p.patient_id,
        COALESCE(COUNT(DISTINCT pr.prescription_id), 0) AS total_prescriptions, -- maximo 7
        COALESCE(COUNT(DISTINCT a.appointment_id), 0) AS total_appointments -- maximo 5
    FROM {{ ref('stg_patients') }} p
    LEFT JOIN {{ ref('stg_prescriptions') }} pr
    	ON (p.patient_id = pr.patient_id)
    LEFT JOIN  {{ ref('stg_appointments') }} a
    	ON (p.patient_id = a.patient_id)
    GROUP BY p.patient_id
),
bucket AS (
    SELECT
        patient_id,
        total_prescriptions,
        total_appointments,
        CASE
          WHEN total_prescriptions = 0 THEN 'None'
          WHEN total_prescriptions BETWEEN 1 AND 2 THEN 'Few'
          WHEN total_prescriptions BETWEEN 3 AND 5 THEN 'Moderate'
          WHEN total_prescriptions BETWEEN 6 AND 10 THEN 'Frequent'
          ELSE 'Very Frequent'
        END AS prescription_frequency_bucket
    FROM prescriptions_appointments
)

SELECT
    prescription_frequency_bucket,
    COUNT(*) AS num_patients,
    AVG(total_prescriptions)::numeric(10,2) AS avg_prescriptions,
    AVG(total_appointments)::numeric(10,2) AS avg_appointments
FROM bucket
GROUP BY prescription_frequency_bucket
ORDER BY
    CASE prescription_frequency_bucket
        WHEN 'None' THEN 1
        WHEN 'Few' THEN 2
        WHEN 'Moderate' THEN 3
        WHEN 'Frequent' THEN 4
        WHEN 'Very Frequent' THEN 5
    END
