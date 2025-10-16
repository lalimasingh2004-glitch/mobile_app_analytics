-- Drop the existing table if it exists
DROP TABLE IF EXISTS user_activity;

-- Create table with your new columns
CREATE TABLE public.user_activity (
    user_id VARCHAR(50) NOT NULL,                
    date DATE NOT NULL,
    session_duration NUMERIC(12,5) NOT NULL,        
    screens_viewed INTEGER NOT NULL,
    app_opens INTEGER NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    user_acquisition_channel VARCHAR(50) NOT NULL,
    user_segment VARCHAR(50) NOT NULL,
    daily_active_users INTEGER NOT NULL,
    retention_rate NUMERIC(6,2) NOT NULL            
);
