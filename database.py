import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
import csv
import io

class ContactDatabase:
    def __init__(self, db_path: str = "contacts.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with the contacts table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                nickname TEXT,
                birthday TEXT,
                personality_notes TEXT,
                social_media TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_contact(self, name: str, nickname: str = "", birthday: str = "", 
                   personality_notes: str = "", social_media: dict = None, 
                   tags: List[str] = None) -> int:
        """Add a new contact to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        social_media_json = json.dumps(social_media or {})
        tags_json = json.dumps(tags or [])
        
        cursor.execute('''
            INSERT INTO contacts (name, nickname, birthday, personality_notes, social_media, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, nickname, birthday, personality_notes, social_media_json, tags_json))
        
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
            contact = {
                'id': row[0],
                'name': row[1],
                'nickname': row[2],
                'birthday': row[3],
                'personality_notes': row[4],
                'social_media': json.loads(row[5]) if row[5] else {},
                'tags': json.loads(row[6]) if row[6] else [],
                'created_at': row[7],
                'updated_at': row[8]
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
            contact = {
                'id': row[0],
                'name': row[1],
                'nickname': row[2],
                'birthday': row[3],
                'personality_notes': row[4],
                'social_media': json.loads(row[5]) if row[5] else {},
                'tags': json.loads(row[6]) if row[6] else [],
                'created_at': row[7],
                'updated_at': row[8]
            }
            conn.close()
            return contact
        
        conn.close()
        return None
    
    def update_contact(self, contact_id: int, name: str = None, nickname: str = None,
                      birthday: str = None, personality_notes: str = None,
                      social_media: dict = None, tags: List[str] = None) -> bool:
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
        updated_personality = personality_notes if personality_notes is not None else current['personality_notes']
        updated_social = social_media if social_media is not None else current['social_media']
        updated_tags = tags if tags is not None else current['tags']
        
        cursor.execute('''
            UPDATE contacts 
            SET name = ?, nickname = ?, birthday = ?, personality_notes = ?, 
                social_media = ?, tags = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (updated_name, updated_nickname, updated_birthday, updated_personality,
              json.dumps(updated_social), json.dumps(updated_tags), contact_id))
        
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
            contact = {
                'id': row[0],
                'name': row[1],
                'nickname': row[2],
                'birthday': row[3],
                'personality_notes': row[4],
                'social_media': json.loads(row[5]) if row[5] else {},
                'tags': json.loads(row[6]) if row[6] else [],
                'created_at': row[7],
                'updated_at': row[8]
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
                'Personality Notes': contact['personality_notes'],
                'Social Media': json.dumps(contact['social_media']),
                'Tags': ', '.join(contact['tags']),
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
