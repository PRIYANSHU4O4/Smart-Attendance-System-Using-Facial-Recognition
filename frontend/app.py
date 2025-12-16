import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import threading
import sys
import os

# -------------------------------------------------
# FIX PROJECT PATH (IMPORTANT)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# -------------------------------------------------
# IMPORT BACKEND MODULES
# -------------------------------------------------
from enrollment.register import register_student_gui
from enrollment.view_students import get_all_students
from attendance.take_attendance import start_attendance
from attendance.view_attendance import get_attendance


# -------------------------------------------------
# MAIN WINDOW
# -------------------------------------------------
root = tk.Tk()
root.title("Smart Attendance System")
root.geometry("900x600")
root.configure(bg="#f4f6f8")
root.resizable(False, False)


# -------------------------------------------------
# HEADER
# -------------------------------------------------
header_frame = tk.Frame(root, bg="#1f2933", height=110)
header_frame.pack(fill="x")

tk.Label(
    header_frame,
    text="GROUP 15 FINAL YEAR PROJECT",
    font=("Helvetica", 16, "bold"),
    fg="white",
    bg="#1f2933",
).pack(pady=(20, 0))

tk.Label(
    header_frame,
    text="SMART ATTENDANCE SYSTEM USING FACIAL RECOGNITION",
    font=("Helvetica", 18, "bold"),
    fg="#4ade80",
    bg="#1f2933",
).pack()


# -------------------------------------------------
# CENTER CONTENT
# -------------------------------------------------
content_frame = tk.Frame(root, bg="#f4f6f8")
content_frame.pack(expand=True)

tk.Label(
    content_frame,
    text="Faculty Control Panel",
    font=("Helvetica", 16, "bold"),
    bg="#f4f6f8",
    fg="#111827",
).pack(pady=25)


# -------------------------------------------------
# FUNCTIONS
# -------------------------------------------------
def register_student():
    enrollment_id = simpledialog.askstring(
        "Student Registration", "Enter Enrollment ID:"
    )
    if not enrollment_id:
        messagebox.showwarning("Input Required", "Enrollment ID is required.")
        return

    name = simpledialog.askstring(
        "Student Registration", "Enter Student Name:"
    )
    if not name:
        messagebox.showwarning("Input Required", "Student name is required.")
        return

    register_student_gui(enrollment_id.strip(), name.strip())


def run_attendance():
    subject = simpledialog.askstring("Subject Name", "Enter Subject Name:")
    if not subject:
        messagebox.showwarning("Input Required", "Subject name is required.")
        return

    threading.Thread(
        target=start_attendance, args=(subject,), daemon=True
    ).start()


def view_attendance_ui():
    subject = simpledialog.askstring("Filter", "Enter Subject (optional):")
    date = simpledialog.askstring("Filter", "Enter Date (DD/MM/YYYY) (optional):")

    records = get_attendance(subject=subject or None, date=date or None)

    win = tk.Toplevel(root)
    win.title("Attendance Records")
    win.geometry("750x400")

    text = tk.Text(win, font=("Courier", 11))
    text.pack(expand=True, fill="both")

    if not records:
        text.insert("end", "No attendance records found.")
        return

    for r in records:
        text.insert("end", f"{r}\n")


def show_student_details():
    students = get_all_students()

    if not students:
        messagebox.showinfo("Student Details", "No students registered yet.")
        return

    win = tk.Toplevel(root)
    win.title("Registered Students")
    win.geometry("600x350")

    cols = ("Enrollment ID", "Student Name")
    tree = ttk.Treeview(win, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=280)

    for student in students:
        tree.insert("", tk.END, values=student)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Button(win, text="Close", command=win.destroy).pack(pady=10)


# -------------------------------------------------
# BUTTONS
# -------------------------------------------------
btn_style = {
    "font": ("Helvetica", 14, "bold"),
    "width": 26,
    "height": 2,
    "bd": 0,
    "cursor": "hand2",
}

tk.Button(
    content_frame,
    text="Register Student",
    bg="#2563eb",
    fg="white",
    command=register_student,
    **btn_style,
).pack(pady=10)

tk.Button(
    content_frame,
    text="Start Attendance",
    bg="#16a34a",
    fg="white",
    command=run_attendance,
    **btn_style,
).pack(pady=10)

tk.Button(
    content_frame,
    text="View Attendance",
    bg="#9333ea",
    fg="white",
    command=view_attendance_ui,
    **btn_style,
).pack(pady=10)

tk.Button(
    content_frame,
    text="Student Details",
    bg="#0f766e",
    fg="white",
    command=show_student_details,
    **btn_style,
).pack(pady=10)


# -------------------------------------------------
# FOOTER
# -------------------------------------------------
footer_frame = tk.Frame(root, bg="#1f2933", height=70)
footer_frame.pack(fill="x")

tk.Label(
    footer_frame,
    text=(
        "Presented by Priyanshu Tiwari | Arijit Saha | "
        "Esha Nandan | Gaurav Kumar Singh"
    ),
    font=("Helvetica", 11),
    fg="white",
    bg="#1f2933",
).pack(pady=22)


# -------------------------------------------------
# START APP
# -------------------------------------------------
root.mainloop()
