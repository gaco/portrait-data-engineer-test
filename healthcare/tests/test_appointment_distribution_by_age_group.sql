-- total of appointments can't be negative
SELECT *
FROM {{ ref('appointment_distribution_by_age_group') }}
WHERE total < 0