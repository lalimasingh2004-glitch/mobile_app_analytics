-- Create table for the generated dataset
CREATE TABLE user_activity (
    session_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    session_duration DECIMAL(5,2) NOT NULL,
    screens_viewed INTEGER NOT NULL,
    app_version VARCHAR(10) NOT NULL,
    device_type VARCHAR(20) NOT NULL,
    acquisition_channel VARCHA