# Development Guide

This guide is for developers who want to contribute to The People DB or understand its architecture.

## 🏗️ Architecture Overview

The People DB follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Interfaces    │    │    Database     │    │    Utilities    │
│                 │    │                 │    │                 │
│ • Web (Flask)   │───▶│ • ContactDB     │◀───│ • Migration     │
│ • TUI (Textual) │    │ • SQLite        │    │ • Repair        │
│ • CLI (Native)  │    │ • JSON Storage  │    │ • System Check  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Code Organization

### Core Components

#### `database.py` - Data Layer
- **ContactDatabase class**: Main database interface
- **Schema management**: Automatic migration and repair
- **CRUD operations**: Create, Read, Update, Delete contacts
- **Search functionality**: Full-text search across fields
- **Export capabilities**: CSV generation with timestamps

#### `app.py` - Web Interface
- **Flask application**: RESTful web interface
- **Form handling**: WTForms integration with validation
- **Template rendering**: Jinja2 templates with Bootstrap
- **API endpoints**: JSON responses for AJAX requests
- **File serving**: Static assets and CSV downloads

#### `main.py` - TUI Interface
- **Textual application**: Rich terminal interface
- **Event-driven**: Keyboard and mouse interactions
- **Component-based**: Reusable UI widgets
- **Reactive updates**: Real-time data synchronization
- **Theming support**: Consistent color schemes

#### `cli.py` - CLI Interface
- **Pure Python**: No external dependencies
- **Menu-driven**: Simple navigation system
- **Color output**: ANSI color codes for readability
- **Error handling**: Graceful degradation
- **Cross-platform**: Works on Windows, Linux, macOS

### Supporting Files

#### `start.py` - Application Launcher
- **Interface selection**: User-friendly menu
- **Dependency checking**: Validates requirements
- **Error reporting**: Clear setup instructions
- **Process management**: Clean startup/shutdown

#### Utility Scripts
- **`migrate_db.py`**: Database schema migration
- **`repair_db.py`**: Data corruption repair
- **`system_check.py`**: Environment validation

## 🛠️ Development Setup

### Prerequisites
```bash
# Install Python 3.7+
python --version

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Optional: Install development tools
pip install pytest black flake8 mypy
```

### Running Tests
```bash
# System validation
python system_check.py

# Manual testing
python start.py

# Database integrity
python repair_db.py
```

### Code Style
```bash
# Format code
black *.py

# Lint code
flake8 *.py

# Type checking
mypy *.py
```

## 🔧 Adding New Features

### Adding a New Contact Field

1. **Update Database Schema** (`database.py`):
```python
# In init_database()
if 'new_field' not in columns:
    cursor.execute('ALTER TABLE contacts ADD COLUMN new_field TEXT DEFAULT ""')
```

2. **Update Contact Methods**:
```python
# In add_contact() and update_contact()
def add_contact(self, name: str, new_field: str = "", ...):
    # Add to INSERT statement
```

3. **Update All Interfaces**:
   - **Web**: Add field to `ContactForm` in `app.py`
   - **TUI**: Add input widget to `ContactFormScreen` in `main.py`
   - **CLI**: Add prompt to `add_contact()` in `cli.py`

4. **Update Templates** (Web interface):
```html
<!-- In add_contact.html and edit_contact.html -->
<div class="mb-3">
    {{ form.new_field.label(class="form-label") }}
    {{ form.new_field() }}
</div>
```

### Adding a New Interface

1. Create new interface file (e.g., `api.py` for REST API)
2. Import `ContactDatabase` class
3. Implement interface-specific logic
4. Update `start.py` to include new option
5. Add to documentation and tests

### Database Migration Pattern

```python
def migrate_to_version_x():
    """Migration for version X changes."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check current schema
    cursor.execute("PRAGMA table_info(contacts)")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Apply changes conditionally
    if 'new_field' not in columns:
        cursor.execute('ALTER TABLE contacts ADD COLUMN new_field TEXT')
        print("✅ Added new_field column")
    
    conn.commit()
    conn.close()
```

## 🧪 Testing Guidelines

### Manual Testing Checklist
- [ ] All interfaces launch successfully
- [ ] CRUD operations work in each interface
- [ ] Search functionality returns correct results
- [ ] Database migrations handle existing data
- [ ] CSV export generates valid files
- [ ] Error handling displays helpful messages

### Automated Testing (Future)
```python
# Example test structure
def test_add_contact():
    db = ContactDatabase(':memory:')
    contact_id = db.add_contact("Test User", "test@email.com")
    assert contact_id is not None
    
    contact = db.get_contact_by_id(contact_id)
    assert contact['name'] == "Test User"
```

## 🐛 Debugging Tips

### Common Issues
1. **Import Errors**: Check virtual environment activation
2. **Database Locked**: Ensure no other instances are running
3. **Template Errors**: Verify template syntax and context variables
4. **JSON Decode Errors**: Run `repair_db.py` to fix corrupted data

### Debugging Tools
```python
# Add debugging to any interface
import logging
logging.basicConfig(level=logging.DEBUG)

# Database debugging
db = ContactDatabase()
contacts = db.get_all_contacts()
print(f"Found {len(contacts)} contacts")
```

## 📋 Contribution Workflow

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-feature`
3. **Make changes** following code style
4. **Test thoroughly** with all interfaces
5. **Update documentation** as needed
6. **Submit pull request** with clear description

## 🚀 Release Process

1. Update version in `CHANGELOG.md`
2. Test all interfaces thoroughly
3. Update documentation
4. Run system checks: `python system_check.py`
5. Tag release: `git tag v2.1.0`
6. Push to GitHub: `git push origin main --tags`

## 📚 Architecture Decisions

### Why SQLite?
- **Simplicity**: No server setup required
- **Portability**: Single file database  
- **Performance**: Fast for small to medium datasets
- **Reliability**: ACID compliance and data integrity

### Why Multiple Interfaces?
- **Accessibility**: Different user preferences
- **Flexibility**: Various deployment scenarios
- **Learning**: Demonstrates different UI paradigms
- **Fallback**: CLI works without dependencies

### Why Flask for Web?
- **Lightweight**: Minimal overhead
- **Flexible**: Easy to customize and extend
- **Popular**: Large community and ecosystem
- **Templates**: Jinja2 for clean HTML generation

## 🔮 Future Enhancements

### Planned Features
- [ ] REST API with authentication
- [ ] Import from vCard/CSV formats
- [ ] Photo/avatar support
- [ ] Contact groups and categories
- [ ] Advanced search with filters
- [ ] Data synchronization options
- [ ] Mobile-responsive improvements
- [ ] Automated testing suite

### Technical Debt
- [ ] Add comprehensive test coverage
- [ ] Implement proper logging system
- [ ] Add configuration file support
- [ ] Optimize database queries
- [ ] Add API documentation
- [ ] Improve error messages

## 📞 Support

For development questions:
1. Check this guide and documentation
2. Review existing code patterns
3. Test with `system_check.py`
4. Create GitHub issue for bugs
5. Submit pull request for improvements
