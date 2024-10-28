-- Attendance table for database

DROP TABLE IF EXISTS attendance;

CREATE TABLE attendance (
    id INTEGER PRIMARY KEY, -- foreign key referencing students table
    checkInTime DATETIME DEFAULT CURRENT_TIMESTAMP -- timestamp of check-in
);