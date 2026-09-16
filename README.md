<p align="center">
  <img src="logo.png" width="120" alt="No Proxy logo">
</p>

<h1 align="center">No Proxy</h1>

<p align="center">Making attendance faster using AI — face and voice recognition for the classroom.</p>

<p align="center">
  <a href="https://noproxy-main.streamlit.app/"><b>Live App →</b></a>
</p>

---

## About

Marking attendance by roll call wastes class time and is easy to fake — a friend answers "present" for someone who never showed up. **No Proxy** replaces the roll call with two AI-driven methods:

- **Face attendance** — a teacher snaps one or more photos of the classroom. The app detects every face, matches each one against enrolled students, and marks them present.
- **Voice attendance** — students say "present" out loud. A single recording is split into individual utterances, and each voice is matched to a registered student.

Students register once with a selfie (and optionally their voice), join classes by scanning a QR code, and can track their own attendance percentage per subject.

## Features

**For teachers**
- Username + password accounts, with passwords hashed using bcrypt
- Create subjects with a subject code and section
- Take attendance from classroom photos — multiple photos per session are supported for large rooms
- Take attendance by voice from a single bulk recording
- Review the detected students before saving the session
- Share a class via a join link and auto-generated QR code
- Attendance records dashboard across all subjects

**For students**
- Passwordless login — the app recognises your face
- Register with a selfie, with optional voice enrollment
- Join a class instantly by scanning the teacher's QR code
- Enroll in or unenroll from subjects manually
- See per-subject attendance history

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Database / Auth | Supabase (PostgreSQL) |
| Face detection & embeddings | dlib + `face_recognition_models` |
| Face classification | scikit-learn (linear SVM) |
| Voice embeddings | Resemblyzer |
| Audio processing | librosa |
| QR codes | segno |
| Password hashing | bcrypt |

## How It Works

### Face recognition pipeline

1. dlib's frontal face detector locates every face in the uploaded image.
2. A shape predictor finds facial landmarks (eyes, nose, lips), and dlib's recognition model converts each face into a **128-dimensional embedding**.
3. Embeddings for all registered students are pulled from Supabase and used to train a linear **SVM classifier** (cached, and refreshed whenever a new student registers).
4. For each detected face, the SVM predicts a student ID, then the Euclidean distance to that student's stored embedding is checked against a threshold of `0.6`. Only confident matches are marked present — this second check stops the classifier from confidently mislabelling strangers.

### Voice recognition pipeline

1. Audio is loaded at a 16 kHz sample rate and preprocessed for Resemblyzer.
2. Resemblyzer produces a **256-dimensional voice embedding** per utterance.
3. For bulk attendance, `librosa.effects.split` segments the recording on silence so multiple students saying "present" are separated. Segments shorter than 0.5 s are discarded as noise.
4. Each segment is matched to the enrolled students of that subject using cosine similarity, with a threshold of `0.65`.

Only students enrolled in the subject are considered as candidates, which keeps matching fast and accurate.

## Project Structure

```
No-Proxy/
├── app.py                     # Entry point — routes to student/teacher/home
├── requirements.txt
├── logo.png
└── src/
    ├── screens/
    │   ├── home_screen.py     # Student vs Teacher landing page
    │   ├── student_screen.py  # Student login, registration, dashboard
    │   └── teacher_screen.py  # Teacher auth, attendance, subjects, records
    ├── components/
    │   ├── dialog_create_subject.py
    │   ├── dialog_enroll.py
    │   ├── dialog_add_photo.py
    │   ├── dialog_voice_attendance.py
    │   ├── dialog_auto_enroll.py     # QR / join-code enrollment
    │   ├── dialog_share_subject.py   # Join link + QR code
    │   ├── dialog_attendance_result.py
    │   ├── subject_card.py
    │   └── header.py
    ├── pipelines/
    │   ├── face_pipeline.py   # dlib embeddings + SVM classifier
    │   └── voice_pipeline.py  # Resemblyzer embeddings + speaker matching
    ├── database/
    │   ├── config.py          # Supabase client
    │   └── db.py              # All queries
    └── UI/
        └── base_layout.py     # Custom CSS and styling
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- A free [Supabase](https://supabase.com) project

### Installation

```bash
git clone https://github.com/heydhruvharish/No-Proxy.git
cd No-Proxy

# Create and activate a virtual environment
python -m venv venv
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

> **Note:** `dlib-bin` ships prebuilt wheels, so no C++ compiler is needed on most systems.

### Configuration

Create `.streamlit/secrets.toml` in the project root:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

This file is gitignored — never commit your keys.

### Database schema

Create these tables in Supabase:

| Table | Columns |
|---|---|
| `teachers` | `teacher_id`, `username` (unique), `password` (bcrypt hash), `name` |
| `students` | `student_id`, `name`, `face_embedding` (float array), `voice_embedding` (float array, nullable) |
| `subjects` | `subject_id`, `subject_code` (unique), `name`, `section`, `teacher_id` → `teachers` |
| `subject_student` | `student_id` → `students`, `subject_id` → `subjects` |
| `attendance_logs` | `student_id`, `subject_id`, `timestamp`, `status` |

### Run

```bash
streamlit run app.py --server.runOnSave true
```

The app opens at `http://localhost:8501`.

## Usage

**Teacher**
1. Register a teacher account, then log in.
2. Create a subject under **Manage subjects**.
3. Hit **Share code** to show the QR code and join link — students scan it to enroll instantly.
4. Go to **Take attendance**, pick the subject, and either upload classroom photos or record voices.
5. Review the detected students and save the session.
6. Check **Attendance records** for history.

**Student**
1. Open the Student Portal and log in with your face — or register a new profile with a selfie.
2. Scan the teacher's QR code to join a class in one tap, or enroll manually.
3. View your attendance per subject from the dashboard.

## Limitations

- Face recognition needs reasonably well-lit, front-facing photos; heavily angled or blurred faces may be missed.
- Large classrooms are better covered with several photos taken from different angles.
- Voice attendance assumes students speak one at a time — heavy overlap reduces accuracy.
- The SVM is retrained on every new registration, so registration is briefly slower as the student count grows.

## Roadmap

- [ ] Attendance export to CSV / Excel
- [ ] Liveness detection to block photo-of-a-photo spoofing
- [ ] Bulk student import for teachers
- [ ] Attendance analytics and low-attendance alerts

## License

Add a license of your choice (MIT is a common default for projects like this).

---

<p align="center">Built by <a href="https://github.com/heydhruvharish">@heydhruvharish</a></p>
