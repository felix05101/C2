# ⚔️ Excalibur C2

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API%20Backend-brightgreen?style=flat&logo=fastapi)
![Frontend](https://img.shields.io/badge/HTML5-%F0%9F%92%BB%20Frontend-orange?style=flat&logo=html5)
![Status](https://img.shields.io/badge/status-in%20development-yellow)

> **Excalibur C2** is a lightweight and powerful Command and Control system (C2) built with FastAPI, SQLite, and a sleek HTML/JS frontend. It enables command execution on registered clients, tracks victim metadata, and supports PowerShell tasking.

---

## 🧩 Project Structure

```bash
.
├── main.py             # FastAPI app setup and launch
├── agent.py            # Victim-side client agent (PowerShell executor)
├── controllers.py      # REST API logic and endpoints
├── excalibur.db        # SQLite database file
├── index.html          # Frontend panel UI (macOS-styled)
└── /panel              # Static frontend folder served by FastAPI
```

---

## 🚀 Features

- ✅ Victim registration with system metadata
- ✅ Periodic heartbeat and status update
- ✅ Remote PowerShell command execution
- ✅ Command history & execution tracking
- ✅ Saved command management (create, edit, delete)
- ✅ Modern macOS-inspired web dashboard
- ✅ SQLite-based persistent backend
- ✅ CORS-ready, API-first architecture

---

## 🖥️ Web Interface

The frontend is written in pure HTML/CSS/JS with a modern, polished UI inspired by macOS aesthetics.

### Highlights:
- 📊 Live Victim Table with metadata and command options
- 💾 Saved Commands modal with easy CRUD
- ⚡ Quick command execution (custom or saved)
- 🌐 Auto-refreshing victim list (every 10s)
- 🔔 Toast notifications & confirmation modals

---

## ⚙️ How It Works

### 1. Victim Agent (`agent.py`)
- Collects hostname, IP, OS info
- Registers with the C2 server via `POST /api/victims/status`
- Polls for pending commands from `/api/victims/{id}/commands`
- Executes them using PowerShell
- Sends back output via `/api/victims/{id}/report`
- Marks command as executed

### 2. Backend (`main.py` + `controllers.py`)
- FastAPI with REST endpoints for:
  - Victim management
  - Command queuing & execution
  - Saved command templates
- Uses SQLite with SQLAlchemy models
- Mounted frontend at `/` using `StaticFiles`

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.10+
- `pip install fastapi uvicorn sqlalchemy pydantic`

### 1. Launch Server
```bash
python main.py
# or
uvicorn main:app --reload
```

Access the panel at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 2. Start Agent on Client
```bash
python agent.py
```

Ensure the `SERVER` address in `agent.py` points to the C2 host.

---

## 🔐 Security Disclaimer

> ⚠️ **This project is for educational and research purposes only.**
Unauthorized deployment, use, or testing of this C2 infrastructure against devices you do not own or have permission to interact with is strictly prohibited and may violate laws or ethical standards.

---

## 🧑‍💻 Developer Notes

- Frontend uses no frameworks — just vanilla HTML/CSS/JS
- You can enhance the DB using `alembic` if needed
- Agent supports only Windows PowerShell execution (can be extended)
- Modify `excalibur.db` schema via SQLAlchemy models

---

## 📌 To-Do
- [ ] Authentication system (JWT or session)
- [ ] Encrypted agent-server communication (HTTPS)
- [ ] Agent obfuscation / stealth mode
- [ ] REST API documentation (Swagger UI)

---

## 🤝 Contributions

Pull requests are welcome! If you have ideas for enhancements, feel free to open an issue.

---

## 📜 License

This project is released under the **MIT License**.

---

> Built with ❤️ by hackers, for hackers — in the spirit of knowledge.
