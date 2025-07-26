#!/usr/bin/env python3
"""
Database repair utility for The People DB
Cleans up corrupted JSON data and ensures data integrity
"""

import sqlite3
import json
import sys
from pathlib import Path

def repair_database(db_path='contacts.db'):
    """Repair corrupted JSON data in the database."""
    print(f"🔧 Repairing database: {db_path}")
    
    # Check if database exists
    if not Path(db_path).exists():
        print(f"❌ Database file {db_path} not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all contacts
        cursor.execute('SELECT id, social_media, tags FROM contacts')
        rows = cursor.fetchall()
        
        repairs_made = 0
        
        for contact_id, social_media, tags in rows:
            needs_update = False
            new_social_media = social_media
            new_tags = tags
            
            # Check and repair social_media JSON
            if social_media:
                try:
                    parsed_social = json.loads(social_media)
                    # Ensure it's a dictionary, not a list
                    if isinstance(parsed_social, list):
                        print(f"🔧 Converting social_media list to dict for contact ID {contact_id}")
                        new_social_media = '{}'
                        needs_update = True
                    elif not isinstance(parsed_social, dict):
                        print(f"🔧 Fixing invalid social_media type for contact ID {contact_id}")
                        new_social_media = '{}'
                        needs_update = True
                except json.JSONDecodeError:
                    print(f"🔧 Repairing social_media for contact ID {contact_id}")
                    new_social_media = '{}'
                    needs_update = True
            
            # Check and repair tags JSON
            if tags:
                try:
                    parsed_tags = json.loads(tags)
                    # Ensure it's a list, not a dict
                    if isinstance(parsed_tags, dict):
                        print(f"🔧 Converting tags dict to list for contact ID {contact_id}")
                        new_tags = '[]'
                        needs_update = True
                    elif not isinstance(parsed_tags, list):
                        print(f"🔧 Fixing invalid tags type for contact ID {contact_id}")
                        new_tags = '[]'
                        needs_update = True
                except json.JSONDecodeError:
                    print(f"🔧 Repairing tags for contact ID {contact_id}")
                    # Try to extract readable tags from corrupted data
                    if isinstance(tags, str) and not tags.startswith('['):
                        # Assume it's a comma-separated string, convert to JSON array
                        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
                        new_tags = json.dumps(tag_list)
                    else:
                        new_tags = '[]'
                    needs_update = True
            
            # Update the record if repairs were needed
            if needs_update:
                cursor.execute('''
                    UPDATE contacts 
                    SET social_media = ?, tags = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (new_social_media, new_tags, contact_id))
                repairs_made += 1
        
        conn.commit()
        conn.close()
        
        if repairs_made > 0:
            print(f"✅ Database repair completed! {repairs_made} records fixed.")
        else:
            print("✅ Database is clean - no repairs needed.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error repairing database: {e}")
        return False

def main():
    """Main function to run database repair."""
    db_path = 'contacts.db'
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    
    print("=" * 50)
    print("🛠️  The People DB - Database Repair Utility")
    print("=" * 50)
    
    success = repair_database(db_path)
    
    if success:
        print("\n🎉 Database repair process completed successfully!")
        print("You can now run the application normally.")
    else:
        print("\n❌ Database repair failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
