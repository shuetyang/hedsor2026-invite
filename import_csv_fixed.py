#!/usr/bin/env python3
"""
Fixed script to properly import CSV records into the wedding RSVP database
"""

from datetime import datetime
from app import app, db, Guest

def import_csv_to_db():
    """Import CSV records manually to handle multi-line entries properly"""
    with app.app_context():
        try:
            # Clear existing records first
            Guest.query.delete()
            db.session.commit()
            print("Cleared existing records")
            
            # Manually define the correct data based on the CSV
            guests_data = [
                {
                    'name': 'Chia Kiah Ni',
                    'email': 'kiahni1212@gmail.com',
                    'partner_name': 'Si Min Hau',
                    'has_partner': 'yes',
                    'wedding_attendance': 'attending',
                    'welcome_lunch': 'attending',
                    'farewell_lunch': 'attending',
                    'accommodation': 'yes',
                    'message': '',
                    'created_at': datetime.strptime('2025-09-10 15:19', '%Y-%m-%d %H:%M')
                },
                {
                    'name': 'YitKwang Hang',
                    'email': 'elvinhang@gmail.com',
                    'partner_name': 'Stacy Lin',
                    'has_partner': 'yes',
                    'wedding_attendance': 'attending',
                    'welcome_lunch': 'attending',
                    'farewell_lunch': 'attending',
                    'accommodation': 'yes',
                    'message': 'Cheers to both of my best friend. Thanks for giving me the chance to look at this cutest pair from teenage couple to life partner. Remind us how the purest love can give courage and determination. Do get drunk that day Shuet. Like what we did when we graduated hahah',
                    'created_at': datetime.strptime('2025-09-10 13:52', '%Y-%m-%d %H:%M')
                },
                {
                    'name': 'NG SHYUE LE',
                    'email': 'shyuele19940523@hotmail.com',
                    'partner_name': 'Zoey',
                    'has_partner': 'yes',
                    'wedding_attendance': 'attending',
                    'welcome_lunch': 'attending',
                    'farewell_lunch': 'attending',
                    'accommodation': 'yes',
                    'message': 'I love you two ❤️❤️',
                    'created_at': datetime.strptime('2025-09-10 13:26', '%Y-%m-%d %H:%M')
                },
                {
                    'name': 'Louis',
                    'email': 'ng_weeping@hotmail.com',
                    'partner_name': 'Yuli',
                    'has_partner': 'yes',
                    'wedding_attendance': 'attending',
                    'welcome_lunch': 'attending',
                    'farewell_lunch': 'attending',
                    'accommodation': 'yes',
                    'message': 'Fantastic background music choice, got a emotional just listening to this hahaha\nCongratulation to you two love bird, can\'t wait to celebrate your big day!!',
                    'created_at': datetime.strptime('2025-09-10 11:25', '%Y-%m-%d %H:%M')
                }
            ]
            
            for guest_data in guests_data:
                guest = Guest(
                    name=guest_data['name'],
                    email=guest_data['email'],
                    has_partner=guest_data['has_partner'],
                    partner_name=guest_data['partner_name'] if guest_data['partner_name'] else None,
                    message=guest_data['message'] if guest_data['message'] else None,
                    created_at=guest_data['created_at'],
                    wedding_attendance=guest_data['wedding_attendance'],
                    welcome_lunch=guest_data['welcome_lunch'],
                    farewell_lunch=guest_data['farewell_lunch'],
                    accommodation=guest_data['accommodation']
                )
                
                db.session.add(guest)
                print(f"Added guest: {guest_data['name']} ({guest_data['email']}) + {guest_data['partner_name']}")
            
            db.session.commit()
            print("CSV import completed successfully!")
            
            total_guests = Guest.query.count()
            print(f"Total guests in database: {total_guests}")
            
        except Exception as e:
            print(f"Error importing CSV: {e}")
            db.session.rollback()
            return False
    
    return True

if __name__ == "__main__":
    print("Importing records with proper data parsing...")
    success = import_csv_to_db()
    if success:
        print("Import completed successfully!")
    else:
        print("Import failed!")
