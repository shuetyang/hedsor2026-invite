#!/usr/bin/env python3
"""
Script to clear all records from the wedding RSVP database
"""

from app import app, db, Guest
import os

def clear_database():
    """Delete all guest records from the database"""
    with app.app_context():
        try:
            # Get count before deletion
            count = Guest.query.count()
            print(f"Found {count} guest records in database")
            
            if count > 0:
                # Delete all records
                Guest.query.delete()
                db.session.commit()
                print(f"Successfully deleted {count} guest records")
            else:
                print("Database is already empty")
                
        except Exception as e:
            print(f"Error clearing database: {e}")
            db.session.rollback()
            return False
            
    return True

if __name__ == "__main__":
    print("Clearing wedding RSVP database...")
    success = clear_database()
    if success:
        print("Database cleared successfully!")
    else:
        print("Failed to clear database")
