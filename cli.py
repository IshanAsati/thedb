#!/usr/bin/env python3
"""
Simple CLI interface for The People DB
This is a fallback interface that works without the textual library
"""

import json
import sys
from database import ContactDatabase

class SimpleContactCLI:
    def __init__(self):
        self.db = ContactDatabase()
    
    def display_menu(self):
        print("\n" + "="*50)
        print("📞 THE PEOPLE DB")
        print("="*50)
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contacts")
        print("4. Edit Contact")
        print("5. Delete Contact")
        print("6. Filter by Tag")
        print("7. View All Tags")
        print("8. Export to CSV")
        print("9. Quit")
        print("="*50)
    
    def add_contact(self):
        print("\n📝 ADD NEW CONTACT")
        print("-" * 30)
        
        name = input("Name * (required): ").strip()
        if not name:
            print("❌ Name is required!")
            return
        
        nickname = input("Nickname: ").strip()
        birthday = input("Birthday (YYYY-MM-DD): ").strip()
        personality_notes = input("Personality notes: ").strip()
        
        # Social media
        print("\nSocial Media Links:")
        print("Enter platform and handle (press Enter to skip)")
        social_media = {}
        while True:
            platform = input("Platform (or press Enter to finish): ").strip()
            if not platform:
                break
            handle = input(f"{platform} handle: ").strip()
            if handle:
                social_media[platform] = handle
        
        # Tags
        tags_input = input("Tags (comma-separated): ").strip()
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        
        try:
            contact_id = self.db.add_contact(
                name=name,
                nickname=nickname,
                birthday=birthday,
                personality_notes=personality_notes,
                social_media=social_media,
                tags=tags
            )
            print(f"✅ Contact '{name}' added successfully! (ID: {contact_id})")
        except Exception as e:
            print(f"❌ Error adding contact: {e}")
    
    def view_all_contacts(self):
        contacts = self.db.get_all_contacts()
        if not contacts:
            print("\n📭 No contacts found.")
            return
        
        print(f"\n📋 ALL CONTACTS ({len(contacts)} total)")
        print("=" * 80)
        
        for contact in contacts:
            self.display_contact_summary(contact)
            print("-" * 80)
    
    def display_contact_summary(self, contact):
        """Display a contact in a formatted way with color-coded tags."""
        print(f"ID: {contact['id']} | Name: {contact['name']}")
        if contact.get('nickname'):
            print(f"Nickname: {contact['nickname']}")
        if contact.get('birthday'):
            print(f"🎂 Birthday: {contact['birthday']}")
        
        if contact.get('tags'):
            # Color-code tags (simple ANSI colors)
            colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']  # Red, Green, Yellow, Blue, Magenta, Cyan
            reset = '\033[0m'
            
            colored_tags = []
            for i, tag in enumerate(contact['tags']):
                color = colors[i % len(colors)]
                colored_tags.append(f"{color}#{tag}{reset}")
            
            print(f"🏷️  Tags: {' '.join(colored_tags)}")
        
        if contact.get('personality_notes'):
            notes = contact['personality_notes']
            if len(notes) > 60:
                notes = notes[:60] + "..."
            print(f"💭 Notes: {notes}")
    
    def search_contacts(self):
        query = input("\n🔍 Enter search term (name, nickname, or tag): ").strip()
        if not query:
            print("❌ Please enter a search term.")
            return
        
        contacts = self.db.search_contacts(query)
        if not contacts:
            print(f"📭 No contacts found matching '{query}'.")
            return
        
        print(f"\n🔍 SEARCH RESULTS for '{query}' ({len(contacts)} found)")
        print("=" * 80)
        
        for contact in contacts:
            self.display_contact_summary(contact)
            print("-" * 80)
    
    def edit_contact(self):
        contact_id = input("\n✏️ Enter contact ID to edit: ").strip()
        try:
            contact_id = int(contact_id)
        except ValueError:
            print("❌ Invalid contact ID.")
            return
        
        contact = self.db.get_contact_by_id(contact_id)
        if not contact:
            print(f"❌ Contact with ID {contact_id} not found.")
            return
        
        print(f"\n✏️ EDITING: {contact['name']}")
        print("Leave blank to keep current value:")
        print("-" * 40)
        
        # Show current values and get new ones
        name = input(f"Name [{contact['name']}]: ").strip() or contact['name']
        nickname = input(f"Nickname [{contact.get('nickname', '')}]: ").strip()
        if nickname == '':
            nickname = contact.get('nickname', '')
            
        birthday = input(f"Birthday [{contact.get('birthday', '')}]: ").strip()
        if birthday == '':
            birthday = contact.get('birthday', '')
            
        personality_notes = input(f"Notes [{contact.get('personality_notes', '')[:30]}...]: ").strip()
        if personality_notes == '':
            personality_notes = contact.get('personality_notes', '')
        
        # Tags
        current_tags = ', '.join(contact.get('tags', []))
        tags_input = input(f"Tags [{current_tags}]: ").strip()
        if tags_input == '':
            tags = contact.get('tags', [])
        else:
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        
        try:
            success = self.db.update_contact(
                contact_id=contact_id,
                name=name,
                nickname=nickname,
                birthday=birthday,
                personality_notes=personality_notes,
                tags=tags
            )
            if success:
                print(f"✅ Contact '{name}' updated successfully!")
            else:
                print("❌ Failed to update contact.")
        except Exception as e:
            print(f"❌ Error updating contact: {e}")
    
    def delete_contact(self):
        contact_id = input("\n🗑️ Enter contact ID to delete: ").strip()
        try:
            contact_id = int(contact_id)
        except ValueError:
            print("❌ Invalid contact ID.")
            return
        
        contact = self.db.get_contact_by_id(contact_id)
        if not contact:
            print(f"❌ Contact with ID {contact_id} not found.")
            return
        
        print(f"\n⚠️ Are you sure you want to delete '{contact['name']}'?")
        confirm = input("Type 'yes' to confirm: ").strip().lower()
        
        if confirm == 'yes':
            try:
                success = self.db.delete_contact(contact_id)
                if success:
                    print(f"✅ Contact '{contact['name']}' deleted successfully!")
                else:
                    print("❌ Failed to delete contact.")
            except Exception as e:
                print(f"❌ Error deleting contact: {e}")
        else:
            print("❌ Deletion cancelled.")
    
    def filter_by_tag(self):
        all_tags = self.db.get_all_tags()
        if not all_tags:
            print("\n📭 No tags found.")
            return
        
        print(f"\n🏷️ AVAILABLE TAGS:")
        for i, tag in enumerate(all_tags, 1):
            print(f"{i}. {tag}")
        
        choice = input("\nEnter tag name to filter by: ").strip()
        if not choice:
            return
        
        contacts = self.db.filter_by_tag(choice)
        if not contacts:
            print(f"📭 No contacts found with tag '{choice}'.")
            return
        
        print(f"\n🏷️ CONTACTS WITH TAG '{choice}' ({len(contacts)} found)")
        print("=" * 80)
        
        for contact in contacts:
            self.display_contact_summary(contact)
            print("-" * 80)
    
    def view_all_tags(self):
        all_tags = self.db.get_all_tags()
        if not all_tags:
            print("\n📭 No tags found.")
            return
        
        # Count tag usage
        contacts = self.db.get_all_contacts()
        tag_counts = {}
        for contact in contacts:
            for tag in contact.get('tags', []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        print(f"\n🏷️ ALL TAGS ({len(all_tags)} unique)")
        print("=" * 40)
        
        for tag in sorted(all_tags):
            count = tag_counts.get(tag, 0)
            # Color-code tags
            colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']
            reset = '\033[0m'
            color = colors[hash(tag) % len(colors)]
            print(f"{color}#{tag}{reset} ({count} contacts)")
    
    def export_to_csv(self):
        try:
            filename = self.db.export_to_csv()
            print(f"✅ Contacts exported to: {filename}")
        except Exception as e:
            print(f"❌ Error exporting contacts: {e}")
    
    def run(self):
        """Main application loop."""
        print("🚀 Starting The People DB...")
        
        while True:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (1-9): ").strip()
                
                if choice == '1':
                    self.add_contact()
                elif choice == '2':
                    self.view_all_contacts()
                elif choice == '3':
                    self.search_contacts()
                elif choice == '4':
                    self.edit_contact()
                elif choice == '5':
                    self.delete_contact()
                elif choice == '6':
                    self.filter_by_tag()
                elif choice == '7':
                    self.view_all_tags()
                elif choice == '8':
                    self.export_to_csv()
                elif choice == '9':
                    print("\n👋 Goodbye!")
                    sys.exit(0)
                else:
                    print("❌ Invalid choice. Please enter 1-9.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")

if __name__ == "__main__":
    cli = SimpleContactCLI()
    cli.run()
