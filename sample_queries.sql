-- Basic data exploration queries

-- 1. Check table sizes
SELECT 'patients' as table_name, COUNT(*) as row_count FROM patients
UNION ALL
SELECT 'appointments', COUNT(*) FROM appointments
UNION ALL
SELECT 'providers', COUNT(*) FROM providers
UNION ALL
SELECT 'prescriptions', COUNT(*) FROM prescriptions;

-- 2. Patient registration overview
SELECT 
    DATE_TRUNC('month', registration_date) as registration_month,
    COUNT(*) as new_patients
FROM patients
GROUP BY registration_month
ORDER BY registration_month;

-- 3. Appointment types distribution
SELECT 
    appointment_type,
    COUNT(*) as appointment_count
FROM appointments
GROUP BY appointment_type
ORDER BY appointment_count DESC;

-- 4. Provider specialties
SELECT 
    specialty,
    COUNT(*) as provider_count
FROM providers
GROUP BY specialty
ORDER BY provider_count DESC;

-- 5. Medication overview
SELECT 
    medication_name,
    COUNT(DISTINCT patient_id) as unique_patients
FROM prescriptions
GROUP BY medication_name
ORDER BY unique_patients DESC;

-- 6. Basic patient demographics (excluding age)
SELECT 
    gender,
    COUNT(*) as patient_count
FROM patients
GROUP BY gender; 