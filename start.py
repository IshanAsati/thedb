#!/usr/bin/env python3
"""
Startup script for Contact Manager
Allows you to choose between different interfaces
"""

import sys
import os
import subprocess

def show_menu():
    print("\n" + "="*60)
    print("🚀 CONTACT MANAGER - INTERFACE SELECTOR")
    print("="*60)
    print("Choose how you'd like to run the Contact Manager:")
    print()
    print("1. 🌐 Web Interface (Flask) - Modern web app with Bootstrap")
    print("2. 🖥️  TUI Interface (Textual) - Modern terminal interface")
    print("3. 📝 CLI Interface (Simple) - Basic command-line interface")
    print("4. ℹ️  Show Information")
    print("5. ❌ Exit")
    print("="*60)

def run_web_interface():
    print("\n🌐 Starting Flask Web Interface...")
    print("📍 Web interface will be available at: http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server")
    print("-" * 40)
    
    try:
        # Import and run Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Error: Flask dependencies not installed. {e}")
        print("📦 Install with: pip install flask wtforms flask-wtf")
    except Exception as e:
        print(f"❌ Error starting web server: {e}")

def run_tui_interface():
    print("\n🖥️ Starting TUI Interface...")
    print("💡 Use keyboard shortcuts: A=Add, S=Search, E=Export, Q=Quit")
    print("-" * 40)
    
    try:
        from main import main
        main()
    except ImportError as e:
        print(f"❌ Error: Textual not installed. {e}")
        print("📦 Install with: pip install textual rich")
        print("🔄 Falling back to CLI interface...")
        run_cli_interface()
    except Exception as e:
        print(f"❌ Error starting TUI: {e}")

def run_cli_interface():
    print("\n📝 Starting CLI Interface...")
    print("💡 Simple menu-driven interface that works without dependencies")
    print("-" * 40)
    
    try:
        from cli import SimpleContactCLI
        cli = SimpleContactCLI()
        cli.run()
    except Exception as e:
        print(f"❌ Error starting CLI: {e}")

def show_info():
    print("\n" + "="*60)
    print("ℹ️  CONTACT MANAGER INFORMATION")
    print("="*60)
    print("📋 Features:")
    print("   • Add, view, edit, and delete contacts")
    print("   • Store: name, nickname, birthday, notes, social media, tags")
    print("   • Search and filter by name or tags")
    print("   • Export to CSV format")
    print("   • SQLite database for reliable storage")
    print()
    print("🖥️  Interface Options:")
    print("   • Web Interface: Modern web app accessible via browser")
    print("   • TUI Interface: Rich terminal interface with mouse support")
    print("   • CLI Interface: Simple command-line menu system")
    print()
    print("📁 Files:")
    print("   • app.py - Flask web application")
    print("   • main.py - Textual TUI application")
    print("   • cli.py - Simple CLI application")
    print("   • database.py - SQLite database operations")
    print("   • contacts.db - SQLite database file (auto-created)")
    print()
    print("📦 Dependencies:")
    print("   • Web: flask, wtforms, flask-wtf")
    print("   • TUI: textual, rich")
    print("   • CLI: No extra dependencies (uses built-in libraries)")
    print("   • All: sqlite3, pandas (for CSV export)")
    print("="*60)

def main():
    """Main menu loop"""
    while True:
        try:
            show_menu()
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                run_web_interface()
            elif choice == '2':
                run_tui_interface()
            elif choice == '3':
                run_cli_interface()
            elif choice == '4':
                show_info()
                input("\nPress Enter to continue...")
            elif choice == '5':
                print("\n👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
