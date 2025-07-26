#!/usr/bin/env python3
"""
Database module for The People DB
Handles all SQLite database operations for contact management
"""

import sqlite3
import json
import csv
from datetime import datetime
from typing import List, Dict, Optional

# Try to import pandas for enhanced CSV export, fall back to basic CSV if not available
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

class ContactDatabase:
    def __init__(self, db_path: str = "contacts.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with the contacts table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create the main contacts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                nickname TEXT,
                birthday TEXT,
                address TEXT,
                personality_notes TEXT,
                social_media TEXT,
                tags TEXT,
                like_as_friend BOOLEAN DEFAULT 0,
                like_romantically BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check if we need to add the new columns for existing databases
        cursor.execute("PRAGMA table_info(contacts)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add address column if it doesn't exist
        if 'address' not in columns:
            cursor.execute('ALTER TABLE contacts ADD COLUMN address TEXT DEFAULT ""')
            print("✅ Added 'address' column to existing database")
        
        # Add like_as_friend column if it doesn't exist
        if 'like_as_friend' not in columns:
            cursor.execute('ALTER TABLE contacts ADD COLUMN like_as_friend BOOLEAN DEFAULT 0')
            print("✅ Added 'like_as_friend' column to existing database")
        
        # Add like_romantically column if it doesn't exist
        if 'like_romantically' not in columns:
            cursor.execute('ALTER TABLE contacts ADD COLUMN like_romantically BOOLEAN DEFAULT 0')
            print("✅ Added 'like_romantically' column to existing database")
        
        conn.commit()
        conn.close()
    
    def add_contact(self, name: str, nickname: str = "", birthday: str = "", 
                   address: str = "", personality_notes: str = "", social_media: dict = None, 
                   tags: List[str] = None, like_as_friend: bool = False,
                   like_romantically: bool = False) -> int:
        """Add a new contact to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        social_media_json = json.dumps(social_media or {})
        tags_json = json.dumps(tags or [])
        
        cursor.execute('''
            INSERT INTO contacts (name, nickname, birthday, address, personality_notes, social_media, tags, like_as_friend, like_romantically)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, nickname, birthday, address, personality_notes, social_media_json, tags_json, like_as_friend, like_romantically))
        
        contact_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return contact_id
    
    def get_all_contacts(self) -> List[Dict]:
        """Retrieve all contacts from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM contacts ORDER BY name')
        rows = cursor.fetchall()
        
        contacts = []
        for row in rows:
            # Safe JSON parsing with error handling
            try:
                social_media = json.loads(row[6]) if len(row) > 6 and row[6] else {}
            except (json.JSONDecodeError, TypeError):
                social_media = {}
            
            try:
                tags = json.loads(row[7]) if len(row) > 7 and row[7] else []
            except (json.JSONDecodeError, TypeError):
                tags = []
            
            contact = {
                'id': row[0],
                'name': row[1],
                'nickname': row[2],
                'birthday': row[3],
                'address': row[4] if len(row) > 4 else '',
                'personality_notes': row[5] if len(row) > 5 else '',
                'social_media': social_media,
                'tags': tags,
                'like_as_friend': bool(row[8]) if len(row) > 8 else False,
                'like_romantically': bool(row[9]) if len(row) > 9 else False,
                'created_at': row[10] if len(row) > 10 else '',
                'updated_at': row[11] if len(row) > 11 else ''
            }
            contacts.append(contact)
        
        conn.close()
        return contacts
    
    def get_contact_by_id(self, contact_id: int) -> Optional[Dict]:
        """Get a specific contact by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
        row = cursor.fetchone()
        
        if row:
            # Get column names to handle different schema versions
            cursor.execute("PRAGMA table_info(contacts)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Safe JSON parsing with error handling
            try:
                social_media = json.loads(row[5]) if row[5] else {}
            except (json.JSONDecodeError, TypeError):
                social_media = {}
            
            try:
                tags = json.loads(row[6]) if row[6] else []
            except (json.JSONDecodeError, TypeError):
                tags = []
            
            contact = {
                'id': row[0],
                'name': row[1],
                'nickname': row[2],
                'birthday': row[3],
                'personality_notes': row[4],
                'social_media': social_media,
                'tags': tags,
            }
            
            # Handle address field with backward compatibility
            if 'address' in columns:
                address_index = columns.index('address')
                contact['address'] = row[address_index] if len(row) > address_index else ''
            else:
                contact['address'] = ''
            
            # Handle new columns with backward compatibility
            if 'like_as_friend' in columns:
                friend_index = columns.index('like_as_friend')
                contact['like_as_friend'] = bool(row[friend_index]) if len(row) > friend_index else False
            else:
                contact['like_as_friend'] = False
                
            if 'like_romantically' in columns:
                romantic_index = columns.index('like_romantically')
                contact['like_romantically'] = bool(row[romantic_index]) if len(row) > romantic_index else False
            else:
                contact['like_romantically'] = False
            
            # Handle created_at and updated_at with backward compatibility
            if 'created_at' in columns:
                created_index = columns.index('created_at')
                contact['created_at'] = row[created_index] if len(row) > created_index else ''
            else:
                contact['created_at'] = ''
                
            if 'updated_at' in columns:
                updated_index = columns.index('updated_at')
                contact['updated_at'] = row[updated_index] if len(row) > updated_index else ''
            else:
                contact['updated_at'] = ''
            
            conn.close()
            return contact
        
        conn.close()
        return None
    
    def update_contact(self, contact_id: int, name: str = None, nickname: str = None,
                      birthday: str = None, address: str = None, personality_notes: str = None,
                      social_media: dict = None, tags: List[str] = None,
                      like_as_friend: bool = None, like_romantically: bool = None) -> bool:
        """Update an existing contact."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # First, get the current contact
        current = self.get_contact_by_id(contact_id)
        if not current:
            conn.close()
            return False
        
        # Update only provided fields
        updated_name = name if name is not None else current['name']
        updated_nickname = nickname if nickname is not None else current['nickname']
        updated_birthday = birthday if birthday is not None else current['birthday']
        updated_address = address if address is not None else current.get('address', '')
        updated_personality = personality_notes if personality_notes is not None else current['personality_notes']
        updated_social = social_media if social_media is not None else current['social_media']
        updated_tags = tags if tags is not None else current['tags']
        updated_friend = like_as_friend if like_as_friend is not None else current.get('like_as_friend', False)
        updated_romantic = like_romantically if like_romantically is not None else current.get('like_romantically', False)
        
        cursor.execute('''
            UPDATE contacts 
            SET name = ?, nickname = ?, birthday = ?, address = ?, personality_notes = ?, 
                social_media = ?, tags = ?, like_as_friend = ?, like_romantically = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (updated_name, updated_nickname, updated_birthday, updated_address, updated_personality,
              json.dumps(updated_social), json.dumps(updated_tags), updated_friend, updated_romantic, contact_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_contact(self, contact_id: int) -> bool:
        """Delete a contact by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    def search_contacts(self, query: str) -> List[Dict]:
        """Search contacts by name, nickname, or tags."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Search in name, nickname, and tags
        cursor.execute('''
            SELECT * FROM contacts 
            WHERE name LIKE ? OR nickname LIKE ? OR tags LIKE ?
            ORDER BY name
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        rows = cursor.fetchall()
        contacts = []
        for row in rows:
            # Safe JSON parsing with error handling
            try:
                social_media = json.loads(row[6]) if len(row) > 6 and row[6] else {}
            except (json.JSONDecodeError, TypeError):
                social_media = {}
            
            try:
                tags = json.loads(row[7]) if len(row) > 7 and row[7] else []
            except (json.JSONDecodeError, TypeError):
                tags = []
            
            contact = {
                'id': row[0],
                'name': row[1],
                'nickname': row[2],
                'birthday': row[3],
                'address': row[4] if len(row) > 4 else '',
                'personality_notes': row[5] if len(row) > 5 else '',
                'social_media': social_media,
                'tags': tags,
                'like_as_friend': bool(row[8]) if len(row) > 8 else False,
                'like_romantically': bool(row[9]) if len(row) > 9 else False,
                'created_at': row[10] if len(row) > 10 else '',
                'updated_at': row[11] if len(row) > 11 else ''
            }
            contacts.append(contact)
        
        conn.close()
        return contacts
    
    def filter_by_tag(self, tag: str) -> List[Dict]:
        """Filter contacts by a specific tag."""
        all_contacts = self.get_all_contacts()
        filtered = []
        
        for contact in all_contacts:
            if tag.lower() in [t.lower() for t in contact['tags']]:
                filtered.append(contact)
        
        return filtered
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export all contacts to CSV format."""
        contacts = self.get_all_contacts()
        
        if not filename:
            filename = f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Flatten the data for CSV export
        csv_data = []
        for contact in contacts:
            row = {
                'ID': contact['id'],
                'Name': contact['name'],
                'Nickname': contact['nickname'],
                'Birthday': contact['birthday'],
                'Address': contact.get('address', ''),
                'Personality Notes': contact['personality_notes'],
                'Social Media': json.dumps(contact['social_media']),
                'Tags': ', '.join(contact['tags']),
                'Like as Friend': 'Yes' if contact.get('like_as_friend') else 'No',
                'Like Romantically': 'Yes' if contact.get('like_romantically') else 'No',
                'Created At': contact['created_at'],
                'Updated At': contact['updated_at']
            }
            csv_data.append(row)
        
        # Write to CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            if csv_data:
                writer = csv.DictWriter(csvfile, fieldnames=csv_data[0].keys())
                writer.writeheader()
                writer.writerows(csv_data)
        
        return filename
    
    def get_all_tags(self) -> List[str]:
        """Get all unique tags from all contacts."""
        contacts = self.get_all_contacts()
        all_tags = set()
        
        for contact in contacts:
            all_tags.update(contact['tags'])
        
        return sorted(list(all_tags))
