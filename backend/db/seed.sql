INSERT INTO locations (name, latitude, longitude, timezone)
SELECT 'Pune', 18.5204, 73.8567, 'Asia/Kolkata'
WHERE NOT EXISTS (SELECT 1 FROM locations WHERE name = 'Pune');
