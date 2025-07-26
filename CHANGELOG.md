# Changelog

All notable changes to The People DB will be documented in this file.

## [2.0.0] - 2025-01-26

### Added
- **Address Field**: Added address support across all interfaces (Web, TUI, CLI)
- **Database Repair Utility**: New `repair_db.py` for fixing corrupted JSON data
- **Improved Error Handling**: Better JSON parsing with graceful fallbacks
- **Enhanced Documentation**: Updated README with badges and better structure

### Fixed
- **JSON Decode Errors**: Resolved issues with corrupted social media and tags data
- **Database Column Mapping**: Fixed column indexing issues after schema changes
- **Template Rendering**: Fixed template errors related to created_at field formatting

### Changed
- **Database Schema**: Added address column to contacts table
- **Form Validation**: Improved form handling for address field
- **Code Cleanup**: Removed unused imports and improved code organization

## [1.0.0] - 2025-01-25

### Added
- **Multi-Interface Support**: Web, TUI, and CLI interfaces
- **Contact Management**: Full CRUD operations for contacts
- **Relationship Preferences**: Friend and romantic preference tracking
- **Search and Filtering**: Advanced search across multiple fields
- **Data Export**: CSV export functionality
- **Database Migration**: Automatic schema migration system
- **Tag Management**: Color-coded tag system with statistics

### Features
- SQLite database with automatic schema updates
- Bootstrap 5 responsive web interface
- Rich terminal UI with keyboard shortcuts
- Simple CLI interface with no dependencies
- JSON-based social media and tag storage
- Real-time search and filtering
- Comprehensive error handling
