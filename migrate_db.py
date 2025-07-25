#!/usr/bin/env python3
"""
Database Migration Script for The People DB
This script adds the new relationship preference columns to existing databases.
Run this if you get "no such column" errors after updating the application.
"""

import sqlite3
import os

def migrate_database(db_path="contacts.db"):
    """Migrate existing database to include relationship preference columns."""
    
    if not os.path.exists(db_path):
        print(f"❌ Database file '{db_path}' not found.")
        print("   The database will be created automatically when you add your first contact.")
        return
    
    print(f"🔄 Migrating database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current table structure
        cursor.execute("PRAGMA table_info(contacts)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"📋 Current columns: {', '.join(columns)}")
        
        changes_made = False
        
        # Add like_as_friend column if it doesn't exist
        if 'like_as_friend' not in columns:
            cursor.execute('ALTER TABLE contacts ADD COLUMN like_as_friend BOOLEAN DEFAULT 0')
            print("✅ Added 'like_as_friend' column")
            changes_made = True
        else:
            print("✓ Column 'like_as_friend' already exists")
        
        # Add like_romantically column if it doesn't exist
        if 'like_romantically' not in columns:
            cursor.execute('ALTER TABLE contacts ADD COLUMN like_romantically BOOLEAN DEFAULT 0')
            print("✅ Added 'like_romantically' column")
            changes_made = True
        else:
            print("✓ Column 'like_romantically' already exists")
        
        if changes_made:
            conn.commit()
            print("💾 Database migration completed successfully!")
            print("🎉 You can now use the relationship preference features.")
        else:
            print("✅ Database is already up to date!")
        
        # Show updated table structure
        cursor.execute("PRAGMA table_info(contacts)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"📋 Updated columns: {', '.join(columns)}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        print("   Please check your database file and try again.")

def main():
    print("🗄️ The People DB - Database Migration Tool")
    print("=" * 50)
    print()
    
    # Check for custom database path
    db_path = "contacts.db"
    if os.path.exists("contacts.db"):
        migrate_database(db_path)
    else:
        print("❌ No existing database found.")
        print("   The database will be created automatically when you first run the application.")
    
    print()
    print("💡 Tips:")
    print("   • This migration is automatically performed when you start the application")
    print("   • You only need to run this manually if you encounter column errors")
    print("   • All existing contact data will be preserved")
    print()

if __name__ == "__main__":
    main()
