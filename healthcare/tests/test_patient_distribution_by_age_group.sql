-- total of patients can't be negative
SELECT *
FROM {{ ref('patient_distribution_by_age_group') }}
WHERE num_patients < 0