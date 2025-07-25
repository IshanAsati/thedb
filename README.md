# The People DB - Multi-Interface Application

A lightweight people management application built with Python. Features three different interfaces: a modern web app, a terminal user interface (TUI), and a simple command-line interface (CLI).

## Features

✨ **Core Functionality:**
- Add, view, edit, and delete contacts
- Store: name, nickname, birthday, personality notes, social media links, custom tags
- SQLite database for reliable local storage
- Export contacts to CSV format

🔍 **Search & Filter:**
- Search by name, nickname, or tags
- Filter contacts by specific tags
- View all unique tags with usage statistics

🎨 **User Interface Options:**
- Modern web interface (Flask + Bootstrap) - accessible via browser
- Modern TUI with tabbed interface (requires textual library)
- Color-coded tags for better visualization
- Simple CLI fallback interface
- Keyboard shortcuts for quick navigation

## Installation

1. **Clone or download the project files**
2. **Install dependencies:**

```powershell
pip install textual rich pandas flask wtforms flask-wtf
```

*Note: If you don't want to install these dependencies, you can use the simple CLI interface (cli.py) which only requires the built-in Python libraries.*

## Usage

### Option 1: Multi-Interface Launcher (Recommended)

```powershell
python start.py
```

Choose from:
1. **Web Interface** - Modern browser-based interface
2. **TUI Interface** - Rich terminal interface
3. **CLI Interface** - Simple command-line interface

### Option 2: Direct Interface Access

#### Web Interface (Flask + Bootstrap)

```powershell
python app.py
```

Then open your browser to: `http://localhost:5000`

**Features:**
- Responsive Bootstrap design
- Add/edit contacts with forms
- Search and filter functionality
- Tag-based filtering
- CSV export
- Social media link integration
- Mobile-friendly interface

#### TUI Interface (Textual)

```powershell
python main.py
```

**Keyboard Shortcuts:**
- `A` - Add new contact
- `S` - Focus search bar
- `E` - Export to CSV
- `R` - Refresh contacts
- `Q` - Quit application
- `?` - Show help

#### Simple CLI Interface

```powershell
python cli.py
```

This interface works without any external dependencies and provides all the same functionality through a menu-driven interface.

## File Structure

```
The People DB/
├── start.py         # Multi-interface launcher
├── app.py           # Flask web application
├── main.py          # Main TUI application (requires textual)
├── cli.py           # Simple CLI interface (no dependencies)
├── database.py      # Database operations and contact management
├── requirements.txt # Python dependencies
├── README.md        # This file
├── templates/       # HTML templates for web interface
│   ├── base.html
│   ├── index.html
│   ├── add_contact.html
│   ├── edit_contact.html
│   └── view_contact.html
├── static/          # Static files (CSS, JS, images)
└── contacts.db      # SQLite database (created automatically)
```

## Database Schema

The application uses SQLite with the following schema:

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nickname TEXT,
    birthday TEXT,
    personality_notes TEXT,
    social_media TEXT,  -- JSON string
    tags TEXT,          -- JSON string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Features in Detail

### Contact Management
- **Add Contact**: Full form with validation
- **Edit Contact**: Modify existing contact information
- **Delete Contact**: Remove contacts with confirmation
- **View Details**: Detailed contact information display

### Search & Filter
- **Text Search**: Search across names, nicknames, and tags
- **Tag Filtering**: Filter contacts by specific tags
- **Tag Statistics**: View all tags with usage counts

### Data Export
- **CSV Export**: Export all contacts to CSV format
- **Timestamped Files**: Automatic filename generation with timestamps
- **Full Data**: Includes all contact fields in export

### Color-Coded Tags
Tags are displayed with different colors for better visual organization:
- Red, Blue, Green, Yellow, Magenta, Cyan rotation
- Consistent coloring based on tag names
- Works in both TUI and CLI interfaces

## Usage Examples

### Adding a Contact
```
Name: John Doe
Nickname: Johnny
Birthday: 1990-05-15
Personality Notes: Friendly, loves hiking and photography
Social Media: {"twitter": "@johndoe", "instagram": "john.doe.photos"}
Tags: friend, photographer, outdoor
```

### Searching
- Search "photo" → finds contacts with "photographer" tag or photography notes
- Search "friend" → finds all contacts tagged as friends
- Search "John" → finds contacts with "John" in name or nickname

### Tag Management
- View all tags with usage statistics
- Filter contacts by specific tags
- Color-coded display for easy identification

## Technical Details

### Dependencies
- **flask**: Web framework (for web interface)
- **wtforms**: Form handling (for web interface)
- **flask-wtf**: Flask integration for WTForms
- **textual**: Modern TUI framework (optional, for main.py)
- **rich**: Rich text formatting (used by textual)
- **sqlite3**: Database (built-in Python library)
- **json**: Data serialization (built-in Python library)
- **pandas**: CSV export (optional, but recommended)

### Data Storage
- Local SQLite database (`contacts.db`)
- JSON serialization for complex fields (social media, tags)
- Automatic timestamp tracking for created/updated dates

### Cross-Platform
- Works on Windows, macOS, and Linux
- PowerShell-friendly commands for Windows users
- ANSI color support for enhanced terminal display

## Troubleshooting

### If textual is not available:
Use the CLI interface: `python cli.py`

### If pandas is not available:
CSV export will still work but may be limited. Install with: `pip install pandas`

### Database issues:
The SQLite database is created automatically. If corrupted, delete `contacts.db` and restart the application.

### Color display issues:
If colors don't display properly, your terminal may not support ANSI colors. The functionality will still work without colors.

## Future Enhancements

Potential improvements for future versions:
- Import from CSV/JSON
- Contact photos/avatars
- Backup and restore functionality
- Advanced search with multiple criteria
- Contact grouping and categories
- Integration with external services
- Data synchronization options

## License

This project is open source and available under the MIT License.
