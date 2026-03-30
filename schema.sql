-- Academic Timetable Conflict Detection System
-- SQL Schema + Sample Data + CRUD Operations

---

## -- TABLE CREATION (SCHEMA)

CREATE TABLE timetable (
id INTEGER PRIMARY KEY AUTOINCREMENT,
class_name TEXT NOT NULL,
subject TEXT NOT NULL,
faculty TEXT NOT NULL,
room TEXT NOT NULL,
day TEXT NOT NULL,
start_time TEXT NOT NULL,
end_time TEXT NOT NULL
);

---

## -- SAMPLE DATA 

INSERT INTO timetable (class_name, subject, faculty, room, day, start_time, end_time)
VALUES ('S4 CSE A', 'OS', 'Anoop', 'R203', 'Monday', '09:00', '10:00');

INSERT INTO timetable (class_name, subject, faculty, room, day, start_time, end_time)
VALUES ('S6 CSE A', 'Artificial Intelligence', 'Akhil', 'Lab 3', 'Monday', '09:00', '10:00');

INSERT INTO timetable (class_name, subject, faculty, room, day, start_time, end_time)
VALUES ('S4 CSE B', 'Data Mining', 'Ryan Mathew', 'Lab 2', 'Monday', '10:00', '11:00');

INSERT INTO timetable (class_name, subject, faculty, room, day, start_time, end_time)
VALUES ('S2 CSE A', 'COA', 'Sonia', 'R209', 'Thursday', '09:00', '10:00');

INSERT INTO timetable (class_name, subject, faculty, room, day, start_time, end_time)
VALUES ('S4 CSE A', 'Maths', 'Jitty', 'R107', 'Wednesday', '09:00', '10:00');

---

## -- CRUD OPERATIONS

-- SELECT (View Timetable)
SELECT * FROM timetable;

-- UPDATE (Modify Entry)
UPDATE timetable
SET subject = 'DBMS'
WHERE id = 3;

-- DELETE (Remove Entry)
DELETE FROM timetable
WHERE id = 5;

-- INSERT (Add New Entry)
INSERT INTO timetable (class_name, subject, faculty, room, day, start_time, end_time)
VALUES ('S3 CSE A', 'Computer Networks', 'Bibin', 'R201', 'Friday', '11:00', '12:00');
