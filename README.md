# Libs-Management-Sys (Python + CustomTkinter + MySQL)

A lightweight desktop app to **add, search, view, edit, and delete** books using a clean **CustomTkinter** UI with a **MySQL** backend. Includes live **type-ahead search**, modal detail views, inline editing, and a “show all books” list.

---

## ✨ Features
- Add new books (Title, Author, Genre, Year)
- Search with live suggestions (by Title)
- View full details in a modal window
- Edit / update book info
- Delete book with confirmation
- Show all books in a scrollable list
- Simple, responsive CustomTkinter UI

---

## 🧱 Tech Stack
- **Python 3.9+**
- **GUI**: `customtkinter`
- **DB**: `mysql-connector-python` (MySQL)
- **Tk widgets**: `tkinter` (Listbox, messagebox)

---

## 🗂️ Project Structure
```

.
├─ lib-management-sys.py         
└─ README.md

````

---

## 🗄️ Database Setup (run once)
Create database and table in MySQL:

```sql
CREATE DATABASE IF NOT EXISTS library CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE library;

CREATE TABLE IF NOT EXISTS librarySet (
  id     INT AUTO_INCREMENT PRIMARY KEY,
  title  VARCHAR(200) NOT NULL,
  author VARCHAR(200) NOT NULL,
  genre  VARCHAR(100) NOT NULL,
  year   VARCHAR(10)  NOT NULL
);

CREATE INDEX idx_title ON librarySet (title);
````

> The app expects MySQL at `localhost` with user `root` and password `OIS@12345`.
> Update credentials in code (`conc.connect(...)`) if yours differ.

---

## 📦 Installation

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install customtkinter mysql-connector-python
```

> `tkinter` ships with most Python distributions. If missing on Linux: `sudo apt install python3-tk`.

---

## ▶️ Run

```bash
python app.py
```

The main window opens with fields to **Title / Author / Genre / Year**, plus buttons:

* **Add Book** (inserts a row)
* **Search Book** (opens live search modal)
* **Show All Books** (list of titles)

---

## 🧭 Usage Guide

* **Add Book**: Fill all fields → *Add Book*. Success message confirms insert.
* **Search Book**: Type at least 2 chars → select a title to open **Book Details**.

  * **Edit Book**: Opens an editable form; *Save Changes* to persist.
  * **Delete Book**: Confirms, then removes the record.
* **Show All Books**: Displays every title in a scrollable list.

---

## 🔒 Notes & Best Practices

* **Credentials** are hardcoded for demo (`root` / `OIS@12345`). Use env vars or a config file in production.
* **Input validation** is minimal; extend as needed (e.g., numeric year).
* **Case-insensitive search**: Current query uses `LIKE` (DB collation drives sensitivity).

---

## 🛠️ Troubleshooting

* **Cannot connect to DB**: Verify MySQL is running and credentials/DB/table names match.
* **Unicode issues**: Ensure DB is `utf8mb4`.
* **Tk not found**: Install `python3-tk` (Linux) or ensure Python with Tk support.

---
