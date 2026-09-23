-- ============================================================
-- JOB MARKET INTELLIGENCE
-- SQL ANALYSIS
-- Step 5.2 - Overall Job Market
-- ============================================================


-- ------------------------------------------------------------
-- QUERY 1: Total number of job postings
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS total_job_postings
FROM job_postings_analysis;
-- ============================================================
-- STEP 5.3 - SALARY ANALYSIS
-- ============================================================


-- ============================================================
-- QUERY 2: Overall salary statistics
-- ============================================================

SELECT
    COUNT(*) AS total_jobs,
    ROUND(AVG(salary_avg_usd), 2) AS avg_salary_usd,
    ROUND(MIN(salary_avg_usd), 2) AS min_salary_usd,
    ROUND(MAX(salary_avg_usd), 2) AS max_salary_usd,
    ROUND(AVG(salary_range_usd), 2) AS avg_salary_range_usd
FROM job_postings_analysis;


-- ============================================================
-- QUERY 3: Salary by experience level
-- ============================================================

SELECT
    experience_level,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_avg_usd), 2) AS avg_salary_usd,
    ROUND(MIN(salary_avg_usd), 2) AS min_salary_usd,
    ROUND(MAX(salary_avg_usd), 2) AS max_salary_usd
FROM job_postings_analysis
GROUP BY experience_level
ORDER BY avg_salary_usd DESC;


-- ============================================================
-- QUERY 4: Salary by employment type
-- ============================================================

SELECT
    employment_type,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_avg_usd), 2) AS avg_salary_usd,
    ROUND(AVG(applicants_estimate), 2) AS avg_applicants
FROM job_postings_analysis
GROUP BY employment_type
ORDER BY avg_salary_usd DESC;


-- ============================================================
-- QUERY 5: Salary by remote option
-- ============================================================

SELECT
    remote_option,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_avg_usd), 2) AS avg_salary_usd,
    ROUND(AVG(applicants_estimate), 2) AS avg_applicants
FROM job_postings_analysis
GROUP BY remote_option
ORDER BY avg_salary_usd DESC;


-- ============================================================
-- QUERY 6: Highest-paying job titles
-- ============================================================

SELECT
    job_title,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_avg_usd), 2) AS avg_salary_usd,
    ROUND(AVG(applicants_estimate), 2) AS avg_applicants
FROM job_postings_analysis
GROUP BY job_title
HAVING COUNT(*) >= 100
ORDER BY avg_salary_usd DESC
LIMIT 10;