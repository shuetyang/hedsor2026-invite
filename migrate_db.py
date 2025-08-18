#!/usr/bin/env python3
"""
Database Migration Script for Wedding RSVP System
This script updates the existing database to the new schema.
"""

from app import app, db, Guest
import json

def migrate_database():
    with app.app_context():
        # Drop existing table and recreate with new schema
        print("Dropping existing Guest table...")
        db.drop_all()
        
        print("Creating new Guest table with updated schema...")
        db.create_all()
        
        print("Database migration completed successfully!")
        print("\nNew schema includes:")
        print("- Primary contact information (name, email)")
        print("- Guest count and guest names (JSON)")
        print("- Welcome Lunch attendance")
        print("- Wedding Day attendance")
        print("- Accommodation preference (default: Yes)")
        print("- Farewell Lunch attendance")
        print("- Optional message")

if __name__ == '__main__':
    migrate_database()
