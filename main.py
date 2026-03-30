# Academic Timetable Conflict Detection System
# Developed using Python, Tkinter, and SQLite

import sqlite3
import tkinter as tk
from tkinter import ttk

# -------- DATABASE --------
conn = sqlite3.connect("timetable.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT NOT NULL,
    subject TEXT NOT NULL,
    faculty TEXT NOT NULL,
    room TEXT NOT NULL,
    day TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL
)
""")

# -------- FORMAT TIME --------
def format_time(t):
    parts = t.split(":")
    return f"{int(parts[0]):02d}:{int(parts[1]):02d}"

# -------- CLEAR INPUT --------
def clear_fields():
    entry_class.delete(0, tk.END)
    entry_subject.delete(0, tk.END)
    entry_faculty.delete(0, tk.END)
    entry_room.delete(0, tk.END)
    combo_day.set("Monday")
    entry_start.delete(0, tk.END)
    entry_end.delete(0, tk.END)

# -------- ADD ENTRY --------
def add_entry():
    class_name = entry_class.get()
    subject = entry_subject.get()
    faculty = entry_faculty.get()
    room = entry_room.get()
    day = combo_day.get()

    try:
        start_time = format_time(entry_start.get())
        end_time = format_time(entry_end.get())
    except:
        message_label.config(text="Invalid time format! Use HH:MM", fg="orange")
        return

    # Validation
    if not (class_name and subject and faculty and room and day and start_time and end_time):
        message_label.config(text="Please fill all fields.", fg="orange")
        return

    # -------- CONFLICT DETECTION --------
    cursor.execute("""
        SELECT class_name, subject, faculty, room, start_time, end_time
        FROM timetable
        WHERE day=? AND (start_time < ? AND end_time > ?)
    """, (day, end_time, start_time))

    conflicts = cursor.fetchall()
    conflict_messages = []

    for c in conflicts:
        if c[2] == faculty:
            conflict_messages.append(f"Faculty '{faculty}' already has a class at {c[4]} - {c[5]}")
        if c[3] == room:
            conflict_messages.append(f"Room '{room}' is already occupied at {c[4]} - {c[5]}")
        if c[0] == class_name:
            conflict_messages.append(f"Class '{class_name}' already has a subject at {c[4]} - {c[5]}")

    if conflict_messages:
        message_label.config(text="\n".join(conflict_messages), fg="red")
        return

    # Insert
    cursor.execute("""
        INSERT INTO timetable
        (class_name, subject, faculty, room, day, start_time, end_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (class_name, subject, faculty, room, day, start_time, end_time))

    conn.commit()
    message_label.config(text="Entry added successfully!", fg="green")
    clear_fields()

# -------- VIEW + DELETE --------
def view_timetable():
    view_win = tk.Toplevel(root)
    view_win.title("Full Timetable")
    view_win.geometry("750x350")

    tree = ttk.Treeview(
        view_win,
        columns=("ID","Class","Subject","Faculty","Room","Day","Time"),
        show="headings"
    )
    tree.pack(fill="both", expand=True)

    for col in ("ID","Class","Subject","Faculty","Room","Day","Time"):
        tree.heading(col, text=col)

    cursor.execute("""
        SELECT id, class_name, subject, faculty, room, day, start_time, end_time
        FROM timetable
        ORDER BY day,start_time
    """)
    rows = cursor.fetchall()

    for r in rows:
        tree.insert("", "end",
            values=(r[0], r[1], r[2], r[3], r[4], r[5], f"{r[6]} - {r[7]}")
        )

    def delete_selected():
        selected = tree.selection()

        if not selected:
            return

        for item in selected:
            values = tree.item(item, "values")
            record_id = values[0]

            cursor.execute("DELETE FROM timetable WHERE id=?", (record_id,))
            conn.commit()
            tree.delete(item)

    tk.Button(view_win, text="Delete Selected", command=delete_selected,
              bg="red", fg="white").pack(pady=10)

# -------- UI --------
root = tk.Tk()
root.title("Academic Timetable Conflict Detection System")
root.geometry("500x450")

title = tk.Label(root, text="Academic Timetable Manager", font=("Arial", 14, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Class Name").grid(row=0, column=0, pady=5, sticky="w")
entry_class = tk.Entry(frame, width=25)
entry_class.grid(row=0, column=1)

tk.Label(frame, text="Subject").grid(row=1, column=0, pady=5, sticky="w")
entry_subject = tk.Entry(frame, width=25)
entry_subject.grid(row=1, column=1)

tk.Label(frame, text="Faculty").grid(row=2, column=0, pady=5, sticky="w")
entry_faculty = tk.Entry(frame, width=25)
entry_faculty.grid(row=2, column=1)

tk.Label(frame, text="Room").grid(row=3, column=0, pady=5, sticky="w")
entry_room = tk.Entry(frame, width=25)
entry_room.grid(row=3, column=1)

tk.Label(frame, text="Day").grid(row=4, column=0, pady=5, sticky="w")
combo_day = ttk.Combobox(frame,
    values=["Monday","Tuesday","Wednesday","Thursday","Friday"],
    width=22
)
combo_day.grid(row=4, column=1)
combo_day.set("Monday")

tk.Label(frame, text="Start Time (HH:MM)").grid(row=5, column=0, pady=5, sticky="w")
entry_start = tk.Entry(frame, width=25)
entry_start.grid(row=5, column=1)

tk.Label(frame, text="End Time (HH:MM)").grid(row=6, column=0, pady=5, sticky="w")
entry_end = tk.Entry(frame, width=25)
entry_end.grid(row=6, column=1)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Entry", command=add_entry, width=15).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="View Timetable", command=view_timetable, width=15).grid(row=0, column=1)

# -------- MESSAGE LABEL (IMPORTANT FOR RECORDING) --------
message_label = tk.Label(root, text="", fg="red", font=("Arial", 10, "bold"), wraplength=450)
message_label.pack(pady=10)

# Run
root.mainloop()

conn.close()
