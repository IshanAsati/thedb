# Quick Setup Guide

## After cloning this repository:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Multi-interface launcher (recommended)
python start.py

# Or run specific interfaces directly:
python app.py      # Web interface (http://localhost:5000)
python main.py     # TUI interface
python cli.py      # CLI interface
```

### 3. Windows Users
Double-click `run.bat` for easy startup.

### 4. First Time Setup
- The SQLite database (`contacts.db`) will be created automatically
- No additional configuration required
- All interfaces share the same database

### 5. Features
- ✅ Add, edit, delete contacts
- ✅ Search and filter by name/tags  
- ✅ Export to CSV
- ✅ Color-coded tags
- ✅ Social media integration
- ✅ Relationship preferences (Friend/Romantic status)
- ✅ Mobile-responsive web interface

### 6. Dependencies
- **Required for Web**: Flask, WTForms, Flask-WTF
- **Required for TUI**: Textual, Rich
- **Optional**: Pandas (for enhanced CSV export)
- **CLI only**: No extra dependencies needed

Enjoy your Contact Manager! 🎉
