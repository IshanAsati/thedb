# Project Structure

```
The People DB/
├── 📚 Documentation
│   ├── README.md              # Main documentation
│   ├── SETUP.md              # Quick setup guide
│   ├── CHANGELOG.md          # Version history
│   └── LICENSE               # MIT license
│
├── 🖥️ Application Files
│   ├── start.py              # Multi-interface launcher
│   ├── app.py               # Flask web application
│   ├── main.py              # Textual TUI application
│   ├── cli.py               # Simple CLI interface
│   └── database.py          # SQLite database operations
│
├── 🛠️ Utilities
│   ├── migrate_db.py        # Database migration tool
│   ├── repair_db.py         # Database repair utility
│   └── run.bat              # Windows batch launcher
│
├── 🎨 Web Interface
│   ├── templates/           # HTML templates
│   │   ├── base.html       # Base template with Bootstrap
│   │   ├── index.html      # Contact listing page
│   │   ├── add_contact.html    # Add contact form
│   │   ├── edit_contact.html   # Edit contact form
│   │   └── view_contact.html   # Contact detail view
│   └── static/             # Static web assets (auto-created)
│
├── ⚙️ Configuration
│   ├── requirements.txt    # Python dependencies
│   ├── .gitignore         # Git ignore rules
│   └── __pycache__/       # Python bytecode cache
│
└── 🗄️ Data (auto-created)
    └── contacts.db        # SQLite database file
```

## File Descriptions

### Core Application Files
- **start.py**: Main launcher with interface selection menu
- **app.py**: Flask web application with Bootstrap UI
- **main.py**: Textual-based terminal user interface
- **cli.py**: Simple command-line interface (no dependencies)
- **database.py**: SQLite database operations and contact management

### Utility Scripts
- **migrate_db.py**: Handles database schema migrations
- **repair_db.py**: Repairs corrupted JSON data in database
- **run.bat**: Windows batch file for easy startup

### Web Interface
- **templates/**: Jinja2 HTML templates with Bootstrap 5
- **static/**: CSS, JavaScript, and image assets (created automatically)

### Configuration
- **requirements.txt**: Python package dependencies
- **.gitignore**: Git version control ignore rules

### Data Storage
- **contacts.db**: SQLite database (created automatically on first run)
- **CSV exports**: Generated in root directory with timestamps

## Interface Dependencies

| Interface | Required Dependencies | Optional |
|-----------|----------------------|----------|
| CLI       | None (built-in only) | -        |
| Web       | flask, wtforms, flask-wtf | -  |
| TUI       | textual, rich        | -        |
| All       | -                    | pandas (CSV export) |

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run launcher: `python start.py`
3. Choose your preferred interface
