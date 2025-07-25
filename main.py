from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Input, Button, DataTable, TextArea, 
    Static, Label, Select, Collapsible, TabbedContent, TabPane
)
from textual.screen import Screen, ModalScreen
from textual.binding import Binding
from textual import events
from textual.reactive import reactive
from rich.text import Text
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from typing import List, Dict, Optional
import json

from database import ContactDatabase

class ContactFormScreen(ModalScreen):
    """Modal screen for adding or editing contacts."""
    
    def __init__(self, contact_data: Dict = None, edit_mode: bool = False):
        super().__init__()
        self.contact_data = contact_data or {}
        self.edit_mode = edit_mode
        
    def compose(self) -> ComposeResult:
        title = "Edit Contact" if self.edit_mode else "Add New Contact"
        
        with Container(classes="contact-form"):
            yield Static(title, classes="form-title")
            
            with Vertical():
                yield Label("Name *")
                yield Input(
                    placeholder="Enter full name",
                    value=self.contact_data.get('name', ''),
                    id="name_input"
                )
                
                yield Label("Nickname")
                yield Input(
                    placeholder="Enter nickname",
                    value=self.contact_data.get('nickname', ''),
                    id="nickname_input"
                )
                
                yield Label("Birthday (YYYY-MM-DD)")
                yield Input(
                    placeholder="2000-01-15",
                    value=self.contact_data.get('birthday', ''),
                    id="birthday_input"
                )
                
                yield Label("Personality Notes")
                yield TextArea(
                    text=self.contact_data.get('personality_notes', ''),
                    id="notes_textarea"
                )
                
                yield Label("Social Media (JSON format)")
                social_media = self.contact_data.get('social_media', {})
                yield TextArea(
                    text=json.dumps(social_media, indent=2) if social_media else '{}',
                    id="social_textarea"
                )
                
                yield Label("Tags (comma-separated)")
                tags = ', '.join(self.contact_data.get('tags', []))
                yield Input(
                    placeholder="friend, work, family",
                    value=tags,
                    id="tags_input"
                )
                
                with Horizontal():
                    yield Button("Save", variant="primary", id="save_btn")
                    yield Button("Cancel", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            self.save_contact()
        elif event.button.id == "cancel_btn":
            self.dismiss(None)
    
    def save_contact(self):
        """Collect form data and save contact."""
        try:
            name = self.query_one("#name_input", Input).value.strip()
            if not name:
                self.notify("Name is required!", severity="error")
                return
            
            nickname = self.query_one("#nickname_input", Input).value.strip()
            birthday = self.query_one("#birthday_input", Input).value.strip()
            notes = self.query_one("#notes_textarea", TextArea).text.strip()
            
            # Parse social media JSON
            social_text = self.query_one("#social_textarea", TextArea).text.strip()
            try:
                social_media = json.loads(social_text) if social_text else {}
            except json.JSONDecodeError:
                self.notify("Invalid JSON format for social media!", severity="error")
                return
            
            # Parse tags
            tags_text = self.query_one("#tags_input", Input).value.strip()
            tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
            
            contact_data = {
                'name': name,
                'nickname': nickname,
                'birthday': birthday,
                'personality_notes': notes,
                'social_media': social_media,
                'tags': tags
            }
            
            if self.edit_mode:
                contact_data['id'] = self.contact_data['id']
            
            self.dismiss(contact_data)
            
        except Exception as e:
            self.notify(f"Error saving contact: {str(e)}", severity="error")

class ContactDetailScreen(ModalScreen):
    """Modal screen for viewing contact details."""
    
    def __init__(self, contact: Dict):
        super().__init__()
        self.contact = contact
        
    def compose(self) -> ComposeResult:
        with Container(classes="contact-detail"):
            yield Static(f"Contact Details: {self.contact.get('name', 'Unknown')}", classes="detail-title")
            
            with ScrollableContainer():
                # Create a rich table for better formatting
                console = Console()
                
                # Basic info section
                yield Static("📋 Basic Information", classes="section-header")
                yield Static(f"Name: {self.contact.get('name', 'N/A')}")
                yield Static(f"Nickname: {self.contact.get('nickname', 'N/A')}")
                yield Static(f"Birthday: {self.contact.get('birthday', 'N/A')}")
                
                yield Static("")  # Spacer
                
                # Notes section
                if self.contact.get('personality_notes'):
                    yield Static("💭 Personality Notes", classes="section-header")
                    yield Static(self.contact['personality_notes'])
                    yield Static("")  # Spacer
                
                # Social media section
                if self.contact.get('social_media'):
                    yield Static("🌐 Social Media", classes="section-header")
                    for platform, handle in self.contact['social_media'].items():
                        yield Static(f"{platform}: {handle}")
                    yield Static("")  # Spacer
                
                # Tags section
                if self.contact.get('tags'):
                    yield Static("🏷️ Tags", classes="section-header")
                    tags_text = self.format_tags(self.contact['tags'])
                    yield Static(tags_text)
                    yield Static("")  # Spacer
                
                # Metadata
                yield Static("ℹ️ Metadata", classes="section-header")
                yield Static(f"Created: {self.contact.get('created_at', 'N/A')}")
                yield Static(f"Updated: {self.contact.get('updated_at', 'N/A')}")
            
            with Horizontal():
                yield Button("Edit", variant="primary", id="edit_btn")
                yield Button("Delete", variant="error", id="delete_btn")
                yield Button("Close", variant="default", id="close_btn")
    
    def format_tags(self, tags: List[str]) -> str:
        """Format tags with colors."""
        if not tags:
            return "No tags"
        
        # Simple color coding - in practice, you might want more sophisticated coloring
        colors = ["red", "blue", "green", "yellow", "magenta", "cyan"]
        colored_tags = []
        
        for i, tag in enumerate(tags):
            color = colors[i % len(colors)]
            colored_tags.append(f"[{color}]{tag}[/{color}]")
        
        return " ".join(colored_tags)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "edit_btn":
            self.dismiss({"action": "edit", "contact": self.contact})
        elif event.button.id == "delete_btn":
            self.dismiss({"action": "delete", "contact": self.contact})
        elif event.button.id == "close_btn":
            self.dismiss(None)

class ContactManagerApp(App):
    """Main TUI application for The People DB."""
    
    CSS = """
    .contact-form {
        width: 80%;
        height: 80%;
        margin: 1 1;
        padding: 1;
        border: solid $primary;
        background: $surface;
    }
    
    .contact-detail {
        width: 80%;
        height: 80%;
        margin: 1 1;
        padding: 1;
        border: solid $primary;
        background: $surface;
    }
    
    .form-title, .detail-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
        color: $primary;
    }
    
    .section-header {
        text-style: bold;
        color: $accent;
        margin-top: 1;
    }
    
    .search-bar {
        margin: 1;
    }
    
    .stats-panel {
        height: 5;
        margin: 1;
        padding: 1;
        border: solid $secondary;
    }
    """
    
    BINDINGS = [
        Binding("a", "add_contact", "Add Contact"),
        Binding("s", "search", "Search"),
        Binding("e", "export", "Export CSV"),
        Binding("r", "refresh", "Refresh"),
        Binding("q", "quit", "Quit"),
        Binding("?", "help", "Help"),
    ]
    
    def __init__(self):
        super().__init__()
        self.db = ContactDatabase()
        self.contacts = []
        self.filtered_contacts = []
        self.current_search = ""
        
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container():
            # Search bar
            with Horizontal(classes="search-bar"):
                yield Input(placeholder="Search contacts by name or tag...", id="search_input")
                yield Button("Search", id="search_btn")
                yield Button("Clear", id="clear_btn")
                yield Button("Filter by Tag", id="tag_filter_btn")
            
            # Stats panel
            yield Static("", id="stats_panel", classes="stats-panel")
            
            # Main content area with tabs
            with TabbedContent():
                with TabPane("Contacts", id="contacts_tab"):
                    yield DataTable(id="contacts_table")
                
                with TabPane("All Tags", id="tags_tab"):
                    yield DataTable(id="tags_table")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the app when mounted."""
        self.refresh_contacts()
        self.setup_contacts_table()
        self.setup_tags_table()
        self.update_stats()
    
    def setup_contacts_table(self):
        """Set up the contacts data table."""
        table = self.query_one("#contacts_table", DataTable)
        table.add_columns("ID", "Name", "Nickname", "Birthday", "Tags")
        table.cursor_type = "row"
        self.populate_contacts_table()
    
    def setup_tags_table(self):
        """Set up the tags data table."""
        table = self.query_one("#tags_table", DataTable)
        table.add_columns("Tag", "Count")
        table.cursor_type = "row"
        self.populate_tags_table()
    
    def populate_contacts_table(self):
        """Populate the contacts table with current data."""
        table = self.query_one("#contacts_table", DataTable)
        table.clear()
        
        contacts_to_show = self.filtered_contacts if self.current_search else self.contacts
        
        for contact in contacts_to_show:
            tags_str = ", ".join(contact.get('tags', []))
            table.add_row(
                str(contact.get('id', '')),
                contact.get('name', ''),
                contact.get('nickname', ''),
                contact.get('birthday', ''),
                tags_str,
                key=contact.get('id')
            )
    
    def populate_tags_table(self):
        """Populate the tags table with tag statistics."""
        table = self.query_one("#tags_table", DataTable)
        table.clear()
        
        all_tags = self.db.get_all_tags()
        tag_counts = {}
        
        for contact in self.contacts:
            for tag in contact.get('tags', []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        for tag in sorted(tag_counts.keys()):
            count = tag_counts[tag]
            table.add_row(tag, str(count), key=tag)
    
    def refresh_contacts(self):
        """Refresh contacts from database."""
        self.contacts = self.db.get_all_contacts()
        self.filtered_contacts = []
        self.current_search = ""
    
    def update_stats(self):
        """Update the statistics panel."""
        stats_panel = self.query_one("#stats_panel", Static)
        total_contacts = len(self.contacts)
        total_tags = len(self.db.get_all_tags())
        
        if self.current_search:
            showing = len(self.filtered_contacts)
            stats_text = f"📊 Showing {showing}/{total_contacts} contacts | {total_tags} unique tags | Search: '{self.current_search}'"
        else:
            stats_text = f"📊 Total contacts: {total_contacts} | Unique tags: {total_tags}"
        
        stats_panel.update(stats_text)
    
    def action_add_contact(self):
        """Show the add contact form."""
        def handle_result(result):
            if result:
                try:
                    self.db.add_contact(
                        name=result['name'],
                        nickname=result['nickname'],
                        birthday=result['birthday'],
                        personality_notes=result['personality_notes'],
                        social_media=result['social_media'],
                        tags=result['tags']
                    )
                    self.refresh_contacts()
                    self.populate_contacts_table()
                    self.populate_tags_table()
                    self.update_stats()
                    self.notify(f"Contact '{result['name']}' added successfully!", severity="success")
                except Exception as e:
                    self.notify(f"Error adding contact: {str(e)}", severity="error")
        
        self.push_screen(ContactFormScreen(), handle_result)
    
    def action_search(self):
        """Focus on the search input."""
        search_input = self.query_one("#search_input", Input)
        search_input.focus()
    
    def action_export(self):
        """Export contacts to CSV."""
        try:
            filename = self.db.export_to_csv()
            self.notify(f"Contacts exported to {filename}", severity="success")
        except Exception as e:
            self.notify(f"Error exporting: {str(e)}", severity="error")
    
    def action_refresh(self):
        """Refresh the contacts list."""
        self.refresh_contacts()
        self.populate_contacts_table()
        self.populate_tags_table()
        self.update_stats()
        self.notify("Contacts refreshed!", severity="info")
    
    def action_help(self):
        """Show help information."""
        help_text = """
        🔧 The People DB Help
        
        Keyboard Shortcuts:
        • A - Add new contact
        • S - Focus search bar
        • E - Export to CSV
        • R - Refresh contacts
        • Q - Quit application
        • ? - Show this help
        
        Table Navigation:
        • Arrow keys - Navigate
        • Enter - View contact details
        
        Search:
        • Type in search bar to filter by name/tag
        • Use "Filter by Tag" for tag-specific filtering
        """
        self.notify(help_text, timeout=10)
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle search input submission."""
        if event.input.id == "search_input":
            self.perform_search(event.value)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "search_btn":
            search_input = self.query_one("#search_input", Input)
            self.perform_search(search_input.value)
        elif event.button.id == "clear_btn":
            self.clear_search()
        elif event.button.id == "tag_filter_btn":
            self.show_tag_filter()
    
    def perform_search(self, query: str):
        """Perform search and update the table."""
        if not query.strip():
            self.clear_search()
            return
        
        self.current_search = query.strip()
        self.filtered_contacts = self.db.search_contacts(query.strip())
        self.populate_contacts_table()
        self.update_stats()
    
    def clear_search(self):
        """Clear the current search."""
        search_input = self.query_one("#search_input", Input)
        search_input.value = ""
        self.current_search = ""
        self.filtered_contacts = []
        self.populate_contacts_table()
        self.update_stats()
    
    def show_tag_filter(self):
        """Show tag filtering options."""
        # For simplicity, this could be enhanced with a proper tag selection modal
        self.notify("Tag filtering: Use search with tag names for now", severity="info")
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection in data tables."""
        if event.data_table.id == "contacts_table":
            contact_id = event.row_key
            contact = self.db.get_contact_by_id(contact_id)
            if contact:
                self.show_contact_detail(contact)
        elif event.data_table.id == "tags_table":
            tag = event.row_key
            self.perform_search(tag)
    
    def show_contact_detail(self, contact: Dict):
        """Show contact detail modal."""
        def handle_result(result):
            if result:
                if result.get("action") == "edit":
                    self.edit_contact(result["contact"])
                elif result.get("action") == "delete":
                    self.delete_contact(result["contact"])
        
        self.push_screen(ContactDetailScreen(contact), handle_result)
    
    def edit_contact(self, contact: Dict):
        """Show edit contact form."""
        def handle_result(result):
            if result:
                try:
                    success = self.db.update_contact(
                        contact_id=result['id'],
                        name=result['name'],
                        nickname=result['nickname'],
                        birthday=result['birthday'],
                        personality_notes=result['personality_notes'],
                        social_media=result['social_media'],
                        tags=result['tags']
                    )
                    if success:
                        self.refresh_contacts()
                        self.populate_contacts_table()
                        self.populate_tags_table()
                        self.update_stats()
                        self.notify(f"Contact '{result['name']}' updated successfully!", severity="success")
                    else:
                        self.notify("Failed to update contact", severity="error")
                except Exception as e:
                    self.notify(f"Error updating contact: {str(e)}", severity="error")
        
        self.push_screen(ContactFormScreen(contact, edit_mode=True), handle_result)
    
    def delete_contact(self, contact: Dict):
        """Delete a contact after confirmation."""
        # In a more sophisticated app, you'd show a confirmation dialog
        try:
            success = self.db.delete_contact(contact['id'])
            if success:
                self.refresh_contacts()
                self.populate_contacts_table()
                self.populate_tags_table()
                self.update_stats()
                self.notify(f"Contact '{contact['name']}' deleted successfully!", severity="success")
            else:
                self.notify("Failed to delete contact", severity="error")
        except Exception as e:
            self.notify(f"Error deleting contact: {str(e)}", severity="error")

def main():
    """Main entry point."""
    app = ContactManagerApp()
    app.run()

if __name__ == "__main__":
    main()
