# The People DB - Multi-Interface Contact Management System

A comprehensive, lightweight contact management application built with Python. Features three different interfaces: a modern web app, a terminal user interface (TUI), and a simple command-line interface (CLI).

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## 🌟 Features

### Core Functionality
- **Complete Contact Management**: Add, view, edit, and delete contacts
- **Rich Contact Data**: Store name, nickname, birthday, address, personality notes, social media links, and custom tags
- **Relationship Preferences**: Track whether you like someone as a friend and/or romantically
- **Reliable Storage**: SQLite database for secure local data storage
- **Data Export**: Export all contacts to CSV format with timestamps

### Search & Organization
- **Powerful Search**: Search across names, nicknames, tags, and notes
- **Tag-Based Filtering**: Organize and filter contacts by custom tags
- **Tag Statistics**: View all unique tags with usage counts
- **Color-Coded Tags**: Visual organization with consistent tag coloring

### Multiple Interfaces
- **🌐 Web Interface**: Modern, responsive web app with Bootstrap UI
- **🖥️ TUI Interface**: Rich terminal interface with keyboard shortcuts and mouse support  
- **📝 CLI Interface**: Simple command-line interface requiring no external dependencies
- **🚀 Unified Launcher**: Easy interface selection via start.py

## 📦 Quick Start

### Prerequisites
- Python 3.7 or higher
- Git (optional, for cloning)

### Installation

1. **Clone or download the project**
   ```bash
   git clone https://github.com/IshanAsati/thedb.git
   cd thedb
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python start.py
   ```

### Windows Users
Double-click `run.bat` for easy startup.

## 🚀 Usage

### Multi-Interface Launcher (Recommended)

```bash
python start.py
```

This presents a menu to choose your preferred interface:

1. **Web Interface** - Browser-based with responsive design (http://localhost:5000)
2. **TUI Interface** - Rich terminal experience with keyboard shortcuts
3. **CLI Interface** - Simple menu-driven interface
4. **Database Utilities** - Migration and repair tools
5. **Exit**

### Direct Interface Access

#### 🌐 Web Interface
```bash
python app.py
```
Then open your browser to: `http://localhost:5000`

**Features:**
- Responsive Bootstrap 5 design
- Form-based contact management with address field
- Real-time search and filtering
- Tag-based organization with color coding
- Social media link integration
- One-click CSV export
- Mobile-friendly interface

#### 🖥️ TUI Interface  
```bash
python main.py
```

**Keyboard Shortcuts:**
- `A` - Add new contact
- `S` - Focus search bar
- `E` - Export to CSV
- `R` - Refresh contacts
- `Q` - Quit application  
- `?` - Show help
- `Enter` - View contact details
- `Tab` - Navigate between tabs

#### 📝 CLI Interface
```bash
python cli.py
```

**Features:**
- No external dependencies required
- Menu-driven navigation
- Color-coded output with relationship status
- Full CRUD operations including address management
- Built-in export functionality

## 🗂️ Project Structure

```
The People DB/
├── start.py              # Multi-interface launcher
├── app.py               # Flask web application
├── main.py              # Textual TUI application
├── cli.py               # Simple CLI interface
├── database.py          # SQLite database operations
├── system_check.py      # System validation utility
├── repair_db.py         # Database repair utility
├── migrate_db.py        # Database migration tool
├── requirements.txt     # Python dependencies
├── README.md           # This documentation
├── SETUP.md            # Quick setup guide
├── CHANGELOG.md        # Version history
├── PROJECT_STRUCTURE.md # Detailed project structure
├── LICENSE             # MIT license
├── run.bat             # Windows batch launcher
├── templates/          # HTML templates for web interface
│   ├── base.html       # Base template with Bootstrap
│   ├── index.html      # Contact listing page
│   ├── add_contact.html    # Add contact form
│   ├── edit_contact.html   # Edit contact form
│   └── view_contact.html   # Contact detail view
├── static/             # Static web assets (auto-created)
└── contacts.db         # SQLite database (auto-created)
```

## 🗄️ Database Schema

The application uses SQLite with the following optimized schema:

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nickname TEXT,
    birthday TEXT,
    address TEXT,                    -- NEW: Full address support
    personality_notes TEXT,
    social_media TEXT,              -- JSON: {"twitter": "@handle", "instagram": "user"}
    tags TEXT,                      -- JSON: ["friend", "work", "family"]
    like_as_friend BOOLEAN DEFAULT 0,
    like_romantically BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Recent Updates
- ✅ **Address Field**: Full address support across all interfaces
- ✅ **Enhanced Error Handling**: Robust JSON parsing with fallbacks
- ✅ **Database Repair**: Automatic corruption detection and repair
- ✅ **Improved Documentation**: Comprehensive guides and structure docs
- `Tab` - Navigate between tabs

#### 📝 CLI Interface
```bash
python cli.py
```

**Features:**
- No external dependencies required
- Menu-driven navigation
- Color-coded output
- Relationship status indicators
- Full CRUD operations

## 🗂️ Project Structure

```
The People DB/
├── start.py              # Multi-interface launcher
├── app.py               # Flask web application
├── main.py              # Textual TUI application
├── cli.py               # Simple CLI interface
├── database.py          # SQLite database operations
├── repair_db.py         # Database repair utility
├── migrate_db.py        # Database migration tool
├── requirements.txt     # Python dependencies
├── README.md           # This documentation
├── SETUP.md            # Quick setup guide
├── LICENSE             # MIT license
├── run.bat             # Windows batch launcher
├── templates/          # HTML templates for web interface
│   ├── base.html       # Base template with Bootstrap
│   ├── index.html      # Contact listing page
│   ├── add_contact.html    # Add contact form
│   ├── edit_contact.html   # Edit contact form
│   └── view_contact.html   # Contact detail view
├── static/             # Static web assets (auto-created)
└── contacts.db         # SQLite database (auto-created)
```

## 🗄️ Database Schema

The application uses SQLite with the following optimized schema:

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nickname TEXT,
    birthday TEXT,
    address TEXT,
    personality_notes TEXT,
    social_media TEXT,      -- JSON: {"twitter": "@handle", "instagram": "user"}
    tags TEXT,              -- JSON: ["friend", "work", "family"]
    like_as_friend BOOLEAN DEFAULT 0,
    like_romantically BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📊 Data Examples

### Adding a Contact
```
Name: John Doe
Nickname: Johnny
Birthday: 1990-05-15
Address: 123 Main St
         New York, NY 10001
         USA
Personality Notes: Friendly photographer who loves hiking
Social Media: {"twitter": "@johndoe", "instagram": "john.doe.photos"}
Tags: friend, photographer, outdoor, travel
Relationship: ✓ Friend  ✗ Romantic
```

### Search Examples
- Search **"photo"** → finds contacts with "photographer" tag or photography notes
- Search **"friend"** → finds all contacts tagged as friends
- Search **"John"** → finds contacts with "John" in name or nickname
- Filter by **"work"** tag → shows only work-related contacts

## 🔧 Advanced Features

### Database Utilities

#### Automatic Migration
The database schema is automatically updated when you run the application. If you encounter column errors, the system will:
- Detect missing columns
- Add new fields safely
- Preserve all existing data
- Show migration progress

#### Manual Repair
If you encounter data corruption:
```bash
python repair_db.py
```

This utility will:
- Fix corrupted JSON data
- Standardize data types
- Clean up inconsistent entries
- Preserve all recoverable information

#### Manual Migration
For troubleshooting database issues:
```bash
python migrate_db.py
```

### Error Recovery
The application includes robust error handling:
- **JSON Parse Errors**: Automatically fixed with safe defaults
- **Missing Columns**: Added automatically with backward compatibility
- **Database Corruption**: Repairable with included utilities
- **Import Errors**: Graceful fallbacks for missing dependencies

## 🎨 Customization

### Tag Colors
Tags are automatically color-coded using a consistent algorithm:
- Same tag → same color across all interfaces
- Color rotation: Red, Blue, Green, Yellow, Magenta, Cyan
- Web interface uses Bootstrap color classes
- Terminal interfaces use ANSI colors

### Web Interface Themes
The web interface uses Bootstrap 5 and can be customized by:
- Modifying `templates/base.html` for layout changes
- Adding custom CSS in the `static/` directory
- Changing the Bootstrap theme CDN link

## 🔍 Dependencies

### Core Dependencies (All Interfaces)
- **sqlite3** - Database (built-in with Python)
- **json** - Data serialization (built-in)
- **datetime** - Timestamp handling (built-in)

### Web Interface
- **flask** - Web framework
- **wtforms** - Form handling and validation
- **flask-wtf** - Flask integration for WTForms

### TUI Interface
- **textual** - Modern terminal UI framework
- **rich** - Rich text formatting and colors

### Optional Enhancements
- **pandas** - Enhanced CSV export (optional)

### Installation Commands
```bash
# All features
pip install flask wtforms flask-wtf textual rich pandas

# Web only
pip install flask wtforms flask-wtf

# TUI only  
pip install textual rich

# CLI only (no extra dependencies needed)
```

## 🚨 Troubleshooting

### Common Issues

#### "Unable to open database file"
```bash
# Check file permissions
ls -la contacts.db

# Repair if corrupted
python repair_db.py

# If all else fails, delete and restart
rm contacts.db
python start.py
```

#### "No such column: like_as_friend"
```bash
# Run migration (automatic)
python start.py

# Or manually
python migrate_db.py
```

#### "Textual not installed"
```bash
# Install textual
pip install textual rich

# Or use CLI fallback
python cli.py
```

#### JSON Decode Errors
```bash
# Run database repair
python repair_db.py
```

#### Import Errors
- **Flask issues**: `pip install flask wtforms flask-wtf`
- **Textual issues**: `pip install textual rich` 
- **Pandas issues**: `pip install pandas` (optional)

### Performance Tips
- **Large datasets**: Use search and filtering instead of browsing all contacts
- **Slow web interface**: Check if debug mode is enabled (only for development)
- **Memory usage**: The TUI interface uses more memory than CLI
- **Database size**: Export and reimport periodically to optimize database

## 🔮 Future Enhancements

### Planned Features
- **Contact Import**: Import from CSV, JSON, and vCard formats
- **Photo Support**: Contact avatars and photo attachments
- **Backup System**: Automated backups with versioning
- **Advanced Search**: Multi-field search with filters
- **Contact Groups**: Organize contacts into custom groups
- **Data Sync**: Cloud synchronization options
- **Mobile App**: React Native companion app
- **API Expansion**: REST API for third-party integrations

### Contributing
This project welcomes contributions! Areas for improvement:
- Additional database backends (PostgreSQL, MySQL)
- Enhanced search algorithms
- More export formats
- UI/UX improvements
- Performance optimizations
- Test coverage
- Documentation improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask** - Lightweight web framework
- **Textual** - Modern terminal UI library  
- **Bootstrap** - Responsive web design framework
- **SQLite** - Reliable embedded database
- **Rich** - Beautiful terminal formatting

## 📞 Support

For issues, questions, or contributions:
- **GitHub Issues**: [Report bugs or request features](https://github.com/IshanAsati/thedb/issues)
- **Documentation**: Check this README and SETUP.md
- **Database Issues**: Use the built-in repair utilities

---

**Made with ❤️ for better contact management**
