from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

from mutagen.mp3 import MP3
from mutagen.wave import WAVE

from controller.config import Config
from controller.database import db
from controller.models import (
    User, Role, Genre, Song,
    Playlist, PlaylistSong
)

# ================= APP SETUP =================
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"mp3", "wav"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ================= DB INIT =================
with app.app_context():
    db.create_all()

    # Roles
    for r in ["ADMIN", "CREATOR", "USER"]:
        if not Role.query.filter_by(role_name=r).first():
            db.session.add(Role(role_name=r))

    # Genres
    if not Genre.query.first():
        db.session.add_all([
            Genre(genre_name="Pop"),
            Genre(genre_name="Rock"),
            Genre(genre_name="Hip-Hop"),
            Genre(genre_name="Classical")
        ])

    db.session.commit()

    # Hardcoded Admin
    admin = User.query.filter_by(email="admin@tunex.com").first()
    if not admin:
        admin = User(
            username="TUNEX_ADMIN",
            email="admin@tunex.com",
            password_hash=generate_password_hash("admin123")
        )
        admin.roles.append(Role.query.filter_by(role_name="ADMIN").first())
        db.session.add(admin)
        db.session.commit()


# ================= AUTH =================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        role = request.form["role"]

        if user and check_password_hash(user.password_hash, request.form["password"]):
            if role not in [r.role_name for r in user.roles]:
                return "Unauthorized role"

            session["user_id"] = user.user_id
            session["username"] = user.username
            session["role"] = role

            if role == "CREATOR":
                return redirect(url_for("creator_dashboard"))
            if role == "USER":
                return redirect(url_for("user_dashboard"))

        return "Invalid login"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(email=request.form["email"]).first():
            return "Email already exists"

        user = User(
            username=request.form["username"],
            email=request.form["email"],
            password_hash=generate_password_hash(request.form["password"])
        )

        role = Role.query.filter_by(role_name=request.form["role"]).first()
        user.roles.append(role)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ================= CREATOR =================
@app.route("/dashboard/creator")
def creator_dashboard():
    if session.get("role") != "CREATOR":
        return redirect(url_for("login"))

    return render_template(
        "creator_dashboard.html",
        username=session["username"],
        genres=Genre.query.all(),
        songs=Song.query.filter_by(creator_id=session["user_id"]).all()
    )


@app.route("/creator/upload", methods=["POST"])
def creator_upload():
    if session.get("role") != "CREATOR":
        return redirect(url_for("login"))

    file = request.files["song"]
    title = request.form["title"]
    genre_id = int(request.form["genre_id"])

    if not allowed_file(file.filename):
        return "Invalid file"

    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    duration = (
        int(MP3(path).info.length)
        if filename.endswith(".mp3")
        else int(WAVE(path).info.length)
    )

    song = Song(
        title=title,
        file_path=path,
        duration=duration,
        creator_id=session["user_id"],
        genre_id=genre_id
    )

    db.session.add(song)
    db.session.commit()

    return redirect(url_for("creator_dashboard"))


@app.route("/creator/edit/<int:song_id>", methods=["POST"])
def edit_song(song_id):
    if session.get("role") != "CREATOR":
        return redirect(url_for("login"))

    song = Song.query.get_or_404(song_id)

    if song.creator_id != session["user_id"]:
        return "Unauthorized", 403

    song.title = request.form["title"]
    db.session.commit()

    return redirect(url_for("creator_dashboard"))


# ================= 🔥 FIXED DELETE ROUTE =================
@app.route("/creator/delete/<int:song_id>", methods=["POST"])
def delete_song(song_id):
    if session.get("role") != "CREATOR":
        return redirect(url_for("login"))

    song = Song.query.get_or_404(song_id)

    if song.creator_id != session["user_id"]:
        return "Unauthorized", 403

    # 🔥 DELETE DEPENDENT RECORDS FIRST
    PlaylistSong.query.filter_by(song_id=song_id).delete()

    db.session.delete(song)
    db.session.commit()

    return redirect(url_for("creator_dashboard"))


# ================= USER =================
@app.route("/dashboard/user")
def user_dashboard():
    if session.get("role") != "USER":
        return redirect(url_for("login"))

    return render_template(
        "user_dashboard.html",
        username=session["username"],
        songs=Song.query.all(),
        playlists=Playlist.query.filter_by(user_id=session["user_id"]).all(),
        active_playlist=None
    )


# ================= PLAYLIST =================
@app.route("/playlist/create", methods=["POST"])
def create_playlist():
    if session.get("role") != "USER":
        return redirect(url_for("login"))

    playlist = Playlist(
        playlist_name=request.form["name"],
        user_id=session["user_id"]
    )

    db.session.add(playlist)
    db.session.commit()

    return redirect(url_for("user_dashboard"))


@app.route("/playlist/add-song", methods=["POST"])
def add_song_to_playlist():
    playlist_id = request.form["playlist_id"]
    song_id = request.form["song_id"]

    exists = PlaylistSong.query.filter_by(
        playlist_id=playlist_id,
        song_id=song_id
    ).first()

    if not exists:
        db.session.add(
            PlaylistSong(
                playlist_id=playlist_id,
                song_id=song_id,
                position=0
            )
        )
        db.session.commit()

    return redirect(url_for("user_dashboard"))


@app.route("/playlist/<int:playlist_id>")
def view_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)

    if playlist.user_id != session["user_id"]:
        return "Unauthorized", 403

    songs = (
        Song.query
        .join(PlaylistSong)
        .filter(PlaylistSong.playlist_id == playlist_id)
        .all()
    )

    return render_template(
        "user_dashboard.html",
        username=session["username"],
        songs=songs,
        playlists=Playlist.query.filter_by(user_id=session["user_id"]).all(),
        active_playlist=playlist
    )


# ================= RUN =================
if __name__ == "__main__":
    app.run()
