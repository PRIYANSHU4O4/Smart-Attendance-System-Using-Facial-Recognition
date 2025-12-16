✅ HOW TO RUN THE SMART ATTENDANCE SYSTEM (STEP-BY-STEP)
🔹 SYSTEM REQUIREMENTS

Operating System: Windows 10 / 11 (64-bit)

Python Version: Python 3.10.x (64-bit only)

Camera: Webcam (internal or external)

Internet: Required only for first-time setup

🔹 STEP 1: INSTALL PYTHON (VERY IMPORTANT)

Download Python 3.10.x (64-bit) from:
https://www.python.org/downloads/release/python-31011/

During installation:

✅ Tick “Add Python to PATH”

Click Install Now

Verify installation:

python --version


Output should be similar to:

Python 3.10.11

🔹 STEP 2: EXTRACT / COPY THE PROJECT

Copy the project folder:

Smart_Attendance_System


Place it anywhere (e.g., Desktop or C:\Projects)

Project structure should look like:

Smart_Attendance_System/
├── attendance/
├── backend/
├── enrollment/
├── frontend/
├── data/
├── venv/          (optional – can be recreated)
└── requirements.txt

🔹 STEP 3: OPEN TERMINAL IN PROJECT FOLDER

Open the project folder

Hold Shift + Right Click

Click “Open PowerShell window here” (or Terminal)

🔹 STEP 4: CREATE & ACTIVATE VIRTUAL ENVIRONMENT
python -m venv venv


Activate it:

.\venv\Scripts\activate


You should see:

(venv)

🔹 STEP 5: INSTALL REQUIRED LIBRARIES

Run:

pip install -r requirements.txt


⚠️ This may take a few minutes because it installs:

OpenCV

face_recognition

dlib

numpy

tkinter dependencies

If successful, no red errors will appear.

🔹 STEP 6: RUN THE APPLICATION (GUI)
python frontend/app.py


🎉 The Smart Attendance GUI will open

🔹 HOW TO USE THE APPLICATION
👨‍🏫 Faculty Actions:
1️⃣ Register Student

Click Register Student

Enter:

Enrollment ID

Student Name

Camera opens → face is captured → student registered

2️⃣ Start Attendance

Click Start Attendance

Enter Subject Name

Students stand in front of camera

Attendance recorded automatically

3️⃣ View Attendance

Click View Attendance

Filter by:

Subject (optional)

Date (optional)

Attendance shown in table

🔹 WHERE DATA IS STORED

Student images:

data/images/


Student details:

data/students.csv


Attendance records:

data/Attendance.csv

🔹 COMMON ERRORS & SOLUTIONS
❌ “cv2 / face_recognition not found”

✔ Ensure Python is 3.10 (64-bit)
✔ Ensure virtual environment is activated

❌ Camera not opening

✔ Close other apps using camera (Zoom, Teams)
✔ Restart system

❌ Attendance not saving

✔ Ensure data/ folder exists
✔ Do not rename project folders

🔹 IMPORTANT RULES (TO AVOID ERRORS)

❌ Do NOT delete data/ folder

❌ Do NOT rename project folders

❌ Do NOT use Python 3.11 / 3.12

✅ Always activate venv before running

🎓 WHAT TO SAY IN VIVA (VERY IMPORTANT)

“The system runs inside a Python virtual environment to ensure dependency stability, especially for facial recognition libraries like dlib and OpenCV.”

This is a perfect technical justification.

✅ FINAL ONE-LINE COMMAND (FOR QUICK RUN)
.\venv\Scripts\activate
python frontend/app.py
