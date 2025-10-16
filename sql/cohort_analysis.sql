--cohort analysis

WITH first_login AS (
    SELECT 
        user_id,
        MIN(date) AS first_date
    FROM public.user_activity
    GROUP BY user_id
),
retention_check AS (
    SELECT 
        f.user_id,
        f.first_date,
        -- Day 1 retention
        MAX(CASE WHEN u.date = f.first_date + INTERVAL '1 day'
                 THEN 1 ELSE 0 END) AS d1_retained,

        -- First week retention (days 2–7)
        MAX(CASE WHEN u.date BETWEEN f.first_date + INTERVAL '2 days'
                              AND f.first_date + INTERVAL '7 days'
                 THEN 1 ELSE 0 END) AS w1_retained,

        -- First month retention (days 8–30)
        MAX(CASE WHEN u.date BETWEEN f.first_date + INTERVAL '8 days'
                              AND f.first_date + INTERVAL '30 days'
                 THEN 1 ELSE 0 END) AS m1_retained,

        -- Rest of the period (days 31–61)
        MAX(CASE WHEN u.date BETWEEN f.first_date + INTERVAL '31 days'
                              AND f.first_date + INTERVAL '61 days'
                 THEN 1 ELSE 0 END) AS rest_retained
    FROM first_login f
    LEFT JOIN public.user_activity u 
           ON f.user_id = u.user_id
    GROUP BY f.user_id, f.first_date
)
SELECT 
    first_date AS cohort_date,
    COUNT(*) AS total_users,
    ROUND(100.0 * SUM(d1_retained) / COUNT(*), 2)   AS d1_retention,
    ROUND(100.0 * SUM(w1_retained) / COUNT(*), 2)   AS week1_retention,
    ROUND(100.0 * SUM(m1_retained) / COUNT(*), 2)   AS month1_retention,
    ROUND(100.0 * SUM(rest_retained) / COUNT(*), 2) AS rest_retention
FROM retention_check
GROUP BY first_date
ORDER BY first_date;


