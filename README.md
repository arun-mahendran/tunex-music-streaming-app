🎵 TuneX – Music Streaming Web Application

TuneX is a role-based music streaming web application built using Flask.
The project demonstrates real-world concepts such as authentication, authorization, playlist management, admin moderation, and AI-powered lyrics transcription.

This project focuses on functionality, clarity, and clean UI, making it suitable for learning and showcasing full-stack development skills.

🚀 Features

👤 User
User registration and login

Browse and play songs

Create, rename, and delete playlists

Add songs to playlists

Drag-and-drop playlist reordering

Dynamic lyrics display during playback

Dark / Light theme toggle

Notifications from admin actions

🎨 Creator

Upload songs (MP3 / WAV)

View uploaded songs

Track play count analytics

Receive admin notifications

Creator dashboard & analytics view

🛠 Admin

View platform statistics

View all users and creators

Block / unblock users

Delete songs with reason-based notifications

Monitor content and activity

🤖 AI Integration

Lyrics are generated using Google Gemini API

Lyrics are transcribed from uploaded audio

Clean line-by-line lyrics display

Lyrics are cached after first generation

🧱 Tech Stack
Layer	Technology
Frontend	HTML, CSS, JavaScript
Backend	Python (Flask)
ORM	SQLAlchemy
Database	SQLite
Authentication	Werkzeug Security
AI	Google Gemini API
UI	Glassmorphism, Dark/Light mode
📂 Project Structure
PROJECT/
│
├── main.py
├── .env
├── requirements.txt
├── README.md
│
├── controller/
│   ├── config.py
│   ├── database.py
│   └── models.py
│
├── instance/
│   └── msa.sqlite3
│
├── static/
│   ├── uploads/
│   └── tunex.png
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── user_dashboard.html
│   ├── creator_dashboard.html
│   ├── creator_analytics.html
│   ├── admin_dashboard.html
│   ├── profile.html
│   ├── edit_profile.html
│   └── change_password.html
│
└── .gitignore


⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/tunex.git
cd tunex

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Environment configuration

Create a .env file:

GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key

5️⃣ Run the application
python main.py


Access the app at:

http://127.0.0.1:5000

🔐 Default Admin Credentials
Email: admin@tunex.com
Password: admin123


⚠️ For demo purposes only.

🎯 Learning Outcomes

Role-based access control

Flask application structuring

SQLAlchemy ORM usage

Playlist and media handling

Admin moderation logic

AI API integration

Frontend–backend coordination

UI/UX design using pure CSS & JS

📌 Future Enhancements

Global modal music player

Accurate time-synced lyrics

Recommendation system

Song likes and favorites

Cloud-based media storage

🧑‍💻 Author

Arun Mahendran B
Pre-final Year Engineering Student
Aspiring Software Engineer
