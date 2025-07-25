#!/usr/bin/env python3
"""
Flask Web Application for The People DB
Provides a web interface for managing contacts with Bootstrap UI
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import TextArea
import json
import os
from datetime import datetime
from database import ContactDatabase

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Initialize database
db = ContactDatabase()

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"class": "form-control"})
    nickname = StringField('Nickname', validators=[Optional()], render_kw={"class": "form-control"})
    birthday = StringField('Birthday (YYYY-MM-DD)', validators=[Optional()], render_kw={"class": "form-control", "placeholder": "2000-01-15"})
    personality_notes = TextAreaField('Personality Notes', validators=[Optional()], render_kw={"class": "form-control", "rows": 4})
    social_media = TextAreaField('Social Media (JSON)', validators=[Optional()], render_kw={"class": "form-control", "rows": 3, "placeholder": '{"twitter": "@username", "instagram": "handle"}'})
    tags = StringField('Tags (comma-separated)', validators=[Optional()], render_kw={"class": "form-control", "placeholder": "friend, work, family"})
    like_as_friend = BooleanField('I like this person as a friend', render_kw={"class": "form-check-input"})
    like_romantically = BooleanField('I like this person romantically', render_kw={"class": "form-check-input"})
    submit = SubmitField('Save Contact', render_kw={"class": "btn btn-primary"})

@app.route('/')
def index():
    """Home page showing all contacts"""
    search_query = request.args.get('search', '')
    tag_filter = request.args.get('tag', '')
    
    if search_query:
        contacts = db.search_contacts(search_query)
        title = f"Search Results for '{search_query}'"
    elif tag_filter:
        contacts = db.filter_by_tag(tag_filter)
        title = f"Contacts with tag '{tag_filter}'"
    else:
        contacts = db.get_all_contacts()
        title = "All Contacts"
    
    # Get all tags for the filter dropdown
    all_tags = db.get_all_tags()
    
    # Count statistics
    total_contacts = len(db.get_all_contacts())
    total_tags = len(all_tags)
    
    return render_template('index.html', 
                         contacts=contacts, 
                         title=title,
                         search_query=search_query,
                         tag_filter=tag_filter,
                         all_tags=all_tags,
                         total_contacts=total_contacts,
                         total_tags=total_tags)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    """Add a new contact"""
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            # Parse social media JSON
            social_media = {}
            if form.social_media.data.strip():
                try:
                    social_media = json.loads(form.social_media.data)
                except json.JSONDecodeError:
                    flash('Invalid JSON format for social media', 'error')
                    return render_template('add_contact.html', form=form)
            
            # Parse tags
            tags = []
            if form.tags.data.strip():
                tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
            
            # Add contact to database
            contact_id = db.add_contact(
                name=form.name.data,
                nickname=form.nickname.data,
                birthday=form.birthday.data,
                personality_notes=form.personality_notes.data,
                social_media=social_media,
                tags=tags,
                like_as_friend=form.like_as_friend.data,
                like_romantically=form.like_romantically.data
            )
            
            flash(f'Contact "{form.name.data}" added successfully!', 'success')
            return redirect(url_for('view_contact', contact_id=contact_id))
            
        except Exception as e:
            flash(f'Error adding contact: {str(e)}', 'error')
    
    return render_template('add_contact.html', form=form)

@app.route('/contact/<int:contact_id>')
def view_contact(contact_id):
    """View a specific contact"""
    contact = db.get_contact_by_id(contact_id)
    if not contact:
        flash('Contact not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('view_contact.html', contact=contact)

@app.route('/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    """Edit an existing contact"""
    contact = db.get_contact_by_id(contact_id)
    if not contact:
        flash('Contact not found', 'error')
        return redirect(url_for('index'))
    
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            # Parse social media JSON
            social_media = {}
            if form.social_media.data.strip():
                try:
                    social_media = json.loads(form.social_media.data)
                except json.JSONDecodeError:
                    flash('Invalid JSON format for social media', 'error')
                    return render_template('edit_contact.html', form=form, contact=contact)
            
            # Parse tags
            tags = []
            if form.tags.data.strip():
                tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
            
            # Update contact in database
            success = db.update_contact(
                contact_id=contact_id,
                name=form.name.data,
                nickname=form.nickname.data,
                birthday=form.birthday.data,
                personality_notes=form.personality_notes.data,
                social_media=social_media,
                tags=tags,
                like_as_friend=form.like_as_friend.data,
                like_romantically=form.like_romantically.data
            )
            
            if success:
                flash(f'Contact "{form.name.data}" updated successfully!', 'success')
                return redirect(url_for('view_contact', contact_id=contact_id))
            else:
                flash('Failed to update contact', 'error')
            
        except Exception as e:
            flash(f'Error updating contact: {str(e)}', 'error')
    
    # Pre-populate form with existing data
    if request.method == 'GET':
        form.name.data = contact['name']
        form.nickname.data = contact['nickname']
        form.birthday.data = contact['birthday']
        form.personality_notes.data = contact['personality_notes']
        form.social_media.data = json.dumps(contact['social_media'], indent=2) if contact['social_media'] else ''
        form.tags.data = ', '.join(contact['tags'])
        form.like_as_friend.data = contact.get('like_as_friend', False)
        form.like_romantically.data = contact.get('like_romantically', False)
    
    return render_template('edit_contact.html', form=form, contact=contact)

@app.route('/delete/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    """Delete a contact"""
    contact = db.get_contact_by_id(contact_id)
    if not contact:
        flash('Contact not found', 'error')
        return redirect(url_for('index'))
    
    try:
        success = db.delete_contact(contact_id)
        if success:
            flash(f'Contact "{contact["name"]}" deleted successfully!', 'success')
        else:
            flash('Failed to delete contact', 'error')
    except Exception as e:
        flash(f'Error deleting contact: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/export')
def export_contacts():
    """Export contacts to CSV"""
    try:
        filename = db.export_to_csv()
        return send_file(filename, as_attachment=True, download_name=filename)
    except Exception as e:
        flash(f'Error exporting contacts: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/contacts')
def api_contacts():
    """JSON API endpoint for contacts"""
    search_query = request.args.get('search', '')
    
    if search_query:
        contacts = db.search_contacts(search_query)
    else:
        contacts = db.get_all_contacts()
    
    return jsonify({
        'contacts': contacts,
        'total': len(contacts)
    })

@app.route('/api/tags')
def api_tags():
    """JSON API endpoint for tags"""
    all_tags = db.get_all_tags()
    
    # Count tag usage
    contacts = db.get_all_contacts()
    tag_counts = {}
    for contact in contacts:
        for tag in contact.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    tags_with_counts = [{'tag': tag, 'count': tag_counts.get(tag, 0)} for tag in all_tags]
    
    return jsonify({
        'tags': tags_with_counts,
        'total': len(all_tags)
    })

@app.template_filter('format_social_media')
def format_social_media(social_media):
    """Template filter to format social media links"""
    if not social_media:
        return ""
    
    formatted = []
    for platform, handle in social_media.items():
        if platform.lower() == 'twitter':
            formatted.append(f'<a href="https://twitter.com/{handle.lstrip("@")}" target="_blank" class="text-decoration-none"><i class="fab fa-twitter"></i> {handle}</a>')
        elif platform.lower() == 'instagram':
            formatted.append(f'<a href="https://instagram.com/{handle.lstrip("@")}" target="_blank" class="text-decoration-none"><i class="fab fa-instagram"></i> {handle}</a>')
        elif platform.lower() == 'linkedin':
            formatted.append(f'<a href="https://linkedin.com/in/{handle.lstrip("@")}" target="_blank" class="text-decoration-none"><i class="fab fa-linkedin"></i> {handle}</a>')
        elif platform.lower() == 'github':
            formatted.append(f'<a href="https://github.com/{handle.lstrip("@")}" target="_blank" class="text-decoration-none"><i class="fab fa-github"></i> {handle}</a>')
        else:
            formatted.append(f'<span class="badge bg-secondary me-1">{platform}: {handle}</span>')
    
    return ' '.join(formatted)

@app.template_filter('format_tags')
def format_tags(tags):
    """Template filter to format tags with colors"""
    if not tags:
        return ""
    
    colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']
    formatted_tags = []
    
    for i, tag in enumerate(tags):
        color = colors[i % len(colors)]
        formatted_tags.append(f'<span class="badge bg-{color} me-1">#{tag}</span>')
    
    return ' '.join(formatted_tags)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
