--DUA CALCULATION

--standard dua
SELECT 
    date,
    daily_active_users as DAU
FROM public.user_activity
group by date , daily_active_users
ORDER BY date;

--  DAU with Session Metrics
SELECT 
    date,
    daily_active_users as DAU,
    COUNT(*) as total_sessions,
    AVG(session_duration) as avg_session_duration,
    SUM(screens_viewed) as total_screens_viewed,
    AVG(screens_viewed) as avg_screens_per_session
FROM public.user_activity
GROUP BY date, daily_active_users
ORDER BY date;

--Peak and Low Activity Days
SELECT 
    date,
    daily_active_users as DAU,
    CASE 
        WHEN daily_active_users = (SELECT MAX(daily_active_users) FROM public.user_activity) THEN 'Peak Day'
        WHEN daily_active_users = (SELECT MIN(daily_active_users) FROM public.user_activity) THEN 'Low Day'
        ELSE 'Regular Day'
    END as activity_level
FROM public.user_activity
GROUP BY date, daily_active_users
ORDER BY daily_active_users DESC;

-- DAU Summary Statistics
SELECT 
    COUNT(DISTINCT date) as total_days,
    MIN(daily_active_users) as min_DAU,
    MAX(daily_active_users) as max_DAU,
    AVG(daily_active_users) as avg_DAU,
    ROUND(STDDEV(daily_active_users), 2) as DAU_standard_deviation
FROM public.user_activity;