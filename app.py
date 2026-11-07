
from flask import Flask, render_template, request, redirect, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "novel-python-engine"

DATABASE = Path(__file__).with_name("database.db")


def buat_database():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pesanan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                email TEXT NOT NULL,
                whatsapp TEXT,
                jenis_layanan TEXT NOT NULL,
                judul_novel TEXT,
                detail_pesanan TEXT
            )
        """)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pesan", methods=["POST"])
def pesan():
    nama = request.form.get("nama", "").strip()
    email = request.form.get("email", "").strip()
    whatsapp = request.form.get("whatsapp", "").strip()
    jenis = request.form.get("jenis_layanan", "").strip()
    judul = request.form.get("judul_novel", "").strip()
    detail = request.form.get("detail_pesanan", "").strip()

    if not nama or not email or not jenis:
        flash("Mohon lengkapi semua data wajib.", "error")
        return redirect("/#kontak")

    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("""
                INSERT INTO pesanan
                (nama, email, whatsapp, jenis_layanan,
                 judul_novel, detail_pesanan)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nama, email, whatsapp, jenis, judul, detail))

        flash("Pesanan berhasil dikirim!", "success")

    except sqlite3.Error as error:
        print("Database error:", error)
        flash("Pesanan gagal dikirim. Silakan coba lagi.", "error")

    return redirect("/#kontak")


if __name__ == "__main__":
    buat_database()
    app.run(debug=True)


