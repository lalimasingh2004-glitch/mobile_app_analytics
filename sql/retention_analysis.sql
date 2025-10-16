
--retention rate calcualtion (daily,weekly and monthly)


-- Daily Retention Rate Analysis
SELECT 
    date,
    AVG(retention_rate) as avg_retention_rate,
    MIN(retention_rate) as min_retention_rate,
    MAX(retention_rate) as max_retention_rate,
    COUNT(*) as sample_size
FROM public.user_activity
GROUP BY date
ORDER BY date;


-- High vs Low Retention Sessions

SELECT 
    date,
    retention_rate,
    CASE 
        WHEN retention_rate >= 30 THEN 'High Retention'
        WHEN retention_rate >= 25 THEN 'Medium Retention'
        ELSE 'Low Retention'
    END as retention_category
FROM public.user_activity
group by date,retention_rate
ORDER BY retention_rate DESC;

--one row retention summary
WITH 
first_login AS (
    SELECT user_id, MIN(date) as first_date
    FROM public.user_activity 
    GROUP BY user_id
),
weekly_returners AS (
    SELECT f.user_id
    FROM first_login f
    JOIN public.user_activity u ON f.user_id = u.user_id
    WHERE u.date BETWEEN f.first_date + 1 AND f.first_date + 7
),
monthly_returners AS (
    SELECT f.user_id
    FROM first_login f
    JOIN public.user_activity u ON f.user_id = u.user_id
    WHERE u.date BETWEEN f.first_date + 1 AND f.first_date + 30
)
-- Main query
SELECT 
    COUNT(f.user_id) as total_users,
    COUNT(w.user_id) as weekly_retained,
    COUNT(m.user_id) as monthly_retained,
    ROUND(100.0 * COUNT(w.user_id) / COUNT(f.user_id), 2) as weekly_retention,
    ROUND(100.0 * COUNT(m.user_id) / COUNT(f.user_id), 2) as monthly_retention
FROM first_login f
LEFT JOIN weekly_returners w ON f.user_id = w.user_id
LEFT JOIN monthly_returners m ON f.user_id = m.user_id;

--first date wise retention rate calculation

--first week
WITH first_login AS (
    SELECT user_id, MIN(DATE(date)) as first_date
    FROM public.user_activity GROUP BY user_id
),
retention_7check AS (
    SELECT 
        f.user_id,
        f.first_date,
        CASE WHEN l.date BETWEEN f.first_date + 1 AND f.first_date + 7 
             THEN 1 ELSE 0 END as retained_7day
    FROM first_login f
    LEFT JOIN public.user_activity l ON f.user_id = l.user_id
)
SELECT 
    first_date,
    COUNT(*) as total_users,
    SUM(retained_7day) as retained_users,
    ROUND(100.0 * SUM(retained_7day) / COUNT(*), 2) as weekly_retention_rate
FROM retention_7check
GROUP BY first_date
order by first_date;

--first month
WITH first_login AS (
    SELECT user_id, MIN(DATE(date)) as first_date
    FROM public.user_activity GROUP BY user_id
),
retention_30check AS (
    SELECT 
        f.user_id,
        f.first_date,
        CASE WHEN l.date BETWEEN f.first_date + 1 AND f.first_date + 30
             THEN 1 ELSE 0 END as retained_30day
    FROM first_login f
    LEFT JOIN public.user_activity l ON f.user_id = l.user_id
)
SELECT 
    first_date,
    COUNT(*) as total_users,
    SUM(retained_30day) as retained_users,
    ROUND(100.0 * SUM(retained_30day) / COUNT(*), 2) as month1st_retention_rate
FROM retention_30check
GROUP BY first_date
order by first_date;

--second month
WITH first_login AS (
    SELECT user_id, MIN(DATE(date)) as first_date
    FROM public.user_activity GROUP BY user_id
),
retention_61check AS (
    SELECT 
        f.user_id,
        f.first_date,
        CASE WHEN l.date BETWEEN f.first_date + 31 AND f.first_date + 61
             THEN 1 ELSE 0 END as retained_61day
    FROM first_login f
    LEFT JOIN public.user_activity l ON f.user_id = l.user_id
)
SELECT 
    first_date,
    COUNT(*) as total_users,
    SUM(retained_61day) as retained_users,
    ROUND(100.0 * SUM(retained_61day) / COUNT(*), 2) as month2nd_retention_rate
FROM retention_61check
GROUP BY first_date
order by first_date;

--for the entire period of 61 days
WITH first_login AS (
    SELECT user_id, MIN(DATE(date)) as first_date
    FROM public.user_activity GROUP BY user_id
),
retention_check AS (
    SELECT 
        f.user_id,
        f.first_date,
        CASE WHEN l.date BETWEEN f.first_date + 1 AND f.first_date + 61
             THEN 1 ELSE 0 END as retained_61days
    FROM first_login f
    LEFT JOIN public.user_activity l ON f.user_id = l.user_id
)
SELECT 
    first_date,
    COUNT(*) as total_users,
    SUM(retained_61days) as retained_users,
    ROUND(100.0 * SUM(retained_61days) / COUNT(*), 2) as retention_rate
FROM retention_check
GROUP BY first_date
order by first_date;