-- Monthly trend data should not have nulls
SELECT *
FROM {{ ref('prescription_trend_by_month') }}
WHERE month IS NULL OR total_prescriptions IS NULL;
