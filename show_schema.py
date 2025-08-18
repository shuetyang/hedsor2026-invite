#!/usr/bin/env python3
"""
Database Schema Display Script
Shows the current structure of the Guest table
"""

from app import app, db, Guest
import sqlite3
import os

def show_schema():
    with app.app_context():
        # Get database path
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not os.path.exists(db_path):
            # Try instance folder
            db_path = 'instance/wedding.db'
        
        if os.path.exists(db_path):
            # Connect to SQLite database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get table info
            cursor.execute("PRAGMA table_info(guest)")
            columns = cursor.fetchall()
            
            print("=" * 60)
            print("DATABASE SCHEMA - Guest Table")
            print("=" * 60)
            print(f"{'Column Name':<20} {'Type':<15} {'Nullable':<10} {'Default':<15}")
            print("-" * 60)
            
            for col in columns:
                cid, name, type_name, not_null, default_val, pk = col
                nullable = "NO" if not_null else "YES"
                default = str(default_val) if default_val else "NULL"
                print(f"{name:<20} {type_name:<15} {nullable:<10} {default:<15}")
            
            print("=" * 60)
            print(f"Total columns: {len(columns)}")
            print("=" * 60)
            
            # Show sample data if any exists
            cursor.execute("SELECT COUNT(*) FROM guest")
            count = cursor.fetchone()[0]
            print(f"\nRecords in table: {count}")
            
            if count > 0:
                print("\nSample data (first 3 records):")
                cursor.execute("SELECT * FROM guest LIMIT 3")
                sample_data = cursor.fetchall()
                for i, row in enumerate(sample_data, 1):
                    print(f"\nRecord {i}:")
                    for j, col in enumerate(columns):
                        print(f"  {col[1]}: {row[j]}")
            
            conn.close()
        else:
            print(f"Database file not found: {db_path}")

if __name__ == '__main__':
    show_schema()
