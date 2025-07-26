#!/usr/bin/env python3
"""
The People DB - System Check Utility
Validates all components and dependencies are working correctly
"""

import sys
import sqlite3
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.7+")
        return False

def check_core_imports():
    """Check core Python libraries."""
    try:
        import sqlite3
        import json
        import datetime
        import os
        print("✅ Core libraries (sqlite3, json, datetime, os) - Available")
        return True
    except ImportError as e:
        print(f"❌ Core library missing: {e}")
        return False

def check_web_dependencies():
    """Check Flask web interface dependencies."""
    try:
        import flask
        import wtforms
        from flask_wtf import FlaskForm
        print(f"✅ Web dependencies (Flask {flask.__version__}) - Available")
        return True
    except ImportError as e:
        print(f"⚠️  Web dependencies missing: {e}")
        print("   Install with: pip install flask wtforms flask-wtf")
        return False

def check_tui_dependencies():
    """Check TUI interface dependencies."""
    try:
        import textual
        import rich
        print(f"✅ TUI dependencies (Textual {textual.__version__}) - Available")
        return True
    except ImportError as e:
        print(f"⚠️  TUI dependencies missing: {e}")
        print("   Install with: pip install textual rich")
        return False

def check_optional_dependencies():
    """Check optional dependencies."""
    try:
        import pandas
        print(f"✅ Optional: Pandas {pandas.__version__} - Available (enhanced CSV export)")
        return True
    except ImportError:
        print("⚠️  Optional: Pandas not installed (basic CSV export only)")
        print("   Install with: pip install pandas")
        return False

def check_database():
    """Check if database can be created and accessed."""
    try:
        from database import ContactDatabase
        db = ContactDatabase()
        
        # Test database connection
        test_db = sqlite3.connect(':memory:')
        test_db.execute('''
            CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)
        ''')
        test_db.close()
        
        print("✅ Database functionality - Working")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_file_structure():
    """Check if all required files exist."""
    required_files = [
        'start.py', 'app.py', 'main.py', 'cli.py', 'database.py',
        'requirements.txt', 'README.md', 'LICENSE'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ File structure - Complete")
        return True

def check_interfaces():
    """Test if interfaces can be imported."""
    interfaces = []
    
    # CLI (always available)
    try:
        from cli import SimpleContactCLI
        interfaces.append("CLI")
    except ImportError:
        pass
    
    # Web interface
    try:
        from app import app
        interfaces.append("Web")
    except ImportError:
        pass
    
    # TUI interface
    try:
        from main import ContactManagerApp
        interfaces.append("TUI")
    except ImportError:
        pass
    
    if interfaces:
        print(f"✅ Available interfaces: {', '.join(interfaces)}")
        return True
    else:
        print("❌ No interfaces available")
        return False

def main():
    """Run all system checks."""
    print("=" * 60)
    print("🔍 The People DB - System Check")
    print("=" * 60)
    print()
    
    checks = [
        check_python_version,
        check_core_imports,
        check_file_structure,
        check_database,
        check_interfaces,
        check_web_dependencies,
        check_tui_dependencies,
        check_optional_dependencies,
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All systems operational!")
        print("   You can run: python start.py")
    elif passed >= 5:
        print("⚠️  System partially operational")
        print("   Some features may not be available")
    else:
        print("❌ System check failed")
        print("   Please install missing dependencies")
    
    print("=" * 60)
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
