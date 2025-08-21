#!/usr/bin/env python3
"""
SendGrid Implementation Script for Crystal & Yang Wedding RSVP System
This script helps you migrate from Resend to SendGrid for email functionality.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_sendgrid_setup():
    """Check if SendGrid is properly configured"""
    print("🔍 Checking SendGrid Configuration...")
    print("=" * 50)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        print("   Create a .env file with your SendGrid configuration")
        return False
    
    # Check SENDGRID_API_KEY
    api_key = os.environ.get('SENDGRID_API_KEY')
    if api_key:
        print(f"✅ SENDGRID_API_KEY found: {api_key[:10]}...")
    else:
        print("❌ SENDGRID_API_KEY not found")
        print("   Add SENDGRID_API_KEY=your_api_key to your .env file")
        return False
    
    # Check FROM_EMAIL
    from_email = os.environ.get('FROM_EMAIL', 'noreply@yourdomain.com')
    print(f"✅ FROM_EMAIL: {from_email}")
    
    return True

def update_app_py():
    """Update app.py to use SendGrid instead of Resend"""
    print("\n📝 Updating app.py for SendGrid...")
    print("=" * 50)
    
    try:
        # Read current app.py
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Check if already using SendGrid
        if 'import sendgrid' in content:
            print("✅ app.py already configured for SendGrid")
            return True
        
        # Replace Resend import with SendGrid
        if 'import resend' in content:
            content = content.replace('import resend', 'import sendgrid\nfrom sendgrid.helpers.mail import Mail')
            print("✅ Replaced Resend import with SendGrid")
        
        # Replace email configuration
        if 'resend.api_key = app_config.RESEND_API_KEY' in content:
            content = content.replace(
                'resend.api_key = app_config.RESEND_API_KEY',
                '# SendGrid configuration is handled in the email function'
            )
            print("✅ Updated email configuration")
        
        # Replace the email sending function
        old_function_start = 'def send_confirmation_email(email, name, guest_names, welcome_lunch, wedding_attendance, accommodation, farewell_lunch):'
        
        if old_function_start in content:
            # Find the start and end of the old function
            start_idx = content.find(old_function_start)
            end_idx = content.find('def ', start_idx + 1)
            if end_idx == -1:
                end_idx = len(content)
            
            # New SendGrid function
            new_function = '''def send_confirmation_email(email, name, guest_names, welcome_lunch, wedding_attendance, accommodation, farewell_lunch):
    """Send confirmation email using SendGrid"""
    try:
        # Validate configuration
        api_key = os.environ.get('SENDGRID_API_KEY')
        from_email = os.environ.get('FROM_EMAIL', 'noreply@yourdomain.com')
        
        if not api_key:
            raise ValueError("SendGrid API key not configured")
        
        # Format guest names
        guest_names_text = ", ".join(guest_names) if len(guest_names) > 1 else guest_names[0]
        
        # Email content
        subject = "Crystal & Yang's Wedding - RSVP Confirmation"
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #333; text-align: center;">🎉 Wedding RSVP Confirmation</h2>
            
            <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p style="font-size: 16px; color: #333;">Dear <strong>{name}</strong>,</p>
                
                <p style="font-size: 16px; color: #333;">Thank you for your RSVP to our wedding celebration!</p>
                
                <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <p style="margin: 0; font-size: 14px; color: #666; font-weight: bold;">Your RSVP Details:</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Guests:</strong> {guest_names_text}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Welcome Lunch (May 10):</strong> {welcome_lunch.replace('_', ' ').title()}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Wedding Day (May 12):</strong> {wedding_attendance.replace('_', ' ').title()}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Accommodation:</strong> {accommodation.title()}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Farewell Lunch (May 13):</strong> {farewell_lunch.replace('_', ' ').title()}</p>
                </div>
                
                <p style="font-size: 16px; color: #333;">We're excited to celebrate with you!</p>
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 14px;">Best regards,</p>
                <p style="color: #333; font-size: 16px; font-weight: bold;">Crystal & Yang</p>
                <p style="color: #666; font-size: 12px;">Hedsor House Wedding - May 12, 2026</p>
            </div>
        </div>
        """
        
        # Send email using SendGrid
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        message = Mail(
            from_email=from_email,
            to_emails=email,
            subject=subject,
            html_content=html_content
        )
        
        response = sg.send(message)
        print(f"Email sent successfully to {email}")
        return response
        
    except Exception as e:
        print(f"Error sending email to {email}: {e}")
        raise e
'''
            
            # Replace the old function with the new one
            content = content[:start_idx] + new_function + content[end_idx:]
            print("✅ Replaced email sending function with SendGrid implementation")
        
        # Write the updated content back
        with open('app.py', 'w') as f:
            f.write(content)
        
        print("✅ app.py updated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating app.py: {e}")
        return False

def update_requirements():
    """Update requirements.txt to include SendGrid"""
    print("\n📦 Updating requirements.txt...")
    print("=" * 50)
    
    try:
        # Read current requirements
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        # Check if SendGrid is already included
        if 'sendgrid' in content:
            print("✅ SendGrid already in requirements.txt")
            return True
        
        # Add SendGrid to requirements
        if content.endswith('\n'):
            content += 'sendgrid==6.10.0\n'
        else:
            content += '\nsendgrid==6.10.0\n'
        
        # Write back
        with open('requirements.txt', 'w') as f:
            f.write(content)
        
        print("✅ Added SendGrid to requirements.txt")
        return True
        
    except Exception as e:
        print(f"❌ Error updating requirements.txt: {e}")
        return False

def update_config():
    """Update config.py to use SendGrid configuration"""
    print("\n⚙️  Updating config.py...")
    print("=" * 50)
    
    try:
        # Read current config
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Check if already using SendGrid config
        if 'SENDGRID_API_KEY' in content:
            print("✅ config.py already configured for SendGrid")
            return True
        
        # Replace Resend config with SendGrid
        if 'RESEND_API_KEY' in content:
            content = content.replace('RESEND_API_KEY', 'SENDGRID_API_KEY')
            print("✅ Updated API key configuration")
        
        # Write back
        with open('config.py', 'w') as f:
            f.write(content)
        
        print("✅ config.py updated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config.py: {e}")
        return False

def create_env_template():
    """Create a template .env file for SendGrid"""
    print("\n📄 Creating .env template...")
    print("=" * 50)
    
    env_content = """# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=production

# Database Configuration
DATABASE_URL=sqlite:///wedding.db

# SendGrid Email Configuration
SENDGRID_API_KEY=your_sendgrid_api_key_here
FROM_EMAIL=noreply@yourdomain.com

# Optional: Custom domain
CUSTOM_DOMAIN=yourwedding.tk
"""
    
    try:
        with open('.env.template', 'w') as f:
            f.write(env_content)
        print("✅ Created .env.template file")
        print("   Copy this to .env and add your SendGrid API key")
        return True
    except Exception as e:
        print(f"❌ Error creating .env template: {e}")
        return False

def main():
    """Main implementation function"""
    print("🚀 SendGrid Implementation for Crystal & Yang Wedding RSVP System")
    print("=" * 70)
    
    print("\n📋 This script will help you migrate from Resend to SendGrid.")
    print("   SendGrid offers better free tier and no sandbox restrictions.")
    
    # Check current setup
    config_ok = check_sendgrid_setup()
    
    if not config_ok:
        print("\n❌ SendGrid configuration incomplete.")
        print("\n📝 To set up SendGrid:")
        print("1. Sign up at https://sendgrid.com (free)")
        print("2. Get your API key from Settings → API Keys")
        print("3. Create a .env file with SENDGRID_API_KEY=your_key")
        print("4. Run this script again")
        return
    
    # Update files
    print("\n" + "=" * 70)
    proceed = input("Proceed with updating files? (y/n): ").strip().lower()
    
    if proceed not in ['y', 'yes']:
        print("❌ Cancelled by user")
        return
    
    # Update all files
    success = True
    success &= update_app_py()
    success &= update_requirements()
    success &= update_config()
    success &= create_env_template()
    
    if success:
        print("\n🎉 SendGrid implementation completed successfully!")
        print("\n📝 Next steps:")
        print("1. Install SendGrid: pip install sendgrid==6.10.0")
        print("2. Update your .env file with your SendGrid API key")
        print("3. Test the email functionality")
        print("4. You can now send emails to any address (no sandbox restrictions!)")
    else:
        print("\n❌ Some updates failed. Please check the errors above.")

if __name__ == "__main__":
    main()
