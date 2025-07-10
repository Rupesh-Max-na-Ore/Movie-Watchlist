# 🎬 Movie Watchlist CLI App

A simple command-line interface (CLI) application for managing your movie watchlist using Python and SQLite.

---

## 📁 Project Structure
```bash
Movie-Watchlist/
├── app.py # Entry point of the application
├── requirements.txt # Python dependencies (optional for this app)
└── README.md # Project documentation
```

---

## 🧰 Prerequisites

- Python **3.8+**
- Terminal or command-line access

> ⚠️ `sqlite3` is used for storage and comes with Python's standard library—no installation needed.

---

## 🚀 Setup Instructions

Open a terminal and run the following commands:

```bash
# Step 1: Create a virtual environment
python3 -m venv .venv

# Step 2: Activate the virtual environment
source .venv/bin/activate          # On macOS/Linux
# .\.venv\Scripts\activate         # On Windows (PowerShell)

# Step 3: Install dependencies (optional in this app)
pip install -r requirements.txt

# Step 4: Run the app
python main.py
```
-----
## Cleanup
To remove the virtual environment (optional):
```bash
deactivate
rm -r .venv   # On Unix/macOS
# rmdir /S .venv  # On Windows (CMD)
```
---
## Features
1. Add movies to your watchlist
2. Mark movies as watched
3. Delete movies
4. View watchlist

---
## Notes
- No internet connection required—everything is local
- Tested on Python 3.12.7 (Fedora Linux)

----
## License
This project is for educational and personal use. Feel free to modify or extend it.